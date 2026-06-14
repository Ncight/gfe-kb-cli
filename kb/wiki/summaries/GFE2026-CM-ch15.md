---
title: "GFE2026 官方命令流 — 第15章 列车振动分析"
type: command-stream-case
software: GFE
chapter: 15
version: v3.x
tags: [gfe, command-stream, train-load, vibration, ssi, dynamic, connector]
sources: ["[[GFE2026-CM-ch15-CM15V8.src]]"]
created: 2026-06-11
updated: 2026-06-11
---

> GFE2026 官方第 15 章命令流 CM15V8.py（16912 行，结构代码约千行，其余为轨道坐标与实测加速度数组）：车致环境振动全链——隧道/道床/钢轨草图建模、连接器扣件、专用 [[列车荷载]] 边界、[[粘弹性人工边界]]、显式动力。它一举解掉了手册截图 OCR 不可辨的全部数值疑案（阵列偏移、扫掠层数、工字钢尺寸），并实证了 v3.x 专门的 `train_load` 类与 track_coord 自动装配脚本。

## 调用链骨架

`import_yjk`（43 元参数与 ch10 多位不同——场景相关再证）→ `import_mat` → 一维土层（bedrock_mat=''，本章无 [[地震场地反应]] 故基岩留空）→ 快速建土 300×300 → 平移/裁剪 → **draft 草图**两轮（圆+辅助线 split/remove → set_normal 设 XZ 面 → fill → export 入 geo_mgr）建隧道断面与道床断面 → `geoprim.builder().extrude(shapes,[0,300,0])`（切土工具体先外移 5 m 再拉 310 m 防贴面布尔失败）→ `make_array(两条道床棱线, 1,1,2, [0,0,0.3])` 阵列出双轨 Array-1/2 → gset/截面（Propery-* 四件）→ 五域网格（道床 0.6 扫掠 500 层）→ 钢轨/道床节点集 → Orientation + 连接器（扣件弹簧-阻尼）→ 三组搜索接触 16 对 Tie → `train_load` ×2 → 两端固定 → 显式动力步（period 15，[[质量缩放]] 5e-5）→ 质心筛选边界面 → 人工边界（structure='SuperStru'）→ case 'case1' → `inpio.writer` 普通 INP 直出（**无 set_trainload2inpx**）。

## 官方实证的关键数值（旧 OCR 疑案关闭）

- 钢轨阵列：行 1 / 列 1 / 高 2，偏移 **z=0.3 m**（旧读"0,0,0,3"作废）。
- 道床扫掠：`sweep_control(source=[9,4,9], target=[9,4,10], body=[9,2,1], dy=300, layers=[500], ratio=[1.0], recomb_lateral=recomb_source=True)`。
- 工字钢梁截面：shape_params=[0.088,0.176,0.073,0.073,0.034,0.034,0.0165]，shear=[327751,230086]，方向 1=(1,0,0) 垂直梁轴。
- 隧道壳材料是 **C1_Mat30**（厚 0.35、积分点 5）；道床实体 C2_Mat30。截面名拼写官方原文即 `Propery-`（少 t），按名引用不可纠正。

## train_load 专用类（v3.x 重点）

`GFE.Pre.boundary.train_load()`：type=9；set=轨道几何集；`begin_end=[起几何id,起vertex,终几何id,终vertex]`（取代旧 node_id 起终点语义）；value=[缩放 1.0, 速度 22.22 m/s, 起时, 起位, 方向(0,0,-1), 0, 轴距序列 2.1/10.3/2.1/3.5×5]；动轮轨力走"轨道实测加速度法"（has_if=True, if_mode=0, if_acce_path+if_acce 双写, if_itv=0.0005, if_param=[1.42,2.55,21.92,5.0,40.0,1700.0,275.0]）。name 留空 add 后自动名 TRAINLOAD/TRAINLOAD-1，再 `bc_mgr().rename` 成 trainload-L/R。**track_coord 官方装配脚本**：取 Array 网格 `node_data()`，按 y 升序排序后平铺 [x,y,z,…]——轨道节点序列全程命令流可生成。工况里列车荷载挂 `c.bcs['Dyna-1']`（按边界条件挂，非 vload）。

## 连接器扣件与节点集 idiom

- [[连接器|connector]] 三件套：connector_behavior（elastic component=7、compressive_stiffness=[39000]×3、tensile 留空=同抗压；damping 'GFE DAMP2' [40,1]×3）+ Orientation（data 九元 [p1,p2,origin]）+ connector_section（`connector_type=(0,3)` 元组=Cartesian+Rotation，set_name 指节点对集合）。
- NSet-Connector-1/2 在官方 py 中是**硬编码节点 ID 交替对**（unsort=True 保序）——GUI"自动搜索"产物的录制回放；换模型须自写最近点配对脚本，此处仍是命令流半断点。
- 钢轨节点集 `node_data()[0][2:]` 切片跳过前两节点（端点留给 BC-liangduan 全约束）；道床节点集用 `mesh_data.find_node_inside(lower,upper)` 包围盒选点，左右必须分建。
- gset_basic 的 `set_shapes_id([[geo_id, dim, tag]])` 中 dim 为 TopAbs 枚举：2=体 4=面 6=线 7=点。

## 经验与陷阱

- 钢轨↔道床用连接器不用绑定（绑死丢扣件隔振柔度）；土-结构/土-隧道/隧道-道床才走搜索接触 [[绑定约束]]。
- 草图中间几何（Geometry-*、切土 Extrude）用完即删，mesh_mgr 与 geo_mgr 两个管理器都要删。
- 官方含录制残留：PickedSet-line-1（12 条边）建而未用、空 search_list 循环——勿当必要步骤。
- 导出疑案裁决：v3.x 官方直接 `writer.set_case('case1').perform()` 出普通 INP，**没有** INPX 专用开关；旧版列车荷载丢失时才考虑 set_trainload2inpx。
- auto_transfinite 官方全开（v3.x），v2.15 实测会崩——版本相关陷阱同 ch10。
