---
title: "SPECFEM3D"
type: entity
tags: [entity, software]
created: 2026-06-04
updated: 2026-06-04
---
# SPECFEM3D
开源谱元法（SEM）三维波场模拟程序，由 Komatitsch、Tromp 等（Princeton / CNRS 等团队）开发，用 Legendre 基 + GLL 积分得对角质量阵、天然适配显式时间推进与 MPI 并行，广泛用于区域地震波传播与盆地效应的源到场地全过程模拟。

## 本库收录 / 关联
- [[Ba2024R32]] —— 在 SPECFEM3D Cartesian 中植入 [[Davidenkov]] 三参数本构 + 非 Masing 不规则加卸载子程序与自适应时间步，对云南施甸盆地 2001 年 Ms5.9 地震做三维非线性场地反应模拟（263.8 万单元，天河一号 400 核 14.5 h）。

相关：[[谱元法SEM]] [[显式动力分析]] [[Davidenkov]] [[沉积盆地]]
