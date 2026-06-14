---
title: "GFE2026 官方命令流案例 ch03 — 华夫板框架频响（CM3-update2.py）"
type: command-stream-case
software: GFE
chapter: 3
version: v3.x
tags: [gfe, 命令流, case, 频响分析, 稳态动力学, 草图draft, 复制网格]
sources: ["[[GFE2026-CM-ch03-CM3-update2.src]]"]
created: 2026-06-11
updated: 2026-06-11
---

# 概览

官方 v3.x 命令流（605 行，参数化），对应 [[GFE-Cases-03-华夫板框架]]。单位 m–t–kPa。**官方 py 全程草图重建几何（非 open_inp 导入）**——发布态 .pre 里的 InpMesh-1 是另一条产品化路径。调用链：参数区 → 材料 C30 → draft 草图（华夫板挖孔/筏板/屋面板梁线/柱线）→ extrude/translate/make_array → 集合（体/面/边三级）→ 截面（实体+[[壳单元]]+[[梁单元]]）→ merge 总装 → 线控制网格 → copy_mesh 建 B31 → 边界/频响激励 → 稳态动力步 → 工况 → inpio 导 INP。详细路径见 `D:\GFE\GFE_KB\02_案例反推\路径_ch03_华夫板框架频响.md`。

# 关键 idiom

- **草图内阵列**：选中线后 `set_operate_mode(14); array_selected(nx,ny,dx,dy)`——孔阵 8×8 再整组 6×6 两级阵列；挖孔=fill 后切 `set_snap_object(4)`（面模式）框选圆面 `remove_selected()`。
- **copy_mesh（"复制网格"命令流 API，v3.x 可达；v2.15 断点）**：`GFE.geometry.geotool.copy_mesh(name="beam", origin_node=True, as_source=True, type_name="B31", new_set_name="beamb31-1")`——平面内嵌梁线划网格不生成梁单元，必须以此补建。
- **manager edit**：`o=sect_mgr().find('beam'); o.elset_name='beamb31-1'; sect_mgr().edit(o)`——改既有对象用 find+edit（[[命令流manager-CRUD]]）。
- **线控制局部加密**：`cc=mesh_generator.curve_control(); cc.set_name='0.5mesh'; cc.edges={几何id:[边id,...]}; cc.density=0.5; controller.size_option=[cc]`——全局 1.0 网格下把华夫板边细化到 0.5。
- **节点集坐标查找**：`mesh_mgr().find('Merge-1').node_data()` 返回 (节点号列表, 坐标列表)，按目标质心 ±0.1 容差匹配 → `nset.data=...; unsort=True; nset_mgr().add`——不可硬编码节点号（改参后会失效，官方 py 自注此坑）。
- **频响虚部激励（仲裁）**：**单个 boundary 对象同时带 value（实部，全零）与 `value_im=[0,0,1,0,0,0]`（虚部 Z 向单位力）**，type=5、valid_dof=4；dump 里的双 BC 对象是 GUI 副产物。value_im/amplitude_im 仅频响分析有效（[[幅值函数]]）。
- **merge 名传空串**：`builder.merge([...], True, '')` → 产物自动名 'Merge-1'。

# 参数真值与坑

- 几何：华夫板 48×48×0.5、孔 r=0.25 @0.9、孔组 6×6 每组 8×8、首孔偏移程序算；筏板 z=-4（壳 t=0.3）、屋面板 z=+4（壳 t=0.15）、柱 7×7 高 8（0.6×0.6）、屋面梁 0.8×0.3。**筏板平移官方 -4.0**（手册"拉伸-0.4m"为错印）。
- 材料 C30：ρ=2.5、E=3e7 kPa、ν=0.2。
- 稳态动力步 SSD-1：direct=True（直接法）、`data=[[1, 50, 10, 1.0, 1.0, 0.1]]`（fmin/fmax/频率点/疑缩放枚举/后两列语义未明——**官方 1.0/0.1 与 dump 0.0/0.0 分叉**）；global_damping structual=0.02。
- 场输出 `time_type=2; frequency=1`——"频率=1"是每 1 个求解点输出一次，不是 1 Hz。
- 后处理频响曲线横轴标"时间"实为频率扫描点（1→50 Hz）；存 .pre/提交作业仍 GUI 断点。
