"""CQA07: Reproduce all figures and tables for the manuscript."""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path

BASE = Path(__file__).resolve().parents[3]
PAPER = BASE / "wave7" / "cqa07" / "paper"
PAPER.mkdir(parents=True, exist_ok=True)

# Exact and bounded f(n,3) values from literature
# n=1: our computation; n=2..6: Adriaensen et al. (exact); n=7: Adriaensen (bounds); n=8: Kuang-Wang (bounds)
f_exact = {1: 2, 2: 3, 3: 5, 4: 8, 5: 12, 6: 18}
f_bounds = {7: (28, 30), 8: (41, 50)}

# B*(n,1) = ceil(log2(f(n,3))) — exact for all n<=8 since bounds lie in single power-of-2 intervals
b_star = {1: 1, 2: 2, 3: 3, 4: 3, 5: 4, 6: 5, 7: 5, 8: 6}

log2_32 = np.log2(3/2)


def figure1_conceptual_pipeline():
    """Figure 1: Conceptual reduction pipeline."""
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_title('Figure 1: Reduction Pipeline', fontsize=14, fontweight='bold')

    steps = [
        (5, 9, 'Zhao-Deng $n$-copy task'),
        (5, 7.5, 'Perfect message classes'),
        (5, 6, 'Coordinate-wise compatibility'),
        (5, 4.5, 'Binary subcubes of $\\{0,1,2\\}^n$'),
        (5, 3, 'Ternary-cube covering $f(n,3)$'),
        (5, 1.5, '$\\gamma_t(K_3^{\\times n})$'),
        (5, 0.3, '$B^* = \\lceil \\log_2 f(n,3) \\rceil$'),
    ]

    for x, y, label in steps:
        ax.text(x, y, label, ha='center', va='center', fontsize=11,
                bbox=dict(boxstyle='round,pad=0.3', facecolor='lightblue', edgecolor='navy'))

    for i in range(len(steps) - 1):
        ax.annotate('', xy=(5, steps[i+1][1] + 0.4), xytext=(5, steps[i][1] - 0.4),
                    arrowprops=dict(arrowstyle='->', color='navy', lw=1.5))

    plt.tight_layout()
    plt.savefig(PAPER / 'fig1_pipeline.pdf', bbox_inches='tight')
    plt.close()
    print(f"  Saved fig1_pipeline.pdf")


def figure2_communication_frontier():
    """Figure 2: B*(n,1) vs n with reference lines."""
    fig, ax = plt.subplots(figsize=(8, 5))

    ns = list(range(1, 9))
    bs = [b_star[n] for n in ns]

    # Exact points
    ax.plot(ns, bs, 'ko-', markersize=8, linewidth=2, label='$B^*(n,1)$ (exact)', zorder=5)

    # Reference: B = n (old conjecture)
    ax.plot(ns, ns, 'r--', linewidth=1.5, label='$B = n$ (old conjecture)', alpha=0.7)

    # Reference: B = n * log2(3/2) (asymptotic)
    ns_cont = np.linspace(1, 8, 100)
    ax.plot(ns_cont, ns_cont * log2_32, 'b--', linewidth=1.5,
            label=f'$B = n \\log_2(3/2) \\approx {log2_32:.3f}n$ (asymptotic)', alpha=0.7)

    ax.set_xlabel('$n$ (number of parallel copies)', fontsize=12)
    ax.set_ylabel('$B^*(n, 1)$ (communication bits)', fontsize=12)
    ax.set_title('Figure 2: Finite-Size Communication Frontier', fontsize=13, fontweight='bold')
    ax.set_xticks(ns)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    ax.set_ylim(0, 9)

    # Annotate compression
    ax.annotate('Compression:\n$B^*(4,1)=3 < 4$', xy=(4, 3), xytext=(4.5, 5.5),
                fontsize=9, arrowprops=dict(arrowstyle='->', color='green'),
                color='green', fontweight='bold')

    plt.tight_layout()
    plt.savefig(PAPER / 'fig2_frontier.pdf', bbox_inches='tight')
    plt.close()
    print(f"  Saved fig2_frontier.pdf")


def figure3_normalized_rate():
    """Figure 3: B*(n,1)/n with asymptotic limit."""
    fig, ax = plt.subplots(figsize=(8, 5))

    ns = list(range(1, 9))
    rates = [b_star[n] / n for n in ns]

    ax.plot(ns, rates, 'ko-', markersize=8, linewidth=2, label='$B^*(n,1)/n$', zorder=5)

    # Asymptotic limit
    ax.axhline(y=log2_32, color='blue', linestyle='--', linewidth=1.5,
               label=f'$\\log_2(3/2) \\approx {log2_32:.4f}$ (limit)')

    # Upper bound
    ax.axhline(y=1.0, color='red', linestyle=':', linewidth=1, label='$1.0$ (upper bound)')

    ax.set_xlabel('$n$', fontsize=12)
    ax.set_ylabel('$B^*(n, 1) / n$', fontsize=12)
    ax.set_title('Figure 3: Normalized Communication Rate', fontsize=13, fontweight='bold')
    ax.set_xticks(ns)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    ax.set_ylim(0.4, 1.1)

    plt.tight_layout()
    plt.savefig(PAPER / 'fig3_rate.pdf', bbox_inches='tight')
    plt.close()
    print(f"  Saved fig3_rate.pdf")


def table1_resource_comparison():
    """Table 1: Resource comparison (text output)."""
    print("\nTable 1: Resource Comparison")
    print("=" * 60)
    print(f"{'Resource':<25s} {'Classical':<20s} {'Quantum':<15s}")
    print("-" * 60)
    print(f"{'Communication':<25s} {'n·log₂(3/2)+O(1)':<20s} {'0':<15s}")
    print(f"{'Preshared entanglement':<25s} {'0':<20s} {'2n Bell pairs':<15s}")
    print(f"{'Success':<25s} {'1':<20s} {'1':<15s}")
    print(f"{'Model':<25s} {'Det. one-way':<20s} {'Zhao-Deng':<15s}")
    print("=" * 60)


def finite_size_table():
    """Print the finite-size table."""
    print("\nFinite-Size Communication Table")
    print("=" * 70)
    print(f"{'n':<5s} {'f(n,3)':<15s} {'B*(n,1)':<10s} {'Status':<20s} {'Source'}")
    print("-" * 70)

    for n in range(1, 9):
        if n in f_exact:
            f_str = str(f_exact[n])
            status = "Exact"
            source = "Adriaensen" if n >= 2 else "This work"
        else:
            lo, hi = f_bounds[n]
            f_str = f"[{lo}, {hi}]"
            status = "B* exact, f bounded"
            source = "Kuang-Wang" if n == 8 else "Adriaensen"

        print(f"{n:<5d} {f_str:<15s} {b_star[n]:<10d} {status:<20s} {source}")

    print("=" * 70)
    print("B* is exact for all n<=8 because covering bounds lie in single")
    print("power-of-2 intervals.")


if __name__ == "__main__":
    print("CQA07: Generating figures and tables")
    print("=" * 50)

    figure1_conceptual_pipeline()
    figure2_communication_frontier()
    figure3_normalized_rate()
    table1_resource_comparison()
    finite_size_table()

    print(f"\nAll figures saved to {PAPER}")
