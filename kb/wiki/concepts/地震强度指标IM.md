---
title: "地震强度指标 IM (Intensity Measure)"
type: concept
tags: [concept, intensity-measure, fragility, seismic-demand]
created: 2026-06-02
updated: 2026-06-02
---

# 地震强度指标 IM (Intensity Measure)

表征地震动破坏能力、降低结构地震响应不确定性的**标量**：如 PGA、PGV、PGD、RMS 速度、谱加速度 Sa(T₁)、Fajfar 指数等。**最优 IM** 应与结构地震响应高相关（回归离散度小），且与结构动力特性密切相关——故同一 IM 对不同结构未必都最优。

## 在本库中的位置
[[Li2023R07]] 指出 [[地上-地下耦合结构]] 的难题：地上(惯性主导)与地下(土变形主导)动力特性不同，**单一 IM 难同时激发两者最不利响应**。为此提出**稳定性准则**——评估结构进入塑性阶段后地震响应离散度的变化——筛选最优 IM；结论 **PGV、RMS 速度、Fajfar 指数**为 AUCS 整体损伤评估最优（PGA 对此类结构并非最优）。

相关：[[Li2023R07]] · [[地上-地下耦合结构]]
