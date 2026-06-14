---
title: "Real-ESSI 求解器"
type: entity
tags: [entity, software]
created: 2026-06-04
updated: 2026-06-04
---
# Real-ESSI 求解器
专用于地震-土-结构相互作用的高保真三维有限元求解器（Realistic Modeling and Simulation of Earthquakes, Soils, Structures），由 UC Davis（Boris Jeremić 等）开发，内置弹塑性土本构、零长度软接触单元、域缩减法（DRM）波动输入与并行计算，面向核电厂等关键设施的非线性 SSI/SSSI 分析。

## 本库收录 / 关联
- [[Kanellopoulos2024R31]] —— 用 Real-ESSI（配 Gmsh 建网格、ParaView 后处理、ETH Euler HPC 并行）对理想化核电厂建模，经 DRM 输入逐级加入非线性土与软接触单元，揭示反应堆楼-辅助楼的 SSSI 有害/有益耦合。

相关：[[SSSI 结构-土-结构相互作用]] [[域缩减法DRM]] [[Armstrong-Frederick 非线性随动硬化]] [[GFE]]
