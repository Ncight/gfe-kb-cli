# GFE 命令流知识库总索引
> 来源：D:\GFE\GFE_KB（gfe-command-stream skill 维护的命令流知识库）。本文件为 raw 检索源副本，2026-06-10 Fable 二审后刷新（ADR-0001：派生快照随主库可变）。

# GFE 命令流知识库（数据库索引）
> Claude 反编译 + 实测 GFE/PrePo 命令流的全部成果。2026-05-30 整理。
> 目标：用代码（命令流）参数化建模 + Claude 经桥无人值守驱动 PrePo。

---

## 这是什么 / 怎么用
GFE 的"命令流"= PrePo 内嵌 CPython 的 **pybind11 API**（非 Tcl）。本库把它的**文法（怎么写）+ 案例反推（怎么用、建了什么）+ 实时桥（让 Claude 直接驱动）**整理成一个可检索的库。

**三层定位**：
1. 不知道某命令怎么写 → 查 `01_API规格与文法/GFE_API_reference.md`（787 函数全签名）
2. 不知道某流程怎么串/某案例怎么建 → 查 `02_案例反推/`（章节理解 + synthesis + 引用关系）
3. 要让 Claude 实际操作 PrePo → 用 `03_工具脚本_Bridge/`（桥 + 反编译器）

---

## 01_API规格与文法/  — 命令流"文法"
| 文件 | 内容 |
|---|---|
| **GFE_API_reference.md** | ★主速查：787 函数全类型签名 + 519 属性 + 43 枚举 + 218 类，分 32 模块（另附 RTTI 453 C++ 类） |
| gfe_api_spec.txt | 自省原始 1607 符号清单（其中 78 条改模型函数为占位，无签名；全签名见 GFE_API_reference.md） |
| gfe_cpp_classes.txt | RTTI 反解的 453 个 GFE C++ 类（内部类型模型/架构） |
| GFE-对象引用关系总览.md | ★（用户撰）模块间引用关系：截面→几何集 / BC→集合(几何集/节点集,非表面集) / Tie→表面对 / Embed→集合+集合(embedded_names列表/host_name) / artbc→表面集+形心 / Case→步+BC+生死单元；含施工步生死单元范例 |
| GFE_manual_diff.md | binding vs 191页命令流手册 diff：手册没讲的隐藏命令（draft 草图器/mesh_data 底层/CDP 字段等）。⚠ diff 基准为 v2025 手册（2.15.2）；v2026_0302（3.4.0）已正式文档化 draft/CDP 等，隐藏清单仅对旧版手册成立，引用前对照 _audit/phase1/GFE-Cmd__merged.md 修订记录 |
| manual_text.txt | 命令流手册 v2025 全文（v2025 原 PDF 已被 v2026_0302 替换，现行 PDF 与本 txt 版本错位，新增 API 以 v2026 为准） |

**建模文法核心**：① 每模块 `X_mgr()` 单例；② 构造对象→设属性(def_readwrite)→`mgr.add(obj)`；③ 工况装配 `case.set_bcs/set_vload/set_artbc/set_fieldReqs/set_elemAdd/set_elemDel(步名,[名])`。

## 02_案例反推/  — 案例信息反推（怎么用 / 建了什么）
| 文件 | 内容 |
|---|---|
| **章节理解总览.md** | ★15 章典型案例分类理解（结构/地震SSI/施工生死单元/特种动力）+ 跨章②语义 |
| 真实工程_400galW7-VC_解析.md | ★用户真实工程反编译解析（三向ElCentro弹塑性SSI/16层Davidenkov土/桩基/β=0） |
| _synthesis_ch10_抗震地铁站.md | 地铁站抗震 SSI 全流程（手册+dump+API 三源合成） |
| _synthesis_ch11_13_15_动力SSI.md | 地上地下抗震 / 反应位移法 / 列车振动 + 动力SSI通用骨架 |
| 案例操作手册_全文.txt | 实际案例操作手册 v2025 全文（原 PDF 在 D:\GFE\手册资料\GFE-实际案例操作手册v2025.pdf） |
| GFE2026 官方命令流 py×13 | E:\GFE2026\典型案例与教程\（v3.x 金标准，raw 快照 GFE2026-CM-*）——路径文件已据其升级 [官方实证 v3.x] |

## 03_工具脚本_Bridge/  — 工具 + 实时桥
| 脚本 | 作用 | 用法 |
|---|---|---|
| **gfe_decompile.py** | ★模型反编译器：读当前 PrePo 模型全状态→dump | 命令框 `MODEL='xx'; exec(open(r"D:\GFE\gfe_decompile.py",encoding="utf-8").read())` → D:\GFE\decomp\xx.txt |
| gfe_introspect.py | API 自省（产 gfe_api_spec.txt） | 同上 exec |
| gfe_fill_mutating.py | 改模型函数"7哨兵逼签名" | 同上 |
| gfe_probe_assembly.py | 装配点探针（构造器/连接器/列车荷载type/case回读） | 同上 |
| build_model.py | ★参数化建模脚本（PARAMS 区改细节重跑；含土材料/一维土层/三维土+占位块） | exec；结尾 File→Save 存 .pre |
| send.py | ★桥：把命令送进 PrePo REPL（自动点框+剪贴板粘贴+回车，无需手点） | 见下"桥工作流" |

### 桥工作流（Claude 无人值守驱动 PrePo）
1. PrePo 须运行（窗口 `GFE-PrePo`）；pywinauto/pyperclip 系统 py3.14 已装
2. 多行代码写 `D:\GFE\bridge\cmd.py`；`D:\GFE\bridge\next.txt` 放单行 `exec(open(r"D:\GFE\bridge\cmd.py",encoding="utf-8").read())`
3. 跑 `py D:\GFE\bridge\send.py` → 在 PrePo 主线程执行；命令自写结果到文件 → Claude 读回自审
4. 坑：next.txt 用无BOM写（PS Out-File utf8 会加BOM致SyntaxError）；send.py 读用 utf-8-sig；REPL 残行用 send.py 内置"先回车冲掉"；多行必须走 cmd.py（勿直接粘多行进 REPL）
> **live 副本**在 D:\GFE\bridge\（send.py/next.txt/cmd.py 实际运行处）；本库为参考副本。

## 04_状态dump/  — 模型状态快照（★按管理器切分）
每个 dump 一个子文件夹 `04_状态dump/<dump名>/`，内含：
- **`_index.md`** — 该模型按管理器的索引表（管理器 | 对象数 | 行数 | 文件 | 对象名预览）+ 空管理器清单
- **`<模块>_<getter>.txt`** — 每个非空管理器的内容单独成文件（如 `soil_soil_manager.txt`/`step_step_manager.txt`/`material_mat_mgr.txt`）

→ 查大模型某一块不用翻几万行：先看 `_index.md` 定位，再开对应小文件。例：真实工程土层 = `400galW7VC/soil_soil_manager.txt`(0.4KB)，而非整 65735 行。
- 已切分：400galW7VC(21管理器) + ch01-07/10/1112(ch11+12 合用)/14/15。原始整 dump 在 `D:\GFE\decomp\`。
- 重新切分工具：`03_工具脚本_Bridge/split_dump.py <dump.txt> <输出目录>`（纯文本，本地跑，不碰 PrePo）。
`_dump清单.txt` = decomp 全 dump 行数/大小清单。

---

## 关键事实速记
- 单位制随模型：m-t-kPa（E~kPa）或 mm-t-MPa；按 density/E 反推
- 阻尼 β=0（显式动力恒定；隐式分析 β 可非零，见隐式手册第六章）；本构 混凝土 user_type=1 / 土 user_type=2(Davidenkov)
- 动力步 dynamic_explicit_step + mass_scaling(type=1,freq=100,target_time 2e-4~3e-5，按章不同：粗 2e-4 / 细 5e-5~3e-5)，modal_damping=None
- 地震输入 vibration.vibra_load(amp_bottom_x/y/z, is_outcrop, pwave_dir=2, soil)；人工边界 artbc.art_bc(structure, surface)
- ⚠ 三向 *Wave：Amp-X/Y/Z 点数必须一致，否则 0xC0000374 堆损坏
- ⚠ 静→动 -prevdb 接力存在 RF 场污染与初始加速度震荡，见 gfe-static-dynamic-diagnosis
- **限制**：命令流无 save API（.pre 存盘只能 GUI File→Save）；裸 python 不能 import GFE（须 PrePo 宿主）；几何 mgr 层 dump 仅名级（decompiler 防崩策略）；shape 级感知可走 geo_mgr.find(名).shape() + geotool(get_shape_box/centre_of_mass/children/get_id_by_shape)，大模型深读稳定性待实测
- 几何：草图器 `draft.get_current()→set_normal→add_*→fill_selected→export` + `geoprim`(extrude/cut/translate/make_array) + occ.brep_prim 基本体
- 记忆索引：[[reference_gfe_command_stream]] [[reference_gfe_live_bridge]]

---

## 二审产物（2026-06-10 Fable 5，详见 docs/二审执行蓝图.md）
| 文件 | 内容 |
|---|---|
| **易错清单_LLM驱动GFE建模.md** | ★红线十诫 + 12 域 149 条防错条目 + Opus 实证 8 错误模式 + 50 待实测——任何 LLM 驱动 GFE 前必读 |
| **能力矩阵.md** | ★1331 项能力 × 自动化三层（①命令流1032/②半自动67/③纯GUI223），含自动化盲区总结 |
| 02_案例反推/路径_ch01~15_*.md | 15 章案例可复现建模路径（命令流步骤链，dump 实证，断点标注；11 章已 GFE2026 官方 py 实证） |
| _audit/phase3/变更总表.md | 二审 328 条修正账目 + 待实测 36 + 报批 19（对象引用关系总览待用户定夺） |
| _audit/phase1/*__merged.md | 8 本手册全文精读真值底座（含 PDF 直读补块），审计仲裁锚点 |
| CONTEXT.md + docs/adr/0001 | 术语表 + raw 快照可变性决策 |
