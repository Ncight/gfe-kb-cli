---
title: "面内撑力 strutting force — 墙位移不协调致楼板/连梁内的面内轴向恢复力"
type: concept
tags: [concept, strutting-force, compatibility-force]
created: 2026-06-04
updated: 2026-06-04
---

# 面内撑力 strutting force

连接两墙的楼板/连梁因两墙位移不协调（δ_INT < δ_EXT）而产生的面内轴向恢复力（内力，不参与整体侧力平衡），集中于界面上下数层、远离界面后归零，有闭式解。

## 在本库中的位置
- [[Yacoubian2017R26]]：解析篇，单层撑力 f_b,k=(δ_INT−δ_EXT)·K_b·[(K_W−2K_b)/K_W]，沿高累加得总撑力 F_b（式8），案例楼连接板最大撑力 Set I=659 kN、Set II=582 kN，沿高近似线性。
- [[Yacoubian2017R14]]：数值篇，把这一 strutting/compatibility force 作为内墙剪力集中的成因；主反撑隔板归一化面内力峰值仅 0.12，不足以使隔板先于墙破坏。

## 相关
相关：[[楼板隔板]] · [[剪力墙剪力重分布]]
