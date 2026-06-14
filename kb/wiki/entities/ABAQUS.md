---
title: "ABAQUS — 通用有限元软件（GFE 手册匿名对标对象「软件A」，社区共识推断）"
type: entity
entity_type: 软件
tags: [software, fea, benchmark]
created: 2026-06-04
updated: 2026-06-04
---
> 国际通用大型有限元软件。GFE 各技术手册中的匿名对标对象「软件 A」，**社区共识推断**为 ABAQUS——手册全程未点名（另有软件 S、软件 Z=PLAXIS 类同为匿名对标），此处属推断而非手册事实。

## 定义
GFE 的 INP 关键字、单元命名（C3D*/S*/B*）、连接器（CONN3D2，历程输出 SE-SF）、显式动力体系均与 ABAQUS 对齐（为其子集）；[[GFE求解器内核]] 显式（GFEXG/GFEXC）与隐式（GFEXN）逐项与之对账：单元/本构级验证差异多在 3% 内，整体模型级（重力场位移、模态、接触反力）差异可达 3–10%，手册自身亦有正文与表格口径不一处。GFE 写出的 inp 可经 Vuel/vload 子程序在 ABAQUS 计算（[[GFE-FAQ]] 有流程，但单元/约束有兼容差异；勾选「写出 Vuel」的 inp 仅 ABAQUS 可算，GFE 本身无法计算）。

## 性能对标（手册匿名口径「软件A」）
- 161 万节点（494 万单元）SSI 显式一体化模型，同稳定步长 5e-5 s：GFE 8h31m32s vs 软件A 64h33m30s（快约 7.6 倍）。
- GFE-SSA E2 等效线性化用时约为软件A 的 1/8。
- GPU 优势边界：≥30 万节点才成立；2 万节点小模型 GFE GPU 反而比软件A CPU 慢。
- 注意：性能对比的硬件/系统基准不一致（i7-11700F vs R5 3600、Win10 vs Ubuntu），跨表推算加速比会失真。

## 在本库中的位置
- [[GFE-Implicit]]、[[GFE-Explicit]]、[[GFE-FAQ]]、[[GFE-UserGuide]]

相关：[[GFE]] [[GFE求解器内核]]

