---
title: "GFE2026 官方命令流案例 ch01 — 球铰支座静力/模态（CM1.py）"
type: command-stream-case
software: GFE
chapter: 1
version: v3.x
tags: [gfe, 命令流, case, 静力分析, 模态分析, occ几何]
sources: ["[[GFE2026-CM-ch01-CM1.src]]"]
created: 2026-06-11
updated: 2026-06-11
---

# 概览

官方 v3.x 命令流（907 行，GUI 录制风格），对应 [[GFE-Cases-01-球铰支座]]。单位 mm–N–t–MPa。调用链：occ 体素建模（make_sphere/make_cylinder/make_box/make_wedge）→ builder 布尔（cut/merge）+ 变换（translate/rotate/make_round_array）→ mesh_generator 划网格 → 材料/集合/截面 → 表面集 → 边界荷载 → 步/输出/工况 → inpio 导出 INP。详细路径见 `D:\GFE\GFE_KB\02_案例反推\路径_ch01_球铰支座.md`。

# 关键 idiom

- **几何改名双轨**：每次 rename 都要 `geo_mgr()` 与 `mesh_mgr()` 各做一次——几何与网格是平行 manager（见 [[命令流manager-CRUD]]、[[GFE对象引用关系]]）。
- **布尔产物固定名**：cut→`BoolCut-N`、merge→`Merge-N`、复制变换→`Trsf-<原名>-N`、阵列→`Array-N`，再 rename 收编；本章 merge 第二参 False（单材料先合并后赋属性合法；多材料须先赋 [[实体单元]] 截面再 merge）。
- **make_round_array(shapes, N, θ_rad, 基点, 轴)**：N 含原件，θ 弧度、正负即方向（实值 ±0.785398/±1.0472/±1.5708）；输入 shape 经 `gt.get_shape_by_id(三元组)` 获取。
- **程序化选面**：`geotool.children(shape,4)` 遍历面 + `centre_of_mass` 条件过滤（底面=z<minz+1e-5；受压面=质心距球心 400），替代 GUI 拾取。
- **集合两形态**：`gset_basic('名').set_shapes(children(shape,2))` 两步法，或 `gset_mgr().add('名', shape列表)` 直接重载（v2.15 实名 basic_set/gset）。
- **表面集 data 三元组**：`s.data=[[geo_obj.id(), 面id, 0]]`（0=面模式），manager 实名 `surf_mgr()`。
- **工况=映射属性赋值**：`c.bcs['Initial']=[...]; c.fieldReqs['STATIC']=[...]`，空步键也显式赋 `[]`——v3.x 可读字典，v2.15 只有 set_*（详见 [[命令流manager-CRUD]]）。
- **INP 导出命令流可达**：`inpio.writer(path); set_case('工况'); perform()`，每工况一份；存 .pre 与作业提交仍只能 GUI。

# 参数真值与坑

- 材料 Q345：ρ=7.8e-09、E=206000、ν=0.25（**官方 py 仲裁 7.8e-09**，dump v2.15 模型为 7.9e-09）。
- **自重仲裁**：本章惯性力 GRA（type=7）= `[0,0,-9800]`，mm 制物理正确；ch02 官方同制却写 -9.8，两章不一致是官方原始状态。
- MODAL `eigen=1`（dump 为 10）；STATIC nlgeom 行被注释（默认 False，dump 为 True）——官方 py 与发布 .pre 参数分叉，复刻须声明取哪个源。
- 网格 Algorithm=6/Algorithm3D=4、DefaultSize=10、auto_transfinite=True（复杂几何可能崩，参 [[质量缩放]] 无关本章静力）。
- BC 字段 `node_id=[]/is_node_set=True` 仅本章出现，ch02/ch03 不写也可。
- 头部 import/set_application_by_ui() 重复 9 次是录制残留。
