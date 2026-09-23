#!/usr/bin/env python3
"""Figure 5, three panels in one style (teaser font/colours).
(a) component increments (numbers from the main tables), legend below;
(b) first-stage energy curve (data: energy_curve.npz from eval/fig5_bc.py on the H100);
(c) MaxSim lines with and without w on the Nordland pair (data: maxsim_lines.npz + pair_{q,d}.png)."""
import sys, numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.patches import Patch; from matplotlib.colors import LinearSegmentedColormap
import matplotlib.gridspec as gs; from PIL import Image
D, OUT = sys.argv[1], sys.argv[2]
FONT="Comic Sans MS"
plt.rcParams.update({"font.family":FONT,"font.size":10,"font.weight":"bold","axes.labelweight":"bold",
                     "pdf.fonttype":42,"ps.fonttype":42,"mathtext.default":"regular"})
GRID,INK,MUTE="#E6E6E6","#2B2B2B","#9A9A9A"
C=["#B9C6D6","#C0736C","#2F7E96","#C0233A"]; C_UNW,C_W=C[3],C[2]
def clean(ax):
    for s in ("top","right"): ax.spines[s].set_visible(False)
    for s in ("left","bottom"): ax.spines[s].set_color(MUTE)
    ax.tick_params(colors=INK,labelsize=9)
# ---------------- (a) ----------------
DS=["VP-Air","AmsterTime"]; V={"VP-Air":[46.0,48.2,61.4,72.1],"AmsterTime":[31.4,47.6,67.3,68.1]}
LAB=["second moment","+ weighted second moment","+ MaxSim","+ weighted MaxSim"]
fig,ax=plt.subplots(figsize=(3.0,3.0)); x=np.arange(2); bw=0.56
for k,ds in enumerate(DS):
    v=V[ds]; ax.bar(k,v[0],bw,color=C[0],edgecolor="white",lw=0.8,zorder=3)
    ax.text(k,(20+v[0])/2,"%.1f"%v[0],ha="center",va="center",fontsize=9,color=INK)
    for j in range(1,4):
        inc=v[j]-v[j-1]
        ax.bar(k,inc,bw,bottom=v[j-1],color=C[j],edgecolor="white",lw=0.8,zorder=3)
        if inc>=4: ax.text(k,v[j-1]+inc/2,"+%.1f"%inc,ha="center",va="center",fontsize=8.5,color="white")
        else: ax.text(k+bw/2+0.03,v[j-1]+inc/2,"+%.1f"%inc,ha="left",va="center",fontsize=8,color=C[j])
    ax.text(k,v[3]+1.2,"%.1f"%v[3],ha="center",va="bottom",fontsize=10,color=C[3])
ax.set_xticks(x); ax.set_xticklabels(DS,fontsize=10); ax.set_xlim(-0.55,1.75)
ax.set_ylim(20,82); ax.set_yticks([20,40,60,80]); ax.set_ylabel("R@1 (%)",fontsize=10)
ax.grid(axis="y",color=GRID,lw=1.0,zorder=0); ax.set_axisbelow(True); clean(ax)
ax.legend(handles=[Patch(facecolor=C[j],label=LAB[j]) for j in range(4)],frameon=False,fontsize=7.6,
          loc="upper center",bbox_to_anchor=(0.45,-0.26),ncol=2,handlelength=1.1,columnspacing=0.9,labelspacing=0.4)
plt.savefig(f"{OUT}/fig_components.pdf",bbox_inches="tight"); plt.close(fig)
# ---------------- (b) ----------------
z=np.load(f"{D}/energy_curve.npz",allow_pickle=True); c0,c1,g=z["c0"],z["c1"],float(z["gap"]); xx=np.arange(1,len(c0)+1)
fig,a=plt.subplots(figsize=(2.9,2.7))
a.plot(xx,100*c0,lw=2.0,color=C_UNW,label="unweighted  $F^TF$"); a.plot(xx,100*c1,lw=2.0,color=C_W,label="weighted  $F^TWF$")
a.fill_between(xx,100*c1,100*c0,where=(c0>=c1),color=C_UNW,alpha=.13,lw=0)
a.set_xscale("log"); a.set_xlim(1,1536); a.set_ylim(0,100); a.set_xticks([1,10,100,1000]); a.set_xticklabels(["1","10","100","1000"])
a.set_yticks([0,20,40,60,80,100]); a.grid(color=GRID,lw=1.0,zorder=0); a.set_axisbelow(True); clean(a)
a.set_xlabel("directions kept",fontsize=10); a.set_ylabel("energy captured (%)",fontsize=10)
a.text(.97,.07,"gap %.1f pts"%g,transform=a.transAxes,ha="right",fontsize=9,color=INK)
a.legend(fontsize=8.2,frameon=False,loc="upper left",handlelength=1.4,borderaxespad=0.2)
plt.savefig(f"{OUT}/fig_energy_one.pdf",bbox_inches="tight"); plt.close(fig)
# ---------------- (c) ----------------
L=np.load(f"{D}/maxsim_lines.npz",allow_pickle=True); cu,cw,mi,ji,G,RES=L["cu"],L["cw"],L["mi"],L["ji"],int(L["G"]),int(L["RES"])
TOP=int(sys.argv[3]) if len(sys.argv)>3 else 24; GAP=10
imq=Image.open(f"{D}/pair_q.png"); imd=Image.open(f"{D}/pair_d.png")
canvas=Image.new("RGB",(2*RES+GAP,RES),"white"); canvas.paste(imq,(0,0)); canvas.paste(imd,(RES+GAP,0))
cmap=LinearSegmentedColormap.from_list("cm",["#00C8D7","#D000B4"])
def xy(idx,off): r,c=divmod(int(idx),G); return off+c*14+7, r*14+7
su=np.argsort(-cu)[:TOP]; sw=np.argsort(-cw)[:TOP]; al=np.union1d(su,sw); lo,hi=mi[al].min(),mi[al].max()
fig=plt.figure(figsize=(3.3,3.55)); grid=gs.GridSpec(3,1,height_ratios=[1,1,0.09],hspace=0.12)
for k,(title,c,sel) in enumerate([("without $w$",cu,su),("with $w$",cw,sw)]):
    ax=fig.add_subplot(grid[k]); ax.imshow(canvas); ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values(): s.set_color(MUTE); s.set_linewidth(0.8)
    ax.set_ylabel(title,fontsize=11.5); cmax=c[sel].max()
    for i in sel:
        if c[i]<=0: continue
        x0,y0=xy(i,0); x1,y1=xy(ji[i],RES+GAP); col=cmap((mi[i]-lo)/max(hi-lo,1e-6))
        ax.plot([x0,x1],[y0,y1],color=col,lw=0.35+0.8*c[i]/cmax,alpha=0.95,solid_capstyle="round")
        ax.plot([x0,x1],[y0,y1],ls="none",marker="o",ms=1.4,mec="none",mfc=col)
cax=fig.add_subplot(grid[2]); cax.imshow(np.linspace(0,1,256)[None,:],aspect="auto",cmap=cmap); cax.set_yticks([])
cax.set_xticks([0,255]); cax.set_xticklabels(["weaker","stronger"],fontsize=9.5); cax.tick_params(length=0,colors=INK)
for s in cax.spines.values(): s.set_visible(False)
cax.set_xlabel("match strength $m_i$   (line width: contribution $c_i$)",fontsize=9.5,labelpad=2)
plt.savefig(f"{OUT}/fig_maxsim_w_stack.pdf",bbox_inches="tight",dpi=220); plt.close(fig); print("saved 3 panels")
