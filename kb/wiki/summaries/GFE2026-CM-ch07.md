---
title: "GFE2026 官方命令流 ch07 — 锚杆隧道施工（CM7.py / CM7-update2-存在bug.py）"
type: command-stream-case
software: GFE
version: v3.x
chapter: 7
tags: [gfe, command-stream, 隧道施工, 锚杆, 生死单元, 嵌入区域, 已知bug]
sources: ["[[GFE2026-CM-ch07-CM7.src]]", "[[GFE2026-CM-ch07-CM7-update2-存在bug.src]]"]
created: 2026-06-11
updated: 2026-06-11
---

> 官方 691 行命令流复刻第 7 章锚杆隧道分段开挖：`build_tunnel_shape` 一行造三心圆隧道+锚杆带 → split 印刻土体 → 形心分段建集 → 线控制网格 → copy_mesh 衬砌 → 锚杆 [[嵌入区域]] → 13 步[[单元生死]]施工链。配套 update2 版（文件名自带"存在bug"）是**官方自证 GFE 内核 bug 的珍贵负面样本**。

## 调用链概览

```
io.import_mat(cm7.gmat) → soil.soil + box_builder + data_builder(Soil-1, 90×20, 3 层)
→ geotool.build_tunnel_shape(...) → [隧道, 隧道土边界, 锚杆带] 手动 geo_mgr.add
→ 锚杆带 children(.,6) 按 y 分段 → gset Tunnel-rockseg-1~10
→ translate 形心对位 + 锚杆 y+0.2 嵌入偏移 → builder.split('Soil-1',['Tunnel-Boundary'],True)
→ 三心圆形心公式锁包围盒 → gset suidaotu-1~10(实体)/suidaoqiao-1~10(侧面)
→ mesh_generator + curve_control×4(count 3/5/10/18, edges 字典手工组装)
→ copy_mesh(suidaoqiao-i → CpMsh-i, S3, as_source=True) → elset data 拼接 Set-CpMsh
→ property_beam(锚杆 r=0.0125) + property_shell(衬砌 t=0.15)
→ interaction.embed(host=Set-tuti, embedded=Set-maogan)
→ boundary + G-whole 惯性力 → static_general_step ×12
→ case 映射属性字典 → inpio.writer('suidaokaiwa')
```

## 关键经验（官方实证）

### 1. 锚杆怎么建：build_tunnel_shape + embed（不是共节点、不是 Tie）

```python
[a,b,c] = GFE.geometry.geotool.build_tunnel_shape(
    1, [5.5, 9], [90, 25],          # 3心圆: [顶弧R,侧弧R], [顶弧角,侧弧角]
    False, 0, 0, True, True,
    [13, 4, 1.8, 0.2],              # 锚杆 [数量,长度,弧长间距,外偏移]
    True, 20, [2], [2], 0, False, None)  # 拉伸 20m, 隧道/锚杆分段间隔 2
mgr.add('Tunnel', a); mgr.add('Tunnel-Boundary', b); mgr.add('Tunnel-Rockbelt', c)
```

- **支持分段和锚杆**（修正早期反推"只造形状不分段不布锚杆"的结论），但产物不落库须手动注册；v2.15 无此 API。
- 锚杆带平移 `[0, 0.2, 0]` 嵌入土体（embed_offset < 分段间隔），划 B31 网格（size 1.0）后整带建 `Set-maogan` 几何集，与土体连接走 **embed**：`host_name='Set-tuti'; embedded_names=['Set-maogan']; roundoff_tolerance=1e-06; exterior_tolerance=0.05`。

### 2. 13 分析步官方版（重大修正：锚杆当段加、衬砌滞后一段）

steps = Initial + Static-1 + Stage-1~11。Static-1 地应力步（nlgeom=**False**，普通静力步）杀光全部支护**分段集**：CpMsh-1~10 + Tunnel-rockseg-1~10（非总集）。施工节奏：

| 步 | elemDel | elemAdd |
|---|---|---|
| Static-1 | CpMsh-1~10 + Tunnel-rockseg-1~10 | — |
| Stage-1 | suidaotu-1 | Tunnel-rockseg-1 |
| Stage-i (2~10) | suidaotu-i | Tunnel-rockseg-i, CpMsh-(i-1) |
| Stage-11 | — | CpMsh-10 |

即 **Stage-i 挖第 i 段 + 当段锚杆立即激活 + 第 i-1 段衬砌滞后安装**，末步收尾。suidaoqiao-n 只是 copy_mesh 源面集，不进工况。

### 3. 已知 bug（CM7-update2-存在bug.py 专设探针复现）

**bug 本体在 GFE 内核，不在脚本。** update2 与 CM7.py 的功能差异仅两处：

1. 注入 `Bug_Check()` 函数，在 `builder.split('Soil-1', ['Tunnel-Boundary'], True)` 前后各打印一次 `children(Soil-1, 2)` 各子实体的 `get_id_by_shape` 结果。官方注释原文：**"存在每次打开gfe，数据不一致的情况"**——同一脚本跨会话两种结果：
   - 正常：每个 id 列表首元素=1（父几何 = Soil-1）；
   - bug：部分列表首元素=3（父几何 = Tunnel-Boundary）。
2. boundary 对象补 11 个新 schema 字段（track_id / track_coord / has_if / if_mode / if_acce_path / if_acce / if_param / if_itv / if_tot / if_grade / if_force——移动荷载轨迹与惯性力时程扩展），全部赋空/默认，适配更新版 GFE。

**性质**：布尔 split 后子实体的父归属/shape-id **跨会话非确定**（疑 OCC 布尔结果排序不稳定）。**后果**：任何"按 `find('Soil-1')` 遍历 children 建集"的下游逻辑可能漏体/错配。**防御**：官方 CM7 全部用 `centre_of_mass` 坐标判定归集、不依赖 id/顺序，故主线仍可跑通；复刻时同样**只信形心坐标，不信 shape id**。

### 4. 其他要点

- 线控制完整写法：`curve_control.edges` 是 `{几何体id: [边子id,…]}` 字典，**手工**从 `get_id_by_shape` 收集组装（取返回列表首尾元素）；`controller.size_option=[cc1..cc4]`；官方未设 density 字段。
- 隧道侧面判据：`abs((round(fy) % spacing) - spacing/2) < 1e-9`（面形心 y 落段中点 = 侧面）；实体分段 `index=(round(sy)+1)//spacing`，**dict + sorted(keys) 保证集合顺序**。
- 三心圆形心到顶/底距离由纯几何公式 `calc_centroid_to_top_bottom(R, r, α, β)` 现算（py 内置 51 行实现），用于锁定隧道包围盒。
- elset 合并 idiom：`elset_mgr().find(f'CpMsh-{i}').data` 逐段拼接 → 新建 `set.elset()` 总集 Set-CpMsh。
- 截面名官方拼写 **Propery-**（笔误照抄保持一致）；gset_mgr().add 双形态：`add(name, shapes)` 与 `add(gset_basic对象)`。

## 相关

[[GFE-Cases-07-锚杆隧道]]（手册 GUI 路线）｜路径文件 `D:\GFE\GFE_KB\02_案例反推\路径_ch07_锚杆隧道施工.md`（已按官方校正）｜[[单元生死]]｜[[嵌入区域]]
