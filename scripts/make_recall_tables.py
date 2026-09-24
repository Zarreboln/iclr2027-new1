#!/usr/bin/env python3
"""Supplementary tables with Recall@1/5/10 from notes/recall_k_supp.json -> stdout (LaTeX)."""
import json,sys
J=json.load(open("/Users/zarreboln/Desktop/iclr2027-new/notes/recall_k_supp.json"))
STD,CROSS=J["order_std"],J["order_cross"]
def cell(d,ds):
    v=d.get(ds); return " & ".join(f"{x:.1f}" for x in v) if v else " & ".join(["--"]*3)
def row(ds,dicts): return ds+" & "+" & ".join(cell(d,ds) for d in dicts)+r" \\"
def group(title,ncol): return r"\multicolumn{%d}{l}{\emph{%s}} \\"%(ncol,title)
out=[]
# ---- Table A: ours v2 / v3 ----
out.append(r"""\begin{table}[H]
\caption{Recall@1, 5 and 10 of our pipeline on all 17 benchmarks, with DINOv2 (\emph{v2}) and DINOv3 (\emph{v3}), in the configuration of the main tables.}
\label{tab:recallk-ours}
\centering
{\footnotesize\setlength{\tabcolsep}{5pt}
\begin{tabular}{l ccc ccc}
\toprule
& \multicolumn{3}{c}{Ours \emph{v2} (DINOv2)} & \multicolumn{3}{c}{Ours \emph{v3} (DINOv3)} \\
\cmidrule(lr){2-4}\cmidrule(lr){5-7}
Benchmark & R@1 & R@5 & R@10 & R@1 & R@5 & R@10 \\
\midrule
"""+group("Standard VPR benchmarks",7)+"\n"+"\n".join(row(d,[J["ours_v2"],J["ours_v3"]]) for d in STD)+"\n\\midrule\n"+group("Cross-environment VPR benchmarks",7)+"\n"+"\n".join(row(d,[J["ours_v2"],J["ours_v3"]]) for d in CROSS)+r"""
\bottomrule
\end{tabular}}
\end{table}""")
# ---- Table B: matched backbone ----
out.append(r"""\begin{table}[H]
\caption{Matched-backbone comparison with Recall@1, 5 and 10: SALAD, BoQ and CliqueMining retrained on DINOv3 under their published recipes, against our pipeline on the same backbone. All runs are ours.}
\label{tab:recallk-backbone}
\centering
{\scriptsize\setlength{\tabcolsep}{3pt}
\begin{tabular}{l ccc ccc ccc ccc}
\toprule
& \multicolumn{3}{c}{SALAD} & \multicolumn{3}{c}{BoQ} & \multicolumn{3}{c}{CliqueMining} & \multicolumn{3}{c}{Ours} \\
\cmidrule(lr){2-4}\cmidrule(lr){5-7}\cmidrule(lr){8-10}\cmidrule(lr){11-13}
Benchmark & R@1 & R@5 & R@10 & R@1 & R@5 & R@10 & R@1 & R@5 & R@10 & R@1 & R@5 & R@10 \\
\midrule
"""+group("Standard VPR benchmarks",13)+"\n"+"\n".join(row(d,[J["salad_v3"],J["boq_v3"],J["clique_v3"],J["ours_v3"]]) for d in STD)+"\n\\midrule\n"+group("Cross-environment VPR benchmarks",13)+"\n"+"\n".join(row(d,[J["salad_v3"],J["boq_v3"],J["clique_v3"],J["ours_v3"]]) for d in CROSS)+r"""
\bottomrule
\end{tabular}}
\end{table}""")
# ---- Table C: signals ----
S=J["signals"]; names=[("none","none (bare \\textsc{MaxSim})"),("selfw","+ self-similarity (ours)"),("cls_attn","+ class-token attention"),("centrality","+ patch-graph centrality"),("norm_a","+ token norm (a)"),("norm_b","+ token norm (b)"),("idf","+ inverse document frequency"),("cross_ref","+ cross-referencing"),("rapid_spatial","+ rapid spatial verification")]
rows=[]
for k,lab in names:
    rows.append(lab+" & "+" & ".join(" & ".join(f"{x:.1f}" for x in S[ds][k]) for ds in ("pitts30k","amstertime","nordland"))+r" \\")
out.append(r"""\begin{table}[H]
\caption{Patch importance signals with Recall@1, 5 and 10 (the Recall@1 columns are Table~\ref{tab:w-signal}).}
\label{tab:recallk-signal}
\centering
{\scriptsize\setlength{\tabcolsep}{3.5pt}
\begin{tabular}{l ccc ccc ccc}
\toprule
& \multicolumn{3}{c}{Pitts30k} & \multicolumn{3}{c}{AmsterTime} & \multicolumn{3}{c}{Nordland} \\
\cmidrule(lr){2-4}\cmidrule(lr){5-7}\cmidrule(lr){8-10}
Patch importance signal & R@1 & R@5 & R@10 & R@1 & R@5 & R@10 & R@1 & R@5 & R@10 \\
\midrule
"""+"\n".join(rows)+r"""
\bottomrule
\end{tabular}}
\end{table}""")
print("\n\n".join(out))
