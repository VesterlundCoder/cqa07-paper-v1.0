"""Generate the manuscript figures from data/*.json (no hard-coded results)."""
import json, math, pathlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

root = pathlib.Path(__file__).resolve().parents[1]
cov = [r for r in json.loads((root / "data/covering.json").read_text())["results"] if r["proven_optimal"]]
lit = json.loads((root / "data/literature.json").read_text())
OWN, LIT, REF, INK = "#2a78d6", "#eb6834", "#8a8a85", "#2b2b29"
plt.rcParams.update({"font.size": 10, "axes.edgecolor": REF, "axes.labelcolor": INK,
                     "xtick.color": INK, "ytick.color": INK, "axes.spines.top": False, "axes.spines.right": False})
L = math.log2(1.5)
own = {r["n"]: (r["best_cover_size"], r["best_cover_size"]) for r in cov}
litv = {int(k): (v["lower"], v["upper"]) for k, v in lit["f_n3"].items() if int(k) not in own}
allv = {**own, **litv}
ns = sorted(allv)
bstar = {n: (math.ceil(math.log2(lo)), math.ceil(math.log2(hi))) for n, (lo, hi) in allv.items()}
for n, (a, b) in bstar.items():
    assert a == b, f"B*({n}) not determined"

# Figure 1: B*(n,1)
fig, ax = plt.subplots(figsize=(6.2, 3.8))
lo_b = [math.ceil(n * L - 1e-12) for n in ns]
ax.vlines(ns, lo_b, [b + 1 for b in lo_b], color=OWN, alpha=0.25, lw=10,
          label=r"$\lceil n\log_2(3/2)\rceil \leq B^* \leq \lceil n\log_2(3/2)\rceil+1$")
ax.plot(ns, ns, ls="--", color=REF, lw=1.5, label=r"trivial bound $B=n$")
o = [n for n in ns if n in own]; l = [n for n in ns if n in litv]
ax.plot(o, [bstar[n][0] for n in o], "o", color=OWN, ms=8, label="from $f(n,3)$ computed here")
ax.plot(l, [bstar[n][0] for n in l], "s", color=LIT, ms=8, label="from $f(n,3)$ in the literature")
ax.set_xlabel("$n$ (parallel copies)"); ax.set_ylabel(r"$B^*(n,1)$ (bits)")
ax.set_xticks(ns); ax.set_yticks(range(0, 9)); ax.grid(alpha=0.25, lw=0.5)
ax.legend(frameon=False, fontsize=8.5, loc="upper left")
fig.tight_layout(); fig.savefig(root / "manuscript/figures/fig1_frontier.pdf"); fig.savefig(root / "manuscript/figures/fig1_frontier.png", dpi=200)

# Figure 2: f(n,3)/(3/2)^n
fig, ax = plt.subplots(figsize=(6.2, 4.4))
c = lit["C3"]
ax.axhspan(c["lower_exclusive"], c["upper"], color=LIT, alpha=0.10, lw=0, label=r"$C_3\in(1.62227,\,2]$ (Kuang–Wang)")
ax.axhline(1, color=REF, ls="--", lw=1.2, label=r"counting bound $f\geq(3/2)^n$")
ax.plot(o, [own[n][0] / 1.5 ** n for n in o], "o", color=OWN, ms=8, label="proven optimal, computed here")
for n in l:
    lo, hi = litv[n]
    if lo == hi:
        ax.plot([n], [lo / 1.5 ** n], "s", color=LIT, ms=8, label="literature: exact value" if n == l[0] else None)
    else:
        ax.vlines(n, lo / 1.5 ** n, hi / 1.5 ** n, color=LIT, lw=2.5, label="literature: bounds" if lo != hi and n == min(m for m in l if litv[m][0] != litv[m][1]) else None)
        ax.plot([n, n], [lo / 1.5 ** n, hi / 1.5 ** n], "_", color=LIT, ms=12, mew=2.5)
ax.set_xlabel("$n$"); ax.set_ylabel(r"$f(n,3)\,/\,(3/2)^n$"); ax.set_xticks(ns); ax.set_ylim(0.9, 2.1)
ax.grid(alpha=0.25, lw=0.5); ax.legend(frameon=False, fontsize=8.5, loc="upper center", bbox_to_anchor=(0.5, -0.17), ncol=2)
fig.tight_layout(); fig.savefig(root / "manuscript/figures/fig2_covering.pdf"); fig.savefig(root / "manuscript/figures/fig2_covering.png", dpi=200)
print("B*:", {n: bstar[n][0] for n in ns})
