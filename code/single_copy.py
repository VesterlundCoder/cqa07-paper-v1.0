"""Exhaustive single-copy checks: S_1(0), Lemma 1, and the strategies of Table 1."""
import itertools, json, pathlib
from task import OUT, win, virt_alice, virt_bob, PAIR_STRATEGY

out = {}
# S_1(0): all 4^4 Alice x 4^4 Bob deterministic strategies
best, count = 0, 0
for fa in itertools.product(OUT, repeat=4):
    for gb in itertools.product(OUT, repeat=4):
        s = sum(win(a, b, fa[a], gb[b]) for a in range(4) for b in range(4))
        count += 1
        best = max(best, s)
out["S1_0"] = {"numerator": best, "denominator": 16, "strategy_pairs_enumerated": count}

# Lemma 1: number of (f on S, g on all 4 Bob inputs) that win on S x {0,1,2,3}
lemma1 = {}
for S in [(1, 2), (1, 3), (2, 3), (1, 2, 3)]:
    n_sol = 0
    for fs in itertools.product(OUT, repeat=len(S)):
        for gs in itertools.product(OUT, repeat=4):
            if all(win(ia, ib, fs[k], gs[ib]) for k, ia in enumerate(S) for ib in range(4)):
                n_sol += 1
    lemma1[str(S)] = n_sol
out["lemma1_number_of_winning_strategies"] = lemma1
assert lemma1["(1, 2, 3)"] == 0 and all(lemma1[str(S)] > 0 for S in [(1, 2), (1, 3), (2, 3)])

# Table 2: constant strategies
tab = {}
for m, st in PAIR_STRATEGY.items():
    S = tuple(i for i in (1, 2, 3) if i != m)
    fails = [(ia, ib) for ia in S for ib in range(4) if not win(ia, ib, st["alice"], st["bob"])]
    tab[str(S)] = {"alice": st["alice"], "alice_virtual": virt_alice(st["alice"]),
                   "bob": st["bob"], "bob_virtual": virt_bob(st["bob"]), "failures": fails}
    assert not fails
out["table2"] = tab

p = pathlib.Path(__file__).resolve().parents[1] / "data" / "single_copy.json"
p.write_text(json.dumps(out, indent=2))
print(json.dumps(out, indent=2))
