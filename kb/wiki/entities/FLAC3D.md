---
title: "FLAC3D"
type: entity
tags: [entity, software]
created: 2026-06-04
updated: 2026-06-04
---
# FLAC3D
三维显式有限差分岩土分析软件（Fast Lagrangian Analysis of Continua in 3 Dimensions），由美国 Itasca 公司开发，强项在大变形、连续介质塑性与时域非线性动力，内置滞回阻尼模型并提供 C++/FISH 自定义本构接口，常用于场地反应与直接法 SSI。

## 本库收录 / 关联
- [[Dai2024R34]] —— 用 C++ 把 [[Davidenkov]] + [[Masing法则]] 循环软化本构写入 FLAC3D 自定义接口，实现三维计算（含六面体拆四面体子区的体积加权处理）。
- [[Scarfone2020R10]] —— 用 FLAC3D 三维有限差分直接法（Mohr-Coulomb + 库内滞回模型）评估 20 层墙-框架高层动力 SSI，逐项剥离场地放大/运动/惯性相互作用。

相关：[[Davidenkov]] [[Masing法则]] [[显式动力分析]] [[直接法]] [[ABAQUS]]
