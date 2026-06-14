---
title: "GFE-命令流SSI骨架 — 动力 SSI 通用建模骨架 + 15 章案例反推"
type: manual
software: GFE
tags: [gfe, manual, 命令流, ssi, 抗震]
sources: ["[[GFE-CmdKB-cases.src]]", "[[GFE-CmdKB-400galVC.src]]"]
created: 2026-06-04
updated: 2026-06-04
---

> 「某流程怎么串」层：由 15 章案例 .pre 反编译 + 三源合成（手册 + dump + API）归纳出的命令流建模范式，核心是动力 [[地上-地下耦合结构|SSI]] 通用骨架，并以真实工程 400galW7-VC 收口。每章 GUI 操作详见对应 [[GFE-Cases]] 子页；本页讲命令流装配。

## 动力 SSI 通用骨架（ch10 / 11 / 13 / 15 归纳）
```
[几何来源] YJK导入([[YJK]]) | 草图器(draft, ch15) | 主体+地连墙(ch13 反应位移法)
 → 土材料(gmat导入 + 弹塑性须 [[Davidenkov]]; [[反应位移法]] 须 基床系数)
 → [[一维土层]] GFE.Pre.soil.soil(depth/materials/bedrock_mat/depth_dir)
 → [[快速建土]] GFE.soil.box_builder → GFE.soil.data_builder（与一维土层是两个模块，须分别 import）
 → 平移定位 geoprim.translate + 布尔裁剪 geoprim.cut(挖基坑/隧道)
 → 相互作用: [[绑定约束]] tie(搜索接触) | [[嵌入区域]] embed(桩) | [[连接器]] connector(道床钢轨,ch15) | 接地弹簧(ch13)
 → [[粘弹性人工边界]] artbc.art_bc(structure + surface 边界面集)
 → 【激励·三选一】
     · 地震: vibration.vibra_load(soil + amp_bottom_x/y/z + is_outcrop + pwave_dir)  [[地震场地反应]]
       （调幅：v3.3.0+ 手册有 geotool.compute_era(target_acce, adjust_iter, adjust_target_tol, a_layer, vibra_name)；自省 spec 未见，装机版本待实测）
     · 拟静力: [[反应位移法]] 助手(惯性力 + 土层剪力 + 相对位移)  ⚠GUI 助手, 可能无 API
     · 移动荷载: boundary([[列车荷载]] type, track_*)  ⚠v3.3.0 破坏性变更：列车属性移入专门对象，旧通用对象写法断裂(merged #63/A6)；导出为 INPX(set_trainload2inpx)
 → 网格 mesh_generator(土 四面体~3 / 结构 六面体~1)
 → 工况 case: 弹性 Initial→DynamicStep; 弹塑性 Initial→StaticStep(地应力平衡)→DynamicStep
 → 提交 GFEXG.exe -db  ([[GFE求解器内核]])
```
统一数值：dynamic_explicit + [[质量缩放]](type=1, freq=100, target_time 地震 2e-4~5e-5——ch10 用 2e-4、400galVC 用 5e-5 / 列车 5e-5)，β=0（[[瑞利阻尼]]），弹塑性插静力步加 AllGrav 做地应力平衡。ch10 中震案例调幅目标地表加速度 2.2 m/s²（§10.20 特定值，非各案例统一数值）。装配范式见 [[命令流manager-CRUD]]、引用规则见 [[GFE对象引用关系]]。

## 15 章案例分类（命令流视角；详见 raw [[GFE-CmdKB-cases.src]]）
- 纯结构静力 / 模态：ch1 [[GFE-Cases-01-球铰支座]] · ch2 [[GFE-Cases-02-钢骨混凝土]]（[[嵌入区域]]）· ch3 [[GFE-Cases-03-华夫板框架]]
- 地震时程 SSI：ch4 [[GFE-Cases-04-核电站]] · ch5 [[GFE-Cases-05-非均匀场地]] · ch10 [[GFE-Cases-10-抗震地铁站]] · ch11 [[GFE-Cases-11-抗震地上地下]]
- 施工生死单元：ch6 [[GFE-Cases-06-基坑开挖]] · ch7 [[GFE-Cases-07-锚杆隧道]] · ch12 [[GFE-Cases-12-施工地上地下综合体]]（[[单元生死]]：⚠土层初始即激活，不可再 elemAdd，否则报"重复添加"）
- 特种动力：ch13 [[GFE-Cases-13-反应位移法]]（拟静力，助手 GUI 专有最难脚本化）· ch14 [[GFE-Cases-14-爆炸]]（incident_wave / [[CONWEP]]）· ch15 [[GFE-Cases-15-列车振动]]（草图器 + [[连接器]] + [[列车荷载]]）· ch8/9 [[SPH光滑粒子流体动力学]]

## 真实工程：400galW7-VC（你的项目，worked example）
见 raw [[GFE-CmdKB-400galVC.src]]：39 层上部（[[YJK]] 导入）+ 16 层 [[Davidenkov]] 土（Soil1D-1，厚度合计 75.85 m，dump soil_soil_manager.txt 求和）+ D1200 桩基 embed×3 + [[粘弹性人工边界]] + 三向 ElCentro。
- 材料：混凝土 density + damping(α, β=0) + user(user_type=1)；土 tu1–16 user_type=2（Davidenkov）。**β 一律 0**（[[瑞利阻尼]]）。
- 步：Initial → StaticStep(地应力平衡) → DynamicStep（显式, period=35s, target_time=5e-5, [[质量缩放]] freq=100）
- 主工况 `400galElcentro` = 三步弹塑性 SSI；与项目记忆（39 层 / 软土 / ElCentro 400gal / Davidenkov / β=0 / 桩基）逐项吻合。

## 诚实缺口（待实跑 / 查证）
- 装配进工况：vibration / artbc / connector / 列车荷载对象字段已拿到，但 case 用哪个 setter 挂、如何 add 进 case 部分未实跑（需 dir()/help() 或录极短 .rpy 验）
- ch13 [[反应位移法]] 助手：GUI 助手，可能无 API，建议暂留 GUI。ch15 草图器 draft：v2026 手册第 4 章已有全套文档（PDF p136-155），未实跑；注意 §4.10/§4.13 手册示例与签名矛盾两处（merged #46），实测后再脚本化

相关：[[GFE-CmdKB]] · [[GFE-命令流API规格]] · [[GFE-命令流桥与工具]] · [[GFE-SSA]] · [[Davidenkov]] · [[地震场地反应]]
