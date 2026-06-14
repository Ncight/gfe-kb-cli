---
title: "GFE2026 官方命令流 ch14 — 半地下室爆炸 CONWEP（T14.py）"
type: command-stream-case
software: GFE
version: v3.x
chapter: 14
tags: [gfe, command-stream, 爆炸, CONWEP, 显式动力, 冲击波]
sources: ["[[GFE2026-CM-ch14-T14.src]]"]
created: 2026-06-11
updated: 2026-06-11
---

> 官方 761 行命令流做半地下室 [[CONWEP]] 空气爆破：与手册"基于官网 .pre 改爆炸件"不同，py 路线**从零建模**——YJK 导结构 + STEP 导土层 + 手写 9 个带退化曲线的 MC 土材料，再加冲击波两件套（incident_wave_property + incident_wave）直接进显式动力步。冲击波全字段实参与起爆点创建方式均为本页首次官方实证。

## 调用链概览

```
io.import_yjk(43 元参数, ch14 专用值) → SuperStru
→ 9 材料 TU1-1…TU4: density+elastic+damping(α=2.59055, β=0)+mohr_coulomb+test_data(8 组退化曲线)
→ io.open_geometry(heb.step) → 'Shape-1' 土层几何
→ contact_pair.search_face('Shape-1','SuperStru',0.01) → 前 6 对建 Tie
→ mesh_mgr().add("dp", x,y,z) 起爆点自由节点 → nset 'dp'
→ incident_wave_property(type=0, data=[100,1000,1,1,1000]) + geometry_surface 迎爆面(side=0) + incident_wave
→ gset_basic.set_shapes_id([[3,2,n]]) 土层集 soil1~9 → property_solid ×9
→ boundary(Set-base/X/Y) → dynamic_explicit_step + mass_scaling
→ field(IWCONWEP/DAMAGEC/DAMAGET…) → case 字典 → mesh(Shape-1 size4 → SuperStru size2) → inpio.writer
```

## 关键经验（官方实证）

### 1. incident_wave_property / incident_wave 全字段实参

```python
prop = GFE.Pre.interaction.incident_wave_property()
prop.name = 'air_blast_prop'
prop.type = 0                                # 属性名是 type（0=AirBlast）——非 def_
prop.data = [100, 1000.0, 1.0, 1.0, 1000.0]  # [TNT当量, 质量→kg, 长度→m, 时间→s, 压力→Pa]，t-m-kPa 系
GFE.Pre.interaction.incident_wave_property_manager().add(prop)

obj = GFE.Pre.interaction.incident_wave()
obj.id = 0; obj.name = 'IW-1'
obj.is_node_set = True; obj.set_name = 'dp'; obj.node_id = 0
obj.surf_name = 'baozha_surface'
obj.time_detonation = 0.0; obj.mag_scale_factor = 1.0
obj.prop_name = 'air_blast_prop'
GFE.Pre.interaction.iw_mgr().add(obj)
```

冲击波属 interaction **不经工况挂载**、全局生效；INP 端落为 `*Conwep charge property` + `*Incident wave interaction, CONWEP, property=…`（官方 Model-1-Case-1.inp 已核）。

### 2. 起爆点（参考点）创建方式

```python
GFE.Pre.mesh.mesh_mgr().add("dp", 190.6268, -0.1791, -18.4)  # 网格管理器直加自由节点
o = GFE.Pre.set.nset(); o.name='dp'; o.data=[2]; o.unsort=False  # ⚠ 硬编码节点号
GFE.Pre.set.nset_mgr().add(o)
```

无须 GUI 参考点/occ vertex。官方在**划网格之前**加点故拿到节点号 2；复刻时应建点后反查实际节点号，硬编码脆弱。

### 3. 迎爆面表面集

`geometry_surface('baozha_surface')`，按面形心 z∈(-20.5, -10.3) 筛 SuperStru 外墙面，`obj.data=[[geo_id, face_id, 0]]`（**side=0 实证可用**），`to_node_surface=False`，入 `surface.surf_mgr()`（与 surface_mgr() 双名）。

### 4. config.txt 不在 py 中处理

T14.py 全文**无 config.txt 相关代码**；单元失效开关（IsRemoved_Co 等三行）仍是装机级人工/外部脚本步骤。配套 rungfe.bat 给出命令行直跑：`PrePo.exe -daemon -dat <inp> -gfedir <dir> -gpu`。

### 5. 其他要点

- 土材料含 `test_data`（n_test_data=8，24 元 [γ, G/Gmax, ζ]×8）= 模量退化+阻尼比曲线，配 `damping params=[2.59055, 0]`——**β=0 显式动力恒定约定**再次印证。
- 土层集合按 id 直建：`gset_basic('soil1').set_shapes_id([[3, 2, 9]])`（[geo_id, 2=实体, sub_id]，soil1~9 对应 sub_id 9~1 **倒序**）——与 ch6/ch7 形心判定不同的第二种建集路线，前提是 STEP 导入几何 id 稳定。
- 显式步 + 质量缩放：`mass_scaling(region='*', type=1, frequency=100, target_time=5e-05)`，`obj.mass_scaling=[ms]` 列表；nlgeom=True，period=1.0。
- 场输出：节点 **IWCONWEP**（冲击波压力是节点变量）/U/UR + 单元 DAMAGEC/DAMAGET/E/PE/S，interval=0.01。
- **无地应力步**：工况 Initial→Dyna-1 直爆（演示简化）；[[搜索接触]] 结果只取前 6 对（tie_list=[0..5]）。
- 官方笔误：soil7 截面 `name='soil'`（漏 7）；`set_application_by_ui()` 开头重复 2 次。

## 相关

[[GFE-Cases-14-爆炸]]（手册 GUI 路线）｜路径文件 `D:\GFE\GFE_KB\02_案例反推\路径_ch14_爆炸CONWEP.md`（已按官方校正）｜[[CONWEP]]｜[[通用接触]]
