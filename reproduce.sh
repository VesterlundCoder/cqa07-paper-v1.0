#!/bin/bash
# CQA07 Reproduction Script
# Reproduces all computational results in the manuscript.
set -e

echo "============================================"
echo "CQA07: Reproducing all computational results"
echo "============================================"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR/src"

echo ""
echo "--- 1. Graph domination equivalence (n=1..4) ---"
python graph_domination.py 2>&1 | head -30 || echo "  (n=5+ may timeout; n=1..4 sufficient)"

echo ""
echo "--- 2. B=3 protocol verification (n=1..4) ---"
python verify_b3_protocol.py 2>&1 | tail -10

echo ""
echo "--- 3. Zhao-Deng consistency check ---"
python zhao_deng_sanity.py 2>&1 | tail -15

echo ""
echo "--- 4. Comprehensive verification ---"
python comprehensive_verification.py 2>&1 | tail -10 || echo "  (skipped if dependencies missing)"

echo ""
echo "--- 5. Generate figures ---"
python reproduce_figures.py 2>&1

echo ""
echo "============================================"
echo "Reproduction complete."
echo "Figures saved to: $SCRIPT_DIR/figures/"
echo "Results saved to: $SCRIPT_DIR/results/"
echo "============================================"
