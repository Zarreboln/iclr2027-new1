# Figure 1（teaser）修改提案 · 2026-09-24

源文件：`~/Desktop/teaser/teaser_zhiyao_final.pptx` → PowerPoint 导出 `figures/teaser_v4.pdf`。
下面每条都写成「现状 → 拟改」，标 ★ 的需要你拍板，其余我按提案直接改。

---

## 0. 先说两处硬伤（数据）

**0.1 散点图 y 轴刻度标错了一格。**
按 MegaLoc(45.6)、BoQ(29.5) 两点反推，网格线间距 10 个点没错，但刻度数字整体贴低了一条线：写着 80 的那条线实际是 70，写着 10 的那条实际是 0。直接后果是读者读出来的所有 VP-Air 数都比真值高 10。★ 这个必须改，无争议，只是提醒你现版有这个问题。

**0.2 若干点的数值与主表不一致。**

| 点 | 图中 (Tokyo, VP-Air) | 主表 Table 3/4 | 处理 |
|---|---|---|---|
| Ours | (98.4, 82.7) | (98.4, **77.6**) v3 | 改成 77.6 |
| AnyLoc | (87.6, 66.7) | (**82.9**, 66.7) | 改 82.9，x 轴下限要放到 82 |
| CricaVPR | (90.2, 19.9) | (90.2, 19.9) | 一致 |
| Pair-VPR | (100, ~12) | 主表没有这个方法 | ★ 删掉，或补进 Table 4 |
| SelaVPR++ | (98.1, 37.3) | 主表只有 SelaVPR (94.0, 32.6) | ★ 换成 SelaVPR，或补 SelaVPR++ 进表 |
| SFRS / CosPlace / R2Former / EigenPlaces / SALAD / CliqueMining / MegaLoc / SAGE / BoQ | — | 一致 | 不动 |

原则：Figure 1 里出现的每个点都要能在主表里查到同一个数。

**0.3 气泡面积 = 有标注训练图像数。**
CosPlace / EigenPlaces 用 41.2M，MegaLoc / SelaVPR++ 45M，SAGE 1.8M，R2Former 1.2M，BoQ / SALAD / CliqueMining / CricaVPR 0.53M (GSV-Cities)，SFRS 0.2M。这些数正文 §1 有出处（GSV-Cities 约 50 万、SF-XL 4100 万）。图例只标了 1M 和 5M 两档，41M 的气泡没有参照 → 图例加一档 **40 million**，或把三档改成 0.5M / 5M / 40M。

---

## 1. 术语逐项对齐（图内文字）

全文口径：两组 benchmark 叫 **standard** 和 **cross-environment**（正文 29 处，`in-domain`/`out-of-distribution` 0 处）；训练开销正文写的是 training。所以图里所有 ID / OOD / in-domain / out-of-distribution / supervision 都换掉。

### 1.1 上排三格

| 位置 | 现状 | 拟改 | 理由 |
|---|---|---|---|
| 格 1 标题 | Trained | Trained | 不动 |
| 格 1 副题 | Place labels decide what counts | Place labels decide what counts | 不动，与 §1 "learns a representation from place labels" 一致 |
| 格 1 左图注 | Large labelled training set | Labelled training set | 去掉 large，气泡已经表达规模 |
| 格 1 右图注 | Corpus-specialized features | Features tied to the training corpus | corpus-specialized 正文没有；§1 原话是 "inherit the imagery that corpus contains" |
| 格 2 标题 | Training-free, prior work | Training-free, prior work | 不动 |
| 格 2 副题 | Added criteria decide what counts | An external criterion decides what counts | §1 原话 "a criterion fixed elsewhere" |
| 格 2 三小图 | Codebook / Segmentation / CLS attention | Codebook / Segmenter / CLS attention | 与 §1 "a segmenter's notion of an object" 对齐 |
| 格 2 底注 | Prior-selected / aggregated features | Features selected by that criterion | 去掉斜杠并列，一句话 |
| 格 3 标题 | Ours | Ours | 不动 |
| 格 3 副题 | Let patches decide what counts | The patches themselves decide what counts | 与前两格句式平行（主语 + decide） |
| 格 3 两小图 | Within-image / Across-image | Self-similarity → weights / Cross-similarity → ranking | 对应 §3 的 P2PS-1 与 P2PS-2/3；§1 原话 "two tables of patch similarity" |
| 格 3 底注 | Balanced, matchable patch evidence | Weighted patch-to-patch similarity | balanced / evidence 正文都没有 |
| 箭头 | train | train | 不动 |

### 1.2 底排 ID / OOD 两行 → 重做（见 §2）

### 1.3 散点图

| 现状 | 拟改 |
|---|---|
| Supervision cost vs. OOD recall | **Training cost vs. cross-environment recall** |
| VP-Air R@1 (out-of-distribution, %) | VP-Air R@1 (cross-environment, %) |
| Tokyo 24/7 R@1 (in-domain, %) | Tokyo 24/7 R@1 (standard, %) |
| 图例 ours (training-free) / training-free / trained / 1 million images / 5 million images | ours / training-free / trained / **labelled training images:** 0.5M · 5M · 40M |
| EigenPl / CliqueM | EigenPlaces / CliqueMining（与表格同名；空间不够就用表格里的缩写 EigenPl. 加点） |

### 1.4 雷达图

| 现状 | 拟改 |
|---|---|
| Recall across 14 benchmarks | **Recall@1 on all 17 benchmarks** ★ 补 Pitts250k、St Lucia、Oxford 三轴；Ours / MegaLoc / AnyLoc 三条线 17 个数附录全表都有 |
| in-domain / out-of-distribution 两段弧标 | standard / cross-environment |
| Amster / Baidu Mall / Gardens Pt | AmsterTime / Baidu / Gardens Point（与 Table 1 同名） |
| 图例 Ours / MegaLoc / AnyLoc | 不动 |

### 1.5 Caption

现：`\textbf{Three ways of deciding what an image contributes.} Top: … place-labelled supervision, additional aggregation or selection criteria, or patch-to-patch similarities. Bottom: Tokyo 24/7 versus VP-Air R@1, with marker area indicating the number of labelled training images. Right: R@1 on 14 of the 17 benchmarks.`

拟：`Three ways of deciding what an image contributes. Top: features shaped by place labels, by an external criterion, or by the patches themselves. Bottom left: Tokyo 24/7 (standard) against VP-Air (cross-environment) Recall@1; marker area is the number of labelled training images. Bottom right: Recall@1 on all 17 benchmarks.`

去粗（其余所有 caption 都不加粗，只剩 Fig 1 和刚改掉的 Fig 2 是孤例）；三格的三个主语与图内副题一一对应。

### 1.6 正文联动（§1 第四段）

- "the scatter plot below … every trained method sits high on the street-level axis and low on the aerial one, while the marker area records the millions of labels it consumed" → labels 改成 labelled training images，与图例一致。
- "The first cell of the top row depicts the supervised recipe" 等三处 "cell" 用法可保留。

---

## 2. 底行两行（原 ID / OOD）重做

### 2.1 结构
每格底部两行，行首不再是 ID / OOD，改成两组 benchmark 的名字，行尾一个表情：

```
Standard         <一句>          🙂
Cross-env.       <一句>          🙁
```

表情用两个小圆脸（矢量画，不用 emoji 字体，PowerPoint 导出稳定），绿脸 = 强，红脸 = 弱，灰脸 = 说不上强弱。三格的六张脸一眼把结论摆出来：Trained 🙂🙁，Prior 😐🙁，Ours 🙂🙂。

### 2.2 文字候选 ★ 选一套，或混搭

**方案 A（定性，最短）**

| 格 | Standard | Cross-environment |
|---|---|---|
| Trained | Strong where the labels come from 🙂 | Drops with the imagery 🙁 |
| Prior TF | Criterion not tuned to places 😐 | Criterion may not transfer 🙁 |
| Ours | Distinctive patches matched 🙂 | Same rule, no retuning 🙂 |

**方案 B（带主表均值，最硬）**

| 格 | Standard | Cross-environment |
|---|---|---|
| Trained | mean 93.0 (best, SAGE) 🙂 | mean 65.1 (best, MegaLoc) 🙁 |
| Prior TF | mean 80.3 (best, EffoVPR-ZS) 😐 | mean 69.5 (best, AnyLoc) 🙁 |
| Ours | mean 93.3 🙂 | mean 76.6 🙂 |

数字全部来自 Table 3/4 的 mean(8) / mean(9) 列。B 的好处是每个笑脸都有据，坏处是 Prior TF 那格 69.5 > 65.1 却给了红脸，需要解释；可以把 Prior 的 cross-env 也给灰脸。

**方案 C（A 的措辞 + B 的数字放括号）**

| 格 | Standard | Cross-environment |
|---|---|---|
| Trained | Strong where labels come from (93.0) 🙂 | Drops with the imagery (65.1) 🙁 |
| Prior TF | Criterion not tuned to places (80.3) 😐 | May not transfer (69.5) 😐 |
| Ours | On par with trained (93.3) 🙂 | Best by 11 points (76.6) 🙂 |

我倾向 C：一格一句话说机制，括号里的数把机制钉在表上。

---

## 3. 上排压扁

现状：上排框 y = 0.22 → 2.46 in（高 2.24），底排 2.62 → 7.42。上排内部五层：标题 0.29 / 副题 0.25 / 小图 0.60 / 图注两行 0.34 / ID-OOD 两行 0.34，层间空隙加起来约 0.42。

拟改（高 1.72，省 0.52 给底排）：
1. 标题和副题合并成一行："**Trained** · Place labels decide what counts"（标题保留颜色和粗体，副题正常字重），省 0.25。
2. 小图缩到 0.85 倍（0.60 → 0.51），图注并成一行放在小图正下方，省 0.20。
3. 两行结论行距 0.19 → 0.16，表情圆脸直径 0.13，省 0.06。
4. 层间空隙统一 0.05。

底排随之上移到 y = 2.10，高度 5.32：散点图纵向多出来的空间正好给 y 轴改成 0–90 的整刻度（现在 80 以上是空的）；雷达加三轴后需要的直径也够。

---

## 4. 实施顺序（拿到你的选择后一次做完）

1. 修 y 轴刻度错位 + 数据点（§0）。
2. 换所有术语（§1.1、1.3、1.4）。
3. 底行重做（§2 选定方案）。
4. 上排压扁、底排上移（§3）。
5. 雷达补到 17 轴（若 ★ 同意）。
6. 改 caption 与 §1 联动句；PowerPoint 导出 pdf（保 Comic Sans 内嵌）；上传 new3 / new2，贴 01_intro.tex。

需要你拍板的 ★：
- Pair-VPR、SelaVPR++ 删还是补进主表？
- 雷达 14 → 17？
- 底行文字选 A / B / C？
- 图例三档 0.5M / 5M / 40M 可以吗？
