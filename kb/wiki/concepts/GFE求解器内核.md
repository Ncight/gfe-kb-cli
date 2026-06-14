---
title: "GFE求解器内核 — GFE solver kernels"
type: concept
tags: [concept, gfe, 求解器]
created: 2026-06-04
updated: 2026-06-04
---
> GFE 的三个计算内核：GFEXN（隐式 CPU 并行）、GFEXC（显式 CPU）、GFEXG（显式多 GPU，厂商宣称比多 CPU 并行快 10 倍以上、未经案例验证，SSI 显式动力主力）。

## 定义
命令行经 `PrePo.exe -daemon -dat <inp路径> -gfedir <结果目录>` 提交 INP（-dat 是参数名，后接 INP 路径，不存在 .dat 输入文件）。批处理内核选择：缺省=GFEXG，`-cpu`=GFEXC，`-standard`=GFEXN；GFEXN 提交时会自动打开所有分析步几何非线性。GFEXN 逐项对标 ABAQUS 隐式（见 [[GFE-Implicit]]）；GFEXC/GFEXG 见 [[GFE-Explicit]]。[[显式动力分析]] 步长由 [[质量缩放]] 目标增量定。

## 在本库中的位置
- [[GFE-Implicit]]、[[GFE-Explicit]]
- 案例：[[GFE-Cases-04-核电站]]、[[GFE-Cases-13-反应位移法]]

相关：[[显式动力分析]] [[质量缩放]] [[PrePo]] [[ABAQUS]]

