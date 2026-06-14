---
title: "GFE2026 官方命令流案例 ch04 — 核电站土-结构显式动力"
type: command-stream-case
chapter: 4
version: v3.x
software: GFE
tags: [gfe, command-stream, ssi, seismic, artificial-boundary, eera]
sources: ["[[GFE2026-CM-ch04-CM4-update2.src]]"]
created: 2026-06-11
---

# GFE2026 官方命令流 ch04：核电站 SSI 显式动力（CM4-update2.py，1345 行）

官方 v3.x 命令流全流程案例：双厂房+安全壳（弹性壳）坐落于 4 层均匀场地（300×300m），[[粘弹性人工边界]] + [[地震场地反应]]（EERA 等效线性）输入，单工况显式动力导 INP。单位 m–t–kPa。

## 调用链概览

1. **草图建模**（draft 状态机）：`set_normal(origin,normal,xdir)` → `set_operate_mode(1直线/2折线/4弧/5三点弧/7圆/-1选择)` + `input(x,y)` 画线；`set_snap_object(2)+snap_object(中点)+select_snaped(True)+fill_selected()` 填面；`export()` → `geo_mgr().add(name, shp)`。楼层落位靠 export 前改 set_normal 的 z 偏移；换图先 `clear()`（官方注释明示替代手册"选面删除"的残留清理）。
2. **三维成形**：`geoprim.builder()` 的 `extrude/make_array/revolve/cut/translate`；产物名用 `mgr.auto_name(base)` 收集列表。安全壳 `revolve([母线],[0,0,0],[0,0,1],6.28319)`。
3. **集合/材料/截面**：面集 `gset_basic(name).set_shapes(faces); gset_mgr().add(…)`；材料 entries 组装 `obj.entries=[density, elastic, damping]`（C40/C60，α=0.948805、**β=0**）；壳截面 `property_shell`（thickness/integral_point=5）。**先属性后合并**，再 `builder.merge(names, True, 'plant')`（三参带新名）。
4. **网格**：`mesh_generator.generator()+controller()`，厂房 size 1.0 / 土 8.0，`GFE.AutoTransfinite=True, generate_dim=3`。
5. **[[快速建土]]**：`GFE.io.get_current().import_mat(gmat)` 导入 4 种土材料（内含 EERA TestData 曲线）→ [[一维土层]] `soil(); depth=[2.42,32.4,4.0,23.8]（自上而下）; depth_dir=2; soil_mgr().add` → **box_builder + data_builder 两段式**：`box_builder().set_height(soil.depth, soil.depth_dir); set_parameter(300,300); shape=build()` → `data_builder(); dimension=3; name='Soil-1'; layer_shape=shape; layer_material=soil.materials; build()` 自动建几何+逐层集合+截面。
6. **挖地下室**：raft `extrude [0,0,16]` 成 basement → 取土体最高面形心对位 `translate` → `cut('Soil-1',['plant-basement'],True)`（True=替换保材料）。
7. **[[绑定约束]]批量 Tie**：`contact_pair.search_face(a,b,0.01)` 一次搜全 → 循环建 `geometry_surface` 对 + `surface_pair(name=tie_mgr.auto_name('Tie'), param_number=1, parameters=[0.01])`。plant-shell 与 Soil-plant 两批合计即 47 对。
8. **[[粘弹性人工边界]]**：包围盒 `get_shape_box_range` + 面形心容差筛 5 个边界 gset → `gset.get_shapes_id()` 转 `[[t[0],t[2],0]]` → `geometry_surface('TUTIAROUND')` → `art_bc(); structure='plant'; surface='TUTIAROUND'; centered=False`。
9. **[[地震场地反应]]**：幅值 1001 点硬编码平铺 → `vibra_load()`（amp_bottom_x 单分量、pwave_dir=2、soil='Soil1D-1'、is_outcrop=True、input_loc=-1）+ **14 个 `set_parameter`**（N=4096, TimeInterval=0.02, SubLayerHeight=1, Rr=0.5, MaxIter=100, Tol=1e-2, UseAmp/UseEERAMat/UseIntgOutp='true' 等）。
10. **分析步/工况/导出**：`dynamic_explicit_step(period=20.0)` + [[质量缩放]] `mass_scaling(type=1, frequency=100, region='*', target_time=5e-05)`、`ds.mass_scaling=[ms]`；工况**映射属性赋值** `c.vload['Dyna-1']=['VibLoad-1']; c.artbc[…]; c.fieldReqs[…]`（bcs 全空，人工边界替代约束）；`inpio.writer(path).set_case('Dyna'); perform()`。

## 关键经验

- **土层阻尼 α 不手写**：土材料 gmat 只带 TestData（G/Gmax-γ、ζ-γ），`UseEERAMat='true'` 使 INP 导出时自动生成 `<材料名>-EERA` 派生材料并逐层写 `*Damping, Alpha`（实测 0.2821/0.6191/0.4771/0.7341, Beta=0）。结构混凝土的 α 才在 material.damping 手写（α=2ζω₁，先模态）。
- **set_height 方向仲裁**：官方直接传一维土层 `soil.depth` 原序（表层在前，自上而下），与 materials 同序对位；旧反推"从下到上"不适用于 v3.x 官方用法。
- 本案例为弹性分析，无[[混凝土塑性损伤]]；CDP 预设库（GUI）被官方用纯命令流材料构造绕过。
- ⚠ v2.15 代差：data_builder、工况映射赋值不存在；v2.15 退回逐层手工建土 + set_* 系列。

相关：[[GFE2026-CM-ch05]]（非均匀场地版）、[[显式动力分析]]、[[土-结构相互作用]]
