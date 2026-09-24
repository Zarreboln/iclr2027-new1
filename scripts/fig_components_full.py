#!/usr/bin/env python3
"""Full version of Figure 5(a): component increments on all 17 benchmarks (numbers of the supplementary component table)."""
import numpy as np, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.patches import Patch
plt.rcParams.update({"font.family":"Comic Sans MS","font.size":10,"font.weight":"bold","axes.labelweight":"bold","pdf.fonttype":42,"ps.fonttype":42})
GRID,INK,MUTE="#E6E6E6","#2B2B2B","#9A9A9A"; C=["#B9C6D6","#C0736C","#2F7E96","#C0233A"]
D=[("Pitts250k",82.3,92.3,93.8,95.7),("Pitts30k",79.4,89.4,91.0,92.5),("Tokyo 24/7",87.3,87.0,96.8,97.5),("MSLS-val",34.9,76.1,85.4,89.1),("Nordland",23.5,58.4,76.1,83.0),("St Lucia",79.6,95.2,99.0,99.0),("Oxford",97.4,90.1,99.5,99.0),("AmsterTime",31.4,47.5,67.3,68.1),
   ("Hawkins",67.8,42.4,67.8,67.0),("Laurel",52.7,49.1,78.6,83.0),("17 Places",64.5,63.8,65.8,65.5),("Gardens",96.0,95.5,99.0,99.5),("Baidu",63.3,72.7,84.7,84.5),("Nardo-Air",71.8,77.5,84.5,83.1),("Nardo-Air R",78.9,95.8,85.9,94.4),("VP-Air",46.0,49.3,61.4,72.1),("Mid-Atlantic",35.6,37.6,38.6,37.6)]
LAB=["second moment","+ weighted second moment","+ MaxSim","+ weighted MaxSim"]
fig,ax=plt.subplots(figsize=(13.5,3.9)); x=np.arange(len(D)); bw=0.16
for j in range(4):
    vals=[d[1+j] for d in D]; ax.bar(x+(j-1.5)*bw,vals,bw,color=C[j],edgecolor="white",lw=0.6,zorder=3)
for i,d in enumerate(D): ax.text(x[i]+1.5*bw,d[4]+1.2,"%.1f"%d[4],ha="center",va="bottom",fontsize=7.5,color=C[3])
ax.set_xticks(x); ax.set_xticklabels([d[0] for d in D],fontsize=9,rotation=28,ha="right"); ax.set_ylim(0,106); ax.set_yticks([0,20,40,60,80,100]); ax.set_ylabel("R@1 (%)")
ax.grid(axis="y",color=GRID,lw=1.0,zorder=0); ax.set_axisbelow(True)
for s in ("top","right"): ax.spines[s].set_visible(False)
for s in ("left","bottom"): ax.spines[s].set_color(MUTE)
ax.axvline(7.5,color=MUTE,lw=0.8,ls="--"); ax.text(3.5,103,"standard VPR benchmarks",ha="center",fontsize=9,color=MUTE); ax.text(12.5,103,"cross-environment VPR benchmarks",ha="center",fontsize=9,color=MUTE)
ax.legend(handles=[Patch(facecolor=C[j],label=LAB[j]) for j in range(4)],frameon=False,fontsize=9,loc="upper center",bbox_to_anchor=(0.5,-0.28),ncol=4)
plt.savefig("/Users/zarreboln/Desktop/iclr2027-new/figures/fig_components_full.pdf",bbox_inches="tight"); print("saved")
