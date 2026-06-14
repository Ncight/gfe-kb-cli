---
title: "Davidenkov 模型 — 土体动力本构（骨架曲线）"
type: concept
tags: [concept, soil, constitutive, dynamic]
created: 2026-06-02
updated: 2026-06-02
---

# Davidenkov 模型 — 土体动力本构骨架曲线

描述土体在循环/地震荷载下的**剪应力-剪应变骨架曲线**，及其衍生的**模量衰减 G/Gmax(γ) 与阻尼比 ζ(γ)**。属 Hardin-Drnevich 类双曲线的改进，能较好拟合土的模量衰减与阻尼随剪应变增大的变化。

骨架形式：$\tau = G_0\,\gamma\,[1 - H(\gamma)]$，其中 $H(\gamma)=\{(\gamma/\gamma_0)^{2B}/[1+(\gamma/\gamma_0)]^{2B}\}^{A}$ 为含三参数 (A, B, γ₀) 的形状函数。滞回曲线按 [[Masing法则]] 二倍放大构造。陈国兴-庄海洋（见 [[Chen2005R79]]）给出常用参数化形式，并以破坏剪应变上限 $\gamma_{ult}$ 分段修正（$\gamma>\gamma_{ult}$ 时骨架取水平线 $\tau_{ult}$）以避免应力无限增长。参数角色：**B 主控阻尼比 $D\text{-}\gamma$ 曲线，γ₀ 主控模量衰减 $G/G_{max}\text{-}\gamma$ 曲线**。广泛用于一维场地地震反应与土-结构动力有限元。

## 在本库中的位置
- 源/参数：[[Chen2005R79]]（修正骨架 + 阻尼比公式 + 南京地区各类土参数）；谱元法实现见 [[Ba2024R32]]。
- 滞回构造规则：[[Masing法则]]。
- 局限延伸：[[Chen2005R79]] 不计软化（仅水平截断）→ [[Dai2024R34]] 引入循环应变软化补足。
- 对比 [[Drucker-Prager]]：Davidenkov 更精细刻画土的**循环非线性**（模量衰减 + 阻尼随应变）；而 [[邱大鹏]] 系列（[[Qiu2023R03]] 等）用的是 Drucker-Prager + 等效线性阻尼，属较简化处理。
- [[Ba2024R32]] — 把 Davidenkov 三参数骨架+非 Masing 准则移植进谱元法 SPECFEM3D 做盆地非线性模拟。
- [[Dai2024R34]] — 在 Davidenkov 骨架上叠加循环软化与阻尼比调整系数，写入 FLAC3D 自定义本构。
- [[Zhao2024R21]] — 13 层土用 Davidenkov 本构+频域等效线性化，作大规模地上-地下 SSI 的土材料。

相关：[[Drucker-Prager]] · [[Chen2005R79]] · [[Masing法则]] · [[Ba2024R32]] · [[Dai2024R34]] · [[Zhao2024R21]] · [[DCZ本构模型]]
