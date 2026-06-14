---
title: "MIC — 最大信息系数 (Maximal Information Coefficient)"
type: concept
tags: [concept, statistics, correlation]
created: 2026-06-02
updated: 2026-06-02
---

# MIC — 最大信息系数 (Maximal Information Coefficient)

度量两变量间**关联强度**的统计量（Reshef et al., *Science* 2011），能同时捕捉**线性与非线性**关系，对大样本、非函数依赖也适用。基于互信息 (MI) + 网格自适应划分，归一到 [0, 1]：越接近 1 关联越强、越接近 0 越无关。

## 在本库中的位置
[[Qiu2023R03]] 用 MIC 计算一体化结构与单体结构地震响应**时程的波形相关性 (CC)**，作为 [[SAUIC]] 的非线性分量（CC 越小 → 相互作用越强）。

相关：[[SAUIC]] · [[Qiu2023R03]]
