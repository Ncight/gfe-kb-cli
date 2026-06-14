---
title: "HSS本构 — Hardening Soil with Small-strain stiffness"
type: concept
tags: [concept, gfe, 本构]
created: 2026-06-04
updated: 2026-06-04
---
> 硬化土小应变本构（HSS），在硬化土基础上加入小应变刚度，含 G0ref/γ0.7/m/pref 等参数，基坑工程常用。

## 定义
继承摩尔库伦强度，非线性弹性段刚度随应变衰减。INP 层 HSS 为 *User Material 标识位 3，**前置必须有 *Mohr Coulomb** 提供塑性部分（手册加粗警告）；⚠ φ/ψ 以弧度输入（手册示例 3.14×40/180，直接填角度差约 57 倍）；仅三维实体单元可用。GFE 实现见 [[GFE-Explicit]]/[[GFE-Implicit]]，参数口径见 [[GFE-UserGuide]]。属 [[本构模型]] 岩土族。

## 在本库中的位置
- [[GFE-Implicit]]、[[GFE-Explicit]]、[[GFE-UserGuide]]

相关：[[本构模型]] [[南水模型]] [[Drucker-Prager]]

