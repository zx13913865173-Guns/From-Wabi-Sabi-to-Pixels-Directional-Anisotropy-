#!/usr/bin/env bash
# Reproduce all analyses and figures for the linen-texture study.

set -euo pipefail

echo "[1/4] Generating simulated data..."
Rscript data/generate_simulated_data.R

echo "[2/4] Generating textures (optional)..."
python src/texture_processing.py || echo "  (skipped: no source texture)"

echo "[3/4] Running statistical analyses..."
Rscript src/statistical_analysis.R

echo "[4/4] Generating figures..."
python src/figures.py

echo "Done. See results/ and figures/."
