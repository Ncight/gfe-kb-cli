---
name: GFE-autobuilding
description: 端到端 GFE/PrePo(广州颖力岩土有限元)自动建模——①在线查命令流知识库(787 API签名/能力矩阵/149避坑/15案例/wiki关联) ②FreeCAD MCP 实时建/改几何调参出STEP ③GFE noGUI 命令流(导几何→坐标分拣→网格→截面材料→施工分析生死单元→导INP)。当用户要 GFE 建模/参数化建几何/车站/基坑/SSI/施工分析/调参重跑、问 GFE 命令流某 API 怎么写、查 GFE 避坑或案例、或要 DWG断面→几何→GFE 全自动管线时使用。既能建模又能调参。未装 FreeCAD程序/freecad-MCP/DWG转DXF工具时主动提示安装。
---

# GFE 端到端自动建模

三块能力，按需组合：**①知识查询(在线) ②FreeCAD MCP 建几何 ③GFE noGUI 命令流**。
典型链：DWG断面 →[ODA转DXF]→ FreeCAD MCP 建几何 →[exportStep]→ GFE noGUI(分拣/网格/属性/施工) →[inpio]→ INP。

## ① 知识查询（在线，无需本地库）

数据托管 **github.com/Ncight/gfe-kb-cli**。答 GFE 命令流 API 签名/避坑前**先在线查准，别凭记忆**。
- 取文件（公开 repo）：WebFetch `https://raw.githubusercontent.com/Ncight/gfe-kb-cli/main/kb/raw/<文件>`
- 关键文件：`GFE-CmdKB-APIref.src.md`(787API签名) / `-pitfalls`(149避坑) / `-capability`(能力矩阵①②③) / `-objref`(模块引用规则) / `-paths`(15章案例建模路径)
- 全文搜：`gh search code "<词>" --repo Ncight/gfe-kb-cli --limit 20`
- 关联：WebFetch `kb/wiki/{entities,concepts,summaries}/*.md`（GFE↔论文↔概念双链）

## ② FreeCAD MCP 建/改几何（`mcp__freecad__*`）

实时驱动 FreeCAD 建几何、改参数、出 STEP 给 GFE。工具：`create_document`/`create_object`/`edit_object`/`delete_object`/`execute_code`/`get_view`/`get_objects`/`run_fem_analysis`。
- **建几何**：`execute_code` 跑 Part API（`makePolygon`/`Face`/`Shell`/`sewShape`/`makeCompound`/`makeLine`），按绝对 3D 坐标摆面/线（与 GFE 同 OCC 内核，STEP 无损）。
- **调参**：`edit_object` 改尺寸 → `get_view` 看 → 重导 STEP。
- **出 STEP**：`execute_code` 跑 `comp.exportStep(r"E:\...\x.step")`。

**前置依赖（未满足必须主动提示用户装，并给命令）**：
1. **FreeCAD 程序** — 本机 `D:\FreeCAD 1.1`。未装 → 提示装 FreeCAD 1.0/1.1（freecad.org）。
2. **freecad MCP** — 已 `pip install freecad-mcp`（本机✓）+ addon 落位 `%APPDATA%\FreeCAD\v1-1\Mod\FreeCADMCP`（✓）+ `claude mcp add freecad`（✓ Connected）。
3. **⚠ 关键运行前提**：`mcp__freecad__*` 调用失败/超时 = **FreeCAD GUI 没开 或 没激活 MCP workbench**。提示用户：**打开 FreeCAD → Workbench 下拉选 "MCP Addon" 激活**（addon 才起 RPC server，MCP 工具才通）。
- 不想开 GUI 时，几何也可走无头 `freecadcmd`：`& "D:\FreeCAD 1.1\bin\freecadcmd.exe" 脚本.py`（跑 Part API 出 STEP，不依赖 MCP/GUI）。
- **⚠ 当前 session 没有 `mcp__freecad__*` 工具时**（MCP 是 session 运行中 add 的、要重启 Claude Code 才加载）→ **fallback 直连 RPC**（等效，不依赖 session 工具）：
  ```python
  from freecad_mcp.freecad_client import FreeCADConnection
  c = FreeCADConnection()              # localhost:9875 (FreeCAD GUI 开+MCP Addon激活)
  c.ping()                              # True=通
  c.execute_code("import FreeCAD,Part; d=FreeCAD.newDocument('X'); ...")  # 跑任意 FreeCAD python
  c.create_document(name); c.create_object(doc, obj_data); c.edit_object(...)
  ```
  用 `py 脚本.py`(PowerShell, $env:PYTHONUTF8=1) 跑即控制 GUI 里的 FreeCAD。实测 PING True + execute_code 建几何成功。

## ③ GFE noGUI 命令流（`PrePo.exe py-script=`）

`E:\GFE2026\program\PrePo.exe` 无界面跑命令流：导几何→分拣→网格→截面材料→施工分析→导INP。
- 调用：`& "E:\GFE2026\program\PrePo.exe" "py-script=脚本.py"`（PowerShell，先 `$env:PYTHONUTF8=1`）
- 脚本要点（完整范式见记忆 `reference_gfe2026_nogui` + 在线 `paths`）：
  - `import GFE` + `import builtins as B`（环境遮蔽 set/round，用 B.set/B.round/B.abs/B.len）
  - 导几何 `GFE.io.get_current().open_geometry(step, name)`；取 shape `geo_mgr().find(name).shape()`
  - 分拣 `GFE.geometry.geotool.children(shape, 4=FACE/6=EDGE)` + `centre_of_mass`(返回 list)
  - 建土 `soil.box_builder`(set_height/set_parameter/build) + `data_builder`(layer_shape/layer_material/build)
  - 嵌入 `geoprim.builder().merge(['Soil-1','结构'],False,'')`→Merge-1（共节点；纯面/线 split 无效用 merge）
  - 网格 `mesh_generator.controller()` **必须给全 number_option(15键)+user_option+geom_to_type+generate_dim=3+auto_transfinite=False**（缺键C++崩；超限法死循环）
  - 析取 `geotool.copy_mesh(几何集, True, False, 'S3'/'B31', 前缀)`（面→S3壳/线→B31梁，**官方'S3'非'S3R'**）
  - 截面 `property_solid/shell/beam`（beam.shape=1矩形BOX/3圆/2工字, integral_point=5）赋单元集
  - 施工 `case.case()` .steps/.elemDel['步']/.elemAdd['步']（生死单元，土用几何集名/结构用copy_mesh集名）
  - 导出 `GFE.io.inpio.writer(path).set_case(c).perform()`（命令流无 save_pre，存盘走 GUI 或导 INP）
- **调参重跑**：改脚本顶部参数（尺寸/土层/网格/施工阶段）重跑 PrePo，脚本幂等（开头 delete_all）。

## ④ FreeCAD→GFE 信息挂接规则（STEP 只传几何骨架，②~⑨ 全在 GFE 端补）

STEP/几何只传 **构件几何+坐标+拓扑(①)**。其余 8 类「几何之外」信息 STEP 不带，全在 GFE 命令流补：

| 信息 | 命令流对象.字段 | 引用集类型 |
|---|---|---|
| ①构件标识 | `gset_basic(name)+set_shapes+gset_mgr.add` | 几何集 gset（坐标分拣建） |
| ②单元离散 | `copy_mesh(gset,type_name)` / 网格 controller | gset→elset |
| ③截面 | `property_shell/beam/solid` `.elset_name`+`.mat_name` | elset_name= gset 或 copy_mesh elset |
| ④材料 | `material.material .as_elastic/.entries`; `mat_mgr.add` | 被截面 `.mat_name` 引用 |
| ⑤连接 | `merge`(共节点) / `surface_pair`(Tie) / `embed` | Tie/接触=**表面集对**; embed=gset/elset |
| ⑥边界 | `boundary(.set,.valid_dof,.value)` / `art_bc(.surface,.structure)` | 约束=gset/nset; 人工边界=**表面集** |
| ⑦荷载 | 压力=`.surface` / 集中力=`.nset_name` / 体力重力=`.elset_name`(type7,value=[0,0,-9.8]) / `vibra_load`(地震) | 见左 |
| ⑧工况生死 | `case(.steps,.bcs[步],.elemDel/elemAdd[步],.vload,.artbc,.fieldReqs)`; `case_mgr.add` | elemDel/Add= gset 或 elset |
| ⑨输出 | `output_request(.sub_output=[node_output/element_output(variables)])`; field_mgr | gset 或整模型 |

**集合铁律 4 条**：**gset 几何集**→截面/BC/体力/生死单元；**surface 表面集**→压力/Tie/接触/人工边界；**nset 节点集**→集中力；**elset 单元集**→copy_mesh 产物(结构面线 S3/B31)/线荷载。（坑：截面/生死单元 `elset_name` 填几何集名也行——GFE 网格后几何集≈同名单元集，土用几何集名/结构用 copy_mesh elset 都实测成功）。完整规则在线查 `objref`。

**判据表做法（构件语义不靠 STEP 传）**：几何是我建的→**构件身份我天然知道**，不靠 STEP 命名（STEP 丢 Label/Group）。建几何时**同步吐「构件→坐标判据」JSON**（标高 z / 横坐标 x / 朝向），GFE 端按判据 `children`+`centre_of_mass` 分拣，不依赖 STEP 命名或 FreeCAD GUI。headless `freecadcmd` 也能做（更干净）。

## DWG → DXF（管线起点）

车站/基坑断面常是 DWG。**推荐装 ODA File Converter**（免费，opendesign.com）转 DXF：本机若有 `ODAFileConverter.exe` 直接批转；FreeCAD 也能 Import 部分 DXF。未装 → 提示装 ODA File Converter。DXF 进 FreeCAD（`Import` 或 `Draft`/`importDXF`）→ 提形/拉伸成几何。

## 单位 / 铁律（高频）

**全链统一 m-t-s → kN/kPa**（力 kN / 应力·模量 kPa：C40 `E=3.25e7 kPa`、`ρ=2.5 t/m³`、土 c[kPa]/φ[°]、g=`9.8 m/s²`；= Abaqus 自洽 SI-m 体系）。**FreeCAD 建模数值按 m 填（非 mm）**——实证 STEP→GFE `open_geometry` 数值一致传递。β=0（显式动力稳定）；`auto_transfinite=False`（嵌入面线防卡死）；命令流无 save_pre。详见记忆 `feedback_unit_convention` + 在线 `pitfalls`。

## 与既有 skill 关系

`gfe-command-stream`（读 D:\GFE\GFE_KB 整库做深度建模/桥）侧重知识全量；本 skill 是**端到端动手**：在线速查 + FreeCAD MCP 建几何 + GFE 命令流跑通 + 调参。
