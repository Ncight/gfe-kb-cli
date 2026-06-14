---
title: "IPA — 整体简化抗震分析法 (Integrated Simplified Seismic Analysis for SIUS)"
type: concept
tags: [concept, SIUS, simplified-method, design]
created: 2026-06-02
updated: 2026-06-02
---

# IPA — 整体简化抗震分析法

[[Qiu2026R06]] 为 [[SIUS]] 提出的简化抗震分析法，用于替代计算量大的全时程分析(DTHA)。

## 核心思想
单独地上结构（pushover 惯性思路）或单独地下结构（反应位移/强迫位移思路）的简化法**都不能直接用于耦合的 SIUS**。IPA **同时计入**：
- 地上部分的**惯性振动**；
- 周围土对地下部分的**强迫位移**。

## 精度（对 DTHA）
地下与界面误差小（多 ≤10%），地上误差略大（~22–28%）；跨烈度、跨软/硬土均在可接受范围。可高效产出各区**性能曲线 + 五级状态阈值**（阈值见 [[Qiu2026R06]]）。

相关：[[SIUS]] · [[Qiu2026R06]]
