"""CQA07: Zhao-Deng message-guessing sanity test.

For any perfect B-bit protocol, we can construct a no-communication
protocol by having Bob guess the message uniformly at random.

The no-communication success probability must be at least 2^{-B}.

Zhao-Deng requires that no-communication success decays exponentially:
S_n(0) = (15/16)^n.

Therefore: 2^{-B*(n,1)} <= S_n(0) = (15/16)^n

Which gives: B*(n,1) >= n * log2(16/15) ≈ 0.093n

This is a weaker bound than the counting bound (0.585n), but it is
an INDEPENDENT consistency check derived from Zhao-Deng's technique.

If this check fails for any n, something is wrong with the protocol
or the B* computation.
"""
import numpy as np
import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[3]


def run_sanity_check():
    print("=" * 70)
    print("CQA07: Zhao-Deng Message-Guessing Sanity Test")
    print("=" * 70)

    # Known gamma values (exact for n=1..5, upper bound for n=6,7)
    gamma_values = {
        1: 2,
        2: 3,
        3: 5,
        4: 8,
        5: 12,
        6: 18,  # upper bound
        7: 29,  # upper bound
    }

    print("\nZhao-Deng technique: If B* bits achieve perfect success,")
    print("then Bob can guess the message to get a no-comm protocol")
    print("with success >= 2^{-B*}.")
    print()
    print("No-comm upper bound: S_n(0) = (15/16)^n")
    print()
    print("Sanity check: 2^{-B*} <= (15/16)^n")
    print("  i.e., B* >= n * log2(16/15) ≈ 0.093n")
    print()

    log2_16_15 = np.log2(16 / 15)
    print(f"log2(16/15) = {log2_16_15:.6f}")
    print()

    print(f"{'n':<5s} {'gamma(n)':<12s} {'B*':<8s} {'2^{-B*}':<15s} "
          f"{'(15/16)^n':<15s} {'Check?':<10s} {'B*/n':<10s} {'0.093n'}")
    print("-" * 85)

    all_pass = True
    results = {}

    for n, gamma in gamma_values.items():
        b_star = int(np.ceil(np.log2(gamma)))
        no_comm_from_protocol = 2 ** (-b_star)
        no_comm_upper = (15 / 16) ** n
        check = no_comm_from_protocol <= no_comm_upper
        rate = b_star / n
        zhao_deng_bound = n * log2_16_15

        if not check:
            all_pass = False

        check_str = "PASS" if check else "FAIL"
        print(f"{n:<5d} {gamma:<12d} {b_star:<8d} {no_comm_from_protocol:<15.6e} "
              f"{no_comm_upper:<15.6e} {check_str:<10s} {rate:<10.4f} {zhao_deng_bound:<.4f}")

        results[n] = {
            "gamma": gamma,
            "b_star": b_star,
            "no_comm_from_protocol": no_comm_from_protocol,
            "no_comm_upper_bound": no_comm_upper,
            "check_passes": check,
            "rate_b_over_n": rate,
            "zhao_deng_lower_bound": zhao_deng_bound,
        }

    print()
    if all_pass:
        print("ALL CHECKS PASS — Zhao-Deng consistency verified.")
    else:
        print("SOME CHECKS FAILED — investigate!")

    print()
    print("Summary of bounds on B*(n,1)/n:")
    print(f"  Zhao-Deng (message guessing): B*/n >= {log2_16_15:.4f}")
    print(f"  Counting bound:               B*/n >= {np.log2(3/2):.4f}")
    print(f"  Rall upper bound:             B*/n <= 1.0")
    print(f"  Observed range:               0.71 - 1.0")

    # Save
    results_path = BASE / "wave7" / "cqa07" / "proof" / "zhao_deng_sanity.json"
    with open(results_path, "w") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\n  Results saved to {results_path}")

    return results


if __name__ == "__main__":
    run_sanity_check()
