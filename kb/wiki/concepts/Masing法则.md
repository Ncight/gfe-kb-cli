---
title: "Masing 法则 (Masing Rule)"
type: concept
tags: [concept, soil, constitutive, dynamic, hysteresis]
created: 2026-06-02
updated: 2026-06-02
---

# Masing 法则 (Masing Rule)

等幅循环荷载下，由**骨架曲线**构造土体动应力-应变**滞回曲线**的规则（Masing 1926）：① 骨架曲线为基准（早期取双曲线）；② 初始加载沿骨架曲线；③ 初始反向卸载时动剪切模量 = 最大剪切模量 $G_{max}$；④ 加卸载应力-应变曲线与骨架曲线成**二倍关系**。

后续扩充：Rosenblueth (1964) 提"外大圈"法则约束再加荷走向，推广到非等幅荷载；Pyke (1979) 用 $n$ 倍法限制后继波滞回圈不超出骨架渐近线。

## 在本库中的位置
[[Davidenkov]] 模型即在 Masing 法则上构造滞回曲线与阻尼比。源 / 用法见 [[Chen2005R79]]（其骨架修正后，加卸载曲线遇上限剪应力 $\tau_{ult}$ 即沿水平线发展）。
- [[Dai2024R34]] — 等幅荷载用 Masing 二倍法、非等幅地震波用 n 倍法构造滞回，并以阻尼比调整系数纠正 Masing 阻尼失真。
- [[Ba2024R32]] — 采用非 Masing 不规则加卸载准则（只跟踪最近反转点+极值点），相比传统 Masing 大幅省存储。
- [[Zhao2024R21]] — Davidenkov+Masing+频域等效线性化路线用于大规模地上-地下 SSI 土本构。

相关：[[Davidenkov]] · [[Chen2005R79]] · [[阻尼比调整系数]]
