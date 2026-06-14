---
title: "GFE-命令流API规格 — 文法、32 模块、787 函数全签名"
type: manual
software: GFE
tags: [gfe, manual, 命令流, api, 文法]
sources: ["[[GFE-CmdKB-APIref.src]]", "[[GFE-CmdKB-APIspec.src]]", "[[GFE-CmdKB-cppclasses.src]]", "[[GFE-CmdKB-manualdiff.src]]"]
created: 2026-06-04
updated: 2026-06-04
---

> GFE 命令流的「文法」层：运行时自省 1607 符号 + RTTI 反解 453 个 C++ 类，得到 787 函数全类型签名、519 属性、43 枚举，分 32 模块。是「某命令怎么写」的权威速查；逐条签名见 raw [[GFE-CmdKB-APIref.src]]（原始自省清单 [[GFE-CmdKB-APIspec.src]]）。

## 核心范式
见 [[命令流manager-CRUD]]：每模块一个单例 `X_mgr()`；构造对象 → 设属性（def_readwrite）→ `mgr.add(obj)`；工况装配 `case.set_bcs / set_vload / set_artbc / set_fieldReqs / set_elemAdd / set_elemDel(步名, [名])`。模块间引用规则见 [[GFE对象引用关系]]。

## 32 模块速览
**前处理 GFE.Pre**：amplitude（[[幅值函数]]）· artbc（[[粘弹性人工边界]]）· boundary（边界 / 荷载，含 type=9 [[列车荷载]]；⚠v3.3.0 起列车属性从通用荷载对象裁撤，旧脚本断裂，见 merged #63/A6）· case（工况，含 [[单元生死]] set_elemAdd/Del）· document · field · geometry · initial_condition · interaction（[[绑定约束]] tie / [[嵌入区域]] embed / [[连接器]] connector / mpc / rigid / contact / incident_wave 爆炸 / spring_dashpot 接地弹簧 / special_interaction）· material（[[本构模型]]：user_type=1 混凝土 / =2 [[Davidenkov]] / [[混凝土塑性损伤]] concrete_damaged）· mesh（含隐藏 mesh_data 底层增删节点 / 单元）· orientation · output · section（[[实体单元]] / [[壳单元]] / [[梁单元]] property_*）· set（gset / elset / nset）· soil（[[一维土层]]）· sph（[[SPH光滑粒子流体动力学]]）· step（含 dynamic_explicit + [[质量缩放]]）· surface · vibration（[[地震场地反应]] vibra_load）
**几何**：geometry.geoprim（extrude / cut / translate / make_array）· geotool · contact_pair（搜索接触）· mesh_generator（gmsh / sweep）· draft（草图器，v3.4.0 新增，v2026 手册第 4 章 PDF p136-155 有全套文档；自省 42 方法）· occ / occ.brep_prim（OpenCascade 基本体）
**IO**：io · io.inpio（INP 读写）
**土体**：soil（顶层 GFE.soil：快速建土 box_builder / data_builder——注意与 GFE.Pre.soil 一维土层是两个模块）

## 隐藏命令（手册查不到，反编译才有；详见 [[GFE-CmdKB-manualdiff.src]]，diff 基于旧版 ≤2.15.2 手册，引用前按 v2026 复核）
- `GFE.draft` 草图器：旧版手册（≤2.15.2）无文档，曾列"整模块隐藏"；v3.4.0 起为手册正式第 4 章（PDF p136-155），已非隐藏。
- **关键隐藏方法**：case.**set_artbc** / case.**set_vload**（工况挂人工边界 / 场地反应）、material.**as_elastic**（弹塑性一键转弹性）、mesh.mesh_data.add_node / add_element（底层网格）
- **隐藏枚举**：material.entry_type、step.StepType、step.modal_damping_*
- **隐藏类**：connector_base、steady_dyn_step（频响）。注：concrete_damaged 与 incident_wave 系旧 diff 机械匹配误报，手册实有文档（CDP 见 §2.6.6；冲击波见 §2.13.11-2.13.14）——incident_wave 的真坑是手册构造器文档名 iw()/incident_wave_property_manager() 与示例 incident_wave()/iw_prop_mgr() 不一致，按章节文档名拼会失败。

## 坑
- 多函数签名靠「TypeError 逼签名」反推；标「疑似改模型，未实调用」的（delete / delete_all）勿乱试
- C++ 类名（[[GFE-CmdKB-cppclasses.src]]）部分为编译器 mangled 名，仅作内部类型模型参考

相关：[[GFE-CmdKB]] · [[GFE-Cmd]] · [[命令流manager-CRUD]] · [[GFE对象引用关系]] · [[GFE-命令流桥与工具]]
