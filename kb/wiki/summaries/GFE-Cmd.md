---
title: "GFE-Cmd — 嵌入式 Python 命令流 API 与 manager-CRUD 参数化建模手册"
type: manual
software: GFE
tags: [gfe, manual, api, scripting, ssi, modeling]
sources: ["[[GFE-Cmd.src]]"]
version: v2026（3.4.0，2026.02）；MD 源版 2.15.2
publisher: 广州颖力科技
created: 2026-06-04
updated: 2026-06-04
---

> [[GFE]] 软件 [[PrePo]] 前处理器的命令流（command stream）参考手册：在 GUI 右侧切到 “python” 输入框，用嵌入式 Python（embedded Python）对每个建模模块的对象做增删查改（CRUD），实现批量、可复现、参数化的土-结构建模。面向需要脚本化 SSI / 抗震建模的工程师。

## 覆盖范围
- **命令流总架构**：顶层 `GFE` 模块下挂 6 大子模块——`Pre`（前处理，最核心）、`geometry`（几何运算 / 网格生成）、`io`（导入导出）、`Soli`（土体建立）、`occ`（简单几何体）、`draft`（草图建模，v3.4.0 新增，第 4 章：u/v 二维草图坐标、`get_current()` 入口、`export()` 导入 OCC）。旧版手册（MD 源 2.15.2）写 5 个子模块。
- **manager-CRUD 范式**：每个前处理模块都有一个对应的单例**管理器（manager）**，所有对象的 add / find / edit / del / rename / 计数 都通过管理器进行。
- **Pre 模块全子模块**：document / geometry / mesh / material / set / surface / section / boundary / initial_condition / amplitude / interaction / step / output / soil / vibration / artbc / case / orientation / field / sph。
- **几何与网格**：contact_pair（搜索接触）、geoprim（布尔 / 平移旋转缩放 / 阵列）、geotool（施工助手 / 隧道建模 / 非均匀土层 / Davidenkov 转换 / 调幅）、mesh_generator（gmsh 风格控制器）、complex_field（复杂场地反应计算，§3.6）、engineer（子模型位移/力传递 pass_disp/pass_force，§3.7）——后两者 v3.4.0 新增。
- **IO**：YJK、Abaqus INP、GFE pre、DWG、gmat 材料的导入导出；INP 写入器。（命令流 IO 无 PKPM 导入函数；PKPM 只是 GUI 导入接口，见 UserGuide §1.2.2。）
- **完整命令流应用示例**（第 8 章，共三个）：① YJK 导入做恒荷载；② 隧道开挖分阶段监测；③ 修改材料属性（§8.3：find→遍历 entries 判型→改 params→edit 提交）。

## 关键章节
- **第 1 章 命令模块总览**：命令流入口 = GUI 右侧输入框点 “python” 切换。必备导入 `import GFE; from GFE import *`，子模块如 `from GFE.Pre import *`、`from GFE.occ import *`（**大小写敏感**）。
- **§2.3 管理器（manager）**：基类通用 API——`auto_name(prefix, has0=False)` 自动唯一命名（如 `Box-1`）；`add(obj, inner=False, auto_name=False)`；`find(name)` / 基于 id 的 `find(id)`；`edit` / `del` / `del_all` / `rename` / 计数 / `exist` 检查；返回 `status` 对象带 `CODE`（`err_code.SUCCESS`）与 `MESSAGE`。这是全手册的建模总骨架。
- **§2.6 材料（material）**：核心是 `material()` 对象 + `entries` 属性列表 + `mat_mgr().add()`。本构对象覆盖 density / elastic / [[瑞利阻尼]]（α, β 两参）/ plastic / concrete_damaged（[[Drucker-Prager]] 系混凝土损伤 CDP）/ hyperelastic / hyperfoam / viscoelastic / [[Drucker-Prager|mohr_coulomb]] / **user（用户材料，user_type=2 即 [[Davidenkov]]）** / test_data / porous_bulk_moduli / expansion / bed_coefficient / creep。
- **§2.10 边界与荷载（boundary）**：单一 `boundary` 对象按 `type` 整数区分 21 种类型（0 约束 / 1 位移 / 3 速度 / 4 加速度 / 5 力 / 7 重力 / 9 列车荷载 [[列车荷载]] / 15 水压力 / 16 孔隙压力 …）；`valid_dof` 用 6 位**二进制位掩码**设自由度（1=放开，0=约束）。
- **§2.11 初始条件（initial_condition）**：InitStress / InitVelocity / InitPorePress / InitRatio / **InitGeostaticStress（地应力，[σ1,σ3,Z,α]）** / InitTemperature / InitSaturation——岩土地应力平衡的脚本入口。
- **§2.13 相互作用（interaction）**：surface_pair（绑定 tie）、**contact（type=0 通用接触 general contact / 1 面面接触，friction 摩擦系数，可设粘性损伤）**、rigid_body、embed（嵌入）、mpc、冲击波 iw、**spring_dashpot（弹簧阻尼器，type 位运算组合 spring1/2/A + dashpot1/2/A）**、connector 连接器行为 / 属性。SSI 中土-结接触、人工边界等价弹簧均在此。
- **§2.14 分析步（step）**：static_general / frequency（模态）/ **dynamic_explicit（显式动力，主力）** / dynamic_implicit / **geo_static（地应力）** / modal_dynamic / response_spectrum（频响）/ **soils（土分析步，可固结 is_consolidation）** / sph。配套 global_damping（α/β/structural）、mass_scaling（质量缩放）、modal_damping / dyn_modal_damping。
- **§2.16 一维土层 / §2.17 场地地震反应（vibload）/ §2.20 人工边界（art_bc）**：SSI 三件套。soil 对象给土层 depth / materials / bedrock_mat；vibra_load 把底部 X/Y/Z 幅值函数 + 1D 土层做[[地震场地反应]]（is_outcrop 露头、input_loc 输入位置、EERA 风格参数 SubLayerHeight/TimeInterval/N=4096 等）；art_bc 用结构形心自动生成[[粘弹性人工边界]]。
- **§2.21 工况（case）**：`case` 对象用 steps 列表 + 各 step→对象名列表的映射（bcs / initialConditions / vload / artbc / fieldReqs / histReqs / **elemAdd / elemDel 生死单元**）组装分析序列，是“模型→可计算工况”的总装配。
- **§3.4 geotool 施工助手**：`sort_stage_items` 按坐标排序、`add_stage` 向工况批量加阶段（施工分步 / 开挖）；`build_tunnel_shape`（圆 / 三心圆 / 五心圆 + 反拱 + 岩带 + 3D 扫掠）；`build_non_uniform_soil`（采样点 + Delaunay 建非均匀土层）；`convert_to_davidenkov` / `revert_davidenkov`（[[Davidenkov]] 材料一键转换，需 test_data）；`compute_era` 地震动调幅。
- **第 6 章 IO**：`io.get_current()` 拿实例；`import_yjk`（含 dtlmodel.ydb/dtlCalc.ydb）/ `open_inp` / `open_pre`（可 merge）/ `open_dwg` / `import_mat`·`export_mat`（gmat）；INP 写入器 `inpio.writer(path).set_case(...).perform()` 导出 Abaqus INP。

## 核心用法与参数
- **建模总范式（必须记住）**：`new 对象 → 设属性 → 取管理器 → mgr.add(对象)`。材料是两层：先建本构 entry（density/elastic/…），塞进 `material.entries=[...]`，再 `mat_mgr().add(material)`。
- **必备导入**：`import GFE` / `from GFE import *` / `from GFE.Pre import *`；子模块 `from GFE.io import inpio`、`from GFE.geometry import geotool, mesh_generator` 等。
- **自由度位掩码**：`valid_dof` 二进制 6 位 `(rz ry rx z y x)`，`7`=`0b000111`=放开三平动锁三转动。
- **常用默认 / 推荐值（手册示例值，非工程定值）**：弹性 `params=[E, ν]`（示例 `[3e7, 0.2]`）；阻尼 `params=[α, β]`；接触 friction 示例 `0.3`，tie 位置容差 `parameters=[0.001~0.01]`；静态步 `init_inc=0.1, period=1.0, min_inc=1e-5, max_inc=0.1`；vibra_load EERA 参数 `N=4096, TimeInterval=0.02, SubLayerHeight=1, MaxIter=100, Tol=1e-2`。
- **典型 SSI 全流程（§8.1 摘要）**：import_yjk 上部结构 → 建土层材料 + soil 对象 → `Soli.box_builder/data_builder` 生成土体实体 → geoprim 平移土体对齐地下室上表面形心 + cut 挖出地下室 → 取底面建集合加 type=0 固定 + type=7 重力 → contact_pair.search_face 找土-结接触面 → 建 geometry_surface + surface_pair(tie) → mesh_generator 划网 → 建 step + case → inpio.writer 导出 INP。

## 坑与注意
- **命令流是嵌入式 Python，不是 Tcl/独立脚本**：在 PrePo 的 “python” 输入框里逐段执行；模块名 `Pre / occ` **大小写敏感**，写错即 import 失败。
- **手册里的本构标签有错印**：§2.6.5 标题写成 “塑性 (elastic_obj)”、§2.6.11 user 材料示例输出却说“摩尔库伦”、§2.6.9 viscoelastic 示例输出说“泡棉”——以**属性表与字段语义**为准，别信示例末尾那句中文输出说明。
- **示例代码有笔误**：如 `dyn_step = [obj_ms1]`（应为 `dyn_step.mass_scaling = [...]`）、`modal_damp工人 definition`、`generator.gender()`（应为 `generator()`）、字符串引号缺右引号（`obj.amplitude = "`）。手抄进生产脚本前需逐处修正。
- **user_type 枚举**（§2.6.11）：0 普通 / 1 一维非线性 / **2 Davidenkov** / 3 HSS / 4 南水 / 5 屈曲钢筋 / 6 JH2 / 7 E_v / 8 E_B / 10 亚塑性——Davidenkov 走 user 材料而非独立类，与 INP 侧 `*User Material`+29 SDVs 对应（参见库内 Davidenkov 记忆）。
- **显式动力阻尼**：本手册给 global_damping 含 α 与 **β**，但 GFE 显式求解中 β 必须为 0（非零 β 触发质量缩放级联 + CDP PD Failed），这是求解器侧约束，命令流不会替你拦——见 [[GFE-Explicit]]。
- **与 ABAQUS / INP 的关系**：命令流本质是“脚本化生成 GFE 模型 → 导出 Abaqus 风格 INP / INPX”。`open_inp` 可反向导入 INP；列车荷载需 `set_trainload2inpx(True)` 才会写进 INPX。
- **版本相关**：现行手册 v2026 对应软件 3.4.0（2026.02，修订记录 PDF p192-193）；本页 MD 源对应 2.15.2（2025.07 首发）。版本演进 2.15.2→3.2.2→3.3.0→3.4.0：3.3.0 列车荷载有破坏性变更，3.4.0 新增 complex_field/engineer/draft。不同版本 API 字段可能增减；`is_consolidation`、SPH、亚塑性等较新功能需对应版本。
- **路径用 UTF-8 / 正斜杠**：IO 全部 `u8path`，支持相对路径（以工作路径为基准，`get_work_path`/`set_work_path`）。

## 交叉引用
- 其他手册：[[GFE-UserGuide]]（GUI 全流程，命令流的图形对应）· [[GFE-Explicit]]（显式求解器，阻尼 / 接触 / 人工边界实现）· [[GFE-Implicit]]（隐式 / 单元本构基准）· [[GFE-SSA]]（地下结构动力分析专版）· [[GFE-Cases]]（工程算例，多由命令流可复现）
- 软件 / 实体：[[GFE]] · [[PrePo]] · [[广州颖力科技]] · [[GFE-Cmd]]（命令流知识库 skill 索引）
- 概念：[[Davidenkov]] · [[Drucker-Prager]] · [[粘弹性人工边界]] · [[地震场地反应]] · [[列车荷载]] · [[地上-地下耦合结构]] · [[SIUS]] · [[ULSFS]] · [[IPA简化抗震分析法]]
- 相关论文：[[Liu2006R78]]（粘弹性人工边界）· [[Chen2005R79]]（土体动力本构 / Davidenkov）· [[Qiu2024R04]] · [[Qiu2025R05]]（地下结构抗震数值模型，与命令流建模能力对应）
