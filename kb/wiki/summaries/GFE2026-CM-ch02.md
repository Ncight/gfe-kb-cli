---
title: "GFE2026 官方命令流案例 ch02 — 钢骨混凝土柱静力/模态（CM2-update2.py）"
type: command-stream-case
software: GFE
chapter: 2
version: v3.x
tags: [gfe, 命令流, case, 静力分析, 模态分析, 草图draft, 嵌入钢筋]
sources: ["[[GFE2026-CM-ch02-CM2-update2.src]]"]
created: 2026-06-11
updated: 2026-06-11
---

# 概览

官方 v3.x 命令流（700 行，**参数表驱动**的整理版），对应 [[GFE-Cases-02-钢骨混凝土]]。单位 mm–N–t–MPa。调用链：参数区 → draft 草图（工字截面/箍筋框/主筋线）→ extrude/make_array/形心对位 → 布尔直接命名（cut/merge 带结果名参数）→ 材料 → 集合 → 截面（实体+梁）→ 总装 merge → 边界荷载 → 输出/步 → [[嵌入区域]] → 工况（映射赋值）→ 划网格 → inpio 导 INP。详细路径见 `D:\GFE\GFE_KB\02_案例反推\路径_ch02_钢骨混凝土柱.md`。

# 关键 idiom

- **draft 草图真 API**：`set_normal(原点,法向,X向)` 三向量定平面；`set_operate_mode`（1=直线、3=矩形、7=圆、14=阵列、-1=选择）；`input(x,y)` 落点；`set_snap_object`（0=落点、2=线、4=面）+ `snap_object`（点选 2 参/框选 4 参）+ `select_snaped` → `split_selected/remove_selected/fill_selected`；重合线要删两次；`export()` 出 shape、`clear()` 清场。
- **布尔直接命名**（对比 ch01 rename 两步舞）：`builder.cut(目标, [工具...], False, '结果名')`、`builder.merge([...], True, '结果名')`。
- **形心对位**：`centre_of_mass` 取两体质心差向量做 translate，实现精确对中。
- **程序化删构件**：箍筋阵列 41 片后按质心 z 过滤删首尾+与钢骨重叠段，`geo_mgr().delete + mesh_mgr().delete` 双删；阵列产物用名字列表全程追踪。
- **集合并集**：`gset_mgr().find('A').get_shapes_id() + find('B').get_shapes_id()` → `gset_basic.set_shapes_id(并集)`——由既有集合合成钢筋笼集。
- **嵌入区域**：`embed(); id=1; host_name='concrete'; embedded_names=['reinforcement-cage']; embed_mgr().add`——必须先有集合再建 Embed（[[嵌入区域]]）。
- **顺序硬规则实证**：多材料体先逐一赋截面再 `merge(替换=True)`；网格划分可放在工况之后（INP 导出前划完即可）。

# 参数真值与坑

- 工字钢 400×400 t=20、柱 600×600×4000、箍筋 500×500@100（截面 r=6.0 圆 [[梁单元]]，direction=(0,0,1)）、主筋 4 根 @500（r=12.5，direction=(1,0,0)）——梁 direction 因构件轴向而异，统一填会错；shear 是软件回显值须显式写入。
- 材料：Q345(7.8e-09, 206000, 0.25)、C40(2.5e-09, 32500, 0.2)。
- **自重 GRA=-9.8**（官方确证；与 mm 制矛盾但忠实手册，ch01 官方为 -9800）。压力：钢翼缘 2 MPa、柱顶 20 MPa（表面集经质心条件筛面）。
- 步：Static-1(nlgeom=False, inc 1.0/1e-05/1.0) + Modal-1(eigen=10)；输出 FO-Static 含 node U/UR/RF/RM + element E/S/SF/SM，`step='Step-1'` 为无害遗留串（官方也写）。
- 网格 Algorithm=2/Algorithm3D=10、DefaultSize=50，分两次 mesh（steel-concrete 与 reinforcement-cage）。
- 工况名官方写 'model'（疑笔误 modal）；模态工况只挂 BC 不挂荷载。
