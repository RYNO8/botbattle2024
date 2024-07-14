"""
handle_claim_territory: aim for south america then branch to north america or africa
handle_place_initial_troop: distribute evenly
handle_distribute_troops: distribute evenly
handle_attack: choose the smallest adjacent territory which has at least 2 more surrounding troops from me
"""

print("V3")

from collections import deque
import random
from typing import Optional, Tuple, Union, cast
from risk_helper.game import Game
from risk_shared.models.territory_model import TerritoryModel
from risk_shared.models.card_model import CardModel
from risk_shared.queries.query_attack import QueryAttack
from risk_shared.queries.query_claim_territory import QueryClaimTerritory
from risk_shared.queries.query_defend import QueryDefend
from risk_shared.queries.query_distribute_troops import QueryDistributeTroops
from risk_shared.queries.query_fortify import QueryFortify
from risk_shared.queries.query_place_initial_troop import QueryPlaceInitialTroop
from risk_shared.queries.query_redeem_cards import QueryRedeemCards
from risk_shared.queries.query_troops_after_attack import QueryTroopsAfterAttack
from risk_shared.queries.query_type import QueryType
from risk_shared.records.moves.move_attack import MoveAttack
from risk_shared.records.moves.move_attack_pass import MoveAttackPass
from risk_shared.records.moves.move_claim_territory import MoveClaimTerritory
from risk_shared.records.moves.move_defend import MoveDefend
from risk_shared.records.moves.move_distribute_troops import MoveDistributeTroops
from risk_shared.records.moves.move_fortify import MoveFortify
from risk_shared.records.moves.move_fortify_pass import MoveFortifyPass
from risk_shared.records.moves.move_place_initial_troop import MovePlaceInitialTroop
from risk_shared.records.moves.move_redeem_cards import MoveRedeemCards
from risk_shared.records.moves.move_troops_after_attack import MoveTroopsAfterAttack
from risk_shared.records.record_attack import RecordAttack
from risk_shared.records.types.move_type import MoveType

_print = print
print = lambda *args, **kwargs: _print(*args, **kwargs, flush=True)

def union(a: list, b: list):
    """does not assume each of a and b have distinct elements"""
    return list(set(a + b))

def intersect(a: list, b: list):
    """does not assume each of a and b have distinct elements"""
    return list(set(a) & set(b))


##############################################################################
################################ STATE #######################################
##############################################################################

# We will store our enemy in the bot state.
class BotState():
    def __init__(self):
        self.enemy: Optional[int] = None

# Get the game object, which will connect you to the engine and
# track the state of the game.
game = Game()
bot_state = BotState()

##############################################################################
############################### HELPERS ######################################
##############################################################################

def find_shortest_path_from_vertex_to_set(source: int, target_set: set[int]) -> list[int]:
    """Used in move_fortify()."""

    # We perform a BFS search from our source vertex, stopping at the first member of the target_set we find.
    queue = deque()
    queue.appendleft(source)

    current = queue.pop()
    parent = {}
    seen = {current: True}

    while len(queue) != 0:
        if current in target_set:
            break

        for neighbour in game.state.map.get_adjacent_to(current):
            if neighbour not in seen:
                seen[neighbour] = True
                parent[neighbour] = current
                queue.appendleft(neighbour)

        current = queue.pop()

    path = []
    while current in parent:
        path.insert(0, current)
        current = parent[current]

    return path

# me
def m_id() -> int:
    return game.state.me.player_id

# troops
def T(t):
    if isinstance(t, int): return game.state.territories[t].troops
    elif isinstance(t, list): return [game.state.territories[x].troops for x in t]
    elif callable(t): return lambda x: T(t(x))
    else: raise TypeError

def O(t):
    if isinstance(t, int): return game.state.territories[t].occupier
    elif isinstance(t, list): return [game.state.territories[x].occupier for x in t]
    elif callable(t): return lambda x: T(t(x))
    else: raise TypeError

def t_ismine(t: int) -> bool:
    return O(t) == game.state.me.player_id

# function
def f_def(t):
    return [x for x in game.state.map.get_adjacent_to(t) if O(x) == O(t)]

def f_empty(t: int) -> list[int]:
    return [x for x in game.state.map.get_adjacent_to(t) if O(x) == None]

def f_opp(t: int) -> list[int]:
    if t_ismine(t):
        return [x for x in game.state.map.get_adjacent_to(t) if O(x) not in [None, m_id()]]
    else:
        return [x for x in game.state.map.get_adjacent_to(t) if O(x) == m_id()]

def f_adj(t: int) -> list[int]:
    return game.state.map.get_adjacent_to(t)

# central
def biggest_bases(owned: list[int]) -> list[list[int]]:
    todo = set(owned)
    bases = []
    while todo:
        t = todo.pop()
        queue = [t]
        i = 0
        while i < len(queue):
            for v in game.state.map.get_adjacent_to(queue[i]):
                if v in todo:
                    todo.remove(v)
                    queue.append(v)
            i += 1
        bases.append(queue)

    # such that bases[0] is biggest, etc.
    bases.sort(key=len, reverse=True)
    return bases

##############################################################################
############################### ACTIONS ######################################
##############################################################################

targets = []
NORTH_AMERICA = [2, 8, 3, 1, 6, 7]
AFRICA = [36, 32, 37, 33, 34, 15]
def handle_claim_territory(query: QueryClaimTerritory) -> MoveClaimTerritory:
    """At the start of the game, you can claim a single unclaimed territory every turn 
    until all the territories have been claimed by players."""

    unclaimed_territories = game.state.get_territories_owned_by(None)

    # aim for roughly south america
    for t in [30, 29]:
        if t in unclaimed_territories:
            return game.move_claim_territory(query, t)

    global targets, NORTH_AMERICA, AFRICA
    if targets == []:
        cnt_NORTH_AMERICA = sum(t in unclaimed_territories for t in NORTH_AMERICA)
        cnt_AFRICA = sum(t in unclaimed_territories for t in AFRICA)
        # print(cnt_NORTH_AMERICA, cnt_AFRICA)
        if cnt_NORTH_AMERICA <= cnt_AFRICA:
            targets = [30, 29, 2, 8, 28, 1, 3]
        else:
            targets = [30, 29, 36, 32, 28, 37]

    for t in targets:
        if t in unclaimed_territories:
            return game.move_claim_territory(query, t)

    # if there are no remaining targets, pick territories with the most friendly adjacents
    selected_territory = sorted(unclaimed_territories, key=lambda x: len(f_def(x)), reverse=True)[0]
    return game.move_claim_territory(query, selected_territory)


def handle_place_initial_troop(query: QueryPlaceInitialTroop) -> MovePlaceInitialTroop:
    """After all the territories have been claimed, you can place a single troop on one
    of your territories each turn until each player runs out of troops."""
    
    # We will place troops along the territories on our border.
    border_territories_id = game.state.get_all_border_territories(
        game.state.get_territories_owned_by(game.state.me.player_id)
    )
    border_territories_id = intersect(border_territories_id, targets)

    initial_troop = min(border_territories_id, key=T)
    return game.move_place_initial_troop(query, initial_troop)

def handle_redeem_cards(query: QueryRedeemCards) -> MoveRedeemCards:
    """After the claiming and placing initial troops phases are over, you can redeem any
    cards you have at the start of each turn, or after killing another player."""

    # We will always redeem the minimum number of card sets we can until the 12th card set has been redeemed.
    # This is just an arbitrary choice to try and save our cards for the late game.

    # We always have to redeem enough cards to reduce our card count below five.
    card_sets: list[Tuple[CardModel, CardModel, CardModel]] = []
    cards_remaining = game.state.me.cards.copy()

    while len(cards_remaining) >= 5:
        card_set = game.state.get_card_set(cards_remaining)
        # According to the pigeonhole principle, we should always be able to make a set
        # of cards if we have at least 5 cards.
        assert card_set != None
        card_sets.append(card_set)
        cards_remaining = [card for card in cards_remaining if card not in card_set]

    # Remember we can't redeem any more than the required number of card sets if 
    # we have just eliminated a player.
    if game.state.card_sets_redeemed > 12 and query.cause == "turn_started":
        card_set = game.state.get_card_set(cards_remaining)
        while card_set != None:
            card_sets.append(card_set)
            cards_remaining = [card for card in cards_remaining if card not in card_set]
            card_set = game.state.get_card_set(cards_remaining)

    return game.move_redeem_cards(query, [(x[0].card_id, x[1].card_id, x[2].card_id) for x in card_sets])


def handle_distribute_troops(query: QueryDistributeTroops) -> MoveDistributeTroops:
    """After you redeem cards (you may have chosen to not redeem any), you need to distribute
    all the troops you have available across your territories. This can happen at the start of
    your turn or after killing another player.
    """

    # We will distribute troops across our border territories.
    total_troops = game.state.me.troops_remaining
    border_territories = game.state.get_all_border_territories(
        game.state.get_territories_owned_by(game.state.me.player_id)
    )
    must_place = game.state.me.must_place_territory_bonus

    distributions = {t: 0 for t in border_territories + must_place}
    potential = lambda t: (distributions[t] + T(t)) - sum(T(f_opp(t)))

    # distribute evenly
    if len(must_place) != 0:
        t = min(must_place, key=potential)
        assert total_troops >= 2
        distributions[t] += 2
        total_troops -= 2
    while total_troops > 0:
        t = min(border_territories + must_place, key=potential)
        distributions[t] += 1
        total_troops -= 1

    return game.move_distribute_troops(query, distributions)


def handle_attack(query: QueryAttack) -> Union[MoveAttack, MoveAttackPass]:
    """After the troop phase of your turn, you may attack any number of times until you decide to
    stop attacking (by passing). After a successful attack, you may move troops into the conquered
    territory. If you eliminated a player you will get a move to redeem cards and then distribute troops."""
    
    my_territories = game.state.get_territories_owned_by(game.state.me.player_id)
    candidates = sorted(game.state.get_all_adjacent_territories(my_territories), key=T)

    def strongest_attack(x):
        t = max(intersect(game.state.map.get_adjacent_to(x), my_territories), key=T)
        if T(t) >= 2:
            return game.move_attack(query, t, x, min(3, T(t) - 1))
        else:
            return None
    
    # choose the smallest adjacent territory which has at least 2 more surrounding troops from me
    for x in candidates:
        if T(x) + 0 <= sum(T(f_opp(x))):
            a = strongest_attack(x)
            if a: return a

    return game.move_attack_pass(query)


def handle_troops_after_attack(query: QueryTroopsAfterAttack) -> MoveTroopsAfterAttack:
    """After conquering a territory in an attack, you must move troops to the new territory."""
    
    # First we need to get the record that describes the attack, and then the move that specifies
    # which territory was the attacking territory.
    record_attack = cast(RecordAttack, game.state.recording[query.record_attack_id])
    move_attack = cast(MoveAttack, game.state.recording[record_attack.move_attack_id])

    # We will always move the maximum number of troops we can.
    return game.move_troops_after_attack(query, T(move_attack.attacking_territory) - 1)


def handle_defend(query: QueryDefend) -> MoveDefend:
    """If you are being attacked by another player, you must choose how many troops to defend with."""

    # We will always defend with the most troops that we can.

    # First we need to get the record that describes the attack we are defending against.
    move_attack = cast(MoveAttack, game.state.recording[query.move_attack_id])
    defending_territory = move_attack.defending_territory
    
    # We can only defend with up to 2 troops, and no more than we have stationed on the defending
    # territory.
    defending_troops = min(game.state.territories[defending_territory].troops, 2)
    return game.move_defend(query, defending_troops)


def handle_fortify(query: QueryFortify) -> Union[MoveFortify, MoveFortifyPass]:
    """At the end of your turn, after you have finished attacking, you may move a number of troops between
    any two of your territories (they must be adjacent)."""

    # We will always fortify towards the most powerful player (player with most troops on the map) to defend against them.
    my_territories = game.state.get_territories_owned_by(game.state.me.player_id)
    total_troops_per_player = {}
    for player in game.state.players.values():
        total_troops_per_player[player.player_id] = sum([game.state.territories[x].troops for x in game.state.get_territories_owned_by(player.player_id)])

    most_powerful_player = max(total_troops_per_player.items(), key=lambda x: x[1])[0]

    # If we are the most powerful, we will pass.
    if most_powerful_player == game.state.me.player_id:
        return game.move_fortify_pass(query)
    
    # Otherwise we will find the shortest path between our territory with the most troops
    # and any of the most powerful player's territories and fortify along that path.
    candidate_territories = game.state.get_all_border_territories(my_territories)
    most_troops_territory = max(candidate_territories, key=T)

    # To find the shortest path, we will use a custom function.
    shortest_path = find_shortest_path_from_vertex_to_set(most_troops_territory, set(game.state.get_territories_owned_by(most_powerful_player)))
    # We will move our troops along this path (we can only move one step, and we have to leave one troop behind).
    # We have to check that we can move any troops though, if we can't then we will pass our turn.
    if len(shortest_path) > 0 and game.state.territories[most_troops_territory].troops > 1:
        return game.move_fortify(query, shortest_path[0], shortest_path[1], game.state.territories[most_troops_territory].troops - 1)
    else:
        return game.move_fortify_pass(query)

##############################################################################
################################# MAIN #######################################
##############################################################################

# Respond to the engine's queries with your moves.
while True:

    # Get the engine's query (this will block until you receive a query).
    query = game.get_next_query()

    # Based on the type of query, respond with the correct move.
    def choose_move(query: QueryType) -> MoveType:
        match query:
            case QueryClaimTerritory() as q:
                return handle_claim_territory(q)

            case QueryPlaceInitialTroop() as q:
                return handle_place_initial_troop(q)

            case QueryRedeemCards() as q:
                return handle_redeem_cards(q)

            case QueryDistributeTroops() as q:
                return handle_distribute_troops(q)

            case QueryAttack() as q:
                return handle_attack(q)

            case QueryTroopsAfterAttack() as q:
                return handle_troops_after_attack(q)

            case QueryDefend() as q:
                return handle_defend(q)

            case QueryFortify() as q:
                return handle_fortify(q)
    
    # Send the move to the engine.
    game.send_move(choose_move(query))
