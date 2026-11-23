"""Binary-subcube covering numbers f(n,3) = gamma_t(K_3^{x n}) by integer programming.

Variable z_a for each centre a in Z_3^n; subcube Q_a = {x : x_i != a_i for all i}.
Constraint: every x is in at least one chosen Q_a. (This single formulation is
identical to total domination in K_3^{x n}, since Q_a is the open neighbourhood of a.)
Solver status, objective and dual bound are recorded verbatim; a value is called
exact only if the solver proved optimality.
"""
import itertools, json, pathlib, sys, time
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import lil_matrix

NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 6
TL = float(sys.argv[2]) if len(sys.argv) > 2 else 120
results = []
for n in range(1, NMAX + 1):
    V = list(itertools.product(range(3), repeat=n)); idx = {v: i for i, v in enumerate(V)}
    A = lil_matrix((len(V), len(V)))
    for x in V:
        for a in itertools.product(*[[c for c in range(3) if c != xi] for xi in x]):
            A[idx[x], idx[a]] = 1
    t = time.time()
    r = milp(np.ones(len(V)), constraints=LinearConstraint(A.tocsr(), lb=1), integrality=np.ones(len(V)),
             bounds=Bounds(0, 1), options={"time_limit": TL, "mip_rel_gap": 0.0, "threads": 1, "random_seed": 0})
    centres = [V[i] for i in range(len(V)) if r.x is not None and r.x[i] > 0.5]
    # independent check that the returned centres cover Z_3^n
    covered = all(any(all(x[i] != a[i] for i in range(n)) for a in centres) for x in V)
    if r.x is not None:
        assert covered, "Returned cover is not feasible"
        assert np.max(np.abs(r.x-np.round(r.x))) < 1e-5
    rec = {"n": n, "status_code": int(r.status), "message": r.message,
           "proven_optimal": bool(r.status == 0),
           "best_cover_size": len(centres), "cover_verified": covered,
           "dual_bound": float(np.ceil(r.mip_dual_bound - 1e-6)) if getattr(r, "mip_dual_bound", None) is not None else None,
           "raw_objective": None if r.fun is None else float(r.fun),
           "raw_dual_bound": None if getattr(r, "mip_dual_bound", None) is None else float(r.mip_dual_bound),
           "mip_gap": None if getattr(r, "mip_gap", None) is None else float(r.mip_gap),
           "mip_node_count": None if getattr(r, "mip_node_count", None) is None else int(r.mip_node_count),
           "counting_bound": int(np.ceil(1.5 ** n - 1e-12)), "time_s": round(time.time() - t, 2),
           "centres": ["".join(map(str, a)) for a in centres]}
    results.append(rec)
    print({k: v for k, v in rec.items() if k != "centres"}, flush=True)
out = {"solver": "HiGHS via scipy.optimize.milp", "time_limit_s_per_instance": TL,
       "solver_options": {"mip_rel_gap": 0.0, "threads": 1, "random_seed": 0}, "results": results}
pathlib.Path(__file__).resolve().parents[1].joinpath("data", "covering.json").write_text(json.dumps(out, indent=1))
