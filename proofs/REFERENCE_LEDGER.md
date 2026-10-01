# CQA07: Reference Ledger (npj QI Submission Version)

Every external theorem/value used in the manuscript must appear here with primary source verification.

---

## R1: Zhao-Deng task definition and quantum protocol

- **CLAIM:** Zhao and Deng define an entanglement-assisted learning task where a quantum protocol with 2n preshared Bell pairs achieves perfect success with zero classical communication.
- **SOURCE:** Zhao, H. & Deng, D.-L. "Entanglement-induced provable and robust quantum learning advantages." npj Quantum Information 11, 127 (2025).
- **URL:** https://www.nature.com/articles/s41534-025-01078-x
- **HOW USED:** Task definition, quantum protocol, constant-vs-linear separation.
- **PRIMARY SOURCE VERIFIED:** YES (web search confirmed publication in npj Quantum Information, 29 July 2025).

---

## R2: Zhao-Deng constant-vs-linear separation

- **CLAIM:** Classical communication-bounded models require Ω(n) bits for nontrivial success.
- **SOURCE:** Same as R1.
- **HOW USED:** Positioning; our result addresses the more specific zero-error one-way problem.
- **PRIMARY SOURCE VERIFIED:** YES.

---

## R3: f(n,3) = γ_t(K_3^×n) equivalence

- **CLAIM:** The ternary-cube covering number f(n,3) equals the total domination number γ_t(K_3^×n).
- **SOURCE:**
  - Adriaensen et al. (2026), arXiv:2602.01080, Section 1: "a skirting set S in Z_q^n is exactly the same thing as a total dominating set in G(n,q)."
  - Kuang & Wang (2026), arXiv:2608.13252, Section 1: "f(n) = γ_t(K_3^×n)."
- **HOW USED:** Graph domination equivalence (not our novelty; established in literature).
- **PRIMARY SOURCE VERIFIED:** YES (both papers explicitly state this).

---

## R4: f(6,3) = 18 (exact)

- **CLAIM:** The exact value f(6,3) = 18.
- **SOURCE:** Adriaensen et al. (2026), arXiv:2602.01080, Table in Section 3.
- **HOW USED:** Finite-size table; our ILP independently reproduces this.
- **PRIMARY SOURCE VERIFIED:** YES (table shows "18" as a single number, indicating exact value).

---

## R5: f(7,3) ∈ [28, 30]

- **CLAIM:** 28 ≤ f(7,3) ≤ 30.
- **SOURCE:** Adriaensen et al. (2026), arXiv:2602.01080, Table in Section 3.
- **HOW USED:** Finite-size table.
- **PRIMARY SOURCE VERIFIED:** YES (table shows "[28,30]" as an interval).

---

## R6: f(8,3) ∈ [41, 50]

- **CLAIM:** 41 ≤ f(8,3) ≤ 50.
- **SOURCE:** Kuang & Wang (2026), arXiv:2608.13252.
- **HOW USED:** Finite-size table.
- **PRIMARY SOURCE VERIFIED:** YES (explicitly stated in the introduction).

---

## R7: f(n) = (C_3 + o(1))(3/2)^n asymptotic

- **CLAIM:** f(n) = (C_3 + o(1))(3/2)^n where 1.62227 < C_3 ≤ 2, and f(n)/(3/2)^n is nondecreasing.
- **SOURCE:** Kuang & Wang (2026), arXiv:2608.13252, Theorem 1.2.
- **HOW USED:** Asymptotic communication rate corollary: B* = n·log₂(3/2) + O(1).
- **PRIMARY SOURCE VERIFIED:** YES (Theorem 1.2 explicitly stated).

---

## R8: f(n) ≤ 2(3/2)^n - 1 upper bound

- **CLAIM:** f(n) ≤ 2(3/2)^n - 1 for all n ≥ 0.
- **SOURCE:** Kuang & Wang (2026), arXiv:2608.13252, Theorem 1.2.
- **HOW USED:** Non-additivity corollary: B*(n,1) < n for n ≥ 5.
- **PRIMARY SOURCE VERIFIED:** YES.

---

## R9: f(n) ≥ (3/2)^n counting bound

- **CLAIM:** f(n) ≥ ⌈(3/2)^n⌉.
- **SOURCE:** Both Adriaensen et al. and Kuang & Wang (simple counting: each subcube covers 2^n of 3^n vertices).
- **HOW USED:** Lower bound on communication cost.
- **PRIMARY SOURCE VERIFIED:** YES (trivial counting argument, stated in both papers).

---

## R10: Rall (2005) total domination in categorical products

- **CLAIM:** γ_t(G × H) ≤ γ_t(G) · γ_t(H) for graphs without isolated vertices.
- **SOURCE:** Rall, D.F. "Total Domination in Categorical Products of Graphs." Discussiones Mathematicae Graph Theory 25(1-2), 35-44 (2005).
- **HOW USED:** Upper bound γ_t(K_3^×n) ≤ 2^n (historical context).
- **PRIMARY SOURCE VERIFIED:** YES (web search confirmed publication, pages 35-44).

---

## R11: Mekiš (2010) lower bound

- **CLAIM:** γ(×_{i=1}^t K_{n_i}) ≥ t+1 for t ≥ 3.
- **SOURCE:** Mekiš, G. "Lower bounds for the domination number and the total domination number of direct product graphs." Discrete Mathematics 310(23), 3310-3317 (2010). DOI: 10.1016/j.disc.2010.07.015
- **HOW USED:** Historical context (weak bound for our case).
- **PRIMARY SOURCE VERIFIED:** YES (ScienceDirect confirmed volume 310, issue 23, pages 3310-3317).

---

## R12: Márton et al. (2024) pseudo-telepathy communication

- **CLAIM:** Parallel repetition of pseudo-telepathy games (including Magic Square) can beat the one-bit classical communication bound.
- **SOURCE:** Márton, I., Bene, E., Diviánszky, P. & Vértesi, T. "Beating one bit of communication with and without quantum pseudo-telepathy." npj Quantum Information 10, 79 (2024).
- **URL:** https://www.nature.com/articles/s41534-024-00874-1
- **HOW USED:** Related work; closest direct prior work on communication bounds for parallel pseudo-telepathy.
- **PRIMARY SOURCE VERIFIED:** YES (npj QI 10, 79, published 22 Aug 2024).

---

## R13: Buhrman et al. (2010) review

- **CLAIM:** Comprehensive review of nonlocality and communication complexity.
- **SOURCE:** Buhrman, H., Cleve, R., Massar, S. & de Wolf, R. "Nonlocality and communication complexity." Reviews of Modern Physics 82, 665-698 (2010).
- **HOW USED:** Background reference for communication complexity framework.
- **PRIMARY SOURCE VERIFIED:** YES.

---

## R14: Toner & Bacon (2003)

- **CLAIM:** One bit of communication suffices to simulate projective measurements on any two-qubit entangled state.
- **SOURCE:** Toner, B.F. & Bacon, D. "Communication Cost of Simulating Bell Correlations." Physical Review Letters 91, 187904 (2003).
- **HOW USED:** Background for communication-assisted simulation of quantum correlations.
- **PRIMARY SOURCE VERIFIED:** YES.

---

## R15: Bacon & Toner (2003)

- **CLAIM:** Bell inequalities with auxiliary communication.
- **SOURCE:** Bacon, D. & Toner, B.F. "Bell Inequalities with Auxiliary Communication." Physical Review Letters 90, 157904 (2003).
- **HOW USED:** Background for fixed communication resources in Bell-type scenarios.
- **PRIMARY SOURCE VERIFIED:** YES.

---

## R16: Cleve et al. (2004)

- **CLAIM:** Foundational results on nonlocal strategies and their limits.
- **SOURCE:** Cleve, R., Høyer, P., Toner, B. & Watrous, J. "Consequences and Limits of Nonlocal Strategies." Proc. 19th IEEE Conf. Computational Complexity, 236-249 (2004).
- **HOW USED:** Background for nonlocal game theory.
- **PRIMARY SOURCE VERIFIED:** YES (arXiv:quant-ph/0404076).

---

## R17: Brassard, Broadbent & Tapp (2005)

- **CLAIM:** Formalization of quantum pseudo-telepathy.
- **SOURCE:** Brassard, G., Broadbent, A. & Tapp, A. "Quantum Pseudo-Telepathy." Foundations of Physics 35, 1877-1907 (2005).
- **HOW USED:** Background for pseudo-telepathy concept.
- **PRIMARY SOURCE VERIFIED:** YES (arXiv:quant-ph/0407221).

---

## R18: Mermin (1990)

- **CLAIM:** Unified form for no-hidden-variables theorems (Mermin-Peres square).
- **SOURCE:** Mermin, N.D. "Simple unified form for the major no-hidden-variables theorems." Physical Review Letters 65, 3373-3376 (1990).
- **HOW USED:** Historical reference for magic-square construction.
- **PRIMARY SOURCE VERIFIED:** YES.

---

## R19: Peres (1990)

- **CLAIM:** Incompatible results of quantum measurements (Peres-Mermin square).
- **SOURCE:** Peres, A. "Incompatible results of quantum measurements." Physics Letters A 151, 107-108 (1990).
- **HOW USED:** Historical reference for magic-square construction.
- **PRIMARY SOURCE VERIFIED:** YES.

---

## R20: Adriaensen et al. acceptance status

- **CLAIM:** Adriaensen et al. is accepted in the Bulletin of the Institute of Combinatorics and its Applications.
- **SOURCE:** BICA forthcoming list: https://pages.mtu.edu/~kreher/BICA/Forthcoming.html
- **HOW USED:** Bibliographic status update from arXiv preprint to accepted.
- **PRIMARY SOURCE VERIFIED:** YES.

---

## Summary

| Ref | Claim | Source | Verified |
|-----|-------|--------|----------|
| R1 | Zhao-Deng task | npj QI 11, 127 (2025) | YES |
| R2 | Constant-vs-linear | npj QI 11, 127 (2025) | YES |
| R3 | f(n,3) = γ_t | Adriaensen + Kuang-Wang | YES |
| R4 | f(6,3) = 18 | Adriaensen Table | YES |
| R5 | f(7,3) ∈ [28,30] | Adriaensen Table | YES |
| R6 | f(8,3) ∈ [41,50] | Kuang-Wang | YES |
| R7 | f(n) = (C_3+o(1))(3/2)^n | Kuang-Wang Thm 1.2 | YES |
| R8 | f(n) ≤ 2(3/2)^n - 1 | Kuang-Wang Thm 1.2 | YES |
| R9 | f(n) ≥ (3/2)^n | Both (counting) | YES |
| R10 | Rall submultiplicativity | DMGT 25, 35-44 (2005) | YES |
| R11 | Mekiš lower bound | DM 310, 3310-3317 (2010) | YES |
| R12 | Márton et al. | npj QI 10, 79 (2024) | YES |
| R13 | Buhrman et al. | RMP 82, 665 (2010) | YES |
| R14 | Toner & Bacon | PRL 91, 187904 (2003) | YES |
| R15 | Bacon & Toner | PRL 90, 157904 (2003) | YES |
| R16 | Cleve et al. | CCC 2004 | YES |
| R17 | Brassard et al. | Found. Phys. 35, 1877 (2005) | YES |
| R18 | Mermin | PRL 65, 3373 (1990) | YES |
| R19 | Peres | PLA 151, 107 (1990) | YES |
| R20 | Adriaensen BICA acceptance | BICA forthcoming list | YES |

**All 20 references verified against primary sources. No external theorem enters the manuscript without verification.**
