---
title: "GFE2026 官方命令流案例 ch05 — 非均匀场地建模（钻孔数据驱动）"
type: command-stream-case
chapter: 5
version: v3.x
software: GFE
tags: [gfe, command-stream, non-uniform-soil, borehole, ssi, seismic, eera]
sources: ["[[GFE2026-CM-ch05-CM5-update2.src]]"]
created: 2026-06-11
---

# GFE2026 官方命令流 ch05：非均匀场地建模（CM5-update2.py，1968 行）

官方 v3.x 命令流案例：与 ch04 同一核电站结构，但场地改为**钻孔数据驱动的非均匀土体**（`build_non_uniform_soil`），并扩展为模态+静力（地应力）+显式动力三工况、一次导三 INP。单位 m–t–kPa。结构建模段与 [[GFE2026-CM-ch04]] 逐行同源（官方整段复用重跑，非 open_pre 合并）。

## 调用链概览（差异段）

1. **钻孔数据进料**：`SoilSamples.txt` 2401 行（49×49 网格、间距 6m），每行 tab 分隔 7 列 = `x, y + 5 个层界面 z 值`（地表 0 起向下取负，如 `0 6 0 -7 -18 -26 -62`，5 界面=4 层）。逐行 float 解析 → `GFE.geometry.geotool.SoilSample(x=row[0], y=row[1], depth=row[2:])`。
2. **[[非均匀土体|build_non_uniform_soil]]**：`GFE.geometry.geotool.build_non_uniform_soil(dim=0, materials=[...], samples=soil_samples)`（dim=0 即 3D Delaunay）。自动建几何 **'NU-Soil-1'**（上表面恒 z=0）+ 逐层集合 + 实体截面。
3. **对位裁剪**：利用"上表面恒 z=0"，`center1=[形心x, 形心y, 0]` → `translate(['NU-Soil-1'], 差向量, False)` → `cut('NU-Soil-1', ['plant-basement'], True)`。
4. **边界面收集**（与 ch04 包围盒法不同）：遍历 `geotool.children(shape,4)` 按面形心 ±0.1 容差追踪运行极值，分组 Set-base/Set-x/Set-y（gset 兼作 BC 集合）；表面集落地用 `geotool.get_id_by_shape(f)` → `data=[[geoid, fid[-1], 0]]`，且 **`to_node_surface=False`**。
5. **BC 四件**（模态/静力工况用）：BC-base `type=0 全约束`；BC-x/BC-y `type=1, valid_dof=1/2`（法向约束=位移型勾单自由度）；重力 'GRA' `type=7, value=[0.0,0.0,-9.8]`（三元）。
6. **[[一维土层]]（仅供场地反应）**：`depth=[7,11,8,36]; materials=[sutiantu→qiangfenghua]（自上而下）; bedrock_mat='qiangfenghuahuagangyan'`。
7. **[[地震场地反应]]**：KOBE 波 2901 点硬编码 → `vibra_load()` + 14 个 `set_parameter`（同 ch04 全表，UseEERAMat='true' 自动派生 `<mat>-EERA` 逐层 `*Damping Alpha`）。[[粘弹性人工边界]] `art_bc(structure='plant', surface='soil-around')`。
8. **三步三工况**：`frequency_step(eigen=10)`、`static_general_step(init_inc=0.1, period=1.0, min_inc=1e-5, max_inc=0.1)`、`dynamic_explicit_step(period=20.0)` + [[质量缩放]] `target_time=3e-05`。工况映射赋值：model 工况 `bcs['Initial']=['BC-base','BC-x','BC-y']`；static 加 `bcs['Static-1']=['GRA']`；dyna 不挂 BC、只挂 vload+artbc+fieldReqs 三件套。`inpio.writer` 对 'static'/'model'/'dyna' 各 perform 一次。

## 关键经验

- **材料顺序双序并存（最易踩坑）**：`build_non_uniform_soil` 的 materials = **自底向上**（`['qiangfenghua','quanfenghua','lizhi','sutiantu']`，materials[0]→最深层），而同文件[[一维土层]]的 materials = **自上而下**（sutiantu 在前）。SoilSample.depth 界面 z 列表自上而下（0 → -62）。三者方向官方同文件铁证，跨 API 勿混。
- **官方无调幅**：CM5 没有 `compute_era` 调用，KOBE 波原始幅值直接输入；调幅是手册 GUI 流程（命令流等效见 ch10 `compute_era(2.2,5,0.01,1,'VibLoad')`，a_layer 0=基岩/1=露头/2=地表）。
- **土层 α 逐层赋值**：同 ch04，由 EERA（UseEERAMat）在 INP 导出时自动生成，命令流不手写；自检即查 INP 中 `<名>-EERA` 材料是否带 `*Damping Alpha`。
- 静力→动力的 -prevdb 地应力链在作业层（GUI/求解器），命令流只负责分别导 INP。
- ⚠ v2.15 代差：`build_non_uniform_soil`、`compute_era`、工况映射赋值均不存在（2026-06-10 实测）——非均匀土在 v2.15 是硬断点。

相关：[[GFE2026-CM-ch04]]、[[土-结构相互作用]]、[[显式动力分析]]、[[地震场地反应]]
