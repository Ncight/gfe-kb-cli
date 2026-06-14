# GFE 命令流案例反推（章节理解 + 动力 SSI synthesis + 真实工程）
> 来源：D:\GFE\GFE_KB（gfe-command-stream skill 维护的命令流知识库）。本文件为 raw 检索源副本，2026-06-10 Fable 二审后刷新（ADR-0001：派生快照随主库可变）。



---
# ===== 章节理解总览.md =====

# GFE 典型案例与教程 — 全章节理解总览
> 依据：实际案例操作手册 v2025（D:\GFE\manual_case_text.txt）+ 各章 .pre 反编译 dump（D:\GFE\decomp\）
> 标注：✅有dump反编译  ◎仅手册（无dump/打不开）

## 章节一览（15 章）

| 章 | 案例 | 类型 | 关键模块/特征 | dump |
|---|---|---|---|---|
| 1 | 球铰支座 | 结构静力+模态 | material/section/boundary/step(模态+静力)/case；几何含 qiujiao(球铰)/zhizuo(支座) | ✅ ch01_Chapter1 |
| 2 | 钢骨混凝土 | 结构静力 | + **interaction.embed**(钢筋笼嵌入混凝土；钢骨经布尔合并共节点)；多截面 | ✅ ch02_section |
| 3 | 华夫板框架 | 频响分析(稳态动力) | 框架+华夫板(wafer)；elset/nset(基于网格)；steady_dyn_step、直接法、集中力虚部激励 | ✅ ch03_wafer |
| 4 | 核电站结构 | **地震 SSI** | **amplitude/soil/vibration/artbc** + interaction；核电厂房+场地反应 | ✅ ch04_section |
| 5 | 非均匀场地 | **地震 SSI** | soil/vibration/artbc；非均匀场地建模重点 | ✅ ch05_section |
| 6 | 邻近建筑基坑开挖 | 施工模拟 | soil/interaction + **生死单元(Model Change)**；12394 行(大) | ✅ ch06 |
| 7 | 锚杆隧道施工 | 施工模拟 | soil/interaction；隧道开挖+锚杆+衬砌施工步 | ✅ ch07 |
| 8 | SPH 小球落水 | 流体动力 SPH | sph 模块 | ◎ 无.pre |
| 9 | SPH 水桶晃动 | 流体动力 SPH | sph 模块 | ◎ 无.pre |
| 10 | 抗震-地铁站 | **地震 SSI(弹性+弹塑性)** | 完整时程：YJK导入→土→相互作用→人工边界→场地反应→工况；弹塑性加 Davidenkov+地应力平衡 | ✅ ch10（见 _synthesis_ch10） |
| 11 | 抗震-地上地下结构 | **地震 SSI** | 同 ch10 范式；x 向、3 步弹塑性 | ✅ ch1112_plastic（见 _synthesis_ch11_13_15） |
| 12 | 施工模拟-地上地下综合体 | 施工模拟 | 生死单元 | ✅(同 ch1112 文件夹) |
| 13 | 反应位移法 | **地下抗震(拟静力)** | 基床系数+主体/地连墙+拟动力+惯性力/土层剪力/相对位移+**反应位移助手**(GUI) | ◎ .pre 打不开（见 _synthesis_ch11_13_15） |
| 14 | 爆炸 | **冲击动力** | shock_wave(CONWEP 冲击波属性/荷载) + amplitude(地震波/墙荷载，沿用前章模型)/soil/vibration/artbc；21063 行(大) | ✅ ch14_plastic |
| 15 | 列车振动 | **移动荷载动力** | 草图器建隧道/道床/轨道 + 连接器(道床-轨) + 列车荷载(boundary type=9) | ✅ ch15（见 _synthesis_ch11_13_15；已用桥自主复刻骨架） |

## 按技术分组（便于检索范式）
- **纯结构静力/模态**：ch1(球铰+模态)、ch2(钢骨嵌入)
- **频响(稳态动力)**：ch3(华夫板，steady_dyn_step 直接法)
- **地震时程 SSI**：ch4(核电)、ch5(非均匀场地)、ch10(地铁站)、ch11(地上地下) → 范式：YJK/几何 → 土材料(Davidenkov) → soil.soil 一维土层 → box_builder/data_builder 三维土 → 平移/裁剪 → tie/embed → artbc 人工边界 → vibration 地震场地反应(amp_bottom_x/y/z) → 网格 → 工况(弹性 Initial→Dyna；弹塑性 Initial→Static地应力平衡→Dyna)
- **施工模拟(生死单元)**：ch6(基坑开挖)、ch7(锚杆隧道)、ch12(综合体) → Model Change：case.set_elemDel/set_elemAdd(分析步名, [几何集名列表])；坑：土层初始即激活不可再 elemAdd（见 [对象引用关系总览 §8]）
- **特种动力**：ch13(反应位移法-拟静力)、ch14(爆炸-冲击波)、ch15(列车-移动荷载)、ch8/9(SPH 流体)

## 关键 ② 语义（跨章归纳，已实测/反编译确认）
- 单位制 **m-t-kPa**（E 单位 kPa，ρ t/m³，C30 E=3e7 kPa=30GPa）；ch01 教学用 mm-t-MPa——**随模型变，按 density/E 反推**；例外：SPH 强制 SI(m)；CONWEP 强制 t-m-kPa（硬约定，不可反推自选）
- 阻尼 **β=0 恒定**（显式动力稳定性；material.damping params=[α, 0]）
- 本构：混凝土 user_type=1、土 **user_type=2(Davidenkov)**；material.entries 为条目列表（density/damping/elastic/plastic/user/mohr_coulomb…），顺序随材料类型不固定，按类型匹配不要按下标
- 动力步 dynamic_explicit_step：mass_scaling(type=1, frequency=100, target_time 地震 2e-4~3e-5（ch05 实测 3e-5）/列车5e-5)，period=分析时长，modal_damping=None
- 地震输入 vibration.vibra_load：amp_bottom_x/y/z(可三向)，is_outcrop=True(露头基岩)，pwave_dir=2(Z)，引用 soil 一维土层名
- 人工边界 artbc.art_bc：structure + surface(土边界面集)；structure=形心参考几何，案例 dump 中 ch10 指土体、ch15 指主体结构（手册待仲裁⑨），复刻时按目标 .pre 反查
- 工况 case：弹性 Initial→DynamicStep；弹塑性 Initial→StaticStep(地应力平衡,动力步加AllGrav)→DynamicStep；调幅目标地表峰值加速度（单位 m/s²，勿按 gal/g 填）案例值 1.5（c06）/ 2.2（c11）


---
# ===== _synthesis_ch10_抗震地铁站.md =====

# 第10章 抗震分析-地铁站 · 理解版重建
> 三源合成：操作手册(意图/顺序/含义) + ch10.txt dump(精确状态/数值) + 命令流API(v2026 §8.1 范式+签名, PDF p169-180; 旧版手册编号 §7.1, KB 统一用 v2026 章号)。
> 标注规范：✅已证(手册或dump直接给出) ｜ 🟐推断(领域知识/范式外推, 需实跑确认) ｜ ⚠未确认(API调用名/参数待查)

## 0. 模型概况（来自 dump，✅）
- 几何 3 体：`SuperStru`(上部结构)、`BasementBoundary`(地下室外轮廓,不参与计算)、`Soil-1`(三维土体)
- 单位制：**m-t-s（→ kN/kPa）**——C30 elastic.params=[3.0e7, 0.2] 即 E=3e7 kPa=30 GPa、density=2.5 t/m³；**注意与 ch01 的 mm-t-MPa 不同，单位随模型变，务必按 density/E 反推**
- 15 材料：混凝土 C1/C2_Mat30/35/60、钢筋 HRB400(E=2e8 kPa)、钢 Q390(E=2.06e8)、**7 土层 4-3/5H-2/6H/7H-A/7H-B/8H/9H**(E 从 155 MPa 递增到 17.9 GPa)
- 214 集合(StoryDrift/floor0-6 构件/Beam_*/Col_*/Pile_*/Wall*/Slab*/jiegou/SuperStru-ALL/Soil-1-Layer1-7/soil)、154 截面（property_beam×117 / property_shell×30 / property_solid×7；shell 例：thickness/mat_name/type=3）

## 1. 弹性分析工作流（§10.2-10.15）

| # | 手册步骤(意图) | dump 实测状态 | 命令流 API 映射 |
|---|---|---|---|
| 1 | §10.3 导入 YJK 模型(几何+荷载+工况自动生成) ✅ | SuperStru 几何 + 214 集合 + Dead_M/Comb_M 荷载 + Dead/Live/Comb 工况均来自导入 | `io.get_current().import_yjk(path, para_int[43], ['',''], True, '', False)`(v2026§8.1(旧版§7.1) 实证；para_int 为 **43 元**整数列表，§6.4.1 与 §8.1 示例取值在第 4/5/7/37 位不同、不能跨场景照抄) ✅ |
| 2 | §10.4 导入土体材料(.gmat) ✅ | 7 土层材料 4-3…9H | gmat 导入：手册 v2026 §6.4.5 有 `io.import_mat(u8path)`→返回材料名**列表**（PDF p162）；⚠本机自省 spec 未见该 API，待实测版本；或逐个 `mat_mgr().add(material with entries=[density,elastic])` 复现 |
| 3 | §10.5 创建一维土层(层数/深度/材料/基岩, 算P/S波速) ✅ | `soil.soil`: depth=[4.72,9.5,11.5,9.5,1.9,5.1,40.0], materials=['4-3'…'9H'], bedrock_mat='9H', depth_dir=2 | `o=soil.soil(); o.depth=[...]; o.materials=[...]; o.bedrock_mat='9H'; o.depth_dir=2; soil_mgr().add(o)` ✅(v2026§8.1(旧版§7.1)同构) |
| 4 | §10.6 快速建土(输入长宽→三维土块) ✅ | 生成 Soil-1 几何 | `b=GFE.soil.box_builder(); b.set_height(depth,depth_dir); b.set_parameter(L,W); shape=b.build()` + `data_builder`(v2026§8.1(旧版§7.1)) ✅ |
| 5 | §10.7 土体定位(两次平移:形心对齐+埋深4m) ✅ | Soil-1 就位 | `geoprim.builder().translate(['Soil-1'], vec)`；埋深 `translate(['Soil-1'],[0,0,4])` ✅(v2026§8.1(旧版§7.1)同构;⚠这里±方向/4m符号需按坐标核) |
| 6 | §10.8 土体裁剪(布尔:土 cut 地下室轮廓) ✅ | Soil-1 被挖出基坑 | `geoprim.builder().cut('Soil-1', ['BasementBoundary'], True)` ✅(v2026§8.1(旧版§7.1)实证) |
| 7 | §10.9 相互作用:绑定+嵌入 ✅ | tie ×20(soil-struct 绑定)、embed ×1(Embed-1：embedded=**floor1-AllCol**，host=集合 'soil'；手册截图 OCR 写 floor0-AllCol 与 dump 不一致，按裁决序实测优先) | tie: `contact_pair.search_face('Soil-1','SuperStru',tol)`→`geometry_surface`→`surface_pair`→`tie_mgr().add`(v2026§8.1(旧版§7.1)实证)；embed: 已证——embed 类 6 属性(embedded_names/exterior_tolerance/host_name/id/name/roundoff_tolerance)，构造后赋属性、`embed_manager().add(obj, inner=False, auto_name=False)` 即可(gfe_api_spec.txt 行 384-393) |
| 8 | §10.10 人工边界(先建土边界表面集→转单元集→建artbc) ✅ | `artbc.art_bc`: structure='Soil-1', surface='soil_boundary', centered=False | 🟐 先 `surface_mgr().add(soil_boundary 面集)`→`o=artbc.art_bc(); o.structure='Soil-1'; o.surface='soil_boundary'; artbc_mgr().add(o)` 已证：art_bc 类 5 属性(center/centered/name/structure/surface)+`artbc_mgr().add(obj, inner=False, auto_name=False)`(gfe_api_spec.txt 行 38-47)；GUI 行为等价性待实跑 |
| 9 | §10.11 地震场地反应(幅值函数预设地震动 + 一维土层→场地反应; **仅 y 向**, 中震, 时程) ✅ | `vibration.vibra_load`: amp_bottom_y='25_RH1TG025_(RenGong_T_025)_y_Ci', amp_bottom_x/z='', soil='Soil1D-1', is_outcrop=True, pwave_dir=2, input_loc=-1, level=0 | `amp_mgr().add(预设地震动幅值)`；`o=vibration.vibra_load(); o.soil='Soil1D-1'; o.amp_bottom_y='<amp名>'; o.is_outcrop=True; o.pwave_dir=2; vib_mgr().add(o)` 🟐 |
| 10 | §10.12 网格(土体四面体 size≈3, 结构六面体 size≈1, BasementBoundary 不划) ✅ | mesh: SuperStru/Soil-1 已划 | `gen=mesh_generator.generator(); c=mesh_generator.controller(); c.user_option={'GFE.DefaultSize':3.0,...}; c.generate_dim=3; gen.mesh(['Soil-1'],c)` 土;结构同法 size=1 ✅(v2026§8.1(旧版§7.1)实证) |
| 11 | §10.13 工况(Initial 加 Comb_M 附加质量; DynamicStep 加 地震场地反应+人工边界+场输出) ✅ | `case 'Case-1'`: steps=['Initial','DynamicStep'] | `o=case.case(); o.name='Case-1'; o.steps=['Initial','DynamicStep']; o.set_bcs('Initial',['Comb_M…']); …(挂 artbc/vibration/输出); case_mgr().add(o)` 已证 setter 具名映射：人工边界挂 `set_artbc('DynamicStep',['ArtBC-1'])`、场地反应挂 `set_vload('DynamicStep',['VibLoad-1'])`、场输出挂 `set_fieldReqs(…)`（签名均 (步名, [对象名])，gfe_api_spec.txt 行 118-125）；实跑验证语义为可选项 |
| 12 | §10.14 提交作业(GFEXC=CPU / GFEXG=GPU) ✅ | — | 作业层不在命令流;求解器 `GFEXG.exe -db <model.db>`(已知) |

**分析步**(dump,✅)：`Initial`(analysis_step) → `DynamicStep`(dynamic_explicit_step: **period=40s, mass_scaling(target_time=0.0002, frequency=100, type=1, region='*'), nlgeom=False, modal_damping=None**)；另 `StaticStep`(static_general_step: period=1, init_inc=1, max_inc=1, min_inc=1e-5)。注：YJK 导入已自动建步，故手册说"省略建步"。

## 2. 弹塑性分析增量（§10.16-10.24，在弹性 pre 副本上改）
- §10.17 **土体材料转换**：工程—土体材料转换 → 给土层加 **Davidenkov 本构**(✅手册明述,与你 [[reference_davidenkov_keywords]] 对应) 对应 API：`geotool.convert_to_davidenkov(mats)`（v2026 §3.4.18, PDF p126；前提"材料有 test data 属性"，返回 list[string] 材料名）；⚠本机自省 spec 的 geotool 清单未见该函数，本机版本待实测
- §10.18 YJK 材料转非线性 + 配筋(选 YJK)
- §10.19 静力边界 BC_X/BC_Y：类型=位移/转动位移，仅 U1/仅 U2 置 0；BC_base：类型=全约束（U1-UR3=0）——⚠勿把三者统一设成全固定
- §10.20 **修改地震场地反应**：用于=时程分析(非线性), 勾调幅, **目标地表加速度峰值=2.2 m/s²（≈0.22g；勿按 gal 填 220）** ✅(②关键数值)；对应 API `geotool.compute_era(2.2, 5, 0.01, a_layer, 'Vibra-load')`（v2026 §3.4.22, PDF p127-128, 版本要求 v3.3.0+；a_layer：0=基岩处/1=基岩露头/2=地表，按"目标地表"应取 2，待实测确认）
- §10.21 加载预设场输出"动力弹塑性"
- §10.22 工况：Initial(加 Comb_M) → **先静力步(加 AllGrav 重力 + BC-X/Y/base)** → **动力步(额外加 AllGrav 做地应力平衡 + 弹塑性场输出)** ✅(弹塑性比弹性多了静力地应力平衡这一步)

## 3. 本章解码出的关键 ② 语义
- **显式动力步**:中震弹性用 period=40s + mass_scaling target_time=2e-4s(与小楼教学例同为 2e-4；其余案例多用 5e-05 更细)、type=1、frequency=100(更新间隔)、modal_damping=None、nlgeom=False
- **地震场地反应(SSI输入)**:`is_outcrop=True`(露头基岩输入)、单向(只 amp_bottom_y)、`pwave_dir=2`(Z 为波传播方向)、引用一维土层名而非直接给波——波在 amplitude 里
- **人工边界**:art_bc 核心字段 structure+surface；形心经 centered/center 表达（GUI 须选土体几何为形心参考，本例落库为 centered=False, center=[]）,粘弹性边界自动施加
- **工况-步-荷载绑定**:静力工况(Dead/Live/Comb)走 StaticStep;地震工况 Case-1 走 Initial→DynamicStep;弹塑性需在动力步前插静力步做地应力平衡
- **单位**:m-t-s(kPa);土层 E 量级 0.15~18 GPa(kPa 计)

## 4. 诚实缺口（需实跑/查证）
- 🟐 标记项是按 v2026§8.1(旧版§7.1) 范式外推,语法对但 GFE 是否接受待实跑
- 工况挂载 setter 已由 API 自省补齐（set_artbc/set_vload/set_bcs/set_fieldReqs/set_histReqs/set_initialConditions/set_elemAdd/set_elemDel，签名统一 (步名, [对象名])，gfe_api_spec.txt 行 118-125）；实跑验证语义为可选项
- gmat 材料导入（v2026 §6.4.5 io.import_mat）、土体材料转换加 Davidenkov（v2026 §3.4.18 geotool.convert_to_davidenkov）已在现行手册文档化，但本机自省 spec 未见、版本待实测；YJK 配筋等"工程—"菜单功能命令流 API 未必暴露,可能仍需 GUI 或 inpx


---
# ===== _synthesis_ch11_13_15_动力SSI.md =====

# 动力 SSI 层合成：ch11 地上地下抗震 / ch13 反应位移法 / ch15 列车振动
> 与 ch10(地铁站抗震, 见 _synthesis_ch10) 配套。基线=ch10, 本文只记**差异**与**跨章统一模式**。
> ✅dump/手册直证 ｜ 🟐范式外推待实跑 ｜ ⚠API名/装配待查 ｜ ❌无dump(仅手册)

═══════════════════════════════════════════
## A. ch11 抗震-地上地下结构（带地下室高层）—— 与 ch10 几乎同构
- 几何：YJK 导入 SuperStru + BasementBoundary；土体 **260×260m**
- 相互作用：**只有绑定 tie(×10)，无桩基嵌入**（ch10 有 embed）
- **dump 是弹塑性版**：`Case-1` steps=**['Initial','StaticStep','DynamicStep']**（3 步=静力地应力平衡+动力，✅ 印证手册 §11.23 弹塑性流程）
- soil `soil_1D`：7 层 depth=[3,4,8.5,14.5,3,5,7], materials=['tu1-2'..'tu7-1'], bedrock='tu7-1'
- 地震场地反应 `VibLoad`：**x 向**(amp_bottom_x='Amp-1')、is_outcrop=True、pwave_dir=2、soil='soil_1D'  ⚠dump 模型为 x 向自建波 Amp-1，与手册 §11.12（"幅值函数激活 y 方向"、预设波 25_RH1TG025）不一致——dump 本身偏离手册案例，方向系建模者自选，复刻手册需按 §11.12 选 y 向
- 人工边界 `ArtBC-1`：structure='SuperStru', surface='arc_surface'
- 工况：§11.14 正文与截图不一致（正文写"惯性力+底部约束+场输出"疑似笔误；截图 OCR 与 §10.13 一样写"场地反应/人工边界/场输出"）——动力步实际挂载应同 ch10：地震场地反应+人工边界+场输出（另加惯性力/底部约束类项）；ch1112 dump 中 VibLoad 与 ArtBC-1 均存在佐证
- **结论**：ch11 = ch10 的 API 链直接套用，仅 soil/波向/有无 embed 不同 → 复用 ch10 模板即可

═══════════════════════════════════════════
## B. ch13 反应位移法 —— ❌无 dump(.pre打不开), 仅手册版工作流, 本质不同
拟静力法(地下结构抗震)，**不是时程**。关键差异：
1. 材料须含 **基床系数**（`material.entry_type=BedCoefficient` / `Mat_BedCoeff`）—— YJK 导入后须补这一项
2. 导入**主体结构 + 地连墙**（地连墙作"附属结构", 名称前缀 DLQ）
3. 地震场地反应选 **"拟动力分析"**(非时程)、激活 **x 向**、并填**结构顶/底到土表的深度**(非负)
3a. 一维土层深度方向选 **y**（二维断面，§13.6），非 ch10/11/15 的默认 z（depth_dir=2）
4. 反应位移法荷载三件套=**地震动惯性力+土层剪力+相对位移**（助手自动建）；底部约束为边界条件，助手不建须手补（见第 7 条）
5. 相互作用：**接地弹簧**(主体/地连墙↔土, 简化, `spring_dashpot`) + **主体↔地连墙 只压不拉 tie**(compression-only)
6. **⚠ 反应位移助手**（工程—反应位移法）：选主结构几何+勾地连墙+选地震场地反应→点"生成", **自动**建好"除底部约束外"的全部边界/荷载/相互作用/分析步/工况。这是个 **GUI 助手, 极可能无命令流 API** → 此法是三者中**最难脚本化**的
7. 助手后手动：建底部约束并加入工况 + 场输出(节点 U) + 提交
- **结论**：反应位移法走助手, 命令流复现需先确认助手有无 API；没有则只能复现它生成的产物(接地弹簧/惯性力/剪力/相对位移边界), 工作量大, **建议此法暂留 GUI**

═══════════════════════════════════════════
## C. ch15 列车振动 —— 移动荷载动力, 无地震; 几何=YJK+快速建土+草图器混合
- **几何来源混合**：主体结构 SuperStru+地下室轮廓 BasementBoundary=YJK 导入（§15.2，模型/荷载/工况均导入）；土体 Soil-1=快速建土（§15.5，300×300）；隧道/道床/钢轨=草图器 `GFE.draft`（v2026 手册第 4 章有正式文档, PDF p136-155）+拉伸/阵列（ch15 新增能力仅指后者）。隧道/道床本体拉伸 300m；另有切土裁剪面拉伸 310m（两端各长 5m 防贴面布尔失败）；钢轨=**阵列**
- soil `Soil1D-1`：**复用 ch10 同一 7 层剖面**(depth=[4.72,9.5,11.5,9.5,1.9,5.1,40], 4-3..9H, bedrock 9H)
- 相互作用(车致振动特色)：
  - **道床-钢轨 连接器**：`orientation`(Orientation-1, data=[1,0,0, 0,1,0, 0,0,0], type=0 局部系) + `connector_behavior`(ConnBeh-1: **弹性 compressive_stiffness=[39000,39000,39000] + 阻尼 'GFE DAMP2' values=[40,1,40,1,40,1]**) + `connector_section`(Connector-1/2 左右轨, connector_type=[0,3], behavior+orientation+nset)
  - `spring_dashpot` RigidBar_0(type=4, stiffness=1e6)
  - `tie`×16(土-结构/土-隧道/隧道-道床)
- **列车荷载**(boundary 特殊类型)：区域=轨道几何集, 参数=起点/终点/缩放系数/列车速度; 轮轨力=静轮压(GFE预设)或动轮轨(轨道实测加速度法/不平顺法/直接输入) → 对应 dump 里 boundary 的 **`track_coord`/`track_id`/`if_*`** 字段; + 轨道两端全约束
- 动力步 `Dyna-1`：dynamic_explicit, **period=15s, target_time=5e-5**(比地震 2e-4 更细, 因高频车致振动)
- 场输出：节点 U, 时间间隔 0.1
- 人工边界 `ArtBC-1`：structure='SuperStru', surface='artbc'；**无地震场地反应**(激励是列车荷载, 非地震)
- 工况 `Case-1`=Initial→Dyna-1
- **结论**：ch15 引入 3 个新能力——草图器建几何 / 连接器(道床-钢轨) / 列车荷载边界；这些 dump 字段都拿到了, 但构造/装配 API 待验

═══════════════════════════════════════════
## D. 跨章统一：动力 SSI 通用骨架（ch10/11/13/15 归纳）
```
[几何来源] YJK 导入(结构, ch10/11/13/15 均有；ch13 二次导入地连墙) + 快速建土(土体) + 草图器(隧道/道床/钢轨, 仅 ch15)
  → 土材料(gmat导入 + 弹塑性须 Davidenkov; 反应位移法须 基床系数)
  → 一维土层 soil.soil(depth/materials/bedrock_mat/depth_dir)
  → 快速建土 GFE.soil.box_builder→data_builder
  → 平移定位(geoprim.translate, 形心对齐±埋深) → 布尔裁剪(geoprim.cut 挖基坑/隧道)
  → 相互作用: tie(搜索接触) / embed(桩基,仅ch10) / connector(道床钢轨,仅ch15) / 接地弹簧(仅ch13)
  → 人工边界 artbc(structure + surface边界面集)
  → 【激励源·三选一】
      · 地震时程: vibration.vibra_load(soil + amp_bottom_x|y + is_outcrop + pwave_dir)  [ch10/11] ⚠多向输入时三向幅值点数必须一致（*Wave 缓冲区 bug，否则 0xC0000374 堆损坏）
      · 反应位移法: 反应位移助手→惯性力+土层剪力+相对位移  [ch13, ⚠可能无API]
      · 列车移动荷载: boundary(列车荷载type, track_*)  [ch15]
  → 网格 mesh_generator(土 四面体 size~3 / 结构 六面体 size~1; ch15道床0.6扫掠)
  → 工况 case.case(steps): 弹性 Initial→DynamicStep; 弹塑性 Initial→StaticStep→DynamicStep(静力地应力平衡)
  → 提交 GFEXG.exe -db
```
**统一 ② 数值**：
- DynamicStep=dynamic_explicit_step, **mass_scaling(type=1, frequency=100, region='*', target_time=地震 2e-4 / 列车 5e-5)**(target_time 是 mass_scaling 对象内字段, 不是 step 直属参数; 越高频越细), period=分析时长(地震40s/列车15s), modal_damping=None
- 弹塑性增量: 土材料转 Davidenkov + 静力步加 AllGrav，**且动力步需再次添加 AllGrav 做地应力平衡（手册 §10.22/§11.23 明文，漏挂则动力步重力消失）** + 调幅目标地表加速度 2.2 m/s²（案例值）
- artbc=粘弹性人工边界, 只需 structure名+surface(边界面集)名
- 单位制随模型: ch10 m-t-kPa(E~kPa) / ch01 mm-t-MPa —— 按 density/E 反推

═══════════════════════════════════════════
## E. 诚实缺口（动力 SSI 层共性，待实跑/查证）
- ✅ **装配进工况已证**：工况装配走 `c.set_bcs/set_vload/set_artbc/set_fieldReqs(步名, [对象名])`（gfe_api_spec.txt L118-125 共 8 个 set_*；_probe_assembly.txt §2 实测 Case-1 全具备）；case 只有 set_* 无 get_*（写专用），挂载验证须看导出 INP
- ✅ art_bc / vibra_load / connector_behavior / 列车荷载 构造已由装配探针实跑坐实（_probe_assembly.txt §1/§3）：范式 `o=Cls(); o.字段=值; X_mgr().add(o)`；连接器嵌套 `connector_behavior.behaviors=[connector_elastic, connector_damping]`；列车荷载 boundary type=9 的 value/track_coord 实值已测
- ⚠ **ch13 反应位移助手**: GUI 助手, 极可能无命令流 API → 此法暂留 GUI 或大量复现其产物
- 🟐 **草图器 GFE.draft**(ch15几何): v2026 命令流手册第 4 章有正式文档（PDF p136-155）；未实跑
- ❌ "工程—"菜单功能(gmat导入 / 土体材料转Davidenkov / YJK配筋 / 快速建土 / 反应位移助手): 多为 GUI 专有, 命令流未必暴露


---
# ===== 真实工程_400galW7-VC_解析.md =====

# 真实工程反编译解析：400galW7-VC.pre
> 源：G:\400gal-W7-VC\400galW7-VC.pre（37.1MB）→ 反编译 dump D:\GFE\decomp\400galW7VC.txt（65735 行，managers=40）

## 概述
完整**三向 El Centro 400gal 弹塑性 SSI**：39 层上部结构(YJK 导入) + 16 层 Davidenkov 土 + D1200 桩基嵌入 + 粘弹性人工边界 + 三步工况（静力→显式动力）。单位制 **m-t-kPa**。

## 规模
geometry 3(SuperStru/Soil-1/WallSurface) / material 35 / gset 2676 / elset 2 / nset 1 / section 1101 / boundary 2202 / surface 200 / embed 3 / tie 2 / amplitude 6 / step 3 / case 7 / vibration 1 / artbc 1 / soil 1 / fieldout 7 / histout 2

## 材料与本构（★）
- 混凝土(C1_Mat30 等)：`density(2.5) + damping(α=0.188, β=0) + user(7常数, user_type=1)`；如 C1_Mat30 user[0]=3e7 kPa=E
- 混凝土 C2 系列(C2_Mat30…C2_Mat80, 7 个)：`density + elastic + damping + concrete_damaged(CDP)`，plasticity=[35.0, 0.1, 1.16, 2/3, 0.005]，压硬化/压损伤曲线 21 点、拉硬化/拉损伤 7 点
- **C1/C2 双轨分工**：同强度等级双材料——C1=user_type=1 一维非线性（配纤维构件），C2=CDP（配壳/实体）
- 钢材 HRB400/Q345/Q390：plastic（双折线硬化）
- 桩 zhuangtong/zhuangqun：弹性（E=2551600 kPa, ν=0.24, α=0.2）
- 土 tu1–tu16：`density + damping(α, β=0) + user(6常数, user_type=2=Davidenkov)`；如 tu1: ρ=1.63, user=[108300(kPa), 0.25(ν), 1.02, 0.44, 0.00045, 100000]
- **β 阻尼一律 0**（显式动力稳定）

## 土层（16 层，★）
`Soil1D-1`：厚度 [1.5,1.5,1.0,1.0,3.35,3.5,3.0,6.0,4.0,15.0,15.0,2.0,3.0,3.0,3.0,10.0]（合计 **75.85m**），materials=tu1…tu16，bedrock=tu16，depth_dir=Z

## 地震输入（★三向）
`VibLoad-1` vibra_load：amp_bottom_x=**Amp-X**, y=**Amp-Y**, z=**Amp-Z**（X/Y/Z 三向同时），is_outcrop=True(露头基岩)，pwave_dir=Z，soil=Soil1D-1。
6 个 amplitude：400galElcentro / Amp-1 / Amp-X / Amp-Y / Amp-Z / Amp-DY

## 边界 / 相互作用
- 人工边界 ArtBC-1：structure=SuperStru, surface=PickedSurf-1
- 桩基嵌入 embed×3：Embed-1 把 Col_D1200_Sub0_C50_814(D1200 桩) 嵌入 host=wallsurface(容差 0.8)；Embed-2=Col_D1200_HRB400_815(容差 0.8)；Embed-3=PIPE1600/PIPE2000 共 4 个钢管构件(**exterior_tolerance=0.5**，与前两者不同)
- 绑定 tie×2：Tie-diban(底板)、Tie-2

## 分析设置
- 步：Initial → StaticStep(普通静力步 static_general_step，承担动力步前自重应力建立——**非** geo_static_step"静力分析(地应力平衡)"独立步类型, init_inc=0.01/max=0.1/min=1e-5, period=1) → **DynamicStep**(显式, **period=35s**, mass_scaling target_time=5e-5/freq=100/type=1, modal_damping=None, nlgeom=False)
- **主工况 = `400galElcentro`**：Initial→StaticStep→DynamicStep（三步弹塑性 SSI）
- 另：400galElcentrostatic(静力对照)、Dead/Live/消防车_gk2/gk3/Comb(静力)

## 输出配置
- 场输出 ×7：FO-Static / FO-DynaPla-All / FO-DynaPla-Jiegou / FO-DynaPla-ShearForce / EO-DynaPla-Max / EO-DynaPla-Min / FieldOutput-1（弹塑性工程前提含"加载弹塑性预设场输出"，手册 §10.16–10.22）
- 历程输出 ×2：HistoryOutput-1 / HistoryOutput-2

## 与项目记忆吻合点
39 层 + 软土 + ElCentro 400gal + Davidenkov(user_type=2) + β=0 + 16 层土 + 桩基 + 三步弹塑性 → 与 [[project_context]]/[[reference_davidenkov_keywords]]/[[project_explicit_beta_damping]] 逐项对上。Amp-X/Y/Z 三向等长(各1710对) → 与 [[project_gfe_wave_buffer_bug]] 合规。
