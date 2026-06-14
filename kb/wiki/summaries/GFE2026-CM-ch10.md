---
title: "GFE2026 官方命令流 — 第10章 地铁站抗震（弹性 + 弹塑性）"
type: command-stream-case
software: GFE
chapter: 10
version: v3.x
tags: [gfe, command-stream, ssi, seismic, dynamic, plastic]
sources: ["[[GFE2026-CM-ch10-第十章命令流-弹性.src]]", "[[GFE2026-CM-ch10-第十章命令流-弹塑性.src]]"]
created: 2026-06-11
updated: 2026-06-11
---

> GFE2026 官方发布的第 10 章命令流双脚本（弹性 411 行 / 弹塑性 916 行），是 [[GFE]] v3.x 动力 [[土-结构相互作用|SSI]] 全链的最权威代码真值：YJK 导入 → 一维土层/快速建土 → 布尔裁剪 → [[粘弹性人工边界]] → [[地震场地反应]] → 绑定接触 → 网格 → 显式动力步（[[质量缩放]]）→ 工况 → INP。弹塑性版在弹性版全文重放之上追加 6 段增量，给出了"弹性→弹塑性"官方升级配方。

## 调用链骨架（弹性版）

`import_yjk(43元)` → `import_mat(tu-Elastic.gmat)` → `soil.soil('Soil1D-1', 7层, bedrock='9H')` → `soil.box_builder().set_height(soil.depth, soil.depth_dir) + set_parameter(300,250)` + `data_builder` → 平移两次（形心对齐 + 上移 4 m 设埋深，移土不移结构）→ `cut('Soil-1',['BasementBoundary'],True)` → **边界面质心筛选脚本**（包围盒 + `geotool.children(shape,4)` + `centre_of_mass`，tolerance=1，产 front/back/left/right/bottom_boundary 五个几何集）→ geometry_surface 'arc_surface' → `art_bc(structure='SuperStru')` → 手贴幅值 Amp-y（25_RH1TG025 人工波归一化，0~20s@0.02s）→ `vibra_load`（仅 amp_bottom_y，14 个 set_parameter 全集）→ `contact_pair.search_face` + Tie 循环 → 网格（土 size 5 / 结构 size 2，Algorithm 2/3D 10，auto_transfinite=True）→ `dynamic_explicit_step`（period 20，[[质量缩放]] target_time 5e-5）→ case 字典挂载 → `inpio.writer`。

## 弹塑性增量（官方升级配方，6 段）

1. **场地反应调幅**：`geotool.compute_era(2.2, 5, 0.01, 1, 'VibLoad')`——目标地表峰值 2.2 m/s²、迭代 5、容差 0.01、第 4 参=1；调用时机在 vib_mgr().add 之后立即。调幅产物以**同名重 add 幅值**回填（原波 ×0.7238）。
2. **五面静力边界**：复用质心筛选产的几何集——BC-bott 全约束 + 左右仅 U1 + 前后仅 U2。
3. **输出切换**：`field_mgr().delete([弹性预设…])` 后挂动力弹塑性五件套：FO-DynaPla-All（U+PE+jiegou 集 DAMAGEC/DAMAGET）、FO-DynaPla-Jiegou（StoryDrift-AllFloor 层间位移）、FO-DynaPla-ShearForce（StoryShear-All NFORC1/2）、EO-DynaPla-Max/Min（损伤包络，type=2 / method=2/3 / time_type=-1）。
4. **三段式工况**：steps=['Initial','StaticStep','Dyna-Step']；StaticStep 挂 AllGrav+五面固定做**地应力平衡**（无 geostatic 步、无初始条件，纯静力步配重力）；**Dyna-Step 再挂一次 AllGrav**（双挂铁律，漏挂则动力段重力消失），固定边界撤掉换 [[粘弹性人工边界]]。
5. **结构弹塑性转换**：`geotool.convert_material(1)` + `geotool.convert_reinforce(1)`（配筋转换 API 实证存在），时机在工况定义后、写 INP 前。
6. 写 INP（Case-dyna-pla）。

## 关键裁决：官方弹塑性如何处理土体非线性

**官方命令流不建 [[Davidenkov本构|Davidenkov]] 材料。** 弹塑性版土体仍用同一份弹性 gmat，土的非线性全部由 `UseEERAMat='true'` + `compute_era` 的 **EERA [[等效线性化|等效线性]]迭代**承担；弹塑性只落在结构（convert_material/convert_reinforce → CDP 类用户材料+配筋）。手册 GUI 的"土体材料转换→Davidenkov"在官方 py 中无对应 API（convert_to_davidenkov 不存在），Davidenkov 入口仍是 GUI 或手写 INP *User Material（29 SDV）。同理，dump 实测模型的桩基 [[嵌入约束|embed]]（floor1-AllCol→soil）也未进官方命令流。

## v3.x 专属 idiom（v2.15 不可用/不同）

- 工况挂载用**映射属性字典**：`c.bcs['步']=[…]; c.vload[…]; c.artbc[…]; c.fieldReqs[…]`，空键也显式赋；v2.15 只有 set_* 写接口。
- `obj.mass_scaling=[ms]` 属性赋值；`import_yjk / import_mat / compute_era / convert_material / convert_reinforce` 五个 API v3.x 实证可用、v2.15 实测缺位。
- 幅值空串语义：`amp_bottom_x=''` 表示该向不输入。
- 场输出"add 后同名 edit"追加子输出；同名 add 幅值=更新。
- 官方注释自认"命令流尚未提供加载预设"——预设地震波须手工贴 value 数组。

## 复刻警告

官方 py 是**会话录制稿**：StaticStep、AllGrav、jiegou、StoryDrift-AllFloor、Comb_M_* 等全是 YJK 导入自动产物，py 内不创建直接引用；`field_mgr().delete` 的清单是 GUI 预设遗留。裸重放须先核这些对象在位。auto_transfinite 官方 v3.x 全开，但 v2.15 实测会崩。
