"""Exhaustive check of the covering-based one-way protocol for n = 1..NMAX.

Uses the optimal covers stored in data/covering.json. For each Alice input X_A
(in {0,1,2,3}^n, index form) Alice completes easy coordinates to index 1, finds a
centre a with I(x_i) - 1 != a_i for all i, sends the centre's label, and both
parties play the constant strategy PAIR_STRATEGY[a_i + 1] in each coordinate.
Every one of the 4^n * 4^n input pairs is tested. This verifies the UPPER bound
B*(n,1) <= ceil(log2 f(n,3)); the matching lower bound is the proof in the paper.
"""
import itertools, json, math, pathlib, sys
from task import win, PAIR_STRATEGY

root = pathlib.Path(__file__).resolve().parents[1]
cov = {r["n"]: r for r in json.loads((root / "data" / "covering.json").read_text())["results"]}
NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 4
out = []
for n in range(1, NMAX + 1):
    assert cov[n]["proven_optimal"]
    centres = [tuple(int(c) for c in s) for s in cov[n]["centres"]]
    bits = math.ceil(math.log2(len(centres))) if len(centres) > 1 else 0

    def encode(xa):
        h = tuple(i - 1 if i else 0 for i in xa)          # completion rho: 00 -> 01, then ternary symbol
        return next(k for k, a in enumerate(centres) if all(h[i] != a[i] for i in range(n)))

    X = list(itertools.product(range(4), repeat=n))
    msgs = {xa: encode(xa) for xa in X}
    assert max(msgs.values()) < 2 ** bits
    fails = 0
    for xa in X:
        a = centres[msgs[xa]]
        ya = [PAIR_STRATEGY[a[i] + 1]["alice"] for i in range(n)]
        yb = [PAIR_STRATEGY[a[i] + 1]["bob"] for i in range(n)]   # Bob's output depends only on the message here
        for xb in X:
            fails += not all(win(xa[i], xb[i], ya[i], yb[i]) for i in range(n))
    rec = {"n": n, "cover_size": len(centres), "message_bits": bits, "input_pairs_tested": len(X) ** 2,
           "failures": fails, "messages_used": len(set(msgs.values()))}
    assert fails == 0, "Constructed protocol failed an input pair"
    out.append(rec); print(rec, flush=True)
(root / "data" / "protocol_check.json").write_text(json.dumps(out, indent=1))
