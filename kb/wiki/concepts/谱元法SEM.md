---
title: "谱元法SEM — spectral element method"
type: concept
tags: [concept, 数值方法, 波场, 显式]
created: 2026-06-04
updated: 2026-06-04
---
# 谱元法SEM
结合有限元几何灵活性与谱方法收敛性的波场离散法：用 Legendre 高阶基函数配 GLL（Gauss-Lobatto-Legendre）配点，使质量矩阵对角化，天然适配显式时间推进且易并行（MPI 分区）。

## 在本库中的位置
- [[Ba2024R32]] — 在开源 SEM 程序 SPECFEM3D 中植入 [[Davidenkov]]+非 Masing 非线性子程序并提出自适应时间步加速，对冲积盆地做源到场地三维非线性模拟（施甸模型 263.8 万单元，400 核 14.5 h）。

## 相关
相关：[[沉积盆地]] · [[显式动力分析]] · [[等效节点力法]]
