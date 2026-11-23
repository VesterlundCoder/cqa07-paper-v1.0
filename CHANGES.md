# Changes from v1 (npj Quantum Information submission) to v2

## Corrected errors
1. **Table 2 (single-copy strategies).** Rows {01,11} and {10,11} were wrong: they lose on index pairs (1,1),(3,2),(3,3) and (2,2),(3,1),(3,3). They are replaced by verified constant strategies (Alice always (1,1); Bob (1,0) and (0,1)). Lemma 1 itself was correct.
2. **No-communication baseline.** v1 claimed S_n(0) = (15/16)^n "computationally verified for n ≤ 4". This is false: an explicit deterministic strategy pair gives S₂(0) ≥ 227/256 > 225/256. The claim and Figure 3 are removed; the appendix now states the correct lower bound.
3. **"Quadratic upper bound n(n−1)/2+2."** False (f(6,3)=18 > 17) and removed, together with the A000124 curve.
4. **Figure 4 / resource section.** "Sublinear" and "B*/E decreases" were wrong (the cost is linear and B*/E → log₂(3/2)/2). Figure 4 is removed.
5. **Methods.** "16^{2n} input pairs" corrected to 4ⁿ·4ⁿ = 16ⁿ. "Two independent ILP formulations" corrected (they are the same formulation). The claim that f(6,3)=18 was independently confirmed is withdrawn: our solver does not prove optimality for n = 6. All solver statuses are now recorded verbatim.
6. **Toner & Bacon.** One bit is proven sufficient for the maximally entangled two-qubit state, not for every two-qubit state.
7. **Figures 1–2** contradicted Table 4 (n = 6 shown as bounds). They are regenerated from data files; no results are hard-coded.

## Improvements
* Rate now explicit for every n: ⌈n log₂(3/2)⌉ ≤ B* ≤ ⌈n log₂(3/2)⌉+1, via monotonicity in Kuang–Wang (the "−1" bound is no longer needed).
* Parity (Mermin–Peres) proof of Lemma 1; necessity in Lemma 2 rewritten with explicit representative inputs.
* Hard-input restriction removed as a separate lemma: compatibility is defined against all Bob inputs, and Alice's completion appears in the upper-bound proof.
* Structural remark: the optimal protocol has constant Alice output, and Bob's output depends only on the message.
* Notation: protocol maps renamed (e, α, β) to avoid clashing with f(n,3); bijection φ: {01,10,11} → Z₃ made explicit.

## Removed from the submission package
`CLAIM_LEDGER.md`, `FINAL_PROOF_AUDIT.md`, `RIGOROUS_PROOFS.md`, `REFERENCE_LEDGER.md` (internal working notes, including draft text), the stale v1 PDF, unused figures, and macOS metadata files.

## Discover Quantum Science preparation (23 November 2026)

* Set the journal and Research article type. Omitted the optional earlier-review
  paragraph rather than asserting a particular journal-transfer history.
* Verified Kuang–Wang v1, Theorem 1.2: finite-n upper bound 2(3/2)^n−1,
  monotonicity and limiting-constant statement. The one-bit window is valid.
* Checked the task, parity conventions, parallel conjunction and 2n Bell pairs
  directly against Zhao–Deng's published text.
* Clarified that the output structure describes the constructed optimal
  protocol, not every optimal protocol.
* Pinned SciPy 1.18.0 and retained full solver logs, primal/dual bounds, gaps,
  node counts, code hashes and independently re-scored incumbents.
* Removed silent failure masking in run_all.sh. Protocol failures now fail
  the command. Solver time limits remain distinguishable from optimal status.
* Numerical manuscript macros are generated from the rerun, rather than
  silently retaining a stronger bound from an earlier environment.
* Used 12-point A4 text, keywords and an ethics applicability statement.
* AI disclosure describes actual AI-assisted execution/checks and does not
  assert that the author personally performed the agent's actions.
* Regenerated the current PDF/Word copy and figures. Added the version DOI.

The completed rerun recovered n=1–5 optima and all 1,118,480 protocol checks.
At n=6 it returned a cover of size 25 and lower bound 15 at the 120-second
limit; the manuscript now reflects this run rather than the supplied size 27.
The two-copy run recovered incumbent 227 and upper bound 238 at 1200 seconds.
Its status remains time-limited, not optimal. These changes do not alter the
analytic main theorem or the cited exact communication costs through n=8.
