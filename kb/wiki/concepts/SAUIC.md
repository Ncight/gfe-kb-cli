---
title: "SAUIC — 地上-地下相互作用系数 (Seismic Aboveground-Underground Interaction Coefficient)"
type: concept
tags: [concept, SIUS, aboveground-underground, metric]
sources: ["[[Qiu2023R03.src]]"]
created: 2026-06-02
updated: 2026-06-02
---

# SAUIC — 地上-地下相互作用系数

把"地上-地下相互作用([[SAUI]])"对[[SIUS]]地震响应的影响，**量化成一个带符号的数**。由 [[Qiu2023R03]] 提出。

## 定义
$$\text{SAUIC}=\begin{cases}\dfrac{\text{AC}}{\text{CC}}, & \text{AC}\ge 1\quad(\text{相互作用}\textbf{放大}响应)\\[2mm] -\dfrac{1}{\text{CC}\cdot\text{AC}}, & \text{AC}<1\quad(\text{相互作用}\textbf{削弱}响应)\end{cases}$$
- **量级** → 相互作用强度；**符号** → 放大(+) / 削弱(−)。

## 两个分量
- **AC 放大系数 (Amplification Coefficient)**：**线性模态频域**下，一体化结构(SIUS)的模态响应 / 单独结构(地上 or 地下)的模态响应之比。>1 放大、<1 削弱。管"幅值"。
- **CC 相关系数 (Correlation Coefficient)**：用 [[MIC 最大信息系数]] 衡量 SIUS 与单体**时程的非线性波形相关性**（0–1）。CC 越小 → 两者波形差异越大 → 相互作用越强。管"波形/变化规律"。

## 直觉
单纯比幅值(AC)只能在小震线弹性下成立；大震结构损伤、应力重分布后，幅值比变得模糊，于是再引入"波形相关性(CC)"补足。SAUIC = 幅值效应 × 波形效应，试图一个数同时刻画"放大多少 + 改变多少"。

## 局限（本库判断）
- AC 来自**线性**模态、CC 来自**非线性** MIC，二者硬乘，**物理意义/量纲是混合的**——属**工程诊断指标**，非严格物理量。
- 需要额外跑"单独地上/地下结构"对照模型 + MIC 程序(Matlab)才能算。

相关：[[SIUS]] · [[SAUI]] · [[Qiu2023R03]] · [[MIC 最大信息系数]]
