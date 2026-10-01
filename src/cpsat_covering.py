"""CQA07: Covering number using OR-Tools CP-SAT solver."""
from __future__ import annotations
import sys
import time
from itertools import product
from pathlib import Path
from ortools.sat.python import cp_model
import numpy as np
import json

BASE = Path(__file__).resolve().parents[3]


def covering_number_cpsat(n: int, k: int = 3, timeout: int = 120) -> int:
    """Compute covering number using OR-Tools CP-SAT."""
    elements = list(product(range(k), repeat=n))
    patterns = list(product(range(k), repeat=n))
    n_elem = len(elements)
    n_pat = len(patterns)
    
    # Precompute coverage
    covers = {}
    for i, e in enumerate(elements):
        covers[i] = []
        for j, p in enumerate(patterns):
            if all(p[d] != e[d] for d in range(n)):
                covers[i].append(j)
    
    model = cp_model.CpModel()
    
    # Variables: x[j] = 1 if pattern j is selected
    x = [model.NewBoolVar(f'x_{j}') for j in range(n_pat)]
    
    # Coverage constraints: for each element, at least one covering pattern
    for i in range(n_elem):
        model.Add(sum(x[j] for j in covers[i]) >= 1)
    
    # Objective: minimize number of patterns
    model.Minimize(sum(x))
    
    # Solve
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = timeout
    solver.parameters.num_search_workers = 8
    
    status = solver.Solve(model)
    
    if status in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
        return int(solver.ObjectiveValue())
    return -1


def main():
    print("CQA07: Covering number via OR-Tools CP-SAT")
    print("=" * 60)
    
    results = {}
    for n in range(1, 9):
        a000124 = n * (n - 1) // 2 + 2
        t0 = time.time()
        cn = covering_number_cpsat(n, timeout=120)
        t1 = time.time()
        b = int(np.ceil(np.log2(cn))) if cn > 0 else -1
        results[n] = cn
        print(f"  n={n}: cn={cn}, A000124={a000124}, match={cn==a000124}, B*={b}, time={t1-t0:.2f}s")
    
    print(f"\n  Sequence: {', '.join(str(results[n]) for n in range(1, 9))}")
    diffs = [results[n+1] - results[n] for n in range(1, 8)]
    print(f"  Differences: {diffs}")
    
    # A000124 check
    print(f"\n  A000124 check:")
    all_match = True
    for n in range(1, 9):
        a = n * (n - 1) // 2 + 2
        match = results[n] == a
        if not match:
            all_match = False
        print(f"    n={n}: cn={results[n]}, A000124={a}, match={match}")
    
    if all_match:
        print(f"\n  *** A000124 pattern CONFIRMED for n=1..8! ***")
        print(f"  γ(n) = n(n-1)/2 + 2")
        print(f"  B*(n,1) = ⌈log₂(n(n-1)/2 + 2)⌉ = O(log n)")
    else:
        print(f"\n  A000124 pattern BROKEN:")
        for n in range(1, 9):
            if results[n] != n * (n - 1) // 2 + 2:
                print(f"    n={n}: γ(n)={results[n]} ≠ {n*(n-1)//2+2} = A000124")
    
    # B* table
    print(f"\n  n | γ(n) | B*(n,1) | n (old) | Falsified?")
    print(f"  --|------|---------|---------|----------")
    for n in range(1, 9):
        cn = results[n]
        b = int(np.ceil(np.log2(cn))) if cn > 0 else -1
        falsified = b < n
        print(f"  {n} | {cn:4d} | {b:7d} | {n:7d} | {'YES' if falsified else 'no':8s}")
    
    results_path = BASE / "wave7" / "cqa07" / "proof" / "covering_numbers_cpsat.json"
    with open(results_path, "w") as f:
        json.dump({str(k): v for k, v in results.items()}, f, indent=2)
    print(f"\n  Saved to {results_path}")


if __name__ == "__main__":
    main()
