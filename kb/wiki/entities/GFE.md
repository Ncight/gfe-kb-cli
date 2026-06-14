---
title: "GFE — 广州颖力高性能有限元分析软件"
type: entity
entity_type: software
tags: [gfe, software, fea, ssi, 岩土, 抗震]
publisher: 广州颖力科技
created: 2026-06-04
updated: 2026-06-14
---

> **GFE**（高性能有限元分析软件，广州颖力科技）是面向土木 / 岩土工程的有限元平台。前后处理一体程序称 **PrePo**（含前/后处理两套界面切换，亦是批处理求解提交入口），内置 GUI 与命令流（嵌入式 Python API）；后端求解器内核三套：**GFEXG**（GPU 显式，默认）、**GFEXC**（旧 CPU 显式）、**GFEXN**（隐式）；强项在土-结构相互作用（SSI）、地下结构抗震、减隔震设计与施工模拟。本库内 [[邱大鹏]]、[[李钢]]、[[李文婷]] 等 SSI / 抗震论文的数值模型多由其（或同类 ABAQUS-兼容 INP 流程）产出。

## 组成与子产品
- **PrePo（前后处理一体程序）** —— GUI 建模 + 命令流，含前/后处理两套界面，亦是批处理求解提交入口（`PrePo.exe -daemon -dat`，纯渗流分析必须经此提交）。GUI 全流程见 [[GFE-UserGuide]]；命令流 Python API 见 [[GFE-Cmd]]。
- **求解器内核** —— **GFEXG**（GPU 显式，批处理默认）/ **GFEXC**（旧 CPU 显式，参数 `-cpu`）/ **GFEXN**（隐式，参数 `-standard`，提交时会强制打开所有分析步的几何非线性）。注意批处理参数名与内核名的映射非直觉。
- **隐式求解器（GFEXN）** —— 单元 / 本构验证基准，见 [[GFE-Implicit]]。
- **显式求解器（GFEXG/GFEXC）** —— 动力 / 接触 / 特殊荷载主力，见 [[GFE-Explicit]]。
- **GFE-SSA** —— 地下结构动力分析专版（时程法 / 反应加速度法 / 反应位移法），见 [[GFE-SSA]]。
- **减隔震分析** —— 消能减震与隔震设计专题，见 [[GFE-Iso]]。
- **新用户 FAQ** —— 导入 / 建模 / 计算实操坑，见 [[GFE-FAQ]]。
- **案例库** —— 15 个工程算例，见 [[GFE-Cases]]。

## 性能边界
- GPU 显式提速仅在 ≥30 万节点模型成立：2 万节点小模型 GPU（200s）反比对标软件A CPU（89s）慢；30 万节点 26m25s vs 76m23s、87 万节点 1h2m vs 4h20m。
- 161 万节点（494 万单元）SSI 一体化模型同稳定步长（5e-5 s）下：GFE 8h31m32s vs 软件A（匿名对标）64h33m30s，快约 7.6 倍。

## 在本库中的位置（工具 ↔ 研究）
- GFE 是本库 SSI / 抗震研究的**数值实验平台**：[[SIUS]]、[[地上-地下耦合结构]]、[[ULSFS]] 等系统的建模与求解能力在各技术手册中有对应实现。
- 关键物理能力对接已有概念页：
  - 吸收边界 / 波动输入 → [[粘弹性人工边界]]（实现见 [[GFE-SSA]]、[[GFE-Explicit]]）
  - 土体动力本构 → [[Davidenkov]]、[[Drucker-Prager]]（材料模块见 [[GFE-UserGuide]]、求解器手册）
  - 简化抗震分析 → 反应位移法 / 反应加速度法（见 [[GFE-SSA]]），与论文侧 [[IPA简化抗震分析法]] 互为软件/方法两端。

## 手册地图
| 手册页 | 角色 | 源 |
|---|---|---|
| [[GFE-UserGuide]] | 前处理 GUI 全流程主参考（v2025） | [[GFE-UserGuide.src]] |
| [[GFE-UserGuide-2026附录]] | v3.4.3 作业管理器+5附录+版本史增量 | [[GFE-UserGuide-2026-附录.src]] |
| [[GFE-Cmd]] | 命令流 / Python API | [[GFE-Cmd.src]] |
| [[GFE-Implicit]] | 隐式求解器单元 / 本构验证 | [[GFE-Implicit.src]] |
| [[GFE-Explicit]] | 显式求解器 / 接触 / 特殊荷载 | [[GFE-Explicit.src]] |
| [[GFE-SSA]] | 地下结构动力分析专版 | [[GFE-SSA.src]] |
| [[GFE-Iso]] | 减隔震分析 | [[GFE-Iso.src]] |
| [[GFE-FAQ]] | 新用户常见问题 | [[GFE-FAQ.src]] |
| [[GFE-Cases]] | 工程案例库（15 例） | [[GFE-Cases.src]] |

相关：[[广州颖力科技]] · [[GFE-Cmd]]（命令流知识库索引）
