---
title: "基础输入运动FIM — 经运动相互作用修正后实际激励结构的运动"
type: concept
tags: [concept, ssi, kinematic, fim]
created: 2026-06-04
updated: 2026-06-04
---
# 基础输入运动FIM
Foundation input motion：自由场运动经运动相互作用（底板平均+埋深）修正后、实际激励结构的运动，定义为底板/结构无质量时底板的理论运动，通常**小于**自由场运动。

## 在本库中的位置
- [[fema-p-2091]] 把 FIM $u_{FIM}$ 与自由场 $u_g$ 并列为全库术语锚点，FIM = 自由场经基底板平均化×埋深效应叠乘修正。
- [[nistgcr12-917-21]] 用传递函数 $H_u(\omega)$=FIM/自由场傅里叶幅值比定义 FIM，反应谱比 $RRS\approx H_u(f)$。
- [[ASCE-7-22]] §19.4 经 $RRS_{bsa}\times RRS_e$（下限 0.7）由自由场谱得到 FIM 修正谱，仅许非线性时程使用。

## 相关
相关：[[运动相互作用]] · [[基底板平均化]] · [[基础埋深效应]]
