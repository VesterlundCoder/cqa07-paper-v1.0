"""Lower bound on S_2(0) (no communication, n = 2) by alternating best-response search.

This is a heuristic search: it yields a certified LOWER bound (the returned
strategy pair is re-scored independently), not a proof of optimality.
"""
import itertools, json, pathlib
import numpy as np
from task import OUT, win

N, RESTARTS, SEED = 2, 4000, 0
X = list(itertools.product(range(4), repeat=N))   # input index tuples
O = list(itertools.product(range(4), repeat=N))   # output code tuples
w1 = np.array([[[[win(a, b, OUT[i], OUT[j]) for j in range(4)] for i in range(4)]
                for b in range(4)] for a in range(4)], dtype=np.int64)
P = np.ones((len(X), len(X), len(O), len(O)), dtype=np.int64)
for c in range(N):
    xa = np.array([x[c] for x in X]); xb = xa
    oa = np.array([o[c] for o in O]); ob = oa
    P *= w1[xa[:, None, None, None], xb[None, :, None, None], oa[None, None, :, None], ob[None, None, None, :]]

rng = np.random.default_rng(SEED)
hist, best, best_s = {}, -1, None
K = len(X)
for _ in range(RESTARTS):
    g = rng.integers(0, len(O), K)
    prev = -1
    while True:
        A = P[:, np.arange(K), :, g].sum(axis=0)          # (xb, xa, oa) -> sum over xb
        f = A.argmax(axis=1)
        B = P[np.arange(K), :, f, :].sum(axis=0)          # (xa, xb, ob) -> sum over xa
        g = B.argmax(axis=1)
        val = int(B.max(axis=1).sum())
        if val <= prev:
            break
        prev = val
    hist[val] = hist.get(val, 0) + 1
    if val > best:
        best, best_s = val, (f.copy(), g.copy())

f, g = best_s
alice = {"".join(map(str, X[i])): [OUT[o] for o in O[f[i]]] for i in range(K)}
bob = {"".join(map(str, X[i])): [OUT[o] for o in O[g[i]]] for i in range(K)}
# independent pure-Python re-score
score = 0
for xa in X:
    for xb in X:
        ya = alice["".join(map(str, xa))]; yb = bob["".join(map(str, xb))]
        score += all(win(xa[c], xb[c], tuple(ya[c]), tuple(yb[c])) for c in range(N))
assert score == best
out = {"n": N, "best_wins": best, "total_pairs": K * K, "product_strategy_wins": 15 ** N,
       "status": "lower bound (heuristic search, not proven optimal)",
       "restarts": RESTARTS, "seed": SEED, "histogram_of_local_optima": {str(k): v for k, v in sorted(hist.items())},
       "input_key": "string of input indices I(x_1)I(x_2); outputs listed per coordinate as (y1,y2)",
       "alice_strategy": alice, "bob_strategy": bob}
pathlib.Path(__file__).resolve().parents[1].joinpath("data", "no_comm_n2.json").write_text(json.dumps(out, indent=1))
print(f"S_2(0) >= {best}/{K*K}  (product strategy: {15**N}/{K*K})"); print(out["histogram_of_local_optima"])
