#!/usr/bin/env python3
"""Full versions of Figure 5(b) and 5(c) for every benchmark, from the data of eval/fig5_full.py (H100)."""
import sys,json,numpy as np, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap; import matplotlib.gridspec as gs; from PIL import Image
D=sys.argv[1]; OUT="/Users/zarreboln/Desktop/iclr2027-new/figures"
plt.rcParams.update({"font.family":"Comic Sans MS","font.size":9,"font.weight":"bold","axes.labelweight":"bold","pdf.fonttype":42,"ps.fonttype":42,"mathtext.default":"regular"})
GRID,INK,MUTE="#E6E6E6","#2B2B2B","#9A9A9A"; C_UNW,C_W="#C0233A","#2F7E96"
ORDER=[("pitts250k","Pitts250k"),("pitts30k","Pitts30k"),("tokyo247","Tokyo 24/7"),("msls_val","MSLS-val"),("nordland","Nordland"),("st_lucia","St Lucia"),("oxford","Oxford"),("amstertime","AmsterTime"),
       ("hawkins","Hawkins"),("laurel","Laurel"),("17places","17 Places"),("gardens","Gardens"),("baidu","Baidu"),("nardo_air","Nardo-Air"),("nardo_air_r","Nardo-Air R"),("vpair","VP-Air"),("eiffel","Mid-Atlantic")]
# ---------- (b) full: 17 energy curves ----------
z=np.load(f"{D}/curves.npz",allow_pickle=True)
fig,axes=plt.subplots(3,6,figsize=(13,6.2)); axes=axes.ravel()
for k,(ds,name) in enumerate(ORDER):
    a=axes[k]; c0,c1,g=z[f"{ds}_c0"],z[f"{ds}_c1"],float(z[f"{ds}_gap"]); x=np.arange(1,len(c0)+1)
    a.plot(x,100*c0,lw=1.6,color=C_UNW); a.plot(x,100*c1,lw=1.6,color=C_W); a.fill_between(x,100*c1,100*c0,where=(c0>=c1),color=C_UNW,alpha=.13,lw=0)
    a.set_xscale("log"); a.set_xlim(1,1536); a.set_ylim(0,100); a.set_xticks([1,10,100,1000]); a.set_xticklabels(["1","10","100","1000"],fontsize=7); a.set_yticks([0,50,100]); a.tick_params(labelsize=7,colors=INK)
    a.grid(color=GRID,lw=0.8); a.set_axisbelow(True)
    for s in ("top","right"): a.spines[s].set_visible(False)
    for s in ("left","bottom"): a.spines[s].set_color(MUTE)
    a.set_title(name,fontsize=9,pad=3); a.text(.97,.08,"gap %.1f"%g,transform=a.transAxes,ha="right",fontsize=7.5,color=INK)
axes[17].axis("off"); axes[17].plot([],[],lw=1.6,color=C_UNW,label="unweighted  $F^TF$"); axes[17].plot([],[],lw=1.6,color=C_W,label="weighted  $F^TWF$"); axes[17].legend(loc="center",frameon=False,fontsize=9)
fig.text(0.5,0.01,"directions kept",ha="center",fontsize=10); fig.text(0.005,0.5,"energy captured (%)",va="center",rotation=90,fontsize=10)
plt.tight_layout(rect=(0.015,0.03,1,1)); plt.savefig(f"{OUT}/fig_energy_full.pdf",bbox_inches="tight"); plt.close(fig); print("saved energy full")
# ---------- (c) full: MaxSim without / with w on one pair per benchmark ----------
L=np.load(f"{D}/lines.npz",allow_pickle=True); RES=336; G=48; sc=RES/672.0; TOP=24; GAP=6
cmap=LinearSegmentedColormap.from_list("cm",["#00C8D7","#D000B4"])
def xy(idx,off): r,c=divmod(int(idx),G); return off+(c*14+7)*sc, (r*14+7)*sc
def draw_gallery(items,fname):
    n=len(items); fig=plt.figure(figsize=(9.2,1.6*n+0.35)); grid=gs.GridSpec(n+1,2,height_ratios=[1]*n+[0.12],hspace=0.06,wspace=0.04)
    for r,(ds,name) in enumerate(items):
        cu,cw,mi,ji=L[f"{ds}_cu"],L[f"{ds}_cw"],L[f"{ds}_mi"],L[f"{ds}_ji"]
        imq=Image.open(f"{D}/{ds}_q.png"); imd=Image.open(f"{D}/{ds}_d.png"); canvas=Image.new("RGB",(2*RES+GAP,RES),"white"); canvas.paste(imq,(0,0)); canvas.paste(imd,(RES+GAP,0))
        su=np.argsort(-cu)[:TOP]; sw=np.argsort(-cw)[:TOP]; al=np.union1d(su,sw); lo,hi=mi[al].min(),mi[al].max()
        for col,(c,sel) in enumerate([(cu,su),(cw,sw)]):
            ax=fig.add_subplot(grid[r,col]); ax.imshow(canvas); ax.set_xticks([]); ax.set_yticks([])
            for s in ax.spines.values(): s.set_color(MUTE); s.set_linewidth(0.6)
            for i in sel:
                if c[i]<=0: continue
                x0,y0=xy(i,0); x1,y1=xy(ji[i],RES+GAP); colr=cmap((mi[i]-lo)/max(hi-lo,1e-6))
                ax.plot([x0,x1],[y0,y1],color=colr,lw=0.7,alpha=0.95,solid_capstyle="round"); ax.plot([x0,x1],[y0,y1],ls="none",marker="o",ms=1.1,mec="none",mfc=colr)
            if col==0: ax.set_ylabel(name,fontsize=9)
            if r==0: ax.set_title("without $w$" if col==0 else "with $w$",fontsize=10,pad=4)
    cax=fig.add_subplot(grid[n,:]); cax.imshow(np.linspace(0,1,256)[None,:],aspect="auto",cmap=cmap); cax.set_yticks([]); cax.set_xticks([0,255]); cax.set_xticklabels(["weaker","stronger"],fontsize=8); cax.tick_params(length=0,colors=INK)
    for s in cax.spines.values(): s.set_visible(False)
    cax.set_xlabel("match strength $m_i$",fontsize=8.5,labelpad=1)
    plt.savefig(f"{OUT}/{fname}",bbox_inches="tight",dpi=200); plt.close(fig); print("saved",fname)
draw_gallery(ORDER[:9],"fig_maxsim_full_1.pdf"); draw_gallery(ORDER[9:],"fig_maxsim_full_2.pdf")
