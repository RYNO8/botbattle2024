_print = print
print = lambda *args, **kwargs: _print(*args, **kwargs, flush=True)
print("e0.py")

from collections import deque, defaultdict
import random
import itertools
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


def union(a: list, b: list):
    """does not assume each of a and b have distinct elements"""
    return list(set(a + b))

def intersect(a: list, b: list):
    """does not assume each of a and b have distinct elements"""
    return list(set(a) & set(b))

def set_diff(a: list, b: list):
    """does not assume each of a and b have distinct elements"""
    return list(set(a) - set(b))

##############################################################################
################################ STATE #######################################
##############################################################################

# We will store our enemy in the bot state.
class BotState():
    def __init__(self):
        self.enemy: Optional[int] = None
        self.numFortify = 0
        self.borderSz = -1
        self.targets = []
        self.attack_from = []

# Get the game object, which will connect you to the engine and
# track the state of the game.
game = Game()
bot_state = BotState()

##############################################################################
############################### HELPERS ######################################
##############################################################################

def find_shortest_path_from_vertex_to_set(source: int, target_set: set[int], owned: set[int]) -> list[int]:
    """Used in move_fortify()."""

    # We perform a BFS search from our source vertex, stopping at the first member of the target_set we find.
    queue = [source]
    parent = {}
    i = 0
    while i < len(queue) and queue[i] not in target_set:
        u = queue[i]
        for v in game.state.map.get_adjacent_to(u):
            if v in owned and v not in queue:
                queue.append(v)
                parent[v] = u
        i += 1

    if i == len(queue): return []
    current = queue[i]
    path = []
    while current in parent:
        path.insert(0, current)
        current = parent[current]
    path.insert(0, source)
    return path

# me
def m_id() -> int:
    return game.state.me.player_id

# troops
def T(t):
    if isinstance(t, int): return game.state.territories[t].troops
    elif isinstance(t, TerritoryModel): return t.troops
    elif isinstance(t, list): return [game.state.territories[x].troops for x in t]
    elif callable(t): return lambda x: T(t(x))
    else: raise TypeError

def O(t):
    if isinstance(t, int): return game.state.territories[t].occupier
    elif isinstance(t, TerritoryModel): return t.occupier == game.state.me.player_id
    elif isinstance(t, list): return [game.state.territories[x].occupier for x in t]
    elif callable(t): return lambda x: T(t(x))
    else: raise TypeError

def O_me(t) -> bool:
    return O(t) == game.state.me.player_id

# function
def f_adj(t: int) -> list[int]:
    return game.state.map.get_adjacent_to(t)

def f_(t: int, id: int) -> list[int]:
    return [x for x in f_adj(t) if O(x) == id]

def f_me(t: int):
    return f_(t, m_id())

def f_def(t):
    return f_(t, O(t))

def f_empty(t: int) -> list[int]:
    return f_(t, None)

def f_opp(t: int) -> list[int]:
    if O_me(t):
        return [x for x in game.state.map.get_adjacent_to(t) if O(x) not in [None, m_id()]]
    else:
        return [x for x in game.state.map.get_adjacent_to(t) if O(x) == m_id()]

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

def containing_base(owned: list[int], start: int) -> list[list[int]]:
    todo = set(owned)
    queue = [start]
    i = 0
    while i < len(queue):
        for v in game.state.map.get_adjacent_to(queue[i]):
            if v in todo:
                todo.remove(v)
                queue.append(v)
        i += 1
    return queue

##############################################################################
############################### ACTIONS ######################################
##############################################################################


CLAIM_PRIORITY = [
    # north america
    6, 3, 8, 2, 1, 5, 7, 4, 0
]


def handle_claim_territory(query: QueryClaimTerritory) -> MoveClaimTerritory:
    """At the start of the game, you can claim a single unclaimed territory every turn 
    until all the territories have been claimed by players."""

    unclaimed_t = game.state.get_territories_owned_by(None)
    my_t = game.state.get_territories_owned_by(m_id())

    for t in CLAIM_PRIORITY:
        if t in unclaimed_t and t not in my_t and f_me(t):
            return game.move_claim_territory(query, t)
    for t in CLAIM_PRIORITY:
        if t in unclaimed_t and t not in my_t:
            return game.move_claim_territory(query, t)

    t = min(unclaimed_t, key=lambda x:(-len(f_me(x)), len(f_adj(x))))
    return game.move_claim_territory(query, t)


def handle_place_initial_troop(query: QueryPlaceInitialTroop) -> MovePlaceInitialTroop:
    """After all the territories have been claimed, you can place a single troop on one
    of your territories each turn until each player runs out of troops."""
    
    # We will place troops along the territories on our border.
    my_t = game.state.get_territories_owned_by(m_id())
    border_t = intersect(game.state.get_all_border_territories(my_t), biggest_bases(my_t)[0])
    t = min(border_t, key=lambda x: T(x) - max(T(f_opp(x))))
    return game.move_place_initial_troop(query, t)


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
    my_t = game.state.get_territories_owned_by(m_id())
    base_t = my_t # biggest_bases(my_t)[0]
    opp_t = game.state.get_all_adjacent_territories(base_t)
    opp_t += game.state.get_all_adjacent_territories(base_t + opp_t)
    border_t = game.state.get_all_border_territories(base_t)
    bot_state.borderSz = len(border_t)
    must_place = game.state.me.must_place_territory_bonus
    num_players = sum(p.alive for p in game.state.players.values())

    # the border size should increase by no more than 1
    
    if False and num_players == 2:
        bot_state.targets = [x for x in game.state.territories.keys() if not O_me(x)]
        attack_from = border_t
    else:
        bestBorderSz = len(border_t) + 2
        bot_state.targets = []
        for targetSz in [1, 2, 3, 4, 5, 6]:
            combs = list(itertools.combinations(opp_t, targetSz))
            for _ in range(min(500, len(combs))):
                targets = random.choice(combs)
                possible = sum(map(T, targets)) + len(targets) <= total_troops
                if not possible: continue
                borderSz = len(game.state.get_all_border_territories(tuple(base_t) + targets))
                if borderSz <= bestBorderSz and (
                    targetSz > 1 or
                    borderSz <= len(border_t) + 1
                ):
                    bestBorderSz = borderSz
                    bot_state.targets = targets
        attack_from = [max(f_me(x), key=T) for x in bot_state.targets if f_me(x)]
        if not attack_from:
            attack_from = border_t
    print(num_players, bot_state.targets, attack_from)

    distributions = defaultdict(int)
    potential = lambda x: T(x) + distributions[x]  - max(T(f_opp(x) or [0]))
    # potential = lambda x: T(x) + distributions[x]
    if len(must_place) != 0:
        t = min(must_place, key=lambda x: ([-100, 100][x in attack_from], potential(x)))
        assert total_troops >= 2
        distributions[t] += 2
        total_troops -= 2


    while total_troops > 6:
        t = min(attack_from, key=potential)
        distributions[t] += 1
        total_troops -= 1
    while total_troops > 0:
        t = min(border_t, key=potential)
        distributions[t] += 1
        total_troops -= 1

    return game.move_distribute_troops(query, distributions)


def handle_attack(query: QueryAttack) -> Union[MoveAttack, MoveAttackPass]:
    """After the troop phase of your turn, you may attack any number of times until you decide to
    stop attacking (by passing). After a successful attack, you may move troops into the conquered
    territory. If you eliminated a player you will get a move to redeem cards and then distribute troops."""

    # if len(game.state.recording) >= 14000: raise Exception()

    my_t = game.state.get_territories_owned_by(game.state.me.player_id)
    border_t = game.state.get_all_border_territories(my_t)
    opp_t = game.state.get_all_adjacent_territories(my_t)
    bot_state.targets = [x for x in bot_state.targets if not O_me(x)]
    num_players = sum(p.alive for p in game.state.players.values())
    if False and num_players == 2:
        for t in sorted(border_t, key=T, reverse=True):
            for x in sorted(f_opp(t), key=T):
                if T(t) >= 3 and T(t) > T(x):
                    return game.move_attack(query, t, x, min(3, T(t) - 1))
        return game.move_attack_pass(query)
    else:
        candidates = sorted(bot_state.targets, key=T)
        for x in candidates:
            adj = sorted(f_me(x), key=lambda t:len(f_opp(t)))
            for t in adj:
                if T(t) >= 3 and T(t) > T(x):
                    return game.move_attack(query, t, x, min(3, T(t) - 1))
    return game.move_attack_pass(query)


def handle_troops_after_attack(query: QueryTroopsAfterAttack) -> MoveTroopsAfterAttack:
    """After conquering a territory in an attack, you must move troops to the new territory."""
    
    # First we need to get the record that describes the attack, and then the move that specifies
    # which territory was the attacking territory.
    record_attack = cast(RecordAttack, game.state.recording[query.record_attack_id])
    move_attack = cast(MoveAttack, game.state.recording[record_attack.move_attack_id])
    attacking_t = move_attack.attacking_territory

    if f_opp(attacking_t):
        return game.move_troops_after_attack(query, T(attacking_t) // 2 + 1)
    else:
        return game.move_troops_after_attack(query, T(attacking_t) - 1)


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

    bot_state.numFortify += 1
    my_t = game.state.get_territories_owned_by(m_id())
    border_t = game.state.get_all_border_territories(my_t)
    internal_t = set_diff(my_t, border_t)
    if internal_t:
        source = max(internal_t, key=T)
        path = find_shortest_path_from_vertex_to_set(source, set(border_t), set(my_t))
        if T(source) > 1 and path:
            return game.move_fortify(query, path[0], path[1], T(source) - 1)

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
