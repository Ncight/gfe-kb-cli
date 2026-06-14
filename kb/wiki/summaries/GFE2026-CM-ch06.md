---
title: "GFE2026 官方命令流 ch06 — 深基坑施工开挖（CM6-update2.py）"
type: command-stream-case
software: GFE
version: v3.x
chapter: 6
tags: [gfe, command-stream, 基坑开挖, 施工模拟, 生死单元, 复制网格]
sources: ["[[GFE2026-CM-ch06-CM6-update2.src]]"]
created: 2026-06-11
updated: 2026-06-11
---

> 官方 961 行命令流把第 6 章基坑开挖案例**全程参数化**：草图放坡 → 逐层拉伸开挖体 → 内支撑/立柱 → 布尔合并印刻土体 → YJK 导入既有建筑 → 形心分区建集 → copy_mesh 生成支护 → [[单元生死]]字典驱动 6 步施工链 → 导 INP。是 v3.x 命令流"几何到作业一条龙"的最完整官方样板。

## 调用链概览

```
draft 草图(多折线/矩形/直线 input) → export + geo_mgr.add
→ geoprim.builder: extrude / common / make_array / translate / merge / split / cut
→ material(手建 C35) + io.import_mat(cm6.gmat 整包导土材料)
→ soil.soil(1D 土层) → soil.box_builder + data_builder(快速建土 Soil-1)
→ io.import_yjk(43 元参数) → SuperStru / BasementBoundary
→ 形心分区 idiom 建 gset: Set-fangpo / Set-kaiwa1~4 / Set-pshnt / Set-dilianqiang / Set-neizhicheng1~2 / Set-lizhu
→ mesh_generator(结构 size2/Algorithm8 → 土体 size3/Algorithm2)
→ geotool.copy_mesh ×5 (S3 壳 / B31 梁, origin_node=True)
→ property_shell / property_beam → contact_pair.search_face + Tie(param_number=1)
→ boundary(bc-z/x/y) → geo_static_step + static_general_step ×5
→ case 映射属性字典(bcs/fieldReqs/elemAdd/elemDel) → inpio.writer
```

## 关键经验（官方实证）

### 1. 开挖分步 elemDel/elemAdd 字典写法（v3.x 工况即映射属性）

```python
case_obj.elemDel['GeoStatic-1'] = ['pshnt-1','dilianqiang-1','neizhicheng1-1','neizhicheng2-1','lizhu-1']  # 地应力步杀光支护
case_obj.elemDel['fangpo']  = ['Set-fangpo']      # 放坡步挖放坡土
case_obj.elemAdd['fangpo']  = ['pshnt-1','dilianqiang-1','neizhicheng1-1','lizhu-1']  # 同步激活第一批支护
case_obj.elemDel[f'kaiwa{i}'] = [f'Set-kaiwa{i}'] # i=1..4 逐层开挖
case_obj.elemAdd['kaiwa2']  = ['neizhicheng2-1']  # 仅挖到第 2 层时加第二道内支撑
```

值混用**几何集名**（土，Set-kaiwa*）与 **copy_mesh 单元集名**（支护，*-1）。v2.15 无映射属性，只有 `set_elemDel/set_elemAdd`。

### 2. 立柱"点拉伸"真身

`geotool.children(shape, 7)` 取草图几何**顶点**（type 7 = vertex），筛出内支撑内部交点后直接 `builder.extrude(顶点列表, [0,0,-12])` 拉成线几何。**extrude 接受顶点 shape，点→线命令流可行**——原 GUI 断点解除。

### 3. copy_mesh：复制网格有命令流 API

```python
GFE.geometry.geotool.copy_mesh(name='Set-pshnt', origin_node=True,
    as_source=False, type_name='S3', new_set_name='pshnt-1')
```

源=几何集（划网格前预建、定稿后调用），origin_node=True 即"使用和源相同的节点"（共节点免[[通用接触]]）。单元类型 S3/B31（官方未用 S3R）。v2.15 无此 API。

### 4. 形心分区建集 idiom（开挖层动态判层）

遍历 `children(Soil-1, 2)` 实体，先用 xy 包围盒锁定基坑柱体，再按实体形心 z 落区动态算层号：`Set-fangpo`（-1<z<0）、`Set-kaiwa1`、循环算 upper/lower_bound 归 `Set-kaiwa{i}`。所有几何选择都靠 `centre_of_mass` 坐标判定，**不依赖子形状顺序或 id**（鲁棒于 ch07 发现的 split 归属 bug）。

### 5. 其他要点

- 草图 API：`set_operate_mode(2/3/1/-1)`=多折线/矩形/直线/退出；`input(u,v)` 二维参数坐标；`set_normal(origin, normal, xdir)` 三向量定平面；`fill_selected()` 后 `remove_selected()` 删线留面。
- 放坡体 = x/y 两个方向断面体 `common()` 布尔取交（非单草图直出）。
- 'AllGrav' 重力边界来自 [[import_yjk]] 导入产物，py 不自建；43 元 yjk_para 跨案例不同位不同值，不能照抄。
- 场输出 ch6 用 `field_mgr().edit(obj)`（覆盖式）而非 add。
- Tie 用 `surfpair.param_number=1; parameters=[0.01]`（[[搜索接触]] search_face 容差同 0.01）。
- 共 6 分析步：geo_static_step + static_general_step×5，全 nlgeom=True。

## 相关

[[GFE-Cases-06-基坑开挖]]（手册 GUI 路线）｜路径文件 `D:\GFE\GFE_KB\02_案例反推\路径_ch06_基坑开挖.md`（已按官方校正）｜[[单元生死]]｜[[搜索接触]]
