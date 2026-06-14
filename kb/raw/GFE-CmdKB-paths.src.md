# GFE 15 章案例可复现建模路径（命令流步骤链）
> 来源：D:\GFE\GFE_KB（gfe-command-stream skill 维护的命令流知识库）。本文件为 raw 检索源副本，2026-06-10 Fable 二审后刷新（ADR-0001：派生快照随主库可变）。



---
# ===== 路径_ch01_球铰支座.md =====

# 路径_ch01_球铰支座（球铰支座建模分析）

- **case**: 实际案例操作手册 第1章（含§2底座部分）；dump 真值 `04_状态dump/ch01_Chapter1/`；**官方命令流 `E:\GFE2026\典型案例与教程\第1章…\CM1.py`（907行，v3.x，2026-06-11 全文核对）**
- **单位制**: mm–N–t–MPa（密度 t/mm³，E=N/mm²；Cases_c01 行439-453）
- **tier_summary**: ①16 ②2 ③0（官方 py 证实 INP 导出命令流可达，原 S18 ②→①；存盘 .pre 与作业提交仍 GUI ②）
- **分析类型**: 模态 + 静力（弹性，Q345 单材料）

## 1 几何
- **S1 [官方实证v3.x] [①]** 建内外球体：**官方真值 make_sphere(200) / make_sphere(160)（参数=半径）**
  - `sp=occ.brep_prim.make_sphere(200); mgr=Pre.geometry.geo_mgr(); mgr.add(mgr.auto_name('Sphere'), sp)`，随后 `geo_mgr().rename('Sphere-1','ball-200')` **且 mesh_mgr() 同步 rename**（官方 py 每次改名都 geo/mesh 双 rename）
- **S2 [官方实证v3.x] [①]** 布尔裁剪得球壳 `ball`
  - `GFE.geometry.geoprim.builder().cut('ball-200', ['ball-160'], False)` → 产物名 `BoolCut-1`，再 rename 为 `ball`
  - 坑: 裁剪后的几何只是空间贴合、**不传力**，最终必须布尔合并（Cases_c01 ② 行1464/6219）
- **S3 [官方实证v3.x] [①]** 圆柱与圆管系 + 圆阵列。**官方真值尺寸（半径,高）**：pipe1=cut(cyl(100,400),cyl(80,400))；pipe2=cut(cyl(100,300),cyl(80,300)) 再 translate z=-300；pipe3=cut(cyl(75,400),cyl(60,400))；pipe4=cut(cyl(50,400),cyl(40,400))；各管再 cut 掉 'ball-200' 得贴球端
  - `occ.brep_prim.make_cylinder(r, h)`；阵列 `builder.make_round_array(shapes, 2, θ_rad, [0,0,0], axis)`，θ 官方实值 ±0.785398(45°)/±1.0472(60°)/±1.5708(90°)，**弧度制、正负即方向**；shapes 经 `gt.get_shape_by_id(id0,id1,id2)` 由三元组 id 取
  - 坑: 阵列数量 N=2 **含原件**；阵列产物名 Array-1/2 需 rename；官方还用 `builder.rotate([名],基点,轴,角度°,True)` 复制式旋转（末参 True=保留原件复制，产物名 `Trsf-<原名>-N`）
- **S4 [官方实证v3.x] [①]** 底座：箱体+楔形裁剪倒角。**官方真值**：`make_box(800,30,300)` translate(-400,-15,-300)；`make_wedge(30,120,120,0,30,0,0)`（7 参数）经两次 rotate+translate 对位后 cut 出斜角 → base1；`make_box(800,30,215)` 同法 → base2；base1/base2 各 round_array(2, 1.5708, z轴) → base1-1/base2-1；四件再 cut 掉 'columu2-100-xia' 与 'ball-200' 得 *-real
- **S5 [官方实证v3.x] [①]** 布尔合并成总装 `qiujiao`
  - 官方：`builder.merge(['base2-1-real','base2-real','base1-real','base1-1-real','pipe4-2','pipe4-1','pipe3-1','pipe2-1','pipe1-6','pipe1-5','pipe1-4','pipe1-3','pipe1-2','pipe1-1','ball'], False)` 共 15 件 → 产物 `Merge-1` rename 为 `qiujiao`。**本章 merge 第二参=False**（单材料、属性在合并后统一赋）
  - 坑: 单材料本案例可先合并再赋属性；多材料案例必须**先赋截面属性再合并**且 replace=True（Cases_c01 行6587-6591；ch02 官方 py 用 `merge([...], True, '名')` 三参直接命名）

## 2 材料与截面
- **S6 [官方实证v3.x] [①]** 材料 Q345：**官方 py 真值 density=7.8e-09**（与手册正文一致；反推版按 dump 取 7.9e-09——dump v2.15 模型与官方 py 不同源，复建以官方 7.8e-09 为准）
  - `m=GFE.Pre.material.material(); m.name='Q345'; d=GFE.Pre.material.density(); d.temp_dp=False; d.n_param=1; d.params=[7.8e-09]; e=GFE.Pre.material.elastic(); e.temp_dp=False; e.n_param=2; e.type=0; e.moduli_time_scale=0; e.compression=False; e.tension=False; e.params=[206000.0,0.25]; m.entries=[d,e]; GFE.Pre.material.mat_mgr().add(m)`
- **S7 [官方实证v3.x] [①]** 几何集 qiujiao / base
  - 官方全集写法（v3.x `gset_basic`，v2.15 实名 basic_set/gset）：`geo_obj=geo_mgr().find('qiujiao'); shapes=GFE.geometry.geotool.children(geo_obj.shape(), 2); gb=GFE.Pre.set.gset_basic('qiujiao'); gb.set_shapes(shapes); GFE.Pre.set.gset_mgr().add(gb)`（children 第二参 2=体）
  - 官方底面写法：`children(shape,4)`(4=面) 逐面 `centre_of_mass(f)[2] < minz+1e-5` 过滤后 **`gset_mgr().add("base", bottom_face)` 直接 (名,shape列表) 重载**，免 gset_basic 两步
  - 官方注释另给三元组 id 法对照：`gset.set_shapes_id([[47,2,1],...])`（手动 GUI 拾取产物）
  - ⚠manager 实名 `gset_mgr()`（反推版写 gset_manager() 为误记）
- **S8 [官方实证v3.x] [①]** 实体截面
  - `p=GFE.Pre.section.property_solid(); p.name='qiujiao'; p.elset_name='qiujiao'; p.mat_name='Q345'; p.has_thickness=False; p.thickness=1.0; GFE.Pre.section.sect_mgr().add(p)`（官方**不设 p.type**——反推版 type=0 为 dump 回显，可省）

## 3 网格
- **S9 [官方实证v3.x] [①]** 全局四面体网格，尺寸 10mm。官方在**材料/截面/集合之前**先划网格（顺序灵活的实证）
  - `from GFE.geometry import mesh_generator; g=mesh_generator.generator(); c=mesh_generator.controller(); c.number_option={'General.ExpertMode':1.0,'General.NumThreads':0.0,'General.Terminal':1.0,'Mesh.Algorithm':6.0,'Mesh.Algorithm3D':4.0,'Mesh.AngleToleranceFacetOverlap':0.001,'Mesh.ElementOrder':1.0,'Mesh.MeshSizeExtendFromBoundary':1.0,'Mesh.MeshSizeFromCurvature':0.0,'Mesh.MeshSizeFromPoints':1.0,'Mesh.MeshSizeMax':1e+22,'Mesh.MeshSizeMin':0.0,'Mesh.Optimize':1.0,'Mesh.RecombinationAlgorithm':0.0}; c.string_option={}; c.user_option={'GFE.AutoTransfinite':True,'GFE.DefaultSize':10.0,'GFE.Optimize':False,'GFE.Recombine2D':False}; c.geom_to_type={0:0,1:5,2:9,3:14,4:17,5:19,6:20,7:22,8:17}; c.generate_dim=3; c.auto_transfinite=True; g.mesh(['qiujiao'], c)`
  - 坑: 本章官方 Algorithm=6/Algorithm3D=4（ch02/ch03 官方为 2/10）；`auto_transfinite` 在复杂几何上可能崩（KB 已知）

## 4 表面集
- **S10 [官方实证v3.x] [①]** 受压表面集 PRESSURE（官方=程序化筛选"质心距球心 400" 的面，即各管外端面）
  - `surf_mgr=GFE.Pre.surface.surf_mgr(); s=GFE.Pre.surface.geometry_surface('PRESSURE')`；遍历 `children(shape,4)`，`(fx²+fy²+fz²)**0.5≈400` 时 `id=geotool.get_id_by_shape(f)` 收集；**`s.data=[[geo_obj.id(), f[-1], 0] for f in 面id列表]`（[几何体id, 面id, 0=面模式]）**；`surf_mgr.add(s)`
  - ⚠manager 实名 `surf_mgr()`（反推版 surface_mgr() 为误记）；官方注释版另示 GUI 拾取三元组 `obj.data=[[47,79,0],...]` + `to_node_surface=False` 对照

## 5 边界与荷载
- **S11 [官方实证v3.x] [①]** BC-base 全约束：`b=GFE.Pre.boundary.boundary(); b.name='BC-base'; b.type=0; b.set='base'; b.valid_dof=0; b.value=[0.0]*6; b.amplitude=''; b.value_im=[0.0]*6; b.amplitude_im=''; b.distribution=''; b.node_id=[]; b.is_node_set=True; GFE.Pre.boundary.bc_mgr().add(b)`（node_id/is_node_set 两字段仅 CM1 出现，ch02/ch03 官方 py 不写也可）
- **S12 [官方实证v3.x] [①]** PRESSURE 压力：`type=6; set='PRESSURE'(表面集); value=[50.0]`（50 MPa）
- **S13 [官方实证v3.x] [①]** 惯性力自重，**官方名 'GRA'（反推版 'GRE' 为 dump 误读）**：`type=7; set='qiujiao'; value=[0.0,0.0,-9800.0]`
  - **仲裁定案: 官方 py 本章写 -9800（mm 制物理正确），与 dump 一致；手册截图 -9.8 为错印**。但 ch02 官方 py 同 mm 制写 -9.8（两章不一致是官方原始状态，复刻各从其章）；自重叫"惯性力"不叫重力

## 6 分析步 / 工况
- **S14 [官方实证v3.x] [①]** 步：`f=GFE.Pre.step.frequency_step(); f.name='MODAL'; f.description=''; f.nlgeom=False; f.eigen=1`；`st=GFE.Pre.step.static_general_step(); st.name='STATIC'; st.init_inc=1.0; st.period=1.0; st.min_inc=1e-05; st.max_inc=1.0`；各 `GFE.Pre.step.step_mgr().add(...)`
  - ⚠官方 py **eigen=1**（dump v2.15 模型 eigen=10）；官方 STATIC **nlgeom 行被注释**（取默认 False；dump 为 True）——复刻官方教程取官方值，复刻 dump 模型取 dump 值
- **S15 [官方实证v3.x] [①]** 场输出 FieldOutput-1：`o=GFE.Pre.output.output_request(); o.name='FieldOutput-1'; o.step=''; o.type=0; o.method=0; o.time_type=0; o.time_interval=1.0; o.number_interval=0; o.frequency=0; o.var_option=-1; o.time_points=''`；node_output(name='output') `variables=['U','UR']`；element_output(name='output1') **`variables=['E','S']`**（反推版漏 'E'）；两子对象均 `var_option=-1; reg_type=-1; nset/elset=''`；`o.sub_output=[no,eo]; GFE.Pre.output.field_mgr().add(o)`
- **S16 [官方实证v3.x] [①]** 工况 modal / static——**官方为 v3.x 映射属性赋值（可读字典），非 v2.15 set_***
  - `c=GFE.Pre.case.case(); c.name='modal'; c.steps=['Initial','MODAL']; c.bcs['Initial']=['BC-base']; c.bcs['MODAL']=[]; c.initialConditions['Initial']=[]; c.fieldReqs['MODAL']=['FieldOutput-1']; c.histReqs['MODAL']=[]; c.elemAdd['MODAL']=[]; c.elemDel['MODAL']=[]; GFE.Pre.case.case_mgr().add(c)`
  - static 同法：`steps=['Initial','STATIC']; bcs['Initial']=['BC-base']; bcs['STATIC']=['PRESSURE','GRA']; fieldReqs['STATIC']=['FieldOutput-1']`（压力/惯性力同属 bc_mgr）
  - 反推版(dump v2.15)对照：`c.set_bcs('Initial',[...]); c.set_fieldReqs(...)`——v2.15 只有 8 个 set_*(只写)；v3.x 字典可读可改
  - 坑: BC 挂 Initial 步、荷载挂分析步（Cases_c01 行1784/1791）；空步键官方也显式赋 `[]`

## 7 求解与后处理
- **S17 [②]** 保存 .pre：命令流无 save API → GUI File→保存（断点；官方 py 也不存 .pre）
- **S18 [官方实证v3.x] [①]** 导出 INP（官方 py 收尾即此，每工况一份）：`from GFE.io import inpio; w=inpio.writer(inp_path); w.set_case('modal'); w.perform()`；static 同法另一路径。作业创建/提交仍无命令流 API → GUI 分析页签（该子段仍②）
- **S19 [②]** 后处理打开 `<作业名>.db`（非 .pre）→ GUI

# 已知不确定项
- ~~全部几何精确尺寸未知~~ **已解决**：官方 py 给出全部尺寸真值（见 S1-S5）
- ~~PRESSURE 表面集 8 个面的几何语义~~ **已解决**：质心距球心 400 的管外端面（S10）
- 手册 -9.8 vs -9800 矛盾**已由官方 py 仲裁**：ch1=-9800、ch2=-9.8，两章不一致是官方原始状态
- 官方 py 与 dump v2.15 模型存在参数分叉（density 7.8e-09 vs 7.9e-09；eigen 1 vs 10；nlgeom 默认 vs True）——两者均"真"，源不同；新建模型以官方 py 为准
- CM1.py 头部 import/set_application_by_ui() 重复 9 次为录制残留，复用时保留一组即可


---
# ===== 路径_ch02_钢骨混凝土柱.md =====

# 路径_ch02_钢骨混凝土柱（钢骨混凝土柱建模分析）

- **case**: 实际案例操作手册 第2章；dump 真值 `04_状态dump/ch02_section/`；**官方命令流 `E:\GFE2026\典型案例与教程\第2章…\CM2-update2.py`（700行，v3.x 参数化，2026-06-11 全文核对）**
- **单位制**: mm–N–t–MPa（Q345 ρ=7.8e-9 t/mm³、E=206000 MPa）
- **tier_summary**: ①17 ②2 ③0（官方 py 证实 INP 导出可达，原 S19 拆出①；存盘 .pre 与作业提交仍 GUI ②）
- **分析类型**: 模态 + 静力（弹性；型钢+钢筋笼嵌入混凝土柱）
- **官方参数真值**: 工字钢 400×400 t=20；模型高 4000；混凝土柱 600×600；箍筋方框 500×500 @100；主筋长 4000 @500 四角；箍筋截面 r=6.0、主筋 r=12.5；压力 钢翼缘 2 / 柱顶 20 MPa；网格 50

## 1 几何
- **S1 [官方实证v3.x] [①]** 草图画工字钢截面——官方 draft 真实 API 与反推版不同，**以官方为准**：
  - `d=GFE.draft.get_current(); d.set_normal([0,0,0],[0,0,1],[1,0,0])`（三向量：原点/法向/X向，非反推版 set_normal(2)）；`d.set_snap_object(0); d.set_operate_mode(3)`（3=矩形模式）；`d.input(x,y)`×2 为矩形对角点，三个矩形叠出工字
  - 选择/编辑：`d.set_snap_object(2)`（2=线）→ `d.snap_object(x1,x2,y1,y2)` 框选（或 `d.snap_object(x,y)` 点选）→ `d.select_snaped(True/False)` → `d.split_selected()` 线段打断 / `d.remove_selected()` 删除重合线（重合线要删**两次**）/ `d.fill_selected()` 填充
  - 完成：`shape=d.export(); GFE.Pre.geometry.geo_mgr().add('section-steel', shape)`；填充后官方把轮廓线 remove_selected 只留填充域
  - 反推版(dump v2.15)对照注：`d.add_line/select_line` 写法未在官方 py 出现，作废
  - 坑: 草图误触遗留点/线会致 fill 失败（"Failed to fill area"，Cases_c01 行5659）
- **S2 [官方实证v3.x] [①]** 拉伸成型钢 + 复制对位成十字钢骨
  - `extruded=builder.extrude([find('section-steel').shape()], [0,0,4000])` → add('I-steel')；复制 `builder.make_array(shapes,2,1,1,[0,0,0])` → 'I-steel-1' → `builder.rotate(['I-steel-1'],[0,0,0],[1,0,0],90.0,False)`
  - **新 idiom（形心对位）**：`c1=geotool.centre_of_mass(find('I-steel').shape()); c2=...('I-steel-1')...; builder.translate(['I-steel-1'], [c1[i]-c2[i] for i in range(3)], False)`——用质心差向量精确对中
- **S3 [官方实证v3.x] [①]** 混凝土柱箱体
  - `sp=occ.brep_prim.make_box(600,600,4000); geo_mgr().add('concrete-pillar', sp)`（官方名带连字符，非空格），再形心对位平移到钢骨中心
- **S4 [官方实证v3.x] [①]** 箍筋/主筋：草图线 + make_array + 程序化删重叠
  - 箍筋：`d.clear()` 清草图 → operate_mode(3) 两角点画 500×500 矩形线框（不填充）→ export → `builder.make_array(shapes,1,1,41,[0,0,100])`（z 向 41 份 @100）；**首尾 2 片 + 与中部钢骨重叠段（z∈模型半高±钢骨半高）经 centre_of_mass 程序化筛出后 geo_mgr().delete + mesh_mgr().delete**
  - 主筋：`d.set_normal([0,0,0],[0,-1,0],[1,0,0])`（xz 平面）→ operate_mode(1)（1=直线）两点画 4000 竖线 → export → translate 到角点 → `make_array(shapes,2,2,1,[500,500,0])` 得 4 根
  - 坑: 阵列数含原件；官方用名字列表 (stirrup_names/reinforcing_bar_names) 全程追踪阵列产物，反推版"按 Array 序号对齐"的顾虑在参数化脚本中不存在
- **S5 [官方实证v3.x] [①]** 钢筋笼集合 `reinforcement-cage`（嵌入的前置；官方名带连字符）
  - **官方新 idiom（集合并集）**：`id1=gset_mgr().find('stirrup').get_shapes_id(); id2=...('reinforcing-bar')...; gb=gset_basic('reinforcement-cage'); gb.set_shapes_id(id1+id2); gset_mgr().add(gb)`——由两个既有 gset 的 id 并集合成
  - 另有同名**几何** merge：`builder.merge(stirrup_names+reinforcing_bar_names, True,'reinforcement-cage')`（划网格用对象）
  - 坑: 嵌入区域顺序硬依赖——**先**建钢筋笼集合**再**建 Embed（Cases_c02 ②）；官方流程实序：截面→合并几何→…→嵌入→工况→网格

## 2 材料与截面
- **S6 [官方实证v3.x] [①]** 材料 Q345(7.8e-09, 206000, 0.25)、C40(2.5e-09, 32500, 0.2)
  - `material()+density()+elastic()` 同 ch01 S6 范式，`mat_mgr().add`；官方用 `materials=[(名,ρ,E,ν),...]` 参数表驱动
- **S7 [官方实证v3.x] [①]** 实体截面 concrete(C40)/steel-steel(Q345)：`property_solid; has_thickness=False; thickness=1.0`（官方不设 type，反推版 type=0 为 dump 回显）
- **S8 [官方实证v3.x] [①]** 梁截面 stirrup（箍筋 r=6.0 圆形）与 reinforcing-bar（纵筋 r=12.5）
  - `pb=GFE.Pre.section.property_beam(); pb.name='stirrup'; pb.elset_name='stirrup'; pb.shape=3; pb.mat_name='Q345'; pb.fiber_num=1; pb.shape_params=[6.0]; pb.params=[]; pb.direction=[0.0,0.0,1.0]; pb.shear=[8.3873e+06,8.3873e+06]; pb.Ecc=[0.0,0.0,0.0,0.0]; GFE.Pre.section.sect_mgr().add(pb)`；纵筋 `shape_params=[12.5]; direction=[1.0,0.0,0.0]; shear=[3.64032e+07,3.64032e+07]`（官方不设 pb.type）
  - 坑: 梁 direction 因构件轴向而异（水平箍筋 (0,0,1)、竖向纵筋 (1,0,0)），统一填会错（Cases_c02 ②）；shear 为软件按截面自动算的回显值，命令流须显式写入
- **S9 [官方实证v3.x] [①]** 几何集：体集 concrete/steel-steel 用 `children(shape,2)`+gset_basic.set_shapes；线集 stirrup/reinforcing-bar 遍历各线几何 `children(shape,6)`(6=边) 汇总；底面集 bc-base 用 `children(shape,4)`+最低 z 质心过滤后 `gset_mgr().add('bc-base', faces)` 直接重载；全集 All 同体集法
  - ⚠manager 实名 `gset_mgr()`；官方集合名全部连字符（无空格）
- **S10 [官方实证v3.x] [①]** 先赋属性再合并混凝土与型钢（共节点传力）——官方实序确证：cut/merge 命名→材料→集合→截面→**再 merge**
  - **官方新 idiom（布尔直接命名）**：`builder.cut('concrete-pillar', ['I-steel-1','I-steel'], False, 'concrete')`（第4参=结果名）；`builder.merge(['I-steel','I-steel-1'], True, 'steel-steel')`（第3参=结果名，第2参 True=替换）——免 ch01 的 BoolCut-1/Merge-1 rename 两步舞
  - 总装：`builder.merge(['concrete','steel-steel'], True,'steel-concrete')` 在 4 个截面全部 add 之后执行
  - 坑: **顺序硬依赖**——先逐一赋截面属性再 merge 且替换=True，否则合并体属性归属不明（Cases_c01 行6587-6591）

## 3 相互作用
- **S11 [官方实证v3.x] [①]** 嵌入区域 Embed-1（钢筋笼→混凝土）
  - `e=GFE.Pre.interaction.embed(); e.id=1; e.name='Embed-1'; e.host_name='concrete'; e.roundoff_tolerance=1e-6; e.exterior_tolerance=0.05; e.embedded_names=['reinforcement-cage']; GFE.Pre.interaction.embed_mgr().add(e)`
  - ⚠manager 实名 `embed_mgr()`（反推版 embed_manager() 为误记）；官方多写 `e.id=1` 字段

## 4 网格
- **S12 [官方实证v3.x] [①]** 全局四面体 50（DefaultSize=50.0），**官方 Algorithm=2.0 / Algorithm3D=10.0**（与 ch01 的 6/4 不同），全量字典同 ch01 S9 范式
  - 官方分两次划：`generator.mesh(['steel-concrete'], c)` + `generator.mesh(['reinforcement-cage'], c)`；且**网格划分放在嵌入/工况定义之后、INP 导出之前**（顺序灵活实证）
  - 坑: 平面内嵌线不会自动划梁单元（本章钢筋为独立线几何不受此限，华夫板案例受限）

## 5 表面集 / 边界荷载
- **S13 [官方实证v3.x] [①]** 表面集 pressure（工字钢上翼缘 2 面：z≈钢骨顶 ±1 且 |y|>柱半宽）/ pressure-2（柱顶=maxz 全部面）：`geometry_surface + surf_mgr().add`；faceid 经 `children(shape,4)`+质心条件+`get_id_by_shape` 筛选；`obj.data=[[geo_obj.id(), f[-1], 0] for f in 面id]`
  - ⚠官方名 'pressure-2'（带连字符）；manager 实名 `surf_mgr()`
- **S14 [官方实证v3.x] [①]** BC 四件：BC-base(type=0 全约束, set='bc-base', value 6 零)；GRA(type=7 惯性力, set='All', value=[0,0,-9.8])；PRESSURE(type=6, set='pressure', value=[2])；PRESSURE-2(type=6, set='pressure-2', value=[20])
  - **仲裁定案: 官方 py 本章确写 -9.8**（与 dump 一致；ch01 官方写 -9800——两章不一致是官方原始状态。按"复现本章案例"取 -9.8、按"物理正确 mm 制"取 -9800，择一须声明）

## 6 分析步 / 输出 / 工况
- **S15 [官方实证v3.x] [①]** Static-1（nlgeom=False, init/max_inc=1.0, min_inc=1e-05, period=1.0）+ Modal-1（eigen=10）；`step_mgr().add`
- **S16 [官方实证v3.x] [①]** FO-Static（"静力"预设的展开真值）：node ['U','UR','RF','RM'] + element ['E','S','SF','SM']；`o.step='Step-1'; o.time_type=0; o.time_interval=1.0`
  - 坑: GUI"加载预设"按钮不可命令流触发，但预设内容已知可直接写 variables（等效①）；**官方 py 也写 step='Step-1'**——确证为无害遗留串，照抄即可
- **S17 [官方实证v3.x] [①]** 工况 **model**(['Initial','Modal-1'])/static(['Initial','Static-1'])——v3.x 映射属性赋值：
  - `c.bcs['Initial']=['BC-base']; c.bcs['Modal-1']=[]; c.initialConditions['Initial']=[]; c.fieldReqs['Modal-1']=['FO-Static']; c.histReqs/elemAdd/elemDel=[]`；static 另 `c.bcs['Static-1']=['GRA','PRESSURE-2','PRESSURE']`
  - ⚠官方模态工况名是 'model'（疑 'modal' 笔误，照抄可复现）；反推版 set_bcs 写法为 v2.15 对照
  - 坑: 模态工况只挂 BC+输出不挂荷载；同一 BC 池按工况裁剪复用（Cases_c02 ②）

## 7 求解
- **S18 [②]** 保存 .pre（GUI；软件"闪退现象较多"，每阶段后手动存盘 checkpoint—Cases_c02 行9347）
- **S19 [官方实证v3.x] [①]** 导出 INP：`inpio.writer(path); set_case('static'/'model'); perform()` 每工况一份（官方 py 收尾）。创建作业+提交+后处理开 .db 仍 GUI（该子段仍②）

# 已知不确定项
- ~~工字钢轮廓/柱尺寸/钢筋布置未知~~ **已解决**：官方 py 参数区给全（见头部"官方参数真值"）
- ~~steel-concrete 等集合成员划分~~ **已解决**：见 S9/S10 官方构造法
- 自重 -9.8 与单位制矛盾**已由官方 py 确证为官方原始状态**（本章 -9.8 / ch01 -9800）
- 官方箍筋初始阵列 41 片删首尾+中部重叠后的精确留存数取决于参数（脚本 print 自检），非固定值


---
# ===== 路径_ch03_华夫板框架频响.md =====

# 路径_ch03_华夫板框架频响（wafer-ssd 频响分析）

- **case**: 实际案例操作手册 第3章；dump 真值 `04_状态dump/ch03_wafer/`；**官方命令流 `E:\GFE2026\典型案例与教程\第3章…\CM3-update2.py`（605行，v3.x 参数化，2026-06-11 全文核对）**
- **单位制**: m–t–kPa（C30 ρ=2.5 t/m³、E=3e7 kPa=30 GPa）
- **tier_summary**: ①11 ②2 ③0（官方 py 证实：几何全程草图重建①、"复制网格"有 copy_mesh API①、INP 导出①；存盘 .pre/作业提交与后处理仍 GUI ②）
- **分析类型**: 稳态动力学（频响 1–50 Hz，直接法）
- **官方参数真值**: 华夫板 48×48×0.5；孔组 6×6、每组 8×8 孔 r=0.25 @0.9（=2r+0.4），首孔偏移=(组距-(n-1)·孔距)/2 取整 4 位；筏板 48×48 @z=-4（壳 t=0.3）；屋面板 @z=+4（壳 t=0.15）带 5×5 内梁线；柱 7×7 根高 8（梁柱 0.8×0.3 / 柱 0.6×0.6）；网格 1.0、华夫板线控 0.5

## 1 几何/网格
- **S1 [官方实证v3.x] [①]** 几何全程草图参数化重建——**官方 py 不走 open_inp**；dump 模型（InpMesh-1）是发布态 .pre 用 INP 导入的产物，两条路径都真，**复建以官方草图路径为准**
  - 华夫板：xy 草图 `set_normal([0,0,0],[0,0,1],[1,0,0])` → 矩形 operate_mode(3) 两角点 → 圆 operate_mode(7) 圆心+半径点两次 input → **草图内阵列** `set_operate_mode(14); array_selected(nx,ny,dx,dy)`（先选中：set_operate_mode(-1)+set_snap_object(2)+snap_object+select_snaped(False)）→ 单孔阵 8×8 → 框选整组再阵 6×6 → `fill_selected()` 填充 → **set_snap_object(4)(4=面) 框选全部圆面 remove_selected() 挖孔** → export → `builder.extrude(shapes,[0,0,0.5])` → 'wafer'
  - 筏板：`d.clear()` → 矩形+fill → export 'raft' → `translate(['raft'],[0,0,-4.0],False)`（**仲裁: 官方平移 -4.0，"拉伸-0.4m"为手册正文错印**）
  - 屋面板：在筏板草图上加内梁线（operate_mode(1) 直线 + array_selected 5×1/1×5）→ export 'roof' → translate z=+4.0
  - 柱：xz 平面草图 `set_normal([0,0,0],[0,-1,0],[1,0,0])` 直线(0,+4)→(0,-4) → export 'column' → `make_array(shapes,7,7,1,[8,8,0])`，col_names 列表追踪
  - 总装：`builder.merge(['wafer','raft','roof']+col_names, True,'')`（名传空串 → 产物 'Merge-1'）
- **S2 [官方实证v3.x] [①]** 激励节点集 Set-cload——官方**程序化坐标查找**，非硬编码节点号：
  - `n=GFE.Pre.set.nset(); n.name='Set-cload'; fm=GFE.Pre.mesh.mesh_mgr().find('Merge-1'); nd=fm.node_data()`（nd[0]=节点号列表, nd[1]=坐标列表）；目标坐标=华夫板顶面（children(shape,4) 取 maxz 面）质心；逐节点 ±0.1 容差匹配收集 → `n.data=need_nodes; n.unsort=True; GFE.Pre.set.nset_mgr().add(n)`
  - 反推版(dump)对照：`n.data=[75286]` 硬编码——与特定 INP 网格绑定，作废；⚠manager 实名 `nset_mgr()`
  - 坑（官方 py 自注）: 改参数重划网格后该坐标可能无节点命中，须微调容差/参数
- **S3 [官方实证v3.x] [①]** "复制网格"建 B31 屋面梁单元——**v3.x 有命令流 API（原判②断点撤销；v2.15 未见此 API 仍断点）**
  - `GFE.geometry.geotool.copy_mesh(name="beam", origin_node=True, as_source=True, type_name="B31", new_set_name="beamb31-1")`
  - 配套改截面归属（manager edit idiom）：`sm=GFE.Pre.section.sect_mgr(); o=sm.find('beam'); o.elset_name='beamb31-1'; sm.edit(o)`
  - 背景: 平面内嵌的梁线划网格时不会生成梁单元，须复制网格另建 B31 集
- **S3b [官方实证v3.x] [①]** 网格划分（含**线控制局部加密**新 idiom）
  - 0.5mesh 边集：遍历 Merge-1 `children(shape,6)` 取 z∈[0,板厚] 的边 → `gset_mgr().add('0.5mesh', edges)`，同时收集 `get_id_by_shape` 的 id
  - `cc=mesh_generator.curve_control(); cc.set_name='0.5mesh'; cc.edges={geo_id:[edge_id,...]}`（由 id 三元组转 {几何id:[末位边id]} 字典）`; cc.density=0.5; controller.size_option=[cc]`
  - 全局 DefaultSize=1.0、Algorithm=2.0/Algorithm3D=10.0（同 ch02），`generator.mesh(['Merge-1'], controller)`

## 2 材料与截面
- **S4 [官方实证v3.x] [①]** 材料 C30：`density=[2.5]; elastic=[3e+07, 0.2]`（material+mat_mgr 范式；官方名 'C30'，dump 'c30'）
- **S5 [官方实证v3.x] [①]** 截面 5 件（全部 mat_name='C30'，官方均不设 type 字段）
  - wafer: `property_solid; elset_name='wafer'; has_thickness=False; thickness=1.0`（反推版照 dump 写 0.0；官方 1.0，两者均不生效于实体）
  - raft: `property_shell; thickness=0.3; integral_point=5; layer_num=1; params=[]; has_rebar=False; Ecc=[0,0,0,0]`；roof 同 raft 但 `thickness=0.15`
  - col: `property_beam; shape=0(矩形); shape_params=[0.6,0.6]; direction=[1.0,0.0,0.0]; shear=[3.75e+06,3.75e+06]`
  - beam: `property_beam; shape=0; shape_params=[0.8,0.3]; direction=[0.0,0.0,1.0]; shear=[2.5e+06,2.5e+06]`，划网格后 elset_name 改 'beamb31-1'（见 S3）
  - 坑: 梁方向柱(1,0,0)/水平梁(0,0,1)；shear 为自动算回显值须显式写

## 3 边界与频响激励
- **S6 [官方实证v3.x] [①]** 底部全约束——官方名 'BC-base'：`type=0; set='base'; value=[0.0]*6`（base 集=Merge-1 最低 z 单面，children(4)+minz 过滤；反推版 dump 名 Encastre-1、value=[] 空列表形态，两形态都合法）
- **S7 [官方实证v3.x] [①]** 频响集中荷载——**官方仲裁：单个 BC 对象同时携带实部+虚部**，非 dump 的双对象：
  - `b=GFE.Pre.boundary.boundary(); b.type=5; b.name='BC-cload'; b.set='Set-cload'; b.valid_dof=4; b.value=[0.0]*6;`（实部全零）`b.amplitude=''; b.value_im=[0.0,0.0,1.0,0.0,0.0,0.0];`（**虚部 Z 向单位力——value_im 就是 boundary 的平行字段**）`b.amplitude_im=''; b.distribution=''; GFE.Pre.boundary.bc_mgr().add(b)`
  - 反推版(dump)对照：CForce-Set-cload（实部全零）+ CForce-Set-cload-1（虚部）两对象——GUI 操作副产物，命令流一个对象即可
  - 坑: "幅值函数2/虚部"（amplitude_im/value_im）仅频响分析有效

## 4 分析步 / 输出 / 工况
- **S8 [官方实证v3.x] [①]** 稳态动力步 SSD-1
  - `s=GFE.Pre.step.steady_dyn_step(); s.name='SSD-1'; s.description=''; s.nlgeom=False; s.direct=True; s.interval=1; s.scale=1; s.data=[[1.0, 50.0, 10.0, 1.0, 1.0, 0.1]]; gd=GFE.Pre.step.global_damping(); gd.alpha=0.0; gd.beta=0.0; gd.field=0; gd.structual=0.02; s.global_damping=gd; GFE.Pre.step.step_mgr().add(s)`
  - 真值：fmin=1, fmax=50, 频率点 10, 直接法, 结构阻尼 0.02；⚠**data 行后两列官方=1.0/0.1，dump=0.0/0.0**——字段语义仍无手册佐证，复刻官方教程照抄 1.0/0.1
- **S9 [官方实证v3.x] [①]** 场输出 FieldOutput-1：node ['U']；`o.time_type=2; o.time_interval=0.0; o.frequency=1; o.step=''; o.method=0; o.var_option=-1`；node_output `reg_type=-1; nset=''`（反推版 reg_type=1 为 dump 形态）
  - 坑: 场输出"频率=1"是**每 1 个求解点输出一次**的间隔语义，不是 1 Hz（Cases_c03 ②）
- **S10 [官方实证v3.x] [①]** 工况 **ssd**（官方名；dump 名 Case-1）——v3.x 映射属性赋值：
  - `c=GFE.Pre.case.case(); c.name='ssd'; c.steps=['Initial','SSD-1']; c.bcs['Initial']=['BC-base']; c.bcs['SSD-1']=['BC-cload']; c.initialConditions['Initial']=[]; c.fieldReqs['SSD-1']=['FieldOutput-1']; c.histReqs['SSD-1']=[]; c.elemAdd['SSD-1']=[]; c.elemDel['SSD-1']=[]; GFE.Pre.case.case_mgr().add(c)`
  - 反推版 set_bcs 写法为 v2.15 对照

## 5 求解与后处理
- **S11 [官方实证v3.x] [①]** 导出 INP：`inpio.writer(inp_path); set_case('ssd'); perform()`（官方 py 收尾）。保存 .pre + 创建作业提交仍 GUI（②，同 ch01 S17/S18）
- **S12 [②]** 后处理 XY 曲线（GUI）
  - 坑: 频响结果曲线横轴标签写"时间"实为**频率扫描点**（1→50 Hz）（Cases_c03 ②）

# 已知不确定项
- steady_dyn_step.data 行 6 列：前三列=fmin/fmax/点数，第 4 列 1.0（疑=缩放方式枚举）；**第 5/6 列官方 1.0/0.1 与 dump 0.0/0.0 分叉**，语义无手册条目佐证——改频响参数只动前三列，其余照抄所复刻源
- ~~激励实部全零对象的必要性~~ **已解决**：官方单对象 value+value_im 并存，双对象是 GUI 副产物
- ~~INP 源文件来源~~ **已定性**：发布态 .pre 为 INP 导入；官方命令流为全草图重建，m05/mesh05 集合仅存在于 INP 路径
- ~~筏板 -0.4 vs -4 矛盾~~ **已仲裁**：官方 py translate -4.0


---
# ===== 路径_ch04_核电站动力.md =====

# 路径_ch04_核电站动力（核电站结构 SSI 显式动力分析）

- **case**: 实际案例操作手册 第4章；dump 真值 `04_状态dump/ch04_section/`；**官方命令流 `E:\GFE2026\典型案例与教程\第4章 核电站土-结构动力分析案例\CM4-update2.py`（1345 行，v3.x，2026-06-11 通读对账）**
- **单位制**: m–t–kPa（C40_PLANT ρ=2.6 t/m³、E=3.25e7 kPa；土 E~1.7e5 kPa）
- **tier_summary**: ①16 ②1 ③0（官方命令流落地后：S4 预设库②→①绕过、S2 残留面②→①clear() 规避；仅 S17 的保存 .pre/提交作业仍 GUI ②）
- **分析类型**: 显式动力（人工边界+一维场地反应输入，弹性壳结构+均匀分层土）
- ⚠ 版本注: 本文件 [官方实证v3.x] 写法面向 E:\GFE2026 v3.x；**本机 D:\GFE PrePo v2.15 无 data_builder/工况映射赋值等 v3.x API**，v2.15 复现须退回 set_* 与逐层手工建土。

## 1 几何（厂房+安全壳+土体）
- **S1 [官方实证v3.x]** 草图厂房墙线（XY 平面）：draft 是**状态机**，不是 add_polyline/add_line 一类方法（反推对照注：旧记 `d.add_polyline/add_line` 写法不存在，以官方为准）
  - `d=GFE.draft.get_current(); d.set_normal([0,0,0],[0,0,1],[1,0,0])`（origin/normal/xdir 三向量，**不是 set_normal(2)**）
  - 画图序：`d.set_snap_object(0); d.set_operate_mode(mode); d.input(x,y)…`；mode 真值：**1=直线(两点一组), 2=多段折线(连续), 4=圆弧(端点接续), 5=三点圆弧(圆心,起,终), 7=圆(圆心,半径点), -1=选择模式**
  - 填充成面：`d.set_operate_mode(-1); d.set_snap_object(2); d.snap_object(边中点x,y); d.select_snaped(True)`（逐边捕捉外环，用相邻两点中点定位）→ `d.fill_selected()`；取消选择 `d.snap_object(0,0); d.select_snaped(False)`
  - 收尾：`shp=d.export(); GFE.Pre.geometry.geo_mgr().add('plant-down-wall-base', shp)`（官方命名 plant-down-wall-base/raft/plant-up-wall-base/plant-up-slab，非 Geometry-N）
  - 外轮廓 13 点多段线 (-50,50)…(-50,50) + 20 条内墙直线（坐标全表见官方 py L40-81）
- **S2 [官方实证v3.x]** 拉伸墙体+楼层阵列：`builder=GFE.geometry.geoprim.builder(); builder.extrude([shape],[0,0,8])`；1-5 层 `make_array(shapes,1,1,5,[0,0,8])`；6-8 层 `extrude(...,[0,0,6])`+`make_array(...,1,1,3,[0,0,6])`
  - 草图落位偏移：**export 前 `set_normal([0,0,offset],[0,0,1],[1,0,0])`**——6-8 层墙基 offset=40（5×8），6-8 层楼板 offset=46（40+6）
  - 阵列产物命名：`name=mgr.auto_name('plant-down-wall'); mgr.add(name,sp)` 并收集 names 列表供后续 merge/gset
  - 坑（官方注释明示）: 手册 GUI 是"选面和线删除"清残留；**命令流优化为 `d.clear()` 清空草图重画**——残留面断点被绕过（原②注作废）
  - 2 层楼板开洞：阵列 raft 得 plant-down-slab → 草图画圆 r=25 填充、offset=8 export 为 plant-down-slab-cut → `builder.cut('plant-down-slab',['plant-down-slab-cut'],True)`
- **S3 [官方实证v3.x]** 安全壳：母线=多段折线 (0,0)(24,0)(24,55) + mode=4 圆弧 (24,55)(18,70)(0,78)，XZ 平面 `set_normal([0,0,0],[0,-1,0],[1,0,0])`；`builder.revolve([shape],[0,0,0],[0,0,1],6.28319)` → 'shell'
  - 合并：`builder.merge(merge_names, True, 'plant')`——**三参带新名**，合并体官方名 'plant'（反推对照注：dump 名 Merge-1 是 GUI 自动名）；merge 前已建好 gset+材料+截面（先属性后合并铁律官方证实）
- **S4 [①，官方实证绕过]** CDP 预设库（GUI 材料库按钮）官方命令流**不用**：直接构造 density+elastic+damping 三 entry（见 S5）。v3.x 命令流可达；预设库读取 API 两代均无。
- **S5 [官方实证v3.x]** 命令流直接建厂房材料（entries 组装范式）
  - `obj=GFE.Pre.material.material(); obj.name='C40_PLANT'`
  - `d=GFE.Pre.material.density(); d.temp_dp=False; d.n_param=1; d.params=[2.6]`
  - `e=GFE.Pre.material.elastic(); e.temp_dp=False; e.n_param=2; e.type=0; e.moduli_time_scale=0; e.compression=False; e.tension=False; e.params=[3.25e7,0.2]`
  - `dp=GFE.Pre.material.damping(); dp.n_param=2; dp.params=[0.948805,0.0]`
  - `obj.entries=[d,e,dp]; GFE.Pre.material.mat_mgr().add(obj)`；C60_PLANT 同构 E=3.6e7
  - 坑: α=2ζω₁（ζ=0.05，模态先行）；**β 恒 0**（显式稳定铁律）；官方脚本 α=0.948805 vs dump/INP 0.9469011585 微差（两次模态结果），复现取其一即可
- **S6 [官方实证v3.x]** 土层材料 4 种：`GFE.io.get_current().import_mat(gmat_path)` 导入 nol-soil.gmat
  - gmat 内每材料含 Density+Elastic+**TestData（EERA 试验曲线 G/Gmax-γ、ζ-γ）**，**无 damping entry**——土层 Rayleigh α 不手写，由场地反应 EERA 自动生成（见 S14 坑）
  - 无 gmat 时手工构造 test_data 同旧记（dump material_mat_mgr.txt 真值：ρ=1.94/1.95/1.87/2.13, E=170180.87/406051/634828/1226880, ν=0.42/0.3/0.25/0.25）

## 2 一维土层与快速建土
- **S7 [官方实证v3.x]** 一维土层 Soil1D-1
  - `s=GFE.Pre.soil.soil(); s.name='Soil1D-1'; s.depth=[2.42,32.4,4.0,23.8]; s.materials=['sutiantu','lizhinianxingtu','quanfenghuahuagangyan','qiangfenghuahuagangyan']; s.bedrock_mat=s.materials[-1]; s.depth_dir=2; GFE.Pre.soil.soil_mgr().add(s)`
  - 官方 manager 短名 **soil_mgr()**（反推对照注：旧记 soil_manager() 为 v2.15 别名习惯，v3.x 官方一律 *_mgr()）
  - **bedrock 官方=qiangfenghuahuagangyan（materials[-1] 最深层）**——旧记 quan… 有误，以官方为准
- **S8 [官方实证v3.x]** 快速建土 → Soil-1：**box_builder + data_builder 两段式**（重大修正）
  - `b=GFE.soil.box_builder(); so=GFE.Pre.soil.soil_mgr().find('Soil1D-1'); b.set_height(so.depth, so.depth_dir); b.set_parameter(300, 300); soil_shape=b.build()`
  - `b2=GFE.soil.data_builder(); b2.dimension=3; b2.name='Soil-1'; b2.layer_shape=soil_shape; b2.layer_material=so.materials; b2.build()`——**自动建几何+逐层集合+实体截面**，无须手工 geo_mgr().add/gset/property_solid（反推对照注：旧记"逐层手工补"作废；⚠ v2.15 无 data_builder，仍须手工逐层）
  - **set_height 仲裁**：官方直接传 `so.depth` 原序=**从上到下（表层 sutiantu 在前）**，与 materials 同序对位——旧记"高度列表从下到上（Cmd 坑88）"在 v3.x 官方用法下不成立，以官方为准；LayerProp-1=表层 sutiantu 不变
- **S9 [官方实证v3.x]** 挖地下室：raft `extrude([raft.shape()],[0,0,16])` → 'plant-basement'；对位=取 Soil-1 **最高面形心** center1（geotool.children(shape,4) 遍历 centre_of_mass 取 z 最大），目标 center2=[0,0,16]，`builder.translate(['Soil-1'], 差向量, False)`；`builder.cut('Soil-1',['plant-basement'],True)`
  - 坑: cut 第三参 True=替换原图形保住已赋材料（官方证实）

## 3 网格 / 相互作用
- **S10 [官方实证v3.x]** 网格：mesh_generator.generator()+controller()；厂房/壳 size=1.0、土 size=8.0（user_option `GFE.DefaultSize`），`Mesh.Algorithm:2, Mesh.Algorithm3D:10(土:1), ElementOrder:1`，`GFE.AutoTransfinite:True, controller.generate_dim=3, controller.auto_transfinite=True`；`generator.mesh(['plant'/'shell'/'Soil-1'], controller)`
- **S11 [官方实证v3.x]** 搜索接触批量建 Tie（plant-shell 一批 + Soil-1-plant 一批，合计即 47 对的来源）
  - `from GFE.geometry import contact_pair as cp; cplist=cp.search_face('Soil-1','plant',0.01)`——**容差官方 0.01**（反推对照注：旧记 0.1 取自 Cmd 示例，案例真值 0.01）
  - 循环每对: `master=GFE.Pre.surface.geometry_surface('CP-{geo1}-{geo2}-{i}-master'); master.data=[[geoid]+list(x) for x in pairs[0]]; surf_mgr.add(master)`（slave 同构）→ `sp=GFE.Pre.interaction.surface_pair(); sp.name=tie_mgr.auto_name('Tie'); sp.first_surf=…; sp.second_surf=…; sp.param_number=1; sp.parameters=[0.01]; GFE.Pre.interaction.tie_mgr().add(sp)`
  - 坑: SSI 界面用绑定非摩擦接触；BOPAlgo 自相交告警刷屏非致命

## 4 人工边界与地震输入
- **S12 [官方实证v3.x]** 土体四周+底面表面集 TUTIAROUND
  - 包围盒 `geotool.get_shape_box_range(shape,0.0)` → 6 极值；遍历 `geotool.children(shape,4)` 按面形心与极值差 < 容差1 归入 front/back/left/right/bottom 五组
  - 每组 `gset_mgr().add(gset_name, faces)`（重名先 `gset_mgr().delete([name])`）→ `gset.get_shapes_id()` 取 id 元组，转 `[[t[0], t[2], 0], …]`（**取元组第0、第2位+0=面模式**）
  - `srf=GFE.Pre.surface.geometry_surface('TUTIAROUND'); srf.data=汇总列表; GFE.Pre.surface.surf_mgr().add(srf)`（官方两别名并存：surf_mgr()/surface_mgr() 同文件均出现，皆可用）
- **S13 [官方实证v3.x]** 地震波幅值（1001 点 dt=0.02 → value 平铺 2002 长）
  - `a=GFE.Pre.amplitude.amplitude(); a.type=0; a.name='25_RH1TG025_(RenGong_T_025)_x_Zhu'; a.spectrum_type=-1; a.gravity=0.0; a.value=[0.0,0.0048, 0.02,0.0053, …]; GFE.Pre.amplitude.amp_mgr().add(a)`
  - 坑: GUI"预设"波库按钮无命令流对应，官方就是把波形数据**硬编码平铺**进脚本；幅值对象属性须全赋
- **S14 [官方实证v3.x]** 场地反应荷载 VibLoad-1（**新增 14 个 set_parameter EERA 真值，旧记缺失**）
  - `v=GFE.Pre.vibration.vibra_load(); v.name='VibLoad-1'; v.amp_bottom_x='25_RH1TG025_(RenGong_T_025)_x_Zhu'; v.amp_bottom_y=''; v.amp_bottom_z=''; v.pwave_dir=2; v.soil='Soil1D-1'; v.is_outcrop=True; v.input_loc=-1; v.level=0`
  - `v.set_parameter(k,v)` 真值表：`DampConvOrder='1', DampScale='1', MaxIter='100', N='4096', Rr='0.5', SubLayerHeight='1', TimeInterval='0.02', Tol='1e-2', UI_ARBot='', UI_ARTop='', UI_Method='0', UseAmp='true', UseEERAMat='true', UseIntgOutp='true'`；`GFE.Pre.vibration.vib_mgr().add(v)`
  - **坑/机制（INP 实证）**: `UseEERAMat='true'` → 导出 INP 时自动生成 `<土材料名>-EERA` 派生材料并写入逐层等效 `*Damping, Alpha=…, Beta=0`（本案例 sutiantu 0.2821/lizhi 0.6191/quanfenghua 0.4771/qiangfenghua 0.7341）——**土层 α 逐层赋值不在命令流手写，由 EERA 等效线性化自动产出**
  - 人工边界：`ab=GFE.Pre.artbc.art_bc(); ab.name='ArtBC-1'; ab.structure='plant'; ab.surface='TUTIAROUND'; ab.centered=False; ab.center=[]; GFE.Pre.artbc.artbc_mgr().add(ab)`（structure=合并体名 'plant'）

## 5 分析步 / 输出 / 工况
- **S15 [官方实证v3.x]** Dyna-1 显式动力步：`ds=GFE.Pre.step.dynamic_explicit_step(); ds.name='Dyna-1'; ds.description=''; ds.nlgeom=False; ds.period=20.0; ms=GFE.Pre.step.mass_scaling(); ms.region='*'; ms.type=1; ms.frequency=100; ms.target_time=5e-05; ds.mass_scaling=[ms]; GFE.Pre.step.step_mgr().add(ds)`
  - 坑: 动力步长=质量缩放 target_time（步长唯一入口）；`obj.mass_scaling=[ms]` 列表赋值为正写
- **S16 [官方实证v3.x]** 输出+工况（**v3.x 工况=映射属性赋值，非 set_***）
  - FO-DynaEla-All：`o=GFE.Pre.output.output_request(); o.step=''; o.type=0; o.method=0; o.time_type=0; o.time_interval=0.1; sub=GFE.Pre.output.node_output(); sub.variables=['U']; sub.var_option=-1; sub.reg_type=-1; sub.nset=''; o.sub_output=[sub]; GFE.Pre.output.field_mgr().add(o)`
  - 工况：`c=GFE.Pre.case.case(); c.name='Dyna'; c.steps=['Initial','Dyna-1']; c.bcs['Initial']=[]; c.bcs['Dyna-1']=[]; c.initialConditions['Initial']=[]; c.vload['Dyna-1']=['VibLoad-1']; c.artbc['Dyna-1']=['ArtBC-1']; c.fieldReqs['Dyna-1']=['FO-DynaEla-All']; c.histReqs['Dyna-1']=[]; c.elemAdd['Dyna-1']=[]; c.elemDel['Dyna-1']=[]; GFE.Pre.case.case_mgr().add(c)`
  - 坑: 动力工况三件套（vload+artbc+fieldReqs）漏挂不报错但不生效；bcs 全空——人工边界替代常规 BC（官方证实）；⚠ v2.15 无映射赋值，退回 set_vload/set_artbc/set_fieldReqs
- **S17 [②保存提交 / ①导INP]** 保存 .pre/创建作业提交/后处理仍 GUI；导 INP 官方实证：`from GFE.io import inpio; w=inpio.writer(inp_path); w.set_case('Dyna'); w.perform()`
  - 坑: 未划网格几何只警告不阻塞导出；"未获取到结构形心,使用默认值(0,0,0)"为人工边界静默回退，须人工核 INP

# 已知不确定项（官方对账后存留）
- 官方脚本 α=0.948805 与 dump/INP 0.9469011585 的微差来源（两次模态频率差异）未逐位核对
- amp 仅 X 向单分量输入为官方+dump 双证；三向输入写法本章无样本
- box_builder.build() 返回值在官方脚本按单 shape 用（layer_shape），与 v2.15 反推"返回 shapes 列表"是否同物未在 v3.x 实测


---
# ===== 路径_ch05_非均匀场地.md =====

# 路径_ch05_非均匀场地（feijunyunchangdi：核电站结构+钻孔非均匀土）

- **case**: 实际案例操作手册 第5章；dump 真值 `04_状态dump/ch05_section/`；**官方命令流 `E:\GFE2026\典型案例与教程\第5章 非均匀场地建模案例\CM5-update2.py`（1968 行，v3.x，2026-06-11 通读对账；钻孔数据 SoilSamples.txt 2401 行）**
- **单位制**: m–t–kPa（材料 6 种与 ch04 完全同名同值）
- **tier_summary**: ①15 ②1 ③0（S1 结构同源②→①官方整段重建、S11 调幅维持"官方未演示"注记；仅 S15 保存/提交 GUI ②）
- **分析类型**: 模态 + 静力（地应力）+ 显式动力（KOBE 波、人工边界），三工况三 INP
- ⚠ 版本注: build_non_uniform_soil / 工况映射赋值为 v3.x API；**本机 v2.15 实测无 build_non_uniform_soil、无 compute_era（2026-06-10 _audit/phase7/实测裁决.md）**——v2.15 非均匀土与调幅仍是硬断点，⚠ 保留。

## 1 几何（结构重建 + 非均匀土）
- **S1 [官方实证v3.x]** 结构部分官方脚本**完整重建**（草图→拉伸→阵列→安全壳→merge(…,True,'plant')，与 CM4 L120-755 逐行同源），**不是 open_pre 合并导入**（反推对照注：旧记 open_pre(merge=True) 路线作废，官方就是代码复用重跑；厂房材料 damping α=0.948805 与 ch4 脚本同值——旧记"ch5 α=0.9409 与 ch4 不同"是 dump 两次模态差异，官方教学脚本未区分）
- **S2 [官方实证v3.x]** 非均匀土体（按钻孔采样点自动建层）——**签名/实参/数据管线全实证**
  - 钻孔数据：`SoilSamples.txt` 每行 **tab 分隔 7 列 = x, y + 5 个层界面 z 值**（如 `0 6 0 -7 -18 -26 -62`：地表 z=0，向下负值，5 界面=4 层），共 2401 孔（49×49 网格、间距 6m）；逐行 `float` 解析进二维数组
  - `sample=GFE.geometry.geotool.SoilSample(x=row[0], y=row[1], depth=row[2:])`（关键字实参）
  - `GFE.geometry.geotool.build_non_uniform_soil(dim=0, materials=soil_materials, samples=soil_samples)`——dim=0 为 3D Delaunay；**自动创建**几何 **'NU-Soil-1'**（首建固定名；反推对照注：dump 名 NU-Soil-2 系 GUI 二次重建）+ 逐层 gset + 实体截面，**上表面恒 z=0**
  - **materials 顺序仲裁（官方推翻旧记）**：官方 `['qiangfenghuahuagangyan','quanfenghuahuagangyan','lizhinianxingtu','sutiantu']` = **从下到上（最深层在前）**，materials[0]→Layer1=最深层——与 dump"NU-Soil-1-1=qiangfenghua（最深层）"自洽；旧记坑①"materials 从上到下"作废。注意与 box_builder/一维土层（从上到下）**方向相反**，跨 API 勿混
  - ⚠ 本机 v2.15 无 build_non_uniform_soil（实测裁决保留），需 GUI 或 v3.x
- **S3 [官方实证v3.x]** 对位裁剪：地下室=raft `extrude([…],[0,0,16])`→'plant-basement'；对位**利用"上表面恒 z=0"**：`cx,cy,cz=geotool.centre_of_mass(soil.shape()); center1=[cx,cy,0.0]; center2=[0,0,16]; builder.translate(['NU-Soil-1'], 差向量, False)`（反推对照注：ch4 用最高面形心，ch5 官方直接取形心 xy+z=0，更简）；`builder.cut('NU-Soil-1',['plant-basement'],True)`
  - 土材料经 `GFE.io.get_current().import_mat(gmat)` 导入（gmat 含 TestData EERA 曲线、无 damping entry，同 ch04 S6）

## 2 网格 / 相互作用
- **S4 [官方实证v3.x]** 网格：土体 `GFE.DefaultSize=6.0`（官方只设单一尺寸，未设最小 3——旧记 3-6 区间来自手册 GUI 注记）；`Mesh.Algorithm3D:10`；`generator.mesh(['NU-Soil-1'], controller)`；厂房/壳 size=1.0 同 ch04
- **S5 [官方实证v3.x]** 搜索接触批量 Tie：`cp.search_face('NU-Soil-1','plant',0.01)`（容差 0.01）+ CP-…-master/slave 表面对 + `surface_pair(param_number=1, parameters=[0.01], name=tie_mgr.auto_name('Tie'))` 循环，骨架同 ch04 S11
- **S6 [官方实证v3.x]** 土体四周+底面表面集 'soil-around'（与 ch04 S12 实现不同，按极值面收集）
  - 底面：遍历 `geotool.children(shape,4)`，形心 z 与运行最小值 ±0.1 容差归组 bottom_faces；X/Y 两侧同法取 min/max 两组
  - `gset_mgr().add('Set-base'/'Set-x'/'Set-y', faces)`（这些 gset 兼作 BC 集合）
  - 落地表面集：`id=geotool.get_id_by_shape(f)` 逐面取 id → `obj.data=[[geo_obj.id(), f_id[-1], 0] for …]`；**`obj.to_node_surface=False`**（新字段，旧记缺）；`GFE.Pre.surface.surface_mgr().add(obj)`

## 3 集合 / 边界 / 荷载
- **S7 [官方实证v3.x]** 几何集 Set-base/Set-x/Set-y 见 S6（官方将选面与建集合一体化）
- **S8 [官方实证v3.x]** BC 四件（模态/静力工况用；动力工况不挂）
  - BC-base: `b=GFE.Pre.boundary.boundary(); b.type=0; b.set='Set-base'; b.valid_dof=0; b.value=[0.0]*6; b.amplitude=''; b.value_im=[0.0]*6; b.amplitude_im=''; b.distribution=''; GFE.Pre.boundary.bc_mgr().add(b)`
  - BC-x: `type=1; set='Set-x'; valid_dof=1`（U1=0）；BC-y: `type=1; set='Set-y'; valid_dof=2`（U2=0）
  - 重力官方名 **'GRA'**：`type=7 惯性力; set=''(全模型); value=[0.0,0.0,-9.8]`（**官方 value 三元**，反推对照注：非 6 元）
  - 坑: "法向约束"=位移型勾单自由度；valid_dof 位掩码（1=U1, 2=U2）
- **S9 [官方实证v3.x]** 一维土层（仅供场地反应，几何不用）：`s.depth=[7.0,11.0,8.0,36.0]; s.materials=['sutiantu','lizhinianxingtu','quanfenghuahuagangyan','qiangfenghuahuagangyan']; s.bedrock_mat='qiangfenghuahuagangyan'; s.depth_dir=2; GFE.Pre.soil.soil_mgr().add(s)`——**从上到下**，与 S2 build_non_uniform_soil 的 materials（从下到上）方向相反，官方同文件双序并存，铁证勿混

## 4 地震输入
- **S10 [官方实证v3.x]** KOBE 波幅值：`a.name='KOBE_JAPAN_1-16-1995_MORIGAWACHI_x'; a.type=0; a.spectrum_type=-1; a.gravity=0.0; a.value=[t,v 平铺]`（官方 py L1141-1873 硬编码全数据）
- **S11 [维持②性质注记]** 调幅至目标地表峰值：**官方 CM5 无 compute_era 调用、无任何调幅步**——KOBE 波按原始幅值直接输入；手册 GUI"调幅"面板在官方命令流中未复现。命令流等效仍为 v3.3.0+ `GFE.geometry.geotool.compute_era(target, max_iter, tol, a_layer, vibload_name)`（ch10 官方用例 `compute_era(2.2,5,0.01,1,'VibLoad')`；a_layer: 0=基岩处/1=基岩露头/2=地表）
  - ⚠ 本机 v2.15 无 compute_era（实测裁决保留）；v3.x 可达但 ch5 官方未演示
- **S12 [官方实证v3.x]** VibLoad-1 + ArtBC-1（含 14 个 set_parameter，同 ch04 S14 全表）
  - `v.amp_bottom_x='KOBE_JAPAN_1-16-1995_MORIGAWACHI_x'; v.amp_bottom_y=v.amp_bottom_z=''; v.pwave_dir=2; v.soil='Soil1D-1'; v.is_outcrop=True; v.input_loc=-1; v.level=0`；set_parameter 真值=ch04 同表（N=4096, TimeInterval=0.02, SubLayerHeight=1, UseEERAMat='true' 等）
  - **土层 α 逐层赋值机制同 ch04**：UseEERAMat → INP 导出自动生成 `<mat>-EERA` 材料带逐层 `*Damping Alpha`，命令流不手写
  - `ab.structure='plant'; ab.surface='soil-around'; ab.centered=False; ab.center=[]`

## 5 分析步 / 输出 / 工况
- **S13 [官方实证v3.x]** 三分析步
  - Modal-1: `fs=GFE.Pre.step.frequency_step(); fs.eigen=10; fs.nlgeom=False`
  - Static-1: `ss=GFE.Pre.step.static_general_step(); ss.init_inc=0.1; ss.period=1.0; ss.min_inc=1e-5; ss.max_inc=0.1`
  - Dyna-1: `period=20.0`（**官方脚本 20.0；反推对照注：dump 60.76 为 GUI 实跑配置，教学脚本截短**）；`mass_scaling: region='*', type=1, frequency=100, target_time=3e-05`，`ds.mass_scaling=[ms]`
  - 坑: target_time 本章 3e-5（非 5e-5）；β=0 铁律；先模态出 f₁→α 写入结构材料 damping
- **S14 [官方实证v3.x]** 输出+三工况（**映射属性赋值**；工况名官方小写 'model'/'static'/'dyna'）
  - FO-Static：node ['U','UR','RF','RM'] + element ['E','S','SF','SM']，`step='Step-1'; time_interval=1.0`；FO-DynaEla-All：node ['U'], time_interval=0.1
  - model: `c.steps=['Initial','Modal-1']; c.bcs['Initial']=['BC-base','BC-x','BC-y']; c.bcs['Modal-1']=[]; c.fieldReqs['Modal-1']=['FO-Static']`（模态挂"静力"输出官方证实）
  - static: `c.bcs['Initial']=[同上]; c.bcs['Static-1']=['GRA']; c.fieldReqs['Static-1']=['FO-Static']`
  - dyna: `c.bcs 全空; c.vload['Dyna-1']=['VibLoad-1']; c.artbc['Dyna-1']=['ArtBC-1']; c.fieldReqs['Dyna-1']=['FO-DynaEla-All']; c.histReqs/elemAdd/elemDel=[]`（三件套；不挂 BC）
  - ⚠ v2.15 退回 set_bcs/set_vload/set_artbc/set_fieldReqs
- **S15 [②保存提交 / ①导INP]** 官方一次导三 INP：`inpio.writer(path_static).set_case('static')+perform()`，再 'model'、'dyna' 各一遍；保存 .pre/作业提交/自检仍 GUI
  - 自检要点: 写出 INP 后核土层 `*Material <名>-EERA` 是否带 `*Damping Alpha`（EERA 阻尼是否生效的唯一可见证据）

# 已知不确定项（官方对账后存留）
- ~~钻孔采样点数据缺~~ 已落地：SoilSamples.txt（2401 孔全量），随官方案例分发
- ~~build_non_uniform_soil 精确签名缺~~ 已实证：`build_non_uniform_soil(dim, materials, samples)` 关键字调用
- 静力步是否以 -prevdb 链入动力步（地应力平衡→动力）：官方脚本只分别导三 INP，链接关系仍在作业层（GUI/求解器命令行），命令流不可见
- 官方未演示调幅：目标 1.5 m/s² 的手册流程与 compute_era 的等价性仅 ch10 旁证，ch5 无直接样本


---
# ===== 路径_ch06_基坑开挖.md =====

# 路径_ch06 邻近建筑的基坑开挖模拟（施工模拟·生死单元）

> case: `jikengkaiwa`（dump: 04_状态dump/ch06/）；单位制 **m-t-kPa**（C35 E=3.15e7 kPa, ρ=2.5 t/m³）
> 真值序：**官方命令流 CM6-update2.py（E:\GFE2026\典型案例与教程\第6章, v3.x, 2026-06 全文通读）** > dump > GFE-Cases_c06/c07/c08/c09（手册第 6 章）> Cmd 手册 §8.2 idiom
> ⚠ 双代际：官方 py 面向 v3.x（E:\GFE2026）；v2.15（D:\GFE PrePo）无 copy_mesh/工况映射属性等，标 [v2.15无此API] 处仍按旧路径
> tier_summary: **①×21 ②×1 ③×2**（官方实证后 S5/S8/S12/S15 升级）

## A. 几何（手册 §6.2/§6.4/§6.5；最终 geo_mgr 4 体: Merge-1 / Soil-1 / SuperStru / BasementBoundary）

- **S1 [官方实证v3.x]** 草图画放坡断面（多折线闭环 (0,0)→(27,0)→(26,-1)→(1,-1)→(0,0)，框选填充成面）
  - 官方 idiom：`d=GFE.draft.get_current(); d.set_snap_object(0); d.set_operate_mode(2)`（2=多折线）`; for p in pts: d.input(p[0],p[1])`；填充：`d.set_operate_mode(-1); d.set_snap_object(2); d.snap_object(-10,37,10,-11); d.select_snaped(True); d.fill_selected(); d.remove_selected()`（删线留面）
  - 平面设置官方签名：`d.set_normal([0,0,0],[1,0,0],[0,1,0])`（origin/normal/xdir 三个 3 维向量，**非枚举值**——反推稿 set_normal(2) 作废）；完成 `shape=d.export()` 后手动 `geo_mgr().add('fangpo-x-base-face', shape)`；第二草图前 `d.clear()`
  - 坑: draft 全程 (u,v) 二维参数坐标，不是模型 xyz（Cmd ②76）；绘制完 `set_operate_mode(-1)` 显式退出（Cmd ②87）；官方 `remove_selected()` 删草图线避免污染导出
- **S2 [官方实证v3.x]** 两放坡草图分别拉伸后**布尔取交**成放坡体（官方与反推不同：不是单草图拉伸，而是 x/y 两个方向断面体 common）
  - x 草图设 YZ 面拉伸 `extrude([face],[42,0,0])`→'fangpo-x-base'；y 草图设 XZ 面（normal=[0,-1,0]）拉伸 `extrude([face],[0,27,0])`→'fangpo-y-base'；`builder.common(['fangpo-x-base','fangpo-y-base'],'fangpo')` → 'fangpo'
  - 坑: 拉伸后草图遗留面必须删除，否则污染后续框选/布尔（c06 ②）；extrude 返回 shape 列表，需逐个 `is_null()` 判空后 `mgr.add(name, sp)`
- **S3 [官方实证v3.x]** 基坑底面逐层拉伸切分开挖土层：-1m / -2m ×3（kaiwa_1_depth=1, kaiwa_2_n_depth=2, kaiwa_num=4）
  - 官方找底面 idiom：`for f in geotool.children(geo_obj.shape(), 4): fz=geotool.centre_of_mass(f)[2]`，取 fz 最小者；`extrude([bottom_face],[0,0,-depth])` 逐次执行，命名 `mgr.auto_name('kaiwa')` → kaiwa-1~4
- **S4 [官方实证v3.x]** 内支撑：双矩形草图（operate_mode=3 矩形：外 (0,0)-(40,25)、内 (5,5)-(35,20)）+ 60 条内部直线（operate_mode=1，两点一线）→ 平移就位 → 三维阵列复制第二道
  - `builder.translate(['neizhicheng-1'],[1,1,-1],False)`；`builder.make_array([shapes],1,1,2,[0,0,-3])` → 'neizhicheng-2'（偏移 = -(kaiwa_1_depth+kaiwa_2_n_depth)）
- **S5 [官方实证v3.x]** 立柱="点拉伸"真身：取内支撑草图几何的**顶点 children(shape, 7)**，筛内部交点后 `extrude(vertex列表, [0,0,-12])` —— **extrude 直接吃顶点 shape，点→线命令流可行**（原③断点解除）
  - `for n in geotool.children(geo_obj.shape(), 7): nx,ny,nz=geotool.centre_of_mass(n)`，按 min/max±0.1 容差筛内部点；产物 `mgr.auto_name('lizhu')` → lizhu-1~N
  - ⚠ [v2.15未验] 顶点拉伸在 v2.15 是否同样可行未实测；替代 occ 造线段仍备用
- **S6 [官方实证v3.x]** 布尔合并 放坡+开挖+内支撑+立柱 → `Merge-1`（共节点前提）
  - `builder.merge(['fangpo','neizhicheng-1','neizhicheng-2']+kaiwa_names+lizhu_names, False, '')`（官方签名：第2参 False、第3参空串，非 replace_set=True）
  - 坑: 合并后旧几何条目要移除；共节点部件后续**免相互作用、免网格尺寸控制**（c06 ②）

## B. 土体与既有结构

- **S7 [①]** 材料 13 个：5 土层 MC + C35/Q345 +（YJK 带入 C1/C2_Mat30/60、HRB400、Q390）
  - `m=material.material(); m.name='zatiantu'; m.entries=[density(params=[1.85]), elastic(params=[140141.0,0.3],type=0), mohr_coulomb(cohesion=[12.0,0.0], plasticity=[10.0,5.0], n_cohesion=2, n_plasticity=2)]; mat_mgr().add(m)`
  - dump 真值（ρ/E/ν/摩擦角/剪胀角/c）: zatiantu 1.85/140141/0.3/10/5/12；niantu 1.65/50699/0.42/17/8.5/15；fenzhiniantu 1.85/165454/0.35/22/11/16；shazhinianxingtu 1.85/384078/0.3/22/11/20；qiangfenghuahuagangyan 2.0/1226880/0.25/28/14/29；C35→dump 名为 'C30' E=3.15e7；Q345 7.8/2.06e8/0.25
  - 坑: dump 剪胀角=摩擦角/2、c 值 12~29 与手册表（剪胀 0°、c=30）**不一致，以 dump 为准**；elastic 必须显式 type=0（Cmd ②41）
- **S8 [官方实证v3.x]** 整包导入 `cm6.gmat`：`import GFE.io; GFE.io.get_current().import_mat(gmat_path)`（官方主路线：py 只手建 C35 一个材料，5 个土层 MC 材料全走 gmat 导入）
  - ⚠ [v2.15未验] v2.15 spec 自省未见此符号
- **S9 [①]** 一维土层（快速建土的前提）
  - `o=soil.soil(); o.name='Soil1D-1'; o.depth=[2.0,4.0,6.0,4.0,9.0]; o.materials=['zatiantu','niantu','fenzhiniantu','shazhinianxingtu','qiangfenghuahuagangyan']; o.bedrock_mat='qiangfenghuahuagangyan'; o.depth_dir=2; soil_manager().add(o)`
  - 坑: GUI 表格"从高到底"填，box_builder 的 set_height 却要**从下到上**（Cmd ②88），方向相反
- **S10 [①]** 快速建土 120×120 → Soil-1 + Soil-1-Layer1~5 集合 + SoilLayerProp 截面自动生成
  - `b=GFE.soil.box_builder(); b.set_height([9,4,6,4,2],2); b.set_parameter(120,120); ls=b.build()`
  - `db=GFE.soil.data_builder(); db.name='Soil-1'; db.dimension=3; db.layer_shape=ls; db.layer_material=['zatiantu',…]; db.build()`
  - 坑: 截面属性已随 data_builder 自动建好，**不要再手工建分层截面**（c07 ②）
- **S11 [①]** 平移对位 + 布尔分割印刻基坑形状进土体（共节点界面）
  - `geoprim.builder().translate(['Merge-1'],[0,30,0])`（案例矢量 0,30,0）
  - `geoprim.builder().split('Soil-1', ['Merge-1'], True)`（先被分割者后工具体；末参=替换原始图形）
  - 坑: 不勾"替换"则新旧两份土体并存极易选错（c07 ②）；分割必须在划网格**之前**
- **S12 [官方实证v3.x]** 导入 YJK 既有建筑 → SuperStru + BasementBoundary（含 Dead/Live/Comb 工况、荷载、集合；**'AllGrav' 边界即 YJK 导入产物**，官方 py 不自建重力）
  - 官方实参（ch6）：`yjk_para = [1,1,0,1,1,1,1,1, 300,5,800,0,600,2800,200,610, 150,3,1,0,5,250,0,0, 1,0,10,300,140,260,80,160, 400,0,310,50,0,260,0,100, 0,0,0]; gfeio.get_current().import_yjk(yjk_file_path, yjk_para, ['',''], True, '', False)`；导入后补一次 `GFE.Pre.document.set_application_by_ui()`
  - 坑: 43 元整数列表取值场景相关（ch14 同位不同值），不能跨案例照抄；目录须同含 dtlmodel.ydb+dtlCalc.ydb
- **S13 [①]** 平移对位 SuperStru 后，土体被建筑地下室裁剪
  - `geoprim.builder().cut('Soil-1', ['BasementBoundary'], True)`

## C. 网格与结构单元（手册 §6.7）

- **S14 [①]** 分批划网格：先结构（尺寸 1~2）后土体（最大 3 最小 2，Delaunay 四面体）
  - `gen=mesh_generator.generator(); c=mesh_generator.controller(); c.user_option={…'GFE.DefaultSize':3.0…}; c.generate_dim=3; gen.mesh(['Soil-1'],c)`
  - 坑: 全局参数是可变状态非几何属性，分批划互不追溯（c08 ②）；网格选项字典三处示例均整套显式给全，**勿省键**（Cmd ②72）；BasementBoundary 不划
- **S15 [官方实证v3.x]** 复制网格**有命令流 API**：`GFE.geometry.geotool.copy_mesh(name='Set-pshnt', origin_node=True, as_source=False, type_name='S3', new_set_name='pshnt-1')`（原③断点解除）
  - 官方 5 次调用：Set-pshnt/Set-dilianqiang→'S3'，Set-neizhicheng1/2、Set-lizhu→'B31'；源是**几何集**（gset，由面/边形心筛选预建），origin_node=True 即"使用和源相同的节点"
  - 单元类型官方用 **S3**（非反推稿 S3R）
  - ⚠ [v2.15无此API] v2.15 spec 无 copy_mesh，GUI"通用—复制网格"专有
  - 坑: 单元集随重划网格失效——网格定稿后才能复制（c08 ②）；dump 真值名 **dilianqiang-1**（手册 OCR 的 diliangqiang 为讹）；官方源集合在划网格**前**预建（几何集），网格后才 copy_mesh
- **S16 [①]** 截面属性赋支护：
  - 喷混壳 `property_shell(elset='pshnt-1', mat='C30(即C35)', thickness=0.2, integral_point=5, type=3)`；地连墙壳 thickness=0.5
  - 立柱梁 `property_beam(elset='lizhu-1', shape=圆 r=0.5)`；内支撑工字 l=0.4,h=0.8,b1=b2=0.5,t1=t2=t3=0.05
  - `sect_mgr().add(o)`；梁截面特性（面积/惯量/剪切刚度）GUI 自动算，命令流需自填 shear 等

## D. 相互作用 / 边界荷载（手册 §6.9）

- **S17 [①]** 搜索接触建土-既有结构绑定 Tie-1~5（容差 0.01）
  - [官方实证v3.x] `cplist=GFE.geometry.contact_pair.search_face('Soil-1','SuperStru',0.01)` 返回 [master面元组列表, slave面元组列表] 对；逐对 `master=[[geo_id]+list(x) for x in pairs[0]]` 组 data 建 `geometry_surface` 入 `surface_mgr()` → `sp=surface_pair(); sp.name=tie_mgr.auto_name('Tie'); sp.first_surf=…; sp.second_surf=…; sp.param_number=1; sp.parameters=[0.01]; tie_mgr().add(sp)`（官方字段 **param_number**，反推稿 tp.type=0 作废）
  - 坑: 基坑内部结构共节点**不建**相互作用，只有非共节点的既有建筑用 Tie（c06 ④5）
- **S18 [官方实证v3.x]** 边界：BC-z 全约束(type=0,valid_dof=0,set='bc-z')、BC-x(type=1,valid_dof=1)、BC-y(type=1,valid_dof=2)；边界面集 bc-z/bc-x/bc-y 用官方"六面筛选" idiom（遍历 children(.,4)，min/max±0.1 容差动态更新底/左右/前后面列表）
  - 重力 **'AllGrav' 官方 py 不自建**——是 import_yjk 带入的荷载名，工况直接引用；若无 YJK 来源需手建 type=7 惯性力 value=[0,0,-9.8]
  - 坑: 重力是 type=7 惯性力非"重力荷载"，分量 **-9.8** 非 -9.81（c08 ②）；约束需先有集合；boundary 必填字段官方全集：type/name/set/valid_dof/value(6元)/amplitude/value_im(6元)/amplitude_im/distribution

## E. 分析步 / 工况（手册 §6.11）

- **S19 [官方实证v3.x]** 分析步 6 个：GeoStatic-1(geo_static_step) + fangpo/kaiwa1~4(static_general_step)，全部 nlgeom=True, period=1, init_inc=1, min_inc=1e-5, max_inc=1
  - `s=step.geo_static_step(); s.name='GeoStatic-1'; s.nlgeom=True; …; step_mgr().add(s)`
  - 坑: "静力分析(地应力平衡)"与"静力分析"是**并列两种步类型**（c08 ②）；nlgeom 影响"随后的"分析步
- **S20 [官方实证v3.x]** 工况组装 + 逐步挂载 + 生死单元——v3.x 用**映射属性直接赋字典**（官方原文）：
  ```python
  case_obj = GFE.Pre.case.case(); case_obj.name='jikengkaiwa'
  case_obj.steps = ['Initial','GeoStatic-1','fangpo','kaiwa1','kaiwa2','kaiwa3','kaiwa4']
  case_obj.bcs['Initial'] = ['BC-z','BC-x','BC-y']
  case_obj.bcs['GeoStatic-1'] = ['AllGrav']        # 重力只挂第一步；AllGrav 来自 YJK 导入
  case_obj.initialConditions['Initial'] = []
  case_obj.fieldReqs['GeoStatic-1'] = ['FO-Static']; case_obj.fieldReqs['fangpo'] = ['FO-Static']
  # 生死单元：地应力步杀光全部支护（含 neizhicheng2-1），放坡步杀放坡土+激活第一批支护
  case_obj.elemDel['GeoStatic-1'] = ['pshnt-1','dilianqiang-1','neizhicheng1-1','neizhicheng2-1','lizhu-1']
  case_obj.elemDel['fangpo'] = ['Set-fangpo']
  case_obj.elemAdd['fangpo'] = ['pshnt-1','dilianqiang-1','neizhicheng1-1','lizhu-1']
  for i in range(1, 5):                            # kaiwa1~4
      case_obj.fieldReqs[f'kaiwa{i}'] = ['FO-Static']
      case_obj.elemDel[f'kaiwa{i}'] = [f'Set-kaiwa{i}']
      if i == 2: case_obj.elemAdd['kaiwa2'] = ['neizhicheng2-1']   # 开挖到第2层才加第二道内支撑
  GFE.Pre.case.case_mgr().add(case_obj)
  ```
  - 开挖土集合名官方实证：**Set-fangpo / Set-kaiwa1~4**（形心分区 idiom 建：遍历 Soil-1 children 实体，按 z 区间动态判层 + f-string 命名 gset_mgr().add）——原"不确定项1"解决
  - elemDel/elemAdd 值=**几何集名（土）或 copy_mesh 单元集名（支护）**混用，官方实证
  - ⚠ [v2.15无此API] v2.15 只有 8 个 set_*（set_bcs/set_elemDel/…），无映射属性；v2.15 写法见上一版（set_bcs('Initial',[…]) 等价）
  - 坑: 漏挂静默不生效；case 映射属性写专用，挂载验证看导出 INP
- **S21 [官方实证v3.x]** 场输出 FO-Static：节点 RF/RM/U/UR + 单元 E/PE/PEEQ/S/SF/SM，time_interval=1
  - `o=output_request(); o.sub_output=[node_output(variables=['RF','RM','U','UR']), element_output(variables=['E','PE','PEEQ','S','SF','SM'])]; GFE.Pre.output.field_mgr().edit(o)`
  - 坑: 官方 ch6 用 **field_mgr().edit(obj)**（覆盖默认输出请求），ch7/ch14 用 .add()——同名覆盖语义留意

## F. 求解 / 后处理

- **S22 [①]** 写 INP 自检 + 提交：`w=inpio.writer(path); w.set_case('jikengkaiwa'); w.perform()`；多静力步程序自动选 GFEXN 隐式求解器（c09 ②）
- **S23 [③]** 作业管理器提交/监控为 GUI；命令行可 `GFEXN/GFEXC -db <model.db>`（作业层不在命令流）
- **S24 [③]** 后处理：IsRemoved 状态变量过滤被移除单元、PE 云图、施工动画——GUI 专有

## 已知不确定项
1. ~~开挖土几何集名~~ → 官方实证 Set-fangpo/Set-kaiwa1~4（CM6-update2.py，见 S20）。
2. ~~S5 点拉伸、S8 import_mat、S12 import_yjk 取值~~ → 全部官方实证（v3.x）；v2.15 侧仍未验。
3. ~~elemAdd 时机推断~~ → 官方实证：fangpo 步加 pshnt/dilianqiang/neizhicheng1/lizhu，kaiwa2 加 neizhicheng2，其余 kaiwa 步只删不加（见 S20）。
4. dump 材料 'C30' 即手册 C35（E=3.15e7 与 §6.3.1 C35 一致而非 C30 的 3.0e7），名实不符；官方 py 自建名就叫 'C35'，复刻 dump 模型时按 dump 名引用。
5. 官方 py 的 mesh controller 结构网格 'Mesh.Algorithm'=8.0、土体=2.0（反推稿未记录算法号差异）；auto_transfinite=True 在小楼案例曾崩，大网格谨慎。


---
# ===== 路径_ch07_锚杆隧道施工.md =====

# 路径_ch07 锚杆隧道施工模拟（隧道设计器·嵌入锚杆·分段生死单元）

> case: 官方 py 名 `suidaokaiwa`（dump GUI 版名 Case-1）steps=Initial→Static-1→Stage-1~11（13 步全证）
> 单位制：手册照录"kg/m³、Pa"但数值非工程量级（fenghuatu ρ=1.83549、E=50000）——**缩尺演示参数**，复刻照抄 dump 字面值即可（c09 ②）
> 真值序：**官方命令流 CM7.py（E:\GFE2026\典型案例与教程\第7章, v3.x, 2026-06 全文通读）** > dump > GFE-Cases_c09（手册第 7 章全章）> Cmd 手册 §3.4.13/§8.2
> ⚠ 命名双轨：GUI 隧道设计器产物带 -1（Tunnel-1-Boundary/Tunnel-1-rockseg-n）；官方 py 手动注册名 **Tunnel / Tunnel-Boundary / Tunnel-Rockbelt / Tunnel-rockseg-n**，本文以 py 名为准
> ⚠ CM7-update2-存在bug.py = 官方自带负面样本：split 后子实体父归属 ID 跨会话非确定（详见 wiki GFE2026-CM-ch07 已知bug节）
> tier_summary: **①×16 ②×1 ③×1**（官方实证后 S4/S9/S14-15 升级）

## A. 材料（手册 §7.2.1-7.2.2；dump mat_mgr 5 个全证）

- **S1 [①]** 5 材料：fenghuatu/fenghuayan(弹性+MC+阻尼)、ruanyan/penhun/maogan(纯弹性+阻尼)；阻尼全部 α=0, **β=0**
  - `m=material.material(); m.name='fenghuatu'; m.entries=[density(params=[1.83549]), elastic(params=[50000.0,0.3],type=0), damping(params=[0.0,0.0]), mohr_coulomb(cohesion=[30.0,0.0], plasticity=[36.0,18.0], n_cohesion=2, n_plasticity=2)]; mat_mgr().add(m)`
  - dump 真值（ρ/E/ν[/摩擦/剪胀/c]）: fenghuatu 1.83549/5e4/0.3/36/18/30；fenghuayan 2.34535/5e5/0.3/36/18/30；ruanyan 2.54929/2e6/0.25；penhun 2.44732/1.5e7/0.2；maogan 8.00477/2.1e8/0.3
  - 坑: entries 顺序按类型匹配不按下标；显式动力虽不涉及本章（纯静力），β=0 仍是全 KB 恒定约定

## B. 土体几何

- **S2 [①]** 一维土层（先建，快速建土依赖它）
  - `o=soil.soil(); o.name='Soil1D-1'; o.depth=[5.0,13.0,42.0]; o.materials=['fenghuatu','fenghuayan','ruanyan']; o.bedrock_mat='ruanyan'; o.depth_dir=2; soil_manager().add(o)`
  - 坑: GUI 土层表"从高到底"填；点"计算"才出 P/S 波速与建议网格尺寸，直接"确定"跳过（c06 ②）
- **S3 [①]** 快速建土 90×20 → Soil-1 + Soil-1-Layer1~3 集合 + Soil-1-LayerProp-1~3 截面（自动）
  - `b=GFE.soil.box_builder(); b.set_height([42,13,5],2); b.set_parameter(90,20); ls=b.build()`（set_height **从下到上**）
  - `db=GFE.soil.data_builder(); db.name='Soil-1'; db.dimension=3; db.layer_shape=ls; db.layer_material=['fenghuatu','fenghuayan','ruanyan']; db.build()`

## C. 隧道与锚杆几何（手册 §7.2.5 隧道设计器）

- **S4 [官方实证v3.x]** `build_tunnel_shape` 命令流一步出三件套（**支持分段+锚杆**，反推稿"不分段不布锚杆"作废）：
  ```python
  [a,b,c] = GFE.geometry.geotool.build_tunnel_shape(
      1, [5.5, 9], [90, 25],            # 断面类型1=3心圆; [顶弧R, 侧弧R]; [顶弧角, 侧弧角]
      False, 0, 0, True, True,          # …(仰拱/偏置类开关); True,True=生成锚杆相关
      [13, 4, 1.8, 0.2],                # 锚杆 [数量, 长度, 弧长间距, 外偏移]
      True, 20, [2], [2], 0, False, None)  # True=3D拉伸; 总长20; [隧道分段间隔2]; [锚杆段间隔2]
  mgr = Pre.geometry.geo_mgr()
  mgr.add('Tunnel', a); mgr.add('Tunnel-Boundary', b); mgr.add('Tunnel-Rockbelt', c)
  ```
  - 返回 [隧道, 隧道土边界, 锚杆带] 三 shape，**不落库须手动 add**（此点反推稿正确）
  - 锚杆分段集 py 侧自建（非设计器产物）：遍历 `children(Tunnel-Rockbelt, 6)` 边，`index = round(ey) // tunnel_layer_spacing` 按 y 归段 → `gset_mgr().add(f'Tunnel-rockseg-{index}', shapes)`
  - ⚠ [v2.15无此API] build_tunnel_shape 为 v3.x API
  - 坑: 锚杆数量超可布置数**静默截断**；曲线扫掠下锚杆生成错误，只有矢量拉伸安全（c09 ②）
- **S5 [官方实证v3.x]** 隧道就位：官方按**形心对位**平移（`centre_of_mass(Tunnel-Boundary)` 与 `centre_of_mass(Soil-1)` 差向量），`translate(['Tunnel','Tunnel-Boundary','Tunnel-Rockbelt'], trsf_vec, False)`；随后**锚杆单独 y 向内移** `translate(['Tunnel-Rockbelt'],[0.0,0.2,0.0],False)`（maogan_embed_offset=0.2 < 分段间隔，保证锚杆嵌入土体不外露）
- **S6 [官方实证v3.x]** 布尔分割：隧道土边界印刻进土体保证共节点
  - `geoprim.builder().split('Soil-1', ['Tunnel-Boundary'], True)`（先被分割者；末参 True=替换原始形状）
  - ⚠ **官方已知bug**：split 后重开 GFE 再跑，`children(Soil-1,2)` 子实体的 get_id_by_shape 父 id 有时=1(Soil-1)正常、有时部分=3(Tunnel-Boundary)——跨会话非确定，下游按 Soil-1 遍历建集可能漏体（CM7-update2-存在bug.py 专设 Bug_Check 复现）

## D. 集合（dump gset 63 个）

- **S7 [官方实证v3.x]** 开挖土集 suidaotu-1~10（实体）、隧道壳面集 suidaoqiao-1~10（面，衬砌复制源）、整体 Set-tuti、边界 bc-base/bc-x/bc-y
  - 官方分段归集 idiom：先用三心圆形心几何公式（py 内置 `calc_centroid_to_top_bottom`）算隧道包围盒 [left/right/bottom/top_pos]；实体 `index=(round(sy)+1)//tunnel_layer_spacing` 入 dict 后**按 key 排序建集**保证顺序；面用"侧面判据" `abs((round(fy)%spacing)-(spacing/2))<1e-9`（质心 y 落段中点=隧道侧面而非端面）
  - 整体集官方用 `gset_basic`：`gs=GFE.Pre.set.gset_basic('Set-tuti'); gs.set_shapes(children(Soil-1,2)); gset_mgr().add(gs)`（锚杆集 Set-maogan 同法，shapes=children(Tunnel-Rockbelt,6)）
  - 坑: gset_mgr().add 双形态——`add(name, shapes)` 与 `add(gset_basic对象)` 官方两种都用；边界面集为几何集（供 BC 引用）

## E. 网格（手册 §7.2.8）

- **S8 [官方实证v3.x]** 土体全局 1.5 划分；锚杆（整个 Tunnel-Rockbelt）单独再划 size=1.0；线控制节点数 3/5/10/18 四组
  - 官方线控制完整 idiom（**edges 字典须手工组装**，非 set_name 副作用自动填）：
    ```python
    cc = mesh_generator.curve_control(); cc.set_name = 'Set-mesh_control_line'
    d = {need_edges_id[0][0]: [e[-1] for e in need_edges_id]}   # {几何体id: [边子id,…]}
    cc.edges = d; cc.count = 3
    controller.size_option = [curvesize_1, curvesize_2, curvesize_3, curvesize_4]
    ```
    其中 need_edges_id 来自筛边时同步收集 `geotool.get_id_by_shape(e)`（返回 [geo_id,…,edge_id]，取首尾）
  - 四组边分类判据（官方）：段中点 y=隧道长直线；其余按 ez>lz 顶弧 / ez<lz 且 ex≈lx 底直线 / 否则侧弧
  - 坑: 官方未设 density 字段（count 直接生效）；反推稿"density=-1 显式关闭"针对旧版本，v3.x 官方代码无此操作；线控制集若与土层线交叉会出问题（官方注释明示）
- **S9 [官方实证v3.x]** 复制网格命令流 API 生成衬砌壳单元集 CpMsh-1~10 + 总集 Set-CpMsh（原③断点解除）
  ```python
  for i in range(1, 11):
      GFE.geometry.geotool.copy_mesh(name=f'suidaoqiao-{i}', origin_node=True,
          as_source=True, type_name='S3', new_set_name=f'CpMsh-{i}')
  # 总集合并：elset data 拼接
  need = []
  for i in range(1, 11): need += GFE.Pre.set.elset_mgr().find(f'CpMsh-{i}').data
  o = GFE.Pre.set.elset(); o.name='Set-CpMsh'; o.data=need; o.unsort=False
  GFE.Pre.set.elset_mgr().add(o)
  ```
  - 单元类型官方 **S3**（非 S3R）；ch7 用 **as_source=True**（ch6 用 False——含义待核，疑为"源面是否保留为源区域"）
  - ⚠ [v2.15无此API] copy_mesh 为 v3.x API
  - 坑: 目标单元类型与源面形状不匹配在"确定"时才报错；单元集随重划网格失效——网格定稿后再复制（c09 ②）

## F. 截面属性（dump sect_mgr 5 个全证）

- **S10 [官方实证v3.x]** 锚杆梁 + 衬砌壳（土层 3 个 LayerProp 已自动生成，勿重建）
  - `pb=section.property_beam(); pb.name='Propery-maogan'; pb.elset_name='Set-maogan'; pb.mat_name='maogan'; pb.shape=3; pb.fiber_num=1; pb.shape_params=[0.0125]; pb.params=[]; pb.direction=[0.0,1.0,0.0]; pb.shear=[35682.8,35682.8]; pb.Ecc=[0.0]*4; sect_mgr().add(pb)`
  - `ps=section.property_shell(); ps.name='Propery-CpMsh'; ps.elset_name='Set-CpMsh'; ps.mat_name='penhun'; ps.thickness=0.15; ps.integral_point=5; ps.layer_num=1; ps.params=[]; ps.has_rebar=False; ps.rebar=section.rebar_layer(); ps.Ecc=[0.0]*4; sect_mgr().add(ps)`
  - 官方**无 pb.type/ps.type 字段**（反推稿 type=2/3 为旧版残留）；壳必填 has_rebar/rebar/layer_num
  - 坑: 梁材料方向向量 (0,1,0) 必填；官方截面名拼写 **Propery-**（非 Property），照抄

## G. 相互作用 / 边界荷载

- **S11 [官方实证v3.x]** 锚杆与土连接=**embed 嵌入**（官方确证，非共节点也非 Tie）
  - `e=interaction.embed(); e.id=0; e.name='Embed-1'; e.host_name='Set-tuti'; e.roundoff_tolerance=1e-06; e.exterior_tolerance=0.05; e.embedded_names=['Set-maogan']; GFE.Pre.interaction.embed_mgr().add(e)`
  - 坑: 嵌入区域=被嵌构件（锚杆），主区域=容纳体（土）——"主"易填反（c10 ②）；官方管理器名 **embed_mgr()**
- **S12 [官方实证v3.x]** 边界 + 重力（官方集合名 bc-base/bc-x/bc-y，dump GUI 版名 tuti-bot/tuti-side-x/y）
  - BC-base: type=0 全约束 set='bc-base' valid_dof=0；BC-X: type=1 valid_dof=1；BC-Y: type=1 valid_dof=2
  - G-whole: type=7 惯性力 **value=[0.0,0.0,-9.8]（3 元）** set=''（整个模型；注意官方惯性力 value 只给 3 元，约束类给 6 元）
  - `b=boundary.boundary(); b.type=0; b.name='BC-base'; b.set='bc-base'; b.valid_dof=0; b.value=[0.0]*6; b.amplitude=''; b.value_im=[0.0]*6; b.amplitude_im=''; b.distribution=''; bc_mgr().add(b)`
  - 注: CM7-update2 版 boundary 多 11 个新 schema 字段（track_id/track_coord/has_if/if_mode/if_acce_path/if_acce/if_param/if_itv/if_tot/if_grade/if_force，移动荷载轨迹+惯性力时程），不赋也有默认值，更新版 GFE 显式赋空

## H. 分析步 / 工况（手册 §7.3；dump step 13 个全证）

- **S13 [官方实证v3.x]** 13 步官方版：Static-1（nlgeom=**False**）+ Stage-1~11（nlgeom=True），全为 static_general_step（period=1, init_inc=1, min_inc=1e-5, max_inc=1）
  - `s=step.static_general_step(); s.name='Stage-1'; s.nlgeom=True; s.period=1.0; …; step_mgr().add(s)`
  - 注: 本章地应力步用普通静力步 Static-1（非 geo_static_step），与 ch06 不同；官方 Static-1 nlgeom=False、Stage-n 才开 nlgeom——反推稿"全 True"作废
- **S14 [官方实证v3.x]** 施工助手产物可全由命令流等价：官方注释明示"直接优化为施工助手操作后的工况（只写最后一次编辑完成的工况）"——循环建 Stage-n 步 + 字典挂生死单元，无须 GUI 助手
  - 坑(GUI 侧仍适用): 助手"添加(移除)"勾选框**默认不勾=移除**，勾选才是添加——语义反转易设反（c09 ②）
- **S15 [官方实证v3.x]** 工况官方版（**重大修正**：锚杆当段立即激活、衬砌滞后一段；Static-1 杀的是分段集而非总集）：
  ```python
  case_obj = GFE.Pre.case.case(); case_obj.name = 'suidaokaiwa'
  case_obj.steps = ['Initial','Static-1'] + [f'Stage-{i}' for i in range(1, 12)]
  case_obj.bcs['Initial'] = ['BC-base','BC-X','BC-Y']
  case_obj.bcs['Static-1'] = ['G-whole']
  case_obj.initialConditions['Initial'] = []
  case_obj.fieldReqs['Static-1'] = ['FieldOutput-1']; case_obj.histReqs['Static-1'] = []
  # 地应力步杀全部支护：CpMsh-1~10 + Tunnel-rockseg-1~10（逐段集，非 Set-CpMsh/Set-maogan 总集）
  case_obj.elemDel['Static-1'] = [f'CpMsh-{i}' for i in range(1,11)] + [f'Tunnel-rockseg-{i}' for i in range(1,11)]
  for i in range(1, 12):
      if i <= 10: case_obj.elemDel[f'Stage-{i}'] = [f'suidaotu-{i}']     # 第 i 段开挖
      if i == 1:               case_obj.elemAdd['Stage-1'] = ['Tunnel-rockseg-1']            # 锚杆当段加
      elif i <= 10:            case_obj.elemAdd[f'Stage-{i}'] = [f'Tunnel-rockseg-{i}', f'CpMsh-{i-1}']  # 锚杆当段+衬砌滞后
      else:                    case_obj.elemAdd['Stage-11'] = ['CpMsh-10']                   # 末步补最后一段衬砌
  GFE.Pre.case.case_mgr().add(case_obj)
  ```
  - 施工节奏官方确证：**Stage-i 挖第 i 段 + 同步打第 i 段锚杆 + 装第 i-1 段衬砌**；Stage-11 收尾装第 10 段衬砌——原"不确定项1/2"解决（激活用 Tunnel-rockseg-n 锚杆段集；suidaoqiao-n 仅作 copy_mesh 源，不进工况）
  - ⚠ [v2.15无此API] 映射属性 elemDel/elemAdd 字典为 v3.x；v2.15 用 set_elemDel/set_elemAdd
  - 坑: 生死单元区域混用**单元集**(CpMsh-n)与**几何集**(suidaotu-n/Tunnel-rockseg-n)；重力只挂 Static-1 一步；漏挂静默不生效
- **S16 [官方实证v3.x]** 场输出 FieldOutput-1：节点 U/UR + 单元 E/PE/S，time_interval=1；`field_mgr().add(o)`

## I. 求解 / 后处理

- **S17 [官方实证v3.x]** 写 INP：`w=inpio.writer(path); w.set_case('suidaokaiwa'); w.perform()`；多静力步自动选 GFEXN
- **S18 [③]** 工况预览（生死单元逐步播放）、施工动画、PE 云图——GUI 专有

## 已知不确定项
1. ~~支护节奏推断~~ → 官方实证：Stage-i 挖+当段锚杆+滞后衬砌（见 S15）；suidaoqiao-n=copy_mesh 源面集，不进工况。
2. ~~rockseg-n 激活步~~ → 官方实证：Tunnel-rockseg-i 在 Stage-i 激活（锚杆段=rockseg）。
3. ~~build_tunnel_shape 精度~~ → 官方以其为主路线（CM7.py），分段+锚杆全参数实证；但 v2.15 无此 API。
4. PickedSet-1~4 为 GUI 拾取残留集，复刻时可忽略。
5. copy_mesh 的 as_source 参数语义（ch6=False / ch7=True）未明，待对照手册或实测。
6. split 父归属非确定 bug（CM7-update2 复现）触发条件未知——同版本同脚本跨会话结果不同，疑 OCC 布尔结果排序不稳定；防御写法：建集时不依赖 children 顺序/父 id，全部用形心坐标判定（官方 CM7 正是如此，故仍可跑通）。


---
# ===== 路径_ch08_SPH小球落水.md =====

# 路径_ch08_SPH小球落水

- **case**: 实际案例操作手册v2025 第8章「SPH 案例一 小球落水」（纯 SPH，无 FEM 耦合；**无 dump**，真值=GFE-Cases c09 §8.3-8.7 + Cmd §2.18/§2.14.9）
- **单位制**: **强制 SI(m)**：kg-m-s-N-Pa（SPH 模块无单位自由度，与其他模块"自洽即可"惯例不同，c09 L79717）
- **tier_summary**: ①4 ②1 ③2

## 几何（按本案例实际流程：几何→SPH对象→SPH分析步→作业xml→批处理→后处理）

**S1 [①]** 建容器箱、水体、小球三个几何（occ 基本体 + geo_mgr 注册 idiom，Cmd §7.3.1/§7.3.5/§8.1）。
```python
from GFE.Pre.geometry import geo_mgr
from GFE import occ
for nm, sp in [('box',    occ.brep_prim.make_box(dx, dy, dz)),      # 容器（中空腔体需布尔做出）
               ('water',  occ.brep_prim.make_box(dx2, dy2, dz2)),   # 水体
               ('sphere', occ.brep_prim.make_sphere(r))]:           # 小球
    if not sp.is_null():
        m = geo_mgr(); m.add(m.auto_name(nm), sp)
```
- 坑：①各几何具体尺寸手册审计未收录（截图 OCR 崩坏），勿编造，复刻需从案例 .pre 反查；②occ 有 occ.make_box 与 occ.brep_prim.make_box 双命名空间（Cmd ②#104）。

## SPH 对象

**S2 [①]** 建 3 个 SPH 流体动力对象（Cmd §2.18.1：`GFE.Pre.sph.sph`，sph_manager().add）。
- box=固体 `obj_type=1` + **填充模式必须选"面" `fill_mode=2`**（中空容器选"全部"会把内部填实，c09 §8.3）
- water=流体 `obj_type=0`（流体参考密度 1000 在分析步设，不在对象上）
- sphere=固体浮体，**浮体密度 500**（`floating` 仅对边界/固体对象有效，Cmd ④#19）
- fill_mode 枚举：0=全部 1=实体 2=面 3=线框；另有 non_newton[密度,粘度,屈服应力,HBP_m,HBP_n]、init_velocity[大小,X,Y,Z]
- 坑：对象与几何/网格/单元集的"SPH 区域"绑定字段名未核（见尾部）。

## SPH 分析步

**S3 [①]** 建流体动力分析步（spec 已核 `GFE.Pre.step.sph_step`，StepType=SPH）。
```python
from GFE.Pre import step
s = step.sph_step(); s.name = 'SPH-1'
s.distance = 0.025          # 内部粒子距离（第8章案例值）
s.gravity = [0, 0, -9.81]
s.rhop0 = 1000; s.rhopgradient = 2   # 流体参考密度 / 初始密度梯度方法
s.gamma = 7; s.coefsound = 20        # 多方常数 / 声音系数
s.auto_area = True                   # 自动计算 SPH 计算区域
s.objects = ['box', 'water', 'sphere']   # 对象顺序页：顺序有语义
step.step_manager().add(s)
```
- 其余案例值（GUI"求解参数"页）：分析时长 1.5s、输出数据间隔 0.01s、移动系数 -2、浮体冻结 0.0s、最小步时 1e-5、最小步时系数 0.05、超界粒子比例 1%、有效密度 700~1300（c09 §8.4 全表）
- 坑：GUI 是"线性摄动"程序类别下的"流体动力"，不在"通用"（c09 ②）。

**S4 [①]** 工况组装：`c = GFE.Pre.case.case(); c.name='Case-1'; c.steps=['Initial','SPH-1']; case_mgr().add(c)`，作业绑定该工况。

## 求解（作业 + xml + 批处理）

**S5 [②]** 作业创建与"高级设置"——**命令流无 job API（Cmd 手册 0 命中），断点：GUI 操作**。作业管理器建作业绑定工况，"高级>>"里**必须勾选"写出SPH xml文件"**（否则不生成 _Def.xml，SPH 无法提交）；案例另设：写出Vuel 0.8 1、求解方法 Pardiso。

**S6 [③]** 提交：SPH **不走 GUI 提交按钮**。编辑批处理文件（改作业名 + SPH 程序路径）后双击/命令行执行 `<作业名>_Def.xml`（c09 §8.6）。bat 编辑与执行本身可由 shell 脚本完成，但 xml 由 S5 的 GUI 产出。

## 后处理

**S7 [③]** GUI 后处理"流体动力"页打开 `<作业名>_out/particle/*.vtk`；查流体选 **_Fluid 后缀**文件（c09 §8.7）。无命令流后处理 API。

# 已知不确定项
1. 容器/水体/小球几何尺寸：手册截图 OCR 崩坏未收录，需从案例 .pre 反查（S1）。
2. `sph` 对象绑定区域（几何/网格/单元集三选一）的字段名与取值未核——spec 只 dump 到 sph_manager，对象类属性表缺失（S2）。
3. sph_step 上"分析时长/输出间隔/移动系数/有效密度上下限"等求解参数页字段的宿主未核（疑在 `excute_para` 参数字典），spec 仅见字段名无语义（S3）。
4. SPH 分析步是否需经工况挂载额外对象（边界/输出）未验证；本案例手册未演示工况细节（S4）。


---
# ===== 路径_ch09_SPH水桶晃动FEM耦合.md =====

# 路径_ch09_SPH水桶晃动（FEM-SPH 耦合）

- **case**: 实际案例操作手册v2025 第9章「SPH 案例二 水桶晃动 FEM-SPH 耦合」（**无 dump**，真值=GFE-Cases c09 §9.2-9.8 + Cmd §2.18/§2.14.9/§4）
- **单位制**: **强制 SI(m)**：kg-m-s-N-Pa（FEM 侧材料同样必须 SI：钢 7800 kg/m³、2.06e11 Pa，c09 L79717/L79760）
- **tier_summary**: ①8 ②1 ③3

## 几何

**S1 [①]** 草图画圆→填充→拉伸成水桶（draft + geoprim，Cmd §4/§3.3.10）。
```python
from GFE import draft
d = draft.get_current()
d.add_circle_centre([0,0], [r,0])      # 圆心+半径点
d.set_operate_mode(13); d.fill_selected()  # 填充成面
shape = d.export()                      # 草图→OCC 形状
# geoprim.builder().extrude(矢量 0,0,1.5 拉成桶体)；需要合并时 merge
```
- 案例操作链：画圆→选择线+填充区域→拉伸 (0,0,1.5)→布尔合并（c09 §9.2）。
- 坑：draft 仅二维 u/v 平面，一切操作经 get_current()；fill_selected 前须选中线条。

## 材料截面

**S2 [①]** 钢材料：`entries=[density(7800), damping(α=0,β=0), elastic(E=2.06e11, ν=0.25, 模量时间尺度"长期")]`，mat_mgr().add。**β 必须为 0**（显式稳定）。

**S3 [①]** 壳截面：类别=壳/各向同性，壳厚度 0.005、积分点 5、偏心 0，绑定桶几何集（sect_mgr CRUD，Cmd §2.9）。

## 网格

**S4 [①]** mesh_generator：水桶大致尺寸 **0.1 m**、单元形状"四边形/六面体"（2D 剖分自动切 Frontal-Delaunay for Quads，三角形显示 S3）。
- 坑（红线级）：**FEM 网格尺寸必须为粒子间距的 5–10 倍**（本例粒距 0.01→网格 0.1）；网格小于粒距则单元内无法生成粒子、计算报错（c09 §9.3）。

## SPH 对象 + SPH 分析步

**S5 [①]** SPH 对象：水=流体 `obj_type=0`；水桶=固体浮体 **浮体密度 7800**（=桶材密度）。其余同 ch8 路径 S2。

**S6 [①]** sph_step：`distance=0.01`（第9章值），gravity (0,0,-9.81)、rhop0=1000、gamma=7、coefsound=20、对象顺序页排序；时长/输出间隔等求解参数页同 ch8（时长 1.5s、**输出数据间隔 0.01s**）。

## 边界荷载（晃动激励）

**S7 [①]** 加速度荷载：boundary type=加速度，A1=1（峰值 1 m/s²）× 幅值函数 `25_RH1TG025_(RenGong_T_025)_x_Zhu`（c09 §9.3）。
- amplitude 对象 value 为**平铺一维列表** (t0,a0,t1,a1,...)，type=0 TABULAR（Cmd §2.12）。
- 坑：①预设地震波库的命令流加载入口未核——波形数据可从既有模型 dump 拷（ch14_plastic dump 有该波 2002 点）；②"幅值函数2"仅频响有效，勿填。

## 场输出

**S8 [①]** FEM 场输出：output_request + node/element 子输出；**时间间隔必须 = SPH 输出数据间隔（0.01s）**，否则流固结果无法对齐（c09 §9.6）。

## 求解（FEM 预计算 → 文件搬运 → 批处理）

**S9 [②]** FEM 预计算作业：命令流无 job API，**断点：GUI** 建作业 + 高级设置勾"写出SPH xml文件"+"写出inp文件"，提交后**算约 1% 即可人工中止**——目的只是生成 fea+db 文件（c09 §9.7）。

**S10 [③]** 耦合文件链（流程级，文件操作可脚本但顺序硬依赖）：
1. "写出 inp"产出的 **mk2inpmap.txt 手动放入 FEM 预计算结果文件夹**（程序不自动放）；
2. 编辑批处理：gfedatapath=预计算结果文件夹名、gfefilename=.fea 文件名、SPH 程序路径；
3. 双击/命令行执行批处理提交 `<作业名>_Def.xml`。

## 后处理

**S11 [③]** GUI 后处理同窗口打开 FEM 的 .db 与 SPH 的 `_out/particle/*.vtk`（流体选 _Fluid 后缀）叠加查看（c09 §9.8）。

# 已知不确定项
1. 水桶几何具体尺寸（半径/高度）审计未收录，仅知拉伸矢量 (0,0,1.5)，需 .pre 反查（S1）。
2. sph 对象区域绑定字段名、sph_step 求解参数页字段宿主——同 ch8 路径不确定项 2/3（S5/S6）。
3. 预设地震波库命令流加载入口未核（S7）。
4. FEM 预计算"算 1% 中止"无程序化判据，需人工盯监控或脚本轮询 db 大小（S9）。
5. 晃动激励施加区域（桶底/整体）审计未明录，复刻前对照 .pre（S7）。


---
# ===== 路径_ch10_抗震地铁站.md =====

# 路径_ch10 抗震分析-地铁站（动力 SSI·弹性时程 + 弹塑性增量）

> case: 官方py `Case-dyna`(弹性)/`Case-dyna-pla`(弹塑性)；dump: `Case-1` steps=Initial→DynamicStep（04_状态dump/ch10/，弹性版）；另 Dead/Live/Comb 静力工况（YJK 自动）
> 单位制 **m-t-kPa**（C30 E=3.0e7 kPa, ρ=2.5 t/m³；按 density/E 反推，勿照搬 ch01 的 mm-t-MPa）
> 真值序：**官方py v3.x（E:\GFE2026\典型案例与教程\第10章 地铁站抗震分析案例\第十章命令流-弹性.py 411行 + 第十章命令流-弹塑性.py 916行，2026-06-11 比对）> dump** > GFE-Cases_c09/c10/c11（手册 §10.1-10.24）> Cmd 手册 §8.1；详细论证见 _synthesis_ch10
> ⚠ 官方 py 是**会话录制稿非洁净脚本**：引用了大量 YJK 自动产物（StaticStep/AllGrav/jiegou/StoryDrift-AllFloor/StoryShear-All/Comb_M_*）和 GUI 预设遗留名（field_mgr().delete 的 FO-DynaEla-* 清单），裸重放须先确认这些对象存在
> tier_summary: **①×19（其中 6 项 v3.x 可达、v2.15 仍断点）②×1 ③×1**

## A. 结构几何与荷载（YJK 导入，手册 §10.2-10.3）

- **S1 [①官方实证v3.x；v2.15 仍断点]** 导入 YJK → SuperStru + BasementBoundary + 214 集合(floorN-All*/jiegou/StoryDrift-*) + Dead/Live/Comb 工况荷载(P_SLAB type=6 压力、M_SLAB type=10 附加质量) + Initial/StaticStep/DynamicStep 分析步全部自动生成
  - 官方原文: `gfeio.get_current().import_yjk(yjk_path, yjk_para(43元), ['',''], True, '', False)`；43 元参数与 Cmd 手册 §8.1 示例逐位一致（[1,1,0,1,1,0,1,0, 300,5,40,0,510,2800,200,610, 150,3,1,0,5,250,0,40000, 1,10,10,300,140,260,80,160, 400,179,310,50,1,260,0,100, 0,0,0]）
  - 坑: para_int 43 元取值场景相关（ch15 官方 py 同接口但第 11/13/14/20/24 位等多处不同），不能跨场景照抄；目录须同含 dtlmodel.ydb+dtlCalc.ydb（缺一不可，Jccad_0.ydb 可选且会被 dtlmodel 内手输基础信息静默顶掉）
  - 坑: YJK 自动建 Initial/StaticStep/DynamicStep——但官方 py **仍另行自建动力步 Dyna-Step**（见 S12），自动步与自建步并存，弹塑性工况里 StaticStep 用 YJK 自动的、动力步用自建的
  - ⚠ 本机 v2.15 无 import_yjk API（实测 2026-06-10，_audit/phase7/实测裁决.md），需 GUI 导入或升级 PrePo

## B. 土体材料与一维土层（手册 §10.4-10.5）

- **S2 [①官方实证v3.x；v2.15 仍断点]** 导入土体材料 .gmat → 7 层 4-3/5H-2/6H/7H-A/7H-B/8H/9H（E 155 MPa→17.9 GPa 递增）
  - 官方原文: `inst = GFE.io.get_current(); inst.import_mat(gmat_path)`（gmat 名 **tu-Elastic.gmat——弹塑性版也用同一弹性 gmat**，见 S17）
  - v2.15 替代=逐个 mat_mgr().add（density+elastic 条目，ch11 官方 py 即此写法）
- **S3 [①官方实证v3.x]** 一维土层（dump+官方双证）
  - `o=soil.soil(); o.name='Soil1D-1'; o.depth=[4.72,9.5,11.5,9.5,1.9,5.1,40.0]; o.materials=['4-3','5H-2','6H','7H-A','7H-B','8H','9H']; o.bedrock_mat='9H'; o.depth_dir=2; soil_mgr().add(o)`（官方管理器名 `GFE.Pre.soil.soil_mgr()`）
  - 坑: 对话框点"计算"输出 S 波速与**建议网格尺寸**——无 API，GUI-only（c11 ②）

## C. 土体几何（手册 §10.6-10.8）

- **S4 [①官方实证v3.x]** 快速建土 300×250 → Soil-1（深度随一维土层自动）
  - 官方原文: `builder=GFE.soil.box_builder(); soil=GFE.Pre.soil.soil_mgr().find('Soil1D-1'); builder.set_height(soil.depth, soil.depth_dir); builder.set_parameter(300,250); soil_shape=builder.build()`
  - `db=GFE.soil.data_builder(); db.dimension=3; db.name='Soil-1'; db.layer_shape=soil_shape; db.layer_material=soil.materials; db.build()`（Soil-1-Layer1~7 集合+LayerProp 截面自动生成）
  - **仲裁注**: 官方直接把 soil.depth（自上而下序）原样传 set_height——与 Cmd 手册 ②#88"box_builder 高度须自下而上"相抵触。以官方 py 为准（find 回读 soil 对象再喂 builder 是官方 idiom）；v2.15 上若建出土层颠倒，再按手册倒序重试
- **S5 [①官方实证v3.x]** 土体定位两次平移：形心对齐 + 上移 4m 设埋深
  - 官方原文: `geoprim.builder().translate(['Soil-1'], [-169.284,-123.968,-85.62], False)`；`translate(['Soil-1'],[0,0,4.0], False)`
  - 坑: 本章埋深靠**移土不移结构**（ch11 官方 py 反向：移 SuperStru+BasementBoundary 入土——两式皆官方实跑，本质是相对定位，任选其一）；形心对齐矢量 GUI 由拾取自动填，命令流用 `geotool.centre_of_mass` 自算
- **S6 [①官方实证v3.x]** 布尔裁剪：土体被地下室外轮廓挖出基坑
  - `geoprim.builder().cut('Soil-1', ['BasementBoundary'], True)`
  - 坑: 末参 False 时生成新几何、原始未裁土体残留树中易误选（c10 ②）；BasementBoundary 仅为工具几何，**不参与计算不划网格**

## D. 相互作用（手册 §10.9；dump tie×20 + embed×1）

- **S7 [①官方实证v3.x]** 搜索接触→绑定 Tie（土-结界面，容差 0.01）
  - 官方原文: `sp=GFE.geometry.contact_pair.search_face("Soil-1","SuperStru",0.01)` → 循环每对建 `geometry_surface(surfMgr.auto_name("Soil-Surf"))`/`("Struct-Surf")`，`surf.data=[[geo_id]+list(x) for x in pairs[n]]` → `surfpair=interaction.surface_pair(); surfpair.name=tieMgr.auto_name("Tie"); surfpair.first_surf=…; surfpair.second_surf=…; surfpair.param_number=1; surfpair.parameters=[0.01]; tieMgr.add(surfpair)`
  - 坑: 项目无特殊要求时选"绑定"而非摩擦接触（手册明文）；官方只搜 Soil-1↔SuperStru 一组（dump 中 CP 前缀对涵盖 4 种组合，系 GUI 操作差异）；官方未显式设 surfpair.type（默认 0=绑定）
- **S8 [①dump实证；官方 py 无]** 桩基嵌入土体
  - `e=interaction.embed(); e.name='Embed-1'; e.embedded_names=['floor1-AllCol']; e.host_name='soil'; e.roundoff_tolerance=1e-06; e.exterior_tolerance=0.05; embed_manager().add(e)`
  - **仲裁注**: 官方弹性/弹塑性两版 py 均**无任何 embed 调用**——桩嵌入是 dump 模型里的 GUI 操作产物，未进官方命令流。复刻官方 py 不建 embed；复刻 dump/手册 §10.9 截图按上式建。dump=floor1-AllCol，手册截图 OCR 作 floor0-AllCol——以 dump 为准；host='soil' 是 YJK 预设几何集；嵌入/主区域方向易反

## E. 人工边界 + 地震输入（手册 §10.10-10.11）

- **S9 [①官方实证v3.x]** 边界面质心筛选脚本（官方 idiom，三章通用）→ 表面集 → 人工边界
  - 官方做法: `geotool.get_shape_box_range(shape,0.0)` 取包围盒 → 遍历 `geotool.children(shape, TopAbs_FACE=4)`，按 `geotool.centre_of_mass(face)` 与五个极值面比对（tolerance=1）分拣 front/back/left/right/bottom → `gset_mgr().add(gset_name, faces)` 建 5 个 *_boundary 几何集（兼供 S19 静力 BC 引用）→ `gset.get_shapes_id()` 取 [[id0,id1,id2]] 转 `[[id0,id2,0]]` → `obj=surface.geometry_surface('arc_surface'); obj.data=平铺三元组; GFE.Pre.surface.surf_mgr().add(obj)`
  - `a=artbc.art_bc(); a.name='ArtBC-1'; a.structure='SuperStru'; a.surface='arc_surface'; a.centered=False; a.center=[]; artbc_mgr().add(a)`
  - **仲裁注**: structure 官方 ch10 py=**'SuperStru'**（旧反推记 'Soil-1'，来源手册推断——废弃）。汇总三章实证：ch10 官方=SuperStru / ch11 官方=Soil-1 / ch11 dump=SuperStru / ch15 官方=SuperStru。**官方自己两值混用，该字段是形心参考几何、无统一规则**，复刻哪个对齐哪个
  - 坑: 官方用 `surf_mgr()` 与 `surface_mgr()` 两个别名混用，皆有效；GUI"表面集→转单元集"流程在命令流里即 geometry_surface 直接引用（to_node_surface 默认 False）
- **S10 [①官方实证v3.x]** 自建幅值 + 地震场地反应（**仅 y 向**，时程）
  - 官方注释明言"**命令流尚未提供加载预设**，故此处经过处理后，再加入幅值函数"——预设波须手工贴值：`amp=amplitude.amplitude(); amp.type=0; amp.name='Amp-y'; amp.spectrum_type=-1; amp.gravity=0.0; amp.value=[t,a,…]（0~20s@0.02s 归一化 1002 对平铺）; amp_mgr().add(amp)`（波形数据=25_RH1TG025 人工波，与 ch11 官方同源）
  - `v=vibration.vibra_load(); v.name='VibLoad'; v.amp_bottom_x=''; v.amp_bottom_y='Amp-y'; v.amp_bottom_z=''; v.pwave_dir=2; v.soil='Soil1D-1'; v.is_outcrop=True; v.input_loc=-1; v.level=0` + **14 个 set_parameter 官方全集**: DampConvOrder='1', DampScale='1', MaxIter='100', N='4096', Rr='0.5', SubLayerHeight='1', TimeInterval='0.02', Tol='1e-2', UI_ARBot='', UI_ARTop='', UI_Method='0', UseAmp='true', UseEERAMat='true', UseIntgOutp='true' → `GFE.Pre.vibration.vib_mgr().add(v)`
  - 坑: 空串=该向不输入（官方实证）；is_outcrop=True 时 input_loc 失效固定基岩露头（Cmd ②50）；模块路径 GFE.Pre.vibration 非章节名 vibload（Cmd ②26）；多向输入三向幅值**点数必须一致**（*Wave 缓冲区 bug，0xC0000374）；官方 py 里 `vibraload_manager()` 与 `vib_mgr()` 别名混用

## F. 网格（手册 §10.12）

- **S11 [①官方实证v3.x]** 土体 size=5、结构 size=2（官方）；Algorithm=2/Algorithm3D=10；BasementBoundary 不划
  - 官方 controller: number_option 含 'Mesh.Algorithm':2.0, 'Mesh.Algorithm3D':10.0（其余模板键照抄）；user_option={'GFE.AutoTransfinite':True,'GFE.DefaultSize':5.0(土)/2.0(结构),'GFE.Optimize':False,'GFE.Recombine2D':False}；`controller.auto_transfinite=True`；顺序先 Soil-1 后 SuperStru
  - **仲裁注**: 旧反推记土 3/结构 1（来源手册"建议网格尺寸"），官方 py 为 5/2——以官方为准；尺寸本就是建模决策，按算力取舍
  - 坑: 网格选项字典勿省键（Cmd ②72）；geom_to_type 固定模板 {0:0,1:5,2:9,3:14,4:17,5:19,6:20,7:22,8:17}；⚠ auto_transfinite 在 v2.15 小楼案例实测会崩——官方 v3.x 全程开启，版本相关，v2.15 上慎开

## G. 分析步 / 工况（手册 §10.13）

- **S12 [①官方实证v3.x]** 官方**自建**显式动力步（不沿用 YJK 自动 DynamicStep）
  - `s=step.dynamic_explicit_step(); s.name='Dyna-Step'; s.description=''; s.nlgeom=False; s.period=20.0; ms=step.mass_scaling(); ms.region='*'; ms.type=1; ms.frequency=100; ms.target_time=5e-05; s.mass_scaling=[ms]; step_mgr().add(s)`（mass_scaling 用**属性赋值** `obj.mass_scaling=[ms]`，v3.x 实证）
  - **仲裁注**: dump 的 YJK 自动 DynamicStep 是 period=40/target_time=2e-4；官方自建 Dyna-Step 是 period=20/5e-5——两套并存，period 跟波长、target_time 跟精度走
  - 坑: **显式步长=质量缩放 target_time**，不设则锁默认 5e-5（c06 ②）；材料阻尼 β 必须=0 否则显式稳定性崩
- **S13 [①官方实证v3.x]** 工况挂载——**v3.x 用映射属性字典直接赋值**（v2.15 只有 8 个 set_* 写接口）
  ```python
  c=case.case(); c.name='Case-dyna'; c.steps=['Initial','Dyna-Step']
  c.bcs['Dyna-Step']=[]                                          # 空键也显式赋（官方风格）
  c.bcs['Initial']=['Comb_M_SLAB10_383','Comb_M_SLAB78_384']     # YJK 附加质量挂 Initial
  c.initialConditions['Initial']=[]
  c.vload['Dyna-Step']=['VibLoad']
  c.artbc['Dyna-Step']=['ArtBC-1']
  c.fieldReqs['Dyna-Step']=['FieldOutput-1']; c.histReqs['Dyna-Step']=[]
  c.elemAdd['Dyna-Step']=[]; c.elemDel['Dyna-Step']=[]
  case_mgr().add(c)
  ```
  - 官方场输出 idiom: 先 `field_mgr().add(o)`（仅 node_output A/U）再**同名重建 + `field_mgr().edit(o)`** 追加 element_output E/S——edit 按 name 整体替换
  - 坑: 动力工况必含"场地反应+人工边界+动力场输出"三项，缺一静默失效（c06 ②）；弹性动力步**不挂 AllGrav**（与弹塑性相反）；v2.15 复刻把字典赋值换 set_bcs/set_vload/set_artbc/set_fieldReqs

## H. 求解 / 后处理

- **S14 [①官方实证v3.x]** 写 INP：`from GFE.io import inpio; w=inpio.writer(inp_path); w.set_case('Case-dyna'); w.perform()`
- **S15 [③]** 提交 GFEXC(CPU)/GFEXG(GPU)；层间位移角查看——GUI/求解器层

## I. 弹塑性增量（手册 §10.16-10.24；官方=第十章命令流-弹塑性.py）

- **S16 [①官方实证v3.x]** 派生方式：官方弹塑性 py = **弹性脚本全文重放（L1-446 与弹性版逐行同构）+ 追加段**，并非"复制 .pre 改"（手册 §10.16 的"复制副本"是 GUI 等价物）。追加段顺序：compute_era → 调幅波回填 → 5 静力 BC → 删弹性输出预设 + FO-DynaPla 5 件 → 三段式工况 → convert_material/convert_reinforce → 写 INP
- **S17 [②]** 土体弹塑性：**官方 py 不转 Davidenkov**——重点仲裁结果（2026-06-11）：
  - 官方弹塑性版土体仍用 **tu-Elastic.gmat 弹性材料**，土的非线性全靠 `UseEERAMat='true'`（EERA 等效线性场地反应）+ compute_era 调幅迭代；全文 **无 convert_to_davidenkov、无 material.user、无 test_data** 调用
  - 三态并记: ①官方 v3.x py=EERA 等效线性土+弹塑性结构；②手册 GUI §10.17="工程—土体材料转换"就地追加 Davidenkov A/B/γ0 参数块（例 A=1.7677,B=0.41904,γ0=1e-4，可"还原"，前提材料有 test data）；③dump v2.15（ch11 同构）=土未转、elastic+MC+Rayleigh α
  - 结论: **Davidenkov 材料在官方命令流中无 API 路径**，唯一入口仍是 GUI 转换或手写 INP *User Material 块（29 SDV Depvar 格式见 reference_davidenkov_keywords）
  - ⚠ 本机 v2.15 无 convert_to_davidenkov API（实测 2026-06-10 确证缺位）
- **S18 [①官方实证v3.x；v2.15 仍断点]** YJK 结构材料转非线性 + 配筋转换——官方双 API 直证：
  - `GFE.geometry.geotool.convert_material(1)`；`GFE.geometry.geotool.convert_reinforce(1)`（**配筋转换 API 存在**，推翻旧反推"配筋 API 未见"）
  - 调用时机官方实证: **工况定义之后、写 INP 之前**（脚本末尾）；重复转换返回 False≠失败（Cmd ②65）
  - ⚠ v2.15 无此二 API，GUI"工程—材料及配筋转换"
- **S19 [①官方实证v3.x]** 静力边界 5 件（引用 S9 质心筛选的 *_boundary 几何集）：
  - BC-bott(type=0 全约束, set='bottom_boundary', valid_dof=0)、BC-left/right(type=1, valid_dof=1, 仅 U1=0)、BC-front/back(type=1, valid_dof=2, 仅 U2=0)；共同字段 value=[0]*6, amplitude='', is_node_set=True, node_id=[]
  - 比旧反推 3 件版（BC_X/BC_Y/BC_base）更细：左右/前后四个侧面各一条法向约束
- **S20 [①官方实证v3.x；v2.15 仍断点]** 场地反应调幅（等效线性迭代）：
  - 官方原文: `GFE.geometry.geotool.compute_era(2.2, 5, 0.01, 1, 'VibLoad')`——目标地表峰值 **2.2 m/s²**（≈0.22g；勿按 gal 填 220）、迭代 5、容差 0.01、**第 4 参=1**（旧反推猜 a_layer=2——以官方为准取 1）
  - 调用时机官方实证: vib_mgr().add 之后**立即**调（先于接触/网格/步/工况）
  - 调幅产物回填 idiom: 官方随后**同名重 add 'Amp-y'**，值=原波×0.7238（调幅系数），同名 add=更新
  - ⚠ 本机 v2.15 无 compute_era API（实测 2026-06-10），调幅需 GUI
- **S21 [①官方实证v3.x]** 弹塑性三段式工况（官方 Case-dyna-pla 直证 AllGrav 双挂）：
  ```python
  c=case.case(); c.name='Case-dyna-pla'; c.steps=['Initial','StaticStep','Dyna-Step']
  c.bcs['Initial']=['Comb_M_SLAB10_383','Comb_M_SLAB78_384']
  c.bcs['StaticStep']=['AllGrav','BC-bott','BC-left','BC-right','BC-front','BC-back']  # 地应力平衡：重力+五面固定
  c.bcs['Dyna-Step']=['AllGrav']                                  # 动力步再挂 AllGrav，固定 BC 撤掉换 ArtBC
  c.vload['Dyna-Step']=['VibLoad']; c.artbc['Dyna-Step']=['ArtBC-1']
  c.fieldReqs['StaticStep']=['FO-static']
  c.fieldReqs['Dyna-Step']=['FO-DynaPla-All','FO-DynaPla-Jiegou','FO-DynaPla-ShearForce','EO-DynaPla-Max','EO-DynaPla-Min']
  case_mgr().add(c)
  ```
  - **地应力平衡官方版**: 无专门 geostatic 步、无 *Initial Conditions——就是 StaticStep（YJK 自动 static_general，py 未创建直接引用）+ AllGrav（YJK 自动重力，py 未创建）+ 五面固定，进动力步撤固定、留 AllGrav、挂人工边界
  - 场输出官方版: 先 `field_mgr().delete(['FO-Static','FO-DynaEla-Jiegou-0.02','FO-DynaEla-ShearForce','FO-DynaEla-All','FO-DynaEla-Max','FO-DynaEla-Min','FieldOutput-1'])` 清弹性预设，再 add：FO-DynaPla-All（U+PE 全模型 + jiegou 集 DAMAGEC/DAMAGET，0.1s，step='Step-1'）；FO-DynaPla-Jiegou（StoryDrift-AllFloor 节点 U，0.02s）；FO-DynaPla-ShearForce（StoryShear-All 单元 NFORC1/NFORC2，0.02s）；EO-DynaPla-Max/Min（jiegou DAMAGEC/DAMAGET 包络，type=2，method=2(max)/3(min)，time_type=-1，time_interval=0）
  - 坑: 动力步漏挂 AllGrav 则进入动力步重力消失（§10.22 明文）；reg_type 0=集合 -1=整模型；官方 obj.step 字段有 'Step-1' 遗留值（与实际步名 Dyna-Step 不符仍可跑，挂载以 case.fieldReqs 为准）

## 已知不确定项
1. S13/S21 中 Initial 步 Comb_M 清单官方 py 直证 2 条（SLAB10_383/SLAB78_384）；case 字典 v3.x 可读、v2.15 setter 写专用不可回读，v2.15 以导出 INP 为准。
2. import_yjk/import_mat/convert_to_davidenkov/compute_era/convert_material/convert_reinforce：v2.15 实测全部缺位（2026-06-10，_audit/phase7/实测裁决.md），须 GUI 或升级 PrePo；其中 import_yjk/import_mat/compute_era/convert_material/convert_reinforce 已被官方 v3.x py 实证可用，convert_to_davidenkov 在官方 py 中也未出现（GUI-only 嫌疑加重）。
3. 官方弹塑性 py 引用的 StaticStep/AllGrav/jiegou 等 YJK 自动产物清单完整性未逐一核对 dump；裸重放前先 step_mgr/bc_mgr name_list 自检。
4. 调幅系数 0.7238 的来源（compute_era 输出回贴 or 手算 2.2/PGA_raw）未证；复刻时以 compute_era 实际输出为准。


---
# ===== 路径_ch11_抗震地上地下.md =====

# 路径_ch11 抗震分析-地上地下结构（带地下室高层·动力 SSI·dump 为弹塑性态）

> case: dump `Case-1` steps=Initial→**StaticStep**→DynamicStep（04_状态dump/ch1112_plastic/，3 步弹塑性全证）；官方py `Case-1` steps=Initial→Dyna-1（**弹性简化版**）
> 单位制 **m-t-kPa**；与 ch10 几乎同构，本路径完整可独立执行，但凡与 ch10 相同的坑只引不重述
> 真值序：**官方py v3.x（E:\GFE2026\典型案例与教程\第11章 高层带地下室抗震分析案例\CM11.py 613行，2026-06-11 比对）与 dump 并列**——⚠ 二者是**两个不同终态**：官方 py=4 层手写弹性土+弹性时程（无静力步/无重力/无材料转换）；dump=8 层 gmat 土+MC+三段式弹塑性。复刻前先选终态 > GFE-Cases_c11/c12（手册 §11.1-11.25）> Cmd 手册 §8.1；详见 _synthesis_ch11_13_15 §A
> tier_summary: **①×15（其中 2 项 v3.x 可达、v2.15 仍断点）②×2 ③×1**

## A. 结构（YJK 导入，手册 §11.2-11.4）

- **S1 [①官方实证v3.x；v2.15 仍断点]** 导入 YJK → SuperStru + BasementBoundary + 844 集合(floor0~N-All*/jiegou/StoryDrift-*/StoryShear-All) + Dead/Live/Comb 工况荷载(LL_BEAM type=8 线载、P_SLAB type=6、M_SLAB type=10、FV type=5) + 三个分析步自动生成
  - 官方原文: `gfeio.get_current().import_yjk(yjk_path, yjk_para(43元，与 ch10 官方逐位相同), ['',''], True, '', False)`
  - 断点: 同 ch10 S1（para_int 场景相关；dtlmodel.ydb+dtlCalc.ydb 双必要；⚠ v2.15 无此 API）

## B. 土体（手册 §11.5-11.9）

- **S2 [①官方实证v3.x，但与 dump 分歧]** 土体材料——三态并记：
  - **官方 v3.x py**: 不导 .gmat，**手写 4 个纯弹性土材料**（粉土/砂土/黏土/砾石）：`obj=material.material(); obj.name='粉土'; d=material.density(); d.temp_dp=False; d.n_param=1; d.params=[1.9]; e=material.elastic(); e.temp_dp=False; e.n_param=2; e.type=0; e.moduli_time_scale=0; e.compression=False; e.tension=False; e.params=[30000.0,0.35]; obj.entries=[d,e]; mat_mgr().add(obj)`（砂土 1.8/[70000,0.3]、黏土 1.6/[10000,0.4]、砾石 2.0/[100000,0.2]）——**无阻尼、无 MC、无 Davidenkov**
  - **dump v2.15 实况**: .gmat 导入 8 个 tu*（tu1-2: density=1.83, elastic=[150000,0.3], damping=[**1.08415, 0.0**], mohr_coulomb(c=[8,0], φ/ψ=[18,9])）——elastic+MC+Rayleigh α 且 **β=0**
  - **手册 GUI**: .gmat 导入后"工程—土体材料转换"转 Davidenkov
  - import_mat API 已被 ch10/ch15 官方 py 实证（v3.x ①）；v2.15 缺位时用官方 ch11 的 mat_mgr().add 手写式
- **S3 [①官方实证v3.x，但与 dump 分歧]** 一维土层——官方与 dump 是**不同土剖面**：
  - 官方: `o.name='Soil1D-1'; o.depth=[2.0,4.0,6.0,5.0]; o.materials=['砾石','粉土','黏土','砂土']; o.bedrock_mat='砂土'; o.depth_dir=2`
  - dump: name='soil_1D', depth=[3,4,8.5,14.5,3,5,7], materials=tu1-2…tu7-1, bedrock='tu7-1'（8 个 tu 材料只有 7 个进剖面，tu2-2 未用）
  - 坑: GUI 支持整表剪贴板"粘贴"导入（c11 ②）
- **S4 [①官方实证v3.x]** 快速建土——官方 **100×40**（dump 260×260，又一处模型版本差异）
  - 官方: `b=GFE.soil.box_builder(); soil=soil_mgr().find('Soil1D-1'); b.set_height(soil.depth, soil.depth_dir); b.set_parameter(100,40); ls=b.build()`；data_builder 同 ch10 S4（直传 soil.depth 原序，见 ch10 S4 仲裁注）
- **S5 [①官方实证v3.x]** 对位 + 裁剪——官方**移结构入土**（与 ch10"移土不移结构"相反，两式皆官方实跑）：
  - `geoprim.builder().translate(['SuperStru','BasementBoundary'], [26.0,14.0,17.0], False)`；`geoprim.builder().cut('Soil-1',['BasementBoundary'],True)`
  - 坑: 同 ch10 S6（不替换则旧土残留；BasementBoundary 不划网格）

## C. 相互作用 / 人工边界 / 地震输入（手册 §11.10-11.12）

- **S6 [①官方实证v3.x]** 搜索接触→绑定 Tie（**本章无桩基嵌入**，官方 py 与 dump 一致 embed 为空——与 ch10 dump 的差异点）
  - 官方扩展 idiom——**先批量搜全组合再按序号挑**: search_list=[['SuperStru','BasementBoundary'],['SuperStru','Soil-1'],['BasementBoundary','Soil-1']] 三组全搜入 search_result，`tie_list=[0..15]` 按索引取 16 对 → 命名 `'CP-'+geo1_name+'-'+geo2_name+'-'+str(i+1)+'-master/-slave'` → surface_pair(param_number=1, parameters=[0.01]) → tie_mgr.add
  - （dump 命名 Soil-Surf-n/Struct-Surf-n 是 ch10 式逐对命名，两种命名 idiom 并存）
- **S7 [①官方实证v3.x，与 dump 相反]** 边界表面集 + 人工边界
  - 官方手写质心比对循环（与 ch10 通用脚本不同的简化版：min/max 初始 0、用 `==` 精确比对质心坐标——**仅适用规则箱体**，有浮点风险）→ `obj=surface.geometry_surface('surface-1'); obj.name='Surface-1'; obj.data=faceID; obj.to_node_surface=False; surface_mgr().add(obj)`
  - `a=artbc.art_bc(); a.name='ArtBC-1'; a.structure='Soil-1'; a.surface='Surface-1'; a.centered=False; a.center=[]; artbc_mgr().add(a)`
  - **仲裁注（任务焦点）**: structure 官方 ch11 py=**'Soil-1'**；dump v2.15 实况=**'SuperStru'**；ch10/ch15 官方=SuperStru。四处实证两值混用——该字段是形心参考几何、无统一规则、非正确性关键，复刻哪个对齐哪个（旧"待仲裁⑨"关闭）
- **S8 [①官方实证v3.x]** 幅值 + 地震场地反应——三态并记：
  - **官方 v3.x**: 自建 amplitude 名 `'25_RH1TG025_(RenGong_T_025)_x_Zhu'`（type=0, spectrum_type=-1, gravity=0.0, 0~20s@0.02s 归一化 RH1TG025 人工波）→ `v=vibra_load(); v.name='VibLoad-1'; v.amp_bottom_x=''; v.amp_bottom_y='25_RH1TG025_(RenGong_T_025)_x_Zhu'; v.amp_bottom_z=''; v.pwave_dir=2; v.soil='Soil1D-1'; v.is_outcrop=True; v.input_loc=-1; v.level=0` + 14 个 set_parameter（与 ch10 S10 官方全集逐键相同）
  - ⚠ 官方坑: **幅值名带 `_x_` 却挂在 amp_bottom_y**——名实不一致是官方原文实况，复刻照抄勿"纠正"
  - **dump v2.15**: x 向自建波 Amp-1 挂 amp_bottom_x，soil='soil_1D'
  - **手册 §11.12**: y 向预设波 25_RH1TG025
  - 坑: 多向输入三向点数必须一致（*Wave bug）；官方无 ElCentro——本章官方激励=RH1TG025 人工波 y 向

## D. 网格（手册 §11.13）

- **S9 [①官方实证v3.x]** 官方一套 controller 划两域：'Mesh.Algorithm':8.0, 'Mesh.Algorithm3D':1.0, 'GFE.DefaultSize':2.0, 'GFE.Recombine2D':True, AutoTransfinite=True；顺序**先 SuperStru 后 Soil-1**；BasementBoundary 不划
  - 仲裁注: 旧反推记土 3/结构 1 两套尺寸（手册）；官方统一 size=2 一套参数。Algorithm 8+3D 1+Recombine2D True 是结构六面体取向（ch15 官方同此组合）
  - 官方顺序注: 网格划分放在**工况定义之后**（建模顺序自由的直接证据，INP 在 writer.perform 时刷新）
  - 坑: 截图旁证存在 "Boolean Operation failed!" 失败模式——布尔/网格失败看输出窗，未划网格几何导 INP 仅警告被静默跳过

## E. 弹塑性材料转换（手册 §11.17-11.19；dump 实证状态；**官方 ch11 py 不含本节**）

- **S10 [①v3.x 可达（援引 ch10 官方）；v2.15 仍断点]** YJK 结构材料转非线性 + 配筋
  - 官方 API 已在 ch10 弹塑性 py 直证：`geotool.convert_material(1)` + `geotool.convert_reinforce(1)`（配筋 API 存在，推翻旧"未见"），时机=工况后写 INP 前
  - dump 实证产物: C1/C2_Mat30/35/60 已变 `user(constants=[E,…7 元], user_type=1)`（混凝土 CDP 类用户材料）+ damping(0,0)
  - ⚠ v2.15 无此二 API，GUI"工程—材料及配筋转换"（材料"非线性"+配筋"YJK"）
- **S11 [②]** 土体材料转 Davidenkov——**官方命令流无路径**（ch10 弹塑性官方 py 用 EERA 等效线性绕开，见 ch10 S17 三态仲裁）：
  - GUI"工程—土体材料转换"就地追加 A/B/γ0 参数块；`convert_to_davidenkov` 在 v2.15 与官方 v3.x py 中均未出现
  - 坑: **dump 实模型土体并未转**——tu* 仍 elastic+MC+Rayleigh α；官方 py 干脆纯弹性。复刻手册流程才转 Davidenkov，三个终态动力响应互不相同，属建模决策点
- **S12 [①dump实证；官方 ch11 py 无]** 静力边界（弹塑性终态用）：BC-1 全约束(type=0, set='PickedSet-1'，底面)、BC-2(type=1, valid_dof=2, 'PickedSet-2')、BC-3(type=1, valid_dof=1, 'PickedSet-3')；AllGrav(type=7, value=[0,0,-9.8], set='')
  - 命令流复刻推荐 ch10 S19 官方式：质心筛选建 bottom/left/right/front/back_boundary 几何集 + 5 条 BC（比 PickedSet 稳）
- **S13 [①v3.x 可达（援引 ch10 官方）；v2.15 仍断点]** 场地反应调幅：`geotool.compute_era(2.2, 5, 0.01, 1, 'VibLoad-1')`——第 4 参官方实证=**1**（旧猜 2 废弃）；调幅产物同名重 add 幅值回填（ch10 S20）
  - ⚠ v2.15 无 compute_era，GUI"时程分析(非线性)+调幅 2.2 m/s²/迭代5/容差0.01/去线性趋势"

## F. 场输出 / 工况（手册 §11.22-11.23）

- **S14 [①]** 弹塑性 5 输出（dump 全证 + ch10 弹塑性官方 py 字段级同构互证）：
  - FO-DynaPla-All（节点 U + 单元 PE + jiegou 集 DAMAGEC/DAMAGET，间隔 0.1）；FO-DynaPla-Jiegou（StoryDrift-AllFloor 节点 U，0.02）；FO-DynaPla-ShearForce（StoryShear-All 单元 NFORC1/NFORC2，0.02）；EO-DynaPla-Max/Min（jiegou DAMAGEC/DAMAGET 包络，type=2，method=2/3，time_type=-1）
  - 官方弹性版工况引用 'FO-DynaEla-All' 但 **py 内未创建**（GUI 预设遗留）——裸重放前须先建或剔除
  - 坑: 包络输出 type=2、time_interval=0；reg_type 0=集合 -1=整模型（Cmd ②32 字段说明错位）
- **S15 [①官方实证v3.x（弹性版工况）]** 工况——官方弹性版直证 v3.x 字典挂载：
  ```python
  c=case.case(); c.name='Case-1'; c.steps=['Initial','Dyna-1']
  c.bcs['Dyna-1']=[]
  c.bcs['Initial']=['Comb_M_SLAB3_109','Comb_M_SLAB3_110','Comb_M_SLAB4_111','Comb_M_Point100',
                    'Comb_M_Point101','Comb_M_Point102','Comb_M_Point103','Comb_M_BEAM0_88',
                    'Comb_M_BEAM1_89','Comb_M_BEAM4_90','Comb_M_BEAM4_91','Comb_M_BEAM2_92']  # 12 条官方直证
  c.initialConditions['Initial']=[]
  c.vload['Dyna-1']=['VibLoad-1']; c.artbc['Dyna-1']=['ArtBC-1']
  c.fieldReqs['Dyna-1']=['FO-DynaEla-All']; c.histReqs['Dyna-1']=[]
  c.elemAdd['Dyna-1']=[]; c.elemDel['Dyna-1']=[]
  case_mgr().add(c)
  ```
  - 弹塑性三段式（dump steps 直证 + ch10 官方 Case-dyna-pla 同构）：steps=['Initial','StaticStep','DynamicStep']；StaticStep 挂 AllGrav+静力 BC；**DynamicStep 再挂 AllGrav**（双挂规则官方在 ch10 弹塑性 py 直证 `c.bcs['Dyna-Step']=['AllGrav']`）
  - 坑: 动力步漏挂 AllGrav 重力即消失（§11.23 明文，与施工模拟"只挂第一步"规则相反）；§11.14 正文与截图挂载描述不一致，以 ch10 同构挂载为准
- **S16 [①官方实证v3.x，与 dump 分歧]** 步参数：
  - 官方自建: `dynamic_explicit_step(); name='Dyna-1'; nlgeom=**True**; period=20.0; mass_scaling=[ms(type=1,frequency=100,region='*',target_time=5e-05)]`（nlgeom=True 是三章官方 py 中唯一开几何非线性的）
  - dump: StaticStep(static_general, period=1, init=1/min=1e-5/max=1)；DynamicStep(dynamic_explicit, period=40, target_time=**2e-4**, nlgeom=False)
  - 坑: 显式步长=target_time；β=0 恒定（tu* 阻尼 α=1.08415, β=0 直证）

## G. 求解 / 后处理

- **S17 [①官方实证v3.x]** 写 INP：`w=inpio.writer(path); w.set_case('Case-1'); w.perform()`
- **S18 [③]** 提交 GFEXC/GFEXG（C=CPU,G=GPU 一字之差）；后处理 U/损伤云图 + 过滤器"单元-集合-jiegou"——GUI

## 已知不确定项
1. **官方 py 与 dump 是两个不同模型版本**（土剖面 4 层 vs 7 层、土域 100×40 vs 260×260、弹性 vs 弹塑性、period 20 vs 40）：官方=教学弹性精简版，dump=手册弹塑性完整版。"复刻官方 py / 复刻 dump / 复刻手册"是三条终态，本路径分块标注。
2. 官方 S7 质心 `==` 精确比对脚本对非规则土体会漏面；通用化用 ch10 S9 的 tolerance 版脚本。
3. PickedSet-1~3 的节点/几何内容（土底面/侧面归属）未从 dump 解出，按 §11.20 语义（底全约束+侧法向）推断；官方替代=ch10 S19 五面几何集。
4. dump Amp-1 波形本体 KB 未存；官方 RH1TG025 归一化波全值在 CM11.py L265-515 可直接取用。


---
# ===== 路径_ch12_施工地上地下综合体.md =====

# 路径_ch12 施工模拟-地上地下综合体（生死单元·逐层开挖+逐层施工）

> 模型与 ch11 同源（dump: 04_状态dump/ch1112_plastic/ 为 ch11+12 合并模型，但其 step/case 是 **ch11 弹塑性终态**——本章施工步链以手册 GFE-Cases_c12（§12.2-12.17）为最高真值，dump 提供几何/材料/集合佐证）
> 单位制 **m-t-kPa**；纯静力多步，无地震模块
> tier_summary: **①×13 ②×4 ③×2**

## A. 模型底座（§12.2-12.7，与 ch11 S1-S5 同构，此处只列差异）

- **S1 [②]** 导入 YJK（连荷载、工况一并导入；dtlmodel.ydb+dtlCalc.ydb 双必要）→ SuperStru + BasementBoundary + floor0~N-All* 集合族 + jiegou
  - `io.get_current().import_yjk(u8dir, para_int(43元), ['',''], True, '', False)`（断点同 ch11 S1）
- **S2 [②]** .gmat 导入土体材料（tu1-2~tu7-1；import_mat 本机 spec 未见，可逐个 mat_mgr().add，参数见 ch11 S2）
- **S3 [①]** 一维土层 soil_1D（depth=[3,4,8.5,14.5,3,5,7]，详 ch11 S3）→ 快速建土 **260×260**（box_builder+data_builder，详 ch11 S4）
- **S4 [①]** 平移对位（土面形心→地下室外轮廓上表面形心）：`geoprim.builder().translate(['Soil-1'],[dx,dy,dz])`

## B. 被挖土体的显式构造（§12.8-12.11——本章区别于 ch10/11 的特有步骤）

- **S5 [①]** 布尔取交：土体 ∩ 地下室外轮廓 → 被挖土体新几何（开挖对象要先"实体化"才能做生死单元）
  - `geoprim.builder().common(['Soil-1','BasementBoundary'])`（生成 BoolCompute-N）
  - 坑: 取交/分割/裁剪三种布尔语义不同选错拓扑全错（c07 ②）；取交**不替换**原几何，产物与原土体重叠是预期状态
- **S6 [①]** 为被挖土体建几何集（供生死单元与截面引用）
  - `gs=set.gset_basic('被挖土体集名'); gset_manager().add(...)`（GUI 流程"创建集合—激活实体选择"）
  - 坑: §12.9 手册操作文字是 §12.8 的复制粘贴错误，以功能入口为准（c12 ②笔误）
- **S7 [①]** 截面属性复制 + 集合重指派：把对应土层的 LayerProp 复制一份、elset_name 改成被挖土体集 → 新挖土体获得正确材料
  - `src=sect_mgr().find('Soil-1-LayerProp-N'); p=section.property_solid(); p.name='…-copy'; p.mat_name=src.mat_name; p.elset_name='被挖土体集名'; p.type=0; sect_mgr().add(p)`
  - 坑: 被挖土体跨多土层时需按层分别取交/赋属性；"颜色设置→Material"着色校验赋材正确性（GUI）
- **S8 [①]** 布尔裁剪：原土体减去地下室外轮廓（被挖土体已另存，原土体腾出空腔由被挖体填回）
  - `geoprim.builder().cut('Soil-1',['BasementBoundary'],True)`
  - 坑: 勾"替换原始图形"；裁剪后被挖土体与土体空腔共形但**不共节点**——依赖后续搜索接触绑定或印刻，手册本章走绑定

## C. 相互作用 / 边界（§12.12-12.13）

- **S9 [①]** 搜索接触→绑定 Tie-1~10（查找区域含 Soil-1/SuperStru/被挖土体，容差 0.01；类型默认"绑定"）
  - `search_face(...,0.01)` → geometry_surface 对 → `surface_pair(type=0, parameters=[0.01])` → `tie_manager().add`
- **S10 [①]** 边界 + 重力：底面全约束(type=0) + 四侧法向(type=1, valid_dof=1/2, U1=x 向 U2=y 向) + AllGrav(type=7, value=[0,0,-9.8])
  - dump 佐证集合：bottom/left/right/front/back_boundary 几何集已在 gset 中，引用它们建 BC

## D. 网格（§12.14）

- **S11 [①]** 土体+被挖土体四面体 size=3、结构六面体 size=1、BasementBoundary 不划
  - `c=mesh_generator.controller(); c.user_option={…'GFE.DefaultSize':3.0…}; c.generate_dim=3; mesh_generator.generator().mesh(['Soil-1','被挖土体'],c)`；结构 size=1 另批
  - 坑: 网格定稿才能做后续单元集类操作；选项字典勿省键

## E. 分析步 / 施工工况（§12.15-12.17——本章核心）

- **S12 [①]** 创建 3 个静力分析步（**几何非线性全开**），后接施工助手批量生成的逐层步
  - `s=step.static_general_step(); s.name='Static-1'; s.nlgeom=True; s.period=1.0; s.init_inc=1.0; s.min_inc=1e-05; s.max_inc=1.0; step_manager().add(s)`（×3：天然场地/开挖/底板回筑，名称见不确定项 2）
  - 坑: nlgeom 影响"随后的"分析步；本章用普通静力步非 geo_static_step（手册 §12.15 直证"类型选静力分析"）
- **S13 [①]** 生死单元-移除：第一步移除 **jiegou 全体**模拟天然场地（YJK 导入后结构已在模型里），第二步移除被挖土体模拟开挖
  ```python
  c=case.case(); c.name='Case-1'
  c.steps=['Initial','Static-1','Static-2','Static-3', …施工助手生成的逐层步]
  c.set_bcs('Initial',[底面全约束,侧向法向约束…])
  c.set_bcs('Static-1',['AllGrav'])            # 重力只挂第一步，后续步不重复添加（§12.16 明文）
  c.set_fieldReqs('Static-1',['FO-Static'])
  c.set_elemDel('Static-1',['jiegou'])          # 天然场地：杀掉全部结构
  c.set_elemDel('Static-2',['被挖土体集名'])      # 开挖
  case_mgr().add(c)
  ```
  - 坑: set_elemDel 传**几何集名**；施工模拟 AllGrav 只挂第一步——与弹塑性动力"动力步再挂一次"规则**相反**，两类分析切换时极易弄错（c12 ②）；土层集合初始即激活、不可再 elemAdd（对象引用总览 §8）
- **S14 [②]** 施工助手逐层回筑：区域类型"几何集"+正则 `floor.*All$` 搜层集 → 排序"最低点"+"Z" → 选工况设初始步与增量 → 应用，自动生成逐层分析步并写入"生死单元-添加"
  - 断点: 施工助手 GUI 专有无命令流 API；命令流等价：
    `for i,f in enumerate(sorted_floors): c.set_elemAdd(f'Stage-{i+1}', [f'floor{i}-All'])`（步需先建好）
  - 坑: 正则搜出的层集**必须手动排序**（最低点+Z），否则施工顺序错乱（c12 ②）；楼层号顺序≠标高顺序
- **S15 [②]** 施工助手二次打开：区域类型切"场输出"，把 FO-Static 批量挂到工况每个分析步
  - 断点: 同上 GUI 助手；命令流等价 `for st in c.steps[1:]: c.set_fieldReqs(st,['FO-Static'])`
- **S16 [①]** 场输出 FO-Static：节点 U/UR/RF/RM + 单元 S/E/SF/SM，time_interval=1（同 ch06 S21 骨架）

## F. 求解 / 后处理

- **S17 [①]** 写 INP 自检（生死单元清单逐字核对）：`w=inpio.writer(path); w.set_case('Case-1'); w.perform()`；多静力步自动选 GFEXN
- **S18 [③]** 工况预览播放生死单元状态（提交前必做的廉价校验）——GUI
- **S19 [③]** 后处理：IsRemoved 过滤 + 逐层施工动画 + 过滤器按集合显示——GUI

## 已知不确定项
1. **dump 不含本章施工态**：ch1112_plastic dump 的 step/case 是 ch11 弹塑性版（3 步 Initial/StaticStep/DynamicStep），ch12 的施工步与工况在该 dump 中不存在；本路径 E 节全部以手册 §12.15-12.17 为真值，无 dump 交叉验证。
2. 3 个静力步的名称与第三步职能（底板/回筑首层?）手册未明示，S12/S13 中 Static-1/2/3 为占位命名；施工助手生成的逐层步名（Stage-n 或 floor 名）未证。
3. 被挖土体集名、是否按土层分多个集（跨层开挖）未证——§12.9-12.10 仅单数表述。
4. 开挖体与原土体界面手册走搜索接触绑定（S9 范围含被挖体）还是布尔印刻共节点，c12 块证据不足，按"裁剪+绑定"理解；复刻前开 .pre 或问原 PDF §12.11-12.12 核对。
5. 本章与 ch11 共用一个 .pre 时，施工工况与地震工况并存（Dead/Live/Comb/Case-1/施工 Case），互不挂扰——工况是引用式组装，未挂载对象对该工况不存在。


---
# ===== 路径_ch13_反应位移法.md =====

# 路径_ch13_反应位移法

- **case**: 实际案例操作手册v2025 第13章「反应位移法」（地下结构抗震拟静力法，**仅二维横断面**，非时程；**无 dump**（.pre 打不开），真值=GFE-Cases c12 §13.x + Cmd 手册）
- **单位制**: 手册未明示，YJK 导入系按 m-t-kPa 自洽（merged 3.1 推断），复刻时按导入材料 density/E 反推确认
- **tier_summary**: ①5 ②4 ③1

## 几何（YJK 导入，无手工建模）

**S1 [①]** 导入主体结构：`GFE.io.import_yjk(u8path, para_int, para_str, ...)`——目录须同含 dtlmodel.ydb + dtlCalc.ydb（缺一不可），路径 UTF-8；版本仅 4.0.0~6.0.0。自动产 SuperStru/floorX-All/分析步等（**本章后续省略分析步创建即因导入已自带**）。

**S2 [①]** 二次导入地连墙（附属结构）：`import_yjk(..., is_accessory=True, name_prefix='DLQ')`——并入第二个模型，材料名加前缀（如 DLQ-C1_Mat35）（§13.4）。
- 坑：para_int 为 43 元整数列表，案例"按默认参数"，各位语义未全核（见尾部）。

## 材料截面

**S3 [①]** 土体材料补**基床系数**：`bed_coefficient()`（kh 水平/kv 垂直，Cmd §2.6.15），走 find→entries 追加→mat_mgr().edit() 三段式。
- 坑（红线级）：①导入材料默认**无**基床系数，缺则接地弹簧无法生成（§13.2/§13.5）；②手册同段误写"基岩系数"，异名同义；③**地基弹簧刚度填 Component 1**（实操经验，勿散填多分量）。

## 集合表面 / 网格

**S4 [①]** 网格：mesh_generator 全局参数+执行（结构六面体 1 / 土四面体 3 量级沿 SSI 惯例；本章正文未给独立网格表）。BasementBoundary 辅助几何**不划网格**。

## 边界荷载前置链（幅值→土层→场地反应）

**S5 [②]** 幅值函数：amplitude 对象本体 ①（value 平铺 (t,a) 对，type=0），但案例用 **GUI"预设"地震时程库**——预设库加载入口未见命令流 API，**断点**：GUI 选取，或从既有 dump 拷波形数据自建 amplitude。

**S6 [①]** 一维土层：`o=GFE.Pre.soil.soil(); o.depth=[...]; o.materials=[...]; o.bedrock_mat='...'; o.depth_dir=1; soil_mgr().add(o)`。
- 坑：①本案例二维横断面，**深度方向选 y（depth_dir=1）**，不是默认 z（§13.6）；②层厚/材料**从高到低**输入；③GUI"计算"按钮（波速/建议网格尺寸）无对应 API，波速可自算 Vs=√(G/ρ)。

**S7 [②]** 地震场地反应（**拟动力分析**模式）：vibra_load 时程字段已核 ①（amp_bottom_x 激活 x 向、soil 关联、is_outcrop），但「用于=拟动力分析」模式开关与「**结构顶/底深度**」（到土表的非负深度，案例 12–14.1，**不是 z 坐标**）两输入未见 API 字段（疑为隐藏属性 level，语义未核）——**断点：GUI 建**。如需调幅可用 `geotool.compute_era(target_acce, iter, tol, a_layer, vibra_name)` ①（a_layer 三档 0=基岩处/1=基岩露头/2=地表）。

## 反应位移法助手（本章核心断点）

**S8 [②]** 工程—反应位移法助手：选结构几何+勾地连墙+选地震场地反应→"生成"，自动建 **惯性力/土层剪力/相对位移/接地弹簧/只压不拉约束/分析步/场输出/工况**。命令流手册 **0 命中**——**大断点：GUI 专有**。
- 手工复现理论可行（boundary 各 type + spring_dashpot + case 全链均 ①），但荷载数值来自场地反应结果，逐节点提取工作量大，**建议此步留 GUI**（_synthesis_ch11_13_15 结论一致）。

**S9 [①]** 底部约束手补并入工况：助手明文**不建底部约束**（§13.10/§13.11）。
```python
from GFE.Pre import boundary, case
b = boundary.boundary(); b.name='BC-bottom'; b.type=0; b.set='<底面集合>'  # 全约束
boundary.bc_mgr().add(b)
c = case.case_mgr().find('<助手生成的工况>'); c.set_bcs('Initial', ['BC-bottom', ...]); case.case_mgr().edit(c)
```
- 坑：case 只有 set_* 无 get_*，挂载验证只能导 INP 查（inpio.writer→set_case→perform）。

**S10 [①]** 场输出：节点 U、区域=整个模型，output_request+node_output，加入工况计算步。

## 求解 / 后处理

**S11 [②]** 作业：命令流无 job API，**断点：GUI** 作业管理器创建+绑定工况+提交；计算核心 GFEXC（CPU）/GFEXG（仅受支持英伟达卡），一字母之差勿拼错。

**S12 [③]** 后处理：GUI 查 U 云图。

# 已知不确定项
1. import_yjk 的 para_int 43 元列表逐位语义未核，案例值="默认"（S1/S2）。
2. 拟动力模式与结构顶底深度在 vibra_load 上的字段宿主未核（隐藏属性 level=? 未实测）（S7）。
3. 反应位移法助手产物（惯性力/土层剪力/相对位移/接地弹簧/只压不拉约束）的对象级参数清单无 dump 佐证，.pre 打不开未能反编译（S8）。
4. 只压不拉约束（compression-only）在命令流的对应类未见——surface_pair 仅 type=0 绑定（S8）。
5. 对照知识（非本章但同族）：**反应加速度法不用人工边界**，边界=底部 Encastre+侧面 U2=0（实操经验，复刻反应加速度法时用，勿混入本章反应位移法路径）。
6. 本章网格尺寸/单元类型案例值正文未独立给出，沿 SSI 惯例外推（S4）。


---
# ===== 路径_ch14_爆炸CONWEP.md =====

# 路径_ch14_爆炸分析（CONWEP）

- **case**: 实际案例操作手册v2025 第14章「爆炸分析」（CONWEP 空气爆破）
- **真值序**: **官方命令流 T14.py（E:\GFE2026\典型案例与教程\第14章, v3.x, 2026-06 全文通读）** > dump=04_状态dump/ch14_plastic > 手册 c13
- **⚠ 两条建模路线并存**: ①手册/dump 路线=基于官网案例7 GFE-model-Plastic .pre 改爆炸件；②**官方 py 路线=从零建**（import_yjk 导结构 + heb.step 导土层几何 + 手写 9 个 MC+退化曲线土材料），两路线爆炸件做法一致，本文以 py 为准、dump 名注括号
- **单位制**: **CONWEP 强制 t-m-kPa**（经验公式单位敏感，套错差数量级，c13 §14.3）；单位换算靠属性 data 系数组自报
- **tier_summary**: ①9 ②1 ③2（官方实证后 S1/S4 细节/S10 部分升级）

## 基底模型

**S0 [③→可绕开]** GUI 路线基底 .pre：官网案例7 GFE-model-Plastic（§14.1，人工下载）。已含 SuperStru/SoilGeom-1/材料 19 种等。
**S0b [官方实证v3.x]** 命令流路线从零建（T14.py）：
- `import_yjk(yjk_path, yjk_para43元, ['',''], True, '', False)` → SuperStru（ch14 实参与 ch6 多位不同：第11位 40、13位 510、24位 40000、26位 10、34位 179、37位 1 等，**不能跨案例照抄**）
- 土层几何 `io.get_current().open_geometry(step_path)` 导 heb.step → 'Shape-1'
- 9 个土材料 TU1-1/1-3/1-5/2-1/2-3/2-5/3-1/3-8/TU4：density+elastic+damping(**params=[2.59055, 0]，α质量阻尼、β=0 恒定**)+mohr_coulomb+**test_data(n_test_data=8, test_data=24元 [γ, G/Gmax, ζ]×8 退化曲线)**；TU4(基岩)纯弹性
- 土层集合按 id 直建：`gs=GFE.Pre.set.gset_basic('soil1'); gs.set_shapes_id([[3,2,9]]); gset_mgr().add(gs)`（[geo_id, 2=实体, sub_id]，soil1~9 对应 sub_id 9~1 **倒序**）+ property_solid 9 个
- Tie：search_face('Shape-1','SuperStru',0.01) 后**只取前 6 对**（tie_list=[0..5]）
- 网格：Shape-1 size=4.0(Mesh.Algorithm=6) → SuperStru size=2.0；**无地应力步**，工况直接 Initial→Dyna-1（演示简化，不做初始应力平衡）

## 集合表面（起爆点 + 迎爆面）

**S1 [官方实证v3.x]** 起爆点=**直接在网格管理器加自由节点**（原②断点解除，无须 occ vertex/参考点）：
```python
GFE.Pre.mesh.mesh_mgr().add("dp", 190.6268, -0.1791, -18.4)   # (名, x, y, z)，官方坐标真值
```
- dump GUI 版对应物 `Ref_node-1`；命令流路线根本不经"参考点"对象。

**S2 [官方实证v3.x]** 起爆点节点集（官方名 'dp'，dump GUI 版 'Node' data=[154200]）：
```python
o = GFE.Pre.set.nset(); o.name='dp'; o.data=[2]; o.unsort=False; GFE.Pre.set.nset_mgr().add(o)
```
- 坑：data 吃**网格节点号**；官方在划网格**前**add 自由节点故拿到小号 id=2——**硬编码 id 脆弱**，复刻时建点后应查实际节点号；冲击波"源点"选择器只认节点集。

**S3 [官方实证v3.x]** 迎爆面表面集：geometry_surface + 面形心 z 区间筛选：
```python
surf_mgr = GFE.Pre.surface.surf_mgr()           # 官方 ch14 用 surf_mgr()（与 surface_mgr() 双名）
obj = GFE.Pre.surface.geometry_surface('baozha_surface')
geo_obj = GFE.Pre.geometry.geo_mgr().find('SuperStru')
ids = [geotool.get_id_by_shape(f) for f in geotool.children(geo_obj.shape(), 4)
       if -20.5+1e-7 < geotool.centre_of_mass(f)[2] < -10.3-1e-7]
obj.data = [[geo_obj.id(), f[-1], 0] for f in ids]   # [geo_id, face_id, side]；官方 side=0
obj.to_node_surface = False
surf_mgr.add(obj)
```
- 官方 **side=0**（迎爆面取默认侧）——原"品红方向 side 语义"半断点部分解决（0 实证可用，其余取值仍未核）；②手册正文笔误把表面选择器写成"节点集"、"最底下俩层"实选三个集合，以操作步骤为准（c13 ②）。

## 相互作用（冲击波两件套）

**S4 [官方实证v3.x]** 冲击波属性全字段（官方名 'air_blast_prop'，dump GUI 版 'IncProp-1'）：
```python
prop = GFE.Pre.interaction.incident_wave_property()
prop.name = 'air_blast_prop'
prop.type = 0                                # 官方属性名是 type（0=AirBlast）——反推稿 def_ 作废
prop.data = [100, 1000.0, 1.0, 1.0, 1000.0]  # [TNT当量, 质量→kg, 长度→m, 时间→s, 压力→Pa]
GFE.Pre.interaction.incident_wave_property_manager().add(prop)   # 官方用全名管理器
```
- 坑：data 是**单位转换系数组**（t-m-kPa 即 1000/1/1/1000），GFE 不锁单位、填错不报错只出错结果（Cmd ②#43）。

**S5 [官方实证v3.x]** 冲击波荷载全字段：
```python
obj = GFE.Pre.interaction.incident_wave()
obj.id = 0; obj.name = 'IW-1'
obj.is_node_set = True; obj.set_name = 'dp'; obj.node_id = 0   # 源点=节点集时 node_id 置 0
obj.surf_name = 'baozha_surface'
obj.time_detonation = 0.0; obj.mag_scale_factor = 1.0
obj.prop_name = 'air_blast_prop'
GFE.Pre.interaction.iw_mgr().add(obj)
```
- 坑：构造名是 `incident_wave()`，命令流手册文档名 iw() 是笔误（Cmd ②#26）；管理器双名 iw_mgr()/incident_wave_property_manager() 官方同文件混用两风格。

## 分析步工况

**S6 [官方实证v3.x]** 显式动力步：`obj=step.dynamic_explicit_step(); obj.name='Dyna-1'; obj.nlgeom=True; obj.period=1.0`；质量缩放子对象 `ms=step.mass_scaling(); ms.region='*'; ms.type=1; ms.frequency=100; ms.target_time=5e-05; obj.mass_scaling=[ms]`（**列表**）；材料阻尼 **β=0 恒定**（官方 damping params=[2.59055, 0] 印证）。

**S7 [官方实证v3.x]** 场输出：节点 ['IWCONWEP','U','UR'] + 单元 ['DAMAGEC','DAMAGET','E','PE','S']，time_interval=0.01；`field_mgr().add(obj)`。
- 坑：**冲击波压力是节点变量 IWCONWEP**，不在单元输出（c13 ②）。

**S8 [官方实证v3.x]** 工况（v3.x 映射属性字典）：
```python
obj = GFE.Pre.case.case(); obj.name='Case-1'; obj.steps=['Initial','Dyna-1']
obj.bcs['Initial'] = ['BC-base','BC-X','BC-Y']; obj.bcs['Dyna-1'] = []
obj.initialConditions['Initial'] = []
obj.fieldReqs['Dyna-1'] = ['FieldOutput-1']; obj.histReqs['Dyna-1'] = []
obj.elemAdd['Dyna-1'] = []; obj.elemDel['Dyna-1'] = []
GFE.Pre.case.case_mgr().add(obj)
```
- 冲击波属 interaction，**不经工况挂载**、全局生效；验证只能导 INP 查（INP 关键字 `*Conwep charge property` + `*Incident wave interaction, CONWEP, property=…`，已在官方 Model-1-Case-1.inp 核实）。
- ⚠ [v2.15无此API] 映射属性字典为 v3.x；v2.15 用 set_bcs 等。

## 求解

**S9 [②]** 单元失效开关（**装机级，不在模型/GUI**）：编辑 `<安装目录>\program\config.txt`：IsRemoved_Co=1、IsRemoved2_Co=1、**手动添加** IsRemoved3_Co=1（默认无此行）。非命令流但纯文本可脚本改。**官方 T14.py 不处理 config.txt**（已核实），此步仍是人工/外部脚本职责。
- 坑：①同目录有 configout.txt 勿改错；②改完影响**该机其后所有作业**；③不改则计算中单元不失效。

**S10 [②]** 作业：命令流无 job API；官方配套 rungfe.bat 给出**命令行直跑路线**：`PrePo.exe -daemon -dat <inp路径> -gfedir <输出目录> -gpu`（绕开作业管理器 GUI）。核心 GFEXC（CPU）/GFEXG（英伟达卡）。可先 `inpio.writer(path); set_case('Case-1'); perform()` 导 INP 自检 [官方实证v3.x]。

## 后处理

**S11 [③]** GUI：过滤器"单元-集合-jiegou"→**必须点"替换"才生效**；查 DAMAGET（受拉损伤）云图，案例色标 0~5.00E-01。
- 坑：§14.10 残留"罕遇地震"字样系第11章复制残留，勿照抄进报告。

# 已知不确定项
1. ~~参考点命令流路径~~ → 官方实证 `mesh_mgr().add(name,x,y,z)` 直建自由节点（S1）；但节点号生成机制仍含混（官方硬编码 data=[2]）。
2. side 取值语义：官方实证 side=0 可用（S3），非 0 取值（"品红"反向）仍未核。
3. ~~def_ 属性名~~ → 官方实证属性名为 `type`（S4）。
4. ~~起爆点坐标真值~~ → 官方实证 (190.6268, -0.1791, -18.4)（S1）。
5. TNT 当量 100 的物理设定（100t? 等效缩放?）手册未明示，官方 py 同值照录（S4）。
6. T14.py 笔误注意：soil7 的 property_solid `name='soil'`（漏 7，elset_name='soil7' 正确）；开头 set_application_by_ui() 重复调用 2 次——照抄无害但非必要。


---
# ===== 路径_ch15_列车振动.md =====

# 路径_ch15_列车振动分析

- **case**: 实际案例操作手册v2025 第15章「列车振动分析」（v2.16.3 新增章；移动荷载动力、无地震激励；**dump=04_状态dump/ch15**；§15.11 后真值来自 P1.5 补块 PDF p400-432）
- **真值序**: **官方py v3.x（E:\GFE2026\典型案例与教程\第15章 列车振动分析案例\CM15V8.py 16912行，结构代码约千行+轨道坐标/幅值大数组，2026-06-11 比对）> dump** > 手册截图。官方 py 解掉了旧"OCR 崩坏禁当真值"项（阵列参数/扫掠层数/工字钢尺寸——见 S4/S5/S6）
- **单位制**: m-t-kPa（YJK 导入系；列车速度单独约定**米/秒**）
- **tier_summary**: **①×16 ③×1**（其中 2 项 v3.x 可达、v2.15 仍断点；S9 内含"通用最近点配对脚本须自写"半断点）

## 几何

**S1 [①官方实证v3.x；v2.15 仍断点]** YJK 导入主体结构 + gmat 土材料：
- 官方原文: `gfeio.get_current().import_yjk(yjk_path, yjk_para, ['',''], True, '', False)`——⚠ 43 元参数与 ch10/11 官方**多位不同**（第11位 400、13位 800、14位 28000、20位 10、24位 0 等），para_int 场景相关再获直证，不可跨章照抄
- `inst=GFE.io.get_current(); inst.import_mat(gmat_path)`（tu-Elastic.gmat）；rail_path=轨道.txt 同目录备 S11 用

**S2 [①官方实证v3.x]** 一维土层+快速建土：
- 官方: soil 7 层 depth=[4.72,9.5,11.5,9.5,1.9,5.1,40]，materials=['4-3','5H-2','6H','7H-A','7H-B','8H','9H']，**bedrock_mat=''（空，旧反推记 '9H' 系沿 ch10 推断——本章官方留空，无场地反应计算故不需基岩材料）**，depth_dir=2
- `box_builder().set_height(soil.depth, soil.depth_dir); set_parameter(300,300)` + data_builder（直传 soil.depth 原序——ch10 S4 仲裁注同此；旧 Cmd ②#88"自下而上"与官方抵触，以官方为准）

**S3 [①官方实证v3.x]** 平移对位+布尔裁剪：`geoprim.builder().translate(['Soil-1'], [-168.956,-184.293,-82.22], False)` + `cut('Soil-1',['BasementBoundary'],True)`

**S4 [①官方实证v3.x]** 隧道/道床/钢轨（draft+geoprim，本章新增能力）：
- 隧道断面：draft 草图（`set_snap_object/set_operate_mode/input(x,y)/select_snaped` 序列；圆+辅助线 `split_selected` 分段+`remove_selected` 删辅助）→ `set_normal([0,0,0],[0,-1,0],[1,0,0])` 设 **XZ 平面（画完再设也可——官方在 export 前才调）** → `fill_selected` → `shape=draft.export(); geo_mgr().add(mgr.auto_name('Geometry'), shape)`
- 拉伸官方 idiom：`shape_ids=[[geo_id,0,1]]; shapes=[geotool.get_shape_by_id(*id) for id in shape_ids]; extruded=geoprim.builder().extrude(shapes,[0.0,300.0,0.0]); for sp in extruded: mgr.add(mgr.auto_name('Extrude'), sp)`
- 切土工具体：Geometry-2 先 `translate([0,-5,0])` 再 extrude **310**（两端各超 5m 防贴面布尔失败——官方直证）→ `cut('Soil-1',['Extrude-2'],True)` → **删中间几何**：`mesh_mgr().delete([...]); geo_mgr().delete(['Geometry-2','Geometry-1','Extrude-2'])`（mesh 与 geo 两个管理器都要删）
- 道床：第二轮草图（圆下部直线裁断面）→ translate [81.044,-184.293,-19.97] → extrude [0,300,0] → 删 Geometry-1
- 钢轨阵列**官方实参（解 OCR 疑案）**：`shape_ids=[[9,6,17],[9,6,1]]`（道床两条棱线）→ `new_shapes=geoprim.builder().make_array(shapes, 1, 1, 2, [0.0,0.0,0.3])`（行1 列1 高2，偏移 **z=0.3 m**，旧 OCR"0,0,0,3"作废）→ auto_name('Array') 产 Array-1/2

## 材料截面

**S5 [①官方实证v3.x]** 四个截面（官方字段级直证；**拼写就是 Propery- 少个 t，官方 py 原文如此，不可纠正**）：
- `property_shell()`: name='Propery-tunnel', elset_name='Set-tunnel', mat_name='C1_Mat30', thickness=0.35, integral_point=5, layer_num=1, has_rebar=False, Ecc=[0]*4（⚠ 官方隧道用 **C1_Mat30**，旧反推记 C2_Mat30 系截图误读）
- `property_solid()`: name='Propery-daochuang', elset_name='Set-daochuang', mat_name='C2_Mat30', has_thickness=False
- `property_beam()`: name='Propery-ganggui-L', elset_name='Set-guidao-L', shape=2(工字钢), mat_name='Q345', fiber_num=1, **shape_params=[0.088,0.176,0.073,0.073,0.034,0.034,0.0165]（7 尺寸官方直证）**, direction=[1.0,0.0,0.0], **shear=[327751.0,230086.0]**, Ecc=[0]*4
- 复制改名官方 idiom：add 'Propery-ganggui-L-copy-1'（elset 仍 -L）→ `sect_mgr().rename('Propery-ganggui-L-copy-1','Propery-ganggui-R')` → 重建同名对象改 elset_name='Set-guidao-R' 后 `sect_mgr().edit(obj)`——**rename 后必须 edit 改集合，漏改全建一侧**
- 坑: 梁"方向1"须**垂直于**梁轴（钢轨沿 y 故填 (1,0,0)），用"显示线/面截面"视图人工校核

## 网格

**S6 [①官方实证v3.x]** 五域参数（官方直证；全程 auto_transfinite=True——⚠ v2.15 实测会崩勿开，版本相关）：
- SuperStru: Algorithm 8/3D 1, Recombine2D=True, size **1.0**（六面体取向）
- Soil-1: Algorithm **6**/3D **10**, Recombine2D=False, size **3.0**（三角形+HXT 四面体）
- Extrude-1 隧道: 8/1, True, size 1.0
- Extrude-2 道床: 8/1, True, size **0.6** + **扫掠官方实参（解疑案）**：`sw=mesh_generator.sweep_control(); sw.source=[9,4,9]; sw.target=[9,4,10]; sw.body=[9,2,1]; sw.dx=0; sw.dy=300.0; sw.dz=0; sw.layers=[500]; sw.ratio=[1.0]; sw.recomb_lateral=True; sw.recomb_source=True; controller.sweep_option=[sw]`（300m/500 层=0.6m 纵向；ratio 单元素 1.0=均匀）
- Array-1/2 钢轨: 8/1, True, size 0.6（**显式重配 controller 执行**，非"沿用上次"）
- 仲裁注: 官方**无线控制（line control）加密**——`PickedSet-line-1`（[3,6,83] 等 12 条边的 gset）在 SuperStru 划分后建了但后文未引用，疑为录制残留/GUI 线控制对应物；2D/3D 算法随单元形状联动勿想当然指定

## 集合

**S7 [①官方实证v3.x]** 几何集 gset_basic 官方 idiom：`gset=GFE.Pre.set.gset_basic('Set-daochuang'); gset.set_shapes_id([[geo_id, dim, tag]]); gset_mgr().add(gset)`——**dim 是 TopAbs 枚举：2=体(SOLID) 4=面(FACE) 6=线(EDGE) 7=点(VERTEX)**（Set-daochuang=[geo,2,1] 体、Set-guidao-L/R=[geo,6,1] 线、Set-tunnel=[6,4,1..4] 四面、PickedSet-liangduan1=[10/11,7,1/2] 四端点）；geo_id 用 `geo_mgr().find(name).id()` 动态取
- 节点集官方两式：
  - **Set-ganggui-L/R**：`node_data=mesh_mgr().find("Array-1").node_data(); ids=node_data[0][2:]`——**切片 [2:] 跳过前两个节点（即起止端点，留给两端固定约束）**，旧"不选起止点"GUI 语义的命令流直译；`nset=set.nset(); nset.data=ids; nset.unsort=False; nset_mgr().add(nset)`
  - **Set-daochuang-L/R**：包围盒选点 `mesh_data=target_mesh.mesh(); nodes=mesh_data.find_node_inside(lower=[80.044,-184.193,-21.97], upper=[80.045,115.607,0]); ids=[n.nid for n in nodes]`（手册 2.5.5/2.5.11 接口；左右两盒 x 各差 2m，**必须分建两个**）
- 坑: 节点集网格改变即失效，先定网格再建

## 相互作用

**S8 [①官方实证v3.x]** 局部坐标系：`o=orientation.orientation(); o.name='Orientation-1'; o.type=0; o.definition=0; o.data=[1,0,0, 0,1,0, 0,0,0]`（[p1,p2,origin] 九元）`orientation_mgr().add(o)`

**S9 [①官方实证v3.x]** 连接器行为+连接器（字段级官方直证）：
```python
b=interaction.connector_behavior(); b.name='ConnBeh-1'
e=interaction.connector_elastic(); e.component=7; e.rigid=False
e.compressive_stiffness=[39000.0]*3; e.tensile_stiffness=[]     # 抗拉留空=同抗压
d=interaction.connector_damping(); d.component=7; d.type='GFE DAMP2'; d.values=[40.0,1.0]*3
b.behaviors=[e,d]; conn_beh_mgr().add(b)
# 节点对集合（官方=GUI 自动搜索产物硬编码回放）
ns=set.nset(); ns.name='NSet-Connector-1'; ns.data=[396581,389078, 396582,389079, …]; ns.unsort=True; nset_mgr().add(ns)
cs=interaction.connector_section(); cs.name='Connector-1'; cs.set_name='NSet-Connector-1'
cs.material=''; cs.behavior='ConnBeh-1'; cs.orientation='Orientation-1'; cs.orientation2=''
cs.connector_type=(0,3)                                          # 官方为元组 (0,3)=Cartesian+Rotation
conn_prop_mgr().add(cs)
```
- ⚠ 半断点保留: NSet-Connector-1/2 官方 py 是**硬编码节点 ID 交替对**（钢轨点,道床点,…，unsort=True 保序）——换网格/换模型须自写最近点配对脚本（遍历集合2每点找集合1最近点成对排列），官方未给生成代码
- 坑: 刚度 39000/阻尼 40+指数 1 手册红字"仅供参考"；右轨复制必改集合

**S10 [①官方实证v3.x]** 搜索接触三组界面→Tie：官方逐组 `search_face` + 按 tie_list 索引建对（命名 'CP-geo1-geo2-N-master/slave'，ch11 式）：Soil-1↔SuperStru 10 对、Soil-1↔Extrude-1 4 对、Extrude-1↔Extrude-2 2 对，共 16（dump Tie-1~16 互证）；surface_pair param_number=1, parameters=[0.01]
- 坑: 钢轨↔道床**不在此列**（用连接器不用绑定，绑死丢隔振柔度）

## 边界荷载

**S11 [①官方实证v3.x]** 列车荷载——官方专门类 `GFE.Pre.boundary.train_load()`（v3.x 直证，旧通用 boundary type=9 语义在 v3.3.0+ 已被此类替代）：
```python
t=boundary.train_load(); t.name=''        # 留空→add 后自动名 TRAINLOAD / TRAINLOAD-1
t.type=9; t.is_mesh=False; t.set='Set-guidao-L'
t.begin_end=[10,1,10,2]                   # [起几何id,起点vertex,终几何id,终点vertex]——取代旧 node_id 起终点语义
t.value=[1.0, 22.22, 0.0, 0.0, 0.0,0.0,-1.0, 0.0,
         2.1,10.3,2.1,3.5, ×5 循环 …, 2.1]  # [缩放,速度m/s,起时,起位, 方向xyz, 0, 轴距序列23元]
t.track_id=[]
t.track_coord=sorted_coords_flat          # 官方给了装配脚本（见下）
t.has_if=True; t.if_mode=0                # 动轮轨力-轨道实测加速度法
t.if_acce_path=rail_path                  # 轨道.txt 绝对路径
t.if_acce=[…实测加速度大数组…]
t.if_param=[1.42, 2.55, 21.92, 5.0, 40.0, 1700.0, 275.0]
t.if_itv=0.0005; t.if_tot=0.0; t.if_grade=0; t.if_force=[]
GFE.Pre.boundary.bc_mgr().add(t)
GFE.Pre.boundary.bc_mgr().rename('TRAINLOAD','trainload-L')      # 右轨同法 rename('TRAINLOAD-1','trainload-R')
```
- **track_coord 官方装配脚本（解旧②半断点）**：`node_data=mesh_mgr().find("Array-1").node_data(); 取 (coord[1],nid,coord) 按 y 升序 sorted → 嵌套坐标平铺成 [x1,y1,z1,x2,y2,z2,…]`——轨道节点序列完全可命令流生成
- 坑: 速度**米/秒**（22.22≈80km/h）；右轨改 set='Set-guidao-R'、begin_end=[11,1,11,2]；if_param 数值红字"仅供参考"；if_acce_path 与 if_acce 并存（路径+内联双写，官方原文如此）

**S12 [①官方实证v3.x]** 轨道两端全约束：PickedSet-liangduan1 官方**命令流直建**（解旧"GUI 框选"断点）：`gset_id=[[10,7,2],[11,7,2],[10,7,1],[11,7,1]]`（两轨×两端 vertex）+ gset_basic；`bc=boundary.boundary(); bc.name='BC-liangduan'; bc.type=0; bc.set='PickedSet-liangduan1'; bc.valid_dof=0; bc.value=[0]*6; bc.is_node_set=True; bc_mgr().add(bc)`

## 人工边界 / 分析步工况

**S13 [①官方实证v3.x]** 人工边界：质心筛选通用脚本（同 ch10 S9，tolerance=1）→ 表面集名 **'arbc'** → `art_bc(); structure='SuperStru'; surface='arbc'; centered=False`（structure=SuperStru 与 dump 一致；ch11 官方用 Soil-1——字段无统一规则，见 ch10 S9 仲裁注，旧"待仲裁⑨"关闭）；**无地震场地反应**（激励是列车）

**S14 [①官方实证v3.x]** 显式动力步：`dynamic_explicit_step(); name='Dyna-1'; period=15.0; nlgeom=False; mass_scaling=[ms(type=1,frequency=100,region='*',target_time=5e-05)]`（高频车振 5e-5 与 ch10 官方动步同值）

**S15 [①官方实证v3.x]** 场输出+工况：FieldOutput-1（节点 U，time_interval=**0.01**——旧反推 0.1 作废，以官方为准）；工况名 **'case1'**（小写）：
```python
c=case.case(); c.name='case1'; c.steps=['Initial','Dyna-1']
c.bcs['Dyna-1']=['trainload-L','trainload-R','BC-liangduan']   # 列车荷载按 BC 挂（非 vload！）
c.bcs['Initial']=[]; c.initialConditions['Initial']=[]
c.artbc['Dyna-1']=['ArtBC-1']; c.fieldReqs['Dyna-1']=['FieldOutput-1']
c.histReqs['Dyna-1']=[]; c.elemAdd['Dyna-1']=[]; c.elemDel['Dyna-1']=[]
case_mgr().add(c)
```

## 求解 / 后处理

**S16 [①官方实证v3.x]** 导出：`from GFE.io import inpio; w=inpio.writer(inp_path); w.set_case('case1'); w.perform()`——**官方 v3.x 无 set_trainload2inpx 调用**，普通 INP 直出（旧反推"列车荷载须 set_trainload2inpx(True) 写 INPX"在 v3.x 官方流程中不出现；若 v2.15/旧版导出列车荷载丢失再补该开关）。作业提交无 API——GUI（GFEXC/GFEXG）

**S17 [③]** 后处理 GUI：U 云图/时程，按集合过滤

# 已知不确定项
1. ~~钢轨阵列参数、工字钢 7 尺寸、扫掠层数/比率~~——已由官方 py 直证（S4/S5/S6），旧 OCR 疑案关闭；线控制种子数仍未证（官方无线控制）。
2. NSet-Connector-1/2 通用最近点配对脚本仍需自写（官方为硬编码回放，S9）；track_coord 装配脚本已官方给出（S11）。
3. begin_end 四元的 vertex tag 语义（1=起端/2=末端）按 PickedSet-liangduan1 同源 tag 推断，未单独验证。
4. if_param 中一系悬挂 5.0/40.0 的刚度-阻尼对应顺序：手册标签辨识置信中等，官方 py 仅数组无字段名（S11）。
5. 官方 py 含录制残留（PickedSet-line-1 未引用、空 search_list 循环、if_acce_path 与 if_acce 双写）——裸重放无害但勿当必要步骤。
