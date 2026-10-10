# -*- coding: utf-8 -*-
"""
Generate FIG. 1 – FIG. 5 for the linen-texture study.

All figures: 16:9, 600 DPI, blue scientific palette, no overlap.
All numeric values are taken strictly from the paper tables.

Output (per figure):
    figures/FIGn_*.png
    figures/FIGn_*.tiff
    figures/FIGn_*.pdf
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle

# ------------------------------------------------------------------
# Global style
# ------------------------------------------------------------------
plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 9,
    "axes.linewidth": 0.9,
    "axes.labelsize": 10,
    "axes.titlesize": 11,
    "xtick.labelsize": 8.5,
    "ytick.labelsize": 8.5,
    "legend.fontsize": 8,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "xtick.direction": "out",
    "ytick.direction": "out",
    "figure.facecolor": "white",
    "savefig.facecolor": "white",
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
})

# Blue scientific palette
C_DARK  = "#0d2b45"
C_NAVY  = "#1f4e79"
C_BLUE  = "#2e75b6"
C_LBLUE = "#9dc3e6"
C_SKY   = "#deebf7"
C_GRAY  = "#7f7f7f"
C_BLACK = "#1a1a1a"

os.makedirs("figures", exist_ok=True)


def panel_label(ax, letter, x=-0.14, y=1.05):
    ax.text(x, y, letter, transform=ax.transAxes,
            fontsize=13, fontweight="bold", va="bottom", ha="left")


def save_all(fig, name):
    fig.savefig(f"figures/{name}.png",  dpi=600, facecolor="white")
    fig.savefig(f"figures/{name}.tiff", dpi=600, facecolor="white")
    fig.savefig(f"figures/{name}.pdf",           facecolor="white")
    plt.close(fig)
    print(f"  saved figures/{name}.png / .tiff / .pdf")


# ==================================================================
# FIG. 1 — Experimental workflow and stimulus materials
# ==================================================================
fig1 = plt.figure(figsize=(16, 9), facecolor="white")
gs1 = GridSpec(1, 2, figure=fig1, left=0.030, right=0.985,
               top=0.90, bottom=0.05, wspace=0.06)

axA = fig1.add_subplot(gs1[0, 0])
axA.set_xlim(0, 10); axA.set_ylim(0, 10); axA.axis("off")


def box(ax, x, y, w, h, text, fc, ec, fs=9, lw=1.2):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                 boxstyle="round,pad=0.05,rounding_size=0.14",
                 fc=fc, ec=ec, lw=lw, zorder=2))
    ax.text(x + w/2, y + h/2, text, ha="center", va="center",
            fontsize=fs, color="black", zorder=3, linespacing=1.4)


def arrow(ax, x1, y1, x2, y2):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2),
                 arrowstyle="-|>", mutation_scale=12,
                 color=C_NAVY, lw=1.2, zorder=1))


box(axA, 0.25, 8.40, 9.50, 1.00,
    "Participants  ·  Exp1 N=60  ·  Exp2 N=125  ·  Exp3 N=40  ·  "
    "Exp4 N=80  ·  Exp5 N=210",
    C_SKY, C_NAVY, fs=8.8)
arrow(axA, 5.0, 8.40, 5.0, 7.85)

box(axA, 1.00, 6.80, 8.00, 1.00,
    "2-min dark adaptation  →  screen instructions  →  reading task (≤ 20 min)",
    C_LBLUE, C_NAVY, fs=9)

exp_texts = [
    "Exp 1\n2×2 mixed\nBackground × Illuminance",
    "Exp 2\n5-level ablation\nA / B / C / D / E",
    "Exp 3\nRobustness\nDevice·Brightness·Text·Age",
    "Exp 4\n4-level validation\nF / G / H / I",
    "Exp 5\n7-level DI validation\n0.10 – 0.50",
]
for i, txt in enumerate(exp_texts):
    xi = 0.25 + i * 1.95
    box(axA, xi, 4.60, 1.70, 1.60, txt, C_SKY, C_NAVY, fs=7.4)
    arrow(axA, xi + 0.85, 6.80, xi + 0.85, 6.25)

box(axA, 0.25, 3.10, 9.50, 1.15,
    "Dependent variables:  discomfort (0–10)  |  workload (0–10)  |  "
    "6-item aesthetic Likert (α = 0.87–0.90)  |  reading persistence (KM, 20-min cap)",
    C_LBLUE, C_NAVY, fs=8.2)
arrow(axA, 5.0, 3.10, 5.0, 2.60)

box(axA, 0.25, 1.20, 9.50, 1.35,
    "Analysis:  mixed / one-way ANOVA  ·  Dunnett & Tukey post hoc  ·  "
    "TOST equivalence  ·  Kaplan–Meier + log-rank  ·  segmented regression  ·  FDR",
    C_SKY, C_NAVY, fs=8.2)

axA.text(-0.02, 10.15, "A", transform=axA.transAxes,
         fontsize=13, fontweight="bold", va="bottom", ha="left")

# ---- Panel B: stimulus materials ----
axB = fig1.add_subplot(gs1[0, 1])
axB.set_xlim(0, 10); axB.set_ylim(0, 10); axB.axis("off")

rng = np.random.default_rng(42)


def make_texture(kind):
    yy, xx = np.mgrid[0:120, 0:120]
    if kind == "pure_white":
        return np.ones((120, 120))
    if kind == "linen":
        base = rng.normal(0.80, 0.06, (120, 120))
        base += 0.06 * np.sin(2 * np.pi * xx / 7.0)
        return np.clip(base, 0, 1)
    if kind == "high_contrast":
        return np.clip(rng.normal(0.50, 0.22, (120, 120)), 0, 1)
    if kind == "high_energy":
        return np.clip(rng.normal(0.72, 0.10, (120, 120)), 0, 1)
    if kind == "matched_beta":
        noise = rng.normal(0, 1, (120, 120))
        F = np.fft.fftshift(np.fft.fft2(noise))
        fy, fx = np.mgrid[-60:60, -60:60]
        f = np.sqrt(fx**2 + fy**2); f[60, 60] = 1e-6
        F *= (f ** (-1.24 / 2.0))
        img = np.real(np.fft.ifft2(np.fft.ifftshift(F)))
        return (img - img.min()) / (img.max() - img.min())
    if kind == "wood":
        base = 0.55 + 0.18 * np.sin(2 * np.pi * (xx * 0.9 + yy * 0.15) / 13.0)
        base += rng.normal(0, 0.04, (120, 120))
        return np.clip(base, 0, 1)
    if kind == "aniso_noise":
        noise = rng.normal(0, 1, (120, 120))
        F = np.fft.fftshift(np.fft.fft2(noise))
        fy, fx = np.mgrid[-60:60, -60:60]
        f = np.sqrt(fx**2 + fy**2); f[60, 60] = 1e-6
        F *= (f ** (-1.95 / 2.0))
        theta = np.arctan2(fy, fx)
        F *= (1 + 0.9 * np.cos(2 * (theta - np.pi / 4)))
        img = np.real(np.fft.ifft2(np.fft.ifftshift(F)))
        return (img - img.min()) / (img.max() - img.min())
    if kind == "cloud":
        return np.clip(rng.normal(0.62, 0.18, (120, 120)), 0, 1)
    return np.ones((120, 120))


def swatch(ax, x, y, w, h, kind, label, sublabel=""):
    img = make_texture(kind)
    ax.imshow(img, extent=[x, x + w, y, y + h], cmap="gray",
              vmin=0, vmax=1, zorder=2, aspect="auto", interpolation="bilinear")
    ax.add_patch(Rectangle((x, y), w, h, fc="none", ec=C_NAVY, lw=1.2, zorder=3))
    ax.text(x + w/2, y + h + 0.10, label, ha="center", va="bottom",
            fontsize=8.0, color="black", zorder=4, linespacing=1.25)
    if sublabel:
        ax.text(x + w/2, y - 0.10, sublabel, ha="center", va="top",
                fontsize=7.0, color=C_DARK, zorder=4)


top_xs = [0.22, 2.17, 4.12, 6.07, 8.02]
top_data = [
    ("pure_white",    "A  Pure white",      "GLCM 0.83 / 0.33"),
    ("linen",         "B  Linen (std.)",    "0.83/0.33 · β 1.24 · DI 0.38"),
    ("high_contrast", "C  High contrast",   "GLCM 0.83 / 0.52"),
    ("high_energy",   "D  High energy",     "GLCM 0.91 / 0.33"),
    ("matched_beta",  "E  Matched-β noise", "β 1.24 · DI 0.02"),
]
for (kind, lab, sub), x in zip(top_data, top_xs):
    swatch(axB, x, 6.55, 1.75, 1.75, kind, lab, sub)

bot_xs = [0.20, 2.65, 5.10, 7.55]
bot_data = [
    ("wood",        "F  Wood grain",     "DI 0.42 · β 1.18"),
    ("aniso_noise", "G  Synthetic aniso.","DI 0.35 · β 1.95"),
    ("cloud",       "H  Cloud (iso.)",   "DI 0.05 · β 2.15"),
    ("linen",       "I  Linen (ctrl)",   "DI 0.38 · β 1.24"),
]
for (kind, lab, sub), x in zip(bot_data, bot_xs):
    swatch(axB, x, 2.40, 2.25, 2.20, kind, lab, sub)

axB.text(-0.02, 10.15, "B", transform=axB.transAxes,
         fontsize=13, fontweight="bold", va="bottom", ha="left")

fig1.suptitle("FIG. 1  Experimental workflow and stimulus materials",
              fontsize=12, fontweight="bold", y=0.975)
save_all(fig1, "FIG1_workflow_stimuli")


# ==================================================================
# FIG. 2 — Higher-order texture statistics + DI threshold
# ==================================================================
fig2 = plt.figure(figsize=(16, 9), facecolor="white")
gs2 = GridSpec(1, 3, figure=fig2, left=0.055, right=0.98,
               top=0.87, bottom=0.13, wspace=0.34)

axA = fig2.add_subplot(gs2[0, 0])
labels = ["Linen\n(B)", "Matched-β\nnoise (E)", "Wood\n(F)", "Cloud\n(H)"]
betas  = [1.24, 1.24, 1.18, 2.15]
errs   = [0.08, 0.05, 0.07, 0.06]
colors = [C_NAVY, C_LBLUE, C_BLUE, C_SKY]
x = np.arange(len(labels))
axA.bar(x, betas, yerr=errs, width=0.60,
        color=colors, edgecolor=C_NAVY, linewidth=1.1,
        error_kw=dict(ecolor="#404040", lw=0.9, capsize=3), zorder=3)
axA.axhline(1.0, color=C_GRAY, lw=0.8, ls=":")
axA.text(-0.42, 1.05, "pink (β=1)", fontsize=7.2, color=C_GRAY,
         va="bottom", ha="left")
axA.axhline(2.0, color=C_GRAY, lw=0.8, ls=":")
axA.text(-0.42, 2.05, "red (β=2)", fontsize=7.2, color=C_GRAY,
         va="bottom", ha="left")
axA.set_xticks(x); axA.set_xticklabels(labels, fontsize=7.8)
axA.set_ylabel("Fourier slope β")
axA.set_ylim(0, 2.9)
axA.set_title("Higher-order texture: β", pad=8)
panel_label(axA, "A")

axB = fig2.add_subplot(gs2[0, 1])
di_vals = [0.38, 0.02, 0.42, 0.05]
di_errs = [0.05, 0.01, 0.06, 0.02]
axB.bar(x, di_vals, yerr=di_errs, width=0.60,
        color=colors, edgecolor=C_NAVY, linewidth=1.1,
        error_kw=dict(ecolor="#404040", lw=0.9, capsize=3), zorder=3)
axB.axhline(0.30, color=C_BLACK, lw=1.2, ls="--", zorder=2)
axB.text(-0.42, 0.315, "candidate DI = 0.30", fontsize=7.4,
         color=C_BLACK, va="bottom", ha="left")
axB.set_xticks(x); axB.set_xticklabels(labels, fontsize=7.8)
axB.set_ylabel("Directional index (DI)")
axB.set_ylim(0, 0.60)
axB.set_title("Higher-order texture: DI", pad=8)
panel_label(axB, "B")

axC = fig2.add_subplot(gs2[0, 2])
di_levels = np.array([0.00, 0.10, 0.20, 0.30, 0.40, 0.50])
dis_mean  = np.array([5.76, 5.67, 5.18, 3.46, 3.14, 3.03])
dis_sd    = np.array([1.39, 1.40, 1.45, 1.33, 1.29, 1.31])

axC.errorbar(di_levels, dis_mean, yerr=dis_sd,
             fmt="o", color=C_NAVY, ecolor=C_NAVY,
             capsize=3.5, capthick=1.1, ms=7,
             mfc="white", mew=1.6, zorder=4, label="Exp 5 (mean ± SD)")
axC.errorbar([0.38], [3.10], yerr=[1.27],
             fmt="s", color=C_BLUE, ecolor=C_BLUE,
             capsize=3.5, capthick=1.1, ms=7,
             mfc=C_SKY, mew=1.6, zorder=4, label="Linen replication")

seg1 = np.polyfit(di_levels[:3], dis_mean[:3], 1)
seg2 = np.polyfit(di_levels[2:], dis_mean[2:], 1)
xs1 = np.linspace(0.00, 0.20, 60)
xs2 = np.linspace(0.20, 0.50, 60)
axC.plot(xs1, np.polyval(seg1, xs1), color=C_LBLUE, lw=1.6, zorder=2)
axC.plot(xs2, np.polyval(seg2, xs2), color=C_NAVY,  lw=1.6, zorder=2)

axC.axvline(0.29, color=C_BLACK, lw=1.2, ls="--", zorder=3)
axC.axvspan(0.26, 0.32, color=C_NAVY, alpha=0.10, zorder=1)
axC.text(0.31, 8.55, "Breakpoint DI = 0.29\n(95% CI 0.26–0.32)",
         fontsize=7.4, color=C_BLACK, va="top", ha="left", linespacing=1.3)

axC.axhspan(0, 3.5, color=C_SKY, alpha=0.35, zorder=0)
axC.text(0.02, 0.90, "comfort zone (< 3.5)",
         fontsize=7.4, color=C_DARK, va="bottom", ha="left")

axC.set_xlabel("Directional index (DI)")
axC.set_ylabel("Discomfort rating (0–10)")
axC.set_xlim(-0.03, 0.55); axC.set_ylim(0, 9.2)
axC.set_title("Experiment 5: segmented regression", pad=8)
axC.legend(loc="lower right", frameon=False, fontsize=7.2,
           handlelength=1.6, labelspacing=0.35)
panel_label(axC, "C")

fig2.suptitle("FIG. 2  Higher-order texture statistics and DI threshold analysis",
              fontsize=12, fontweight="bold", y=0.965)
save_all(fig2, "FIG2_higher_order_texture")


# ==================================================================
# FIG. 3 — Experiment 1 results
# ==================================================================
fig3 = plt.figure(figsize=(16, 9), facecolor="white")
gs3 = GridSpec(1, 2, figure=fig3, left=0.06, right=0.98,
               top=0.87, bottom=0.12, wspace=0.25)

axA = fig3.add_subplot(gs3[0, 0])
x = np.array([0, 1])
pw   = np.array([5.83, 4.40]); pw_e = np.array([1.41, 1.52])
ln   = np.array([3.02, 3.52]); ln_e = np.array([1.25, 1.40])
off = 0.06

axA.errorbar(x - off, pw, yerr=pw_e, fmt="o-", color=C_NAVY,
             capsize=4, lw=1.8, ms=8, mfc="white", mew=1.7,
             label="Pure white", zorder=3)
axA.errorbar(x + off, ln, yerr=ln_e, fmt="s-", color=C_BLUE,
             capsize=4, lw=1.8, ms=8, mfc=C_SKY, mew=1.7,
             label="Linen texture", zorder=3)

axA.set_xticks(x); axA.set_xticklabels(["< 1 lx", "5 lx"])
axA.set_xlabel("Ambient illuminance")
axA.set_ylabel("Discomfort rating (0–10)")
axA.set_xlim(-0.45, 1.45); axA.set_ylim(0, 9.2)
axA.legend(loc="upper right", frameon=False)
axA.set_title("Experiment 1: background × illuminance", pad=8)


def sig_bracket(ax, x1, x2, ybar, txt):
    ax.plot([x1, x1, x2, x2], [ybar - 0.28, ybar, ybar, ybar - 0.28],
            lw=1.0, color="black", clip_on=False)
    ax.text((x1 + x2)/2, ybar + 0.10, txt, ha="center", va="bottom",
            fontsize=10, color="black")


sig_bracket(axA, x[0] - off, x[0] + off, 7.9, "***")
sig_bracket(axA, x[1] - off, x[1] + off, 6.5, "n.s.")
panel_label(axA, "A")

axB = fig3.add_subplot(gs3[0, 1])
t = np.linspace(0, 20, 500)


def surv(t, m, k=1.5):
    lam = m / (np.log(2) ** (1.0 / k))
    return np.exp(-(t / lam) ** k)


S_pw = surv(t, 7.8)
S_ln = surv(t, 13.5)
axB.fill_between(t, 0, S_pw, color=C_SKY, alpha=0.55, zorder=1)
axB.plot(t, S_pw, color=C_NAVY, lw=2.0, label="Pure white (median 7.8 min)", zorder=3)
axB.fill_between(t, 0, S_ln, color=C_LBLUE, alpha=0.55, zorder=2)
axB.plot(t, S_ln, color=C_BLUE, lw=2.0, label="Linen texture (median 13.5 min)", zorder=4)

axB.axvline(7.8,  color=C_NAVY, lw=0.9, ls="--")
axB.axvline(13.5, color=C_BLUE, lw=0.9, ls="--")
axB.axhline(0.5,  color=C_GRAY, lw=0.7, ls=":")

axB.text(7.55, 0.56, "7.8", fontsize=8.5, color=C_NAVY, ha="right", va="bottom")
axB.text(13.25, 0.56, "13.5", fontsize=8.5, color=C_BLUE, ha="right", va="bottom")

axB.text(0.35, 0.14,
         "Completion rate < 1 lx: 21.7% (pure white) vs 57.5% (linen)",
         fontsize=7.6, color=C_DARK, va="bottom", ha="left")

axB.set_xlabel("Reading time (min)")
axB.set_ylabel("Survival probability")
axB.set_xlim(0, 20); axB.set_ylim(0, 1.02)
axB.legend(loc="upper right", frameon=False, fontsize=7.6)
axB.set_title("Experiment 1: Reading persistence (< 1 lx)", pad=8)
panel_label(axB, "B")

fig3.suptitle("FIG. 3  Experiment 1 — basic effect and persistence",
              fontsize=12, fontweight="bold", y=0.965)
save_all(fig3, "FIG3_exp1_results")


# ==================================================================
# FIG. 4 — Experiment 2 ablation
# ==================================================================
fig4 = plt.figure(figsize=(16, 9), facecolor="white")
gs4 = GridSpec(1, 2, figure=fig4, left=0.06, right=0.98,
               top=0.87, bottom=0.14, wspace=0.30,
               width_ratios=[1.15, 1.0])

axA = fig4.add_subplot(gs4[0, 0])
cond = ["A\nPure\nwhite", "B\nLinen\nstandard", "C\nHigh\ncontrast",
        "D\nHigh\nenergy", "E\nMatched-β\nisotropic"]
mean = np.array([5.79, 3.11, 5.08, 4.95, 5.38])
sd   = np.array([1.38, 1.30, 1.55, 1.48, 1.46])
col  = [C_LBLUE, C_NAVY, C_SKY, C_SKY, C_SKY]

xp = np.arange(len(cond))
axA.bar(xp, mean, yerr=sd, width=0.62,
        color=col, edgecolor=C_NAVY, lw=1.1,
        error_kw=dict(ecolor="#404040", lw=0.9, capsize=3), zorder=3)

p_labels = ["ref.", "***", "n.s.", "n.s.", "n.s."]
for xi, lab in zip(range(5), p_labels):
    axA.text(xi, mean[xi] + sd[xi] + 0.28, lab,
             ha="center", va="bottom", fontsize=9.5, color="black")

ybar = 8.55
axA.plot([0, 0, 1, 1], [ybar - 0.28, ybar, ybar, ybar - 0.28],
         lw=1.0, color="black")
axA.text(0.5, ybar + 0.05, "***", ha="center", va="bottom", fontsize=11)

axA.set_xticks(xp); axA.set_xticklabels(cond, fontsize=8)
axA.set_ylabel("Discomfort rating (0–10)")
axA.set_ylim(0, 9.2)
axA.set_title("Experiment 2: five-level ablation", pad=8)
panel_label(axA, "A")

axB = fig4.add_subplot(gs4[0, 1])
persist = np.array([7.5, 13.0, 8.0, 8.3, 7.9])
col2 = [C_LBLUE, C_NAVY, C_SKY, C_SKY, C_SKY]
axB.barh(np.arange(len(cond))[::-1], persist,
         color=col2, edgecolor=C_NAVY, lw=1.1, height=0.62, zorder=3)
for i, v in enumerate(persist):
    axB.text(v + 0.20, len(cond) - 1 - i, f"{v:.1f}",
             va="center", ha="left", fontsize=8.5)
axB.axvline(20, color=C_GRAY, lw=0.8, ls=":")
axB.text(19.6, -0.55, "cap = 20 min", fontsize=7.4,
         color=C_GRAY, ha="right", va="top")
axB.set_yticks(np.arange(len(cond))[::-1])
axB.set_yticklabels([c.replace("\n", " ") for c in cond], fontsize=8)
axB.set_xlabel("Median reading persistence (min)")
axB.set_xlim(0, 21.5)
axB.set_title("Experiment 2: median persistence", pad=8)
panel_label(axB, "B")

fig4.suptitle("FIG. 4  Experiment 2 — redesigned ablation with corrected matched-β isotropic noise",
              fontsize=12, fontweight="bold", y=0.965)
save_all(fig4, "FIG4_exp2_ablation")


# ==================================================================
# FIG. 5 — Experiment 4 + Experiment 5 validation
# ==================================================================
fig5 = plt.figure(figsize=(16, 9), facecolor="white")
gs5 = GridSpec(1, 3, figure=fig5, left=0.055, right=0.98,
               top=0.87, bottom=0.12, wspace=0.34)

axA = fig5.add_subplot(gs5[0, 0])
labels = ["F\nWood\ngrain", "G\nSynthetic\naniso.", "H\nCloud\n(iso.)",
          "I\nLinen\n(ctrl)"]
means = np.array([3.15, 3.42, 5.61, 3.08])
sds   = np.array([1.31, 1.35, 1.42, 1.28])
cols  = [C_LBLUE, C_LBLUE, C_SKY, C_NAVY]
xp = np.arange(4)
axA.bar(xp, means, yerr=sds, width=0.62,
        color=cols, edgecolor=C_NAVY, lw=1.1,
        error_kw=dict(ecolor="#404040", lw=0.9, capsize=3), zorder=3)

p_labels4 = ["n.s.", "n.s.", "***", "ref."]
for i, lab in zip(range(4), p_labels4):
    axA.text(i, means[i] + sds[i] + 0.28, lab,
             ha="center", va="bottom", fontsize=9.5)

ybar = 8.50
axA.plot([0, 0, 3, 3], [ybar - 0.28, ybar, ybar, ybar - 0.28],
         lw=1.0, color="black")
axA.text(1.5, ybar + 0.05, "n.s.", ha="center", va="bottom", fontsize=9)

ybar2 = 7.35
axA.plot([2, 2, 3, 3], [ybar2 - 0.28, ybar2, ybar2, ybar2 - 0.28],
         lw=1.0, color="black")
axA.text(2.5, ybar2 + 0.05, "***", ha="center", va="bottom", fontsize=10)

axA.set_xticks(xp); axA.set_xticklabels(labels, fontsize=7.8)
axA.set_ylabel("Discomfort rating (0–10)")
axA.set_ylim(0, 9.2)
axA.set_title("Experiment 4: directional structure", pad=8)
panel_label(axA, "A")

axB = fig5.add_subplot(gs5[0, 1])
di_matched = np.array([0.10, 0.20, 0.30, 0.40, 0.50])
dis_m      = np.array([5.67, 5.18, 3.46, 3.14, 3.03])
dis_m_sd   = np.array([1.40, 1.45, 1.33, 1.29, 1.31])

axB.errorbar(di_matched, dis_m, yerr=dis_m_sd,
             fmt="o-", color=C_NAVY, capsize=4, capthick=1.1,
             lw=1.8, ms=7.5, mfc="white", mew=1.6, zorder=4,
             label="Matched-β noise")
axB.errorbar([0.00], [5.76], yerr=[1.39],
             fmt="s", color=C_LBLUE, capsize=4, capthick=1.1,
             ms=7.5, mfc="white", mew=1.6, zorder=4,
             label="Pure white")
axB.errorbar([0.38], [3.10], yerr=[1.27],
             fmt="D", color=C_BLUE, capsize=4, capthick=1.1,
             ms=7.5, mfc=C_SKY, mew=1.6, zorder=4,
             label="Linen replication")

axB.axvline(0.30, color=C_BLACK, lw=1.2, ls="--", zorder=2)
axB.text(0.315, 8.55, "candidate DI = 0.30", fontsize=7.6,
         color=C_BLACK, va="top", ha="left")

axB.axhspan(0, 3.5, color=C_SKY, alpha=0.35, zorder=0)
axB.text(0.02, 0.90, "comfort zone (< 3.5)",
         fontsize=7.4, color=C_DARK, va="bottom", ha="left")

axB.set_xlabel("Directional index (DI)")
axB.set_ylabel("Discomfort rating (0–10)")
axB.set_xlim(-0.03, 0.55); axB.set_ylim(0, 9.2)
axB.set_title("Experiment 5: DI dose–response", pad=8)
axB.legend(loc="lower right", frameon=False, fontsize=7.2,
           handlelength=1.6, labelspacing=0.35)
panel_label(axB, "B")

axC = fig5.add_subplot(gs5[0, 2])
pts_iso = np.array([
    [0.00, 5.79], [0.02, 5.38], [0.05, 5.61],
    [0.10, 5.67], [0.20, 5.18],
])
pts_aniso = np.array([
    [0.30, 3.46], [0.35, 3.42], [0.38, 3.11], [0.38, 3.08],
    [0.40, 3.14], [0.42, 3.15], [0.50, 3.03],
])
pts_glcm = np.array([
    [0.38, 5.08], [0.38, 4.95],
])

axC.scatter(pts_iso[:, 0], pts_iso[:, 1], s=75, c=C_LBLUE,
            edgecolors=C_NAVY, lw=1.2,
            label="Isotropic (DI < 0.20)", zorder=4)
axC.scatter(pts_aniso[:, 0], pts_aniso[:, 1], s=75, c=C_NAVY,
            edgecolors=C_NAVY, lw=1.2,
            label="Anisotropic (DI ≥ 0.30)", zorder=4)
axC.scatter(pts_glcm[:, 0], pts_glcm[:, 1], s=75, c="white",
            edgecolors=C_BLACK, lw=1.6, marker="D",
            label="GLCM perturbed (C, D)", zorder=4)

axC.axvline(0.30, color=C_BLACK, lw=1.2, ls="--", zorder=2)
axC.text(0.315, 8.55, "candidate DI = 0.30", fontsize=7.6,
         color=C_BLACK, va="top", ha="left")
axC.axhspan(0, 3.5, color=C_SKY, alpha=0.35, zorder=0)

axC.set_xlabel("Directional index (DI)")
axC.set_ylabel("Discomfort rating (0–10)")
axC.set_xlim(-0.03, 0.55); axC.set_ylim(0, 9.2)
axC.set_title("Pooled: DI vs discomfort", pad=8)
axC.legend(loc="lower left", frameon=False, fontsize=7.2,
           handletextpad=0.4, labelspacing=0.4)
panel_label(axC, "C")

fig5.suptitle("FIG. 5  Experiment 4 and Experiment 5 — directional anisotropy validation",
              fontsize=12, fontweight="bold", y=0.965)
save_all(fig5, "FIG5_exp4_exp5_validation")


print("\nAll 5 figures generated in figures/ (PNG / TIFF / PDF, 600 DPI, 16:9).")
