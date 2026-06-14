---
title: "GFE2026 官方命令流 — 第11章 高层带地下室抗震（弹性简化版）"
type: command-stream-case
software: GFE
chapter: 11
version: v3.x
tags: [gfe, command-stream, ssi, seismic, dynamic, basement]
sources: ["[[GFE2026-CM-ch11-CM11.src]]"]
created: 2026-06-11
updated: 2026-06-11
---

> GFE2026 官方第 11 章命令流 CM11.py（613 行）：带地下室高层的动力 [[土-结构相互作用|SSI]] 弹性时程。最大价值不在流程本身（与 ch10 同构），而在它与 v2.15 实测 dump 构成**同一案例的两个官方认可终态**——弹性教学版 vs 弹塑性完整版——把"哪些差异是版本、哪些是建模决策"切分清楚了。

## 调用链骨架

`import_yjk(43元，与 ch10 官方逐位相同)` → **手写 4 个纯弹性土材料**（mat_mgr().add，density+elastic 两条目，无 gmat）→ `soil.soil('Soil1D-1', depth=[2,4,6,5], 砾石/粉土/黏土/砂土, bedrock='砂土')` → `box_builder(100×40)` + data_builder → `translate(['SuperStru','BasementBoundary'],[26,14,17])`（**移结构入土**，与 ch10 移土相反，两式皆官方实跑）→ `cut` → 质心精确比对筛边界面（`==` 简化版，仅适用规则箱体）→ Surface-1 → `art_bc(structure='Soil-1')` → `dynamic_explicit_step('Dyna-1', period=20, nlgeom=True, target_time=5e-5)` → 三组合搜索接触 + 16 对 Tie（CP-geo1-geo2-N-master/slave 命名）→ 幅值 '25_RH1TG025_(RenGong_T_025)_x_Zhu' → `vibra_load('VibLoad-1', amp_bottom_y)` → case 字典挂载（Initial 挂 12 条 Comb_M 附加质量）→ 网格（Algorithm 8/3D 1、Recombine2D=True、size 2，先结构后土）→ `inpio.writer('Case-1')`。

## 三态对照（弹性官方 py / 弹塑性 dump / 手册 GUI）

| 维度 | 官方 v3.x py | dump v2.15 实况 | 手册 GUI |
|---|---|---|---|
| 土材料 | 手写 4 层纯弹性（无阻尼无 MC） | gmat 8 层 elastic+[[摩尔-库仑|MC]]+Rayleigh α(β=0) | gmat 导入后转 [[Davidenkov本构|Davidenkov]] |
| 土剖面/土域 | 4 层 / 100×40 | 7 层 / 260×260 | 同 dump |
| 地震波 | RH1TG025 人工波挂 **y** 向（幅值名带 `_x_` 名实不一致，官方原文如此） | 自建波挂 x 向 | 预设波 y 向 |
| 工况 | Initial→Dyna-1（无重力无静力步） | Initial→StaticStep→DynamicStep 三段式 | 同 dump |
| artbc.structure | **'Soil-1'** | **'SuperStru'** | 形心拾取 |
| 动力步 | period 20 / nlgeom=True / 5e-5 | period 40 / nlgeom=False / 2e-4 | — |

仲裁结论：`art_bc.structure` 在四处实证里两值混用（ch10/ch15 官方=SuperStru，ch11 官方=Soil-1，ch11 dump=SuperStru）——它只是[[粘弹性人工边界]]的形心参考几何，**无统一规则、非正确性关键**。弹塑性增量（AllGrav 双挂、compute_era、convert_material/convert_reinforce）官方版本以 ch10 弹塑性 py 为真值源，本章 dump 与其同构互证。

## 经验要点

- nlgeom=True 是三章官方 py 中唯一开几何非线性的案例；[[质量缩放]] target_time 仍 5e-5、β=0 铁律不变。
- 官方把网格划分放在工况定义之后——建模顺序自由、INP 在导出时统一刷新的直接证据。
- 工况引用的 'FO-DynaEla-All' 在 py 内未创建（GUI 预设遗留），裸重放须先建。
- "批量搜全组合再按 tie_list 索引挑"是官方第二种 Tie 装配 idiom（ch10 为逐对式）。
- [[地震场地反应]] vibra_load 的 14 个 set_parameter 键集与 ch10 完全一致，可当模板固化。
