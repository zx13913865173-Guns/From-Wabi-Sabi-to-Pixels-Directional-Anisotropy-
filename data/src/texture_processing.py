# -*- coding: utf-8 -*-
"""
Texture processing for the linen-texture study.

Key correction:
    The original implementation divided the Fourier amplitude by f,
    producing power ∝ 1/f², i.e., red/Brownian noise (β ≈ 2.0).
    The corrected version uses:
        P(f) ∝ f^(-β)
        A(f) ∝ f^(-β/2)
    For Condition E, β is matched to the linen texture (β = 1.24).
"""

import numpy as np
from numpy.fft import fft2, ifft2, fftshift, ifftshift
from skimage import io
from skimage.feature import graycomatrix, graycoprops


# ------------------------------------------------------------------
# GLCM features
# ------------------------------------------------------------------
def compute_glcm(image_path, distance=1, angle=0, levels=256):
    """Compute GLCM energy and contrast for a grayscale image."""
    img = io.imread(image_path, as_gray=True)
    img = (img * 255).astype(np.uint8)
    glcm = graycomatrix(
        img,
        distances=[distance],
        angles=[angle],
        levels=levels,
        symmetric=True,
        normed=True,
    )
    energy   = float(np.mean(graycoprops(glcm, "energy")))
    contrast = float(np.mean(graycoprops(glcm, "contrast")))
    return energy, contrast


# ------------------------------------------------------------------
# Fourier slope β
# ------------------------------------------------------------------
def compute_fourier_slope(img, f_min=4, f_max=None):
    """
    Estimate the Fourier power spectrum slope β via log-log regression
    on the radially averaged power spectrum.
    """
    if img.dtype != np.float64:
        img = img.astype(np.float64)
    img = img - img.mean()

    F = fftshift(fft2(img))
    P = np.abs(F) ** 2

    h, w = img.shape
    cy, cx = h // 2, w // 2
    yy, xx = np.mgrid[0:h, 0:w]
    r = np.sqrt((yy - cy) ** 2 + (xx - cx) ** 2).astype(int)

    if f_max is None:
        f_max = min(cy, cx) - 1

    r_flat = r.ravel()
    P_flat = P.ravel()
    nbins = f_max + 1

    sum_P = np.bincount(r_flat, weights=P_flat, minlength=nbins)
    cnt   = np.bincount(r_flat, minlength=nbins)
    radial = sum_P / np.maximum(cnt, 1)

    f = np.arange(nbins)
    mask = (f >= f_min) & (f <= f_max) & (radial > 0)
    if mask.sum() < 5:
        return np.nan

    log_f = np.log10(f[mask])
    log_P = np.log10(radial[mask])
    slope, _ = np.polyfit(log_f, log_P, 1)
    beta = -slope
    return float(beta)


# ------------------------------------------------------------------
# Directional index DI
# ------------------------------------------------------------------
def compute_di(img):
    """
    Compute the directional index (DI) from the Fourier power spectrum
    as the normalized difference of the second-moment eigenvalues of
    the angular energy distribution.
    """
    if img.dtype != np.float64:
        img = img.astype(np.float64)
    img = img - img.mean()

    F = fftshift(fft2(img))
    P = np.abs(F) ** 2

    h, w = img.shape
    cy, cx = h // 2, w // 2
    yy, xx = np.mgrid[0:h, 0:w]
    dy = yy - cy
    dx = xx - cx
    r = np.sqrt(dx ** 2 + dy ** 2)
    r_max = min(cy, cx) - 1
    mask = (r > 2) & (r < r_max)

    theta = np.arctan2(dy, dx)
    weights = P[mask]
    thetas = theta[mask]

    c = np.cos(2 * thetas)
    s = np.sin(2 * thetas)
    C = np.sum(weights * c) / np.sum(weights)
    S = np.sum(weights * s) / np.sum(weights)

    DI = np.sqrt(C ** 2 + S ** 2)
    return float(DI)


# ------------------------------------------------------------------
# Fractal dimension (box counting)
# ------------------------------------------------------------------
def compute_fd(img, n_sizes=10):
    """Box-counting fractal dimension."""
    img = img.astype(np.float64)
    img = (img - img.min()) / (img.max() - img.min() + 1e-12)
    binary = img > 0.5

    h, w = binary.shape
    min_side = min(h, w)
    sizes = np.unique(
        np.floor(np.logspace(np.log10(2), np.log10(min_side // 2), n_sizes))
    ).astype(int)

    counts = []
    for s in sizes:
        if s < 2:
            continue
        n_h = h // s
        n_w = w // s
        count = 0
        for i in range(n_h):
            for j in range(n_w):
                block = binary[i * s:(i + 1) * s, j * s:(j + 1) * s]
                if block.any():
                    count += 1
        counts.append(count)

    sizes = sizes[: len(counts)]
    log_s = np.log(1.0 / sizes)
    log_c = np.log(np.array(counts, dtype=float) + 1e-12)
    slope, _ = np.polyfit(log_s, log_c, 1)
    return float(slope)


# ------------------------------------------------------------------
# Matched-β isotropic noise (Condition E)
# ------------------------------------------------------------------
def generate_matched_beta_noise(size=1024, beta=1.24, seed=42):
    """
    Generate isotropic noise with a prescribed Fourier power slope β.

    Correct formula:
        P(f) ∝ f^(-β)
        A(f) ∝ f^(-β/2)

    Note: the previous implementation used A(f) ∝ 1/f, which gives
    P(f) ∝ 1/f², i.e., red/Brownian noise (β ≈ 2), not pink noise.
    """
    rng = np.random.default_rng(seed)

    # Step 1: complex Gaussian random field
    noise = rng.normal(0, 1, (size, size)) + 1j * rng.normal(0, 1, (size, size))

    # Step 2: radial frequency grid
    freq = np.fft.fftfreq(size)
    fx, fy = np.meshgrid(freq, freq)
    f = np.sqrt(fx ** 2 + fy ** 2)
    f[0, 0] = 1e-10

    # Step 3: apply amplitude scaling A(f) ∝ f^(-β/2)
    F = fft2(noise)
    F = fftshift(F)
    f_shift = fftshift(f)
    F = F * (f_shift ** (-beta / 2.0))

    # Step 4: inverse transform
    pink = np.real(ifft2(ifftshift(F)))

    # Step 5: normalize to [0, 255]
    pink = pink - pink.min()
    if pink.max() > 0:
        pink = pink / pink.max()
    pink = (pink * 255).astype(np.uint8)

    return pink


# ------------------------------------------------------------------
# Main
# ------------------------------------------------------------------
if __name__ == "__main__":
    import os

    os.makedirs("figures", exist_ok=True)

    # --- Condition E: matched-β isotropic noise ---
    beta_target = 1.24
    pink = generate_matched_beta_noise(size=1024, beta=beta_target, seed=42)
    io.imsave("figures/pink_noise_condition_E.png", pink)

    beta_est = compute_fourier_slope(pink.astype(np.float64))
    di_est   = compute_di(pink.astype(np.float64))
    print(f"Condition E — target β = {beta_target:.2f}")
    print(f"  estimated β  = {beta_est:.3f}")
    print(f"  estimated DI = {di_est:.3f}")

    # --- Linen texture (if available) ---
    linen_path = "data/linen_texture.png"
    if os.path.exists(linen_path):
        energy, contrast = compute_glcm(linen_path)
        print(f"Linen GLCM: energy = {energy:.3f}, contrast = {contrast:.3f}")

        img = io.imread(linen_path, as_gray=True).astype(np.float64)
        img = (img * 255).astype(np.uint8).astype(np.float64)
        print(f"Linen β  = {compute_fourier_slope(img):.3f}")
        print(f"Linen DI = {compute_di(img):.3f}")
    else:
        print(f"Linen texture not found at {linen_path}. Skipping.")
