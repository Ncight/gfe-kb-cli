---
title: "Drucker-Prager 模型 — 土体弹塑性本构"
type: concept
tags: [concept, soil, constitutive, plasticity]
created: 2026-06-02
updated: 2026-06-02
---

# Drucker-Prager 模型 — 土体弹塑性本构

压力相关的弹塑性屈服准则（Mohr-Coulomb 的光滑近似），适合摩擦型材料（砂土、岩石类），允许塑性体积变化与各向同性硬化/软化。ABAQUS 等通用 FEA 内置，建模简便、适用性广。

## 在本库中的位置
[[邱大鹏]] 系列（[[Qiu2023R03]]、[[Qiu2024R04]]、[[Qiu2025R05]]）用它 + EERA 等效线性阻尼模拟土体。相对 [[Davidenkov]] 类骨架本构，对土的循环模量衰减/阻尼随应变变化刻画较简化——是工程上常见、可接受的折中。

相关：[[Davidenkov]] · [[Qiu2023R03]]
