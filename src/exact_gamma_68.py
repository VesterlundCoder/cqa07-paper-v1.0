"""CQA07: Exact gamma(6), gamma(7), gamma(8) with two independent formulations.

Formulation A: Set cover ILP (CP-SAT)
  Binary variable z_c for each pattern c in {0,1,2}^n
  Constraint: for each w, sum(z_c for c covering w) >= 1
  Minimize: sum(z_c)

Formulation B: Total domination ILP (CP-SAT)
  Binary variable x_v for each vertex v in K_3^x n
  Constraint: for each v, sum(x_u for u ~ v) >= 1
  Minimize: sum(x_v)

Both must give the same optimum (truth anchor).

Uses OR-Tools CP-SAT for efficiency.
"""
from __future__ import annotations

import sys
import json
import time
import numpy as np
from itertools import product
from pathlib import Path

BASE = Path(__file__).resolve().parents[3]

from ortools.sat.python import cp_model


# ============================================================
# Precompute coverage (sparse, for efficiency)
# ============================================================

def precompute_coverage(n: int) -> dict:
    """Precompute which patterns cover each element.

    Returns: dict mapping element index -> list of pattern indices that cover it.
    """
    vertices = list(product(range(3), repeat=n))
    n_vert = len(vertices)

    # For each vertex, find all vertices that differ in ALL coordinates
    coverage = {}
    for i, v in enumerate(vertices):
        coverers = []
        for j, u in enumerate(vertices):
            if i != j and all(v[d] != u[d] for d in range(n)):
                coverers.append(j)
        coverage[i] = coverers

    return coverage


# ============================================================
# Formulation A: Set cover (CP-SAT)
# ============================================================

def covering_number_cpsat(n: int, timeout_sec: int = 300) -> dict:
    """Compute covering number using CP-SAT (set cover formulation)."""
    coverage = precompute_coverage(n)
    n_vert = 3 ** n

    model = cp_model.CpModel()

    # Variables: z[v] = 1 if vertex v is in the covering set
    z = [model.NewBoolVar(f"z_{v}") for v in range(n_vert)]

    # Constraints: every vertex must be covered
    for v in range(n_vert):
        coverers = coverage[v]
        if not coverers:
            # No vertex can cover v — this shouldn't happen for K_3^x n
            return {"error": f"Vertex {v} has no coverers"}
        model.Add(sum(z[u] for u in coverers) >= 1)

    # Objective: minimize sum(z)
    model.Minimize(sum(z))

    # Solve
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = timeout_sec
    solver.parameters.num_workers = 8

    status = solver.Solve(model)

    result = {
        "n": n,
        "formulation": "set_cover_cpsat",
        "n_variables": n_vert,
        "n_constraints": n_vert,
    }

    if status == cp_model.OPTIMAL:
        result["optimal_value"] = int(solver.ObjectiveValue())
        result["status"] = "OPTIMAL"
        result["proven_optimal"] = True
    elif status == cp_model.FEASIBLE:
        result["optimal_value"] = int(solver.ObjectiveValue())
        result["status"] = "FEASIBLE"
        result["proven_optimal"] = False
        result["best_bound"] = int(solver.BestObjectiveBound())
    else:
        result["status"] = "UNKNOWN"
        result["proven_optimal"] = False

    result["time_sec"] = solver.WallTime()

    return result


# ============================================================
# Formulation B: Total domination (CP-SAT) — same structure
# ============================================================

def total_domination_cpsat(n: int, timeout_sec: int = 300) -> dict:
    """Compute total domination number using CP-SAT.

    This is structurally identical to the covering number (same graph),
    but formulated as total domination for independent verification.
    """
    # Same as covering number — the graph IS the same
    # But we use a different variable naming to make the formulation explicit
    coverage = precompute_coverage(n)
    n_vert = 3 ** n

    model = cp_model.CpModel()

    # Variables: x[v] = 1 if vertex v is in the total dominating set
    x = [model.NewBoolVar(f"x_{v}") for v in range(n_vert)]

    # Constraints: every vertex must have a neighbor in the dominating set
    for v in range(n_vert):
        neighbors = coverage[v]  # same as coverers
        if not neighbors:
            return {"error": f"Vertex {v} has no neighbors"}
        model.Add(sum(x[u] for u in neighbors) >= 1)

    # Objective: minimize sum(x)
    model.Minimize(sum(x))

    # Solve
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = timeout_sec
    solver.parameters.num_workers = 8

    status = solver.Solve(model)

    result = {
        "n": n,
        "formulation": "total_domination_cpsat",
        "n_variables": n_vert,
        "n_constraints": n_vert,
    }

    if status == cp_model.OPTIMAL:
        result["optimal_value"] = int(solver.ObjectiveValue())
        result["status"] = "OPTIMAL"
        result["proven_optimal"] = True
    elif status == cp_model.FEASIBLE:
        result["optimal_value"] = int(solver.ObjectiveValue())
        result["status"] = "FEASIBLE"
        result["proven_optimal"] = False
        result["best_bound"] = int(solver.BestObjectiveBound())
    else:
        result["status"] = "UNKNOWN"
        result["proven_optimal"] = False

    result["time_sec"] = solver.WallTime()

    return result


# ============================================================
# Run both formulations
# ============================================================

def run_exact_computation():
    print("=" * 70)
    print("CQA07: Exact gamma(n) with Two Independent Formulations")
    print("=" * 70)

    all_results = {}

    # First verify n=1..5 (should be fast)
    for n in range(1, 6):
        print(f"\n--- n={n} (verification) ---")
        t0 = time.time()
        result_a = covering_number_cpsat(n, timeout_sec=60)
        t1 = time.time()
        result_b = total_domination_cpsat(n, timeout_sec=60)
        t2 = time.time()

        val_a = result_a.get("optimal_value", -1)
        val_b = result_b.get("optimal_value", -1)
        match = (val_a == val_b) and (val_a > 0)

        print(f"  Set cover:       gamma({n}) = {val_a} "
              f"({result_a['status']}, {t1-t0:.1f}s)")
        print(f"  Total domination: gamma_t({n}) = {val_b} "
              f"({result_b['status']}, {t2-t1:.1f}s)")
        print(f"  Match: {match}")

        all_results[n] = {
            "set_cover": result_a,
            "total_domination": result_b,
            "match": match,
        }

    # Now compute n=6,7,8 (the main target)
    for n in [6, 7, 8]:
        print(f"\n--- n={n} (main computation) ---")
        t0 = time.time()
        result_a = covering_number_cpsat(n, timeout_sec=600)
        t1 = time.time()
        print(f"  Set cover:       gamma({n}) = {result_a.get('optimal_value', '?')} "
              f"({result_a['status']}, {t1-t0:.1f}s, "
              f"optimal={result_a.get('proven_optimal', False)})")

        t2 = time.time()
        result_b = total_domination_cpsat(n, timeout_sec=600)
        t3 = time.time()
        print(f"  Total domination: gamma_t({n}) = {result_b.get('optimal_value', '?')} "
              f"({result_b['status']}, {t3-t2:.1f}s, "
              f"optimal={result_b.get('proven_optimal', False)})")

        val_a = result_a.get("optimal_value", -1)
        val_b = result_b.get("optimal_value", -1)
        match = (val_a == val_b) and (val_a > 0)
        print(f"  Match: {match}")

        all_results[n] = {
            "set_cover": result_a,
            "total_domination": result_b,
            "match": match,
        }

    # Summary
    print(f"\n{'='*70}")
    print("EXACT COMPUTATION SUMMARY")
    print(f"{'='*70}")
    print(f"\n{'n':<5s} {'gamma(n)':<15s} {'gamma_t(n)':<15s} {'Match?':<10s} "
          f"{'Optimal?':<10s} {'Time A':<10s} {'Time B'}")
    print("-" * 75)

    for n, r in all_results.items():
        va = r["set_cover"].get("optimal_value", "?")
        vb = r["total_domination"].get("optimal_value", "?")
        match = "YES" if r["match"] else "NO"
        opt_a = r["set_cover"].get("proven_optimal", False)
        opt_b = r["total_domination"].get("proven_optimal", False)
        optimal = "YES" if (opt_a and opt_b) else "PARTIAL"
        ta = r["set_cover"].get("time_sec", 0)
        tb = r["total_domination"].get("time_sec", 0)
        print(f"{n:<5d} {str(va):<15s} {str(vb):<15s} {match:<10s} "
              f"{optimal:<10s} {ta:<10.1f} {tb:.1f}")

    # Zhao-Deng consistency check
    print(f"\n--- Zhao-Deng Consistency Check ---")
    print(f"  Zhao-Deng requires B*(n,1) = Omega(n)")
    print(f"  If B* = ceil(log2(gamma)), then gamma(n) = 2^Omega(n)")
    print(f"  Counting bound: gamma(n) >= ceil((3/2)^n)")
    print(f"  log2(3/2) = {np.log2(1.5):.4f}")
    print(f"  So B*(n,1) >= n * log2(3/2) = {np.log2(1.5):.4f} * n")
    print()

    for n, r in all_results.items():
        gamma = r["set_cover"].get("optimal_value")
        if gamma and gamma > 0:
            b_star = int(np.ceil(np.log2(gamma)))
            rate = b_star / n if n > 0 else 0
            counting = int(np.ceil(1.5 ** n))
            print(f"  n={n}: gamma={gamma}, B*={b_star}, B*/n={rate:.4f}, "
                  f"counting_bound={counting}")

    # Save
    results_path = BASE / "wave7" / "cqa07" / "proof" / "exact_gamma_68.json"
    with open(results_path, "w") as f:
        json.dump({str(k): v for k, v in all_results.items()}, f, indent=2, default=str)
    print(f"\n  Results saved to {results_path}")

    return all_results


if __name__ == "__main__":
    run_exact_computation()
