"""House style shared by every matplotlib figure of the paper: the palette of Figure 1 (teaser) and Figure 2 (method).

Roles (Figure 2 legend): query patch = blue, database patch = purple, weight = amber shades, coarse descriptor = green,
patch matching = coral; ink 2B2B2B, muted 8E8E8E, dashed grey grid, dashed rounded panel frames in the deck's blue.
Series (Figure 1): Ours C0233A, MegaLoc C0736C, AnyLoc 2F7E96.
"""
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import FancyBboxPatch

FONT = "Comic Sans MS"
INK, MUTE, GRID = "#2B2B2B", "#8E8E8E", "#C9C9C9"
FRAME = "#3E5C8A"                       # analysis panels (teaser bottom row)
RED_ROLE, GREEN_ROLE = "#B31E2E", "#1E7A46"   # trained / ours frames of the teaser
Q_FILL, Q_INK = "#A3BBDF", "#4F6FB5"    # query
D_FILL, D_INK = "#C9B8E0", "#927CC0"    # database
W_LIGHT, W_MID, W_DARK = "#F0E1BE", "#DDB04A", "#A9761A"   # weight shades (darker = larger)
C_FILL, C_INK, C_DARK = "#B7D9C3", "#6BA37F", "#3F8A5C"    # coarse (second moment)
M_FILL, M_INK, M_DARK = "#E8B8AA", "#C45B3C", "#8E2F1B"    # matching (MaxSim)
OURS, MEGALOC, ANYLOC = "#C0233A", "#C0736C", "#2F7E96"

WEIGHT_CMAP = LinearSegmentedColormap.from_list("weight", ["#FBF6EA", W_LIGHT, W_MID, W_DARK])
MATCH_CMAP = LinearSegmentedColormap.from_list("match", [W_MID, M_INK, M_DARK])   # weaker = amber, stronger = deep coral; stays visible on snow and foliage
COMPONENTS = [C_FILL, C_DARK, M_FILL, M_INK]   # second moment, + weighted, + MaxSim, + weighted


def rc(size=10):
    plt.rcParams.update({"font.family": FONT, "font.size": size, "font.weight": "bold", "axes.labelweight": "bold",
                         "axes.titleweight": "bold", "pdf.fonttype": 42, "ps.fonttype": 42, "mathtext.default": "regular",
                         "text.color": INK, "axes.labelcolor": INK, "xtick.color": INK, "ytick.color": INK})


def clean(ax, labelsize=9):
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    for s in ("left", "bottom"): ax.spines[s].set_color(MUTE)
    ax.tick_params(colors=INK, labelsize=labelsize)


def dgrid(ax, axis="both", lw=0.8):
    ax.grid(axis=axis, color=GRID, lw=lw, ls=(0, (4, 3)), zorder=0); ax.set_axisbelow(True)


def frame(fig, color=FRAME, pad=0.012, lw=1.6, rounding=0.02):
    """dashed rounded frame around the whole figure, as the teaser fences its panels"""
    p = FancyBboxPatch((pad, pad), 1 - 2 * pad, 1 - 2 * pad, boxstyle=f"round,pad=0,rounding_size={rounding}",
                       transform=fig.transFigure, fill=False, ec=color, lw=lw, ls=(0, (5, 3)), zorder=10, clip_on=False)
    fig.patches.append(p)
    return p


def border(ax, color, lw=1.6):
    for s in ax.spines.values(): s.set_visible(True); s.set_color(color); s.set_linewidth(lw)
