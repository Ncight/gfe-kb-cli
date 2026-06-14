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

## DWG → DXF（管线起点）

车站/基坑断面常是 DWG。**推荐装 ODA File Converter**（免费，opendesign.com）转 DXF：本机若有 `ODAFileConverter.exe` 直接批转；FreeCAD 也能 Import 部分 DXF。未装 → 提示装 ODA File Converter。DXF 进 FreeCAD（`Import` 或 `Draft`/`importDXF`）→ 提形/拉伸成几何。

## 单位 / 铁律（高频）

m-t-kPa（E[kPa]/ρ[t/m³]/c[kPa]）；β=0（显式动力稳定）；`auto_transfinite=False`（嵌入面线防卡死）；命令流无 save_pre。更多见在线 `pitfalls` / `INDEX`。

## 与既有 skill 关系

`gfe-command-stream`（读 D:\GFE\GFE_KB 整库做深度建模/桥）侧重知识全量；本 skill 是**端到端动手**：在线速查 + FreeCAD MCP 建几何 + GFE 命令流跑通 + 调参。
