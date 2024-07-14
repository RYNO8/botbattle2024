vertices = {
    # North America
    "ALASKA": 0,
    "ALBERTA": 1,
    "CENTRAL_AMERICA": 2,
    "EASTERN_US": 3,
    "GREENLAND": 4,
    "NORTHWEST_TERRITORY": 5,
    "ONTARIO": 6,
    "QUEBEC": 7,
    "WESTERN_US": 8,
    # Europe
    "GREAT_BRITAIN": 9,
    "ICELAND": 10,
    "NORTHERN_EUROPE": 11,
    "SCANDINAVIA": 12,
    "SOUTHERN_EUROPE": 13,
    "UKRAINE": 14,
    "WESTERN_EUROPE": 15,
    # Asia
    "AFGHANISTAN": 16,
    "CHINA": 17,
    "INDIA": 18,
    "IRKUTSK": 19,
    "JAPAN": 20,
    "KAMCHATKA": 21,
    "MIDDLE_EAST": 22,
    "MONGOLIA": 23,
    "SIAM": 24,
    "SIBERIA": 25,
    "URAL": 26,
    "YAKUTSK": 27,
    # South America
    "ARGENTINA": 28,
    "BRAZIL": 29,
    "VENEZUELA": 30,
    "PERU": 31,
    # Africa
    "CONGO": 32,
    "EAST_AFRICA": 33,
    "EGYPT": 34,
    "MADAGASCAR": 35,
    "NORTH_AFRICA": 36,
    "SOUTH_AFRICA": 37,
    # Australia
    "EASTERN_AUSTRALIA": 38,
    "NEW_GUINEA": 39,
    "INDONESIA": 40,
    "WESTERN_AUSTRALIA": 41,
}

continents = {
    0 : [
            vertices["ALASKA"],
            vertices["ALBERTA"],
            vertices["CENTRAL_AMERICA"],
            vertices["EASTERN_US"],
            vertices["GREENLAND"],
            vertices["NORTHWEST_TERRITORY"],
            vertices["ONTARIO"],
            vertices["QUEBEC"],
            vertices["WESTERN_US"]
        ],
    1 : [
            vertices["GREAT_BRITAIN"],
            vertices["ICELAND"],
            vertices["NORTHERN_EUROPE"],
            vertices["SCANDINAVIA"],
            vertices["SOUTHERN_EUROPE"],
            vertices["UKRAINE"],
            vertices["WESTERN_EUROPE"],
        ],
    2 : [
            vertices["AFGHANISTAN"],
            vertices["CHINA"],
            vertices["INDIA"],
            vertices["IRKUTSK"],
            vertices["JAPAN"],
            vertices["KAMCHATKA"],
            vertices["MIDDLE_EAST"],
            vertices["MONGOLIA"],
            vertices["SIAM"],
            vertices["SIBERIA"],
            vertices["URAL"],
            vertices["YAKUTSK"],
        ],
    3: [
            vertices["ARGENTINA"],
            vertices["BRAZIL"],
            vertices["VENEZUELA"],
            vertices["PERU"],
        ],
    4: [
            vertices["CONGO"],
            vertices["EAST_AFRICA"],
            vertices["EGYPT"],
            vertices["MADAGASCAR"],
            vertices["NORTH_AFRICA"],
            vertices["SOUTH_AFRICA"]
        ],
    5: [
            vertices["EASTERN_AUSTRALIA"],
            vertices["NEW_GUINEA"],
            vertices["INDONESIA"],
            vertices["WESTERN_AUSTRALIA"],
        ],
}

continent_bonuses = {
    0 : 5,
    1 : 5,
    2 : 7,
    3 : 2,
    4 : 3,
    5 : 2,
}

edges = {
    vertices["ALASKA"]: [
        vertices["ALBERTA"],
        vertices["NORTHWEST_TERRITORY"],
        vertices["KAMCHATKA"],
    ],
    vertices["ALBERTA"]: [
        vertices["ONTARIO"],
        vertices["NORTHWEST_TERRITORY"],
        vertices["ALASKA"],
        vertices["WESTERN_US"],
    ],
    vertices["CENTRAL_AMERICA"]: [
        vertices["EASTERN_US"],
        vertices["WESTERN_US"],
        vertices["VENEZUELA"],
    ],
    vertices["EASTERN_US"]: [
        vertices["QUEBEC"],
        vertices["ONTARIO"],
        vertices["WESTERN_US"],
        vertices["CENTRAL_AMERICA"],
    ],
    vertices["GREENLAND"]: [
        vertices["NORTHWEST_TERRITORY"],
        vertices["ONTARIO"],
        vertices["QUEBEC"],
        vertices["ICELAND"],
    ],
    vertices["NORTHWEST_TERRITORY"]: [
        vertices["GREENLAND"],
        vertices["ALASKA"],
        vertices["ALBERTA"],
        vertices["ONTARIO"],
    ],
    vertices["ONTARIO"]: [
        vertices["QUEBEC"],
        vertices["GREENLAND"],
        vertices["NORTHWEST_TERRITORY"],
        vertices["ALBERTA"],
        vertices["WESTERN_US"],
        vertices["EASTERN_US"],
    ],
    vertices["QUEBEC"]: [
        vertices["GREENLAND"],
        vertices["ONTARIO"],
        vertices["EASTERN_US"],
    ],
    vertices["WESTERN_US"]: [
        vertices["EASTERN_US"],
        vertices["ONTARIO"],
        vertices["ALBERTA"],
        vertices["CENTRAL_AMERICA"],
    ],
    vertices["GREAT_BRITAIN"]: [
        vertices["NORTHERN_EUROPE"],
        vertices["SCANDINAVIA"],
        vertices["ICELAND"],
        vertices["WESTERN_EUROPE"],
    ],
    vertices["ICELAND"]: [
        vertices["SCANDINAVIA"],
        vertices["GREENLAND"],
        vertices["GREAT_BRITAIN"],
    ],
    vertices["NORTHERN_EUROPE"]: [
        vertices["UKRAINE"],
        vertices["SCANDINAVIA"],
        vertices["GREAT_BRITAIN"],
        vertices["WESTERN_EUROPE"],
        vertices["SOUTHERN_EUROPE"],
    ],
    vertices["SCANDINAVIA"]: [
        vertices["UKRAINE"],
        vertices["ICELAND"],
        vertices["GREAT_BRITAIN"],
        vertices["NORTHERN_EUROPE"],
    ],
    vertices["SOUTHERN_EUROPE"]: [
        vertices["MIDDLE_EAST"],
        vertices["UKRAINE"],
        vertices["NORTHERN_EUROPE"],
        vertices["WESTERN_EUROPE"],
        vertices["NORTH_AFRICA"],
        vertices["EGYPT"],
    ],
    vertices["UKRAINE"]: [
        vertices["AFGHANISTAN"],
        vertices["URAL"],
        vertices["SCANDINAVIA"],
        vertices["NORTHERN_EUROPE"],
        vertices["SOUTHERN_EUROPE"],
        vertices["MIDDLE_EAST"],
    ],
    vertices["WESTERN_EUROPE"]: [
        vertices["SOUTHERN_EUROPE"],
        vertices["NORTHERN_EUROPE"],
        vertices["GREAT_BRITAIN"],
        vertices["NORTH_AFRICA"],
    ],
    vertices["AFGHANISTAN"]: [
        vertices["CHINA"],
        vertices["URAL"],
        vertices["UKRAINE"],
        vertices["MIDDLE_EAST"],
        vertices["INDIA"],
    ],
    vertices["CHINA"]: [
        vertices["MONGOLIA"],
        vertices["SIBERIA"],
        vertices["URAL"],
        vertices["AFGHANISTAN"],
        vertices["INDIA"],
        vertices["SIAM"],
    ],
    vertices["INDIA"]: [
        vertices["SIAM"],
        vertices["CHINA"],
        vertices["AFGHANISTAN"],
        vertices["MIDDLE_EAST"],
    ],
    vertices["IRKUTSK"]: [
        vertices["KAMCHATKA"],
        vertices["YAKUTSK"],
        vertices["SIBERIA"],
        vertices["MONGOLIA"],
    ],
    vertices["JAPAN"]: [
        vertices["KAMCHATKA"],
        vertices["MONGOLIA"],
    ],
    vertices["KAMCHATKA"]: [
        vertices["ALASKA"],
        vertices["YAKUTSK"],
        vertices["IRKUTSK"],
        vertices["MONGOLIA"],
        vertices["JAPAN"],
    ],
    vertices["MIDDLE_EAST"]: [
        vertices["INDIA"],
        vertices["AFGHANISTAN"],
        vertices["UKRAINE"],
        vertices["SOUTHERN_EUROPE"],
        vertices["EGYPT"],
        vertices["EAST_AFRICA"],
    ],
    vertices["MONGOLIA"]: [
        vertices["JAPAN"],
        vertices["KAMCHATKA"],
        vertices["IRKUTSK"],
        vertices["SIBERIA"],
        vertices["CHINA"],
    ],
    vertices["SIAM"]: [
        vertices["CHINA"],
        vertices["INDIA"],
        vertices["INDONESIA"],
    ],
    vertices["SIBERIA"]: [
        vertices["YAKUTSK"],
        vertices["URAL"],
        vertices["CHINA"],
        vertices["MONGOLIA"],
        vertices["IRKUTSK"],
    ],
    vertices["URAL"]: [
        vertices["SIBERIA"],
        vertices["UKRAINE"],
        vertices["AFGHANISTAN"],
        vertices["CHINA"],
    ],
    vertices["YAKUTSK"]: [
        vertices["KAMCHATKA"],
        vertices["SIBERIA"],
        vertices["IRKUTSK"],
    ],
    vertices["ARGENTINA"]: [
        vertices["BRAZIL"],
        vertices["PERU"],
    ],
    vertices["BRAZIL"]: [
        vertices["NORTH_AFRICA"],
        vertices["VENEZUELA"],
        vertices["PERU"],
        vertices["ARGENTINA"],
    ],
    vertices["VENEZUELA"]: [
        vertices["CENTRAL_AMERICA"],
        vertices["PERU"],
        vertices["BRAZIL"],
    ],
    vertices["PERU"]: [
        vertices["BRAZIL"],
        vertices["VENEZUELA"],
        vertices["ARGENTINA"],
    ],
    vertices["CONGO"]: [
        vertices["EAST_AFRICA"],
        vertices["NORTH_AFRICA"],
        vertices["SOUTH_AFRICA"],
    ],
    vertices["EAST_AFRICA"]: [
        vertices["MIDDLE_EAST"],
        vertices["EGYPT"],
        vertices["NORTH_AFRICA"],
        vertices["CONGO"],
        vertices["SOUTH_AFRICA"],
        vertices["MADAGASCAR"],
    ],
    vertices["EGYPT"]: [
        vertices["MIDDLE_EAST"],
        vertices["SOUTHERN_EUROPE"],
        vertices["NORTH_AFRICA"],
        vertices["EAST_AFRICA"],
    ],
    vertices["MADAGASCAR"]: [
        vertices["EAST_AFRICA"],
        vertices["SOUTH_AFRICA"],
    ],
    vertices["NORTH_AFRICA"]: [
        vertices["EAST_AFRICA"],
        vertices["EGYPT"],
        vertices["SOUTHERN_EUROPE"],
        vertices["WESTERN_EUROPE"],
        vertices["BRAZIL"],
        vertices["CONGO"],
    ],
    vertices["SOUTH_AFRICA"]: [
        vertices["MADAGASCAR"],
        vertices["EAST_AFRICA"],
        vertices["CONGO"],
    ],
    vertices["EASTERN_AUSTRALIA"]: [
        vertices["NEW_GUINEA"],
        vertices["WESTERN_AUSTRALIA"],
    ],
    vertices["NEW_GUINEA"]: [
        vertices["INDONESIA"],
        vertices["WESTERN_AUSTRALIA"],
        vertices["EASTERN_AUSTRALIA"],
    ],
    vertices["INDONESIA"]: [
        vertices["NEW_GUINEA"],
        vertices["SIAM"],
        vertices["WESTERN_AUSTRALIA"],
    ],
    vertices["WESTERN_AUSTRALIA"]: [
        vertices["EASTERN_AUSTRALIA"],
        vertices["NEW_GUINEA"],
        vertices["INDONESIA"],
    ],
}

# for k, V in edges.items():
#     for v in V:
#         print(k, v)

# for c, V in continents.items():
#     print(continent_bonuses[c], V)

V = list(vertices.values())

def getBoundary(S):
    return [u for u in S if any(v not in S for v in edges[u])]

def getOpp(S):
    return [u for u in V if u not in S and any(v in S for v in edges[u])]

import random
import itertools

# by len(getOpp)
BEST_OPP = {
    1: (2, [(20,), (28,), (35,), (38,)]),
    2: (2, [(28, 31), (35, 37), (38, 39), (38, 41), (39, 41)]),
    3: (1, [(38, 39, 41)]),
    4: (1, [(38, 39, 40, 41)]),
    5: (2, [(24, 38, 39, 40, 41)]),
    6: (3, [(1, 3, 5, 6, 7, 8), (18, 24, 38, 39, 40, 41), (19, 20, 21, 23, 25, 27), (28, 29, 31, 32, 35, 37), (28, 29, 31, 38, 39, 41), (28, 30, 31, 38, 39, 41), (28, 31, 38, 39, 40, 41), (32, 35, 37, 38, 39, 41), (35, 37, 38, 39, 40, 41)]),
    7: (3, [[0, 1, 3, 5, 6, 7, 8], [1, 2, 3, 5, 6, 7, 8], [1, 3, 4, 5, 6, 7, 8]]),
    8: (3, [[0, 1, 2, 3, 5, 6, 7, 8], [0, 1, 3, 4, 5, 6, 7, 8], [1, 2, 3, 4, 5, 6, 7, 8]]),
    9: (3, [[0, 1, 2, 3, 4, 5, 6, 7, 8]]),
    10: (3, [[1, 2, 3, 5, 6, 7, 8, 28, 30, 31]]),
    11: (3, [[0, 1, 2, 3, 5, 6, 7, 8, 28, 30, 31], [1, 2, 3, 4, 5, 6, 7, 8, 28, 30, 31], [1, 2, 3, 5, 6, 7, 8, 28, 29, 30, 31]]),
    12: (3, [[0, 1, 2, 3, 4, 5, 6, 7, 8, 28, 30, 31], [0, 1, 2, 3, 5, 6, 7, 8, 28, 29, 30, 31], [1, 2, 3, 4, 5, 6, 7, 8, 28, 29, 30, 31]]),
    13: (3, [[0, 1, 2, 3, 4, 5, 6, 7, 8, 28, 29, 30, 31]]),
    14: (3, [[16, 17, 18, 19, 20, 23, 24, 25, 26, 27, 38, 39, 40, 41]]),
    15: (3, [[16, 17, 18, 19, 20, 21, 23, 24, 25, 26, 27, 38, 39, 40, 41]]),
    16: (4, [[0, 1, 2, 3, 4, 5, 6, 7, 8, 19, 20, 21, 27, 28, 30, 31], [0, 1, 2, 3, 5, 6, 7, 8, 19, 20, 21, 23, 27, 28, 30, 31], [0, 1, 2, 3, 5, 6, 7, 8, 19, 20, 21, 27, 28, 29, 30, 31], [0, 16, 17, 18, 19, 20, 21, 23, 24, 25, 26, 27, 38, 39, 40, 41], [9, 10, 11, 12, 13, 15, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37]]),
    17: (4, [[0, 1, 2, 3, 4, 5, 6, 7, 8, 19, 20, 21, 23, 27, 28, 30, 31], [0, 1, 2, 3, 4, 5, 6, 7, 8, 19, 20, 21, 27, 28, 29, 30, 31], [0, 1, 2, 3, 5, 6, 7, 8, 19, 20, 21, 23, 25, 27, 28, 30, 31], [0, 1, 2, 3, 5, 6, 7, 8, 19, 20, 21, 23, 27, 28, 29, 30, 31], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 15, 28, 29, 30, 31]]),
    18: (4, [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 15, 28, 29, 30, 31], [0, 1, 2, 3, 4, 5, 6, 7, 8, 19, 20, 21, 23, 25, 27, 28, 30, 31], [0, 1, 2, 3, 4, 5, 6, 7, 8, 19, 20, 21, 23, 27, 28, 29, 30, 31], [0, 1, 2, 3, 5, 6, 7, 8, 19, 20, 21, 23, 25, 27, 28, 29, 30, 31]]),
    19: (4, [[0, 1, 2, 3, 4, 5, 6, 7, 8, 19, 20, 21, 23, 25, 27, 28, 29, 30, 31], [9, 11, 12, 13, 14, 15, 16, 18, 22, 24, 32, 33, 34, 35, 37, 38, 39, 40, 41]]),
    20: (4, [[9, 10, 11, 12, 13, 14, 15, 16, 18, 22, 24, 32, 33, 34, 35, 37, 38, 39, 40, 41],
        [9, 11, 12, 13, 14, 15, 16, 18, 22, 24, 26, 32, 33, 34, 35, 37, 38, 39, 40, 41],
        [9, 11, 12, 13, 14, 15, 16, 18, 22, 24, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41],
        [16, 17, 18, 19, 20, 22, 23, 24, 25, 26, 27, 32, 33, 34, 35, 37, 38, 39, 40, 41]
    ]),
    21: (4, [
        [9, 10, 11, 12, 13, 14, 15, 16, 18, 22, 24, 26, 32, 33, 34, 35, 37, 38, 39, 40, 41], 
        [9, 10, 11, 12, 13, 14, 15, 16, 18, 22, 24, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41], 
        [9, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 22, 23, 25, 26, 27, 32, 33, 34, 35, 37], 
        [9, 11, 12, 13, 14, 15, 16, 17, 18, 22, 24, 26, 32, 33, 34, 35, 37, 38, 39, 40, 41], 
        [9, 11, 12, 13, 14, 15, 16, 18, 22, 24, 26, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41], 
        [16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 32, 33, 34, 35, 37, 38, 39, 40, 41]
    ]),
}

BEST_BOUNDARY = {
    6: (2, [[2, 28, 29, 30, 31, 36], [17, 24, 38, 39, 40, 41], [18, 24, 38, 39, 40, 41]]),
    7: (2, [[17, 18, 24, 38, 39, 40, 41]]),
    8: (3, [[0, 17, 19, 20, 21, 23, 25, 27], [2, 3, 8, 28, 29, 30, 31, 36], [13, 22, 32, 33, 34, 35, 36, 37], [16, 17, 18, 24, 38, 39, 40, 41], [17, 18, 22, 24, 38, 39, 40, 41], [17, 18, 23, 24, 38, 39, 40, 41], [17, 18, 24, 25, 38, 39, 40, 41], [17, 18, 24, 26, 38, 39, 40, 41], [17, 19, 20, 21, 23, 25, 26, 27]]),
    9: (3, [[0, 1, 2, 3, 4, 5, 6, 7, 8], [0, 17, 19, 20, 21, 23, 25, 26, 27], [16, 17, 18, 22, 24, 38, 39, 40, 41], [28, 29, 30, 31, 32, 33, 35, 36, 37]]),
    10: (3, [[0, 1, 2, 3, 4, 5, 6, 7, 8, 10], [0, 1, 2, 3, 4, 5, 6, 7, 8, 21], [0, 1, 2, 3, 4, 5, 6, 7, 8, 30], [2, 28, 29, 30, 31, 32, 33, 35, 36, 37]]),
    11: (3, [[0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 21], [0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 30], [0, 1, 2, 3, 4, 5, 6, 7, 8, 21, 30]]),
    12: (3, [[0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 21, 30]]),
    13: (3, [[0, 1, 2, 3, 4, 5, 6, 7, 8, 28, 29, 30, 31]]),
    14: (3, [[0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 28, 29, 30, 31], [0, 1, 2, 3, 4, 5, 6, 7, 8, 21, 28, 29, 30, 31], [0, 1, 2, 3, 4, 5, 6, 7, 8, 28, 29, 30, 31, 36]]),
    15: (3, [[0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 21, 28, 29, 30, 31], [0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 28, 29, 30, 31, 36], [0, 1, 2, 3, 4, 5, 6, 7, 8, 21, 28, 29, 30, 31, 36]]),
    16: (3, [[0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 21, 28, 29, 30, 31, 36]]),
    17: (3, [[14, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 38, 39, 40, 41]]),
    18: (3, [[0, 14, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 38, 39, 40, 41]]),
    19: (4, [[0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 17, 19, 20, 21, 23, 25, 26, 27, 30], [0, 1, 2, 3, 4, 5, 6, 7, 8, 19, 20, 21, 23, 25, 27, 28, 29, 30, 31], [0, 1, 2, 3, 4, 5, 6, 7, 8, 21, 28, 29, 30, 31, 32, 33, 35, 36, 37], [0, 1, 14, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 38, 39, 40, 41], [0, 5, 14, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 38, 39, 40, 41], [0, 11, 14, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 38, 39, 40, 41], [0, 12, 14, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 38, 39, 40, 41], [0, 13, 14, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 38, 39, 40, 41], [0, 14, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 33, 38, 39, 40, 41], [0, 14, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 34, 38, 39, 40, 41], [2, 9, 10, 11, 12, 13, 14, 15, 22, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37], [4, 9, 10, 11, 12, 13, 14, 15, 22, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37]]),
    20: (4, [[0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 19, 20, 21, 23, 25, 27, 28, 29, 30, 31], [0, 1, 2, 3, 4, 5, 6, 7, 8, 17, 19, 20, 21, 23, 25, 27, 28, 29, 30, 31], [0, 1, 2, 3, 4, 5, 6, 7, 8, 19, 20, 21, 23, 25, 27, 28, 29, 30, 31, 36], [0, 1, 5, 14, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 38, 39, 40, 41], [2, 4, 9, 10, 11, 12, 13, 14, 15, 22, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37]]),
    21: (4, [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 28, 29, 30, 31, 36], [0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 17, 19, 20, 21, 23, 25, 27, 28, 29, 30, 31], [0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 19, 20, 21, 23, 25, 27, 28, 29, 30, 31, 36], [0, 1, 2, 3, 4, 5, 6, 7, 8, 17, 19, 20, 21, 23, 25, 26, 27, 28, 29, 30, 31], [0, 1, 2, 3, 4, 5, 6, 7, 8, 17, 19, 20, 21, 23, 25, 27, 28, 29, 30, 31, 36]]),
}

N = 17000

# for sz in range(6, 22):
#     best = []
#     bestSz = 1e19
#     # for S in itertools.combinations(V, sz):
#     for rep in range(N):
#         S = [random.choice(V)]
#         for _ in range(sz - 1):
#             S.append(random.choice(getOpp(S)))
#         boundary = getBoundary(S)
#         if len(boundary) < bestSz:
#             best = []
#             bestSz = len(boundary)
#         if len(boundary) == bestSz:
#             S = sorted(S)
#             if S not in best: best.append(S)

#     best.sort()
#     print(bestSz, best, sep=", ")



for k in range(6, 22):
    sz, SS = BEST_BOUNDARY[k]
    print(*[str(u).zfill(2) for u in V])
    # print(*["**" if any(u in S for S in SS) else "  " for u in V])
    for S in SS:
        print(*["**" if u in S else "  " for u in V])
    # print(*["--" for u in V])
