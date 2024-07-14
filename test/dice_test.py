import itertools
from collections import defaultdict
import functools
import random
import time

def prob(a, b):
    """attacker rolls a dice, defender rolls b dice"""
    freq = defaultdict(int)
    for prod in itertools.product(*[range(1, 7)] * (a + b)):
        diceA = sorted(prod[:a], reverse=True)
        diceB = sorted(prod[a:], reverse=True)
        deadA = deadB = 0
        for dA, dB in zip(diceA, diceB):
            if dA > dB: deadB += 1
            else: deadA += 1
        freq[(deadA, deadB)] += 1 / 6**(a + b)
    return freq

def probRand(a, b):
    diceA = sorted([random.randint(1, 6) for _ in range(a)], reverse=True)
    diceB = sorted([random.randint(1, 6) for _ in range(b)], reverse=True)
    deadA = deadB = 0
    for dA, dB in zip(diceA, diceB):
        if dA > dB: deadB += 1
        else: deadA += 1
    return deadA, deadB

# (A, B) -> (deadA, deadB) -> probability
PROB = {
    (1, 1): {(1, 0): 0.5833333333333335, (0, 1): 0.4166666666666668},
    (1, 2): {(1, 0): 0.7453703703703722, (0, 1): 0.2546296296296294},
    (2, 1): {(1, 0): 0.4212962962962968, (0, 1): 0.5787037037037048},
    (2, 2): {(2, 0): 0.4483024691358043, (1, 1): 0.32407407407407535, (0, 2): 0.22762345679012433},
    (3, 1): {(1, 0): 0.3402777777777791, (0, 1): 0.6597222222222134},
    (3, 2): {(2, 0): 0.29256687242799495, (1, 1): 0.3357767489712081, (0, 2): 0.3716563786008405},
}

@functools.lru_cache(maxsize=1000)
def challenge(A, B):
    """returns map from num remaining to probability"""
    if A == 0 or B == 0: return [0] * A + [1]

    a = min(3, A)
    b = min(2, B)
    dis = [0] * (A + 1)
    for k, v in PROB[(a, b)].items():
        for x, p in enumerate(challenge(A - k[0], B - k[1])):
            dis[x] += p * v
    return dis

def challengeRand(A_, B_):
    P = {a: 0 for a in range(A_ + 1)}
    for _ in range(200000):
        A = A_
        B = B_
        while A and B:
            deadA, deadB = probRand(min(3, A), min(2, B))
            A -= deadA
            B -= deadB
        P[A] += 1/200000
    return P

def challengePath(A, Bs):
    Adis = [0] * A + [1]
    for B, leave in Bs:
        # assert leave >= 1
        AdisNew = [0] * (A + 1)
        for A, p1 in enumerate(Adis):
            if p1 < 1e-5: continue
            for Anew, p2 in enumerate(challenge(A, B)):
                AdisNew[max(0, Anew - leave)] += p1 * p2
        Adis = AdisNew
    return Adis

def challengePathRand(A_, Bs):
    P = [0] * (A_ + 1)
    for _ in range(200000):
        A = A_
        for B, leave in Bs:
            while A and B:
                deadA, deadB = probRand(min(3, A), min(2, B))
                A -= deadA
                B -= deadB
            A = max(0, A - leave)
        P[A] += 1/200000
    return P

# x = time.perf_counter()
# for _ in range(10000):
#     (challengePath(
#         20,
#         [(3, 3), (1, 3), (3, 1), (1, 1), (1, 1), (1, 0)]
#     ))
# y = time.perf_counter()
# print((y - x) / 10000)
# print(__file__)

# for i, x in enumerate(challenge(14, 9)):
#     print((i, x))
for b in range(200):
    E = sum(i * x for i, x in enumerate(challenge(200, b)))
    print((b, E))
