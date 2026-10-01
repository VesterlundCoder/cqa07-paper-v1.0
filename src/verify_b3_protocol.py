"""CQA07: Verify B=3 protocol for n=4.

CRITICAL TEST: If covering number = 8 = 2^3 for n=4, then B=3 should suffice.

This script:
1. Finds 8 covering patterns for {0,1,2}^4
2. Constructs a B=3 protocol from these patterns
3. Verifies perfect success exhaustively on the n=4 Zhao-Deng task

If this works, the conjecture B*(n,1) = n is FALSIFIED for n=4.
"""
from __future__ import annotations

import sys
import json
import itertools
import numpy as np
from itertools import product
from pathlib import Path

BASE = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(BASE / "wave7" / "cqa07" / "canonical_task"))

from generator import (
    INPUTS_2BIT, OUTPUTS_2BIT, index_function,
    alice_virtual, bob_virtual, subtask_win, task_win,
)


def find_covering_patterns_ilp(n: int, k: int = 3):
    """Find minimum covering set using ILP."""
    from scipy.optimize import milp, LinearConstraint, Bounds

    elements = list(product(range(k), repeat=n))
    patterns = list(product(range(k), repeat=n))
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
    constraints = LinearConstraint(A, lb=1, ub=np.inf)
    bounds = Bounds(lb=0, ub=1)
    integrality = np.ones(n_pat)

    result = milp(c, constraints=constraints, bounds=bounds, integrality=integrality)

    if result.success:
        chosen = []
        for j, p in enumerate(patterns):
            if result.x[j] > 0.5:
                chosen.append(p)
        return chosen
    return None


def verify_covering(patterns, n: int, k: int = 3):
    """Verify that patterns cover all elements of {0,...,k-1}^n."""
    elements = list(product(range(k), repeat=n))
    uncovered = []
    for e in elements:
        covered = False
        for p in patterns:
            if all(p[d] != e[d] for d in range(n)):
                covered = True
                break
        if not covered:
            uncovered.append(e)
    return len(uncovered) == 0, uncovered


# ============================================================
# Protocol construction
# ============================================================

# Map: I-value to pattern index
# I(x_A^i) = 0 (x=00): auto-win, no constraint
# I(x_A^i) = 1 (x=01): pattern index 0
# I(x_A^i) = 2 (x=10): pattern index 1
# I(x_A^i) = 3 (x=11): pattern index 2
I_TO_PATTERN_IDX = {1: 0, 2: 1, 3: 2}


def encode(x_A_bits, patterns, n):
    """Encode Alice input to message (pattern index).

    x_A_bits is a 2n-bit array. Each pair of bits is a subtask input.
    Returns the message m (index of covering pattern).
    """
    # Convert bits to I-values per subtask
    i_values = []
    for i in range(n):
        x_A_i = (int(x_A_bits[2*i]), int(x_A_bits[2*i+1]))
        i_values.append(index_function(x_A_i))

    # Find a pattern that covers this input
    # Pattern p covers input if for each subtask i with I in {1,2,3}:
    #   p[i] != I_TO_PATTERN_IDX[I(x_A^i)]
    # For subtasks with I=0 (x=00): no constraint
    for m, p in enumerate(patterns):
        valid = True
        for i in range(n):
            if i_values[i] == 0:  # auto-win, no constraint
                continue
            idx = I_TO_PATTERN_IDX[i_values[i]]
            if p[i] == idx:
                valid = False
                break
        if valid:
            return m

    # Should not happen if patterns form a valid covering
    return 0


def alice_output(x_A_bits, n):
    """Alice's output function. 

    For the constructive protocol, Alice outputs (0,0) per subtask.
    This means y_1^A = 0, y_2^A = 0, y_3^A = 0 XOR 0 XOR 1 = 1.
    """
    return np.zeros(2 * n, dtype=int)


def bob_decode(x_B_bits, m, patterns, n):
    """Bob's decode function.

    For each subtask i, Bob knows:
    - x_B^i (his input)
    - m (the message, which tells him the pattern p)
    - p[i] = the excluded I-value for subtask i

    Bob needs to choose y_B^i such that for all x_A^i in the class:
      y_{I(x_A^i)}^B == y_{I(x_B^i)}^A

    Since Alice outputs (0,0), we have:
      y_1^A = 0, y_2^A = 0, y_3^A = 1

    So Bob needs:
      y_{I(x_A^i)}^B == y_{I(x_B^i)}^A

    where y_{I(x_B^i)}^A is determined by Alice's output (0,0):
      If I(x_B^i) = 0: auto-win, no constraint
      If I(x_B^i) = 1: y_1^A = 0
      If I(x_B^i) = 2: y_2^A = 0
      If I(x_B^i) = 3: y_3^A = 1

    So Bob needs y_{I(x_A^i)}^B to equal:
      0 if I(x_B^i) in {1, 2}
      1 if I(x_B^i) = 3

    The class for subtask i excludes pattern value p[i], meaning
    I(x_A^i) can be any of {1,2,3} except the one mapped by p[i].
    So I(x_A^i) is in a 2-element subset of {1,2,3}.

    Bob needs to choose y_B^i = (y_1^B, y_2^B) such that:
      y_{I(x_A^i)}^B == target for all possible I(x_A^i) in the class

    where target = 0 if I(x_B^i) in {1,2}, 1 if I(x_B^i) = 3.

    The possible I(x_A^i) values are {1,2,3} \ {PATTERN_IDX_TO_I[p[i]]}.
    Bob's virtual output: y_1^B, y_2^B, y_3^B = y_1^B XOR y_2^B.

    Bob needs y_j^B == target for all j in the possible set.
    """
    y_B = np.zeros(2 * n, dtype=int)

    p = patterns[m]

    for i in range(n):
        x_B_i = (int(x_B_bits[2*i]), int(x_B_bits[2*i+1]))
        I_B = index_function(x_B_i)

        if I_B == 0:  # auto-win
            y_B[2*i] = 0
            y_B[2*i+1] = 0
            continue

        # Target value
        if I_B in [1, 2]:
            target = 0  # y_{I_B}^A = 0
        else:  # I_B == 3
            target = 1  # y_3^A = 1

        # Possible I(x_A^i) values: {1,2,3} \ {excluded}
        excluded_idx = p[i]  # pattern index (0, 1, or 2)
        # Map back: pattern idx 0 -> I=1, 1 -> I=2, 2 -> I=3
        excluded_I = excluded_idx + 1
        possible_I = [j for j in [1, 2, 3] if j != excluded_I]

        # Bob needs y_j^B == target for all j in possible_I
        # y_1^B = y_B[2*i], y_2^B = y_B[2*i+1], y_3^B = y_1^B XOR y_2^B

        # Find y_1^B, y_2^B such that y_j^B == target for all j in possible_I
        found = False
        for y1 in [0, 1]:
            for y2 in [0, 1]:
                y3 = y1 ^ y2
                virtual = {1: y1, 2: y2, 3: y3}
                if all(virtual[j] == target for j in possible_I):
                    y_B[2*i] = y1
                    y_B[2*i+1] = y2
                    found = True
                    break
            if found:
                break

        if not found:
            # This should not happen if the protocol is correct
            y_B[2*i] = 0
            y_B[2*i+1] = 0

    return y_B


def verify_protocol_exhaustive(patterns, n):
    """Verify protocol achieves perfect success by exhaustive enumeration."""
    total = 0
    wins = 0
    failures = []

    for x_bits in product([0, 1], repeat=4 * n):
        x = np.array(x_bits, dtype=int)
        X_A = x[:2 * n]
        X_B = x[2 * n:]

        m = encode(X_A, patterns, n)
        Y_A = alice_output(X_A, n)
        Y_B = bob_decode(X_B, m, patterns, n)
        y = np.concatenate([Y_A, Y_B])

        if task_win(x, y, n):
            wins += 1
        else:
            if len(failures) < 10:
                failures.append((x.copy(), m, Y_A.copy(), Y_B.copy()))
        total += 1

    return wins, total, failures


def main():
    print("=" * 70)
    print("CQA07: Verify B=3 protocol for n=4")
    print("=" * 70)

    n = 4

    # Step 1: Find covering patterns
    print(f"\n--- Step 1: Find covering patterns for n={n} ---")
    patterns = find_covering_patterns_ilp(n)
    if patterns is None:
        print("  FAILED to find covering patterns")
        return

    print(f"  Found {len(patterns)} patterns:")
    for i, p in enumerate(patterns):
        print(f"    Pattern {i}: {p}")

    # Step 2: Verify covering
    print(f"\n--- Step 2: Verify covering ---")
    valid, uncovered = verify_covering(patterns, n)
    if valid:
        print(f"  All {3**n} elements covered. Valid covering!")
    else:
        print(f"  ERROR: {len(uncovered)} elements uncovered!")
        for e in uncovered[:5]:
            print(f"    Uncovered: {e}")
        return

    # Step 3: Verify protocol exhaustively
    print(f"\n--- Step 3: Verify protocol exhaustively (n={n}) ---")
    print(f"  Enumerating all {2**(4*n)} = {2**(4*n)} inputs...")
    wins, total, failures = verify_protocol_exhaustive(patterns, n)
    score = wins / total
    print(f"  Score: {wins}/{total} = {score:.6f}")

    if score == 1.0:
        print(f"\n  *** PERFECT SUCCESS with B=3 for n=4! ***")
        print(f"  This FALSIFIES the conjecture B*(n,1) = n for n=4!")
        print(f"  B*(4,1) <= 3, not 4!")
    else:
        print(f"\n  Protocol does NOT achieve perfect success.")
        print(f"  Failures: {len(failures)}")
        for x, m, y_A, y_B in failures[:5]:
            print(f"    x={x}, m={m}, y_A={y_A}, y_B={y_B}")

    # Step 4: Also test n=1,2,3
    print(f"\n--- Step 4: Test all n=1,2,3,4 ---")
    for n_test in [1, 2, 3, 4]:
        patterns_test = find_covering_patterns_ilp(n_test)
        if patterns_test is None:
            print(f"  n={n_test}: FAILED to find patterns")
            continue

        valid, _ = verify_covering(patterns_test, n_test)
        if not valid:
            print(f"  n={n_test}: Invalid covering")
            continue

        wins, total, failures = verify_protocol_exhaustive(patterns_test, n_test)
        score = wins / total
        n_patterns = len(patterns_test)
        n_bits = int(np.ceil(np.log2(n_patterns))) if n_patterns > 0 else 0
        print(f"  n={n_test}: {n_patterns} patterns, B={n_bits}, score={score:.6f}, "
              f"{'PERFECT' if score == 1.0 else 'IMPERFECT'}")

    # Step 5: Check Fibonacci pattern
    print(f"\n--- Step 5: Fibonacci pattern check ---")
    fib = [1, 1]
    for i in range(20):
        fib.append(fib[-1] + fib[-2])

    print(f"  n | covering_num | Fibonacci(n+2) | B = ceil(log2(cn)) | n (conjecture)")
    print(f"  --|-------------|----------------|-------------------|-------------")
    for n_test in [1, 2, 3, 4]:
        patterns_test = find_covering_patterns_ilp(n_test)
        cn = len(patterns_test) if patterns_test else -1
        fib_val = fib[n_test + 2]
        b_bound = int(np.ceil(np.log2(cn))) if cn > 0 else -1
        print(f"  {n_test} | {cn:11d} | {fib_val:14d} | {b_bound:17d} | {n_test:11d}")


if __name__ == "__main__":
    main()
