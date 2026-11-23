"""Zhao--Deng task definition shared by all scripts.

Inputs are represented by their index I(x) = 2*x1 + x2 in {0,1,2,3}
(0 = easy input 00; 1,2,3 = hard inputs 01,10,11).
Outputs are pairs (y1, y2) in {0,1}^2, encoded as integers 0..3 via OUT.
"""
OUT = [(0, 0), (0, 1), (1, 0), (1, 1)]


def virt_alice(y):
    return (y[0], y[1], y[0] ^ y[1] ^ 1)


def virt_bob(y):
    return (y[0], y[1], y[0] ^ y[1])


def win(ia, ib, ya, yb):
    """Single-copy winning predicate W (ia, ib are indices; ya, yb are output pairs)."""
    if ia == 0 or ib == 0:
        return 1
    return int(virt_bob(yb)[ia - 1] == virt_alice(ya)[ib - 1])


# Constant single-copy strategies for each 2-element set of hard Alice indices,
# keyed by the MISSING index m in {1,2,3}. Alice always outputs (1,1).
# (Verified exhaustively in single_copy.py.)
PAIR_STRATEGY = {
    3: {"alice": (1, 1), "bob": (1, 1)},  # S = {1,2} = {01,10}
    2: {"alice": (1, 1), "bob": (1, 0)},  # S = {1,3} = {01,11}
    1: {"alice": (1, 1), "bob": (0, 1)},  # S = {2,3} = {10,11}
}
