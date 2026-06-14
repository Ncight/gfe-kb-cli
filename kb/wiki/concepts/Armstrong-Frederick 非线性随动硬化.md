---
title: "Armstrong-Frederick 非线性随动硬化 — Armstrong-Frederick nonlinear kinematic hardening"
type: concept
tags: [concept, 本构, 塑性]
created: 2026-06-04
updated: 2026-06-04
---
# Armstrong-Frederick 非线性随动硬化
描述多轴循环加载下 Bauschinger 效应的非线性随动硬化本构规律，背应力含线性强化项与回复（动态恢复）项，常配 von Mises 屈服准则使用。

## 在本库中的位置
- [[Kanellopoulos2024R31]]：核电厂土的弹塑性本构取 von Mises 屈服 + Armstrong-Frederick 随动硬化 + 关联流动（压力无关），用参数 R、$h_a$、$c_r$ 把 $h_a/c_r$ 标定到目标不排水抗剪强度 $S_u$；同一规律也用于软接触单元切向，使摩擦系数渐增到残余值。本文走 von Mises+AF 路线，可与本库 [[Davidenkov]]/[[Masing法则]] 滞回路线对照。

## 相关
相关：[[本构模型]] · [[非线性接触]]
