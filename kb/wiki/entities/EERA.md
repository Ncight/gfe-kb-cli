---
title: "EERA — 一维等效线性场地反应程序"
type: entity
entity_type: 软件
tags: [software, 场地, benchmark]
created: 2026-06-04
updated: 2026-06-04
---
> Equivalent-linear Earthquake site Response Analysis，经典一维等效线性化场地地震反应程序，GFE 一维等效线性化场地反应（[[地震场地反应]]/ERA 模块）的对标基准。

## 定义
按应变水平迭代折减土体剪切模量、提升阻尼比。GFE 第 7 章一维场地反应以其为基准。在 GFE-SSA 手册中该模块又写作 ERA（ERA/EERA 为同一模块，手册写法不统一，检索两名都要试）。UseEERAMat=true 时等效线性化自动替换 EERA 土材料并写入 Alpha（瑞利）阻尼——须土层有试验数据曲线才生效，无曲线须手动处理；UseAmp/UseEERAMat 可独立开关；完整流程须跑两遍（首遍生成瑞利阻尼回填）。与 SHAKE 同族。

## 在本库中的位置
- [[GFE-SSA]]、[[GFE-Explicit]]（第 7 章）、[[GFE-FAQ]]

相关：[[地震场地反应]] [[一维土层]]

