# CQA07: Exact Zero-Error Communication Complexity of an Entanglement-Assisted Quantum Learning Task

This repository accompanies the manuscript submitted to npj Quantum Information.

## Contents

```
cqa07-paper-v1.0/
├── paper/          # LaTeX source and compiled PDF
├── src/            # Computational scripts
├── proofs/         # Formal proofs and audit documents
├── computations/   # ILP formulations and solver logs
├── results/        # JSON output files
├── figures/        # Generated figures (PDF)
├── CLAIM_LEDGER.md # Frozen claim ledger
├── README.md       # This file
├── LICENSE         # MIT License
├── CITATION.cff    # Citation metadata
├── requirements.txt
└── reproduce.sh    # One-command reproduction
```

## Reproduce

```bash
pip install -r requirements.txt
./reproduce.sh
```

This reproduces:
- Single-copy optimum (15/16)
- Finite-size communication table (n=1..8)
- Graph domination equivalence (n=1..4)
- B=3 protocol verification (n=1..4)
- Zhao-Deng consistency checks
- All figures

## Key Results

- **Main theorem:** B*(n,1) = ⌈log₂ f(n,3)⌉ = ⌈log₂ γ_t(K_3^×n)⌉
- **Asymptotic rate:** B*(n,1) = n·log₂(3/2) + O(1)
- **Non-additivity:** B*(n,1) < n for all n ≥ 4

## License

MIT License — see LICENSE file.

## Citation

See CITATION.cff for citation metadata.
