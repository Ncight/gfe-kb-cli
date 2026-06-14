---
title: "SPH光滑粒子流体动力学 — smoothed particle hydrodynamics"
type: concept
tags: [concept, gfe, 流体]
created: 2026-06-04
updated: 2026-06-04
---
> smoothed particle hydrodynamics，无网格粒子法，GFE「流体动力」模块用其模拟自由液面流固耦合（晃荡、落水），独立于 GFE 有限元求解器的外部 SPH 引擎路线（DualSPHysics）。

## 定义
把几何登记为流体/固体/浮体粒子对象，配流体动力分析步（GUI 中挂在「线性摄动」程序族；设内部粒子距离、参考密度、[[状态方程]] 多方常数、声音系数），写 SPH xml 经批处理（可 GPU）求解，VTK 粒子文件后处理。⚠ SPH 强制 SI(m) 单位制，材料参数不得沿用其他单位制模型。FEM（耦合固体域）网格尺寸须为粒子间距 5-10 倍；中空几何填充须选「面」（选「全部」会填实）。

## 在本库中的位置
- 案例：[[GFE-Cases-08-SPH小球落水]]、[[GFE-Cases-09-SPH水桶晃动]]

相关：[[显式动力分析]] [[流固耦合]]

