# CQA07 Claim Ledger (FROZEN — npj QI Submission Version)

No manuscript sentence may state a scientific result absent from this ledger.
This ledger is frozen for the npj Quantum Information submission.

---

## CLAIM A: B*(n,1) = ⌈log₂ f(n,3)⌉ = ⌈log₂ γ_t(K_3^×n)⌉

- **STATUS:** THEOREM (proof audited, PASS)
- **EVIDENCE:**
  - Lemma 1 (single-copy compatibility): proven with explicit strategies for all 3 subsets + ⊕1 contradiction
  - Lemma 2 (factorization, necessity + sufficiency): proven with explicit per-coordinate construction
  - Lemma 3 (binary subcubes): proven with enlargement argument
  - Lemma 4 (hard-input extension): proven with completion map ρ
  - Theorem 1 (main): proven (lower + upper bound)
  - Computational verification: n=1..4 exhaustive, n=5..7 ILP
- **AUDIT:** FINAL_PROOF_AUDIT.md — all items PASS
- **ALLOWED WORDING:** "B*(n,1) = ⌈log₂ f(n,3)⌉ = ⌈log₂ γ_t(K_3^×n)⌉, where f(n,3) is the ternary-cube covering number."
- **FORBIDDEN WORDING:** None (this is a theorem).

---

## CLAIM B: f(n,3) = γ_t(K_3^×n)

- **STATUS:** KNOWN GRAPH-THEORETIC EQUIVALENCE (not our novelty)
- **EVIDENCE:** Established in Adriaensen et al. [2026] and Kuang & Wang [2026].
- **ALLOWED WORDING:** "The covering number f(n,3) equals the total domination number γ_t(K_3^×n) [Adriaensen et al., 2026; Kuang & Wang, 2026]."
- **FORBIDDEN WORDING:** "We discovered that f(n,3) = γ_t(K_3^×n)."

---

## CLAIM C: B*(n,1) = n·log₂(3/2) + O(1)

- **STATUS:** COROLLARY of our Theorem 1 + Kuang & Wang [2026]
- **EVIDENCE:**
  - Theorem 1: B* = ⌈log₂ f(n,3)⌉
  - Kuang & Wang: f(n) = (C₃ + o(1))(3/2)^n, 1.62227 < C₃ ≤ 2
  - Therefore: B* = ⌈n·log₂(3/2) + log₂(C₃ + o(1))⌉ = n·log₂(3/2) + O(1)
- **ALLOWED WORDING:** "B*(n,1) = n·log₂(3/2) + O(1), so lim B*/n = log₂(3/2) ≈ 0.585. The covering asymptotic is due to Kuang & Wang [2026]; the communication corollary follows from our reduction."
- **FORBIDDEN WORDING:** "We proved the covering asymptotic."

---

## CLAIM D: B*(n,1) < n for all n ≥ 4

- **STATUS:** THEOREM (strengthened from finite-size-only)
- **EVIDENCE:**
  - n=4: B*(4,1) = 3 < 4 (exact)
  - n≥5: Kuang-Wang upper bound f(n) ≤ 2(3/2)^n - 1 < 2^(n-1), so B* ≤ n-1 < n
  - Asymptotically: B*/n → log₂(3/2) ≈ 0.585 < 1
- **ALLOWED WORDING:** "B*(n,1) < n for all n ≥ 4. Joint encoding of parallel subtasks produces nontrivial classical communication compression."
- **FORBIDDEN WORDING:** "Quantum compression." (This is a classical property.)

---

## CLAIM E: Shared randomness does not reduce perfect-success communication

- **STATUS:** THEOREM (quantifiers verified with full-support distribution)
- **EVIDENCE:** For S=1 with full-support input distribution, every seed with positive probability must induce a deterministic perfect protocol. Proof uses: E_R[Pr(W_n=0|R)] = 0 implies Pr(W_n=0|R=r) = 0 a.e.
- **AUDIT:** FINAL_PROOF_AUDIT.md — PASS
- **ALLOWED WORDING:** "B*_{shared-random}(n,1) = B*_{deterministic}(n,1)."
- **FORBIDDEN WORDING:** None (this is a theorem, with the worst-case/full-support assumption stated).

---

## CLAIM F: S_n(0) = (15/16)^n

- **STATUS:** AUDIT — multiplicativity NOT proven
- **EVIDENCE:**
  - S_1(0) = 15/16 (exhaustively verified)
  - S_n(0) ≥ (15/16)^n (product strategy lower bound)
  - Equality computationally verified for n ≤ 4
  - General multiplicativity is an OPEN QUESTION
- **ALLOWED WORDING:** "S_1(0) = 15/16. S_n(0) ≥ (15/16)^n, with equality computationally verified for n ≤ 4. General multiplicativity is open."
- **FORBIDDEN WORDING:** "S_n(0) = (15/16)^n" (as a theorem). "Multiplicativity is proven."

---

## CLAIM G: B*(n,1) = n (linear conjecture)

- **STATUS:** FALSIFIED
- **EVIDENCE:** B*(4,1) = 3 < 4. More generally B*(n,1) < n for all n ≥ 4.
- **ALLOWED WORDING:** "The conjecture B*(n,1) = n is falsified for n ≥ 4."
- **FORBIDDEN WORDING:** "B*(n,1) = n."

---

## CLAIM H: A000124 / quadratic formula

- **STATUS:** RETRACTED
- **EVIDENCE:** The sequence 2,3,5,8,12 is not OEIS A000124. The quadratic formula is contradicted by f(6,3)=18 > 17.
- **ALLOWED WORDING:** "The first five covering numbers are 2,3,5,8,12. No general formula is established."
- **FORBIDDEN WORDING:** "γ(n) is A000124." "γ(n) = n(n-1)/2+2." "Quadratic growth."

---

## CLAIM I: Quantum protocol (B=0, E=2n, S=1)

- **STATUS:** PROVEN (from Zhao-Deng [2025])
- **ALLOWED WORDING:** "The quantum protocol achieves perfect success with 2n preshared Bell pairs and zero input-dependent classical communication [Zhao & Deng, 2025]."
- **FORBIDDEN WORDING:** "One Bell pair replaces X bits." "Exponential computational advantage." "General quantum computational advantage." "Universal quantum speedup."

---

## CLAIM J: ⊕1 asymmetry mechanism

- **STATUS:** PROVEN
- **EVIDENCE:** The ⊕1 in Alice's third virtual component creates the incompatibility. Proven in Lemma 1.
- **ALLOWED WORDING:** "The ⊕1 asymmetry in Alice's virtual output is the mechanism preventing zero-communication perfect success."
- **FORBIDDEN WORDING:** None (this is proven).

---

## CLAIM K: Hard-input extension

- **STATUS:** THEOREM (Lemma 4)
- **EVIDENCE:** Completion map ρ replaces easy inputs with fixed hard inputs. Coordinate-wise verification: easy coordinates auto-win, hard coordinates use the hard-input protocol.
- **ALLOWED WORDING:** "Solving the all-hard restriction with B bits is equivalent to solving the full task with B bits."
- **FORBIDDEN WORDING:** None (this is a theorem).

---

## CLAIM L: Zhao-Deng positioning

- **STATUS:** CORRECTED
- **EVIDENCE:** Zhao-Deng establish a constant-vs-linear separation for communication-bounded classical models. Our work addresses the more specific zero-error one-way communication problem.
- **ALLOWED WORDING:** "Zhao and Deng establish a constant-versus-linear separation for communication-bounded classical models. Our result addresses the more specific zero-error one-way communication problem."
- **FORBIDDEN WORDING:** "Our result improves/sharpens Zhao-Deng's main ML theorem." (Unless specifying exactly which restricted quantity.)

---

## Finite-Size Table (FROZEN)

| n | f(n,3) | B*(n,1) | Status | Source |
|---|--------|---------|--------|--------|
| 1 | 2 | 1 | Exact | This work |
| 2 | 3 | 2 | Exact | Adriaensen |
| 3 | 5 | 3 | Exact | Adriaensen |
| 4 | 8 | 3 | Exact | Adriaensen |
| 5 | 12 | 4 | Exact | Adriaensen |
| 6 | 18 | 5 | Exact | Adriaensen |
| 7 | [28,30] | 5 | B* exact, f bounded | Adriaensen |
| 8 | [41,50] | 6 | B* exact, f bounded | Kuang-Wang |

B* is exact for all n ≤ 8 because covering bounds lie in single power-of-2 intervals.

---

## References (FROZEN — 13 entries)

| # | Reference | Role |
|---|-----------|------|
| 1 | Zhao & Deng, npj QI 11, 127 (2025) | PRIMARY: task, quantum protocol |
| 2 | Adriaensen et al., BICA (forthcoming) | PRIMARY: covering, finite-size |
| 3 | Kuang & Wang, arXiv:2608.13252 (2026) | PRIMARY: asymptotic |
| 4 | Rall, DMGT 25, 35-44 (2005) | CONTEXT: total domination |
| 5 | Mekiš, DM 310, 3310-3317 (2010) | CONTEXT: lower bounds |
| 6 | Márton et al., npj QI 10, 79 (2024) | CONTEXT: pseudo-telepathy comm |
| 7 | Buhrman et al., RMP 82, 665 (2010) | BACKGROUND: review |
| 8 | Toner & Bacon, PRL 91, 187904 (2003) | BACKGROUND: simulation |
| 9 | Bacon & Toner, PRL 90, 157904 (2003) | BACKGROUND: Bell+comm |
| 10 | Cleve et al., CCC 2004 | BACKGROUND: nonlocal strategies |
| 11 | Brassard et al., Found. Phys. 35, 1877 (2005) | BACKGROUND: pseudo-telepathy |
| 12 | Mermin, PRL 65, 3373 (1990) | HISTORICAL: magic square |
| 13 | Peres, PLA 151, 107 (1990) | HISTORICAL: magic square |

---

## Ledger Freeze Date

This ledger is frozen for npj Quantum Information submission. Any change requires re-auditing the affected claims.
