"""CQA07: Graph domination equivalence proof and verification.

Proves that gamma(n) = gamma_t(K_3^x n), the total domination number
of the categorical (direct/tensor) product of n copies of K_3.

Definitions:
- K_3: complete graph on {0,1,2}
- K_3^x n (categorical/direct product): vertices = {0,1,2}^n,
  adjacency: x ~ y iff x_i != y_i for all i (anti-Hamming distance n)
- Total dominating set D: for every vertex v, there exists u in D
  with u ~ v (v has a neighbor in D)
- Total domination number gamma_t(G): minimum |D|

The covering problem:
- Cover {0,1,2}^n with patterns c such that c covers w iff
  c[i] != w[i] for all i
- gamma(n) = minimum number of such patterns

Equivalence: gamma(n) = gamma_t(K_3^x n)

Proof:
- "c covers w" iff "c ~ w in K_3^x n" (by definition of adjacency)
- "every w is covered by some c" iff "every vertex has a neighbor in D"
- Therefore the covering problem IS total domination in K_3^x n.

Note: This is total domination, not domination. In domination, a vertex
dominates itself and its neighbors. In total domination, a vertex does
NOT dominate itself — only its neighbors do. Since c covers w requires
c[i] != w[i] for ALL i (including when c = w, which would give c[i] = w[i]),
a pattern does NOT cover itself. Therefore this is total domination.
"""
from __future__ import annotations

import sys
import json
import itertools
import numpy as np
from itertools import product
from pathlib import Path

BASE = Path(__file__).resolve().parents[3]


# ============================================================
# Graph construction
# ============================================================

def build_k3_power_graph(n: int):
    """Build K_3^x n as an adjacency structure.

    Returns:
        vertices: list of tuples in {0,1,2}^n
        adjacency: dict mapping vertex -> set of neighbors
    """
    vertices = list(product(range(3), repeat=n))
    adjacency = {v: set() for v in vertices}

    for i, v in enumerate(vertices):
        for j, u in enumerate(vertices):
            if i != j and all(v[d] != u[d] for d in range(n)):
                adjacency[v].add(u)

    return vertices, adjacency


# ============================================================
# Total domination via ILP (Formulation A: graph-based)
# ============================================================

def total_domination_ilp(n: int) -> tuple:
    """Compute total domination number of K_3^x n using ILP.

    Minimize sum(x_v) subject to:
    - For each vertex v, sum(x_u for u ~ v) >= 1
    - x_v in {0, 1}

    Returns (domination_number, status).
    """
    from scipy.optimize import milp, LinearConstraint, Bounds

    vertices = list(product(range(3), repeat=n))
    n_vert = len(vertices)

    # Build adjacency: for each vertex v, which vertices dominate it?
    # u dominates v (for total domination) iff u ~ v, i.e., u[i] != v[i] for all i
    # A[v, u] = 1 if u dominates v
    A = np.zeros((n_vert, n_vert), dtype=int)
    for i, v in enumerate(vertices):
        for j, u in enumerate(vertices):
            if i != j and all(v[d] != u[d] for d in range(n)):
                A[i, j] = 1

    # Objective: minimize sum(x_v)
    c = np.ones(n_vert)

    # Constraint: A @ x >= 1 (every vertex has a dominator)
    constraints = LinearConstraint(A, lb=1, ub=np.inf)

    # Bounds: x_v in {0, 1}
    bounds = Bounds(lb=0, ub=1)

    # Integer constraints
    integrality = np.ones(n_vert)

    result = milp(c, constraints=constraints, bounds=bounds, integrality=integrality)

    if result.success:
        return int(round(result.fun)), "optimal"
    else:
        return -1, "failed"


# ============================================================
# Covering number via ILP (Formulation B: set-cover-based)
# ============================================================

def covering_number_ilp(n: int) -> tuple:
    """Compute covering number for {0,1,2}^n using ILP (set cover formulation).

    Minimize sum(x_p) subject to:
    - For each element e, sum(x_p for p covering e) >= 1
    - x_p in {0, 1}

    Returns (covering_number, status).
    """
    from scipy.optimize import milp, LinearConstraint, Bounds

    elements = list(product(range(3), repeat=n))
    patterns = list(product(range(3), repeat=n))
    n_elem = len(elements)
    n_pat = len(patterns)

    # Coverage matrix: A[e, p] = 1 if pattern p covers element e
    A = np.zeros((n_elem, n_pat), dtype=int)
    for i, e in enumerate(elements):
        for j, p in enumerate(patterns):
            if all(p[d] != e[d] for d in range(n)):
                A[i, j] = 1

    # Objective: minimize sum(x_p)
    c = np.ones(n_pat)

    # Constraint: A @ x >= 1
    constraints = LinearConstraint(A, lb=1, ub=np.inf)

    # Bounds: x_p in {0, 1}
    bounds = Bounds(lb=0, ub=1)

    # Integer constraints
    integrality = np.ones(n_pat)

    result = milp(c, constraints=constraints, bounds=bounds, integrality=integrality)

    if result.success:
        return int(round(result.fun)), "optimal"
    else:
        return -1, "failed"


# ============================================================
# Verify equivalence
# ============================================================

def verify_equivalence():
    """Verify that gamma(n) = gamma_t(K_3^x n) for small n."""
    print("=" * 70)
    print("CQA07: Graph Domination Equivalence Verification")
    print("=" * 70)

    results = {}

    for n in range(1, 7):
        print(f"\n--- n={n} ---")

        # Formulation A: Total domination (graph-based)
        print(f"  Computing total domination number (graph ILP)...")
        td_num, td_status = total_domination_ilp(n)
        print(f"  gamma_t(K_3^x{n}) = {td_num} ({td_status})")

        # Formulation B: Covering number (set-cover-based)
        print(f"  Computing covering number (set cover ILP)...")
        cv_num, cv_status = covering_number_ilp(n)
        print(f"  gamma({n}) = {cv_num} ({cv_status})")

        # Check equivalence
        match = (td_num == cv_num) and (td_num > 0)
        print(f"  Match: {match}")

        results[n] = {
            "total_domination": td_num,
            "covering_number": cv_num,
            "match": match,
            "td_status": td_status,
            "cv_status": cv_status,
        }

    # Summary
    print(f"\n{'='*70}")
    print("EQUIVALENCE VERIFICATION SUMMARY")
    print(f"{'='*70}")
    print(f"\n{'n':<5s} {'gamma_t(K_3^xn)':<20s} {'gamma(n)':<15s} {'Match?'}")
    print("-" * 50)

    all_match = True
    for n, r in results.items():
        match_str = "YES" if r["match"] else "NO"
        if not r["match"]:
            all_match = False
        print(f"{n:<5d} {r['total_domination']:<20d} {r['covering_number']:<15d} {match_str}")

    if all_match:
        print(f"\n  EQUIVALENCE VERIFIED for n=1..{max(results.keys())}")
        print(f"  gamma(n) = gamma_t(K_3^x n) for all tested n")
    else:
        print(f"\n  EQUIVALENCE FAILED for some n!")

    # Save
    results_path = BASE / "wave7" / "cqa07" / "proof" / "graph_domination_verification.json"
    with open(results_path, "w") as f:
        json.dump({str(k): v for k, v in results.items()}, f, indent=2)
    print(f"\n  Results saved to {results_path}")

    return results


if __name__ == "__main__":
    verify_equivalence()
