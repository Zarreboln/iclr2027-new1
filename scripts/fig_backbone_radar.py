#!/usr/bin/env python3
"""Figure 6: matched-backbone radar over all 17 benchmarks (DINOv3 rows of Table 7).
Baselines from /home/tmp_l/logs/baseline_table.md (+ Pitts250k: SALAD-7B 96.16, BoQ-7B 96.85);
Ours = Ours v3 rows of the main tables, two-decimal values from s2_final_*_7b_newS1.log."""
import numpy as np, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
import os,sys; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); import house_style as H; H.rc(10)
LAB=["Pitts250k","Pitts30k","Tokyo 24/7","MSLS-val","Nordland","St Lucia","Oxford","AmsterTime","Baidu Mall","17 Places","Gardens Pt","Hawkins","Laurel","Nardo-Air","Nardo-Air R","VP-Air","Mid-Atlantic"]
S=[96.16,93.31,97.78,89.05,90.99,99.93,94.24,64.34,64.41,62.32,95.50,44.07,61.61,78.87,87.32,42.65,19.80]
B=[96.85,94.40,98.73,91.89,94.34,100.00,98.95,68.16,71.66,63.79,98.50,33.05,48.21,84.51,100.00,49.82,21.78]
C=[96.09,93.63,98.10,93.51,94.76,100.00,98.95,60.44,68.59,61.58,95.00,22.03,37.50,76.06,90.14,47.19,13.86]
O=[96.12,93.74,98.41,89.32,96.56,99.73,98.95,73.60,83.45,65.27,99.50,61.02,75.89,91.55,97.18,77.64,37.62]
SER=[("SALAD",S,H.MEGALOC,"--",1.5),("BoQ",B,H.ANYLOC,"--",1.5),("CliqueMining",C,H.W_DARK,"--",1.5),("Ours",O,H.OURS,"-",2.4)]
n=len(LAB); ang=np.linspace(0,2*np.pi,n,endpoint=False); ang2=np.r_[ang,ang[0]]
fig=plt.figure(figsize=(6.6,6.2)); ax=fig.add_subplot(111,polar=True); ax.set_theta_zero_location("N"); ax.set_theta_direction(-1)
ax.set_ylim(0,100); ax.set_yticks([20,40,60,80,100]); ax.set_yticklabels(["20","","60","","100"],fontsize=8,color="#8A8A8A")
ax.yaxis.grid(True,color="#BEBEBE",ls=(0,(3,3)),lw=0.8); ax.xaxis.grid(True,color="#D9D9D9",ls=(0,(2,3)),lw=0.7)
ax.spines["polar"].set_color("#2B2B2B"); ax.spines["polar"].set_linewidth(1.0); ax.set_rlabel_position(97)
ax.set_xticks(ang); ax.set_xticklabels([]); 
for a,l in zip(ang,LAB):
    ha="center" if abs(np.sin(a))<0.15 else ("left" if np.sin(a)>0 else "right")
    ax.text(a,112,l,fontsize=10,color="#2B2B2B",ha=ha,va="center")
for name,v,col,ls,lw in SER:
    vv=np.r_[v,v[0]]; ax.plot(ang2,vv,color=col,ls=ls,lw=lw,label=name,zorder=4 if name=="Ours" else 3)
    if name=="Ours": ax.fill(ang2,vv,color=col,alpha=0.13,zorder=2)
ax.legend(loc="upper center",bbox_to_anchor=(0.5,-0.06),ncol=4,frameon=False,fontsize=10.5,handlelength=2.2,columnspacing=1.6)
plt.savefig("/Users/zarreboln/Desktop/iclr2027-new/figures/fig_backbone_radar.pdf",bbox_inches="tight"); print("saved radar")
