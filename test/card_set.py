from collections import defaultdict
from typing import Optional, Tuple, Literal, Union
from pydantic import BaseModel
import random

SYMBOLS = ["Infantry", "Cavalry", "Artillery", "Wildcard"]

class CardModel:
    def __init__(self, card_id):
        self.card_id = card_id
        self.symbol = random.choice(SYMBOLS)


def builtin_get_card_set(cards: list[CardModel]) -> Optional[Tuple[CardModel, CardModel, CardModel]]:
    cards_by_symbol: dict[str, list[CardModel]] = defaultdict(list)
    for card in cards:
        cards_by_symbol[card.symbol].append(card)
    
    # Try to make a different symbols set.
    symbols_held = [symbol for symbol in cards_by_symbol.keys() if len(cards_by_symbol[symbol]) > 0]
    if len(symbols_held) >= 3:
        return (cards_by_symbol[symbols_held[0]][0], cards_by_symbol[symbols_held[1]][0], cards_by_symbol[symbols_held[2]][0])
    
    # To prevent implicitly modifying the dictionary in the for loop, we explicitly initialise the "Wildcard" key.
    cards_by_symbol["Wildcard"]
    
    # Try to make a matching symbols set.
    for symbol, _cards in cards_by_symbol.items():
        if symbol == "Wildcard":
            continue

        if len(_cards) >= 3:
            return (_cards[0], _cards[1], _cards[2])
        elif len(_cards) == 2 and len(cards_by_symbol["Wildcard"]) >= 1:
            return (_cards[0], _cards[1], cards_by_symbol["Wildcard"][0])
        elif len(_cards) == 1 and len(cards_by_symbol["Wildcard"]) >= 2:
            return (_cards[0], cards_by_symbol["Wildcard"][0], cards_by_symbol["Wildcard"][1])


def my_get_card_set(cards: list[CardModel]) -> Optional[Tuple[CardModel, CardModel, CardModel]]:
    cards_by_symbol: dict[str, list[CardModel]] = defaultdict(list)
    for card in cards:
        cards_by_symbol[card.symbol].append(card)
    
    # Try to make a different symbols set.
    symbols_held = [symbol for symbol in cards_by_symbol.keys() if len(cards_by_symbol[symbol]) > 0]
    if len(symbols_held) >= 3:
        return (cards_by_symbol[symbols_held[0]][0], cards_by_symbol[symbols_held[1]][0], cards_by_symbol[symbols_held[2]][0])
    
    # To prevent implicitly modifying the dictionary in the for loop, we explicitly initialise the "Wildcard" key.
    cards_by_symbol["Wildcard"]
    
    # Try to make a matching symbols set.
    for symbol, _cards in cards_by_symbol.items():
        if symbol == "Wildcard":
            continue
        if len(_cards) >= 3:
            return (_cards[0], _cards[1], _cards[2])
    for symbol, _cards in cards_by_symbol.items():
        if symbol == "Wildcard":
            continue
        elif len(_cards) == 2 and len(cards_by_symbol["Wildcard"]) >= 1:
            return (_cards[0], _cards[1], cards_by_symbol["Wildcard"][0])
    for symbol, _cards in cards_by_symbol.items():
        if symbol == "Wildcard":
            continue
        elif len(_cards) == 1 and len(cards_by_symbol["Wildcard"]) >= 2:
            return (_cards[0], cards_by_symbol["Wildcard"][0], cards_by_symbol["Wildcard"][1])

def build(cards, f):
    sets = []
    while len(cards) >= 5 and (x := f(cards)):
        sets.append(x)
        cards = [card for card in cards if card not in x]
    return sets

my = 0
builtin = 0
for _ in range(1000):
    cards = [CardModel(i) for i in range(5)]
    M = build(cards, my_get_card_set)
    B = build(cards, builtin_get_card_set)
    assert M == B
    my += sum(c.symbol == "Wildcard" for C in M for c in C)
    builtin += sum(c.symbol == "Wildcard" for C in B for c in C)
print(my, builtin)
