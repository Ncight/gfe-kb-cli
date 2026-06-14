---
name: GFE-autobuilding
description: 端到端 GFE/PrePo(广州颖力岩土有限元)自动建模——能力盘式,AI 按「明确需求→对照能力→调用」三步自主编排,不套固定流程。能力:⓪在线查命令流知识库(API/避坑/能力矩阵/案例/挂接) · 建模端(A1 YJK正交结构带配筋 / A2 FreeCAD异形几何 / A3 GFE原生draft / A4 直导STEP·INP·ydb) · GFE处理(几何组织/土体/网格含copy_mesh析取/材料截面/连接边界/荷载/工况分析步/输出) · 求解后处理(导INP/daemon求解/读db/存盘)。当用户要 GFE/PrePo 建模/参数化建几何/车站/基坑/隧道/SSI/施工分析/调参重跑、问命令流某API怎么写、查GFE避坑或案例、YJK→GFE、FreeCAD→GFE、DWG断面→几何→GFE 时使用。既能建模又能调参。未装 FreeCAD程序/freecad-MCP/YJK/DWG转DXF工具时主动提示安装。
---

# GFE 端到端自动建模 —— 能力盘

## 用法总则（怎么用这个 skill）

拿到 GFE 建模任务，你（AI）自己：
1. **明确需求**——什么结构？什么分析(静力/施工分阶/SSI动力/损伤/模态/反应谱…)？要不要土？要不要配筋？输出什么？**不清楚就问用户**。
2. **对照能力盘**——看下面你掌握哪些能力、各能做什么、边界/断点在哪、入口怎么调。
3. **选+组合+调用**——按需求从能力里挑、拼、正确调用。
   - **怎么拼**：不确定能力怎么组合 → 查 ⓪ 案例库(`paths` 15 章找相似工程的建模路径)**参考拼法** → 拼出方案**先与用户对齐**(说清走哪几个能力、为什么、断点在哪)→ 再执行。
   - **不套固定流程、不背组合模板**（流程因任务而异，案例库是参照不是模板）；任何 GFE 具体范式/API/坑/挂接不确定，**先查 ⓪，别凭记忆**。

**划分原则**：能力按**功能/流程位置**归类，**不按 API 在哪个模块**（如 `geotool.copy_mesh` 归网格 B3、`geotool.convert_material` 归参数 B4，虽都挂在 geotool 模块）。

---

## 能力盘

### ⓪ 知识检索（元能力，撑起其余全部）
- **做什么**：在线查 GFE 命令流全知识——787 API 签名 / 149 避坑 / 能力矩阵(①命令流②半自动③纯GUI) / 15 章案例建模路径 / 对象引用挂接规则 / wiki 关联(GFE↔论文↔概念)
- **入口**：WebFetch `https://raw.githubusercontent.com/Ncight/gfe-kb-cli/main/kb/raw/<文件>`（公开 repo）；全文搜 `gh search code "<词>" --repo Ncight/gfe-kb-cli`
- **关键文件**：GFE—`GFE-CmdKB-APIref.src.md`(API签名) `-pitfalls`(避坑) `-capability`(能力矩阵) `-objref`(挂接规则) `-paths`(15章案例) ；wiki `kb/wiki/{entities,concepts,summaries}/`。**YJK**—`kb/yjk/YJK-API-index.src.md`(导航) → `YJK-CmdKB-commands`(命令清单2708) `-api`(YJKAPI方法) `-patterns`(建模范式) `-workflow`(YJK→GFE全链+驱动)；全量命令 `kb/yjk/_raw/cmd_*.tsv`
- **边界**：GFE + YJK 命令流知识都在本 repo（FreeCAD 的 API 查各自源）

### 建模端（产几何）— 按结构类型/来源选最省，土体一律走 B2
| 能力 | 做什么 | 入口 | 边界 |
|---|---|---|---|
| **A1 YJK** | 正交框架/地下室/明挖箱型车站/箱涵 → **带配筋**(三ydb:dtlmodel+dtlCalc+Jccad筏板) | YJK API python310 + 在线查 ⓪YJK KB | 仅正交标准层；盾构/圆/曲线不行；dtlCalc/Jccad 需 YJK 开着 |
| **A2 FreeCAD** | 任意**异形**结构几何(盾构/曲线/复杂) → STEP | `mcp__freecad__*` / 直连RPC / freecadcmd | 只几何无FE属性；不建土 |
| **A3 GFE原生** | 规则几何/隧道/支护 → 直接在GFE里建 | `draft`草图+`geoprim`布尔+`occ`基本体+`geotool.build_tunnel_shape` | 极复杂异形不如FreeCAD |
| **A4 直导已有** | 有现成几何就别重建 | STEP/IGES→`open_geometry`；INP→`open_inp`；ydb→`import_yjk` | — |

### B GFE 模型处理（几何→可解模型）— 核心，按流程
| 能力 | 做什么（命令流①可全自动） |
|---|---|
| **B1 几何组织** | 导入 + 坐标分拣(`geotool.children`/`centre_of_mass`→gset几何集) + 嵌入(`geoprim.merge`共节点；纯面/线 split 无效用 merge) |
| **B2 土体** ★一律走这 | `soil.soil`一维(层厚/材料/基岩/深向) → `box_builder`+`data_builder`三维(**自动产**分层集+LayerProp截面+一维"计算"出Vs/50建议网格) + `build_non_uniform_soil`非均匀 |
| **B3 网格** | 划分(`generator.mesh`+`controller`**全键**,auto_transfinite=False) + 线控/扫掠 + **析取(`copy_mesh`:几何集→命名单元集+换'S3'壳/'B31'梁+共节点)** + 查找(`mesh_data`)。断点:二阶C3D10转换(GUI/INP直写) |
| **B4 参数** | 材料(`elastic`/`concrete_damaged`CDP/`mohr_coulomb`/Davidenkov/阻尼 + YJK `convert_material`/`convert_reinforce`) + 截面(`property_solid/shell/beam`)。挂接见落地参考 objref 表 |
| **B5 连接边界** | 连接(`surface_pair`Tie/`contact`/`embed`/`connector`/`spring_dashpot`地基弹簧/`special_interaction`拉压异性·只压·带材料Tie) + 边界(`boundary` type全谱 + 初始条件InitGeostaticStress) + 人工边界(`art_bc`,SSI) |
| **B6 荷载** | 集中力/重力体力(type7,value=[0,0,-9.8])/压力/线荷载 + 地震(`vibra_load`+`compute_era`场地反应) |
| **B7 工况/分析步** | 步**全谱**(static/geo_static/dynamic_explicit·implicit/frequency模态/modal_dynamic/response_spectrum反应谱/steady_dyn频响+global_damping) + `case`装配(steps/bcs/生死单元elemDel·elemAdd/vload/artbc/fieldReqs)。**施工分阶=生死单元序列** |
| **B8 输出** | `output` field/history/envelope request |

### ⚑ 导出前自检（B 完成 → C 之前必过一遍；GFE 漏挂静默不报，不自检会跑错）
- **数量**：gset/elset/材料/截面/分析步 `count()` == 预期
- **单位自洽**：E[kPa](C40~3.25e7)·ρ[t/m³]·坐标[m]·g=9.8
- **挂接完整**：截面 `.elset_name`/`.mat_name` 指向存在的集/材料；BC/Tie/工况/输出 引用的集都存在(不存在静默失效)
- **漏挂**：每分析步该挂的 BC/荷载/生死单元/输出 都挂了
- **几何/网格**：分拣无遗漏面边(warn) · 嵌入界面共节点 · 无畸形单元

### C 求解 / IO / 后处理 — 多断点，命令流到 C1 为止
| 能力 | 状态 |
|---|---|
| **C1 导出** | `inpio.writer`(INP/INPX) + `export_mat` ← **命令流终点** |
| **C2 求解** | ⚠ 无API → CLI `gfe -daemon -dat <INP> -gfedir <目录>` / `PrePo -daemon`（GFEXC-CPU / GFEXG-GPU） |
| **C3 后处理** | ⚠ 云图/动画/层间位移角/轴压比 = 纯GUI；**可脚本读 `.db` SQLite** |
| **C4 存盘** | ⚠ `.pre` 无API → GUI File→Save 或桥 |

### 全局锚点（高频铁律，推理直接用、不必每次查）
单位 **m-t-s→kN/kPa**(E[kPa]/ρ[t/m³]/g9.8) · **土一律GFE内置(B2)** · `auto_transfinite=False`(嵌入面线防卡死) · `copy_mesh` 用 **'S3'非'S3R'** · **无save_pre** · **漏挂工况静默不报**(必自检) · 几何语义靠**自建「构件→坐标判据」JSON**(不靠STEP命名,STEP丢Label/Group)

---

## 落地参考（选了能力后怎么调：入口细节 / 坑 / 安装）

### ⓪ / 在线查用法
大文件(APIref/capability)可先 `gh search code` 定位再精取；WebFetch 取回在内容里找目标段。

### A1 YJK 入口（记忆 `yjkapi-pipeline`；本机 setup 已完成，直接可用）
- 跑：`$env:PATH="D:\YJKS\YJKS_8_0_0;"+$env:PATH`；cwd=安装目录；`& "D:\YJKS\YJKS_8_0_0\python310\python.exe" script.py`；脚本 `from YJKAPI import *`。
- 文法：`DataFunc()`→`StdFlr_Generate(层高)`→`ColSect_Def/BeamSect_Def/WallSect_Def(6,1,"b,h")`→`Joint_Generate(sf,x,y)`(mm)→`Grid_Generate`→`column/beam/wall_arrange`→`slab_arrange(SlabCreateInfo,cx/cy须int)`→`Floors_Assemb`→`DbModel_Assign()`→`Hi_AddToAndReadYjk(model).CreateYDB(目录,"dtlmodel.ydb")`。已有 `_build_station_yjkapi.py`(箱型车站)。
- **三ydb(实测)**：`dtlmodel.ydb`(YJKAPI CreateYDB headless 产) + `dtlCalc.ydb`(前处理计算产) + `Jccad_0.ydb`(基础筏板;**筏板 Raft 来自此,去掉则无底板**)。后两者需 **YJK 软件运行中**——可命令驱动不必纯手点: 计算序列 `yjk_setlayersupport/yjkspre_genmodrel/yjktransload_tlplan/_tlvert/yjkdesign_dsncalculating_all`(出 dtlCalc); `jccad_read` 重新读取上部数据(出初始 Jccad_0) + `JcDataFunc.JcRaftSlab_Def/App` 布筏板。详见 ⓪YJK KB `-workflow`/`-patterns`。
- **★需 YJK 开着的步 → 提示用户打开 YJK**：dtlCalc/Jccad/前处理计算/后处理 都需 YJK 运行中(用户打开工程)。两套驱动: 进程外 `YJKSControl.RunCmd`(先在 YJK 命令行输 `yjksipccontrol`) / 进程内 `YJKSCommandPy().RunCommand`+`yjks_pyload`(入口 `def pyyjks`)。dtlmodel 建模 + 筏板布置(JcDataFunc) 可纯 headless。
- **GFE 导入(ch10)**：`io.get_current().import_yjk(目录, yjk_para(43元整数), ['',''], True, '', False)` + `document.set_application_by_ui()`→自动产 SuperStru+构件集+截面+材料+配筋+工况。⚠ yjk_para 不能跨案例照抄(查 paths ch10/11/15)。
- ✅ 本机已替 5 dll+python310，`import YJKAPI` 实测 OK；换新机才需重做(关yjks.exe+用户授权,旧dll备份 `_dll_backup`)。

### A2 FreeCAD 入口
- 工具 `mcp__freecad__*`：create_document/create_object/edit_object/execute_code/get_view/get_objects/get_parts_list/run_fem_analysis。建几何走 `execute_code` 跑 Part API(makePolygon/Face/Shell/sewShape/makeCompound/makeLine/revolve/sweep/布尔)，出 STEP `comp.exportStep(path)`。
- ⚠ 运行前提：`mcp__freecad__*` 失败/超时 = FreeCAD GUI 没开或没激活 workbench → 提示用户**开 FreeCAD → Workbench 下拉选 "MCP Addon"**(起 RPC)。
- 无 GUI：headless `& "D:\FreeCAD 1.1\bin\freecadcmd.exe" 脚本.py`。
- session 无 `mcp__freecad__*` 工具(中途 add 要重启)→ 直连 RPC：`from freecad_mcp.freecad_client import FreeCADConnection; c=FreeCADConnection()`(localhost:9875); `c.ping()`/`c.execute_code(code)`。

### A3/A4 GFE 原生建 / 直导
draft 草图(add_line/arc/circle/polyline+约束+变换→export)→geoprim(extrude/cut/merge/common/split)；occ.brep_prim(make_box/sphere/cylinder/cone/torus)；隧道 `geotool.build_tunnel_shape`。直导 `io.get_current().open_geometry/open_inp/import_yjk`。

### B / GFE noGUI 调用（范式见记忆 `reference_gfe2026_nogui` + 在线 `paths`）
- 调用：`& "E:\GFE2026\program\PrePo.exe" "py-script=脚本.py"`（PowerShell 先 `$env:PYTHONUTF8=1`）。
- 脚本：`import GFE` + `import builtins as B`(环境遮蔽 set/round/abs，用 B.*)；坐标 `centre_of_mass` 返回 list；FACE=4/EDGE=6/SOLID=2。
- B3 网格 controller **必须给全** number_option(15键)+user_option+geom_to_type+generate_dim=3+auto_transfinite=False(缺键C++崩)。
- **调参重跑**：改脚本顶部参数(尺寸/土层/网格/工况)重跑 PrePo，脚本幂等(开头 delete_all)。改几何参数若涉结构→重跑 A1/A2 重出几何；只改 GFE 参数/工况→只重跑 B 脚本。

### B4/B5 挂接规则（objref；集合类型铁律）
- **gset 几何集**→截面`.elset_name`/BC`.set`/体力/生死单元`elemDel·Add`；**surface 表面集**→压力/Tie`first·second_surf`/接触/人工边界`art_bc.surface`；**nset 节点集**→集中力；**elset 单元集**→copy_mesh产物(结构面线S3/B31)/线荷载。
- 坑：截面/生死单元 `elset_name` 填几何集名也行(GFE网格后几何集≈同名单元集；土用几何集名/结构用copy_mesh elset 都实测成功)。完整查在线 `objref`。

### DWG → DXF（管线起点之一）
断面常是 DWG → **ODA File Converter**(免费 opendesign.com)转 DXF → FreeCAD `Import`/`importDXF` 提形拉伸。未装 → 提示装 ODA。

### 安装依赖（未满足主动提示+给命令）
FreeCAD程序(D:\FreeCAD 1.1) · freecad-mcp(pip+addon→`%APPDATA%\FreeCAD\v1-1\Mod`+`claude mcp add`,✓Connected) · YJK(D:\YJKS,✓) · ODA转DXF · GFE2026(E:\GFE2026,✓)。

## 与既有 skill 关系
`gfe-command-stream`(读 D:\GFE\GFE_KB 整库做深度建模/桥)侧重知识全量；本 skill 是**能力盘 + 端到端动手**：在线速查 + 多源建模 + GFE 处理 + 调参。
