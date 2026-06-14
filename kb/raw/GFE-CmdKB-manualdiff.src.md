# GFE 命令流 binding vs 手册 diff
> 来源：D:\GFE\GFE_KB（gfe-command-stream skill 维护的命令流知识库）。本文件为 raw 检索源副本，2026-06-10 Fable 二审后刷新（ADR-0001：派生快照随主库可变）。

---
手册基线: manual_text.txt（v2025 截断提取文本, 2.15.2）
binding基线: gfe_api_spec.txt（运行时自省）
警示: v2026_0302（3.4.0）手册补齐 draft/复杂场地/子模型等章节后, 本页 A-F 节大量"隐藏"论断失效; 2026-06 P3 已按 phase2 审计复核修订
---

# GFE 命令流手册 vs binding 差异报告
手册函数声明(函数:)约 244 处（⚠基于 v2025 截断提取文本 manual_text.txt 的统计口径，v2026 全本口径已变）; binding: 32 模块/787 func/519 prop/43 enum/218 class

## A. 整个模块/子系统在手册中名字都查不到(强隐藏)
- （空——原列 `GFE.draft`：仅 v2025 截断文本中不可见；v3.4.0 起手册第 4 章整章文档化（PDF p136-155），已移出）

## B. 各模块专有方法文档覆盖率 (命中/专有总数; 低=大量隐藏)
- `GFE.Pre.material`  0/1 (0%)
- `GFE.Pre.step`  0/1 (0%)
- `GFE.Pre.surface`  0/1 (0%)
- `GFE.draft`  约39/42 (≈93%, 按 v2026 第4章；仅 import_shape/set_constrain_value/set_normal 仍未见于手册)
- `GFE.Pre.mesh`  5/25 (20%)
- `GFE.occ`  9/17 (53%)
- `GFE.geometry.geotool`  9/10 (90%, §3.4.14-16 在 v2025 原文即有文档；仅 get_id_by_shape 隐藏)
- `GFE.Pre.case`  6/8 (75%)
- `GFE.Pre.document`  4/5 (80%)
- `GFE.Pre.set`  6/6 (100%, get_shapes_id 在 v2025 §2.7.2 即有示例)
- `GFE.geometry.geoprim`  12/14 (86%)
- `GFE.Pre.geometry`  2/2 (100%)
- `GFE.Pre.output`  3/3 (100%)
- `GFE.Pre.vibration`  1/1 (100%)
- `GFE.geometry.contact_pair`  2/2 (100%)
- `GFE.geometry.mesh_generator`  3/3 (100%)
- `GFE.io`  5/5 (100%)
- `GFE.io.inpio`  3/3 (100%)
- `GFE.occ.brep_prim`  6/6 (100%)
- `GFE.soil`  6/6 (100%)

## C. 隐藏的专有方法 (名字全文不出现, 共 40；原 80, 2026-06 复核删 40 条已文档化/误判条目)
- `GFE.Pre.case.case.set_artbc`
- `GFE.Pre.case.case.set_vload`
- `GFE.Pre.document.set_application`
- `GFE.Pre.material.material.as_elastic`
- `GFE.Pre.mesh.manager.update`
- `GFE.Pre.mesh.mesh_data.add_element`
- `GFE.Pre.mesh.mesh_data.add_node`
- `GFE.Pre.mesh.mesh_data.get_element`
- `GFE.Pre.mesh.mesh_data.get_element_subtype`
- `GFE.Pre.mesh.mesh_data.get_element_surface`
- `GFE.Pre.mesh.mesh_data.get_element_type`
- `GFE.Pre.mesh.mesh_data.get_node`
- `GFE.Pre.mesh.mesh_data.rebuild_surface`
- `GFE.Pre.mesh.mesh_data.remove_element`
- `GFE.Pre.mesh.mesh_obj.each_et_elems`
- `GFE.Pre.mesh.mesh_obj.each_et_nodes`
- `GFE.Pre.mesh.mesh_obj.et_elems`
- `GFE.Pre.mesh.mesh_obj.et_elems_by_id`
- `GFE.Pre.mesh.mesh_obj.et_nodes`
- `GFE.Pre.mesh.mesh_obj.et_nodes_by_id`
- `GFE.Pre.mesh.mesh_obj.get_node_coordinate`
- `GFE.Pre.mesh.mesh_obj.is_valid`
- `GFE.Pre.mesh.mesh_obj.prs`
- `GFE.Pre.mesh.mesh_obj.transformation`
- `GFE.Pre.step.steady_dyn_step.get_single_points`
- `GFE.Pre.surface.geometry_surface.get_shape`
- `GFE.draft.controller.import_shape`
- `GFE.draft.controller.set_constrain_value`
- `GFE.draft.controller.set_normal`
- （注：原列 36 条 draft.controller 方法已于 v2026 第 4 章逐函数文档化（含签名/参数表/示例），2026-06 复核移出；仅上列 3 条仍隐藏）
- `GFE.geometry.geoprim.builder.revolve`
- `GFE.geometry.geoprim.set_tolerance_limit`
- `GFE.geometry.geotool.get_id_by_shape`
- （注：原列 get_selected_shape/get_selected_shape_id/get_shape_by_id 在 v2025 手册 §3.4.14-§3.4.16 即有完整文档，系 manual_text.txt 提取有损导致误判，2026-06 复核移出）
- `GFE.occ.compound.is_same`
- `GFE.occ.edge.is_same`
- `GFE.occ.face.is_same`
- `GFE.occ.shape.is_same`
- `GFE.occ.shell.is_same`
- `GFE.occ.solid.is_same`
- `GFE.occ.vertex.is_same`
- `GFE.occ.wire.is_same`

## D. 隐藏的枚举 (共 9)
- `GFE.Pre.material.entry_type`
- `GFE.Pre.step.StepType`
- `GFE.Pre.step.global_damping_field`
- `GFE.Pre.step.modal_damping_definition`
- `GFE.Pre.step.modal_damping_field`
- `GFE.Pre.step.modal_damping_type`
- `GFE.draft.Normal`
- `GFE.draft.OpMode`（取值表已在 v2026 §4.4-§4.6 文档化，仅枚举类型名未导出到手册）
- `GFE.draft.SnapObjMode`（同上，取值表见 §4.4-§4.6）

## E. 隐藏的类 (名字全文不出现, 共 34；原 38, 2026-06 复核删 4 条已文档化条目)
- `GFE.Pre.boundary.generic_bc`
- `GFE.Pre.document.application`
- `GFE.Pre.field.discrete_field`
- `GFE.Pre.field.expression_field`
- `GFE.Pre.field.field_manager`
- `GFE.Pre.initial_condition.InitialCondition`
- `GFE.Pre.interaction.connector_base`
- `GFE.Pre.interaction.contact_manager`
- `GFE.Pre.interaction.embed_manager`
- `GFE.Pre.interaction.general_section`
- `GFE.Pre.interaction.incident_wave_manager`
- （注：原列 incident_wave 类在 v2025 手册 §2.13.11 即有文档，2026-06 复核移出）
- `GFE.Pre.interaction.mpc_manager`
- `GFE.Pre.interaction.rigid_manager`
- `GFE.Pre.interaction.special_manager`
- `GFE.Pre.interaction.tie_manager`
- `GFE.Pre.material.mat_general`
- （注：原列 concrete_damaged(CDP) 类在 v2025 手册 §2.6.6 即有完整文档（含曲线属性与 n_* 按"组数"计数语义），2026-06 复核移出）
- `GFE.Pre.material.mat_permeability`
- `GFE.Pre.material.mat_sorption`
- `GFE.Pre.material.rate_dependent`
- `GFE.Pre.mesh.element`（对象属性 eid/sub_type/node_size/nodes 已在 v2025 §2.5.12 文档，仅类名字面未现）
- `GFE.Pre.output.history_mgr`
- `GFE.Pre.output.integrated_output`
- `GFE.Pre.output.out_req_mgr`
- `GFE.Pre.section.property`
- `GFE.Pre.section.property_bush`
- `GFE.Pre.section.property_membrane`
- `GFE.Pre.sph.sph_manager`
- `GFE.Pre.step.analysis_step`
- `GFE.Pre.step.steady_dyn_step`
- `GFE.geometry.mesh_generator.gmsh_control`
- （注：原列 curve_control/sweep_control 已在 v2026 §3.5 完整文档化（v3.2.2 修订记录"增加线控制、扫掠法的说明"），2026-06 复核移出）
- `GFE.io.instance`（类名未现但对象经 io.get_current() 完整文档化（§6），不应视为无文档）
- `GFE.occ.edge`
- `GFE.occ.vertex`
- `GFE.occ.wire`

## F. 隐藏的属性字段 (共 17；原 45, 2026-06 复核删 28 条已文档化条目)
- `GFE.Pre.field.discrete_field.datatype`
- `GFE.Pre.field.discrete_field.default`
- `GFE.Pre.field.expression_field.expression`
- `GFE.Pre.interaction.incident_wave.is_node_set`（v3.2.2 起荷载对象同名属性已文档化，incident_wave 侧归属存疑待实测）
- `GFE.Pre.interaction.incident_wave.mag_scale_factor`
- `GFE.Pre.interaction.incident_wave.node_id`（同 is_node_set，归属存疑待实测）
- （注：原列 prop_name/surf_name/time_detonation 在 v2025 手册 §2.13.11 即有文档，2026-06 复核移出）
- `GFE.Pre.interaction.incident_wave_property.def`
- `GFE.Pre.interaction.rigid_body.ref_set`
- （注：原列 concrete_damaged 10 条 CDP 曲线属性在 v2025 §2.6.6、hyperelastic.N/hyperfoam.N 在 v2025 §2.6.7/§2.6.8 即有文档，2026-06 复核移出）
- `GFE.Pre.material.mat_permeability.entities`
- `GFE.Pre.material.mat_sorption.entities`
- `GFE.Pre.material.porous_bulk_moduli.solid_grains`
- `GFE.Pre.mesh.element.state`
- `GFE.Pre.mesh.mesh_obj.doc`
- `GFE.Pre.mesh.mesh_obj.label`
- （注：原列 element.eid/node_size 与 node.nid/xyz 在 v2025 §2.5.9-2.5.12 即有文档，2026-06 复核移出）
- `GFE.Pre.step.sph_step.b`
- `GFE.Pre.step.sph_step.h`
- `GFE.Pre.step.steady_dyn_step.interval`
- （注：原列 curve_control 2 属性与 sweep_control 5 属性已在 v2026 §3.5 文档化，2026-06 复核移出）
## G. 手册名与 binding 名不一致（手册侧失真，照手册拼调用会 import/AttributeError 失败）
- 手册文档构造名 `iw()` → 实际类名 `incident_wave()`（§2.13.11 示例不一致）
- 手册文档名 `incident_wave_property_manager()` → 实际示例用 `iw_prop_mgr()`
- 手册章节名 `vibload` → 实际 Python 路径 `GFE.Pre.vibration`
- 手册章节名 `art_bc`（章名）→ 实际模块路径 `GFE.Pre.artbc`
- v3.x 修订记录 `gset_basic` 改名条目为笔误（存废待仲裁，见 GFE-Cmd__merged.md A2 条）
（真值锚点：GFE-Cmd__merged.md 行 501"模块章节名 ≠ Python 路径"陷阱、行 187/190；GFE-Cmd_p177-193.md 行 277）
