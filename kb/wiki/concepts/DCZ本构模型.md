---
title: "DCZ本构模型 — Davidenkov-Chen-Zhao 非线性滞回本构"
type: concept
tags: [concept, soil, constitutive, dynamic]
created: 2026-06-04
updated: 2026-06-04
---
# DCZ本构模型
Davidenkov-Chen-Zhao 非线性滞回本构（赵丁凤等 2017）：以 [[Davidenkov]] 骨架曲线为初始加载路径，配 Non-Masing 不规则加卸载准则——滞回曲线转向后指向历史最值点再回归骨架，比经典 [[Masing法则]] 更贴合不规则加卸载试验。小应变下另引入 λ₀=1.5%~5.0% 阻尼补足材料与散射阻尼。

## 在本库中的位置
- [[Wang2021R80]] — 用作其一维场地 [[有效应力分析法]] 的土骨架本构：与剪切-体应变耦合孔压模型联立后，瞬态剪切模量与参考剪应变随孔压衰退，VUMAT 实现于 ABAQUS/Explicit。

## 相关
相关：[[Davidenkov]] · [[Masing法则]] · [[有效应力分析法]] · [[本构模型]]
