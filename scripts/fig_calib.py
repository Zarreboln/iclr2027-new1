#!/usr/bin/env python3
"""Appendix calibration figure: R@1 on SF-XL val against tau (patch-importance threshold) and
against theta (rerank gate). Same face as the teaser: Comic Sans, the teaser ink and accent,
a rounded panel with a faint hatch, the chosen operating point marked with the teaser's star."""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from matplotlib.path import Path as MPath

TAU_X = [0, .10, .20, .30, .35, .40, .45, .50, .55, .60, .70]
TAU_Y = [82.09, 87.36, 89.09, 89.40, 90.05, 90.34, 90.50, 90.82, 90.61, 90.50, 89.95]
TH_X  = [0, .20, .30, .40, .50, .55, .60, .65, .70, .75, .80]
TH_Y  = [86.95, 86.91, 85.21, 81.96, 84.77, 87.50, 89.74, 90.76, 90.28, 88.56, 83.90]
PICK  = {"tau": .50, "theta": .65}

INK   = "#2B2B2B"; BLUE = "#3E5C8A"; OURS = "#C0233A"; GREY = "#8E8E8E"
FRAME = "#3E5C8A"; WASH = "#F7F4F2"
plt.rcParams.update({"font.family": "Comic Sans MS", "axes.linewidth": 0.9,
                     "text.color": INK, "axes.labelcolor": INK,
                     "xtick.color": INK, "ytick.color": INK})

fig, axes = plt.subplots(1, 2, figsize=(7.4, 2.55))
fig.subplots_adjust(left=.085, right=.985, top=.845, bottom=.20, wspace=.26)

def panel(ax, xs, ys, pick, title, xlabel):
    ax.set_facecolor(WASH)
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    for s in ("left", "bottom"): ax.spines[s].set_color(INK)
    ax.grid(axis="y", color=GREY, lw=.5, ls=(0, (2, 3)), alpha=.55); ax.set_axisbelow(True)
    ax.plot(xs, ys, color=BLUE, lw=1.9, marker="o", ms=3.6, mfc="white", mew=1.2, zorder=3)
    i = xs.index(pick)
    ax.plot([pick], [ys[i]], marker="*", ms=15, color=OURS, zorder=4, lw=0)
    ax.annotate(f"{ys[i]:.2f}", (pick, ys[i]), textcoords="offset points", xytext=(2, 9),
                ha="center", fontsize=8.5, color=OURS)
    lo, hi = min(ys), max(ys); pad = (hi - lo) * .18
    ax.set_ylim(lo - pad, hi + pad * 1.9)
    ax.set_title(title, fontsize=10.5, color=FRAME, pad=6)
    ax.set_xlabel(xlabel, fontsize=9)
    ax.set_ylabel("R@1 (%)", fontsize=9)
    ax.tick_params(labelsize=8, length=3)

panel(axes[0], TAU_X, TAU_Y, PICK["tau"],   "Patch-importance threshold $\\tau$", "$\\tau$   ($\\tau{=}0$ is unweighted)")
panel(axes[1], TH_X,  TH_Y,  PICK["theta"], "Rerank gate $\\theta$",              "$\\theta$")
fig.savefig("/Users/zarreboln/Desktop/iclr2027-new/figures/fig_calib.pdf")
fig.savefig("/Users/zarreboln/Desktop/vpr/figures/fig_calib.png", dpi=190)
print("saved")
