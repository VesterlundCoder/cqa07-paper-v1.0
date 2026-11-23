"""Exact S_2(0) via a mixed-integer program (HiGHS through SciPy).

Variables: a[xa,oa], b[xb,ob] binary (one output per input), z[xa,xb] in [0,1].
Constraint for every (xa, xb, ob):  z[xa,xb] <= sum_{oa : win} a[xa,oa] + 1 - b[xb,ob].
Maximise sum z. The solver status and dual bound are recorded verbatim.
"""
import itertools, json, pathlib, sys, time
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import lil_matrix
from task import OUT, win

N = 2; TL = float(sys.argv[1]) if len(sys.argv) > 1 else 600
X = list(itertools.product(range(4), repeat=N)); O = list(itertools.product(range(4), repeat=N))
K, L = len(X), len(O)
def W(xa, xb, oa, ob):
    return all(win(xa[c], xb[c], OUT[oa[c]], OUT[ob[c]]) for c in range(N))
na = K * L; nb = K * L; nz = K * K; nv = na + nb + nz
ia = lambda x, o: x * L + o; ib = lambda x, o: na + x * L + o; iz = lambda x, y: na + nb + x * K + y
rows = []; A = lil_matrix((K * K * L + 2 * K, nv)); lb = []; ub = []; r = 0
for x in range(K):
    for y in range(K):
        for ob in range(L):
            A[r, iz(x, y)] = 1; A[r, ib(y, ob)] = 1
            for oa in range(L):
                if W(X[x], X[y], O[oa], O[ob]):
                    A[r, ia(x, oa)] = -1
            lb.append(-np.inf); ub.append(1); r += 1
for x in range(K):
    for o in range(L): A[r, ia(x, o)] = 1
    lb.append(1); ub.append(1); r += 1
for y in range(K):
    for o in range(L): A[r, ib(y, o)] = 1
    lb.append(1); ub.append(1); r += 1
c = np.zeros(nv); c[na + nb:] = -1
integ = np.zeros(nv); integ[:na + nb] = 1
# No extra symmetry-breaking constraint is imposed.
bnd_lo = np.zeros(nv); bnd_hi = np.ones(nv)
t = time.time()
res = milp(c, constraints=LinearConstraint(A.tocsr(), lb, ub), integrality=integ,
           bounds=Bounds(bnd_lo, bnd_hi), options={"time_limit": TL, "disp": True,
                                                  "mip_rel_gap": 0.0, "threads": 1, "random_seed": 0})
verified_wins = None
alice = bob = None
if res.x is not None:
    aa = res.x[:na].reshape(K,L); bb = res.x[na:na+nb].reshape(K,L)
    assert np.max(np.abs(res.x[:na+nb]-np.round(res.x[:na+nb]))) < 1e-5
    assert np.allclose(aa.sum(axis=1),1) and np.allclose(bb.sum(axis=1),1)
    alice = aa.argmax(axis=1).tolist(); bob = bb.argmax(axis=1).tolist()
    verified_wins = sum(W(X[x],X[y],O[alice[x]],O[bob[y]]) for x in range(K) for y in range(K))
    assert verified_wins >= -res.fun-1e-5
out = {"n": N, "solver": "HiGHS via scipy.optimize.milp", "time_limit_s": TL, "time_s": round(time.time() - t, 1),
       "status_code": int(res.status), "message": res.message,
       "best_wins": None if res.x is None else int(round(-res.fun)),
       "upper_bound_wins": None if getattr(res, "mip_dual_bound", None) is None else float(-res.mip_dual_bound),
       "proven_optimal": bool(res.status == 0),
       "raw_minimization_objective": None if res.fun is None else float(res.fun),
       "raw_minimization_dual_bound": None if getattr(res, "mip_dual_bound", None) is None else float(res.mip_dual_bound),
       "mip_gap": None if getattr(res, "mip_gap", None) is None else float(res.mip_gap),
       "mip_node_count": None if getattr(res, "mip_node_count", None) is None else int(res.mip_node_count),
       "solver_options": {"mip_rel_gap": 0.0, "threads": 1, "random_seed": 0},
       "independently_rescored_incumbent_wins": verified_wins,
       "incumbent_alice_output_indices": alice, "incumbent_bob_output_indices": bob,
       "certificate_scope": "Solver bounds at floating-point tolerances; not an exported exact-arithmetic proof certificate"}
pathlib.Path(__file__).resolve().parents[1].joinpath("data", "no_comm_n2_exact.json").write_text(json.dumps(out, indent=1))
print(json.dumps(out, indent=1))
