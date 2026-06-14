---
title: "GFE-UserGuide-2026附录 — 用户手册 v3.4.3 作业管理器 + 五大附录 + 版本修订史"
type: manual
software: GFE
tags: [gfe, manual, prepo, inp, inpx, yjk, batch, job-manager, file-system]
sources: ["[[GFE-UserGuide-2026-附录.src]]"]
version: v3.4.3（2026.3.30）
publisher: 广州颖力科技
created: 2026-06-14
updated: 2026-06-14
---

> [[GFE]] 用户手册 **v3.4.3（2026.3.30）** 中用户重点标注章节的结构化参考：§1.15.3 作业管理器（含批处理参数全表、重启动、静力转动力）+ 附录一~五（文件系统、INP 关键字、**新增的 INPX 关键字**、YJK 命名规则、参考文献）+ 修订记录。补充并更新 [[GFE-UserGuide]]（旧版基于 v2025 2025.09），二者配合使用。章节号自 v2025 起有迁移：作业管理器由原 §1.15.4 改为 **§1.15.3**；YJK 命名规则因插入 INPX 附录由原「附录三」后移为 **「附录四」**。

## 版本修订史（修订记录摘要）

GFE 用户手册从 v0.48.0（2022.9，首次正式发布）演进到 **v3.4.3（2026.3.30）**。[[GFE-UserGuide]] 旧摘要对应 **v3.0.0（2025.09）**；以下为 v3.0.0 之后的关键增量（决定本库需要更新的内容）：

- **v3.4.3（2026.3.30）**：[[粘弹性人工边界]]补充说明、建议网格尺寸计算公式补充、波速计算说明。
- **v3.4.2（2026.3.23–3.26）**：新增静力分析/隐式动力分析线性计算说明；冲击波 B31 单元说明；**新增 INPX 关键字说明附录（即附录三）**；三方向刚度特殊相互作用截图 + 特殊相互作用容差说明；通用接触面面接触说明调整；HSS 参数更新。
- **v3.4.0（2026.2.5–3.13）**：新增 1.13.2(11) 热固耦合分析步、1.13.2(10) 渗流分析步、1.11.19 车轨耦合列车荷载、1.5.3(4) 外框扫掠；补充大量命令行参数（intersect / py-script / check-level / case-insensitive / hdf5 / coup-temp-penalty / splitsc / fix-dt / mergestep / include-mat / fake-material）；附录二新增单元输出关键字截面点说明；新增 *boundary 特殊自由度解释；更新接触摩擦/cohesive 说明。
- **v3.3.0（2026.1.7–2.4）**：1.15.4 作业管理器补充 (7) 重启动计算、(8) 静力转动力；1.11 补充边界荷载传递逻辑；2.6.2 层间剪力补充 NFORC 说明；更新批处理参数 -scotch。
- **内部测试（2025.10）**：特殊相互作用新增「支持的求解器类型」表；**删除附录二 Cohesive Behavior 支持**。
- v3.0.4（2025.11）：修正空间分布文字错误。

## 作业管理器（§1.15.3，原 §1.15.4）

创建作业需设「作业名称 / 模型名称 / 工况 / 目录 / 计算核心（GFEXC/GFEXG/GFEXN）/ GPUID」，并有「高级」「移除单元」两个展开项。作业条目支持编辑/复制/删除、写出 INP（不计算）/提交/监控/结果/中断。选 **GFEXN** 时若有分析步未开几何非线性会弹窗，确认后强制全开（GFEXN 一般推荐打开几何非线性）。

- **(3) 导出计算文件**：界面提交计算后自动导出 inp + inpx；若模型由 ydb 导入，**还会自动导出 gjdy 文件**。命令行提交则需先有 inp + inpx。
- **(4) 移除畸形单元**：按长宽比 / 偏斜度 / 长度(1D) / 面积(2D) / 体积(3D) 设阈值，达标单元写出 inp 时被注释掉、不参与计算。单元质量分级参考：长宽比「非常差>20 / 较差5~20 / 普通2~5 / 较好1~2」。
- **(5) 高级**：①写出 Vuel——写 inp 时把人工边界单元写入 inp，并把场地地震动输入生成 vload 文件；②列车荷载写入 inpx（默认勾选，不勾则以节点力形式写入 inp）；③写出 SPH xml——把 SPH 流体动力工况写成 xml 求解文件。
- **(7) 重启动计算**：仅批处理，用 `inps=` 指定一个文本文件（每行一个 inp 路径，相对路径相对 inps 所在目录）。程序把多个 inp **合并为一个含多 step 的 multi-steps.inp** 再算——本质是把重启动转成多分析步，**不支持中途暂停后再续算**。
- **(8) 静力转动力**：仅批处理，在 inpx 加 `*Param2 / STATIC_TO_DYNAMIC / *End`，支持多 step。分析步若指定质量缩放则按其步长，否则按静力分析步初始步长做质量缩放（`*Static` 行：步长, 总时长, 最小步长, 最大步长，后两位暂未用）。

### 批处理参数（PrePo.exe -daemon …）

调用范式：`PrePo.exe -daemon -dat <inp路径> -gfedir <结果目录> [选项]`。多 GPU 需在批处理文件首行加 `CUDA_VISIBLE_DEVICES=0,1,2,3`。

**必填**：`-daemon`（不启界面）、`-dat`（inp 路径）、`-gfedir`（结果目录，手册原文偶误印 -gfeidr）。

**求解器选择**：`-cpu`（GFEXC 旧 CPU 求解器）/`-standard`（GFEXN 隐式求解器），二者互斥；都不给则默认 **GFEXG（显式动力）**。

**常用可选**：`-prevdb`（前置 db 路径，静力接动力做地应力平衡）、`-split N`（仅 Linux，多 GPU 分区数）、`-scotch x|y|z|xy|…`（分区切割方向，须配 -split，空值默认 xy）、`-minElemVol`（体积/面积小于该值的单元预处理移除，1D 不处理）、`-cutquad`（曲率大于阈值的四边形拆成两三角形，默认 0.2）、`-config`（config.txt 路径）、`-solvemethod 0|1|2`（线性方程组库：0 Pardiso 默认 / 1 Mumps / 2 AMGX）、`-range a-b`（每个 *Element 只读第 a~b 行）、`-debug`（调试，开发用）。

**新式选项（不带「-」，值用「=」接驳，如 `include_inner_face=Surf-1`）**：
- `case-insensitive`：解析 inp 忽略大小写，后处理名称全转大写。
- `inps=`：重启动计算必填，指定 inps 文件路径。
- `py-script=`：**不打开界面执行 GFE 命令流**（嵌入式 Python），一般不与其他选项联用 — 与 [[GFE-Cmd]] 命令流的无界面入口。
- `check-level=None|Warning|Error`：数据检查级别，默认 Error。
- `hdf5`：场输出各帧存 FieldOutput 文件夹内 h5（每帧一个），边算边看时用。
- `coup-temp-penalty=`：手动指定热固耦合分析中绑定约束罚系数（默认按导热系数自动算，与导热系数正相关、与单元尺寸负相关）。
- `splitsc`：把复合材料厚壳单元按截面属性拆为多层实体单元。
- `all_exterior`：无论 inp 是否含通用接触，总把通用接触外表面信息传给求解器。
- `include_inner_face[=elset]`：把（指定单元集 / 全部）单元面加入通用接触。
- `nomiddlenode`：通用接触表面信息中考虑二阶四面体中间节点（手册自承名称易误导）。
- `splittet2=E,σy` / `splittet2-prefea=`：二阶四面体（弹塑性且模量、屈服应力达阈值）拆为 4 个六面体；prefea 复用拆分前通用接触面信息。
- `tmp-soils`：纯渗流分析计算模式。
- **XM 项目专用**：`intersect`（须配 splitsc+inps）、`fix-dt`（多分析步取最大步长统一）、`mergestep`（合并单 inp 多分析步为一）、`include-mat`（转换多分析步时保留 *include 格式）、`fake-material`（db 写假材料防泄密）。
- 开发/废弃：`test-exchange`、`searchstep`（已废弃）。

## 附录一 GFE 的文件系统（10 类文件）

| 后缀 | 名称 | 内容 |
|---|---|---|
| `.pre` | 前处理文件 | 保存模型后产生，含几何/材料/荷载/边界/网格全套数据 |
| `.stp`/`.step` | 几何信息文件 | CAD 产出的几何，可直接导入生成模型 |
| `dtlmodel.ydb`+`dtlCalc.ydb` | YJK 模型目录 | 盈建科产出，导入生成结构模型（几何+材料） |
| `.gmat` | 材料信息文件 | GFE 导出的二进制材料库，导入后追加到当前模型材料，重名自动加后缀 |
| `.inp` | 任务文件 | 计算输入，格式同 Nastran Inp，文本可编辑，含网格/材料/截面/荷载/分析步 |
| `.inpx` | 任务补充文件 | 与 inp 一并生成，补充 Nastran 不支持的 GFE 特有功能（构件偏心、地震荷载、人工边界、工况、空间分布、包络输出等） |
| `.feasta` | 监控信息文件 | 求解状态文件，记录作业管理器「监控」输出：进度/耗时/中止/报错原因 |
| `.db` | 后处理文件 | 结果数据，后处理可视化打开 |
| `.gjdy` | YJK 几何对应文件 | YJK 模型写 inp 时随同写出，记录平移旋转信息 + 几何构件对应单元信息 |
| `.chklog` | 数据检查文件 | 提交后预处理阶段在结果目录生成 |

## 附录二 GFE 支持的 INP 关键字（ABAQUS 子集）

仅列 GFE 当前版本支持的 INP 关键字范围与简释，功能详见 Abaqus Keyword Reference（手册简称「A」）。分类：**(1) 有限元网格**（*Node / *Element / *Nset / *Elset / *Surface，Surface 目前仅支持 type=element）；**(2) 材料**（*Density、*Damping α/β、*Elastic 支持 isotropic 与 lamina[仅显式]、*Plastic 硬化支持 Isotropic/Johnson-Cook、*Concrete Damaged Plasticity 系列、*Creep[law=strain/time]、*Hyperelastic[N 1~6]、*Viscoelastic[time 仅 prony / frequency 仅隐式 tabular]、*User Material、孔隙流体相关）；**(3) 截面属性**（*Solid/Shell/Beam Section + *Section Controls，GFE 写出 inp 会自动建 ENHANCED 沙漏控制并引用）；**(4) 边界条件与荷载**（*Boundary 支持 velocity/acceleration + amplitude、*Cload/*Dload、*Mass、初始条件 *Initial Conditions: stress/velocity/pore pressure/ratio）；**(5) 相互作用**（*Tie[position tolerance]、*Contact/通用接触、*Surface Interaction、cohesive 能量型、*Incident Wave[air/surface blast + conwep]、*Spring/*Dashpot、*Connector Behavior、MPC/*Coupling 含 rigid）。增量：v3.0.0 新增 *User Material 各类材料说明、热固耦合关键字 *Conductivity/*CFlux/*Coupled Temperature-Displacement；2025.10 **删除 Cohesive Behavior 支持**。

## 附录三 INPX 文件关键字（v3.4.2 新增附录）

inpx 是 inp 的补充文件，承载 GFE 特有、Nastran Inp 不支持的功能。该附录首次系统化列出其关键字：

- `*NameList`（name）：定义名称列表，数据行每行一个名称。
- `*Material`（name；子关键字 `*Johnson cook rate`、`$ConcreteRate`）：定义材料的 Johnson-Cook 率效应、混凝土率效应。
- `*Rload`（name / type / ref）：定义频响分析动态荷载，ref 引用静态荷载名。
- `*Envelop Ouput`（method / step）：定义包络输出（手册原文拼写 Ouput）。
- `*Custom Property`（type / parameters / surfaces）：**定义特殊相互作用**（类型、刚度/容差等参数、作用表面）。
- `*Mat Test Data`（name）：定义材料非线性曲线（试验数据反算本构）。
- `*Surface`：定义[[粘弹性人工边界]]。
- `*Layer`：定义地震场地反应土层信息。
- `*Wave`：定义地震场地反应波动输入信息。
- `*Param`：定义人工边界 + 地震场地反应参数。
- `*Param2`：定义其他全局参数（如静力转动力的 `STATIC_TO_DYNAMIC`）。
- `*TrainLoad` / `*Train` / `*Track` / `*Force`：[[列车荷载]]——分别定义列车荷载、列车数据、轨道点、轨道点上的力，须同时使用。
- `$TrainLoad-Coupling`：定义车轨耦合列车荷载（v3.4.0 新增）。
- `*WATER PRESS`（NAME / SURF）：定义水压力（动水压力）。
- `*Modal Damping`（Modal db / nset）：定义显式动力分析模态阻尼（模态 db 路径 + db 内节点集）。
- `*End`：结束上一关键字，可嵌套。

## 附录四 YJK 数据命名规则（原附录三）

[[YJK]]/PKPM 导入后截面、荷载、附加质量按此规则自动命名：

- **工况**：`Dead` 恒载、`Live` 活载、`gk1`~`gk4` 自定义工况、`Comb` 组合工况（各单工况×组合系数求和，系数同 YJK 重力荷载代表值组合系数）。
- **荷载**：`LL_BEAM` 梁竖向线荷载、`LL_HORI` 梁水平线荷载、`LL_COL` 柱水平线荷载、`P_SLAB` 板压力、`P_WALL` 墙压力、`FV` 点集中竖向荷载、`FH` 点水平荷载。
- **附加质量**：`M_Point` 点质量、`M_BEAM` 梁质量、`M_SLAB` 板质量。
- **截面/厚度命名**：以标识符开头 + 后缀集合序号，例 `WallC_Conc800_C35_1576`、`Beam_H500x200_Sub0_Q355_385`。
  - 构件标识符：`WallC` 剪力墙、`WallB` 墙梁(壳模拟连梁)、`Slab` 板、`Beam` 梁、`Col` 柱、`Brace` 斜撑、`Raft` 筏板、`Pile` 桩。
  - 厚度材料标识符：`Conc` 混凝土、`St` 钢板。
  - 截面形状标识符：`REC` 矩形、`H` 工字钢、`D` 圆、`CROSS` 十字、`BOX` 箱形、`PIPE` 管形、`TRAPE` 梯形、`CFT_PIPE`/`CFT_BOX` 圆/方钢管混凝土、`REC_H`/`REC_BOX`/`REC_CROSS` 内置型钢的矩形型钢混凝土、`D_H`/`D_PIPE`/`D_CROSS` 内置型钢的圆形型钢混凝土、`L`/`T` 形等。
  - 形状标识符后跟尺寸：矩形/箱形「宽×高」、圆「直径」、管「直径×壁厚」、工字钢「高×宽」、T 形「宽×高」。
  - 子截面序号 `Sub`，第 0 个截面为外轮廓子截面。

## 附录五 参考文献

手册中为占位空标题，**正文为空**（无条目）。

## 坑与注意
- **章节/附录号迁移**：作业管理器 §1.15.4→§1.15.3；YJK 命名规则 附录三→附录四（因 v3.4.2 插入 INPX 附录占了「附录三」）。引用旧库 [[GFE-UserGuide]] 内的节号需对照本页。手册正文 §1.15.3 内的配图题注仍残留旧编号「图 1.15.4-x」（手册自身未刷新）。
- **重启动不是真重启动**：本质转成多分析步 inp，不能中途暂停续算。
- **静力转动力须手改 inpx**（`*Param2 STATIC_TO_DYNAMIC`），仅批处理。
- **批处理求解器默认 GFEXG**（不给 -cpu/-standard 时）；与界面创建作业默认不同，提交脚本须显式确认。
- `py-script=` 是命令流无界面驱动的官方入口，可与 [[GFE实时桥]] / 总工监工类无人值守方案配合。

## 交叉引用
- 主手册：[[GFE-UserGuide]]（v2025 全流程 GUI 参考，本页为其 v3.4.3 红框 delta 补充）
- 命令流：[[GFE-Cmd]]（py-script 无界面执行的嵌入式 Python API）
- 软件/实体：[[GFE]]、[[YJK]]、[[PrePo]]
- 概念：[[粘弹性人工边界]]、[[列车荷载]]、[[GFE对象引用关系]]
