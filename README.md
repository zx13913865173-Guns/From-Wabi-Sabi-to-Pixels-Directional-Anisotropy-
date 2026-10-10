# Reproducibility Package for "From Wabi-Sabi to Pixels"

This package reproduces all analyses and figures for:

> **From Wabi-Sabi to Pixels: Directional Anisotropy as a Candidate
> Ergonomic Constraint for Mitigating Visual Discomfort in
> Dark-Environment Smartphone Reading—An Aesthetic-Ergonomic Ablation Study**

## Key corrections in this version

1. **Condition E is now matched-β isotropic noise**, not pink noise.
   The previous implementation divided the Fourier amplitude by `f`,
   producing power ∝ 1/f², i.e., **red/Brownian noise (β ≈ 2.0)**.
   The corrected version uses:
   - Power spectrum: `P(f) ∝ f^(-β)`
   - Amplitude spectrum: `A(f) ∝ f^(-β/2)`
   - Target: `β = 1.24` (matched to the linen texture)

2. **Histogram operations are constrained** for Conditions C and D,
   holding mean luminance, RMS luminance, β, and DI within tolerance.

3. **Code fixes**:
   - `sqtr` → `sqrt`
   - `graycrops` → `graycoprops`
   - `if name == "main"` → `if __name__ == "__main__":`

## Requirements

- Conda (recommended) OR Python 3.11 + R 4.3.2
- See `environment.yml` (Conda) or `requirements.txt` (pip + R)

## Setup

### With Conda (recommended)

```bash
conda env create -f environment.yml
conda activate linen_study
