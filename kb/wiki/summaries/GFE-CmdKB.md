---
title: "GFE-CmdKB — GFE 命令流知识库（反编译 API + 案例反推 + 实时桥）"
type: manual
software: GFE
tags: [gfe, manual, 命令流, api, automation]
sources: ["[[GFE-CmdKB-INDEX.src]]"]
publisher: 反编译/实测（gfe-command-stream skill）
created: 2026-06-04
updated: 2026-06-04
---

> GFE「命令流」= PrePo 内嵌 CPython 的 **pybind11 API（非 Tcl）**。本页是 `D:\GFE\GFE_KB` 的编译入口：把命令流的**文法（怎么写）+ 案例反推（怎么用 / 建了什么）+ 实时桥（让 Claude 无人值守驱动 PrePo）**整理成可检索结构。与官方 [[GFE-Cmd]]（命令流手册）互补——手册讲文档化命令，本库补全反编译出的 787 函数全签名 + 隐藏命令 + 真实工程反推。注意版本口径：库内 manual_text.txt / GFE_manual_diff.md 基于 v2025（2.15.2，191 页）手册；现行 PDF 为 v2026（3.4.0），draft 草图器等原"隐藏命令"已在 v2026 文档化（第 4 章），manual_diff 结论引用前须按 v2026 复核。

## 三层定位
1. **某命令怎么写** → [[GFE-命令流API规格]]（787 函数全签名 / 32 模块 / [[命令流manager-CRUD]] 范式 / [[GFE对象引用关系]]）
2. **某流程怎么串 / 某案例怎么建** → [[GFE-命令流SSI骨架]]（15 章理解 + 动力 SSI 通用骨架 + 真实工程 400galW7-VC）
3. **让 Claude 实操 PrePo** → [[GFE-命令流桥与工具]]（实时桥 send.py + 反编译器 + 参数化建模）

## 关键事实速记
- 单位制随模型：m-t-kPa（E~kPa）或 mm-t-MPa；按 density/E 反推
- 阻尼 **β=0 恒定**（显式动力稳定，见 [[瑞利阻尼]] / [[显式动力分析]]）；本构 混凝土 user_type=1 / 土 user_type=2（[[Davidenkov]]）
- 动力步 dynamic_explicit + [[质量缩放]]（type=1, freq=100, target_time 地震 2e-4 / 列车 5e-5），modal_damping=None
- 地震输入 vibration.vibra_load(amp_bottom_x/y/z, is_outcrop, pwave_dir=2, soil)，即 [[地震场地反应]]；人工边界 artbc.art_bc(structure, surface)，即 [[粘弹性人工边界]]
- **限制**：命令流无 save API（.pre 存盘只能 GUI File→Save）；裸 python 不能 import GFE（须 PrePo 宿主）；几何只能名级感知

## 源文件（raw 检索层）
[[GFE-CmdKB-INDEX.src]] · [[GFE-CmdKB-APIref.src]] · [[GFE-CmdKB-APIspec.src]] · [[GFE-CmdKB-cppclasses.src]] · [[GFE-CmdKB-objref.src]] · [[GFE-CmdKB-manualdiff.src]] · [[GFE-CmdKB-cases.src]] · [[GFE-CmdKB-tools.src]] · [[GFE-CmdKB-400galVC.src]]

相关：[[GFE]] · [[GFE-Cmd]] · [[GFE-UserGuide]] · [[PrePo]]
