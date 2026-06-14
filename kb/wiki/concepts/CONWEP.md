---
title: "CONWEP — conventional weapons effects"
type: concept
tags: [concept, gfe, 荷载, 爆炸]
created: 2026-06-04
updated: 2026-06-04
---
> Conventional Weapons Effects Program 经验空气爆炸超压模型（Kingery-Bulmash 1984），GFE 冲击波荷载的底层算法。

## 定义
由起爆点/作用面/爆炸类型/TNT 当量算到达时间、最大入射/反射超压与衰减因子；无需建空气域，适用自由空气场/近距爆。⚠ 案例手册明文强制 t-m-kPa（吨-米-千帕）：经验公式量纲敏感，套错差数量级（Cases §14.3）；是否求解器级硬约定待关键字手册仲裁。配 [[显式动力分析]] 与单元失效（侵蚀）评估爆炸损伤——单元失效开关不在 GUI/INP，在求解器安装目录 Program\config.txt 的 IsRemoved_Co 系列（装机级全局设置，影响其后所有作业）。

## 在本库中的位置
- [[GFE-Explicit]]（第 6 章）
- 案例：[[GFE-Cases-14-爆炸]]

相关：[[显式动力分析]]

