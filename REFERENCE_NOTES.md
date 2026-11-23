# Source comparison for the DQS submission

Checked against primary texts on 23 November 2026.
This records the scope of the assisted checks, not an assertion of independent
human peer review or an exhaustive novelty search.

## Kuang–Wang, arXiv:2608.13252v1

Primary text: https://arxiv.org/html/2608.13252v1

Theorem 1.2 states, for every integer n>=0,
f(n)<=2(3/2)^n−1. It also states that f(n)/(3/2)^n is nondecreasing and
converges to C3 with 1.62227<C3<=2.

The proof uses even-degree induced vertex sets to construct binary-subcube
covers; their expected number in G(n,1/2) is 2(3/2)^n−1. The projection
inequality f(n)>=(3/2)^(n−k)f(k) supplies monotonicity. These arguments and
their use in the manuscript were checked.

The manuscript's weaker f(n)<=2(3/2)^n and hence
ceil(n log2(3/2))<=B*<=ceil(n log2(3/2))+1 are valid for each n, not just
asymptotically. This remains a clearly identified arXiv preprint.
The paper explicitly quotes 41<=f(8,3)<=50.

## Adriaensen et al., arXiv:2602.01080v1

Primary text: https://arxiv.org/html/2602.01080v1

The tabulated q=3 values include f(6,3)=18 and f(7,3) in [28,30].
These are cited values, not independently solved by our n=6 rerun.
Kuang–Wang gives the tighter quoted n=8 interval used in the manuscript.
Combining either interval with ceil(log2 f) uniquely determines B*.

## Zhao–Deng, npj Quantum Information 11, 127 (2025)

Primary text: https://www.nature.com/articles/s41534-025-01078-x
DOI: 10.1038/s41534-025-01078-x.

The published definition matches `code/task.py`:
- I(x)=2x1+x2; 00 is an automatically winning input for either party.
- Alice's virtual third output is y1 xor y2 xor 1; Bob's is y1 xor y2.
- Otherwise the compared outputs are Bob[I(xA)] and Alice[I(xB)].
- n copies are won only if every copy is won.
- The first and last 2n bits are the parties' respective inputs/outputs.

The paper explicitly uses two Bell pairs per copy and 2n Bell pairs in
Theorem 1. These are 4n physical qubits in total, not 2n qubits.
The supplied entanglement is independent of the input; the zero-communication
statement concerns input-dependent communication.

The manuscript studies the original noiseless conjunction task R, not the
different noise-tolerant translation rule Rp introduced later in Zhao–Deng.
It proves a one-way zero-error communication statement, not their full
learning-theoretic constant-parameter advantage.

## Other reference checks

Toner–Bacon (PRL 91, 187904; doi:10.1103/PhysRevLett.91.187904) concerns
projective measurements on a maximally entangled Bell pair. It is not a
theorem covering all two-qubit states.
Márton et al. (npj Quantum Information 10, 79, 2024;
doi:10.1038/s41534-024-00874-1) discusses the remaining general two-qubit
question and the bidirectional one-bit bound for parallel magic-square games.

Rall's categorical-product paper is doi:10.7151/dmgt.1257, pp.35–44 (2005).
Mekiš's direct-product lower-bound paper is doi:10.1016/j.disc.2010.07.015
(2010). The general nonlocality and magic-square references provide context;
the manuscript's parity and message-class arguments are written explicitly.

## Journal formatting

Discover Quantum Science's submission guidance was consulted:
https://link.springer.com/journal/44464/submission-guidelines

Research article; abstract below 250 words; 12-point body text; numeric
references; source ZIP with figures; cover letter; funding, contributions,
competing interests and data/code availability. The LaTeX/PDF is canonical.
Preprints are explicitly identified rather than presented as peer-reviewed papers.
