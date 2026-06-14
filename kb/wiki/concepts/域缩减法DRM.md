---
title: "域缩减法DRM — Domain Reduction Method"
type: concept
tags: [concept, 边界, 波动输入]
created: 2026-06-04
updated: 2026-06-04
---
# 域缩减法DRM
Domain Reduction Method（Bielak 等）：两步法把大尺度震源区域波场转换为缩减域边界一层节点上的等效有效力，从而在局域非线性模型中复现三维地震波，避免对整个震源到场地区域做精细计算。

## 在本库中的位置
- [[Kanellopoulos2024R31]] — 在 Real-ESSI 核电厂 SSSI 分析中用 DRM 输入竖直传播 SV 波：先在分层半空间一维波传播解析求 DRM 等效力，再施加到 DRM 节点；缩减域外围加阻尼单元吸收外辐射波，一维土柱验证可复现地表目标谱至 30 Hz。

## 相关
相关：[[等效节点力法]] · [[粘弹性人工边界]]
