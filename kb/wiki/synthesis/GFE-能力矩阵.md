# GFE 有限元自动化建模能力矩阵

> 2026-06-10 Fable 5 二审产物（自包含单文件，面向任何 LLM 直读）。
> 数据源：8 本官方手册全文精读（P1+P1.5 PDF 补块）提炼 1361 行能力 → 同名合并 1331 行 → API 自省 gfe_api_spec.txt（1607 符号）逐条裁决自动化层级。
> **三层定义**：① 命令流（PrePo 内嵌 Python API）可全自动 ② 半自动（命令流无入口但 INP/INPX 层可写、批处理 CLI、改 config.txt 或经桥可达——断点见行内）③ 纯 GUI（对话框/拾取/后处理界面专属）。
> 引用约定：出处列 = 手册缩写+§节/PDF页（Cases/Cmd/Exp/FAQ/Imp/Iso/SSA/UG）。真值仲裁序：实测 dump/自省 > 手册 > 推断。
> **版本前提（2026-06-11 更新：双代际现实）**：本矩阵①层裁决基于 v2026 手册（3.4.0）+ api_spec 自省。本机两套安装并存：**D:\GFE PrePo=v2.15 代际（2025.07，运行中）**、**E:\GFE2026=v3.x 完整安装（本机已装）**。v3.x 新 API（convert_to_davidenkov/revert_davidenkov/compute_era/build_non_uniform_soil/build_tunnel_shape/import_yjk/import_mat/find_near_node/copy_mesh/train_load 等）不再是"本机不可用"——**E:\GFE2026 可用、D:\GFE v2.15 不可用**（v2.15 缺位清单见 `_audit/phase7/实测裁决.md`；v3.x 可用性由 E:\GFE2026 官方命令流 py×13 实证，raw 快照 GFE2026-CM-*）。涉及上述 API 的①行：在 E:\GFE2026 直接可用；在 D:\GFE 须先 hasattr 实探，缺位则按②/③断点处理。另注意工况配置两形态随版本：v3.x=映射属性字典 obj.bcs['步']=[...]（可读），v2.15=8 个 set_*（只写）。

## 全局统计

| 域 | 计 | ① | ② | ③ | 未知 |
|---|---|---|---|---|---|
| D01 几何建模 | 176 | 171 | 0 | 5 | 0 |
| D02 材料与本构 | 185 | 173 | 10 | 1 | 1 |
| D03 网格 | 73 | 67 | 5 | 1 | 0 |
| D04 边界条件与荷载 | 112 | 107 | 5 | 0 | 0 |
| D05 相互作用与约束 | 117 | 115 | 2 | 0 | 0 |
| D06 分析步与求解控制 | 137 | 118 | 16 | 3 | 0 |
| D07 地震SSI与场地反应 | 93 | 64 | 3 | 23 | 3 |
| D08 人工边界与波动输入 | 26 | 25 | 1 | 0 | 0 |
| D09 IO与外部接口 | 70 | 48 | 3 | 18 | 1 |
| D10 后处理与输出 | 188 | 52 | 14 | 121 | 1 |
| D11 特殊分析 | 59 | 43 | 4 | 12 | 0 |
| D12 GUI工具与工程管理 | 95 | 49 | 4 | 39 | 3 |
| **总计** | **1331** | **1032** | **67** | **223** | **9** |

## 自动化盲区总结（LLM 驱动建模的硬边界）

- **作业提交层全线无 API**：命令流无 job/submit/solver 函数（api_spec 零命中）。统一对策：`inpio.writer` 导出 INP/INPX 自检 → `gfe -daemon -dat <INP> -gfedir <目录>`（或 PrePo.exe -daemon）CLI 提交，或 GUI/桥。作业须等 success 状态才可读结果。
- **后处理界面 119 条③**：spec 无 GFE.Post 模块。云图/动画/报告/层间位移角/轴压比等界面功能不可命令流；但输出请求类（GFE.Pre.output，场/历史/包络）是①，且 .db 为 SQLite 可脚本直读（②，FFM 提取实践已验证）。
- **GUI 助手族③**：反应位移法助手、施工助手（勾选框语义反转）、隧道设计器分段落库、二阶四面体转换、移除畸形网格对话框。复制网格 CpMsh 已脱离此族——geotool.copy_mesh ①（v3.x 官方 py 实证，v2.15 断点）。
- **存盘断点**：命令流无 save API，.pre 只能 GUI File→Save（或桥代点）。
- **D12 工程管理域无任何专属 API**（仅 set_work_path/config.txt 文件层可②）。
- 声学/热/Van-der-Waals 超弹/visco 频域等小众材料-单元族：entry_type 枚举缺位，断点=手改 INP（②）。


## D01 几何建模（176 项：①171 ②0 ③5）

| 层 | 能力 | API入口 | 断点/理由 | 出处 | 说明 | 源手册 |
|---|---|---|---|---|---|---|
| ① | 2D 草图导入三维建模 | draft.export()+geoprim.extrude |  | UG§1.3.5 | 完成的草图导入三维建模板块（三维建模—几何图元—导入草图） | GFE-UserGuide |
| ① | OCC 几何注册入文档 idiom | geo_mgr.add |  | Cmd§8.1 | sp=occ.brep_prim.make_box(...); if not sp.is_null(): mgr=geo_mgr(); mgr.add(mgr. | GFE-Cmd |
| ① | OCC 模块导入 | GFE.occ |  | Cmd§7.2 | from GFE import occ；模块定位"负责一些简单的几何建立" | GFE-Cmd |
| ① | UI 模式输入 input(u,v) | draft.input |  | Cmd§4.46 | 输入当前操作模式所需参数点；手册明示为 UI 交互设计，命令流可用其他函数 | GFE-Cmd |
| ① | draft 模块导入 | GFE.draft |  | Cmd§4.2 | from GFE import draft；不使用前处理界面即可二维建模并导入 OCC 主界面 | GFE-Cmd |
| ① | 三点添加圆弧 add_arc_points | draft.add_arc_points |  | Cmd§4.29 | 起点、中间点、终点三点定弧 | GFE-Cmd |
| ① | 三点添加圆形 add_circle_points | draft.add_circle_points |  | Cmd§4.31 | 圆周上三点定圆 | GFE-Cmd |
| ① | 几何/网格移除（右键菜单） | geo_mgr/mesh_mgr.delete |  | Cases§6.2.5 | "移除全部/移除几何/移除网格"；裁剪/拉伸后删中间几何（Geometry-1/2、Extrude-2 残留）的标准手段 | GFE-Cases |
| ① | 几何修复 | geotool.fix_selected_shape |  | UG§1.5.4 | 修复小缝隙/自相交线，线面转 B 样条；入口「通用—工具」 | GFE-UserGuide |
| ① | 几何修复 fix_selected_shape | geotool.fix_selected_shape |  | Cmd§3.4.10 | 按几何名称修复几何体 | GFE-Cmd |
| ① | 几何对象属性访问 | geometry_object |  | Cmd§2.4.2-2.4.5 | geometry_object 的 id()/name()/shape() 方法（方法调用，非属性） | GFE-Cmd |
| ① | 几何布尔分割 split | geoprim.builder.split |  | Cmd§8.2 | geoprim.builder().split(目标几何名, [工具几何名列表], True) 用面切割实体——§3.3 布尔家族（merge/common/c | GFE-Cmd |
| ① | 几何平移 translate | geoprim.translate |  | Cmd§3.3.4; SSA§3.1.3(1) | 接受 shape 列表或名称列表 + 向量；copy 默认 False | GFE-Cmd+GFE-SSA |
| ① | 几何平移（含形心提取） | - |  | UG§1.5.1(1) | 顶点/矢量两方式；可自动拾取点坐标或图元形心 | GFE-UserGuide |
| ① | 几何撤销 undo / 重做 redo | geoprim.undo/redo |  | Cmd§3.3.2-3.3.3 | 撤销/重做上一步几何操作 | GFE-Cmd |
| ① | 几何旋转 | - |  | UG§1.5.1(2) | 绕 X/Y/Z/自定义轴；选择模式锁定 Shape | GFE-UserGuide |
| ① | 几何旋转 rotate | geoprim.rotate |  | Cmd§3.3.5 | 轴位置+轴方向+角度（度）；copy 默认 False | GFE-Cmd |
| ① | 几何模块总览（4 子模块） | GFE.geometry |  | Cmd§3.1 | contact_pair 搜索接触、geoprim 布尔与基本操作、geotool 实用函数、mesh_generator 网格生成 | GFE-Cmd |
| ① | 几何缩放 | - |  | UG§1.5.1(3) | 缩放系数+缩放中心（可用质心） | GFE-UserGuide |
| ① | 几何缩放 scale | geoprim.scale |  | Cmd§3.3.6 | 双重载：纯因子缩放或指定中心点缩放 | GFE-Cmd |
| ① | 几何重命名 | - |  | Cases§2.2.1 | 树状列表右键重命名 | GFE-Cases |
| ① | 几何阵列（线性/圆） | - |  | UG§1.5.3(3) | 线性：xyz 偏移+行列高数量；圆：轴起点方向+角度+数量 | GFE-UserGuide |
| ① | 几何面集合创建（Sets） | - |  | SSA§4.1.2(a) | 选侧面建 Set-X、底面建 Set-Y 供边界条件引用 | GFE-SSA |
| ① | 分割选中的线 split_selected() | draft.split_selected |  | Cmd§4.12 | 对选中的线按交点分割 | GFE-Cmd |
| ① | 创建参考点 | - |  | UG§1.4(1) | 单独网格节点作参考点，用于刚体/MPC/耦合控制点 | GFE-UserGuide |
| ① | 创建圆柱体 | - |  | UG§1.4(5) | 底面半径+高 | GFE-UserGuide |
| ① | 创建圆柱体 make_cylinder(r,h) | occ.brep_prim.make_cylinder |  | Cmd§7.3.4 | 底面半径+高度建圆柱（该节示例误印为球体代码，见②） | GFE-Cmd |
| ① | 创建圆柱（半径+高） | - |  | Cases§1.2.1 | 参数化创建圆柱体 | GFE-Cases |
| ① | 创建圆环体 make_torus(r1,r2) | occ.brep_prim.make_torus |  | Cmd§7.3.7 | r1 主半径（中心到管道中心）、r2 管道半径 | GFE-Cmd |
| ① | 创建圆锥/圆台 | - |  | UG§1.4(7) | 底面半径+高+顶面半径（顶面半径默认 0=圆锥） | GFE-UserGuide |
| ① | 创建圆锥/圆台 make_cone(bot_r,h,top_r=0) | occ.brep_prim.make_cone |  | Cmd§7.3.3 | top_r 默认 0 为圆锥，非 0 为圆台 | GFE-Cmd |
| ① | 创建平面 | - |  | UG§1.4(3) | 多点/多边/图形外轮廓三种方式生成面 | GFE-UserGuide |
| ① | 创建折线段 | - |  | UG§1.4(2) | 输入多点坐标 | GFE-UserGuide |
| ① | 创建楔形 | - |  | Cases§1.2.1 | 七参数 Dx/Dy/Dz/xmin/xmax/zmin/zmax（倒角裁剪用） | GFE-Cases |
| ① | 创建楔形体 | - |  | UG§1.4(8) | Dx/Dy/Dz/xmin/xmax/zmin/zmax 定义 | GFE-UserGuide |
| ① | 创建楔形体 make_wedge | occ.brep_prim.make_wedge |  | Cmd§7.3.6 | make_wedge(dx,dy,dz,xmin,xmax,zmin,zmax)，截面在 dy 面由 (xmin,zmin)→(xmax,zmax) 定义，无  | GFE-Cmd |
| ① | 创建环形（圆环体） | - |  | UG§1.4(9) | 扫掠半径+截面半径 | GFE-UserGuide |
| ① | 创建球体 | - |  | UG§1.4(6) | 半径 | GFE-UserGuide |
| ① | 创建球体 make_sphere(r) | occ.brep_prim.make_sphere |  | Cmd§7.3.5 | 按半径建球 | GFE-Cmd |
| ① | 创建球体（按半径） | - |  | Cases§1.2.1 | 输入半径 R 建实心球 | GFE-Cases |
| ① | 创建立方体（两点式）make_box(pt1,pt2) | occ.make_box |  | Cmd§7.3.2 | occ.make_box([0,0,0],[1,1,1]) 两对角点建盒（同名重载，命名空间不同，见②） | GFE-Cmd |
| ① | 创建立方体（尺寸式）make_box(dx,dy,dz) | occ.brep_prim.make_box |  | Cmd§7.3.1 | occ.brep_prim.make_box(10.0,5.0,3.0)，返回 TopoDS_Shape | GFE-Cmd |
| ① | 创建表面集 | - |  | UG§1.7(2) | 几何/单元/节点三种方式；实体表面默认外表面；二维面需选颜色定正反 | GFE-UserGuide |
| ① | 创建长方体 | - |  | UG§1.4(4) | 长宽高（dx,dy,dz）或两对角点 | GFE-UserGuide |
| ① | 创建长方体/箱体 | - |  | Cases§1.2.1 | dx/dy/dz 参数或两点方式 | GFE-Cases |
| ① | 创建集合（几何/节点/单元） | - |  | UG§1.7(1) | 同类型集合不许重名；网格改变则节点/单元集失效 | GFE-UserGuide |
| ① | 包围盒包含判断 insidebox | geotool.insidebox |  | Cmd§3.4.7 | 判断形状是否在 Bnd_Box 内 | GFE-Cmd |
| ① | 包围盒对象 get_shape_box | geotool.get_shape_box |  | Cmd§3.4.6 | 返回 Bnd_Box 对象 | GFE-Cmd |
| ① | 包围盒范围 get_shape_box_range | geotool.get_shape_box_range |  | Cmd§3.4.5 | 返回 [x_min,y_min,z_min,x_max,y_max,z_max]，可 enlarge | GFE-Cmd |
| ① | 单种几何选择模式 set_snap_object(mode) | draft.set_snap_object |  | Cmd§4.5 | -1/0/1/2 = 不设置/点/线/面（单模式排他） | GFE-Cmd |
| ① | 参数化隧道建模 build_tunnel_shape | geotool.build_tunnel_shape |  | Cmd§3.4.13 | 圆形/三心圆/五心圆截面 + 反拱 + 岩带 + 3D 分段 + 沿曲线扫掠，返回 (tunnel, boundary, rockbelt) 原始 OCC 形状 | GFE-Cmd |
| ① | 参考点创建（键入坐标） | mesh_mgr().add(name,x,y,z) 参考节点 |  | Cases§14.2 | 建参考点作爆炸起爆点等 | GFE-Cases |
| ① | 取消选中 remove_selected() | draft.remove_selected |  | Cmd§4.15 | 取消选中 | GFE-Cmd |
| ① | 圆形阵列 make_round_array | geoprim.make_round_array |  | Cmd§3.3.12 | cnt 数量 + rad 旋转角（弧度）+ 中心 + 轴向 | GFE-Cmd |
| ① | 圆心一点添加圆形 add_circle_centre | draft.add_circle_centre |  | Cmd§4.32 | 圆心+圆周点（定半径）定圆 | GFE-Cmd |
| ① | 圆心两点添加圆弧 add_arc_centre | draft.add_arc_centre |  | Cmd§4.30 | 圆心+起点+终点定弧 | GFE-Cmd |
| ① | 圆锥/环形/折线段/平面等图元入口 | occ.brep_prim.make_cone/torus+create_segment/face |  | Cases§1.2.1 | 三维建模页签其余图元（未演示参数） | GFE-Cases |
| ① | 圆阵列选中对象 round_array_selected | draft.round_array_selected |  | Cmd§4.14 | round_array_selected(cnt, rad, centre_u, centre_v)，rad 标注为整型阵列角度 | GFE-Cmd |
| ① | 圆阵列（旋转复制） | - |  | Cases§1.2.1 | "数量 角度"+"轴起点 轴方向"，θ 顺时针、N 含原件 | GFE-Cases |
| ① | 土体布尔裁剪（修订记录线索） | geoprim.builder.cut |  | FAQ修订记录 | 指向 §2.3，仅作能力线索不计入能力总数 | GFE-FAQ |
| ① | 填充选中对象 fill_selected() | draft.fill_selected |  | Cmd§4.11 | 填充选中对象（成面） | GFE-Cmd |
| ① | 复合几何体 make_compound | geotool.make_compound |  | Cmd§3.4.4 | 组合多形状；copy 默认 False（引用原形状） | GFE-Cmd |
| ① | 多段线创建 create_segment | geotool.create_segment |  | Cmd§3.4.11 | 点坐标列表（≥2 点）建多段线，可自动命名 | GFE-Cmd |
| ① | 多种几何选择模式 set_snap_object(list) | draft.set_snap_object |  | Cmd§4.6 | 3 元 0/1 列表 [点,线,面] 各自开关（同名重载） | GFE-Cmd |
| ① | 子几何体遍历 children / children(shape,type) | geotool.children |  | Cmd§3.4.2-3.4.3 | 按 TopAbs_ShapeEnum（COMPOUND=0…VERTEX=7, SHAPE=8）过滤子形状 | GFE-Cmd |
| ① | 完成草图 | - |  | Cases§2.2.1 | 提交草图为三维界面的 Geometry-N 对象 | GFE-Cases |
| ① | 布尔-其他类型入口（替换/相交/增加/对称差/移除） | builder merge/common/cut/split 可组合等效 |  | Cases§1.2.1 | 列出未演示 | GFE-Cases |
| ① | 布尔-分割（印刻） | - |  | Cases§6.4.4 | 把工具体形状印刻进被分割体，保证共节点界面 | GFE-Cases |
| ① | 布尔-取交 | - |  | Cases§6.2.1; UG§1.5.2(3) | 生成交集新几何（如被挖土体） | GFE-Cases+GFE-UserGuide |
| ① | 布尔-合并 | - |  | Cases§1.2.1; UG§1.5.2(1) | ≥2 图形合并，支持跨维度（低维完全在高维内时效果同切割） | GFE-Cases+GFE-UserGuide |
| ① | 布尔-裁剪 | - |  | Cases§1.2.1; UG§1.5.2(2) | 工具体切除被裁体重叠体积；可勾"替换原始图形" | GFE-Cases+GFE-UserGuide |
| ① | 布尔分割 | - |  | UG§1.5.2(4) | ≥2 图形互相分割 | GFE-UserGuide |
| ① | 布尔合并 merge | geoprim.merge |  | Cmd§3.3.7 | replace_set 替换原集合（限点/线/面/实体） | GFE-Cmd |
| ① | 布尔求交 common | geoprim.common |  | Cmd§3.3.8 | 多几何体交集 | GFE-Cmd |
| ① | 布尔求差 cut | geoprim.cut |  | Cmd§3.3.9 | 被减体 − 减体列表；remove_origin 默认 False；小节标题误写为「求交操作」 | GFE-Cmd |
| ① | 布尔裁剪（Boolean Operation→Cut） | builder.cut |  | SSA§3.1.3(2)/§6.1 | 2D 选土体为对象、面实体为工具；3D 可直接用导入 ydb 时生成的外轮廓实体，无需额外建几何体 | GFE-SSA |
| ① | 布尔裁剪（含"替换原图形"选项） | cut(remove_origin=True) |  | FAQ§2.1-2.3 | 土体与地下室箱体布尔裁剪；勾"替换原图形"才继承截面属性 | GFE-FAQ |
| ① | 平移-矢量方式 | - |  | Cases§1.2.1 | 输入 (dx,dy,dz) 平移；操作方式可选复制/移动 | GFE-Cases |
| ① | 平移-顶点/形心拾取方式 | builder.translate+geotool.centre_of_mass 等效 |  | Cases§1.2.1 | 拾取起/终点（可自动回填面形心坐标）做对位平移 | GFE-Cases |
| ① | 平移选中（两点向量法）translate_selected(begin,end,copy) | draft.translate_selected |  | Cmd§4.33 | 以 end-begin 为平移向量，copy 默认 False | GFE-Cmd |
| ① | 平移选中（直接向量法）translate_selected(vector,copy) | draft.translate_selected |  | Cmd§4.34 | 直接给 [dx,dy]（同名重载） | GFE-Cmd |
| ① | 拉伸 extrude | geoprim.extrude |  | Cmd§3.3.10 | 沿向量拉伸（面→体等） | GFE-Cmd |
| ① | 拉伸建模 | - |  | UG§1.5.3(1) | 点→线、线→面、面→体（体不可拉伸） | GFE-UserGuide |
| ① | 拉伸建模（面→体 / 线→壳 / 点→线柱） | - |  | Cases§2.2.1 | 选对象+矢量拉伸；输入对象可为点（直接拉出立柱线） | GFE-Cases |
| ① | 按 ID 取形状 get_shape_by_id | geotool.get_shape_by_id |  | Cmd§3.4.16 | pid+类型+索引（从 1 开始）定位形状 | GFE-Cmd |
| ① | 捕获区域内对象 snap_object(u_min,u_mau,v_min,v_mau) | draft.snap_object |  | Cmd§4.7 | 对角点构造矩形捕获区域 | GFE-Cmd |
| ① | 撤销 undo() / 恢复 redo() | draft.undo/redo |  | Cmd§4.17-4.18 | redo 每次恢复一个操作、可恢复多次 | GFE-Cmd |
| ① | 旋转 | - |  | Cases§1.2.1 | 绕轴旋转几何 | GFE-Cases |
| ① | 旋转建模 | - |  | UG§1.5.3(2) | 低维图形绕轴旋转升维（体不可） | GFE-UserGuide |
| ① | 旋转建模（Revolve） | - |  | Cases§1.2.1 | 草图线绕轴旋转成体（树节点 Revolve-N） | GFE-Cases |
| ① | 旋转选中 rotate_selected(centre,angle,copy) | draft.rotate_selected |  | Cmd§4.35 | 指定中心旋转指定角度（单位：度） | GFE-Cmd |
| ① | 框选点几何 select_point(u_min,u_mau,v_min,v_mau,replace) | draft.select_point |  | Cmd§4.20 | 区域内选点（同名重载） | GFE-Cmd |
| ① | 框选线几何 select_line(u_min,u_max,v_min,v_max,replace) | draft.select_line |  | Cmd§4.22 | uv 矩形区域选线（同名重载） | GFE-Cmd |
| ① | 框选面几何 select_face(umin,umax,vmin,vmax,replace) | draft.select_face |  | Cmd§4.24 | uv 矩形区域选面（同名重载） | GFE-Cmd |
| ① | 梁/壳/实体混合三维建模 | geoprim+section 全链 API |  | SSA§6.2 | 土体一阶四面体实体单元（3m），楼板侧墙壳单元、梁柱梁单元（1.0m） | GFE-SSA |
| ① | 添加多段线 add_polyline(points_list) | draft.add_polyline |  | Cmd§4.27 | 连续坐标点添加多段线（首尾不闭合） | GFE-Cmd |
| ① | 添加点 add_point(point) | draft.add_point |  | Cmd§4.25 | 指定二维位置添加点几何，点为 [x,y] 或 (x,y) | GFE-Cmd |
| ① | 添加矩形 add_rectangle(corner1, corner2) | draft.add_rectangle |  | Cmd§4.28 | 两对角点添加矩形（边与坐标轴平行） | GFE-Cmd |
| ① | 添加线 add_line(start_point, end_point) | draft.add_line |  | Cmd§4.26 | 起终点坐标添加直线 | GFE-Cmd |
| ① | 清除草图 clear() | draft.clear |  | Cmd§4.16 | 清除当前绘制的草图 | GFE-Cmd |
| ① | 点选捕获对象 snap_object(u,v) | draft.snap_object |  | Cmd§4.8 | 按坐标点选对象（同名重载） | GFE-Cmd |
| ① | 点选点几何 select_point(u,v,replace) | draft.select_point |  | Cmd§4.19 | 选择点 (u,v) 附近的点 | GFE-Cmd |
| ① | 点选线几何 select_line(u,v,replace) | draft.select_line |  | Cmd§4.21 | 选择点附近的线，replace 默认 True | GFE-Cmd |
| ① | 点选面几何 select_face(u,v,replace) | draft.select_face |  | Cmd§4.23 | 选择点附近的面 | GFE-Cmd |
| ① | 生成面 create_face | geotool.create_face |  | Cmd§3.4.9 | type 0=点成面 1=线成面 2=形状成面 | GFE-Cmd |
| ① | 由结构外轮廓创建面实体 | geotool.create_face(type 0/1/2) |  | SSA§3.1.3(2) | 根据结构外轮廓边创建面实体作为布尔裁剪工具（2D 流程必需） | GFE-SSA |
| ① | 矩形阵列 make_array | geoprim.make_array |  | Cmd§3.3.11 | 行×列×层 + 偏移向量 | GFE-Cmd |
| ① | 矩形阵列（行/列/高+xyz偏移） | - |  | Cases§2.2.1 | 线性阵列复制楼层/内支撑/钢轨等（钢轨=选道床体上的线阵列生成） | GFE-Cases |
| ① | 约束垂直 constrain_selected_vertical() | draft.constrain_selected_vertical |  | Cmd§4.40 | 选中直线约束为平行 Y 轴，无参 | GFE-Cmd |
| ① | 约束垂直关系 constrain_selected_perpendicular(set_ref) | draft.constrain_selected_perpendicular |  | Cmd§4.43 | 两步协议同上 | GFE-Cmd |
| ① | 约束平行 constrain_selected_parallel(set_ref) | draft.constrain_selected_parallel |  | Cmd§4.42 | 两步协议：True 设参考线，False 约束与参考线平行 | GFE-Cmd |
| ① | 约束水平 constrain_selected_horizontal() | draft.constrain_selected_horizontal |  | Cmd§4.39 | 选中直线约束为平行 X 轴，无参 | GFE-Cmd |
| ① | 约束相切 constrain_selected_tangent(set_ref) | draft.constrain_selected_tangent |  | Cmd§4.44 | True 设参考圆弧，False 约束选中线与之相切 | GFE-Cmd |
| ① | 约束长度 constrain_selected_length(length) | draft.constrain_selected_length |  | Cmd§4.41 | 约束选中直线长度（需 >0） | GFE-Cmd |
| ① | 缩放选中 scale_selected(centre,factor,copy) | draft.scale_selected |  | Cmd§4.36 | >1 放大，0<factor<1 缩小，负数反转 | GFE-Cmd |
| ① | 缩放（入口） | builder.scale |  | Cases§1.2.1 | 未演示参数 | GFE-Cases |
| ① | 自动创建集合 | - |  | UG§1.18.6 | 按形心坐标自动分组或参考值区间分组批量建集合 | GFE-UserGuide |
| ① | 节点集合创建 | - |  | SSA§5.1.2(b) | 结构划分网格后在节点上建节点集，供弹簧施加 | GFE-SSA |
| ① | 草图-分段（线条互切） | draft.split_selected |  | Cases§15.8.1 | 框选线条点"分段"在交点互切（圆切 4 段利于剖网格） | GFE-Cases |
| ① | 草图-删除线/面 | - |  | Cases§2.2.1 | 删多余线段、拉伸后的草图遗留面 | GFE-Cases |
| ① | 草图-圆 | - |  | Cases§3.1.2 | 圆心+圆上一点定半径（亦可指定半径，如道床基圆 3m）；左键长按切换画圆方式 | GFE-Cases |
| ① | 草图-圆弧 | draft.add_arc_points/centre |  | Cases§4.2.1 | 三点/圆心法画弧，系统默认逆时针 | GFE-Cases |
| ① | 草图-填充区域 | - |  | Cases§2.2.1 | 框选闭合线框生成面域（失败报 "Failed to fill area"） | GFE-Cases |
| ① | 草图-多段折线 | draft.add_polyline |  | Cases§4.2.1 | 逐点输坐标连续画折线 | GFE-Cases |
| ① | 草图-清空 | - |  | Cases§3.1.2; UG§1.3.4(14) | 一键删除草图工作区全部元素 | GFE-Cases+GFE-UserGuide |
| ① | 草图-直线 | - |  | Cases§2.2.1 | 两点坐标画线（坐标可命令行输入） | GFE-Cases |
| ① | 草图-矩形 | - |  | Cases§2.2.1 | 两角点坐标画矩形 | GFE-Cases |
| ① | 草图-选择面/线编辑复用 | draft.select_face/select_line |  | Cases§4.2.1 | 在旧草图上删改线段改出新层墙线 | GFE-Cases |
| ① | 草图-阵列 | - |  | Cases§3.1.2 | 行/列数+偏移量复制草图图元 | GFE-Cases |
| ① | 草图中心对称（复制/移动两模式） | draft.mirror_selected(point,copy) |  | UG§1.3.4(4) | 选对象→对称中心→执行 | GFE-UserGuide |
| ① | 草图分段 | draft.split_selected |  | UG§1.3.4(7) | 整体连续图形截断为若干部分 | GFE-UserGuide |
| ① | 草图创建圆弧（三点/圆心两方式） | add_arc_points/add_arc_centre |  | UG§1.3.3(5) | 长按图标切换方式 | GFE-UserGuide |
| ① | 草图创建圆（三点/圆心两方式） | add_circle_points/add_circle_centre |  | UG§1.3.3(6) | 三点式或圆心+圆上一点式 | GFE-UserGuide |
| ① | 草图创建多段折线 | draft.add_polyline |  | UG§1.3.3(3) | 多次"下一步"输入关键点，右键结束 | GFE-UserGuide |
| ① | 草图创建点 | draft.add_point |  | UG§1.3.3(1) | 拾取或输入 X,Y 坐标创建点 | GFE-UserGuide |
| ① | 草图创建直线 | draft.add_line |  | UG§1.3.3(2) | 拾取/输入起终点坐标 | GFE-UserGuide |
| ① | 草图创建矩形 | draft.add_rectangle |  | UG§1.3.3(4) | 对角两点定义 | GFE-UserGuide |
| ① | 草图删除/撤销/重做 | remove_selected/undo/redo |  | UG§1.3.4(15)(16)(17) | 选中删除；撤销/重做最近操作 | GFE-UserGuide |
| ① | 草图圆阵列 | draft.round_array_selected |  | UG§1.3.4(5) | 旋转轴起点与方向 + 角度 + 数量环形阵列 | GFE-UserGuide |
| ① | 草图垂直约束 | constrain_selected_perpendicular |  | UG§1.3.4(12) | 多线段与参考线段垂直 | GFE-UserGuide |
| ① | 草图填充区域（封闭线围面） | draft.fill_selected |  | UG§1.3.4(6) | 选封闭线段（Shift 框选）填充成面 | GFE-UserGuide |
| ① | 草图导出形状 export() | draft.export |  | Cmd§4.45 | 当前草图内容形成 OCC 形状并返回（draft→3D 的桥） | GFE-Cmd |
| ① | 草图平移（复制/移动两模式） | translate_selected(copy) |  | UG§1.3.4(1) | HintBar 流程：选方式→选对象→向量起终点→执行 | GFE-UserGuide |
| ① | 草图平行约束 | constrain_selected_parallel |  | UG§1.3.4(11) | 多线段与参考线段平行 | GFE-UserGuide |
| ① | 草图平面/栅格设置 | draft.set_normal(栅格仅显示辅助) |  | Cases§2.2.1 | 画前选 XY/XZ/YZ 平面（可反向、偏移），设栅格长度/间隔；偏移决定草图落位 | GFE-Cases |
| ① | 草图旋转（复制/移动两模式） | rotate_selected(copy) |  | UG§1.3.4(2) | 选对象→旋转中心→角度→执行 | GFE-UserGuide |
| ① | 草图水平约束 | constrain_selected_horizontal |  | UG§1.3.4(8) | 任意方向线段调整为水平 | GFE-UserGuide |
| ① | 草图相切约束 | constrain_selected_tangent |  | UG§1.3.4(13) | 线段与参考圆/圆弧相切 | GFE-UserGuide |
| ① | 草图竖直约束 | constrain_selected_vertical |  | UG§1.3.4(9) | 任意方向线段调整为竖直 | GFE-UserGuide |
| ① | 草图线性阵列 | draft.array_selected |  | UG§1.3.4(5) | 行列数 + x,y 方向偏移量 | GFE-UserGuide |
| ① | 草图缩放（复制/移动两模式） | scale_selected(copy) |  | UG§1.3.4(3) | 选对象→缩放中心→缩放因子→执行 | GFE-UserGuide |
| ① | 草图设置（工作平面/偏移/反向/栅格） | set_normal 双重载定平面/偏移/方向 |  | UG§1.3.1 | 工作平面 XY/XZ/YZ、法向偏移、栅格长度与间隔 | GFE-UserGuide |
| ① | 草图长度约束 | constrain_selected_length |  | UG§1.3.4(10) | 线段约束为固定长度（HintBar 输入约束值） | GFE-UserGuide |
| ① | 获取几何构建器 builder() | geoprim.builder |  | Cmd§3.3.1 | GFE.geometry.geoprim.builder() 取当前文档构建器 | GFE-Cmd |
| ① | 获取几何管理器（单例） | geometry.geo_mgr |  | Cmd§2.4.1 | geo_mgr()，本模块几乎所有函数的入口 | GFE-Cmd |
| ① | 获得当前绘制界面 get_current() | draft.get_current |  | Cmd§4.3 | GFE.draft.get_current()，后续所有 draft 操作的入口 | GFE-Cmd |
| ① | 表面集创建（Surfaces） | geometry/element/node_surface+surf_mgr |  | SSA§3.1.7 | 选土体外边缘建立表面，作为人工边界载体 | GFE-SSA |
| ① | 设置变换模式 set_copy_transform(f) | draft.set_copy_transform |  | Cmd§4.48 | 设置是否平移复制，UI 交互用 | GFE-Cmd |
| ① | 设置捕获容差 set_snap_tolerance(tol) | draft.set_snap_tolerance |  | Cmd§4.9 | 浮点容差 | GFE-Cmd |
| ① | 设置操作模式 set_operate_mode(mode) | draft.set_operate_mode |  | Cmd§4.4 | 枚举 -1~23：点/线/多段折线/矩形/弧/圆/平移/对称/旋转/缩放/填充/阵列/拉伸/回转/几何约束等；-1=结束当前模式 | GFE-Cmd |
| ① | 质心计算 centre_of_mass | geotool.centre_of_mass |  | Cmd§3.4.1 | 返回 [x,y,z] | GFE-Cmd |
| ① | 选中几何输入 input_selected() | draft.input_selected |  | Cmd§4.47 | 选择模式后将所选几何"输入"，用于平移/缩放/中心对称/旋转 | GFE-Cmd |
| ① | 选中捕获的对象 select_snaped(add) | draft.select_snaped |  | Cmd§4.10 | add=True 追加到已选，False 替换已选（手册示例传 1e-2 与布尔签名矛盾，见②） | GFE-Cmd |
| ① | 通用扫掠 general_sweep_by_shapes | geotool.general_sweep_by_shapes |  | Cmd§3.4.23 | (path_shape, face_shape, is_solid) 面外轮廓/线框沿路径扫掠成壳/实体，返回 (success, res) 元组，失败 res | GFE-Cmd |
| ① | 镜像选中（点对称）mirror_selected(sym_point,copy) | draft.mirror_selected |  | Cmd§4.37 | 指定点为对称中心 | GFE-Cmd |
| ① | 镜像选中（轴对称）mirror_selected(point1,point2,copy) | draft.mirror_selected |  | Cmd§4.38 | 两点确定对称轴（同名重载） | GFE-Cmd |
| ① | 阵列选中对象 array_selected | draft.array_selected |  | Cmd§4.13 | array_selected(row, col, offset_u, offset_v) 矩形阵列（示例无参调用为笔误，见②） | GFE-Cmd |
| ① | 隧道设计器 | geotool.build_tunnel_shape 参数化隧道 |  | Cases§7.2.5 | 3 心圆断面（R1/R2/A1/A2/仰拱）+锚杆自动布置+3D 扫掠分段（含每分析步分段数施工选项）；参数可存/导 | GFE-Cases |
| ① | 隧道设计器—3D | - |  | UG§1.18.5(3) | 矢量拉伸或曲线扫掠；间距支持循环数列；勾"施工"自动建分析步+工况 | GFE-UserGuide |
| ① | 隧道设计器—锚杆 | - |  | UG§1.18.5(2) | 数量/长度/弧长/偏移；可独立成体或与隧道同体 | GFE-UserGuide |
| ① | 隧道设计器—隧道截面 | - |  | UG§1.18.5(1) | 圆/3心圆/5心圆；2D 配梁、3D 配壳；可保存/导入 | GFE-UserGuide |
| ③ | 光标吸附—栅格 | - |  | UG§1.3.2(2) | 鼠标靠近栅格点自动吸附 | GFE-UserGuide |
| ③ | 光标吸附—线段中点 | - |  | UG§1.3.2(5) | 鼠标靠近线段中点自动吸附 | GFE-UserGuide |
| ③ | 光标吸附—邻近几何 | - |  | UG§1.3.2(3) | 鼠标靠近已有几何自动吸附 | GFE-UserGuide |
| ③ | 光标吸附—邻近点 | - |  | UG§1.3.2(4) | 鼠标靠近已有点自动吸附 | GFE-UserGuide |
| ③ | 草图对象选择（点/线/面） | - |  | UG§1.3.2(1) | 草图模式下选择顶点/直线曲线/封闭面 | GFE-UserGuide |

## D02 材料与本构（185 项：①173 ②10 ③1 未知1）

| 层 | 能力 | API入口 | 断点/理由 | 出处 | 说明 | 源手册 |
|---|---|---|---|---|---|---|
| ① | *Beam Section | - |  | UG附录二(3) p288 | 梁截面，Elset/Material/Section(如 RECT、CIRC) 必要 | GFE-UserGuide |
| ① | *Concrete Compression Damage | - |  | UG附录二(2) p280 | CDP 压缩损伤曲线，tension recovery 默认 0 | GFE-UserGuide |
| ① | *Concrete Compression Hardening | - |  | UG附录二(2) p279-280 | CDP 压缩硬化曲线，多行：屈服应力,非弹性应变 | GFE-UserGuide |
| ① | *Concrete Damage Plasticity | - |  | UG附录二(2) p279 | CDP 混凝土塑性损伤，单行 5 个公式参数（第 4 位未用） | GFE-UserGuide |
| ① | *Concrete Tension Damage | - |  | UG附录二(2) p280-281 | CDP 拉伸损伤曲线，compression recovery 默认 1 | GFE-UserGuide |
| ① | *Concrete Tension Stiffening | - |  | UG附录二(2) p280 | CDP 拉伸刚度曲线，多行：屈服应力,开裂应变 | GFE-UserGuide |
| ① | *Creep | material.creep(构造名crep()) |  | UG附录二(2) p281 | 蠕变，仅 law=strain, time=creep，数据行只读前三个数 | GFE-UserGuide |
| ① | *Damping | - |  | UG附录二(2) p277-278 | 材料级 Rayleigh 阻尼，alpha/beta 两参数 | GFE-UserGuide |
| ① | *Density | - |  | UG附录二(2) p277 | 密度，仅支持均匀密度，不可单独使用 | GFE-UserGuide |
| ① | *Elastic | - |  | UG附录二(2) p278 | 弹性参数，type=isotropic(缺省)/lamina，moduli 缺省=long term | GFE-UserGuide |
| ① | *Expansion | material.expansion |  | UG附录二(2) p287 | 热膨胀系数，单行一个数 | GFE-UserGuide |
| ① | *HyperElastic | material.hyperelastic he_type 0-7 |  | UG附录二(2) p281-282 | 超弹本构，9 种互斥计算模型（marlow/mooney-rivlin/ogden/yeoh/polynomial/reduced polynomial/arr | GFE-UserGuide |
| ① | *HyperFoam | material.hyperfoam |  | UG附录二(2) p282-283 | 泡棉材料，N 有效范围 1–6（缺省 1），公式参数个数 N*3 | GFE-UserGuide |
| ① | *Material | - |  | UG附录二(2) p277 | 材料容器，name 必要；必要子关键字 *Density + 一种互斥本构 | GFE-UserGuide |
| ① | *Membrane Section | - |  | UG附录二(3) p288 | 膜截面，elset/material 必要 | GFE-UserGuide |
| ① | *Mohr Coulomb | - |  | UG附录二(2) p279 | 摩尔库伦，数据行仅支持前两位，必要同级 *Elastic | GFE-UserGuide |
| ① | *Mohr Coulomb Hardening | mohr_coulomb.plasticity 多行硬化 |  | UG附录二(2) p279 | MC 硬化，归属 *Mohr Coulomb，数据行仅支持前两位 | GFE-UserGuide |
| ① | *Permeability | material.mat_permeability(entry_type含) |  | UG附录二(2) p287 | 渗透性，仅孔压单元+隐式计算，type 仅 isotropic | GFE-UserGuide |
| ① | *Plastic | - |  | UG附录二(2) p278 | 塑性，hardening=isotropic(缺省)/Johnson Cook，可选 rate | GFE-UserGuide |
| ① | *Porous Bulk Moduli | material.porous_bulk_moduli |  | UG附录二(2) p287 | 孔隙体积模量，仅孔压单元+隐式计算 | GFE-UserGuide |
| ① | *Rate Dependent | material.rate_dependent |  | UG附录二(2) p279 | 率相关，type 仅支持 Johnson Cook，归属 *Plastic | GFE-UserGuide |
| ① | *Rebar Layer | - |  | UG附录二(3) p289 | 钢筋层，归属 *Shell Section/*Membrane Section，可选 orientation | GFE-UserGuide |
| ① | *Section Controls | - |  | UG附录二(3) p289 | 截面控制，GFE 计算 INP 必须含 Name=ENG, Hourglass=ENHANCED，GFE 写出 INP 自动创建并引用 | GFE-UserGuide |
| ① | *Shell Section | - |  | UG附录二(3) p288 | 壳截面，elset/material/control 必要，仅均质截面 | GFE-UserGuide |
| ① | *Solid Section | - |  | UG附录二(3) p289 | 实体截面，elset/material/control 必要 | GFE-UserGuide |
| ① | *Transverse Shear Stiffness | property_beam.shear |  | UG附录二(3) p288 | 剪切刚度，归属上方最近 *Beam Section | GFE-UserGuide |
| ① | *Uniaxial Test Data（及 Biaxial/Planar/Volumetric） | hyperelastic.uniaxial/biaxial/planar/volumetric |  | UG附录二(2) p282 | 超弹/泡棉试验数据输入，多行每行两个数，四种格式相同 | GFE-UserGuide |
| ① | *User Material | - |  | UG附录二(2) p283-287 | GFE 内置自定义材料，数据行第一位为本构标识位（1–8 共 8 种），constants 与数据行参数个数一致 | GFE-UserGuide |
| ① | *ViscoElastic | material.viscoelastic(Prony) |  | UG附录二(2) p283 | 粘弹性，time 仅 prony；frequency 仅隐式计算支持 tabular | GFE-UserGuide |
| ① | Arruda-Boyce 超弹 | - |  | Imp§2.2.7 | μ/λm/D 三参数 8 链模型 | GFE-Implicit |
| ① | CDP 循环/复合加载验证（往复位移、压剪-拉剪） | - |  | Explicit§2.4.2.4 | 幅值曲线 0→1→-1 × 比例系数实现拉压滞回与双向循环 | GFE-Explicit |
| ① | CDP 率效应三选项 | material.concrete_damaged |  | Cmd§2.6.6 | rate_type：0 无 / 1 Johnson-Cook / 2 CEB 规范率效应 | GFE-Cmd |
| ① | Davidenkov | - |  | UG§1.8.6a | A、B、γ0；可选液化参数组；仅显式动力+三维实体 | GFE-UserGuide |
| ① | Davidenkov 土体本构 | - |  | SSA§1.1.5/表2.2-2/§6.3 | 可考虑土体动力特性的 Davidenkov 模型（参数 A、B、γ0） | GFE-SSA |
| ① | Davidenkov 本构（3D C3D8R + 2D CPE4R） | - |  | Explicit§2.5.1 | 参数 A/B/γ0；2D 验证基准是自家 C3D8R；平面应变/实体；仅显式动力 | GFE-Explicit |
| ① | Davidenkov 液化本构（孔压耦合有效应力法） | user(user_type=2) 12参数液化 |  | Explicit§2.6 | Martin-Byrne-陈国兴孔压增量模型，刚度随孔压累积衰退；无第三方对标 | GFE-Explicit |
| ① | E-B 本构 | - |  | UG§1.8.6h | c、φ0、Δφ0、Rf、K、n、Kb、m | GFE-UserGuide |
| ① | E-v 本构 | - |  | UG§1.8.6g | c、φ0、Δφ0、Rf、K、n、Kur、G、F、D | GFE-UserGuide |
| ① | HSS 小应变模型 | - |  | UG§1.8.6e | γ0.7、m、G0ref、Eur_ref、pref、νur、σL；继承摩尔库伦 | GFE-UserGuide |
| ① | HSS 小应变硬化土本构 | user(user_type=3),需配Mohr Coulomb |  | Explicit§2.11; Imp§2.4 | G0ref/γ0.7/m/pref/Eur/μur/c/φ/ψ 等，与软件 Z（PLAXIS 类）对比 | GFE-Explicit+GFE-Implicit |
| ① | Hyperelastic：Arruda-Boyce | hyperelastic he_type=6 |  | Explicit§2.7.6 | μ/λm/D 三参数 | GFE-Explicit |
| ① | Hyperelastic：Mooney-Rivlin | hyperelastic he_type=0 |  | Explicit§2.7.1 | C10/C01/D1，C3D4 大变形剪切验证 | GFE-Explicit |
| ① | Hyperelastic：Neo-Hooke | hyperelastic he_type=7 |  | Explicit§2.7.7 | C10/D1 两参数（手册公式印刷错误，以参数表为准） | GFE-Explicit |
| ① | Hyperelastic：Ogden（多阶 N≥2） | he_type=1+N属性 |  | Explicit§2.7.2 | μi/αi/Di 按阶次输入 | GFE-Explicit |
| ① | Hyperelastic：Polynomial | hyperelastic he_type=3 |  | Explicit§2.7.4 | Cij/Di 多项式形式（算例 D1=100 量级存疑） | GFE-Explicit |
| ① | Hyperelastic：Reduced Polynomial | hyperelastic he_type=5 |  | Explicit§2.7.5 | Ci0/Di，N=2 验证 | GFE-Explicit |
| ① | Hyperelastic：Yeoh | hyperelastic he_type=2 |  | Explicit§2.7.3 | C10/C20/C30/D1/D2/D3 | GFE-Explicit |
| ① | Hyperfoam 本构（可压缩泡沫超弹，μi/αi/νi 多阶） | - |  | Explicit§2.8.1-2.8.2 | C3D4 大变形剪切（500% 名义剪应变）验证 | GFE-Explicit |
| ① | Hyperfoam（可压缩泡沫超弹） | - |  | Imp§2.2.3/§1.1.5.2 | 阶次+μ/α/ν 参数化，支持测试数据输入 | GFE-Implicit |
| ① | JH-2 本构 | - |  | UG§1.8.6f | 陶瓷/玻璃硬脆材料，20+ 参数；仅显式动力 | GFE-UserGuide |
| ① | Johnson-Cook 率效应 | material.plastic |  | Cmd§2.6.5 | has_jc_rate + jc_rate_C + jc_rate_Ep0_dot1 | GFE-Cmd |
| ① | Marlow 超弹本构 | hyperelastic he_type=4 |  | Imp§2.2.2 | 不输 Cij：Poisson+MODULI(INSTANTANEOUS)+名义应力-应变曲线 | GFE-Implicit |
| ① | Mohr Coloumb 弹塑性本构 | - |  | Imp§2.1.2 | 参数 E、ν、摩擦角、黏聚力 | GFE-Implicit |
| ① | Mohr-Coulomb 土体本构 | - |  | SSA§1.1.5/表2.2-3/§6.3 | 经典摩尔库伦模型（2D/3D 非线性时程均用） | GFE-SSA |
| ① | Mooney-Rivlin 超弹（C10/C01/D1 直接参数） | - |  | Imp§2.2.1 | 二参数超弹静力验证 | GFE-Implicit |
| ① | Neo-Hooke 超弹 | - |  | Imp§2.2.8 | C10/D1 两参数（手册印刷公式异常，见②） | GFE-Implicit |
| ① | Polynomial 多项式超弹（1/2 阶） | - |  | Imp§2.2.4/§3.4.2表3.4.2-1 | C10/C01/C11/C20/C02 + D1/D2 应变势能 | GFE-Implicit |
| ① | Rayleigh 阻尼（α/β） | - |  | Cases§7.2.1 | 常规类下添加阻尼两系数 | GFE-Cases |
| ① | Reduced Polynomial 缩减多项式超弹（2 阶） | - |  | Imp§2.2.5 | C10/C20/D1/D2 | GFE-Implicit |
| ① | SoilLayerProp-N 自动生成 | soil.data_builder 自动建属性集合 |  | Cases§6.4.2 | 快速建土后自动按土层生成分层截面属性 | GFE-Cases |
| ① | Uniaxial Test Data 方式输入超弹/泡沫材料 | hyperelastic/hyperfoam test_data 属性 |  | Explicit§2.7.1.2 | 输入单轴试验数据，GFE 预处理阶段自动拟合转换为材料参数；仅此三处明文支持 | GFE-Explicit |
| ① | UserMat 1：一维非线性混凝土 | - |  | UG附录二(2) p283-284 | 7 参数，支持 Johnson Cook 率效应 | GFE-UserGuide |
| ① | UserMat 2：Davidenkov / 液化 Davidenkov | - |  | UG附录二(2) p284 | 岩土类，6 参数 / 12 参数 | GFE-UserGuide |
| ① | UserMat 3：HSS | - |  | UG附录二(2) p284 | 岩土类，7 参数，前面必须有 *Mohr Coulomb | GFE-UserGuide |
| ① | UserMat 4：南水本构 | - |  | UG附录二(2) p285 | 岩土类，11 参数（见⑤待仲裁#1） | GFE-UserGuide |
| ① | UserMat 5：考虑屈曲的钢筋滞回 | - |  | UG附录二(2) p285 | 5 参数（Es, fy, Esh/Es, LDR, α） | GFE-UserGuide |
| ① | UserMat 6：JH-2 | - |  | UG附录二(2) p285-286 | 陶瓷材料，23 参数 | GFE-UserGuide |
| ① | UserMat 7：E-v（邓肯-张） | - |  | UG附录二(2) p286 | 岩土类，10 参数 | GFE-UserGuide |
| ① | UserMat 8：E-B（邓肯-张改进） | - |  | UG附录二(2) p286-287 | 岩土类，8 参数 | GFE-UserGuide |
| ① | Van-der-Waals 超弹 | - |  | Imp§2.2.9 | μ/λm/a/β/D 五参数 | GFE-Implicit |
| ① | YJK 结构材料线性/非线性转换 | geotool.convert_material(0/1) |  | UG§1.18.10 | 导入 YJK 模型后材料线性↔非线性转换；非 GFE 预设材料不转换 | GFE-UserGuide |
| ① | YJK 结构材料线性/非线性转换+配筋转换 | convert_material+convert_reinforce |  | Cases§10.18 | 工程—材料及配筋转换：材料选"非线性"、配筋选"无/默认/YJK"分别转换 | GFE-Cases |
| ① | Yeoh 超弹（3 阶） | - |  | Imp§2.2.6/§3.6 | C10/C20/C30+D1/D2/D3，算例 C20 取负值 | GFE-Implicit |
| ① | davidenkov 材料复原 revert_davidenkov | geotool.revert_davidenkov |  | Cmd§3.4.19 | revert_davidenkov(mats) 转回普通材料，返回 list[string] | GFE-Cmd |
| ① | truss 特殊单元截面 | - |  | UG§1.9.5 | 按实体截面建立，"厚度"实为截面面积 | GFE-UserGuide |
| ① | 一维塑性损伤本构（梁单元专用混凝土） | user(user_type=1) 7参数 |  | Explicit§2.4.1 | 受压硬化/损伤+抗拉刚度/受拉损伤四曲线；仅梁单元 | GFE-Explicit |
| ① | 一维非线性混凝土 | - |  | UG§1.8.5b | 梁单元用；泊松比固定 0.2；可选 JC 率效应 | GFE-UserGuide |
| ① | 一键生成/移除配筋 | geotool.convert_reinforce(0/1/2) |  | FAQ§3.13 | 配筋可选"无/默认（参数可调）/读取YJK配筋"三种模式 | GFE-FAQ |
| ① | 一键转换结构材料线性/非线性 | geotool.convert_material |  | FAQ§3.13 | "YJK结构材料与配筋转换"对话框一键切换结构材料线性/非线性 | GFE-FAQ |
| ① | 三轴排水固结试验数值复现 | - |  | Explicit§2.10.2 | 三步硬顺序：自重应力平衡→施加围压→施加轴向偏差载荷；3 级围压 | GFE-Explicit |
| ① | 三轴排水固结试验数值模拟流程 | soils_step固结+材料/边界全API |  | Imp§2.5.2 | 三步串行：自重应力平衡→施加围压→施加轴向偏差载荷 | GFE-Implicit |
| ① | 创建材料（密度/弹性） | material()+density+elastic+mat_mgr |  | SSA§3.1.2(1) | Materials→Create：General/Density 填质量密度，Elasticity/Elastic 填杨氏模量、泊松比 | GFE-SSA |
| ① | 剪切失效定义（塑性内嵌） | material.plastic |  | Cmd§2.6.5 | params 前两位 = 剪切失效等效塑性应变及应变率 | GFE-Cmd |
| ① | 区域选择同步创建集合 | 等效gset/nset/elset.add直接建集 |  | Cases§1.2.2 | 选区域同时生成命名集合（raft/col/bc-z/PickedSet-N 等） | GFE-Cases |
| ① | 单元级本构测试方法（单拉/剪切/反复加卸载） | - |  | Explicit§2.11.1.2-2.11.1.4 | 单 c3d8 固定底面 4 顶点+顶面 4 顶点位移幅值历程的标准测试流程 | GFE-Explicit |
| ① | 南水双屈服面本构（NHRI） | user(user_type=4) 11参数 |  | Explicit§2.10 | f1=p²+r²q²、f2=q^s/p 双屈服面，10 参数，非线性/剪胀/软化 | GFE-Explicit |
| ① | 南水双屈服面模型（NHRI）本构 | user(user_type=4) |  | Imp§2.5 | 10 参数双屈服面土体模型（非线性、剪胀、软化），围压 500/1000/2000 kPa 三轴对标 | GFE-Implicit |
| ① | 南水模型 | - |  | UG§1.8.6d | 10 参数双屈服面模型 | GFE-UserGuide |
| ① | 反复加卸载滞回分析 | - |  | Imp§2.4.2.4 | 三角波式幅值函数驱动位移反复加卸载，输出滞回曲线 | GFE-Implicit |
| ① | 土体材料→Davidenkov 转换（可还原） | convert_to_davidenkov/revert_davidenkov |  | UG§1.18.9 | 含试验数据土材料一键转 Davidenkov，保留试验数据支持还原；拟合范围示例 1e-5~1e-3（可达性 c02 判是/c03 判未知，待仲裁） | GFE-UserGuide |
| ① | 土体材料转换（弹性→Davidenkov，含液化参数与"还原"） | convert_to_davidenkov/revert_davidenkov |  | Cases§10.17 | 工程—土体材料转换：批量勾选一键追加 Davidenkov 参数块（A/B/γ0+yh_* 液化系列），可逆 | GFE-Cases |
| ① | 基床系数 | material.bed_coefficient |  | Cmd§2.6.15; UG§1.8.6c | bed_coefficient()，kh 水平 / kv 垂直 | GFE-Cmd+GFE-UserGuide |
| ① | 塑性损伤本构 CDP（壳/实体） | - |  | Explicit§2.4.2 | 剪胀角/偏移分数/单双轴强度比/粘性参数；拉/压/剪/循环验证齐全 | GFE-Explicit |
| ① | 塑性（各向同性/Johnson-Cook 硬化） | - |  | UG§1.8.4a | 多组应力-应变；可开率效应、剪切失效；JC 硬化 6 参数 | GFE-UserGuide |
| ① | 壳截面属性 | - |  | UG§1.9.3 | 各向同性（材料/壳厚/积分点数/偏心）或膜（材料/膜厚） | GFE-UserGuide |
| ① | 壳截面属性（各向同性/膜） | - |  | Cases§3.1.3 | 材料/壳厚度/积分点个数/钢筋层/偏心（单值） | GFE-Cases |
| ① | 壳截面（分层、积分点、钢筋层） | section.property_shell |  | Cmd§2.9.2 | property_shell()，thickness/integral_point/layer_num/has_rebar/rebar | GFE-Cmd |
| ① | 壳钢筋层 | - |  | UG§1.9.3 | 单/多层：层名/材料/面积/间隔/位置/角度/方向/延伸率/半径 | GFE-UserGuide |
| ① | 多孔体积模量 | material.porous_bulk_moduli |  | Cmd§2.6.13 | porous_bulk_moduli()，permeating_fluid 渗透流体体积模量 | GFE-Cmd |
| ① | 孔隙体积模量 | - |  | UG§1.8.7b | 显式动力孔隙流体必需 | GFE-UserGuide |
| ① | 完整示例③：修改材料属性 | mat_mgr.edit |  | Cmd§8.3 | find→遍历 entries 按 type(entry).__name__ 判型→改 params→mat_mgr().edit() 提交 | GFE-Cmd |
| ① | 实体截面 | section.property_solid |  | Cmd§2.9.1 | property_solid()，绑 elset_name + mat_name，可选厚度 | GFE-Cmd |
| ① | 实体截面属性 | - |  | Cases§1.2.2; UG§1.9.2 | 类别"实体"+单元集+材料+各向同性厚度（默认 1） | GFE-Cases+GFE-UserGuide |
| ① | 密度 | - |  | Cases§1.2.2; UG§1.8.2a | 常规类→密度 | GFE-Cases+GFE-UserGuide |
| ① | 密度定义 | material.density |  | Cmd§2.6.2 | density()，params[0]=密度，temp_dp 一般 False | GFE-Cmd |
| ① | 屈曲钢筋本构滞回验证（T3D2） | user(user_type=5)+常规命令流建模 |  | Imp§2.7.2 | 5 个 T3D2 单元拉压滞回曲线与软件A对比 | GFE-Implicit |
| ① | 弹塑性本构（线性强化） | - |  | Explicit§2.2 | 塑性应力应变曲线输入；表列梁/壳/实体（验证例却用平面应变，见②）；仅显式动力 | GFE-Explicit |
| ① | 弹性/弹塑性土体材料文件导入（*.gmat） | io.import_mat |  | FAQ§3.13 | 直接导入 gmat 土体材料文件，再在土层界面替换材料属性 | GFE-FAQ |
| ① | 弹性本构 | - |  | Explicit§2.1 | 梁/平面应变/壳/实体；隐式静力+模态+显式动力 | GFE-Explicit |
| ① | 弹性模型转弹塑性（修订记录线索） | geotool.convert_material(1) |  | FAQ修订记录 | 指向 §3.13，仅作能力线索不计入能力总数 | GFE-FAQ |
| ① | 弹性（E/ν/模量时间尺度） | - |  | Cases§2.2.2 | 弹性类→弹性；含"模量时间尺度"下拉（默认/案例选"长期"） | GFE-Cases |
| ① | 截面属性复制+集合重指派 | - |  | Cases§12.10 | 右键复制截面，双击副本改"单元集"（Propery-ganggui-L→-R 对称件惯用法） | GFE-Cases |
| ① | 摩尔库伦 | material.mohr_coulomb |  | Cmd§2.6.10; UG§1.8.4b | mohr_coulomb()，n_plasticity/plasticity + n_cohesion/cohesion | GFE-Cmd+GFE-UserGuide |
| ① | 摩尔库伦塑性 | - |  | Cases§6.1.2 | 摩擦角/剪胀角/黏结力屈服应力-绝对塑性应变表 | GFE-Cases |
| ① | 摩尔库伦塑性参数输入 | - |  | FAQ§3.21 | 大震弹塑性、无试验曲线时手动填摩尔库伦参数 | GFE-FAQ |
| ① | 摩尔库伦本构 | - |  | Explicit§2.3 | 摩擦角+剪胀角+初始屈服粘聚力；平面应变/实体；仅显式动力 | GFE-Explicit |
| ① | 时域粘弹性（Prony） | - |  | UG§1.8.3d | g_i/k_i/τ_i；频域 Tabular 仅可直接改 inp（附录二） | GFE-UserGuide |
| ① | 材料 CRUD 与特性管理 | - |  | UG§1.8.1 | 创建/编辑/重命名/移除材料；名称创建后不可改 | GFE-UserGuide |
| ① | 材料创建框架（常规/弹性/塑性/混凝土/岩土五大类页签） | - |  | Cases§1.2.2 | 材料对话框五页签体系 | GFE-Cases |
| ① | 材料对象创建（entries 容器模式） | material.material |  | Cmd§2.6.1 | material() 对象 + entries 列表装入各属性子对象，再 mat_mgr().add() | GFE-Cmd |
| ① | 材料导入 .gmat | io.import_mat |  | Cases§4.2.2 | 通用—文件—导入—导入材料，仅认 *.gmat | GFE-Cases |
| ① | 材料导出 .gmat | io.export_mat |  | Cases§4.2.1 | 通用—导出—导出材料，GFE Material File(*.gmat) | GFE-Cases |
| ① | 材料核对/编辑 | - |  | Cases§6.3.3 | 双击树中材料打开参数对话框改值 | GFE-Cases |
| ① | 材料级 Rayleigh 阻尼 | material.damping |  | Cmd§2.6.4; UG§1.8.2b | α、β 两参数（显式/隐式动力、频响；须与其他本构组合） | GFE-Cmd+GFE-UserGuide |
| ① | 材料级瑞利阻尼（按材料差异化 α/β） | - |  | Imp§6.1/§6.6/§6.6.1 p172-173 | 不同材料可分别赋不同瑞利参数；验证例左柱 β=0.001 vs 右柱 β=0.01 衰减对照，Newmark 隐式动力 | GFE-Implicit |
| ① | 梁截面-圆形 | - |  | Cases§6.1.3 | 半径 r 输入自动算截面特性 | GFE-Cases |
| ① | 梁截面-工字型/H形 | - |  | Cases§6.1.3 | l/h/b1/b2/t1/t2/t3 七参数；"数据"页填材料/方向矢量/偏心 | GFE-Cases |
| ① | 梁截面-矩形（自动算截面常数） | - |  | Cases§3.1.3 | a/b 输入自动算面积/扭转惯量/剪切刚度等；数据页设材料+方向向量+偏心（4 分量） | GFE-Cases |
| ① | 梁截面属性 | - |  | UG§1.9.4 | 矩形/箱/工字/圆/L/管/厚管/任意/通用 9 种；可一键算 A、Asy、Asz、Ixx、Iy、Iz、Ksy、Ksz | GFE-UserGuide |
| ① | 梁截面形状参数对照表 | property_beam.shape 0-7+shape_params |  | Cmd§2.9.7 | shape 0-7 与 shape_params 逐型对照（见③） | GFE-Cmd |
| ① | 梁截面（8 种形状+纤维） | section.property_beam |  | Cmd§2.9.3 | property_beam()，shape 0-7 + shape_params + direction 主方向 + fiber_num | GFE-Cmd |
| ① | 梁通用截面（直接给截面常数） | section.property_beam_general |  | Cmd§2.9.4 | property_beam_general()，density/poisson/param1（面积惯性矩等）/param2（E、G）/axis（手册示例配错，见 | GFE-Cmd |
| ① | 泡棉 | - |  | UG§1.8.3c | 最多 6 组 (μ,α,ν)，暂不支持数据行输入 | GFE-UserGuide |
| ① | 泡棉（hyperfoam） | material.hyperfoam |  | Cmd§2.6.8 | hyperfoam()，比超弹多 simple_shear 试验数据 | GFE-Cmd |
| ① | 混凝土塑性损伤本构（一维梁单元版 + 平面应力分层壳版） | user_type=1+concrete_damaged分层壳 |  | SSA§1.1.5/§3.4/§6.3 | 梁单元用一维 CDP、分层壳用平面应力 CDP，输出压/拉损伤 | GFE-SSA |
| ① | 混凝土塑性损伤预设库（C2_Mat30~80） | - |  | Cases§4.2.1 | 内置 CDP 参数组，选后改名、可移除特性 | GFE-Cases |
| ① | 混凝土塑性损伤（CDP） | - |  | UG§1.8.5a | 剪胀角+压缩硬化/损伤+拉伸刚度/损伤 | GFE-UserGuide |
| ① | 混凝土塑性损伤（CDP）完整定义 | material.concrete_damaged |  | Cmd§2.6.6 | concrete_damaged()：plasticity 5 参数 + 压硬化/压损伤/拉刚度/拉损伤四条曲线 + 拉压刚度恢复 + 率效应 | GFE-Cmd |
| ① | 渗透性（孔隙流体） | - |  | UG§1.8.7a | 仅各向同性；间隙流体比重+渗透系数 K | GFE-UserGuide |
| ① | 渗透系数材料属性 | - |  | Imp§1.5.2/§1.5.3 | 孔压单元材料带渗透系数（m/s） | GFE-Implicit |
| ① | 热膨胀 | material.expansion |  | Cmd§2.6.14 | expansion()，sub_type + value 列表 | GFE-Cmd |
| ① | 用户材料（11 种 user_type） | material.user |  | Cmd§2.6.11 | user()，user_type：0普通/1一维非线性/2 Davidenkov/3 HSS/4南水/5屈曲钢筋/6 JH2/7 E_v/8 E_B/9 Use | GFE-Cmd |
| ① | 用户材料（入口） | material.user 11种user_type |  | Cases§6.3.1 | 常规类含"用户材料"入口（未演示；对应 Davidenkov 等 *User Material） | GFE-Cases |
| ① | 用户自定义材料 | - |  | UG§1.8.2c | 任意数量常数（配合 *User Material） | GFE-UserGuide |
| ① | 粘弹性（Prony 级数） | material.viscoelastic |  | Cmd§2.6.9 | viscoelastic()，params 按 g_i,k_i,τ_i 顺序排列 | GFE-Cmd |
| ① | 线弹性 | - |  | UG§1.8.3a | 杨氏模量、泊松比、模量时间尺度 | GFE-UserGuide |
| ① | 线弹性定义 | material.elastic |  | Cmd§2.6.3 | elastic()，params=[E, ν]，type 必须设 0，moduli_time_scale 0长期/1瞬态 | GFE-Cmd |
| ① | 线性强化弹塑性本构（屈服应力-塑性应变表） | - |  | Imp§2.1.1/§1.1.3.2/§1.2/§1.3 | 表格式硬化曲线，支持≥2行折线 | GFE-Implicit |
| ① | 考虑土层液化的 Davidenkov 本构 | user(user_type=2) 12参数 |  | SSA§3.5/§6.4 | 液化扩展参数 γtv/m/n/a3/c1/c3，输出孔压比（SDV），可对指定土层启用 | GFE-SSA |
| ① | 考虑屈曲的一维钢筋本构（VECCHIO 受拉 + 屈曲受压） | user(user_type=5) |  | Imp§2.7.1 | 双折线受拉骨架 + 长细比 L/D 控制受压屈曲软化，用于 T3D2 桁架钢筋 | GFE-Implicit |
| ① | 考虑屈曲的一维钢筋本构（VECCHIO+屈服效应） | user(user_type=5) |  | Explicit§2.12 | 受拉双折线+受压 4 段屈曲曲线，L/D 长细比+α 系数，T3D2 桁架单元 | GFE-Explicit |
| ① | 膨胀系数 | - |  | UG§1.8.3e | 配合温度荷载 | GFE-UserGuide |
| ① | 获取截面管理器 | section.sect_mgr |  | Cmd§2.9.6 | sect_mgr() | GFE-Cmd |
| ① | 获取材料管理器 | material.mat_mgr |  | Cmd§2.6.17 | mat_mgr()（单例） | GFE-Cmd |
| ① | 蠕变 | material.crep |  | Cmd§2.6.16; UG§1.8.4c | crep()（注意类名拼写非 creep），law/time/nRow/data；必须与塑性属性同列 entries | GFE-Cmd+GFE-UserGuide |
| ① | 蠕变材料（strain hardening 律） | creep law=strain |  | Imp§2.6 | ε̇^cr=(A·q̃^n·[(m+1)ε̄^cr]^m)^(1/(m+1))，A/n/m 用户定义，静力中生效 | GFE-Implicit |
| ① | 试验数据对象 | material.test_data |  | Cmd§2.6.12 | test_data()，n_test_data 行数 + test_data 值 | GFE-Cmd |
| ① | 试验数据（G/Gmax+阻尼比） | - |  | UG§1.8.6b | 拟合出 Davidenkov 参数；默认拟合应变范围 1e-5~1e-3 | GFE-UserGuide |
| ① | 试验曲线一键计算 A、B、γ0 | convert_to_davidenkov内含曲线拟合 |  | FAQ§3.21 | 由试验数据曲线一键拟合 Davidenkov 类参数 A、B、γ0 填入土体材料 | GFE-FAQ |
| ① | 质量比例阻尼（α 阻尼，材料级） | - |  | Explicit§1.1.3 | 质量阻尼系数参与动力分析 | GFE-Explicit |
| ① | 超弹 Uniaxial Test Data 输入 | hyperelastic.uniaxial+test_data |  | Imp§2.2.1/§2.2.3/§2.2.4 | M-R/Hyperfoam/Polynomial 支持单轴试验数据，GFE 在预处理阶段转为材料参数 | GFE-Implicit |
| ① | 超弹性 | - |  | UG§1.8.3b | Mooney-Rivlin/Ogden/Yeoh/Polynomial/Marlow/Reduced Polynomial 六种 | GFE-UserGuide |
| ① | 超弹性（8 种本构） | material.hyperelastic |  | Cmd§2.6.7 | hyperelastic()，he_type 0-7：Mooney-Rivlin/Ogden/Yeoh/Polynomial/Marlow/Repolynomi | GFE-Cmd |
| ① | 超弹试验数据输入 | material.hyperelastic |  | Cmd§2.6.7 | uniaxial/biaxial/planar/volumetric 四类试验数据列表 | GFE-Cmd |
| ① | 转化为 davidenkov 材料 convert_to_davidenkov | geotool.convert_to_davidenkov |  | Cmd§3.4.18 | convert_to_davidenkov(mats) 把输入材料转为 davidenkov 材料（需材料有 test data 属性），返回 list[str | GFE-Cmd |
| ① | 转换材料（YJK）convert_material | geotool.convert_material |  | Cmd§3.4.20 | convert_material(type)：0=非线性→线性，1=线性→非线性；YJK 导入材料专用，返回 bool | GFE-Cmd |
| ① | 转换配筋（YJK）convert_reinforce | geotool.convert_reinforce |  | Cmd§3.4.21 | convert_reinforce(type)：0=移除全部配筋，1=转 YJK 配筋，2=转默认配筋，返回 bool | GFE-Cmd |
| ① | 金属塑性（各向同性硬化/Johnson-Cook） | material.plastic |  | Cmd§2.6.5 | plastic()，harden_type 0/1；params 前两位为剪切失效参数，不用时填 <0 | GFE-Cmd |
| ① | 钢筋层定义 | section.rebar_layer |  | Cmd§2.9.5 | rebar_layer()，rebar_geometry/orientation_name/rebar_num/layer_name/mat_name/para | GFE-Cmd |
| ① | 钢筋弹塑性本构（纤维梁/分层壳单元） | plastic+rebar_layer+fiber_num |  | SSA§1.1.5 | 纤维梁单元和分层壳单元中引入钢筋弹塑性本构 | GFE-SSA |
| ① | 阻尼转换 | - |  | UG§1.18.8 | 按阻尼比+固有频率算 Rayleigh 阻尼写入选中材料 | GFE-UserGuide |
| ① | 陶瓷本构模型（JH-2 类，含损伤演化） | user(user_type=6) 23参数 |  | Explicit§2.9 | 22 参数（A/B/C/M/N、HEL/PHEL、D1/D2、K1-K3、FS 等），SDEG 损伤输出与破坏模拟 | GFE-Explicit |
| ① | 预设材料 | - |  | UG§1.8.8 | 一维非线性、CDP、钢材三类预设参数包 | GFE-UserGuide |
| ② | *Acoustic medium | - | 材料entry_type无声学项,改INP *Acoustic medium | UG附录二(2) p277 | 声学介质，归属上方最近 *Material，数据行 BULK MODULUS | GFE-UserGuide |
| ② | *Conductivity | - | 命令流无热传导项,改INP(需热固耦合步) | UG附录二(2) p287 | 热传导系数，需热固耦合分析步，仅支持 C3D4（见⑤待仲裁#3） | GFE-UserGuide |
| ② | Hyperelastic：Van-der-Waals | - | he_type 0-7 无此型,改INP *HyperElastic | Explicit§2.7.8 | μ/λm/α/β/D 五参数 | GFE-Explicit |
| ② | visco 频域粘弹性阻尼（超弹基材复模量） | - | viscoelastic仅Prony,频域tabular改INP | Imp§6.5/§6.5.1 p170-172 | 频域复模量参数表（Omega g*/k* real/imag + Frequency），Mooney-Rivlin 基底，仅直接法频响 | GFE-Implicit |
| ② | 一键计算 Alpha 阻尼 | - | 无一键API,自算α后material.damping写入 | FAQ§3.21 | 按土体阻尼比+场地反应分析一阶土体模态一键算出 Alpha 阻尼填入材料 | GFE-FAQ |
| ② | 声学材料定义（体积模量+密度） | - | entry_type无声学,改INP *Acoustic medium | Explicit§1.5.1 | 空气：1.424×10⁵ N/m² + 1.21 kg/m³（注意此节为 SI 制） | GFE-Explicit |
| ② | 热膨胀材料 + 温度载荷静力分析 | - | expansion有API,温度荷载type=14未用改INP | Imp§2.3 | 热膨胀系数+整体温度载荷（20℃）求热应力/热变形 | GFE-Implicit |
| ② | 瑞利阻尼自动计算并写入材料 | - | 无自动算API,自算αβ后damping写入 | FAQ§3.3 | 输入阻尼比+频率，程序自动算瑞利阻尼系数写入材料参数 | GFE-FAQ |
| ② | 阻尼转换（阻尼比→材料阻尼） | - | 无转换API,自算后写damping entry | Cases§4.3.1 | 工程—阻尼比：选材料+输阻尼比+模态频率→自动算 α 写入材料（β=0） | GFE-Cases |
| ② | 预设常用材料非线性参数库 | - | 预设库为GUI面板,等效import_mat载gmat | Explicit第2章引言; SSA§1.1.5 | 预置 Q235-Q460 钢材、HPB235-HPB500 钢筋、C30-C80 混凝土非线性参数，可直接调用 | GFE-Explicit+GFE-SSA |
| ③ | *Shear Failure | - |  | UG附录二(2) p278 | 剪切失效——整节为删除线文本，标注"求解器暂时未接"，不可用 | GFE-UserGuide |
| 未知 | 材料级"质量系数"参数 | - |  | Explicit§12.2.1 | 线弹性材料表含"质量系数"列（硬岩 1.702、混凝土 2.004），与密度并列；本区间手册未解释其定义 | GFE-Explicit |

## D03 网格（73 项：①67 ②5 ③1）

| 层 | 能力 | API入口 | 断点/理由 | 出处 | 说明 | 源手册 |
|---|---|---|---|---|---|---|
| ① | *Elset（generate 选项） | - |  | UG附录二(1) p275-276 | 单元集定义，必要参数 elset=名称，可选 generate | GFE-UserGuide |
| ① | *Node / *Element / *Nset | - |  | UG附录二(1) p275 | 节点、单元（type 必要、elset 可选）、节点集（nset 必要、generate 可选） | GFE-UserGuide |
| ① | *Surface | - |  | UG附录二(1) p276 | 表面集定义，name 必要；type 缺省=element 且目前仅支持 element | GFE-UserGuide |
| ① | B21 二维纤维梁（线弹性 / 线性强化） | - |  | Imp§1.3.2 | 二维版纤维梁 | GFE-Implicit |
| ① | B31 三维纤维梁（线弹性 / 线性强化） | - |  | Imp§1.3.1 | 悬臂梁端部集中力，输出位移+截面弯矩 SM1 | GFE-Implicit |
| ① | C3D10 二阶四面体（线弹性 / Hyperfoam） | - |  | Imp§1.1.5 | 超弹验证用位移控制加载（1s 匀速 5m） | GFE-Implicit |
| ① | C3D4 + Mohr Coloumb 弹塑性 | - |  | Imp§1.1.1.2 | MC参数摩擦角+黏聚力，惯性力加载 | GFE-Implicit |
| ① | C3D4 一阶四面体（线弹性静力） | - |  | Imp§1.1.1.1 | 底部固定+顶面集中力，输出位移/最大主应变/Mises，与软件A对比 | GFE-Implicit |
| ① | C3D6 楔形体（线弹性 / MC） | - |  | Imp§1.1.2 | 楔形体单元两种本构静力验证 | GFE-Implicit |
| ① | C3D8 一阶六面体（线弹性 / 线性强化） | - |  | Imp§1.1.3 | 塑性用屈服应力-塑性应变表 | GFE-Implicit |
| ① | C3D8I 非协调模式六面体（线弹性 / MC） | - |  | Imp§1.1.4 | C3D8I 是独立于 C3D8 的单元子类型 | GFE-Implicit |
| ① | CPE3 平面应变三角形（线弹性 / MC） | - |  | Imp§1.4.1 | 自重（9.8 m/s² 惯性力）平面应变验证 | GFE-Implicit |
| ① | CPE4 平面应变四边形单元（单元生死工况实证） | generate_dim=2网格+case.set_elemDel |  | Imp§7.4.2 p188-190 | 既有 I 表 #91 缺口补齐：CPE4 正文验证存在（差异 ≤1.47%） | GFE-Implicit |
| ① | CPE4 平面应变四边形单元（目录预告） | mesh_generator generate_dim=2 |  | Imp表1行258/§7.4.2 | 第一章未验证 CPE4；已于 P1.5 补齐：§7.4.2 单元生死验证（见 L 表#116） | GFE-Implicit |
| ① | S3 三角形分层壳（线弹性 / 线性强化） | - |  | Imp§1.2.1 | 三向惯性力静力验证 | GFE-Implicit |
| ① | S4 四边形分层壳（线弹性 / 线性强化） | - |  | Imp§1.2.2 | 同上，四边形 | GFE-Implicit |
| ① | 一阶六面体实体单元（静/模态/动力） | - |  | Explicit§1.4.3.1-1.4.3.3 | 同一柱体换六面体三类分析 | GFE-Explicit |
| ① | 一阶四面体实体单元（静力/模态/动力） | - |  | Explicit§1.4.1.1-1.4.1.3 | 惯性力静力+前三阶模态+正弦惯性力显式动力 | GFE-Explicit |
| ① | 一阶楔形（wedge）实体单元（静/模态/动力） | - |  | Explicit§1.4.2.1-1.4.2.3 | 同一柱体换楔形单元三类分析 | GFE-Explicit |
| ① | 三维纤维梁单元（2节点、6自由度/节点） | - |  | Explicit§1.1.2 | 空间梁静力/模态/动力 | GFE-Explicit |
| ① | 三节点三角形分层壳单元（6自由度/节点） | - |  | Explicit§1.3.1 | 三向惯性力静/模态/动力，输出 SF/SM 内力 | GFE-Explicit |
| ① | 三节点三角形平面应变单元（CPE3 类） | - |  | Explicit§1.2.1 | 2自由度/节点，静/模态/动力，差异<0.2% | GFE-Explicit |
| ① | 二维纤维梁单元（2节点、3自由度/节点） | - |  | Explicit§1.1.1 | 平面内梁静力/模态/动力，位移/剪力/弯矩与软件A差异<3% | GFE-Explicit |
| ① | 全局网格参数 | - |  | UG§1.6(3) | 最大/最小尺寸、单元形状、2D/3D 剖分算法、单元类型 | GFE-UserGuide |
| ① | 全局网格控制（最大/最小尺寸、2D/3D 剖分算法、2D 合并算法、合并全部） | - |  | FAQ§3.2 | 网格划分参数面板：Frontal-Delaunay for Quads / Delaunay / MeshAdapt / HXT / Simple / Reco | GFE-FAQ |
| ① | 分层壳几何非线性（显式动力大变形） | - |  | Explicit§1.3.3.1 | 三角形/四边形分层壳（4m×3m×0.1m），底边固定+顶边位移荷载，显式动力 nlgeom | GFE-Explicit |
| ① | 分批划网格（中途改全局参数） | - |  | Cases§6.7.1 | 结构/土体按不同参数（甚至不同单元形状）分批划分 | GFE-Cases |
| ① | 单元类型指定（默认映射） | - |  | FAQ§3.2 | 线 B31、三角形 S3R、四边形 S4R、四面体 C3D4、六面体 C3D8R、四棱锥 C3D5、三棱柱 C3D6 | GFE-FAQ |
| ① | 四节点四边形分层壳单元（6自由度/节点） | - |  | Explicit§1.3.2 | 同上，差异<3% | GFE-Explicit |
| ① | 四节点四边形平面应变单元（CPE4 类） | - |  | Explicit§1.2.2 | 静/模态/动力，差异<3% | GFE-Explicit |
| ① | 四边形/六面体主导网格 | - |  | Cases§9.3 | 单元形状选"四边形/六面体"，2D 算法切 Frontal-Delaunay for Quads | GFE-Cases |
| ① | 地震分析网格波长准则 | - |  | Explicit§9.4 | 土体网格尺寸满足一般地震波波长 1/5-1/10 倍要求（§12.2.3 处写 1/5，手册内部口径不一） | GFE-Explicit |
| ① | 复制网格 | geotool.copy_mesh |  | UG§1.17.6 | 由几何/单元/表面集生成新网格（可与源共节点）；生成后无法删除 | GFE-UserGuide |
| ① | 复制网格（共节点生成壳/梁单元集） | copy_mesh(origin_node+typeName) |  | Cases§3.1.5 | 源区域=几何集，指定目标单元类型（S3R/B31/<同源>），勾"使用和源相同的节点"，产物名=前缀+"-1" | GFE-Cases |
| ① | 快速设全局网格尺寸 set_approximate_size | controller.set_approximate_size |  | Cmd§3.5.1 | set_approximate_size(size) 等价于 user_option["GFE.DefaultSize"]=size | GFE-Cmd |
| ① | 恢复推荐默认参数 set_as_default() | controller.set_as_default |  | Cmd§3.5.1 | 恢复为推荐的默认参数配置 | GFE-Cmd |
| ① | 扫掠法网格 | - |  | UG§1.6(5) | 起始/终止/连接区+层数/比例/dx,dy,dz；支持非均匀分层 | GFE-UserGuide |
| ① | 扫掠法网格控制 | - |  | Cases§15.11 | 形状规则体用扫掠法：指定源面/目标面与层参数后再执行划分 | GFE-Cases |
| ① | 扫掠网格控制器 sweep_control | mesh_generator.sweep_control |  | Cmd§3.5.2 | source/target/body 形状ID三元组 + dx/dy/dz + layers/ratio 非均匀分层 + recomb_lateral/reco | GFE-Cmd |
| ① | 控制器八项属性配置 | mesh_generator.controller |  | Cmd§3.5.1 | number_option/string_option/user_option/sweep_option/size_option/geom_to_type/ge | GFE-Cmd |
| ① | 查找最近单元 | mesh_data.find_near_element |  | Cmd§2.5.10 | find_near_element(centre, distance=1e-7)，返回只读副本 | GFE-Cmd |
| ① | 查找最近节点 | mesh_data.find_near_node |  | Cmd§2.5.9 | mesh_data.find_near_node(centre, distance=1e-7)，返回只读副本 | GFE-Cmd |
| ① | 梁单元偏心连接（梁+实体混合模型） | mpc type=0 梁式多点约束等效 |  | Explicit§1.1.3 | 下部实体+上部梁组合悬臂梁静/动力验证 | GFE-Explicit |
| ① | 梁单元几何非线性（大变形拟静力） | - |  | Explicit§1.1.4 | 斜杆顶端弯矩缓慢加载（60s 至 500kN·m），线性 vs 几何非线性 | GFE-Explicit |
| ① | 线控制 | - |  | UG§1.6(4) | 几何线集按"数量(节点数)"或"间距(密度)"控制网格点 | GFE-UserGuide |
| ① | 线控制（局部加密/指定节点数） | - |  | Cases§3.1.5 | 对指定线单独控制尺寸或网格点个数（密度默认 -1）；类型"通过数量/通过间距"二选一 | GFE-Cases |
| ① | 线（边）网格密度控制器 curve_control | mesh_generator.curve_control |  | Cmd§3.5.3 | 按边集合 set_name 控制边上节点数 count 或间距 density，挂入 ctrl.size_option | GFE-Cmd |
| ① | 网格全局参数（尺寸/算法/单元类型映射） | - |  | Cases§1.2.7 | 最大/最小尺寸（或单一"大致尺寸"）、2D/3D 剖分算法、2D 合并算法、各形状单元类型、合并全部(2D)、自动超限 | GFE-Cases |
| ① | 网格划分失败定位（QueryShape 命令） | - |  | FAQ§3.17 | test 功能对话框输入 "QueryShape -id 几何体编号,类型号,编号" 在黑色命令窗口查坐标定位 | GFE-FAQ |
| ① | 网格划分（Mesh） | mesh_generator.generator.mesh+controller |  | SSA§3.1.5 | 激活几何体选择→Mesh→选单元类型与网格尺寸 | GFE-SSA |
| ① | 网格划分（失败定位、合并几何体不共节点、二维网格类型）（修订记录线索） | generator.mesh+controller(失败定位为GUI提示) |  | FAQ修订记录 | 指向 §3.15-3.18，仅作能力线索不计入能力总数 | GFE-FAQ |
| ① | 网格删除 | - |  | UG§1.6(1) | 树状列表右键"移除网格"；重剖前必须先删除 | GFE-UserGuide |
| ① | 网格复制 copy_mesh | geotool.copy_mesh |  | Cmd§3.4.8 | 复制几何集/单元集网格；可换单元类型（typeName 仅 asSource=False 时有效）、可共节点（origin_node） | GFE-Cmd |
| ① | 网格对象属性访问 | mesh_object |  | Cmd§2.5.2-2.5.8 | mesh_object：id()/name()/mesh()/element_data()/node_data()/geo_obj()，另有 max_node_ | GFE-Cmd |
| ① | 网格控制器创建 controller() | mesh_generator.controller |  | Cmd§3.5.1 | mesh_generator.controller() 创建网格控制器对象 | GFE-Cmd |
| ① | 网格控制管理器 | - |  | UG§1.6(2) | 统一管理全局参数/扫掠法/超限法/线控制条目 | GFE-UserGuide |
| ① | 网格生成 | - |  | UG§1.6(1) | 选中 ≥1 个几何部件后执行剖分 | GFE-UserGuide |
| ① | 网格生成执行 generator().mesh | mesh_generator.generator.mesh |  | Cmd§3.5.1-3.5.2 | generator.mesh(shapes, controller)，shapes 为几何名称列表 | GFE-Cmd |
| ① | 网格生成（按几何体执行） | - |  | Cases§7.2.8 | 选几何→执行划分；HintBar 内含全局参数快捷入口；主体/土体/隧道/道床/钢轨逐个划分 | GFE-Cases |
| ① | 网格阶次转换 | - |  | UG§1.6(6) | 一阶四面体↔二阶四面体整部件转换 | GFE-UserGuide |
| ① | 自动超限（AutoTransfinite）网格划分 | controller.auto_transfinite |  | FAQ§3.2 | 网格全局参数中的自动超限选项（MeshAdvance: AutoTransfinite=true），有不共节点副作用 | GFE-FAQ |
| ① | 获取网格管理器（单例） | mesh.mesh_mgr |  | Cmd§2.5.1 | mesh_mgr() | GFE-Cmd |
| ① | 获取节点 id+坐标列表 | mesh_object.node_data |  | Cmd§2.5.7 | node_data() 返回 ([nodeid…],[[x,y,z]…])，已排序 | GFE-Cmd |
| ① | 超限法网格 | - |  | UG§1.6(2) | 管理器中可创建"超限法"控制（手册未展开细节） | GFE-UserGuide |
| ① | 边界框内单元搜索 | mesh_data.find_element_inside |  | Cmd§2.5.12 | find_element_inside(lower, upper)，单元对象含 eid/sub_type/node_size/nodes | GFE-Cmd |
| ① | 边界框内节点搜索 | mesh_data.find_node_inside |  | Cmd§2.5.11 | find_node_inside(lower, upper) | GFE-Cmd |
| ① | 选择性不划网格（辅助几何） | - |  | Cases§10.12 | Basementboundary 等工具几何不划网格不参与计算 | GFE-Cases |
| ② | AC3D4 四节点四面体声学单元瞬态分析 | - | 声学材料无API,单元/材料改INP | Explicit§1.5.3 | 同一管道换 AC3D4 | GFE-Explicit |
| ② | AC3D6 六节点楔形声学单元瞬态分析 | - | 声学材料无API,单元/材料改INP | Explicit§1.5.2 | 同一管道换 AC3D6 | GFE-Explicit |
| ② | AC3D8 八节点六面体声学单元瞬态分析 | - | 声学材料无API,单元/材料改INP | Explicit§1.5.1 | 4m 空气管道、100Hz 正弦声压源、0.05s 瞬态声学动力 | GFE-Explicit |
| ② | 二阶四面体实体单元（10节点；静/模态/动力） | - | 阶次转换无命令流,GUI 1.6(6)或INP直写C3D10 | Explicit§1.4.4.1-1.4.4.3 | 同一柱体换二阶四面体三类分析 | GFE-Explicit |
| ② | 移除畸形网格功能 | - | GUI阈值对话框1.15.4(4),可自检后改INP | FAQ§3.7-5d | GFE 自带"移除畸形网格"功能，用于排查发散 | GFE-FAQ |
| ③ | 网格划分耗时日志 | - | GUI消息窗输出,无API读取 | Cases§5.3.1 | 输出"划分网格耗时/网格划分完成!" | GFE-Cases |

## D04 边界条件与荷载（112 项：①107 ②5 ③0）

| 层 | 能力 | API入口 | 断点/理由 | 出处 | 说明 | 源手册 |
|---|---|---|---|---|---|---|
| ① | *Amplitude | - |  | UG附录二(4) p291-292 | 幅值函数，name 必要，数据行仅支持 tabular | GFE-UserGuide |
| ① | *Boundary | - |  | UG附录二(4) p290 | 边界条件（约束/位移/初始速度），type=veolocity(原文)/acceleration，amplitude 可选 | GFE-UserGuide |
| ① | *CFlow | boundary type=17 集中孔隙流 |  | UG附录二(4) p292 | 集中孔隙流量，仅孔压单元+隐式计算，格式同 *Cload | GFE-UserGuide |
| ① | *Cload | - |  | UG附录二(4) p290 | 集中力；GFE 前处理创建的列车荷载写出 inp 时转换为集中力（见⑤待仲裁#5） | GFE-UserGuide |
| ① | *Dload | - |  | UG附录二(4) p290-291 | 惯性力/线荷载/区域外表面压力(P)/体积力(BX/BY/BZ) | GFE-UserGuide |
| ① | *DsFlow | boundary type=18 表面孔隙流 |  | UG附录二(4) p292 | 表面孔隙流量，仅孔压单元+隐式计算，格式同 *Dsload | GFE-UserGuide |
| ① | *Dsload | - |  | UG附录二(4) p291 | 面压力，数据行三位：表面集名称, P, 荷载数值 | GFE-UserGuide |
| ① | *Initial Conditions | - |  | UG附录二(4) p293 | 初始条件（stress/velocity/pore pressure/ratio），最外层、不能放 step 内 | GFE-UserGuide |
| ① | *Mass | boundary type=10 附加质量 |  | UG附录二(4) p292 | 节点质量，需配套 *Element, type=Mass 的单元集，仅各向同性 | GFE-UserGuide |
| ① | 21 种边界条件类型枚举 | boundary.boundary.type |  | Cmd§2.10.3 | type 0-20：约束/位移/初速度/速度/加速度/力/表面载荷/重力/线载荷/列车载荷/质量/声学/RLOAD/压力(未用)/温度(未用)/水压力/孔隙压力 | GFE-Cmd |
| ① | BC/荷载类型清单（10 种） | - |  | Cases§7.2.11 | 全约束/位移转动位移/初始速度/速度角速度/加速度/集中力力矩/压力/等效动水压力/惯性力/线荷载 | GFE-Cases |
| ① | Line Load 线荷载施加周面剪应力 | - |  | SSA§5.1.2(5) | Type=Line Load，Component 2 写 -1，Distribution=Y，Amplitude=SX | GFE-SSA |
| ① | Line Load 线荷载施加等效相对位移力 | - |  | SSA§5.1.2(d) | Type=Line Load，Component 1=区域 X 向弹簧刚度（如 40000），Distribution=Y，Amplitude=deltaUX， | GFE-SSA |
| ① | YJK 导入自动生成 Comb_M_xxx 附加质量 | io.import_yjk 自动产物 |  | FAQ§3.4/3.5 | 导入时自动在"边界条件与荷载"生成 (1.0附加恒载+0.5活载)/9.8 的附加质量 | GFE-FAQ |
| ① | 传递位移 pass_disp | engineer.pass_disp |  | Cmd§3.7.1 | engineer.pass_disp(db, src, dst, tolerance) 从 db 读 src 节点集位移，作为荷载施加到 dst 节点集 | GFE-Cmd |
| ① | 传递力 pass_force | engineer.pass_force |  | Cmd§3.7.2 | engineer.pass_force(db, src, dst, tolerance) 从 db 读 src 表面集节点位移/速度+单元应力，转集中力施加到  | GFE-Cmd |
| ① | 位移/转动位移 BC | - |  | UG§1.11.3 | U1~UR3 六自由度，基础系数×幅值函数 | GFE-UserGuide |
| ① | 位移/转动位移载荷（U1-U3/UR1-UR3）+ 缩放函数 | - |  | Imp§2.4.2.2图2.4.2-3 | GUI：区域+六分量+缩放函数（=幅值曲线，时间-值表格） | GFE-Implicit |
| ① | 位移/转动位移边界（显式动力+静力） | - |  | Explicit§3.1.1 | 节点/几何集位移直接指定；时域分布✓、空间分布✗ | GFE-Explicit |
| ① | 位移/转动位移（逐 DOF 勾选赋值） | - |  | Cases§5.3.1 | 侧面法向约束（U1=0 / U2=0）的实现载体 | GFE-Cases |
| ① | 位移/转动边界（Displacement/Rotation） | - |  | SSA§4.1.2(a)/§5.1.2(a) | 反应加速度法：侧面 Set-X 勾 U2 填 0（水平滑移）；反应位移法：地连墙底部两点 Set-base 约束 U1、U2 | GFE-SSA |
| ① | 位移边界 / 位移控制加载 | - |  | Imp§1.1.5.2/§2.2.1/§4.1.1/§4.2.1 | 节点/面指定位移，可时程内匀速施加 | GFE-Implicit |
| ① | 体力 | - |  | Imp§4.1.6/§4.2.7; UG§1.11.17 | 体积力荷载（GFE vs 软件A 差 5.7%，见②） | GFE-Implicit+GFE-UserGuide |
| ① | 体力荷载 | - |  | Explicit§3.1.8 | 单元体力（静力验证差异 5.7%） | GFE-Explicit |
| ① | 作用区域选择（集合或直接输 ID） | - |  | Cases§3.2.1 | "区域"按钮弹选择框，可选同类型集合或 ID 直输 | GFE-Cases |
| ① | 全约束 | - |  | UG§1.11.2 | 节点集/节点 ID，无其他参数 | GFE-UserGuide |
| ① | 全约束边界（Encastre） | - |  | SSA§4.1.2(a) | BCs & Loads→Type: Encastre，作用于底面集合 Set-Y | GFE-SSA |
| ① | 全约束（U1~UR3 全 0） | - |  | Cases§1.2.3 | 底面固支标准做法；轨道两端节点框选 PickedSet 全约束（BC-liangduan） | GFE-Cases |
| ① | 分布场关联边界 | boundary.boundary |  | Cmd§2.10.1 | distribution 字段挂分布场名称 | GFE-Cmd |
| ① | 初始地应力 InitGeostaticStress | initial_condition.InitGeostaticStress |  | Cmd§2.11.6 | value=[σ1, σ3, Z, α] 四参数 | GFE-Cmd |
| ① | 初始孔压 | - |  | UG§1.12.3 | 常数/线性（线性按 3D-Z、2D-Y 坐标） | GFE-UserGuide |
| ① | 初始孔隙压力 InitPorePress | initial_condition.InitPorePress |  | Cmd§2.11.4 | is_constant + value=[p1,v1,p2,v2] 两点插值 | GFE-Cmd |
| ① | 初始孔隙比 | - |  | UG§1.12.4 | 常数/线性（同上坐标约定） | GFE-UserGuide |
| ① | 初始孔隙比 InitRatio | initial_condition.InitRatio |  | Cmd§2.11.5 | is_constant + value=[r1,v1,r2,v2] | GFE-Cmd |
| ① | 初始孔隙比/初始孔压 初始条件 | InitRatio/InitPorePress |  | Imp§1.5.1/§1.5.3 | 渗流分析前需给定初始孔隙比与初始孔压分布 | GFE-Implicit |
| ① | 初始应力 | - |  | UG§1.12.1 | 6 分量；GUI 可设但求解器尚未支持计算 | GFE-UserGuide |
| ① | 初始应力 InitStress | initial_condition.InitStress |  | Cmd§2.11.2 | value=[σ11,σ22,σ33,σ12,σ13,σ23]，可挂 distribution 分布场 | GFE-Cmd |
| ① | 初始条件基类（name + set_name） | initial_condition |  | Cmd§2.11.1 | 所有初始条件共有属性 | GFE-Cmd |
| ① | 初始条件管理器 | initial_condition.ic_mgr |  | Cmd§2.11.9 | manager() 或别名 ic_mgr() | GFE-Cmd |
| ① | 初始温度 | - |  | UG§1.12.5 | 常数，支持空间分布 | GFE-UserGuide |
| ① | 初始速度 InitVelocity | initial_condition.InitVelocity |  | Cmd§2.11.3 | valid_dof 位掩码 + value=[v1,v2,v3] | GFE-Cmd |
| ① | 初始速度条件 | - |  | Explicit表5.1 | 初始条件类；时域✓、空间✗ | GFE-Explicit |
| ① | 初速度 | - |  | UG§1.12.2 | V1/V2/V3，支持空间分布 | GFE-UserGuide |
| ① | 加速度 BC | - |  | UG§1.11.5 | A1~A3；隐式动力不支持 | GFE-UserGuide |
| ① | 加速度约束荷载（节点级，时变正弦） | boundary type=4+amplitude |  | Explicit§6.3.2 | 节点随时间正弦变化的加速度约束 | GFE-Explicit |
| ① | 加速度荷载（幅值函数驱动） | - |  | Cases§9.3 | A1=1 × 预设地震波幅值函数 | GFE-Cases |
| ① | 加速度边界条件 | - |  | Explicit§3.1.3 | 节点加速度指定（算例 -0.1m/s²） | GFE-Explicit |
| ① | 动水压力（附加质量法） | - |  | UG§1.11.12 | Westgarrd（开阔，原文拼写）/Housner（封闭）；写在 inpx | GFE-UserGuide |
| ① | 压力荷载 | - |  | UG§1.11.7 | 表面集；支持空间分布 | GFE-UserGuide |
| ① | 压力荷载（面压力） | - |  | Explicit§3.1.5 | 仅 Surface 面；唯一时域+空间分布均支持的面荷载 | GFE-Explicit |
| ① | 压力（面分布压力） | - |  | Imp§4.1.3/§4.2.3 | 面分布压力 | GFE-Implicit |
| ① | 压力（面荷载） | - |  | Cases§1.1.3 | 必须先建表面集；数值+均匀分布+可"使用相对空间分布" | GFE-Cases |
| ① | 土层剪应力幅值（Amp-SX） | - |  | SSA§5.1.1 | 用 EERA 的 S 变量数据建空间分布剪应力幅值 | GFE-SSA |
| ① | 土层相对位移幅值（Amp-UX） | - |  | SSA§5.1.1 | EERA 位移数据须先减去结构最低点处位移再建幅值 | GFE-SSA |
| ① | 地震作用整体惯性力输入 | - |  | Iso§3.1图3.1.3/§5.1图5.1.3 p57-58 | 边界条件与荷载类型=惯性力，区域=(整个模型)，分量给 PGA(m/s²)，挂归一化幅值函数；空间分布=均匀（第五章中震 200gal→分量1=2） | GFE-Iso |
| ① | 地震动幅值函数预设 | - |  | UG§1.14 | 内置地震动预设一键生成幅值数据 | GFE-UserGuide |
| ① | 声源边界条件（正弦声压激励） | boundary type=11 声学+amplitude |  | Explicit§1.5.1-1.5.3 | x=0 端 100Hz 正弦声压 | GFE-Explicit |
| ① | 复数（虚部）边界值 | boundary.boundary |  | Cmd§2.10.1 | value_im + amplitude_im，用于复数分析（频响类） | GFE-Cmd |
| ① | 孔压荷载 | - |  | UG§1.11.13 | 仅 Soils 分析；支持空间分布 | GFE-UserGuide |
| ① | 孔压边界条件（沿坐标线性分布） | boundary type=16+distribution分布场 |  | Imp§1.5.1/§1.5.2 | 侧边施加随高度线性变化孔压（地表0→底部392 kPa） | GFE-Implicit |
| ① | 岩土构造二维应力 | - |  | UG§1.12.6 | Sigma1/Sigma3/水平夹角→换算应力(11,22,33,12) | GFE-UserGuide |
| ① | 幅值函数 | - |  | UG§1.14 | 表格输入/行复制粘贴/外部 txt 导入（逗号或空格分隔） | GFE-UserGuide |
| ① | 幅值函数/幅值函数2 字段 | - |  | Cases§5.3.1 | BC/荷载均挂幅值函数（默认"(瞬时)/(即时)"）；幅值函数2=复数荷载虚部、仅频响有效 | GFE-Cases |
| ① | 幅值函数创建与地震动导入 | - |  | SSA§3.1.8 | Amplitudes 双击创建，地震动可 txt 导入或手动录入 | GFE-SSA |
| ① | 幅值函数创建（表格/粘贴） | - |  | Cases§4.3.3 | 类型"表格"，时间-幅值逐行或整表粘贴 | GFE-Cases |
| ① | 幅值函数定义 amplitude | amplitude.amplitude |  | Cmd§2.12.1 | value 为平铺的 (x0,y0,x1,y1,...) 对；含 spectrum_type、gravity 谱参数 | GFE-Cmd |
| ① | 幅值函数管理器 | amplitude.amp_mgr |  | Cmd§2.12.3 | GFE.Pre.amplitude.amp_mgr() | GFE-Cmd |
| ① | 幅值函数类型（表格/平滑分析步/波谱） | amplitude.amplitude.type |  | Cmd§2.12.2 | type: 0=TABULAR, 4=SMOOTH_STEP, 6=SPECTRUM（编码不连续） | GFE-Cmd |
| ① | 幅值函数表格定义 | - |  | Iso§3.1截图/§5.1图5.1.3 p57-58 | 类型=表格，时间/频率/空间位置—幅值两列（示例 1001 行，dt=0.02s），可绘制预览 | GFE-Iso |
| ① | 幅值函数（x/y/z 三向波形指定） | amplitude+vibra_load.amp_bottom_x/y/z |  | FAQ§3.3 | 幅值函数节点；场地反应界面 x/y/z 各指定一条波（示例 WallLoad63 / 25_RH1TG025_(RenGong_T)） | GFE-FAQ |
| ① | 幅值函数（时间-幅值表 Amplitude） | - |  | Explicit§1.1 | 表格型加载历程；真实荷载=幅值曲线×比例系数 | GFE-Explicit |
| ① | 底部全约束边界 + 网格划分生成 FE 模型 | - |  | Iso§5.1 p56 | 结构底部全约束边界条件，划分网格后生成有限元分析模型（隔震案例节点 6014/单元 7883） | GFE-Iso |
| ① | 惯性力 | - |  | UG§1.11.8 | 默认作用整个模型，三分量；支持空间分布 | GFE-UserGuide |
| ① | 惯性力荷载（Type: Gravity + 空间分布幅值） | - |  | SSA§4.1.2(b)/§5.1.2(c) | Type=Gravity，Region=Whole Model，Component 1=1，Distribution=Y，Amplitude=Amp-AX，实现 | GFE-SSA |
| ① | 惯性力荷载（恒定/正弦时变） | - |  | Explicit§1.1.1.1 | 作用域=整体模型；⚠ 第1章按加速度（m/s²）给、§4.5 按力（kN）给，口径分裂见② | GFE-Explicit |
| ① | 惯性力（按加速度幅值指定） | - |  | Imp§1.1.1.2/§3.3/§4.1.4/§4.2.4 | 全模型体加速度型惯性荷载（量纲标注自相矛盾，见②） | GFE-Implicit |
| ① | 惯性力（自重） | - |  | Cases§1.2.3 | 类型"惯性力"，区域默认(整个模型)，分量3=-9.8，幅值(瞬时)，空间分布均匀 | GFE-Cases |
| ① | 温度初始条件 InitTemperature | initial_condition.InitTemperature |  | Cmd§2.11.7 | 可挂离散场 dis_field，value 为单浮点温度 | GFE-Cmd |
| ① | 温度荷载 | - |  | UG§1.11.16 | 仅静力+显式动力且核心须 GFEXN；材料须有膨胀系数 | GFE-UserGuide |
| ① | 离散场 | - |  | UG§1.13.2 | 按节点号/单元号给标量（或矩阵 6）系数 | GFE-UserGuide |
| ① | 空间分布幅值函数（加速度沿深度，Amp-AX） | - |  | SSA§4.1.1 | 创建 Amp-AX，把按空间升序排列的加速度-深度数据粘贴进幅值函数 | GFE-SSA |
| ① | 等效动水压力 | boundary type=15 水压力 |  | Explicit§3.1.10 | 流体密度+水位高度参数自动施加；无第三方基准 | GFE-Explicit |
| ① | 线荷载 | - |  | UG§1.11.9 | 仅线单元的单元集；三分量；时间+空间幅值 | GFE-UserGuide |
| ① | 线荷载（B31 梁单元） | - |  | Imp§4.1.7/§4.2.8 | 梁单元沿线分布荷载 | GFE-Implicit |
| ① | 线荷载（梁单元分布荷载/几何线集） | - |  | Explicit§3.1.11 | B31 梁线荷载；时域+空间✓ | GFE-Explicit |
| ① | 自由度位掩码设置 | boundary.boundary.valid_dof |  | Cmd§2.10.4 | valid_dof 6 位二进制，低→高 x,y,z,rx,ry,rz；1=开放、0=限制 | GFE-Cmd |
| ① | 节点流量荷载（注水/抽水） | boundary type=17 集中孔隙流 |  | Imp§1.5.1 | 指定节点设置流量载荷向土体注水 | GFE-Implicit |
| ① | 获取边界条件管理器 | boundary.bc_mgr |  | Cmd§2.10.5 | GFE.Pre.boundary.bc_mgr() | GFE-Cmd |
| ① | 表格型幅值函数支持负值与 >1 值 | - |  | Imp图5.5.2-2/5.5.3-2 p147-148 | 幅值列可取负（反向加载）和 2 倍值，非 0~1 归一化 | GFE-Implicit |
| ① | 表达式场 | - |  | UG§1.13.1 | X/Y/Z 连续函数；支持 (float)(条件)*(表达式) 分段；区分大小写 | GFE-UserGuide |
| ① | 表面孔隙流量 | - |  | UG§1.11.15 | 仅"土"分析步 | GFE-UserGuide |
| ① | 通用边界条件对象 | boundary.boundary |  | Cmd§2.10.1 | boundary()：name/set/type/valid_dof/value/amplitude/value_im/amplitude_im/distrib | GFE-Cmd |
| ① | 速度/角速度 BC | - |  | UG§1.11.4 | V1~VR3；隐式动力不支持 | GFE-UserGuide |
| ① | 速度约束荷载（节点级，时变正弦） | boundary type=3+amplitude |  | Explicit§6.3.1 | 节点随时间正弦变化的速度约束，含解析解对账 | GFE-Explicit |
| ① | 速度边界条件 | - |  | Explicit§3.1.2 | 节点速度指定（算例 1m/s） | GFE-Explicit |
| ① | 重力场预加载（斜坡幅值重力初始化） | - |  | Explicit§6.1.1 | 爆炸/动力分析前 1s 斜坡施加 -9.8m/s² 重力后保持 | GFE-Explicit |
| ① | 重力按惯性加速度荷载施加（方向可指定、可三向同时） | - |  | Explicit§9.1-9.3 | 重力以加速度幅值（9.8 或 980 m/s²）的惯性力荷载形式施加 | GFE-Explicit |
| ① | 重力荷载代表值=附加质量+自重质量 | import_yjk自动Comb_M+bc type=7重力 |  | FAQ§3.4 | 地震动力计算中以"Comb_M_xxx 附加质量+程序自动自重质量"形式考虑重力荷载代表值 | GFE-FAQ |
| ① | 集中力/力矩 | - |  | UG§1.11.6 | CF1~CF3+CM1~CM3+幅值函数 | GFE-UserGuide |
| ① | 集中力/力矩荷载 | - |  | Explicit§1.1.2.1 | 节点/几何点集集中力（静/动均可）；弯矩荷载见 §1.1.4 | GFE-Explicit |
| ① | 集中力（含虚部 Value(Imaginary)） | - |  | Cases§3.2.1 | 频响激励：虚部单位集中荷载 0,0,1,0,0,0 | GFE-Cases |
| ① | 集中力（节点/顶面静力） | - |  | Imp§1.1.x/§4.1.2/§4.2.2 | 节点集中静力 | GFE-Implicit |
| ① | 集中孔隙流量 | - |  | UG§1.11.14 | 仅"土"分析步 | GFE-UserGuide |
| ① | 非结构性质量 | - |  | UG§1.11.11 | 节点/单位长度/单位面积质量；须加在 Initial 步 | GFE-UserGuide |
| ① | 非结构性质量（节点附加质量） | - |  | Explicit§3.1.7; Imp§4.1.5/§4.2.5 | 节点附加质量参与惯性（算例 10t/节点）；时域/空间分布均✗ | GFE-Explicit+GFE-Implicit |
| ① | 面流载荷（抽水管井降水） | boundary type=18 表面孔隙流 |  | Imp§1.5.2 | 管井面上设面流（m/s），分阶段改流量 | GFE-Implicit |
| ① | 饱和度初始条件 InitSaturation | initial_condition.InitSaturation |  | Cmd§2.11.8 | saturation 单浮点 | GFE-Cmd |
| ② | *CFlux | - | bc枚举无热流量,改INP(热固耦合步) | UG附录二(4) p293 | 集中热流量，需热固耦合分析步，仅 C3D4，格式类似 Cload | GFE-UserGuide |
| ② | *Nonstructural Mass | - | bc枚举无此项,改INP *Nonstructural Mass | UG附录二(4) p292 | 非结构质量（均布），units=mass per length / mass per area | GFE-UserGuide |
| ② | *Temperature | - | bc type=14 标未使用,改INP *Temperature | UG附录二(4) p292 | 温度荷载，仅适用于含热膨胀系数的材料，可带 amplitude | GFE-UserGuide |
| ② | 温度荷载（含热膨胀系数） | - | bc温度type=14未用,荷载改INP *Temperature | Imp§4.2.6/§2.3 | 静力分析中节点温度+膨胀系数产生热变形；仅在静力荷载清单出现 | GFE-Implicit |
| ② | 温度荷载（含线膨胀系数） | - | 同温度荷载,改INP *Temperature | Explicit§3.1.9 | 整体温度荷载+膨胀系数热变形 | GFE-Explicit |

## D05 相互作用与约束（117 项：①115 ②2 ③0）

| 层 | 能力 | API入口 | 断点/理由 | 出处 | 说明 | 源手册 |
|---|---|---|---|---|---|---|
| ① | *Cohesive Behavior | contact.isCohesive+damage系列属性 |  | UG附录二(5) p295-296 | 接触粘聚行为；测试功能待完善，UI 上不支持 | GFE-UserGuide |
| ① | *Connector Behavior | - |  | UG附录二(5) p298 | 连接器行为容器（name 必要） | GFE-UserGuide |
| ① | *Connector Damping | - |  | UG附录二(5) p300 | 连接器阻尼，仅 nonlinear；type=VISCOUS 或 GFE DAMP2 | GFE-UserGuide |
| ① | *Connector Elasticity | - |  | UG附录二(5) p298-299 | 连接器弹性，GFE 自定义 definition=GFE ELA 支持拉压异性刚度 | GFE-UserGuide |
| ① | *Connector Hardening | - |  | UG附录二(5) p299-300 | 连接器硬化，A 类型仅 Half Cycle；GFE 扩展 GFE HDN2/GFE BW/GFE PEND | GFE-UserGuide |
| ① | *Connector Plasticity | - |  | UG附录二(5) p299 | 连接器塑性（component 必要） | GFE-UserGuide |
| ① | *Connector Section 连接器截面 | - |  | UG附录二(5) p298 | 连接器单元（CONN3d2）截面，类型仅 Catesian/Join/Rotation/Align 四种 | GFE-UserGuide |
| ① | *Contact Inclusions | - |  | UG附录二(5) p295 | 指定通用接触作用区域（两个表面集或 all exterior） | GFE-UserGuide |
| ① | *Contact Pair 面面接触 | - |  | UG附录二(5) p295 | 面-面接触对，引用 *Surface Interaction 名称 | GFE-UserGuide |
| ① | *Contact Property Assignment | - |  | UG附录二(5) p295 | 给通用接触区域指派接触属性（cohesive 区域特殊处理） | GFE-UserGuide |
| ① | *Contact 通用接触 | - |  | UG附录二(5) p294 | 通用接触总开关，目前只能位于 INP 顶层 | GFE-UserGuide |
| ① | *Conwep Charge Property | - |  | UG附录二(5) p297 | Conwep 装药属性，归属上方最近的 Incident Wave Interaction Property | GFE-UserGuide |
| ① | *Damage Evolution（接触） | - |  | UG附录二(5) p296 | 接触损伤演化，type=energy/softening=linear/power law | GFE-UserGuide |
| ① | *Damage Initiation（接触） | - |  | UG附录二(5) p296 | 接触损伤起始，criterion=quads | GFE-UserGuide |
| ① | *Dashpot 阻尼器 | - |  | UG附录二(5) p298 | 接地/两点阻尼（Dashpot1/Dashpot2/DashpotA），输入自由度+阻尼系数 | GFE-UserGuide |
| ① | *Embedded Element 嵌入区域 | - |  | UG附录二(5) p294 | 把单元集嵌入 host elset（如钢筋嵌入混凝土/桩嵌入土） | GFE-UserGuide |
| ① | *Friction 摩擦属性 | - |  | UG附录二(5) p296 | 摩擦系数（仅一位数据），紧邻 *Surface Interaction | GFE-UserGuide |
| ① | *Incident Wave Interaction Property | - |  | UG附录二(5) p297 | 冲击波属性，type 仅 air blast / surface blast | GFE-UserGuide |
| ① | *Incident Wave Interaction 冲击波 | - |  | UG附录二(5) p297 | 冲击波荷载（仅 conwep） | GFE-UserGuide |
| ① | *MPC 多点约束 | - |  | UG附录二(5) p294 | 多点约束，仅 BEAM 和 TIE 两类（见⑤待仲裁#2） | GFE-UserGuide |
| ① | *Rigid Body 刚体约束 | - |  | UG附录二(5) p294 | 刚体约束，从属区域须为 R3D3/R3D4 刚性单元 | GFE-UserGuide |
| ① | *Spring 弹簧 | - |  | UG附录二(5) p297 | 接地/两点弹簧（Spring1/Spring2/SpringA），输入自由度+刚度 | GFE-UserGuide |
| ① | *Surface Interaction | - |  | UG附录二(5) p295 | 接触属性容器（name 必要） | GFE-UserGuide |
| ① | *Tie 绑定约束 | - |  | UG附录二(5) p294 | 主从面绑定约束，可设 position tolerance 与 cyclic symmetry | GFE-UserGuide |
| ① | Connector 连接器行为（弹性/塑性、F1-F3/M1-M3） | connector_elastic/plastic component位掩码 |  | FAQ§3.24 | 连接器行为可按分量勾选刚度，抗拉/抗压刚度可不同（默认相等） | GFE-FAQ |
| ① | Coupling 耦合约束（参考点-节点组） | - |  | Imp§5.2.2 | 参考点带动节点组，参考点施加位移做静力 | GFE-Implicit |
| ① | GFE BW 连接器（Bouc-Wen 滞回） | connector_plastic kh_define=GFE BW |  | Explicit§4.7.2(2) | 增加屈服指数参数 | GFE-Explicit |
| ① | GFE DAMP2 连接器（F=C·V^exp 幂律阻尼） | connector_damping type=GFE DAMP2 |  | Explicit§4.7.1(2) | 阻尼系数 C+阻尼指数 exp，对标软件S | GFE-Explicit |
| ① | GFE HDN2 连接器（二折线位移型消能器） | connector_plastic kh_define=GFE HDN2 |  | Explicit§4.7.2(1) | 抗压刚度+屈服力+刚度折减系数 | GFE-Explicit |
| ① | GFE PEND 连接器（摩擦摆隔震支座 FPB） | connector_plastic kh_define=GFE PEND |  | Explicit§4.7.3(1) | 竖/横刚度+快慢摩擦系数+等效半径；须配竖向力 | GFE-Explicit |
| ① | GFE 内直接创建连接器（connector） | connector_section+behavior+set_name |  | Iso§2.2.1图2.2.1.3 | 右击【连接器】创建；三要素：连接器行为、局部坐标系、作用区域；对话框含平动类型(Cartesian)/转动类型(None)/有效分量(F1,F2,F3)/受约束 | GFE-Iso |
| ① | HALF CYCLE 连接器（铅芯橡胶支座 LRB） | connector_plastic kh_define=HALF CYCLE |  | Explicit§4.7.3(2) | 抗压刚度+（屈服力,塑性变形）多行表 | GFE-Explicit |
| ① | MPC 多点约束（点-点集） | - |  | Imp§5.2.1 | 梁交点位移协调，模态前10阶验证 | GFE-Implicit |
| ① | MPC 管理器 mpc_mgr() | interaction.mpc_mgr |  | Cmd§2.13.10 | 文档写 MPC_mgr()，示例为小写 mpc_mgr() | GFE-Cmd |
| ① | SPRING2 改为 SPRINGA（沿线弹簧） | spring_dashpot type位运算 springA=4 |  | FAQ§3.8-1 | 在 GFE 中可将两点弹簧改为沿线弹簧以兼容 ABAQUS 显式 | GFE-FAQ |
| ① | Tie 绑定约束（线-线、面-面） | - |  | Imp§5.1 | 两部件绑定，静力+模态双验证（模态差 2-3%，见②） | GFE-Implicit |
| ① | VISCOUS 连接器（阻尼力-速度列表型） | connector_damping type=VISCOUS |  | Explicit§4.7.1(1) | F-V 数据表定义黏滞阻尼，对标软件A | GFE-Explicit |
| ① | 两点弹簧/阻尼 | - |  | UG§1.10.7b | 点对批量添加；轴向"沿线方向"或"固定方向" | GFE-UserGuide |
| ① | 两节点连接器单元动力分析 | connector全API+动力分析步 |  | Explicit§4.7 | 上下两节点（距1m）+连接器体系 | GFE-Explicit |
| ① | 共节点建模策略（免相互作用） | - |  | Cases§2.2.1 | 布尔合并/分割印刻实现共节点，免接触、免独立网格尺寸控制 | GFE-Cases |
| ① | 冲击波属性 | - |  | UG§1.10.5 | 空气爆破 CONWEP：TNT 等效质量+四个单位转换系数 | GFE-UserGuide |
| ① | 冲击波（CONWEP 爆炸） | - |  | UG§1.10.5 | 源点+作用表面+属性+起爆时间+数值放缩；镜像冲击波为测试功能 | GFE-UserGuide |
| ① | 刚体单元/刚性壳 | - |  | Explicit§4.4.1 | 四边形刚体单元，参考点输出 RF | GFE-Explicit |
| ① | 刚体管理器 rigid_mgr() | interaction.rigid_mgr |  | Cmd§2.13.6 | 获取刚体管理器 | GFE-Cmd |
| ① | 刚体约束 | - |  | UG§1.10.2 | 区域随参考点运动；需给密度、厚度 | GFE-UserGuide |
| ① | 刚体约束 rigid_body | interaction.rigid_body |  | Cmd§2.13.5 | type 0=单元集 1=表面集；ref_node 为整型节点编号 | GFE-Cmd |
| ① | 刚体约束、弹簧约束 | rigid_body+spring_dashpot |  | Imp第五章引言/§5.4 p143-145 | 章首列举，表5 未列适用范围 | GFE-Implicit |
| ① | 刚体约束（刚性面+参考点） | - |  | Imp§5.4 p143-145 | 悬臂板右侧刚性面与参考点定义刚体约束，参考点加位移载荷静力验证；与 Coupling 算例同几何同载荷，结果等效（均 5.001E-01 m） | GFE-Implicit |
| ① | 刚体约束（参考点主控点+从属单元集） | rigid_body.ref_node+set_name |  | Explicit§4.5 | 顶面中心参考点主控、从属域为顶面单元集 | GFE-Explicit |
| ① | 创建局部坐标系（相互作用-坐标系） | - |  | Cases§15.12.1 | 树"相互作用—坐标系"双击创建；类型=矩形、定义=坐标，原点+点1+点2 三点定义，供连接器引用 | GFE-Cases |
| ① | 创建连接器（Cartesian+Rotation） | - |  | Cases§15.12 | 选平动类型/转动类型、绑定连接器行为、点1/点2 局部坐标系 | GFE-Cases |
| ① | 地基弹簧（Springs/Dashpots） | interaction.spring_dashpot |  | SSA§5.1.2(b)/§5.2 | 双击【Springs/Dashpots】，设弹簧类型、施加区域、方向、刚度；案例为法向+切向地基弹簧 | GFE-SSA |
| ① | 地连墙绑定约束自动生成 | contact_pair.search_face+surface_pair批量 |  | UG§1.18.13 | 勾"地连墙"选几何后自动生成地连墙与主体结构间绑定约束 | GFE-UserGuide |
| ① | 坐标系管理器 | orientation.orientation_mgr |  | Cmd§2.19.2 | manager() 或 orientation_mgr() | GFE-Cmd |
| ① | 多点约束 mpc | interaction.mpc |  | Cmd§2.13.9; Explicit§4.2; UG§1.10.4 | type: 0=梁, 1=tie, 2=耦合；ref_node 为字符串（集合名） | GFE-Cmd+GFE-Explicit+GFE-UserGuide |
| ① | 局部坐标系 orientation | orientation.orientation |  | Cmd§2.19.1 | type 0=矩形 1=圆形；data 9 元素 [p1×3, p2×3, origin×3] | GFE-Cmd |
| ① | 嵌入区域 | - |  | UG§1.10.3 | 钢筋嵌入混凝土、土钉加固；舍入容差+外部容差 | GFE-UserGuide |
| ① | 嵌入区域（Embedded region） | - |  | Cases§2.2.7 | 嵌入区域=被嵌构件、主区域=容纳体；默认舍入容差 1e-06、外部容差 0.05 | GFE-Cases |
| ① | 嵌入管理器 embed_mgr() | interaction.embed_mgr |  | Cmd§2.13.8 | 获取嵌入管理器 | GFE-Cmd |
| ① | 嵌入约束 Embedded | - |  | Explicit§4.3 | 仅线→面/线→体/面→体/体→体（算例壳嵌入实体） | GFE-Explicit |
| ① | 嵌入约束 Embedded（线→面/线→体/面→体/体→体）+ 模态验证 | - |  | Imp§5.3/§5.3.2 p141-143 | 壳体嵌入实体（9345 节点算例），静力+模态（前三阶差<0.2%）；补块给出静力表 5.3.1-1 + 模态表 5.3.2-1 完整值（见③3.10） | GFE-Implicit |
| ① | 嵌入约束 embed | interaction.embed |  | Cmd§2.13.7; SSA§3.1.6(2) | host_name 主域 + embedded_names 列表；双容差 roundoff_tolerance/exterior_tolerance | GFE-Cmd+GFE-SSA |
| ① | 弹簧阻尼器 spring_dashpot | interaction.spring_dashpot |  | Cmd§2.13.15 | type 位运算组合：spring1=1, spring2=2, springA=4, dashpot1=8, dashpot2=16, dashpotA=32 | GFE-Cmd |
| ① | 弹簧阻尼器管理器 | interaction.spring_dashpot_manager |  | Cmd§2.13.16 | spring_dashpot_manager() | GFE-Cmd |
| ① | 接地弹簧/阻尼 | - |  | UG§1.10.7a | 单节点弹簧，选自由度+刚度/阻尼系数 | GFE-UserGuide |
| ① | 接地弹簧（拉压异性） | special_interaction type=1 |  | Imp§5.5.1 p145-146 | X/Y/Z 三向各设抗拉刚度+抗压刚度共 6 值；隐式动力+静力双验证 | GFE-Implicit |
| ① | 接触定义 contact | interaction.contact |  | Cmd§2.13.3 | type 0=通用接触 1=表面到表面；friction 摩擦系数；isCohesive 粘性接触含 damageInitiation/damageEvolut | GFE-Cmd |
| ① | 接触管理器 contact_mgr() | interaction.contact_mgr |  | Cmd§2.13.4 | 获取接触管理器 | GFE-Cmd |
| ① | 接触边自动搜索 search_edge | contact_pair.search_edge |  | Cmd§3.2.2 | 同上，搜索接触边 | GFE-Cmd |
| ① | 接触面自动搜索 search_face | contact_pair.search_face |  | Cmd§3.2.1 | 在两几何体间按容差搜索接触面对，返回（主面集合,从面集合）对列表，元素为 (面ID, 侧面) | GFE-Cmd |
| ① | 接触（通用/面对面） | - |  | UG§1.10.6 | 选类型、区域、摩擦系数 | GFE-UserGuide |
| ① | 搜索土-结接触、自动创建绑定约束 | search_face+surface_pair |  | FAQ§3.25 | 自动搜索土-结构接触面并自动生成表面集与 Tie | GFE-FAQ |
| ① | 搜索接触 | contact_pair.search_face/search_edge |  | UG§1.17.2 | 按容差自动查找接触对，自动生成表面集+tie 绑定（绑定/只压/无） | GFE-UserGuide |
| ① | 搜索接触（批量生成绑定） | search_face循环+tie_mgr.add |  | Cases§4.2.2 | 通用—搜索接触：查找区域+容差（案例 0.01）→自动列 CP-* 接触对→"添加为绑定"生成 Tie-N；结果表逐行配置 类型(相互作用)/滑移(有限)/添加 | GFE-Cases |
| ① | 桩-筏板 embedded（嵌固）连接 | interaction.embed |  | FAQ§3.8-2 | 导入时桩与筏板分别导入、线单元对面单元面外嵌固，提高筏板网格质量 | GFE-FAQ |
| ① | 特殊相互作用 special_interaction | interaction.special_interaction |  | Cmd§2.13.24 | type: 1=GroundSpring_Anisotropy, 2=Tie_OnlyCompress（仅压法向、切向自由）, 3=Tie_OnlyCompre | GFE-Cmd |
| ① | 特殊相互作用族总入口（共 5 种） | special_interaction type+parameters |  | Imp§5.5 p145 | GUI「创建特殊相互作用」对话框，5 种类型；均经主从面（PickedSurf）定义 | GFE-Implicit |
| ① | 特殊相互作用族（目录预告：接地弹簧/只压不拉绑定×2/附材料属性绑定/三向刚度绑定） | special_interaction type 1-4+parameters |  | Imp§5.5目录行168-174 | 已于 P1.5 经 PDF 直读补齐 p145-150（见 J 表#96-#101，正文确为 5 种） | GFE-Implicit |
| ① | 特殊相互作用管理器 spec_mgr() | interaction.spec_mgr |  | Cmd§2.13.25 | 获取特殊相互作用管理器 | GFE-Cmd |
| ① | 特殊绑定①：法向只压不拉+切向无作用 | special type=2 Tie_OnlyCompress |  | Explicit§4.8.1 | 显式求解器特殊相互作用，主面红色高亮指定 | GFE-Explicit |
| ① | 特殊绑定②：法向只压不拉+切向绑定 | special type=3 Tie_OnlyCompress_Normal |  | Explicit§4.8.2 | 同上变体 | GFE-Explicit |
| ① | 特殊绑定③：附带材料属性的绑定 | special type=4 Tie_Material |  | Explicit§4.8.3 | 界面携材料属性，与 TIE 云图对照 | GFE-Explicit |
| ① | 特殊绑定④：三向刚度可指定（含 config 参数） | special_interaction.parameters可设 |  | Explicit§4.8.4 | 三方向刚度独立设定；config 仅 GUI 截图无文字说明 | GFE-Explicit |
| ① | 相互作用类型体系 | - |  | Cases§2.2.7 | 树状"相互作用"节点下全家桶 | GFE-Cases |
| ① | 线-体嵌固（桩嵌入土） | embed host_name+embedded_names |  | FAQ§3.19 | 桩（线单元）嵌入土（体单元），但不约束转动自由度 | GFE-FAQ |
| ① | 绑定管理器 tie_mgr() | interaction.tie_mgr |  | Cmd§2.13.2 | 获取绑定管理器 | GFE-Cmd |
| ① | 绑定约束 Tie（主从面设置） | surface_pair type=0+tie_mgr |  | FAQ§4.13 | Tie 主从面可设；三维土-结土做主面，二维平面应变结构做主面 | GFE-FAQ |
| ① | 绑定约束 Tie（修订记录线索） | surface_pair+tie_mgr |  | FAQ修订记录 | 指向 §4.13，仅作能力线索不计入能力总数 | GFE-FAQ |
| ① | 绑定约束（Tie） | - |  | Cases§4.2.1; Explicit§4.1; UG§1.10.1 | 土-结/厂房-保护壳界面默认连接方式；单选/shift 多选红色/灰色高亮查看 | GFE-Cases+GFE-Explicit+GFE-UserGuide |
| ① | 绑定约束（三向刚度可指定） | - |  | Imp§5.5.5 p149-150 | INP 关键字 *Custom Property type=5，6 参数序=法向/侧向/侧向刚度+法向/侧向/侧向阻尼（逐字见③3.10） | GFE-Implicit |
| ① | 绑定约束（法向只压不拉、切向无作用） | special type=2 |  | Imp§5.5.2 p146-147 | 主从面法向只传压不传拉、切向自由滑动；负幅值先拉后压验证；隐式动力+静力 | GFE-Implicit |
| ① | 绑定约束（法向只压不拉、切向绑定） | special type=3 |  | Imp§5.5.3 p148 | 同上但切向位移绑定（切向位移 0.1 m 工况）；隐式动力+静力 | GFE-Implicit |
| ① | 耦合约束 coupling（参考点主控点+从属面） | mpc type=2 耦合 |  | Explicit§4.6 | 与 §4.5 算例完全同构，独立功能 | GFE-Explicit |
| ① | 自动查找 Tie 接触对（Find Contact；2D"查找几何边"/3D"查找几何面"） | search_edge/search_face |  | SSA§3.1.6(1)/§6.1 | Search Domain 四种选择方式，自动搜索土-结构间接触并建绑定约束；2D/3D 命令异名 | GFE-SSA |
| ① | 表面绑定（Tie）surface_pair | interaction.surface_pair |  | Cmd§2.13.1 | type=0 绑定；parameters[0] 为位置容差 | GFE-Cmd |
| ① | 连接器 | - |  | UG§1.10.9 | 连接类型（Cartesian/Align/Join/Rotation 等）+行为+局部坐标系；两集合间自动搜索最近点配对 | GFE-UserGuide |
| ① | 连接器区域手动指定 | connector_section.set_name |  | Cases§15.12 | 区域另两种方式：几何集/节点集、从窗口中拾取 | GFE-Cases |
| ① | 连接器塑性行为 connector_plastic | interaction.connector_plastic |  | Cmd§2.13.19 | kh_define 取 HALF CYCLE / GFE HDN2 / GFE BW / GFE PEND（含 GFE 自有滞回模型） | GFE-Cmd |
| ① | 连接器局部坐标系创建 | orientation+connector_section.orientation |  | Iso§2.2.1图2.2.1.11 | 【坐标系】类型=矩形、定义=坐标：原点+点1(=局部X)+点2(=局部Y)，X×Y 叉乘得 Z；选中连接器/坐标系可在图形区左上角预览方向 | GFE-Iso |
| ① | 连接器属性管理器 | interaction.connector_property_manager |  | Cmd§2.13.23 | connector_property_manager() | GFE-Cmd |
| ① | 连接器属性（截面）connector_section | interaction.connector_section |  | Cmd§2.13.22 | connector_type 为（平移,旋转）类型对：NONE=-1, CARTESIAN=0, JOIN=1, LINK=2, ROTATION=3, Ali | GFE-Cmd |
| ① | 连接器弹性行为 connector_elastic | interaction.connector_elastic |  | Cmd§2.13.18 | 按 component 位掩码逐自由度给压缩/拉伸刚度（列表） | GFE-Cmd |
| ① | 连接器行为 | - |  | UG§1.10.8 | 弹性（6DOF 可设刚性）、塑性（GFE HDN2/HALF CYCLE/GFE BW/GFE PEND）、阻尼（VISCOUS/GFE_DAMP2） | GFE-UserGuide |
| ① | 连接器行为-弹性 | - |  | Cases§15.12 | 树"相互作用→连接器行为"，左栏右键添加"弹性"，勾选分量 F1/F2/F3（或 M1/M2/M3）逐分量填抗压刚度 | GFE-Cases |
| ① | 连接器行为-阻尼（GFE DAMP2） | - |  | Cases§15.12 | 同对话框左栏切"阻尼"，类型下拉选 GFE DAMP2，逐分量填阻尼系数+阻尼指数 | GFE-Cases |
| ① | 连接器行为容器 connector_behavior | interaction.connector_behavior |  | Cmd§2.13.17 | 行为通过管理器绑定到名称 | GFE-Cmd |
| ① | 连接器行为管理器 | interaction.connector_behavior_manager |  | Cmd§2.13.21 | connector_behavior_manager() | GFE-Cmd |
| ① | 连接器行为附加选项 | connector_behavior.behaviors列表 |  | Cases§15.12 | 弹性页"刚性约束"与"抗拉刚度"两个复选框（本例均不勾；抗拉默认=抗压） | GFE-Cases |
| ① | 连接器行为（ConnBehavior）创建 | connector_behavior+conn_beh_mgr |  | Iso§2.2.1 | 右击【连接器行为】，对话框空白处右击添加【弹性】/【阻尼】/【塑性】子参数块，按器件类型组合 | GFE-Iso |
| ① | 连接器阻尼行为 connector_damping | interaction.connector_damping |  | Cmd§2.13.20 | type 取 VISCOUS / GFE DAMP2 | GFE-Cmd |
| ① | 通用接触 Contact（面-面） | - |  | Imp表5(L7815) | 面-面接触相互作用（仅表5 列出适用范围，本册无验证正文） | GFE-Implicit |
| ① | 通用接触（面-面，法向硬接触+切向摩擦） | - |  | Explicit§4.4 | 大规模通用接触（验证至 87 万节点） | GFE-Explicit |
| ① | 钢板/钢筋/拉结钢构件嵌入混凝土（Embedded 工程级应用） | interaction.embed |  | Explicit§10.2 | "利用嵌入实现了混凝土和钢材的位移协调"——钢混协同用嵌入而非绑定/接触（既有能力 #66 的工程级应用） | GFE-Explicit |
| ① | 钢筋嵌入混凝土（节点分析） | interaction.embed |  | FAQ§3.26 | 钢筋几何嵌入混凝土体，建议先合并钢筋为单一几何体 | GFE-FAQ |
| ① | 附带材料属性的绑定约束（界面可变形） | special type=4 Tie_Material |  | Imp§5.5.4 p149 | 界面绑定带材料属性，与纯 TIE 云图对比；算例用显式动力分析步，隐式适用性未验证 | GFE-Implicit |
| ② | 特殊相互作用（5 种） | - |  | UG§1.10.10 | 拉压异性接地弹簧、只压不拉 Tie×2、附带材料 Tie、三向刚度 Tie；写出在 inpx | GFE-UserGuide |
| ② | 连接器区域自动搜索配对 | - | 无配对API,find_near_node自实现搜索 | Cases§15.12 | 区域=自动搜索+节点集：遍历集合-2 各点找集合-1 最近点，逐对自动建连接器 | GFE-Cases |

## D06 分析步与求解控制（137 项：①118 ②16 ③3）

| 层 | 能力 | API入口 | 断点/理由 | 出处 | 说明 | 源手册 |
|---|---|---|---|---|---|---|
| ① | "线性计算"模式 | dynamic_implicit_step.gfe_linear |  | Imp§4.1 | 将材料设为线性，刚度矩阵只计算一遍（静默线性化，见②） | GFE-Implicit |
| ① | "非线性计算"模式 | - |  | Imp§4.1 | 迭代求解非线性方程组 | GFE-Implicit |
| ① | *Coupled Temperature-Displacement 热固耦合 | - |  | UG附录二(6) p305 | 稳态热固耦合：先纯热分析再显式动力分析（GFE 特有两段式实现）；有使用限制，详见实际案例手册 | GFE-UserGuide |
| ① | *Dynamic 动力分析（显式/隐式） | - |  | UG附录二(6) p300-301 | 带 Explicit 为显式，否则隐式；显式步长由质量缩放控制 | GFE-UserGuide |
| ① | *Frequency 模态分析 | - |  | UG附录二(6) p301 | 模态分析步，数据行仅第一位=模态阶数 | GFE-UserGuide |
| ① | *Geostatic 地应力平衡 | - |  | UG附录二(6) p304 | 地应力平衡分析步，数据行同 *Static | GFE-UserGuide |
| ① | *Global Damping 全局阻尼 | - |  | UG附录二(6) p304 | 频响分析的全局 Rayleigh 阻尼（alpha, beta） | GFE-UserGuide |
| ① | *Modal Damping 振型阻尼 | - |  | UG附录二(6) p302-304 | 模态阻尼，type 仅 direct/rayleigh，definition 仅 mode | GFE-UserGuide |
| ① | *Modal Dynamic 模态动力分析 | - |  | UG附录二(6) p301 | 振型叠加法时程分析，前置步必须是模态分析 | GFE-UserGuide |
| ① | *Model Change 生死单元 | - |  | UG附录二(6) p300 | 单元激活/移除（add 与 remove 互斥），归属 *Static | GFE-UserGuide |
| ① | *Response Spectrum 反应谱分析 | - |  | UG附录二(6) p302 | 反应谱分析步，读前五位（谱名+xyz方向余弦+放缩系数） | GFE-UserGuide |
| ① | *Spectrum 反应谱定义 | - |  | UG附录二(6) p302 | 反应谱曲线，type=acceleration/velocity/displacement，三位数据多行 | GFE-UserGuide |
| ① | *Static 静力分析 | - |  | UG附录二(6) p300 | 静力分析步，数据行四位目前均未实际使用但必须填 | GFE-UserGuide |
| ① | *Steady State Dynamics 频响分析 | - |  | UG附录二(6) p302 | 频响分析，direct 参数=直接法，否则模态法 | GFE-UserGuide |
| ① | *Step 分析步 | - |  | UG附录二(6) p300 | 分析步容器，name+nlgeom，必须配 *End Step | GFE-UserGuide |
| ① | *Variable Mass Scaling 质量缩放 | - |  | UG附录二(6) p301 | 对稳定步长小于 dt 的单元做质量缩放，并把迭代步长固定为 dt | GFE-UserGuide |
| ① | *Visco 粘弹性静力分析 | - |  | UG附录二(6) p304 | 考虑粘弹性的静力分析，数据行同 *Static | GFE-UserGuide |
| ① | 中震弹性 / 大震弹塑性分析工况（隔震案例） | - |  | Iso§5.1/§5.3/§5.4 p57 | 隔震案例分别以 200gal（中震弹性）/400gal（大震弹塑性）峰值惯性力做两个独立分析 | GFE-Iso |
| ① | 二阶四面体大规模接触求解 | - |  | Explicit§4.4.1-4.4.2 | 二阶四面体+刚体接触显式计算 | GFE-Explicit |
| ① | 作业全生命周期管理 | - |  | Cases§1.3.2 | 编辑/复制/删除/提交/监控/中断/结果（后三者提交后可用） | GFE-Cases |
| ① | 作业创建 | - |  | Cases§1.3.1 | 字段：作业名称/模型名称/工况/目录/前置的DB/计算核心/GPUID/"高级>>"/"移除单元>>" | GFE-Cases |
| ① | 作业管理器 | - |  | UG§1.15.4 | 创建/编辑/复制/删除/写 INP/提交/监控/结果/中断；前置 DB、计算核心、GPUID | GFE-UserGuide |
| ① | 作业高级写出选项 | - |  | UG§1.15.4(5) | 写出 Vuel（人工边界单元入 inp+vload）；列车荷载写 inpx（默认）；写 SPH xml | GFE-UserGuide |
| ① | 全局瑞利阻尼（*Global Damping） | - |  | Imp§6.1/§6.1.1-6.1.4 p152-158 | 全模型统一 α+β，INP 关键字逐字明示（alpha=1.5,beta=0.0001）；配模态动力/Newmark/直接法频响/振型叠加频响四类验证 | GFE-Implicit |
| ① | 全局结构阻尼（*global damping, structural=） | - |  | Imp§6.2/§6.2.1 p159-160 | 刚度阵引入迟滞型阻尼项，系数 0.05 算例；仅线性系统小振动适用 | GFE-Implicit |
| ① | 全局阻尼 global_damping | step.global_damping |  | Cmd§2.14.10 | alpha/beta Rayleigh 阻尼 + structural 结构阻尼 + field 场类型 | GFE-Cmd |
| ① | 几何非线性开关 | - |  | Cases§6.11.1 | "决定是否引入大位移非线性，并将影响到随后的分析步"；显式动力步默认=关闭 | GFE-Cases |
| ① | 几何非线性开关（nlgeom，工况级） | - |  | Explicit§1.1.4 | 线性/几何非线性是独立工况设置，非自动判断 | GFE-Explicit |
| ① | 分析步插入位置控制 | - |  | Cases§1.2.5 | "后面插入新的计算步"+参照步决定步序 | GFE-Cases |
| ① | 分析步管理器 step_manager() | step.step_manager |  | Cmd§2.14.14 | 小节标题误写为「获取连接器属性管理器」，实为分析步管理器 | GFE-Cmd |
| ① | 分析步类型库（含热-固耦合分析） | - |  | Cases§15.14 | 创建对话框类型列表可辨：显式动力/静力/静力(地应力平衡)/隐式动力/热-固耦合分析（另一项被高亮遮挡未辨清）；程序=通用 | GFE-Cases |
| ① | 分析步级阻尼页签（全局阻尼/振型阻尼双复选框） | step.global_damping+modal_damping |  | Imp图6.1.1-3等 p153-169 | 频响/模态动力/反应谱分析步均带「阻尼」页签：α、β、Structural 三并列字段 + 模态区间表（起始模态/截止模态/参数），行数可增 | GFE-Implicit |
| ① | 分析步设置（静力通用/动力显式） | static_general_step/dynamic_explicit_step |  | SSA§3.1.4 | Steps 右键创建；二维横断面动力时程分析应选动力显式 | GFE-SSA |
| ① | 前置 DB 链接（静→动接力，-prevdb） | - |  | Cases§2.3.1 | "前置的DB"字段链接前序分析结果 | GFE-Cases |
| ① | 动态模态阻尼 dyn_modal_damping | step.dyn_modal_damping |  | Cmd§2.14.13 | 从数据库 db + set_name 取模态，values 给阻尼比列表 | GFE-Cmd |
| ① | 单元生死/施工阶段分析总功能 | case.set_elemAdd/set_elemDel |  | Imp第七章 p176-190/§7.5 p190 | 8 种单元（C3D4/C3D8/S3R/S4R/B31/B21/CPE3/CPE4）单元生死验证，证实 GFEXN 施工阶段分析可行；全章无任何 INP 关键字 | GFE-Implicit |
| ① | 单元生死开挖 idiom | case.set_elemDel |  | Cmd§8.2 | set_elemDel('Static-N', ['kaiwaN'])，传几何集名按分析步移除单元 | GFE-Cmd |
| ① | 反应谱分析步 | - |  | UG§1.15.1(8) | 仅单方向激励+绝对值求和；SRSS/CQC 在后处理自定义场做 | GFE-UserGuide |
| ① | 反应谱分析步 response_spectrum_step | step.response_spectrum_step |  | Cmd§2.14.7 | sum 求和类型（示例 1=SRSS）、spectrum 谱类型、data 数据 | GFE-Cmd |
| ① | 反应谱分析（输入加速度谱） | response_spectrum_step+amplitude谱 |  | Imp§3.5.1 | X 向加速度谱输入，与软件A 0.00% 吻合 | GFE-Implicit |
| ① | 发散定位流程（逐帧场输出） | - |  | FAQ§4.3 | 总时长改 0.02s、全模型场输出、频率 0.001s，逐帧查最大位移节点定位发散 | GFE-FAQ |
| ① | 命令行无 GUI 提交计算（daemon 模式） | - |  | FAQ§5.3 | `gfe -daemon -dat INP路径 -gfedir 结果目录` 直接驱动求解器，绕过 PrePo GUI | GFE-FAQ |
| ① | 地应力分析步 geo_static_step | step.geo_static_step |  | Cmd§2.14.5 | 地应力平衡步，增量参数同静力步 | GFE-Cmd |
| ① | 地应力平衡分析 | - |  | Imp§1.5.1/§1.5.2 | 渗流/开挖分析第一步均为地应力平衡步 | GFE-Implicit |
| ① | 基坑开挖范式（单元杀死） | case.set_elemDel(步名,集名) |  | Imp§7.1 p176-179/§7.4 p187-190 | 实体/平面应变单元，线弹性+自重+底固，两分析步逐步挖除 | GFE-Implicit |
| ① | 多 GPU 卡并行求解 | - |  | FAQ§5.3 | 支持多卡并行，nvidia 显卡，卡间互联建议 nvlink | GFE-FAQ |
| ① | 多分析步序列定义（每步改变模型拓扑） | - |  | Imp§7.1-7.4 p176-190 | 全部算例"分两个分析步进行施工模拟"，每步一次单元增/删 | GFE-Implicit |
| ① | 小震弹性 / 大震弹塑性时程分析 | gfe_linear开关+材料/分析步全API |  | Iso§2.1/§3.3/§3.4 | 同一模型分别以 70gal / 400gal 幅值跑弹性与弹塑性时程 | GFE-Iso |
| ① | 工况 setter 式配置 | case.set_bcs |  | Cmd§8.1 | case 对象 set_bcs/set_initialConditions/set_fieldReqs/set_histReqs/set_elemAdd/set | GFE-Cmd |
| ① | 工况与荷载组合（Dead/Live/Comb 等） | case_mgr组装+YJK命名约定 |  | FAQ§3.1 | 模型树含工况节点（Dead、Live、屋面活、消防车等）与组合 Comb | GFE-FAQ |
| ① | 工况创建与按分析步组装 | - |  | Cases§1.2.6 | 左侧"所有组"对象池→选中右侧分析步→"+/-"挂入；BC 挂 Initial、荷载/输出挂计算步；作业以工况为提交单位 | GFE-Cases |
| ① | 工况定义（含生死单元） | - |  | UG§1.15.3 | 激活组装配分析步/BC/输出；分析步内"生死单元-添加/移除"集合 | GFE-UserGuide |
| ① | 工况管理器 | case.case_mgr |  | Cmd§2.21.2 | manager() 或 case_mgr()；示例用 case_mgr().add(obj) 注册工况 | GFE-Cmd |
| ① | 工况组装 case | case.case |  | Cmd§2.21.1 | steps 步序列 + 按步映射 bcs/initialConditions/vload/artbc/fieldReqs/histReqs；elemAdd/el | GFE-Cmd |
| ① | 工况设置（Cases） | case+set_bcs等setter |  | SSA§3.1.10 | 提交计算前设置计算工况；非线性需在动力步前加重力静力步 | GFE-SSA |
| ① | 弹塑性三段式工况 | - |  | Cases§10.22 | Initial→静力步（AllGrav+静力边界）→动力步（再挂 AllGrav 地应力平衡+弹塑性输出） | GFE-Cases |
| ① | 批处理命令提交计算 | - |  | FAQ§4.1 | 命令行批处理提交 inp 计算（需 inpx 文件同路径） | GFE-FAQ |
| ① | 批处理提交 | PrePo.exe -daemon |  | Cases§5.3.3; UG§1.15.4(6) | PrePo.exe -daemon -dat -gfedir … 全参数表 | GFE-Cases+GFE-UserGuide |
| ① | 批处理提交分析（PrePo.exe -daemon -dat + tmp-soils） | PrePo.exe -daemon |  | Imp§1.5.3 | bat 循环对 .inp 调 PrePo.exe，尾缀 tmp-soils 激活纯渗流 | GFE-Implicit |
| ① | 振型叠加法动力分析步（GUI 类型名「模态动力分析」ModalDyn） | - |  | Imp§6.1.1 p152-154/§6.3.1/§6.4.1 | 既有 #67 的 GUI 实名确认 + 阻尼配置验证 | GFE-Implicit |
| ① | 振型瑞利阻尼（*Modal Damping, rayleigh） | - |  | Imp§6.4/§6.4.1-6.4.2 p166-169 | 数据行 4 列 起始阶,截止阶,α,β；仅振型叠加类分析 | GFE-Implicit |
| ① | 振型阻尼比（*Modal Damping） | - |  | Imp§6.3/§6.3.1-6.3.3 p161-166 | 数据行 3 列 起始阶,截止阶,ζ（区间语义）；用于模态动力/振型叠加频响/反应谱三类分析步 | GFE-Implicit |
| ① | 施工助手 | - |  | Cases§7.3.3; UG§1.18.7 | 选几何集（支持正则 `floor.*All$`）→按中心/最低点/最高点沿 X/Y/Z 排序→批量生成各分析步生死单元；二次打开可批量加场输出 | GFE-Cases+GFE-UserGuide |
| ① | 施工工况（多静力步序列） | - |  | Cases§6.11 | GeoStatic→放坡→逐层开挖/逐层施工，重力只在第一个静力步挂一次 | GFE-Cases |
| ① | 施工阶段分析（目录预告：支持单元 C3D4/C3D8/S3R/S4R/B31/B21/CPE3/CPE4） | case.set_elemAdd/Del |  | Imp第七章目录行212-234 | 已于 P1.5 经 PDF 直读补齐 p176-190（见 L 表#113-#117）；正文证实壳单元确名 S3R/S4R | GFE-Implicit |
| ① | 施工阶段批量添加/移除 add_stage | geotool.add_stage |  | Cmd§3.4.12(2) | 把排序后的项按 begin+inc 阶段编号批量挂入/移出工况 | GFE-Cmd |
| ① | 施工阶段项排序 sort_stage_items | geotool.sort_stage_items |  | Cmd§3.4.12(1) | 按坐标(中心/最低/最高点 × X/Y/Z 分量)对几何集/单元集/边界条件排序并去重 | GFE-Cmd |
| ① | 显式动力分析步 | - |  | Cases§2.2.6; UG§1.15.1(3) | 程序"通用"下与静力并列；爆炸案例分析时间 1s、列车案例 15s；编辑对话框含 基本/质量缩放/阻尼 三页签 | GFE-Cases+GFE-UserGuide |
| ① | 显式动力分析步 dynamic_explicit_step | step.dynamic_explicit_step |  | Cmd§2.14.3 | period + mass_scaling 列表 + 可选 modal_damping（官方示例自带 bug，见②） | GFE-Cmd |
| ① | 显式动力分析（DynamicStep） | - |  | FAQ§3.1 | 含短时(1s)试算诊断流程 | GFE-FAQ |
| ① | 显式动力时程分析 | step.dynamic_explicit_step |  | Explicit全书动力小节 | 正弦惯性力/任意荷载时程的时域响应 | GFE-Explicit |
| ① | 显式拟静力分析（斜坡缓慢加载求静力解） | - |  | Explicit§1.1.3.1 | 非线性本构的"静力"结果只能由显式斜坡加载（1s-60s 量级）获得 | GFE-Explicit |
| ① | 模态分析 + YJK 周期/质量对账 | frequency_step+db直读对账 |  | Iso§3.2/§4.2/§5.2表5.2 p58 | GFE 与 YJK 自振周期、Uz 质量对比验证模型一致性（隔震案例同口径：前三阶周期 + 质量 Uz/kN） | GFE-Iso |
| ① | 模态分析步 | - |  | UG§1.15.1(5) | （手册仅图示） | GFE-UserGuide |
| ① | 模态分析步 frequency_step | step.frequency_step |  | Cmd§2.14.2 | eigen 特征值数量 | GFE-Cmd |
| ① | 模态分析步（线性摄动） | - |  | Cases§1.2.5 | 程序"线性摄动"→模态分析 | GFE-Cases |
| ① | 模态分析（含附加质量统计） | - |  | FAQ§3.1 | 查局部振动异常、取第一模态频率；模态总质量=附加质量+自重质量，与 YJK 周期计算质量一致 | GFE-FAQ |
| ① | 模态分析（固有频率+振型提取） | step.frequency_step |  | Explicit§1.1.1.2 | 各单元与各约束体系均做前三阶频率/振型对比；仅弹性本构可用（表2.1） | GFE-Explicit |
| ① | 模态分析（固有频率+振型） | - |  | Imp§3.2 | 前 N 阶频率/振型，验证差异 0.000% | GFE-Implicit |
| ① | 模态分析（固有频率+振型，2D/3D） | frequency_step.eigen |  | SSA附录二 | 输出前 10 阶固有频率与前三阶振型（土-结构系统及结构） | GFE-SSA |
| ① | 模态分析（桩-土嵌固模型、YJK-GFE 振型对比）（修订记录线索） | frequency_step+embed全API |  | FAQ修订记录 | 指向 §3.19/4.15，仅作能力线索不计入能力总数 | GFE-FAQ |
| ① | 模态动力分析步 | - |  | UG§1.15.1(7) | 振型叠加法；阻尼比或瑞利阻尼；需先模态步 | GFE-UserGuide |
| ① | 模态动力学分析步 modal_dynamic_step | step.modal_dynamic_step |  | Cmd§2.14.6 | cont 继续标志 + time_increment/time_period + 模态阻尼 | GFE-Cmd |
| ① | 模态阻尼 modal_damping | step.modal_damping |  | Cmd§2.14.12 | type/definition/field | GFE-Cmd |
| ① | 求解器参数设置 | - |  | UG§1.16.3 | GUI 部分参数+config.txt 全量参数（稳定步长系数/沙漏/接触/液化/OOC 等） | GFE-UserGuide |
| ① | 生死单元-添加/移除 | - |  | Cases§2.2.8 | 每分析步两个挂接槽，模拟开挖（移除）与施工（添加）；区域可用单元集或几何集 | GFE-Cases |
| ① | 用户指定固定稳定时间步长 | - |  | Explicit§13.3 | 显式算法稳定时间步长可设（案例取 5e-5 s，线弹性/弹塑性两模型相同） | GFE-Explicit |
| ① | 移除畸形单元 | - |  | UG§1.15.4(4) | 长宽比/偏斜度/长度/面积/体积阈值，命中单元在 inp 中被注释掉 | GFE-UserGuide |
| ① | 组合壳综合管廊拟静力推覆验证（位移控制加载） | - |  | Explicit§10.2-10.3 | 顶端水平 30mm 位移、0→3.0s 线性 ramp；层间位移角 1/77 时局部进入非线性但承载力未软化 | GFE-Explicit |
| ① | 自动导出计算文件 | - |  | UG§1.15.4(3) | 提交自动导出 inp+inpx（ydb 导入的模型另出 gjdy） | GFE-UserGuide |
| ① | 计算核心选择 GFEXC/GFEXG | - |  | Cases§4.3.8 | GFEXC=CPU、GFEXG=英伟达 GPU（仅一字母之差）；下拉项原文"使用 CPU 计算 / 使用软件支持的英伟达显卡进行计算" | GFE-Cases |
| ① | 质量缩放 mass_scaling | step.mass_scaling |  | Cmd§2.14.11 | region/type/frequency/target_time | GFE-Cmd |
| ① | 质量缩放设置（目标时间增量） | step.mass_scaling.target_time |  | FAQ§3.1 | 按区域/类型/频率/系数/目标设置动力迭代步长，控制 mass scaling 程度 | GFE-FAQ |
| ① | 质量缩放（=显式动力步长） | - |  | Cases§4.3.5 | 勾"使用下面的缩放定义"→添加→目标时间增量；未设则步长默认 5e-5 | GFE-Cases |
| ① | 重力荷载静力分析（2D/3D） | static_general_step+bc type=7重力 |  | SSA附录一 | 地震分析前置的重力静力工况，输出内力与竖向位移 | GFE-SSA |
| ① | 阻尼-分析类型兼容矩阵（表6） | 知识表;各阻尼API齐备按矩阵取用 |  | Imp表6 p152 | 5 类阻尼 × 6 类分析的 Y/N 矩阵，完整转录见③3.11；模态分析全 N、反应谱仅振型阻尼比 Y | GFE-Implicit |
| ① | 阻尼族（目录预告：全局瑞利/全局结构/振型阻尼比/振型瑞利/visco/材料瑞利） | global/modal/material damping API齐 |  | Imp第六章目录行178-210 | 已于 P1.5 经 PDF 直读补齐 p152-174（见 K 表#103-#112，6 族全部实证） | GFE-Implicit |
| ① | 附加质量 Comb_M 挂 Initial | - |  | Cases§10.13 | YJK 导入的附加质量荷载加在 Initial 步 | GFE-Cases |
| ① | 附加质量添加到 initial 分析步 | bc type=10+case按步挂载 |  | FAQ§3.4/3.5 | 地震工况/模态工况中将 Comb_M_xxx 加入 initial 步参与质量统计 | GFE-FAQ |
| ① | 隐式动力分析 Newmark 法 | - |  | Imp§3.3 | 直接积分动力时程，惯性力正弦激励 | GFE-Implicit |
| ① | 隐式动力分析 振型叠加法 | modal_dynamic_step |  | Imp§3.3(误标3.2.2) | 模态叠加法动力时程（正文描述误写 newmark，见②） | GFE-Implicit |
| ① | 隐式动力分析步 | - |  | UG§1.15.1(4) | 总时长/几何非线性/时间增量 | GFE-UserGuide |
| ① | 隐式动力分析步 dynamic_implicit_step | step.dynamic_implicit_step |  | Cmd§2.14.4 | direct 直接求解标志、gfe_linear 线性标志、explicit 只读 | GFE-Cmd |
| ① | 隐式静力分析（仅弹性本构） | step.static_general_step |  | Explicit表2.1 | 表2.1 明文仅弹性本构支持"隐式静力分析" | GFE-Explicit |
| ① | 静力分析 | static_general_step |  | Iso§2.1/§3.2 | 减隔震流程必经步骤（Dead/Live/Comb 工况见工况树截图） | GFE-Iso |
| ① | 静力分析(地应力平衡)步 | - |  | Cases§6.11.1 | 与"静力分析"并列的独立类型（GeoStatic-1） | GFE-Cases |
| ① | 静力分析步 | - |  | UG§1.15.1(1) | 总时长/几何非线性/增量（初始/最小/最大） | GFE-UserGuide |
| ① | 静力分析步（地应力平衡） | - |  | UG§1.15.1(2) | 地应力场与荷载、边界取得平衡 | GFE-UserGuide |
| ① | 静力分析步（通用） | - |  | Cases§1.2.5 | 总时长 1；时间增量 初始1/最小1e-05/最大1 为常见默认 | GFE-Cases |
| ① | 静力分析（StaticStep） | - |  | FAQ§3.1 | 用于查局部位移异常 | GFE-FAQ |
| ① | 静力分析（含线性强化弹塑性） | - |  | Imp§3.1 | 底固模型静力集中荷载 | GFE-Implicit |
| ① | 静态通用分析步 static_general_step | step.static_general_step |  | Cmd§2.14.1 | init_inc/period/min_inc/max_inc 增量控制 | GFE-Cmd |
| ① | 非线性分析动接静（自动地应力平衡） | - |  | FAQ§4.11/4.12 | 动力分析步接静力分析步时软件自动进行地应力平衡，动力步重力瞬时加载 | GFE-FAQ |
| ① | 频响分析 模态法 | steady_dyn_step direct=False |  | Imp§3.4.2 | 模态法频响，算例用超弹 Polynomial(n=2) | GFE-Implicit |
| ① | 频响分析 直接法 | steady_dyn_step direct=True |  | Imp§3.4.1 | 顶面集中力 100kN，0-200Hz 扫频 | GFE-Implicit |
| ① | 频响分析步 | - |  | UG§1.15.1(6) | 模态法/直接法；对数/线性缩放；Range/Eigen frequency/Spread 间距 | GFE-UserGuide |
| ① | 频响分析步（线性摄动） | - |  | Cases§3.2.3 | 计算方法直接法/缩放线性/频率范围与点数/结构阻尼 | GFE-Cases |
| ① | 高层建筑施工范式（单元激活） | case.set_elemAdd |  | Imp§7.2 p180-183/§7.3 p183-186 | 壳/梁框架模型自下而上逐层激活加层 | GFE-Implicit |
| ② | CPU 并行隐式求解 | - | 命令流无作业模块,INP写出后CLI/桥提交 | Imp前言行245 | 隐式求解器 GFEXN 为 CPU 并行架构 | GFE-Implicit |
| ② | CPU 计算 | - | 无作业API,INP+求解器命令行 | FAQ§3.7 | CPU 求解路径，占用内存比 GPU 多 | GFE-FAQ |
| ② | CPU+GPU 异构并行显式动力求解 | - | 作业设置无API,INP+CLI参数/桥 | UG前言 | 多 GPU 并行显式动力计算，宣称比多 CPU 并行快 10 倍以上 | GFE-UserGuide |
| ② | GFEXN 隐式非线性求解器自动选用 | - | 求解器内部行为,断点在作业提交 | Cases§6.12.1 | 工况含多个静力分析步时程序自动改选 GFEXN | GFE-Cases |
| ② | GPU 单卡显式计算（双精度） | - | 作业设置无API,CLI/桥提交 | Explicit§4.4.1.1-4.4.1.3 | 2 万~158 万节点规模实测；小模型反而慢于 CPU | GFE-Explicit |
| ② | GPU 双卡并行显式计算 | - | 作业设置无API,CLI/桥提交 | Explicit§4.4.2.1-4.4.2.3 | 35万/92万/158万节点，加速比约 1.77× | GFE-Explicit |
| ② | GPU 计算 | - | 作业设置无API,CLI/桥提交 | FAQ§3.7 | 支持 NVIDIA GPU 求解（6GB+ 显存、CUDA≥11.0） | GFE-FAQ |
| ② | 作业管理器：提交作业 | - | 无API,桥点击或求解器CLI | FAQ§5.4 | 在 GFE 内提交计算作业，完成时提示 success | GFE-FAQ |
| ② | 作业管理（创建/提交/监控/结果） | - | 无API;提交走CLI,监控读日志/db | SSA§3.1.10 | Job Manager：Create→选工况→Submit→Monitor→Results 进后处理 | GFE-SSA |
| ② | 作业高级设置 | - | GUI对话框,等效CLI参数/桥 | Cases§8.5 | "高级>>"：写出SPH xml / 写出Vuel / 求解方法 Pardiso / 列车荷载写入inpx | GFE-Cases |
| ② | 多 GPU 显式动力求解 | - | 作业层无API,CLI/桥 | Iso前言 | CPU+GPU 异构并行显式动力分析，称比多 CPU 并行快 10 倍以上 | GFE-Iso |
| ② | 多GPU并行显式动力求解（单卡/双卡，双精度） | - | 作业层无API,CLI/桥 | SSA前言行137/§6.2/第7章 | CPU+GPU 异构并行显式动力；2080 单卡 504min / 双卡 263min 完成 E2 三维时程，约为软件A CPU 的 1/10 | GFE-SSA |
| ② | 粘弹性分析（Prony 级数 + 超弹 Yeoh 基材） | - | StepType无Visco步,材料有API分析步改INP | Imp§3.6 | 二阶 Prony 叠加 Yeoh 应变势能，输出位移徐变曲线 | GFE-Implicit |
| ② | 跨平台求解（Windows10 / Ubuntu） | - | 求解器CLI跨平台,命令流无提交入口 | Explicit§4.4.1-4.4.2 | GFE GPU 求解两平台均有实测 | GFE-Explicit |
| ② | 钢筋影响可选计入模态 | - | 无开关API,convert_reinforce移除配筋等效 | FAQ§4.15-4 | GFE 模态分析可考虑或不考虑钢筋刚度贡献 | GFE-FAQ |
| ② | 静力分析强制线弹性 | - | static步无gfe_linear字段,INP/GUI层 | FAQ§3.12 | 静力分析仅读弹性参数；动力分析才读塑性参数做非线性 | GFE-FAQ |
| ③ | *.feasta 稳定步长/质量缩放诊断 | - |  | FAQ§3.1-5/6 | 计算生成 *.feasta，搜关键字"mass"看各单元类型稳定步长与质量缩放 | GFE-FAQ |
| ③ | 工况预览（生死单元播放） | - | GUI动画播放界面专属 | Cases§6.11.5 | 通用页"工况预览"按分析步播放激活状态 | GFE-Cases |
| ③ | 求解器 Config 文件修改（单元失效开关） | - |  | Cases§14.8 | 改安装目录 Program\config.txt：IsRemoved_Co=1、IsRemoved2_Co=1，添加 IsRemoved3_Co=1 | GFE-Cases |

## D07 地震SSI与场地反应（93 项：①64 ②3 ③23 未知3）

| 层 | 能力 | API入口 | 断点/理由 | 出处 | 说明 | 源手册 |
|---|---|---|---|---|---|---|
| ① | E2/E3 双水准基岩露头地震动输入 | - |  | Explicit§13.2.3 | 线弹性分析用 E2 露头波、弹塑性分析用 E3 露头波 | GFE-Explicit |
| ① | EERA 土体材料自动替换+Alpha 阻尼自动输入 | vibra_load.set_parameter UseEERAMat/DampScale 参数可达 |  | FAQ§3.21 | 等效线性化后软件自动替换 EERA 土材料并自动写入 Alpha 阻尼（inp 中可见） | GFE-FAQ |
| ① | ERA 用于拟动力分析（Use for: Pseudo Dyna） | set_parameter UI_Method 可选用途 |  | SSA§4.1.1 | 反应加速度法专用：勾选幅值、输入 Struc Top-Bot Depth、Compute | GFE-SSA |
| ① | ERA 用于时程分析（Use for: Time History） | set_parameter UI_Method 可选用途 |  | SSA§3.1.8 | ERA 窗口选 Time History，选输入位置与幅值函数方向，Save 保存 | GFE-SSA |
| ① | GFE-SSA E2 等效线性化工程级分析 | soil+vibra_load+convert_to_davidenkov 全链命令流 |  | Explicit§13.7 | 大型交通枢纽 E2 等效线性化分析与软件A 基本一致，计算时间仅为软件A 的 1/8 | GFE-Explicit |
| ① | GFE-SSA 人工边界地震动载荷自动生成 | artbc_mgr+vibra_load 命令流可建边界与载荷 |  | Explicit§7.1.1 | 依据场地反应结果直接在人工边界处生成地震动载荷 | GFE-Explicit |
| ① | 一维土层创建 | - |  | Cases§4.2.2; UG§1.18.1(1) | 层数/深度方向(x/y/z 可选)/各层厚度+材料（从高到低）/基岩材料；"计算"按钮自动算 P 波速、S 波速、建议网格尺寸（=Vs/50，c03 实证）；支 | GFE-Cases+GFE-UserGuide |
| ① | 一维土层剖面定义 soil | soil.soil |  | Cmd§2.16.1 | depth 列表逐层深度 + materials 逐层材料 + bedrock_mat 基岩材料 + depth_dir 深度方向(0:x,1:y,2:z) | GFE-Cmd |
| ① | 一维土层计算（建议网格尺寸） | set_parameter SubLayerHeight 参数 |  | FAQ§3.2-2 | "一维土层计算"给出土体建议网格尺寸，作为划分上限 | GFE-FAQ |
| ① | 一维场地地震反应分析（等效线性化，对标 EERA） | - |  | Explicit第7章 | 土体等效线性化 1D 场地反应，功能与 EERA 相同；补块证实位移/加速度与 EERA 完全重合（图7.1-6/7.1-7） | GFE-Explicit |
| ① | 三位置地震动输入（基岩露头/基岩-土交界面/场地地表，Outcrop 选项） | vibra_load.input_loc/is_outcrop 属性 |  | Explicit§7.1.1-7.1.2 | 三种实测位置任一输入均可获得同一场地反应；处理方式各不同（露头折半/交界面直接/地表反演）；补块证实三种输入的基岩处剪应力时程重合（图7.1-8） | GFE-Explicit |
| ① | 三维土层 / 一维土层（模型树节点） | GFE.Pre.soil Soil1D+GFE.soil 构建器 |  | FAQ§3.1/3.3 | 模型树分别有"三维土层""一维土层"节点 | GFE-FAQ |
| ① | 三维时程分析全流程（E2/E3/液化） | 材料/步/工况/载荷全链命令流,INP 可 daemon 提交 |  | SSA第6章 | ydb 3D 导入→外轮廓实体裁剪→查找几何面→GPU 显式求解 | GFE-SSA |
| ① | 二维时程分析全流程（线性 E2 / 非线性 E3 / 液化） | 同三维:全链命令流可达 |  | SSA第3章 | ydb 导入→土体建模→人工边界→ERA→显式动力求解→后处理 | GFE-SSA |
| ① | 创建土体 | - |  | UG§1.18.1(2) | 按一维土层生成 长方体(3D)/圆柱体(3D)/长方形(2D)，自动建各土层集合与截面 | GFE-UserGuide |
| ① | 创建土体几何（Create Soil） | GFE.soil.box_builder |  | SSA§3.1.2(3) | 选 2D、选土层、输入 Length 宽度，自动生成成层土体几何 | GFE-SSA |
| ① | 创建土层（Soil Layers） | GFE.soil.data_builder+Pre.soil |  | SSA§3.1.2(2) | 材料创建完毕后按层定义土层 | GFE-SSA |
| ① | 动剪切模量比/阻尼比-剪应变曲线按土类定义 | - |  | Explicit§7.1.2 | 黏土/砂土（第7章）与黏质粉土/细砂/粉质黏土（第13章）各组 G/Gmax-γ 与 λ-γ 曲线按土体类别输入 | GFE-Explicit |
| ① | 动力工况三要素挂接 | - |  | Cases§4.3.7 | 动力步必须显式挂：地震场地反应+人工边界+动力场输出请求 | GFE-Cases |
| ① | 固定边界+惯性力式地震输入（无 SSI 模式） | - |  | Explicit§13.4 | 结构与土体接触面设固定边界，地震动以惯性力形式施加到结构模型 | GFE-Explicit |
| ① | 土-结构动力相互作用分析方法集成 | SSI 时程全链命令流可建可算 |  | UG前言 | 动力人工边界、场地地震反应分析、地震动输入（详文 §1.18） | GFE-UserGuide |
| ① | 土体模块导入 | GFE.soil |  | Cmd§5.2 | from GFE import soil（几何构建器命名空间；土体数据对象在 GFE.Pre.soil，见 §2.16） | GFE-Cmd |
| ① | 土层数据复制/粘贴 | - |  | UG§1.18.1(1) | 表格与文本互转（逗号分隔列） | GFE-UserGuide |
| ① | 土层管理器 | soil.soil_manager |  | Cmd§2.16.2 | soil_manager() 或 soil_mgr() | GFE-Cmd |
| ① | 地下结构-土体系统地应力平衡（大规模混合单元模型） | - |  | Explicit§9.4 | 470m×175m×83.65m、61.5 万单元（梁1452+三角壳2550+四边壳18306+四面体592849）整体平衡 | GFE-Explicit |
| ① | 地下结构三维反应谱分析全流程 | response_spectrum_step 命令流可建 |  | Imp§3.5.2 | 五步：建模→由地震波生成响应谱→底固+四周滚轴→分析步与工况→后处理 | GFE-Implicit |
| ① | 地应力平衡（初始应力条件） | - |  | Explicit第9章引言 | 对无地下结构自由场施重力生成初始应力场，再保留应力场、平衡（清除）初始位移场 | GFE-Explicit |
| ① | 地震动幅值 set_amplitude(int, str) | complex_field.set_amplitude |  | Cmd§3.6.1 | 设置某方向地震动幅值，0/1/2 = x/y/z | GFE-Cmd |
| ① | 地震动调幅 compute_era | geotool.compute_era |  | Cmd§3.4.22 | compute_era(target_acce, adjust_iter, adjust_target_tol, a_layer, vibra_name) 迭代 | GFE-Cmd |
| ① | 地震场地反应 | - |  | Cases§4.3.4 | "用于"三模式：时程分析(等效线性化)/时程分析(非线性)/拟动力分析；输入位置=基岩露头；x/y/z 逐向激活幅值函数；调幅（目标地表峰值 m/s²+迭代次数 | GFE-Cases |
| ① | 地震场地反应分析 | - |  | UG§1.18.3 | 三用途：时程（等效线性化）/时程（非线性）/拟动力；输入位置 基岩处/基岩露头/地表 | GFE-UserGuide |
| ① | 地震场地反应（模型树节点） | GFE.Pre.vibration 模块整体可达 |  | FAQ§3.1/3.3 | 模型树有"地震场地反应"独立节点 | GFE-FAQ |
| ① | 场地反应与地下结构抗震分析无缝对接 | case 按步挂 vload 命令流联动 |  | Explicit§7.3 | 场地反应结果直接对接反应位移法、反应加速度法、时程方法，无需多软件间数据处理 | GFE-Explicit |
| ① | 场地反应分析（含高级参数调整）（修订记录线索） | vibra_load.set_parameter 全套高级参数 |  | FAQ修订记录 | 指向 §3.20-3.22，仅作能力线索不计入能力总数 | GFE-FAQ |
| ① | 场地反应分析（土体模态/时程/统计量；地震波多位置输入） | - |  | FAQ§3.3 | 场地分析结果含时程曲线、统计量、土体模态频率；支持基岩波/地表波/基岩露头波在对应位置输入 | GFE-FAQ |
| ① | 场地反应调幅 | - |  | UG§1.18.3 | 设目标地表加速度峰值迭代调输入幅值（2024 新增） | GFE-UserGuide |
| ① | 场地反应高级参数 | - |  | UG§1.18.3 | N/MaxIter/Tol/Rr/SubLayerHeight/TimeInterval/DampConvOrder/DampScale/UseIntgOutp | GFE-UserGuide |
| ① | 场地反应高级参数 UseEERAMat | set_parameter UseEERAMat |  | FAQ§3.21 | true=等效线性化（需试验数据曲线），false=不采用 | GFE-FAQ |
| ① | 场地反应高级参数 UseIntgOutp | set_parameter UseIntgOutp |  | FAQ§3.21 | true=时域法结果，false=频域法结果 | GFE-FAQ |
| ① | 场地地震反应分析 | vibra_load+soil 命令流全配置 |  | Imp前言行244 | 自由场反应分析 | GFE-Implicit |
| ① | 场地地震反应管理器 | vibration.vibraload_manager |  | Cmd§2.17.2 | vibraload_manager() 或 vib_mgr()，模块路径为 GFE.Pre.vibration（非章节名 vibload） | GFE-Cmd |
| ① | 场地地震反应载荷 vibra_load | vibration.vibra_load |  | Cmd§2.17.1 | 三方向底部幅值 amp_bottom_x/y/z + 关联一维土层 + is_outcrop 露头开关 + input_loc 输入位置；set_paramet | GFE-Cmd |
| ① | 复杂场地对象 complex_field() | complex_field.complex_field |  | Cmd§3.6.1 | GFE.geometry.complex_field.complex_field() 创建复杂场地反应计算对象 | GFE-Cmd |
| ① | 实体（一阶四面体）单元地应力平衡 | - |  | Explicit§9.3 | 三向 980 m/s² 惯性力下平衡：位移 1.064m→8.304×10⁻³m，应力基本不变 | GFE-Explicit |
| ① | 工况与分析步 set_analysis(str, str) | complex_field.set_analysis |  | Cmd§3.6.1 | 设置计算的工况和分析步，其内分析时长/荷载/输出请求被继承 | GFE-Cmd |
| ① | 快速建土 | GFE.soil.box_builder 快速建土 |  | Cases§4.2.2 | 工程页签：形状 长方体(3D)/圆柱体(3D)/长方形(2D)+长宽；深度随已建一维土层；自动生成 SoilGeom-N 与 SoilLayerProp-N | GFE-Cases |
| ① | 执行计算 perform() | complex_field.perform |  | Cmd§3.6.1 | 执行复杂场地计算 | GFE-Cmd |
| ① | 数据构建器 data_builder() | soil.data_builder |  | Cmd§5.4 | 属性赋值式：dimension(2/3)/name/layer_shape/layer_material 后 build()/perform()，构建几何体、集 | GFE-Cmd |
| ① | 无土模型（不考虑 SSI）输入构造 | - |  | Explicit§13.2.3 | 无土模型输入取"场地分析中结构底板相应位置处的场地加速度"，非原始露头波 | GFE-Explicit |
| ① | 核岛结构-地基 SSI 地震反应全流程 | - |  | Explicit§12.3-12.6 | 重力场分析→模态分析→线弹性 SSI 时程→CDP+摩尔库伦非线性时程，与软件A 四类指标逐项对比 | GFE-Explicit |
| ① | 梁/三角形壳/四边形壳单元地应力平衡 | - |  | Explicit§9.1-9.2.2 | 结构单元也参与初应力平衡：位移降约 2 个数量级、应力基本不变 | GFE-Explicit |
| ① | 盒子构建器 box_builder() | soil.box_builder |  | Cmd§5.3 | set_height(土层高度列表[从下到上], depth_dir) + set_parameter(长,宽) + build()/perform()，返回  | GFE-Cmd |
| ① | 等效线性化一维场地地震反应分析（ERA/EERA 模块） | vibra_load 等效线性化+compute_era |  | SSA§1.1.3 | 等效线性化一维场地反应，结果自动转化为后续 SSI 分析地震荷载，无需导入导出 | GFE-SSA |
| ① | 等效线性化时程方法整体流程 | - |  | Explicit§13.1 | 自由场等效线性分析→折减土层 E + 附加阻尼比→整体 SSI 时程（GB 50909-2014 / GB/T 51336-2018 驱动） | GFE-Explicit |
| ① | 设置几何 set_geometry(str) | complex_field.set_geometry |  | Cmd§3.6.1 | 设置复杂场地反应的几何体名称（需已划分网格） | GFE-Cmd |
| ① | 读取当前材料截面 set_material_as_current() | complex_field.set_material_as_current |  | Cmd§3.6.1 | 从当前模型读取材料截面信息 | GFE-Cmd |
| ① | 超大规模显式 SSI 一体化计算 | - |  | Explicit§13.2.4 | 1122m×940m×105m，161 万节点、494 万单元（梁121万+三角壳6万+四边壳103万+四面体264万）一体化计算 | GFE-Explicit |
| ① | 输出目录 set_output_dir(str) | complex_field.set_output_dir |  | Cmd§3.6.1 | 设置结果输出目录（需预先已创建好） | GFE-Cmd |
| ① | 静力-动力连续分析（初始地应力平衡） | geo_static_step+InitGeostaticStress 命令流 |  | SSA§1.1.6/§3.1 | 人工边界法向约束+体力静力分析→应力与边界约束力自动传入动力分析，免手动数据传递 | GFE-SSA |
| ① | 非均匀土体（网格插值法） | geotool.build_non_uniform_soil |  | UG§1.18.15 | 钻孔数据（nodes/surface 两 txt）对已划网格土体插值赋土层材料，适用土层不连续/杂糅场地 | GFE-UserGuide |
| ① | 非均匀土体（钻孔数据建模） | - |  | Cases§5.2.1; UG§1.18.4 | 工程—非均匀(土体)：土层数+逐层材料；钻孔坐标(x,y)+土层深度可粘贴 | GFE-Cases+GFE-UserGuide |
| ① | 非均匀土层构建 build_non_uniform_soil | geotool.build_non_uniform_soil |  | Cmd§3.4.17 | 按采样点(SoilSample: x,y,depth 列表)构建 2D/3D 非均匀土层，自动创建几何对象、几何集和属性；materials 顺序从上到下，di | GFE-Cmd |
| ① | 非线性分析初始应力条件（梁/壳/实体/地下结构-土体系统） | - |  | Explicit第9章 | 已于 P1.5 经 PDF 直读补齐 p235-240，正文条目见 M 节 | GFE-Explicit |
| ① | 频域等效线性化→时域瑞利阻尼转换 | set_parameter DampConvOrder/DampScale |  | Explicit§7.2 | 等效阻尼比转换为 [C]=α[M] 质量比例瑞利阻尼（无刚度项），α=2ωζ_n，ζ_n 为各土层滞回阻尼比、ω 取土层第一阶固有圆频率；模量须用等效线性化衰减 | GFE-Explicit |
| ② | ERA 现场计算与结果查看（Compute/Result） | - | 计算可 geotool.compute_era;Result 结果查看仅 GUI 面板 | SSA§3.1.8/§4.1.1 | 点 Compute 计算、Result 查看场地分析结果 | GFE-SSA |
| ② | 内置预设地震波库 | - | 波库为安装目录数据文件可读;选择界面 GUI | Cases§4.3.3 | 对话框内"预设"按钮调用天然/人工波库（25_RH1TG025_* 系列、KOBE 等），填充进表格 | GFE-Cases |
| ② | 地基弹簧刚度两种确定方法 | - | spring_dashpot 可设值;刚度计算器为 GUI | SSA§1.2.2 | 基床系数法 k=KLd 或静力有限元法（孔洞四侧面加载测位移） | GFE-SSA |
| ③ | ERA/EERA 结果查看（AR：变量 A/U/S）与表格导出、深度→坐标转换 | - | AR 结果四视图/表格导出为后处理界面专属 | SSA§4.1.1/§5.1.1 | AR/反应加速度下 A/U/S 给出"结构顶底位移差最大时刻"的土层加速度/位移/剪应力曲线；Table 出表；【Top coord of depth dir】 | GFE-SSA |
| ③ | 一维场地反应深度剖面输出（峰值加速度/位移/剪应力随深度） | - | 深度剖面结果输出为 ERA 结果界面专属 | Explicit§12.2.2 | 等效线性化场地反应输出三条深度剖面曲线，供 SSI 模型与无土模型构造输入 | GFE-Explicit |
| ③ | 二维分析模型（反应位移法、反应加速度法） | - | 反应位移/加速度法依赖助手向导对话框 | FAQ§3.15 | 支持二维抗震分析法，梁用 B21、壳用 CPE3/CPE4R | GFE-FAQ |
| ③ | 反应位移法助手 | - | 助手向导对话框专属 | Cases§13.10 | 选结构几何+勾地连墙+选地震场地反应→"生成"自动建惯性力/土层剪力/相对位移/接地弹簧/只压不拉约束/分析步/场输出/工况（不含底部约束） | GFE-Cases |
| ③ | 反应位移法助手（自动建模，联动 1.18.3 场地反应） | - | 助手向导对话框专属 | UG§1.18.13 | 自动完成反应位移法荷载/弹簧/相互作用建模与工况设置；材料需含基床系数；"地震场地反应"下拉依赖先完成 1.18.3 | GFE-UserGuide |
| ③ | 反应位移法整体流程（荷载-结构模型） | - | 流程以助手向导为核心,无命令流入口 | SSA§1.2.2/第5章 | 地基弹簧+三类荷载（土层相对位移/结构惯性力/周围土层剪力），位移约束在地连墙底部 | GFE-SSA |
| ③ | 反应加速度法 / 反应位移法 | - | 两法均为助手向导,无命令流入口 | Imp前言行244/§3.5.2 | 地下结构抗震简化分析方法（声明仅二维） | GFE-Implicit |
| ③ | 反应加速度法整体流程（2D） | - | 助手向导流程,无命令流入口 | SSA§1.2.1/第4章 | 一维场地反应取最大相对位移时刻剪应力→有效反应加速度→底面固定+侧面竖向约束→Gravity 惯性力→静力求解 | GFE-SSA |
| ③ | 土压力自动生成（密度+g+泊松比） | - | 土压力自动生成为 GUI 工具,无 API 符号 | FAQ§3.23 | 土-结整体模型中土压力由自重竖向压缩经泊松比转横向挤压自动形成，无需另施加 | GFE-FAQ |
| ③ | 地下结构抗震规范方法集成 | - | 规范方法集成依赖助手向导族 | UG前言 | 2D/3D、线性/非线性时程、反应加速度法、反应位移法 | GFE-UserGuide |
| ③ | 场地反应结果四视图 | - | 结果视图为后处理界面专属 | Cases§4.3.4 | 时程曲线/统计量（折减系数、阻尼比、最大反应）/一维土柱模态/材料折减，频域法与时域法 | GFE-Cases |
| ③ | 场地反应结果查看 | - | 结果查看为后处理界面专属 | UG§1.18.3 | 时程曲线/统计量（折减系数、阻尼比、峰值）/土柱模态与材料变化 | GFE-UserGuide |
| ③ | 由地震波生成响应谱 | - | 谱生成工具仅 GUI,无 API 符号 | Imp§3.5.2步骤2 | 程序内由地震动时程生成加速度反应谱 | GFE-Implicit |
| ③ | 选波-导入/导出周期 | - |  | UG§1.18.14(6) | 导入结构周期及质量参与系数（txt）用于谱比对周期点 | GFE-UserGuide |
| ③ | 选波-工作路径设置 | - |  | UG§1.18.14(3) | 设置输出与读取的工作目录 | GFE-UserGuide |
| ③ | 选波-添加/删除已选与绘图对比 | - |  | UG§1.18.14(9) | 双击加入已选；绘图区画时程或反应谱（叠目标谱） | GFE-UserGuide |
| ③ | 选波-筛选地震波 | - |  | UG§1.18.14(7) | 按双重比值范围筛选（平均谱 0.80-1.20、单条谱 0.50-1.50 默认） | GFE-UserGuide |
| ③ | 选波-自定义人工波/天然波导入 | - |  | UG§1.18.14(5) | 文件夹自动读 txt 自定义波；修改后须点"更新自定义" | GFE-UserGuide |
| ③ | 选波-自定义反应谱导入 | - |  | UG§1.18.14(4) | 导入用户 txt 自定义目标谱（如安评谱） | GFE-UserGuide |
| ③ | 选波-规范反应谱 | - |  | UG§1.18.14(4) | 按《建筑抗震设计标准》GB/T50011-2010 设定目标谱（标准名/编号照手册原文） | GFE-UserGuide |
| ③ | 选波-输出反应谱 | - |  | UG§1.18.14(10) | 工作路径下生成已选波时程/反应谱 txt+图形及对比 | GFE-UserGuide |
| ③ | 选波工具（整体） | - |  | UG§1.18.14 | 选取与目标反应谱接近的地震波；独立程序 SelWave.exe（安装路径 program），前处理"工程"页按钮可启动 | GFE-UserGuide |
| ③ | 隧道反应位移法助手 | - | 助手向导对话框专属 | UG§1.18.12 | 隧道几何+截面+场地材料+波型+柔度系数 δ 等 10 项参数算地震下隧道某一最不利时刻响应 | GFE-UserGuide |
| 未知 | §7.1.2 后半 + §7.2 瑞利阻尼转换正文 | - |  | Explicit第7章 | 已于 P1.5 经 PDF 直读补齐 p219-224，正文条目见 H 节 #94/#115-117 | GFE-Explicit |
| 未知 | 土-结整体模型土压力考虑方式（修订记录线索） | - |  | FAQ修订记录 | 指向 §3.23，仅作能力线索不计入能力总数 | GFE-FAQ |
| 未知 | 工程案例：组合壳综合管廊/地铁环境振动/核岛/大型交通枢纽 | - |  | Explicit第10-13章 | 已于 P1.5 经 PDF 直读补齐 p241-288，正文条目见 N 节 | GFE-Explicit |

## D08 人工边界与波动输入（26 项：①25 ②1 ③0）

| 层 | 能力 | API入口 | 断点/理由 | 出处 | 说明 | 源手册 |
|---|---|---|---|---|---|---|
| ① | 2D P 波入射（平面应变） | - |  | Explicit§8.5 | 同 2D 模型，竖向（Y/U2）入射，底/顶与理论一致 | GFE-Explicit |
| ① | 2D S 波入射（平面应变） | - |  | Explicit§8.4 | 250m 正方形、四边形平面应变单元 15625 个，底/顶位移速度与理论一致 | GFE-Explicit |
| ① | 3D P 波垂直入射 | - |  | Explicit§8.2 | 因 P 波波速较快网格由 10m 加密至 5m；振动方向选 Z 与波传播方向一致 | GFE-Explicit |
| ① | 3D S 波（SV）垂直入射——立方体/三棱柱/圆柱/半球四种截断域 | - |  | Explicit§8.1.1-8.1.4 | 250m 域 + 黏弹性边界 + 底部脉冲垂直入射剪切波，四种外形顶部响应均与理论解一致（网格 10m 六面体/5m 六面体/5m 六面体/5m 四面体） | GFE-Explicit |
| ① | 3D 三向（X/Y/Z）同时波动入射 | - |  | Explicit§8.3 | 同一模型同时输入三向脉冲，底面和顶部位移/速度与理论一致 | GFE-Explicit |
| ① | P 波 / SV 波 / SH 波波动输入 | - |  | Explicit第8章引言 | 提供不同地震动波形的波动输入；SH 波引言明文列出但本章无算例 | GFE-Explicit |
| ① | 三种地震动输入位置换算 | vibra_load.input_loc+is_outcrop |  | SSA§1.1.3/§3.1.8 | 支持地表输入/基岩输入/基岩露头（Outcrop）三种输入位置 | GFE-SSA |
| ① | 三维黏弹性人工边界 | artbc.art_bc+artbc_mgr |  | SSA§1.1.2 | 法向/切向并联弹簧-阻尼，K 含 1/r 系数 | GFE-SSA |
| ① | 二维黏弹性人工边界 | artbc.art_bc(2D同口径) |  | SSA§1.1.2 | 法向/切向并联弹簧-阻尼，K 含 1/(2r) 系数 | GFE-SSA |
| ① | 人工边界 GUI 施加（Art BCs） | artbc_mgr.add等效GUI面板 |  | SSA§3.1.7 | 选择结构和已建表面，一键完成人工边界设置 | GFE-SSA |
| ① | 人工边界定义 art_bc | artbc.art_bc |  | Cmd§2.20.1 | structure 以几何定形心 / centered+center 以坐标定形心 + surface 表面集合；模块路径 GFE.Pre.artbc（非章节名 | GFE-Cmd |
| ① | 人工边界管理器 | artbc.artbc_mgr |  | Cmd§2.20.2 | manager() 或 artbc_mgr() | GFE-Cmd |
| ① | 人工边界（黏弹性边界）施加 | - |  | FAQ§3.1/3.3 | 人工边界施加于表面集（不可用节点集） | GFE-FAQ |
| ① | 动力人工边界条件 | artbc.art_bc+case.set_artbc |  | Imp前言行244 | 粘弹性人工边界已在 §3.4.3 部分实证，其余动力边界未见正文 | GFE-Implicit |
| ① | 地震动输入方法 | vibra_load+art_bc组合 |  | Imp前言行244 | 土-结构系统地震动输入 | GFE-Implicit |
| ① | 地震动输入：三维 S波/P波/三向入射（立方体/三棱柱/圆柱/半球域）、二维 S/P 波 | - |  | Explicit第8章 | c01 目录登记；已于 P1.5 经 PDF 直读补齐 p226-234，正文条目见 L 节 | GFE-Explicit |
| ① | 基于黏弹性边界的地震动输入（多波型） | vibra_load.pwave_dir+amp三向 |  | SSA§1.1.4 | 支持 P 波、SV 波、SH 波及不同人工边界几何形状的等效节点力输入 | GFE-SSA |
| ① | 复杂模型截断边界地震动输入 | complex_field模块+artbc |  | Explicit第8章引言 | 对复杂模型的截断边界施加地震动波动输入 | GFE-Explicit |
| ① | 扩展网格参考解对账法 | 常规命令流建模可复现对账 |  | Explicit第5章 | 加大计算域的无边界模型作黏弹性边界精度参考解（方法论） | GFE-Explicit |
| ① | 粘弹性人工边界 | - |  | Cases§4.3.2 | 选表面集（或转换的单元集）+形心（选结构几何自动定或手动输坐标）；列车案例形心几何=SuperStru | GFE-Cases |
| ① | 粘弹性人工边界自动施加 | - |  | UG§1.18.2 | 选表面+形心（选几何或直接输入）一键创建；形心不支持网格方式 | GFE-UserGuide |
| ① | 粘弹性人工边界（底部+侧面）频响/波动分析 | - |  | Imp§3.4.3 | 半径50m×高24m 4层土场地，地表中心激励 | GFE-Implicit |
| ① | 黏弹性人工边界一键自动施加（2D/3D，考虑边界非规则性） | - |  | Explicit第5章 | 手册明言"一键命令快速实现自动施加"；补块证实立方体/三棱柱/圆柱/半球/2D 正方形截断域均通过理论解验证 | GFE-Explicit |
| ① | 黏弹性人工边界自动施加 | artbc_mgr.add自动施加 |  | SSA§1.1.2 | 自动考虑土层性质变化与边界几何非规则性，快速自动施加 | GFE-SSA |
| ① | 黏弹性边界弹簧-阻尼参数公式自动计算 | art_bc写出INP时自动计算参数 |  | Explicit第5章式(4-1) | K_N/K_T/C 按 λ、G、ρ、c_P、c_S、r、A、B 计算；A=0.8、B=1.1、r=模型高度 | GFE-Explicit |
| ② | 二维/三维黏性人工边界 | - | art_bc无黏性/黏弹类型字段,INPX/GUI层 | Explicit第5章 | 截断边界黏性吸收 | GFE-Explicit |

## D09 IO与外部接口（70 项：①48 ②3 ③18 未知1）

| 层 | 能力 | API入口 | 断点/理由 | 出处 | 说明 | 源手册 |
|---|---|---|---|---|---|---|
| ① | Connector 等效刚度/非线性刚度切换 | connector_elastic/plastic 行为命令流可换 |  | FAQ§1.19 | 默认读非线性刚度；模态/静力分析需手动改等效刚度 | GFE-FAQ |
| ① | DWG 导入（经 AutoCAD 插件中间文件） | io.open_dwg(u8path,parameter) |  | UG§1.2.2(12) | AutoCAD 内加载 GfePJ2020.arx 跑 wsd 产中间文件，GFE 再读 | GFE-UserGuide |
| ① | GMAT 材料库导入 | io.import_mat |  | UG§1.2.2(5) | 文件—导入—导入材料 | GFE-UserGuide |
| ① | GMAT 材料库导出 | io.export_mat |  | UG§1.2.2(5) | 已建材料导出为 .gmat 备复用 | GFE-UserGuide |
| ① | INP 写出（不提交计算） | inpio.writer set_case+perform |  | UG§1.2.2(2) | 任务管理器中"写出 Inp 文件"仅产出 INP 不提交 | GFE-UserGuide |
| ① | INP 导入 | open_inp |  | UG§1.2.2(2) | INP（GFE 计算任务文件）可作为模型文件导入 | GFE-UserGuide |
| ① | IO 模块导入 | GFE.io |  | Cmd§6.2 | from GFE import io / from GFE.io import inpio | GFE-Cmd |
| ① | YJK YDB 模型导入 | io.import_yjk 43 整参+字符串参 |  | FAQ§1.1-1.2 | 读取 dtlmodel.ydb + dtlCalc.ydb（必需）与 Jccad_0.ydb（可选）导入上部结构与基础 | GFE-FAQ |
| ① | YJK 刚性杆→SPRING2 两点弹簧自动转换 | import_yjk 导入时自动执行 |  | FAQ§3.8-1 | YJK 导入时刚性杆转为两点弹簧 SPRING2 | GFE-FAQ |
| ① | YJK 模型导入 | io.import_yjk |  | UG§1.2.2(6) | dtlmodel.ydb+dtlCalc.ydb（必要）+Jccad_0.ydb（可选）导入荷载/截面/几何/材料/施工阶段/配筋/基础 | GFE-UserGuide |
| ① | YJK 模型导入（含基础、筏板、地基梁/独立基础/条形基础、无地下室项目）（修订记录线索） | import_yjk para_int 覆盖基础选项 |  | FAQ修订记录 | 指向 §1.3/1.6/1.7/1.13-1.15，仅作能力线索不计入能力总数 | GFE-FAQ |
| ① | YJK 消能器模型联导 | import_yjk 导入自动转 Connector |  | Iso§2.2.1图2.2.1.1 | YJK 内两种建模路径（【构件布置→减震器】直接布置；或支撑构件+【特殊支撑→设置连接属性】），导入 GFE 时构件与参数一并带入 | GFE-Iso |
| ① | YJK 配筋转换（三态） | geotool.convert_reinforce(0/1/2) |  | UG§1.18.10 | 无配筋（删除全部）/GFE 默认配筋（需材料+构件配筋参数）/YJK 配筋（需 4 种 ydb） | GFE-UserGuide |
| ① | YJK 钢筋接口导入 | import_yjk+convert_reinforce |  | SSA§6.3 | E3 模型钢筋由 YJK 给出，通过接口程序导入 GFE | GFE-SSA |
| ① | YJK 附属结构导入（前缀命名） | import_yjk(is_accessory,name_prefix) |  | Cases§13.4 | 点选"附属结构"+名称前缀（DLQ）并入第二个模型（地连墙），材料名加前缀 | GFE-Cases |
| ① | YJK 隔震支座/减隔震构件导入（导入后转为 Connector 连接器，含刚度参数读取与坐标系对应）（修订记录线索） | import_yjk 自动转 Connector 含参数 |  | FAQ修订记录 | 指向 §1.18-1.21，仅作能力线索不计入能力总数 | GFE-FAQ |
| ① | YJK 隔震支座联导 | io.import_yjk |  | Iso§2.2.1图2.2.1.2/§5.1 p56 | YJK【前处理及计算→设置支座】定义支座类型参数后点构件赋属性，随模型导入 GFE；第五章隔震案例即从 YJK 导入结构模型 | GFE-Iso |
| ① | inpx 文件（扩展信息载体） | writer.set_trainload2inpx 产 INPX |  | FAQ§4.1 | inpx 含构件偏心、地震载荷、人工边界、工况、空间分布函数、包络输出等信息 | GFE-FAQ |
| ① | pre 文件复制派生 | - |  | Cases§10.16 | 弹塑性模型最佳做法：复制弹性 .pre 在副本上改材料 | GFE-Cases |
| ① | ydb 导入配筋选项（YJK 配筋/默认配筋） | convert_reinforce/import_yjk 参数 |  | SSA§3.1 | 非线性分析导入时选择 YJK 配筋或默认配筋，结构材料选"塑性" | GFE-SSA |
| ① | 写出 INP 文件（只写不算） | - |  | Cases§1.3.2 | 独立按钮导出求解器输入；兼作模型人工检查手段 | GFE-Cases |
| ① | 写出 inp 文件 | - |  | FAQ§3.6 | 前处理模型导出 inp 求解文件（需先划分网格） | GFE-FAQ |
| ① | 列车荷载导出 INPX 开关 set_trainload2inpx | writer.set_trainload2inpx |  | Cmd§6.5.3 | set_trainload2inpx(enable)，导出目标是 INPX 文件而非 INP | GFE-Cmd |
| ① | 创建 INP 写入器 inpio.writer | inpio.writer |  | Cmd§6.5.1 | writer = inpio.writer(file_path)（导入路径两版本并存，见②） | GFE-Cmd |
| ① | 基础导入控制参数（筏板最大周长 / 超出外轮廓最大距离） | import_yjk para_int 导入参数 |  | FAQ§1.6 | 控制读取基础时筏板轮廓识别的两个阈值参数 | GFE-FAQ |
| ① | 导入 AutoCAD DWG open_dwg | io.open_dwg |  | Cmd§6.4.4 | open_dwg(u8path, parameter)，parameter 整数列表（示例 [1,0,1,0]） | GFE-Cmd |
| ① | 导入 YJK import_yjk | io.import_yjk |  | Cmd§6.4.1 | import_yjk(u8path, para_int, para_str, to_cur_win, name_prefix, is_accessory)；u8 | GFE-Cmd |
| ① | 导入 YJK ydb 结构模型（2D/3D 模式） | io.import_yjk |  | SSA§3.1.1/§6.1 | Import→Import YJK DB；"模型维度"选 2D/3D，3D 时自动生成三维土体 | GFE-SSA |
| ① | 导入主目录选择 | import_yjk u8path/io.set_work_path |  | FAQ§1.2 | 主目录可选 YJK 计算路径目录或其"施工图"子目录 | GFE-FAQ |
| ① | 导入其他有限元软件计算模型 | open_inp |  | Cases前言(3); Imp前言行246; SSA前言行138 | 支持导入第三方有限元软件模型 | GFE-Cases+GFE-Implicit+GFE-SSA |
| ① | 导入接口族（8 类） | - |  | Cases§6.3.2 | 导入YJK/PKPM模型、导入INP、导入几何、导入GTS模型、导入Key、导入IFC、导入Ansys CDB、导入材料 | GFE-Cases |
| ① | 导入材料库 import_mat | io.import_mat |  | Cmd§6.4.5 | import_mat(u8path) 导入 gmat 文件，返回导入材料名列表（非 bool） | GFE-Cmd |
| ① | 导出材料库 export_mat | io.export_mat |  | Cmd§6.4.6 | export_mat(u8path) 导出当前材料到 gmat | GFE-Cmd |
| ① | 打开 Abaqus INP open_inp | io.open_inp |  | Cmd§6.4.2 | open_inp(u8path) 打开 INP 文件，返回操作状态 | GFE-Cmd |
| ① | 打开/合并 pre 文件 open_pre | io.open_pre |  | Cmd§6.4.3 | open_pre(u8path, merge=False, prefix="Part")，merge=True 时合并到当前文档并加名称前缀 | GFE-Cmd |
| ① | 执行 INP 导出 perform | writer.perform |  | Cmd§6.5.4 | result = writer.perform()，返回操作状态 | GFE-Cmd |
| ① | 构件过滤阈值（梁夹角阈值 / 最小板内角） | import_yjk para_int 导入参数 |  | FAQ§1.13 | 控制接口自动过滤小夹角梁与小内角三角形板，防畸形网格 | GFE-FAQ |
| ① | 桩合并阈值（YJK 导入参数） | import_yjk para_int 导入参数 |  | FAQ§3.8-2 | 导入时填非零值则桩-筏板改为共节点连接 | GFE-FAQ |
| ① | 结构设计软件模型导入 + 土-结构一体化建模 | import_yjk+土体/网格命令流全链 |  | Imp前言行246 | 设计软件模型导入后补建土体 | GFE-Implicit |
| ① | 自动生成基础模型（导入选项） | import_yjk 导入选项参数 |  | FAQ§1.3 | 按 YJK 地下室参数自动生成筏板基础与地下室外轮廓 | GFE-FAQ |
| ① | 自动生成筏板（厚度参数） | import_yjk 导入选项参数 |  | FAQ§1.5 | "自动生成筏板厚度"参数控制自动替换生成的筏板 | GFE-FAQ |
| ① | 获取 IO 实例 io.get_current() | io.get_current |  | Cmd§6.3 | 获取当前 IO 实例句柄 | GFE-Cmd |
| ① | 获得工作路径 get_work_path | io.get_work_path |  | Cmd§6.4.7 | 取当前工作路径（v3.3.0 新增） | GFE-Cmd |
| ① | 设置导出工况 set_case | writer.set_case |  | Cmd§6.5.2 | writer.set_case(case_name) 指定要导出的分析工况名 | GFE-Cmd |
| ① | 设置工作路径 set_work_path | io.set_work_path |  | Cmd§6.4.8 | 设置工作路径（手册未列参数说明） | GFE-Cmd |
| ① | 读取基础模型（导入选项） | import_yjk 导入选项参数 |  | FAQ§1.4 | 优先读 dtlmodel.ydb 基础，否则读 Jccad_0.ydb 的筏板/承台/桩/地梁 | GFE-FAQ |
| ① | 轴线围合地下室外轮廓 + 楼层号指定 | import_yjk para_int/para_str 选项 |  | FAQ§1.3-3 | 半地下室无侧壁处用轴线/梁围合，导入接口框中填对应楼层号 | GFE-FAQ |
| ① | 隔震支座→Connector 连接器导入 | import_yjk 自动转换 |  | FAQ§1.18-1.21 | YJK 减隔震构件导入为 Connector，含局部坐标系映射与刚度类型 | GFE-FAQ |
| ② | .pre 模型保存/打开、.db 结果打开 | - | open_pre 可达;保存与 .db 打开无 API,GUI 断点 | UG§1.2.1 | "打开"同时承担 .pre（前处理）与 .db（后处理结果）两种文件 | GFE-UserGuide |
| ② | YJK/PKPM 模型导入 | - | YJK 走 import_yjk;PKPM 仅 GUI | Cases§6.5.1 | 通用—导入—土木工程：指定数据主目录；dtlmodel.ydb+dtlCalc.ydb 必要、Jccad_0.ydb 可选；基本/外轮廓/减隔震三页签；基础模型 | GFE-Cases |
| ② | 通用导入 | - | inp/dwg/pre 有 API;其余格式仅 GUI | UG§1.2.2(1) | 对话框不过滤格式，不支持格式导入时弹窗报错 | GFE-UserGuide |
| ③ | Ansys CDB 导入 | - | 无 CDB API/命令行,仅导入对话框 | UG§1.2.2(11) | 读 cdb 含网格/材料/截面/实常数/相互作用/边界与荷载 | GFE-UserGuide |
| ③ | GFE 结果导回 YJK（效应组合/截面验算/配筋/计算书） | - | 后处理 YJK 回导向导专属 | Cases前言(3) | 宣称双向对接，案例正文未演示 | GFE-Cases |
| ③ | GTS NX mec 导入 | - | 无 API,仅导入菜单 | UG§1.2.2(8) | 读 GTS NX 求解器输入文件转 GFE 格式 | GFE-UserGuide |
| ③ | IFC 导入（仅几何） | - | 无 API,仅导入菜单 | UG§1.2.2(10) | BIM IFC 导入，GFE 主要读取几何信息 | GFE-UserGuide |
| ③ | Ls-Dyna K 文件导入 | - | 无 API,仅导入菜单 | UG§1.2.2(4) | 读取 K 文件网格/材料/边界转为 GFE 存储格式 | GFE-UserGuide |
| ③ | Ls-Dyna K 文件导出 | - | 无 API,仅导出菜单 | UG§1.2.2(4) | 文件—导出—导出 Key | GFE-UserGuide |
| ③ | OpenSees tcl 导出 | - | 无 API,仅导出菜单 | UG§1.2.2(9) | 文件—导出—导出 Opensees | GFE-UserGuide |
| ③ | PKPM 模型导入 | - | 无 API(import_yjk 仅 YJK) | UG§1.2.2(7) | .jwd+_calc.jwd（必要）+.dwb（可选基础，需 CAD 插件转换） | GFE-UserGuide |
| ③ | STP/STEP 几何导入 | - | 无 API,仅导入菜单 | UG§1.2.2(3) | 文件—导入—几何文件—导入 STP | GFE-UserGuide |
| ③ | YJK 双向对接（结果回导配筋出计算书） | - | 结果回导/计算书为后处理 GUI 专属 | UG前言 | GFE 结果可导回 YJK 做效应组合、截面验算、配筋、生成计算书 | GFE-UserGuide |
| ③ | YJK 工况命名约定 | - |  | UG附录三 p308 | Dead/Live/gk1-gk4/Comb 工况名与 YJK 数据的映射规则 | GFE-UserGuide |
| ③ | YJK 截面与厚度集合命名规则 | - |  | UG附录三 p309-310 | 构件标识符_材料厚度_截面形状尺寸_子截面序号_钢材牌号 的组合命名语法；解析 YJK 导入模型时必须依赖 | GFE-UserGuide |
| ③ | YJK 荷载/附加质量命名约定 | - |  | UG附录三 p308 | LL_BEAM 等 7 类荷载名 + M_Point/M_BEAM/M_SLAB 质量名 | GFE-UserGuide |
| ③ | 写出 inp 高级选项"写出 Vuel"（inp+*.vload 供 ABAQUS 子程序） | - | writer 无该开关,仅写出对话框选项 | FAQ§3.7-5e | inp 中额外写出人工边界单元并生成 *.vload 文件，由官网/技术支持提供的子程序在 ABAQUS 处理 | GFE-FAQ |
| ③ | 几何导出 | - | 无几何导出 API | UG§1.2.2(3) | 文件菜单—导出—导出几何 | GFE-UserGuide |
| ③ | 导入质量校验（prep_notes.txt） | - |  | FAQ§1.10 | 导入后在 YDB 路径自动生成 prep_notes.txt，sum 行=总质量(1.0恒+0.5活)，与 YJK wmass.out 对比 | GFE-FAQ |
| ③ | 导入选项记忆（prop.txt） | - |  | FAQ§1.11 | 主目录下自动生成 prop.txt 记录上次导入设置，存在时二次导入默认沿用 | GFE-FAQ |
| ③ | 自动生成数据说明文档 | - |  | FAQ§1.12 | 导入自动生成的数据信息详见用户手册附录三 | GFE-FAQ |
| 未知 | GFE 文件系统 10 种文件类型 | - |  | UG附录一 p273-274 | pre / stp·step / YJK模型目录 / gmat / inp / inpx / feasta / db / gjdy / chklog 的角色定义 | GFE-UserGuide |

## D10 后处理与输出（188 项：①52 ②14 ③121 未知1）

| 层 | 能力 | API入口 | 断点/理由 | 出处 | 说明 | 源手册 |
|---|---|---|---|---|---|---|
| ① | *Contact Output 接触输出 | - |  | UG附录二(7) p307 | 接触子输出，surface 与 general contact 互斥 | GFE-UserGuide |
| ① | *Element Output 单元输出 | - |  | UG附录二(7) p306 | 单元子输出，elset 缺省=整个模型 | GFE-UserGuide |
| ① | *Energy Output 能量输出 | - |  | UG附录二(7) p306 | 能量子输出，仅归属 *Output, history | GFE-UserGuide |
| ① | *Integrated Output 统计量输出 | - |  | UG附录二(7) p307 | 统计量子输出，仅归属 *Output, history；surface 与 elset 互斥 | GFE-UserGuide |
| ① | *Node Output 节点输出 | - |  | UG附录二(7) p306 | 节点子输出，nset 缺省=整个模型 | GFE-UserGuide |
| ① | *Output 输出请求 | - |  | UG附录二(7) p306 | 场/历程输出总请求，归属 *Step | GFE-UserGuide |
| ① | *Time Points 自定义输出时间序列 | - |  | UG附录二(7) p307 | 顶层关键字，自定义输出时间点（generate 或显式列点） | GFE-UserGuide |
| ① | GFE 特有能量分量 VELDAMP/DISPDAMP | energy_output.variables 可请求 |  | Iso§2.2.3表2.2.3 | 速度型阻尼器耗能（VELDAMP）与位移型阻尼器耗能（DISPDAMP）单列输出，区别于"软件A"（国际通用有限元软件）的归并口径 | GFE-Iso |
| ① | Mises 应力云图 | - |  | Imp第一章各节/§2.2 | S, Mises | GFE-Implicit |
| ① | NFORC1/NFORC2 场输出变量 | element_output.variables 可请求 |  | FAQ§3.8-4 | GFE 专有节点力场输出设置（ABAQUS 不支持） | GFE-FAQ |
| ① | 上/下包络（envmax/envmin） | output_request type=2 包络命令流可设 |  | UG§2.5.4(3) | 一系列 XY 数据求上/下包络 | GFE-UserGuide |
| ① | 两节点相对位移（顶-底位移差）时程输出 | - |  | Explicit§12.5.1 | Node_7821 与 Node_14246 位移差时程曲线 | GFE-Explicit |
| ① | 主控点位移时程输出 | node_output 历史输出请求可达 |  | Explicit§4.5 | 约束主控点（参考点）位移结果 | GFE-Explicit |
| ① | 位移云图（分量/Magnitude） | - |  | Imp第一章各节/§2.2 | 全场位移输出 | GFE-Implicit |
| ① | 包络（MAX）场输出 | output_request type=2 包络 |  | Iso§2.2.3 | 在 MAX 后缀场输出请求中同样勾选 SE/SF/SM，生成时程最大值包络输出 | GFE-Iso |
| ① | 单元场变量清单 | - |  | Cases§6.10.2 | DAMAGEC/DAMAGET/DELTAP/DUCTCRT/E/ELEN/EMSF/EVOL/IsRemoved/LE/PE/PEEQ/PEEQT/PEEQ_ | GFE-Cases |
| ① | 单元应力时程曲线（S11/S33/S13） | - |  | Imp§2.2.7-2.2.9 | 指定单元应力分量随时间曲线 | GFE-Implicit |
| ① | 单元输出 element_output | output.element_output |  | Cmd§2.15.3 | variables 如 ['DAMAGEC','DAMAGET']；reg_type -1/0/2（2=单元集） | GFE-Cmd |
| ① | 历史输出请求 | - |  | Cases§1.2.4; UG§1.15.2 | 与场输出同框架的独立树节点；手册明文"可以加速提取结果" | GFE-Cases+GFE-UserGuide |
| ① | 历史输出请求能量输出（ALLEN） | energy_output ALLEN 命令流可请求 |  | Iso§2.2.3图2.2.3.2 | 右击【历史输出请求】勾选 ALLEN（All energy）；可选变量含 ALLEN/ALLIE/ALLPD/ALLSE/ALLVD/ALLKE/ALLAE；时 | GFE-Iso |
| ① | 反力云图（RF/RF1） | - |  | Imp§2.1.1/§2.2 | 节点反力分量 | GFE-Implicit |
| ① | 变形缩放云图（变形系数） | - |  | Explicit§2.7-2.8 | 云图显示支持变形缩放系数 | GFE-Explicit |
| ① | 地面反力时程输出（接触反力合力） | integrated/contact_output 请求可达 |  | Explicit§4.4.2 | 刚性地面法向反力时程曲线 | GFE-Explicit |
| ① | 场输出/包络输出请求 | - |  | UG§1.15.2 | 时间间隔/间隔数/频率三种输出频率；子输出 5 类 | GFE-UserGuide |
| ① | 场输出/历史输出请求（模型树节点） | GFE.Pre.output 模块 |  | FAQ§3.1 | 模型树含"场输出请求""历史输出请求"节点 | GFE-FAQ |
| ① | 场输出管理器 field_mgr() | output.field_mgr |  | Cmd§2.15.6 | 获取场输出管理器 | GFE-Cmd |
| ① | 场输出请求手动创建（子输出体系） | - |  | Cases§1.2.4 | 子输出物理量类型五选一：节点/单元/能量/接触/统计量；每条单独配区域+变量 | GFE-Cases |
| ① | 场输出请求设置 | output_request+field_mgr 命令流 |  | SSA§3.1.9 | Time interval 输出间隔；Add 子输出分 Node/Element，Symbol 勾选输出变量 | GFE-SSA |
| ① | 场输出请求设置（SE/SF/SM） | element_output.variables 含 SE/SF/SM |  | Iso§2.2.3 | 在 ALL 后缀场输出请求勾选 SE/SF/SM（截面变形/截面力/截面弯矩），供阻尼器/支座内力变形输出 | GFE-Iso |
| ① | 塑性应变输出（PE11/PE22/PE12、PEEQ） | - |  | Explicit§2.2.1 | 单元塑性应变分量时程 | GFE-Explicit |
| ① | 塑性输出量 PE/PEEQ 时程 | - |  | Imp§2.4.2.3/§2.4.2.4 | PE31/PE33、PEEQ，判定进塑性时刻 | GFE-Implicit |
| ① | 壳单元内力输出 SF1/SF2/SM1/SM2 | - |  | Explicit§1.3.1 | 局部坐标内力分量；精确语义已于 P1.5 经附录补齐（见 ③-3.22）：壳 SF=单位长度截面力、SM1/SM2 下标与 t1/t2 轴交叉；⚠ 与 c01  | GFE-Explicit |
| ① | 壳单元局部坐标系自动约定与全套输出量 | - |  | Explicit附录(2) | 坐标系 (t1,t2,n)：t1 由全局 x 轴（壳面⊥x 时改用 z 轴）在壳面内投影确定、n 由节点顺序右手定则确定；输出 SF1-5/SM1-3/SE1- | GFE-Explicit |
| ① | 孔压 POR 输出 | 输出请求 variables 含 POR |  | Imp§1.5.1/§1.5.2 | 渗流结果场名为 POR | GFE-Implicit |
| ① | 孔压比时程输出 | SDV 历史输出请求可达 |  | Explicit§2.6.1 | 孔压比 0→1.0（完全液化）全过程 | GFE-Explicit |
| ① | 应力/应变分量输出（Mises、S11/S13/S22/S33、最大主应变、LE/E22） | - |  | Explicit§1.2 | 单元级标量场时程与云图 | GFE-Explicit |
| ① | 截面弯矩 SM1 输出 | element_output.variables 含 SM |  | Imp§1.3.1 | 纤维梁截面弯矩 | GFE-Implicit |
| ① | 损伤场输出（SDEG / DAMAGEC / DAMAGET） | element_output.variables 可请求 |  | Explicit§2.9.2 | 陶瓷损伤、混凝土受压/受拉损伤云图；软件A 同物理量名 SDV_Damage；补块新增受拉损伤变量名 DAMAGET（图例逐字 `DAMAGET, DAMAGE | GFE-Explicit |
| ① | 接触输出 contact_output | output.contact_output |  | Cmd§2.15.5 | reg_type 3=通用接触 4=表面；general_contact 布尔 | GFE-Cmd |
| ① | 支反力输出 RF1/RF2/RF3（单点+合力时程） | - |  | Explicit§2.1起 | 节点反力与支座合力（如底部 RF1 合力） | GFE-Explicit |
| ① | 支座反力合力曲线（RF1 合力） | - |  | Imp§2.2.7-2.2.9 | 底部支座节点集 RF1 求合 | GFE-Implicit |
| ① | 最大主应变/最大塑性主应变/LE Max. Principal 云图 | - |  | Imp第一章各节/§2.2.2/§2.2.3 | 对数应变最大主值 | GFE-Implicit |
| ① | 枚举全部输出请求 field_mgr().find_all() | output.field_mgr.find_all |  | Cmd§2.15.7 | 返回所有场输出请求对象列表（模型感知/反编译可用） | GFE-Cmd |
| ① | 梁单元内力输出（剪力/弯矩） | - |  | Explicit§1.1.1.1 | 按单元号输出 Y 向剪力、X-Y 平面弯矩 | GFE-Explicit |
| ① | 梁单元局部坐标系用户自定义（n1 向量）与全套输出量 | - |  | Explicit附录(1) | 坐标系 (n1,n2,t)，需在全局坐标系定义 n1 向量；输出 SF1-3/SM1-3/SE1-3/SK1-3/S11/S12（逐字定义见 ③-3.22） | GFE-Explicit |
| ① | 滞回曲线输出（应力-应变 / 连接器 SE-SF） | - |  | Explicit§2.6 | 液化滞回环退化、连接器变形-力滞回 | GFE-Explicit |
| ① | 能量输出 energy_output | output.energy_output |  | Cmd§2.15.4 | per_element_set 控制是否按单元集分别输出 | GFE-Cmd |
| ① | 节点位移/时程输出与云图（U, Magnitude） | - |  | Explicit全书 | 按节点号提取位移分量/时程；云图 | GFE-Explicit |
| ① | 节点场变量清单 | - |  | Cases§6.10.1 | ISTIE/IWCONWEP/P/POR/RF/RM/U/UR/V/VR；选择模式 自定义/所有/预选/清除 | GFE-Cases |
| ① | 节点输出 node_output | output.node_output |  | Cmd§2.15.2 | variables 如 ['A','V']；reg_type -1=整个模型 0=几何集 1=节点集 | GFE-Cmd |
| ① | 输出时间间隔/按频率输出 | - |  | Cases§3.2.2 | 时间选项"频率"=输出间隔语义（非 Hz）；FEM-SPH 须与 SPH 输出间隔一致 | GFE-Cases |
| ① | 输出请求 output_request（场/历史/包络） | output.output_request |  | Cmd§2.15.1 | type 0=场 1=历史 2=包络；时间间隔/间隔数/频率/时间点列表多种触发方式；sub_output 挂子输出 | GFE-Cmd |
| ② | XY 数据—提取历史输出数据 | - | .db 为 SQLite 可脚本直读;GUI 提取器无 API | UG§2.5.4(2) | 从历史输出记录直接存为 XY 数据 | GFE-UserGuide |
| ② | XY 数据—提取场输出数据 | - | .db 为 SQLite 可脚本直读;GUI 提取器无 API | UG§2.5.4(1) | 按帧、物理量、区域（标签/节点集/单元集）提取曲线 | GFE-UserGuide |
| ② | 内力/单元级时程曲线提取 | - | .db 为 SQLite 可脚本直读;GUI 提取器无 API | SSA§3.3.1/§6.2.1 | 典型部位时程曲线；3D 按单元号（如柱4498050、楼板4503337）提取轴力/弯矩时程 | GFE-SSA |
| ② | 单元拾取查询 | - | 数值可 .db 直读;拾取为 GUI 交互 | Iso§2.2.4截图 | 后处理中右键点选单元显示：内部ID/标签/类型(S4R、CONN3D2)/材料/截面属性/YJK构件ID | GFE-Iso |
| ② | 场变量 XY 时程曲线提取 | - | .db 为 SQLite 可脚本直读;GUI 提取器无 API | Iso§2.2.4 | 【XY数据】→XY数据管理器→创建→场变量输出：勾选变量(SE1/SE2/SE3/SF1/SF2/SF3…)，区域填单元标签或图形区选中后【来自选择】，保存 | GFE-Iso |
| ② | 场查询 | - | 场数值可 .db 直读;查询界面 GUI | UG§2.5.2 | 输出当前云图场类型、范围、最值点/单元编号、当前帧号 | GFE-UserGuide |
| ② | 声压输出 POR（时程+云图） | - | POR 请求可命令流;云图查看 GUI | Explicit§1.5.1-1.5.3 | 节点声压时程；云图变量名 POR | GFE-Explicit |
| ② | 孔压比云图（SDV）与单元孔压比时程 | - | SDV 时程 .db 可读;云图 GUI | SSA§3.5.2/§6.4.2 | 液化分析输出 SDV 孔压比云图及指定单元孔压比时程曲线 | GFE-SSA |
| ② | 拾取节点响应曲线 | - | 节点时程 .db 直读;拾取为 GUI | Cases§3.2.7 | 点选节点生成响应曲线 | GFE-Cases |
| ② | 时程包络云图（时程最大值/最小值分布） | - | 包络场可命令流请求;云图查看 GUI | SSA§6.2.1 | 输出内力"时程最大值分布""时程最小值分布"两类包络云图 | GFE-SSA |
| ② | 模态结果查看（频率+振型） | - | 频率/振型数据 .db 可读;界面查看 GUI | Cases§1.3.3 | 状态栏"帧: N; 频率: x.xxx"+振型动画 | GFE-Cases |
| ② | 网格查询 | - | 网格信息可命令流/.db 读;查询界面 GUI | UG§2.5.2 | 输出节点数、单元数、单元类型及各类型数量 | GFE-UserGuide |
| ② | 能量曲线查看（历程变量输出） | - | 能量历程 .db 可直读;曲线界面 GUI | Iso§2.2.5/§4.4.4图4.4.4 p52 | XY数据管理器→创建→勾选历程变量输出→保存能量结果并绘制；案例四同窗叠绘 ETOTAL/ALLVD/DISPDAMP 三条能量时程 | GFE-Iso |
| ② | 频响实部/虚部曲线 | - | 频响数据 .db 可读;曲线界面 GUI | Cases§3.2.7 | 同节点自动生成 U:Magnitude:N* 与 _Imginary 两条曲线 | GFE-Cases |
| ③ | CAD 配筋图纸生成（消能子结构/中震工况组合） | - | 图纸/报告向导 GUI 专属 | Iso§4.4.7图4.4.7.2 p55/§5.3.4 p61 | 输出消能子结构逐层 CAD 配筋设计信息图；"GFE 可通过不同的工况组合生成设计师需要的中震工况下结构模型的 CAD 配筋图纸" | GFE-Iso |
| ③ | DWG 图导出（包络工况） | - | DWG 导出为后处理 GUI | FAQ§4.6/4.9 | 输出 dwg 内力/配筋图，仅为所有组合工况的包络输出 | GFE-FAQ |
| ③ | DualSPHysics 流体结果单独显示 | - | 后处理界面专属,无命令流/Post API | UG§2.7 p264 | 后处理直接打开 DualSPHysics vtk 文件，无需打开 db；入口：Ribbon「流体动力」页面卡 | GFE-UserGuide |
| ③ | SPH vtk 结果查看 | - | 后处理界面专属,无命令流/Post API | Cases§8.7 | 后处理"流体动力"页打开"作业名_out/particle"内 vtk（流体选 _Fluid 后缀） | GFE-Cases |
| ③ | VC 振级计算（rms_velo） | - | 振级为 XY 运算 GUI 函数 | UG§2.5.4(3) | 速度时程→VC 振级 | GFE-UserGuide |
| ③ | XY 数据复制到 DB/从 DB 加载/导出 | - | XY 管理器界面专属 | UG§2.5.4图 | 管理器含"复制到DB""从DB加载""导出(测试)"按钮 | GFE-UserGuide |
| ③ | XY 数据管理器 | - | XY 管理器界面专属 | Cases§3.2.7 | 创建/编辑/删除/绘制/复制到DB/从DB加载/导出 | GFE-Cases |
| ③ | XY 数据运算函数库 | - | XY 运算为后处理 GUI 函数库 | Iso§2.2.4截图 | +、-、*、/、abs(A)、combine(X1,X2)、envmax(X_…)、envmin(X_…)、fft(X) 等运算符可添加到表达式 | GFE-Iso |
| ③ | XY 数据运算（表达式） | - | XY 运算为后处理 GUI 函数库 | UG§2.5.4(3) | 加减乘除/abs/combine/envmax/envmin/fft/log/pow/sum/振级/噪声/反应谱等函数 | GFE-UserGuide |
| ③ | XY 绘图对数刻度切换 | - | 绘图界面设置 | UG§2.5.4(6) | 右键"普通/对数坐标轴"，X 轴线性⇄对数（底 10） | GFE-UserGuide |
| ③ | Z 振级计算（vlz_1985/vlz_1997） | - | 振级为 XY 运算 GUI 函数 | UG§2.5.4(3) | 加速度时程→Z 振级，按 ISO 2631-1:1985 / 1997 | GFE-UserGuide |
| ③ | db+vtk 联合显示（流固叠加） | - | 后处理界面专属,无命令流/Post API | Cases§9.8 | 同窗口打开 FEM db 与 SPH vtk | GFE-Cases |
| ③ | word 查看报告与占位符修改 | - |  | UG§2.6.5 p262 | 点"word"查看报告；需自定义处以 *XXX* 格式标红，用通配符 >\**\*< 查找 | GFE-UserGuide |
| ③ | 二次结构噪声计算（noise1/noise2） | - | 噪声为 XY 运算 GUI 函数 | UG§2.5.4(3) | 速度时程→1/3 倍频程声压级（_Lp）+最大等效连续 A 声级（_LAeq）；noise1 标准房间、noise2 其他房间 | GFE-UserGuide |
| ③ | 云图动画播放 | - | 云图/动画为后处理界面专属 | Cases§3.2.7; UG§2.3.4 | 循环播放/间隔时间（默认 20ms，施工动画建议调大）/帧控制 | GFE-Cases+GFE-UserGuide |
| ③ | 云图区间放缩（线性/对数底10） | - | 云图设置为后处理界面专属 | UG§2.3.1(1) | 色标区间线性或以 10 为底对数划分 | GFE-UserGuide |
| ③ | 云图变形缩放显示（变形系数） | - | 云图设置为后处理界面专属 | Imp§2.2.7.2/§2.2.8.2/§2.2.9.2 | 位移云图按系数（算例 0.25）缩放显示 | GFE-Implicit |
| ③ | 云图显示类型切换（原始/平滑） | - | 云图设置为后处理界面专属 | UG§2.3.1(2) | 原始=单元单色；平滑=按节点相邻单元均值插值着色 | GFE-UserGuide |
| ③ | 云图查看（变量切换+变形系数） | - | 云图查看为后处理界面专属 | Cases§1.3.3 | 选场输出变量（U Magnitude 等）；云图位移按"变形系数"自动放大 | GFE-Cases |
| ③ | 云图标量条设置 | - | 云图设置为后处理界面专属 | Cases§2.3.4 | 标题/标签字号、粗体、小数位、颜色 | GFE-Cases |
| ③ | 云图自定义范围+平滑 | - | 云图设置为后处理界面专属 | Cases§6.13.3 | PE Max.Principal 自定义 0–0.0003 并平滑 | GFE-Cases |
| ③ | 云图颜色范围（当前/历史/自定义） | - | 云图设置为后处理界面专属 | UG§2.3.1(1) | 色标 min/max：当前帧范围 / 全时程范围 / 用户指定 | GFE-UserGuide |
| ③ | 仅显示梁、壳单元（显示过滤） | - | 显示过滤为后处理界面专属 | UG图2.2.8-1 | 过滤只看梁/壳单元（仅图题证据，操作路径在截图） | GFE-UserGuide |
| ③ | 位移云图与变形放大显示 | - | 云图显示为后处理界面专属 | SSA§3.3.2/§4.2.2/§5.2.2 | 整体/结构水平位移云图，支持设置变形放大倍数（500×/200×） | GFE-SSA |
| ③ | 作业管理器：查看计算结果 | - | 作业管理器结果查看 GUI | FAQ§5.4 | 计算完成（提示 success）后从作业管理器进入结果查看 | GFE-FAQ |
| ③ | 保存动画 | - | 动画保存为 GUI 操作 | UG§2.3.4(4) | 动画导出保存 | GFE-UserGuide |
| ③ | 内力云图（剪力/弯矩）与典型部位取值 | - | 云图/取值为后处理界面专属 | SSA§3.3.1/§4.2.1/§5.2.1 | 梁单元剪力/弯矩云图、顶板端部/侧墙顶底/底板端部取值 | GFE-SSA |
| ③ | 减隔震报告书一键生成 | - | 报告书向导 GUI | Iso前言 | 前言列为专项新功能之一（本块未给操作细节） | GFE-Iso |
| ③ | 分频振级计算（val） | - | 振级为 XY 运算 GUI 函数 | UG§2.5.4(3) | 加速度时程→分频振级 | GFE-UserGuide |
| ③ | 切割平面编辑与直接编辑模式 | - | 切割编辑为后处理界面专属 | UG§2.4.2 | 编辑切割面中心点与法向；辅助平面拖拽调整、支持偏移 | GFE-UserGuide |
| ③ | 切割显示（平面剖切） | - | 剖切显示为后处理界面专属 | UG§2.4.2 | 隐函数（暂只支持平面）裁剪；正面/背面/中间切片三种结果 | GFE-UserGuide |
| ③ | 前/后处理模块切换 | - | 界面切换操作 | Cases§1.3.3 | 右上方"后处理"按钮/"返回前处理"，同进程切换；打开对象为 .db | GFE-Cases |
| ③ | 剖面切片后处理 | - | 切片显示为后处理界面专属 | Explicit§6.2.2 | 隧道中心剖面位移云图提取 | GFE-Explicit |
| ③ | 动画播放模式 | - | 动画设置为后处理界面专属 | UG§2.3.4(2) | 单次/循环/反向循环/摆动 四种 | GFE-UserGuide |
| ③ | 动画播放速度设置 | - | 动画设置为后处理界面专属 | UG§2.3.4(1) | 帧间隔时间，下限 20 毫秒 | GFE-UserGuide |
| ③ | 压强变化云图（爆炸过程） | - | 云图为后处理界面专属 | Explicit§6.1.2.2 | 爆炸作用面压强云图随时间输出 | GFE-Explicit |
| ③ | 反应谱计算（spectrum） | - | 谱计算为 XY 运算 GUI 函数 | UG§2.5.4(3) | 加速度时程→a/v/u 时程及 a-T/v-T/u-T 反应谱共 6 组 | GFE-UserGuide |
| ③ | 变形显示与变形系数 | - | 变形显示为后处理界面专属 | UG§2.2.2 | 未变形/变形/同时显示；系数 自动计算/一致/非均匀（XYZ 各自） | GFE-UserGuide |
| ③ | 后处理帧导出 vtu/vtk | - | 帧导出按钮 GUI 专属 | UG§2.9 p267 | 各帧导出为 vtu 或 vtk；「导出」按钮在 ribbon 栏最右侧；可勾选帧、选类型（节点/单元等）、选物理量 | GFE-UserGuide |
| ③ | 后处理渲染风格组合 | - | 渲染设置为后处理界面专属 | UG§2.2.1 | 渲染风格（点/框线/表面）×可见边缘（全部/外部/特征/没有） | GFE-UserGuide |
| ③ | 后处理窗口部件显隐 | - | 窗口部件设置 GUI | UG§2.1.1 | 文件菜单—视图，显隐树状列表/信息/输出等停靠窗口 | GFE-UserGuide |
| ③ | 后处理背景颜色 | - | 背景设置 GUI | UG§2.2.3 | Ribbon-「显示」设置-「背景」页面卡 | GFE-UserGuide |
| ③ | 后处理自定义场（SRSS/CQC 模态组合） | - | 自定义场为后处理 GUI 功能 | Imp§3.5.2 | 组合结果由用户在后处理"自定义场"中组合，非求解器输出 | GFE-Implicit |
| ③ | 后处理视角切换与旋转 | - | 视角操作为后处理界面专属 | UG§2.1.2(2) | 正等轴测/六视图按钮；自动调整视图、平行投影开关、水平/垂直/时针旋转 | GFE-UserGuide |
| ③ | 后处理鼠标交互 | - | 鼠标交互为界面专属 | UG§2.1.2(1) | 左键拖动旋转、中键拖动平移、滚轮缩放、右键拖动放大缩小、单击拾取 | GFE-UserGuide |
| ③ | 响应谱 SRSS 组合位移场 srssU | - | SRSS 组合场为后处理 GUI 功能 | Imp§6.3.3图6.3.2-4 p166 | 响应谱云图变量名为 srssU, Magnitude 而非 U——与既有「SRSS/CQC 后处理自定义场手工组合」表面冲突，见⑤待仲裁#1 | GFE-Implicit |
| ③ | 固液包络色标自动计算 | - | 色标计算为后处理界面专属 | UG§2.7 p264 | 固液同显时按双方物理量最大/最小值自动算包络区间作云图色标范围 | GFE-UserGuide |
| ③ | 壳单元真实厚度拉伸显示 | - | 厚度拉伸显示为界面专属 | UG§2.2.9 | 按壳真实厚度渲染，同一入口同一勾选项 | GFE-UserGuide |
| ③ | 多组 XYData 批量运算 | - | 批量运算为 XY 管理器 GUI | UG§2.5.4(4) | 多个 XY 数据导入待算列表按所选函数批量执行 | GFE-UserGuide |
| ③ | 导出场地反应结果 | - | 导出按钮 GUI 专属 | UG§2.6.3 | 地下结构——导出场地反应结果 .txt | GFE-UserGuide |
| ③ | 导出计算书 | - | 计算书向导 GUI | FAQ§4.4 | 自动生成计算书（依赖 Office/WPS） | GFE-FAQ |
| ③ | 层间位移角/位移结果输出 | - | 内置层间统计为后处理 GUI | Cases§10.15 | 按层输出 Displacement（手册给 8 层数值表） | GFE-Cases |
| ③ | 层间位移角/层间剪力/导出场地反应结果/自动截图 | - | 内置层间统计/截图为后处理 GUI | FAQ§4.6 | 土木工程后处理功能区：层间位移角、层间剪力、导出层间位移角、导出场地反应结果、自动截图、生成计算书 | GFE-FAQ |
| ③ | 层间位移角后处理 | - | 内置层间统计为后处理 GUI | Iso§3.3.1/§3.4.1/§5.3.1图5.3.1/§5.4.1图5.4.1 | 输出各层层间位移角曲线及最大值，对照 1/550（弹性）与 1/50（弹塑性）限值；隔震案例同窗叠绘 JZ/NOJZ 曲线并加 1/500（中震）或 1/100 | GFE-Iso |
| ③ | 层间位移角导出 | - | 内置层间统计为后处理 GUI | UG§2.6.1(2) | 地下结构——导出层间位移角，输出各层时程+包络 .txt | GFE-UserGuide |
| ③ | 层间位移角查看 | - | 内置层间统计为后处理 GUI | UG§2.6.1(1) | 按层节点集（仅层底+层顶节点）计算各层层间位移角 | GFE-UserGuide |
| ③ | 层间位移角输出（含时程曲线） | - | 内置层间统计为后处理 GUI | SSA§3.3.2/§4.2.2(b)/§6.2.2(b) | 输出结构各层层间位移角及其时程曲线 | GFE-SSA |
| ③ | 层间剪力后处理 | - | 内置层间统计为后处理 GUI | Iso§3.3.2/§3.4.2/§5.3.2图5.3.2/§5.4.2图5.4.2 | 输出各层层间剪力曲线及最大值，减震/隔震前后对比 | GFE-Iso |
| ③ | 层间剪力查看 | - | 内置层间统计为后处理 GUI | UG§2.6.2 | 按层单元集（仅层底单元）基于 NFORC 输出计算层间剪力 | GFE-UserGuide |
| ③ | 工况文件路径配置表 | - | 报告配置对话框 GUI | UG§2.6.5 p260 | 按行配置 CaseType / CaseName / DB / GJDY / Soil / Valid / End；路径下须含工况 inp 及结果 db | GFE-UserGuide |
| ③ | 工况系数组合对话框（报告） | - | 报告配置对话框 GUI | UG§2.6.5 p260-261 | 工况选择完后弹出 load combination table，可修改组合系数；"type"为规范组合类型（基本、准永久等） | GFE-UserGuide |
| ③ | 工况组合系数表编辑 | - | 报告配置对话框 GUI | UG§2.6.4 p258 | 配筋/轴压比模块中按工况（Dead/E2Y/E2Yb/E2Yc/Live）编辑组合系数矩阵，每行带「类型」列（基本） | GFE-UserGuide |
| ③ | 快速傅里叶变换（fft） | - | FFT 为 XY 运算 GUI 函数 | UG§2.5.4(3) | 对选中 XY 数据做 FFT | GFE-UserGuide |
| ③ | 报告书类型选择 | - | 报告向导 GUI | UG§2.6.5 p259 | 正文称支持三种：反应位移法/弹性地震/塑性地震报告书；选择对话框实列 Response / UnderElastic / UnderPlastic / abso | GFE-UserGuide |
| ③ | 报告云图查看 | - | 报告云图查看 GUI | UG§2.6.5 p261 | 生成报告时主对话框同步生成云图展示（UnderM_Col / UnderM_DispX/Y / UnderM_MomX/Y / UnderM_Pi / Unde | GFE-UserGuide |
| ③ | 拾取输出选项 | - | 拾取选项为界面交互 | UG§2.5.1 | 单选：内部编号/形状/类型/数据/材料/截面属性/截面属性集合/YJK 构件编号；框选：材料/截面属性/求和/超限转 txt | GFE-UserGuide |
| ③ | 拾振点加速度时程与 1/3 倍频程计权加速度级 VL(dB) 后处理 | - | 振级后处理 GUI 计算 | Explicit§11.2 | 各层室内地面中央拾振点垂向加速度时程 + 计权加速度级 VL（1-80Hz），与实测对比 | GFE-Explicit |
| ③ | 按阈值过滤（单元移除显示） | - | 阈值过滤显示为界面专属 | UG§2.5.5 | 每帧数据落在阈值区间内的单元移除；可显示被移除单元粒子（灰点） | GFE-UserGuide |
| ③ | 按阈值过滤（状态变量） | - | 阈值过滤显示为界面专属 | Cases§6.13.1 | 勾"使用状态变量"（如 IsRemoved）设最小/最大值滤掉被移除单元 | GFE-Cases |
| ③ | 振型云图输出 | - | 振型云图为后处理界面专属 | Explicit§1.x.2 | 前 N 阶频率表+振型位移云图 | GFE-Explicit |
| ③ | 损伤云图（受拉/受压破坏） | - | 损伤云图为后处理界面专属 | Cases§14.10 | DAMAGET/DAMAGEC 云图，色标 0~5.00E-01 | GFE-Cases |
| ③ | 损伤等级阈值设置 | - | 阈值设置为界面专属 | UG§2.6.7 p263 | 性能评价对话框「设置」分页可设各损伤等级、各构件类型阈值，一般按默认 | GFE-UserGuide |
| ③ | 效应组合、截面验算、配筋、生成计算书 | - | 设计验算/计算书 GUI 向导 | Imp前言行246 | 构件设计后处理 | GFE-Implicit |
| ③ | 显示参考点/边界/文本信息 | - | 显示开关为界面专属 | UG§2.2.7 | 「其他」页面卡；可调符号大小、文本大小与颜色 | GFE-UserGuide |
| ③ | 构件性能评价 | - | 性能评价为后处理 GUI 功能 | UG§2.6.7 p262-263 | 基于单元损伤结果（DAMAGEC、DAMAGET）+ 构件-单元关联（.gjdy）计算构件级损伤，按预设阈值划 6 个等级（无损伤→严重损伤）；入口：后处理-- | GFE-UserGuide |
| ③ | 标量条文字与小数位设置 | - | 标量条设置 GUI | UG§2.3.1(3) | 标量条标题/标注字号、粗体、小数点位数 | GFE-UserGuide |
| ③ | 树状列表选中高亮联动 | - | 界面联动交互 | UG§2.4.1 | 树选中集合/材料/荷载/相互作用即高亮其载体区域 | GFE-UserGuide |
| ③ | 梁、壳单元局部坐标系显示 | - | 坐标系显示为界面专属 | UG§2.2.8 | "完整坐标系"与"根据物理量而定"两模式；滑动条缩放坐标轴 | GFE-UserGuide |
| ③ | 梁单元真实截面形状拉伸显示 | - | 截面拉伸显示为界面专属 | UG§2.2.9 | 按梁真实截面渲染；入口：「显示」设置→「其他」页卡→勾"显示截面"；默认关闭 | GFE-UserGuide |
| ③ | 楼板混凝土损伤云图（分层爆炸显示） | - | 损伤云图显示为界面专属 | Iso§4.4.6图4.4.6(c)(d) p54 | 减震前/后逐层楼板 DAMAGEC 云图对比，分层爆炸显示 | GFE-Iso |
| ③ | 流体+固体共同显示 | - | 联合显示为界面专属 | UG§2.7 p264 | 打开 db 并将流体分析变量与场输出变量设置一致（当前物理量只有速度），固液同屏 | GFE-UserGuide |
| ③ | 流体多帧动画播放 | - | 动画播放为界面专属 | UG§2.7 p264 | 「打开」按钮选 vtk 目录、列表多选；帧顺序按列表从上到下；有固体结果时固液帧同步切换 | GFE-UserGuide |
| ③ | 流体物理量手动对应 | - | 物理量对应为界面交互 | UG§2.7 p264 | DualSPHysics 与 GFE 物理量名称/单位可能不一致且不能自动匹配，允许手动指定对应 | GFE-UserGuide |
| ③ | 混凝土压/拉损伤云图 | - | 损伤云图为后处理界面专属 | SSA§3.4.1/§6.3.1 | 2D 整体云图；3D 按楼层/构件类型（梁、板、墙、柱）输出 | GFE-SSA |
| ③ | 混凝土损伤云图 | - | 损伤云图为后处理界面专属 | Iso§3.4.6/§4.4.6图4.4.6 p53-54/§5.4.5图5.4.5 p66 | 罕遇地震下梁柱构件损伤因子（DAMAGEC）云图；减震/隔震前后对比 | GFE-Iso |
| ③ | 滞回曲线合成（combine 运算） | - | combine 为 XY 运算 GUI 函数 | Iso§2.2.4图2.2.4/§4.4.3/§5.3.3/§5.4.3 | XY数据运算选 combine(X1,X2) 函数，把 SE、SF 两条时程合成力-位移滞回曲线；案例四阻尼器与第五章隔震支座 SF–SE 滞回环（ZH-X/Z | GFE-Iso |
| ③ | 生成配筋 DWG 图 | - |  | UG§2.6.6 p262 | 计算书/轴压比云图成功后产出 GfeDwg 中间文件（pj.pjb / pj.pje），AutoCAD2020 中 APPLOAD 加载 GfePJ2020.a | GFE-UserGuide |
| ③ | 简化轴压比计算 | - | 轴压比计算为后处理 GUI | UG§2.6.4 | 需结合 SF 包络场输出使用的快捷选项 | GFE-UserGuide |
| ③ | 简化轴压比计算选项 | - | 轴压比计算选项 GUI | FAQ§4.8 | 勾选后只读时程分析工况的包络输出（SF/SM）结果 | GFE-FAQ |
| ③ | 结构层间位移角结果输出 | - | 内置层间统计为后处理 GUI | Imp§3.5.2图3.5.2-9 | 反应谱与时程层间位移角对比 | GFE-Implicit |
| ③ | 结构层间位移（角）时程与峰值包络输出（分建筑/分地上地下） | - | 内置层间统计为后处理 GUI | Explicit§13.3.1 | 逐层最大层间位移角统计+包络曲线，用于规范限值与对比软件比对 | GFE-Explicit |
| ③ | 结构构件设计与计算书生成 | - | 设计/计算书向导 GUI | SSA前言行138 | 基于 GFE 结果做效应组合、截面验算、配筋、生成计算书 | GFE-SSA |
| ③ | 缩放/谐波动画（单帧形变过程） | - | 动画显示为界面专属 | UG§2.3.4(3) | 全/半周期、线性/谐波系数模式、可设半周期帧数 | GFE-UserGuide |
| ③ | 能量堆叠图 | - | 堆叠图为后处理 GUI 绘图 | UG§2.8 p266 | 时程能量堆叠图；入口：Ribbon「其他」页卡「能量图」按钮；数据源 .BAEnH 文件；能量定义见减隔震分析技术手册 | GFE-UserGuide |
| ③ | 自动生成计算书 | - | 计算书向导 GUI | UG§2.6.5 p258-262 | 按所选工程结果生成 .docx；需装 Office Word/Excel 或 WPS；不需打开 db、只需切到后处理模块；入口：工程——生成计算书；目标路径须同 | GFE-UserGuide |
| ③ | 自动调整视图开关 | - | 视图开关 GUI | UG§2.4.1技巧2 | 布尔运算后自动缩放视图，可取消勾选 | GFE-UserGuide |
| ③ | 自定义 XY 数据（手工输入） | - | 手工输入为界面交互 | UG§2.5.4(5) | 手工输入 XY 表格；勾"接受复数"可输 a+bi；支持复制/粘贴 | GFE-UserGuide |
| ③ | 自定义动画时间轴 | - | 动画时间轴为界面设置 | UG§2.3.4(5) | 自选播放帧（所有帧或自定义子集，带规律选择辅助） | GFE-UserGuide |
| ③ | 自定义场结果查看 | - | 自定义场查看为后处理 GUI | UG§2.5.3(3)d | 场=Custom → 自定义场名 → 变量 | GFE-UserGuide |
| ③ | 自定义场（对多帧取值） | - | 自定义场为后处理 GUI 功能 | UG§2.5.3(2) | min/max/absmin/absmax（全时程逐点取值）及 CQC/SRSS（反应谱组合） | GFE-UserGuide |
| ③ | 自定义场（物理量帧操作） | - | 自定义场为后处理 GUI 功能 | UG§2.5.3(1) | 多帧间计算（需帧数对齐）或多帧对单帧；+ - * / abs pow log | GFE-UserGuide |
| ③ | 自定义编号（节点/单元别名） | - | 别名编号为界面功能 | UG§2.2.5 | 选节点/单元、设行数、输入标签与自定义编号（英文） | GFE-UserGuide |
| ③ | 节点/单元标签显示（双编号体系） | - | 标签显示为界面专属 | UG§2.2.4 | 标签分"内部"（0 起连续）与"Inp"（不保证 0 起/连续）两种 | GFE-UserGuide |
| ③ | 节点/单元鼠标拾取与编号输入拾取 | - | 拾取交互为界面专属 | UG§2.5.1 | 不拾取/拾取点/拾取单元三态；单击单选、Shift 框选、Ctrl 增选；可输编号 | GFE-UserGuide |
| ③ | 荷载组合后轴压比云图 | - | 轴压比云图为后处理 GUI | FAQ§4.6 | "土木工程-场输出"按工况组合查看构件轴压比云图（需 *.gjdy 文件） | GFE-FAQ |
| ③ | 视图窗口截屏 | - | 截屏为 GUI 操作 | UG§2.3.2 | Ribbon"截屏"，输入名称选路径 | GFE-UserGuide |
| ③ | 轴压比云图按组合切换 | - | 轴压比云图为后处理 GUI | UG§2.6.4 p258 | 后处理物理量切到轴压比（Comb1~Comb10 下拉），结合「过滤器」仅显示墙柱构件 | GFE-UserGuide |
| ③ | 轴压比云图生成 | - | 轴压比云图为后处理 GUI | UG§2.6.4 | 工程——场输出：选工程主目录自动搜工况，自动生成默认工况组合（可改系数），生成 ACR 轴压比云图 | GFE-UserGuide |
| ③ | 轴压比查看 / 轴压比云图-DWG 图（地震组合系数调整）（修订记录线索） | - | 轴压比/DWG 为后处理 GUI | FAQ修订记录 | 指向 §4.6/4.9，仅作能力线索不计入能力总数 | GFE-FAQ |
| ③ | 输出特定层轴压比 | - | 轴压比输出为后处理 GUI | UG§2.6.4 | "输出控制"分页设置仅输出特定层 | GFE-UserGuide |
| ③ | 输出请求加载预设 | - | 预设钮 GUI;命令流需显式列变量 | Cases§2.2.5 | 右键"加载预设"：静力 / 动力弹性 / 动力弹塑性 三套（弹塑性预设批量生成 FO-DynaPla-* / EO-DynaPla-*） | GFE-Cases |
| ③ | 输出请求预设 | - | 预设钮 GUI;命令流需显式列变量 | UG§1.15.2 | 右键"加载预设"：动力弹性/动力弹塑性/静力三套 | GFE-UserGuide |
| ③ | 过滤器布尔运算显示 | - | 过滤显示为界面专属 | UG§2.4.1 | 替换/添加/移除/相交/或/所有 六种布尔运算，支持 Undo/Redo | GFE-UserGuide |
| ③ | 过滤器（单元/节点/表面提取高亮） | - | 过滤显示为界面专属 | UG§2.4.1 | 按单元标签/单元集/单元形状/节点标签/单元类型/YJK 构件、节点集、表面集/绑定约束提取并高亮 | GFE-UserGuide |
| ③ | 过滤器（按集合 孤立/移除/布尔显示） | - | 过滤显示为界面专属 | Cases§2.3.4 | "单元-集合-xxx"+替换/增加/移除/相交/对称差；须点"替换"等执行钮 | GFE-Cases |
| ③ | 逐帧损伤饼图与等级云图 | - | 饼图/云图为后处理界面专属 | UG§2.6.7 p263 | 每帧损伤结果（饼图+损伤等级云图）；「动画」板块切帧饼图同步更新；饼图上方下拉框切构件类型 | GFE-UserGuide |
| ③ | 钢筋塑性应变云图（壳内 R_PE1/R_PE2；梁内 PE11） | - | 钢筋应变云图为后处理界面专属 | SSA§3.4.1/§6.3.1(e)(f) | 分层壳钢筋 1、2 方向塑性应变与梁柱钢筋塑性应变输出，变量异名 | GFE-SSA |
| ③ | 集合排序辅助（排序按钮） | - | 排序按钮为界面辅助 | UG§2.6.1(1)d | 名称前缀相同的集合按后缀数字升序排列 | GFE-UserGuide |
| ③ | 颜色设置（按材料/集合/单元类型分色） | - | 颜色设置 GUI | UG§2.3.3 | 图元 All/Element；属性 Material/Set/Type；场选 "Solid Color" | GFE-UserGuide |
| ③ | 高亮开关（性能优化） | - | 高亮开关 GUI | UG§2.4.1技巧1 | 大模型下关闭树状列表右上方高亮开关提高流畅度 | GFE-UserGuide |
| ③ | 高亮透视开关 | - | 高亮开关 GUI | UG§2.2.6 | 「显示」设置-「高亮」页面卡，高亮是否透视显示 | GFE-UserGuide |
| 未知 | 附录：梁和壳单元局部坐标与输出物理量定义 | - |  | Explicit附录 | 第1章全部内力数据（SF/SM 等）的语义真值源；已于 P1.5 经 PDF 直读补齐 p290-292，正文条目见 O 节、逐字转录见 ③-3.22 | GFE-Explicit |

## D11 特殊分析（59 项：①43 ②4 ③12）

| 层 | 能力 | API入口 | 断点/理由 | 出处 | 说明 | 源手册 |
|---|---|---|---|---|---|---|
| ① | Bouc-Wen 位移型阻尼器模拟 | connector_plastic kh_define=GFE BW |  | Iso§1.2.2/§2.2.1图2.2.1.7 | 连接器行为=弹性+塑性(定义方式 GFE BW：屈服力+刚度折减系数+屈服指数) | GFE-Iso |
| ① | C3D4P 三维孔压单元 基坑降水-开挖施工阶段耦合 | soils_step+case elemAdd/Del 命令流 |  | Imp§1.5.2 | 4 段开挖×4 阶段降水交替的应力-渗流分析 | GFE-Implicit |
| ① | CONWEP 爆炸荷载（Kingery-Bulmash 1984） | incident_wave_property type 0/1 CONWEP |  | Explicit§6.1 | 起爆点+作用面+爆炸类型+TNT当量 → 自动算到达时间/最大超压/超压时间/指数衰减因子；无需空气域 | GFE-Explicit |
| ① | CPE3P 二维孔压单元 应力-渗流耦合 | soils_step 固结/渗流命令流 |  | Imp§1.5.1 | 两步：①地应力平衡（含孔压边界）②稳态应力-渗流耦合 | GFE-Implicit |
| ① | Kelvin 速度型阻尼器模拟 | connector_elastic+damping 并联可建 |  | Iso§1.2.1/§2.2.1图2.2.1.5 | 弹簧+阻尼并联；单个连接器行为，阻尼类型选 GFE DAMP2（阻尼系数+阻尼指数） | GFE-Iso |
| ① | Maxwell 速度型阻尼器模拟 | connector_damping VISCOUS |  | Iso§1.2.1/§2.2.1图2.2.1.4 | 弹簧+阻尼串联；需创建两个连接器行为（弹性、阻尼）分别赋给两个串联连接器；阻尼类型选 VISCOUS | GFE-Iso |
| ① | SPH 分析步 sph_step | step.sph_step |  | Cmd§2.14.9 | 粒子间距/计算域/重力/状态方程(γ, 声速)/CFL 数/对象列表/执行参数字典等全套 SPH 求解参数 | GFE-Cmd |
| ① | SPH 初始速度 | sph.init_velocity |  | UG§1.20 | 初速度数值+方向 [X,Y,Z] | GFE-UserGuide |
| ① | SPH 填充模式 | sph.fill_mode |  | UG§1.20 | 全部/实体/面/线 四种生成粒子方式 | GFE-UserGuide |
| ① | SPH 对象定义 sph | sph.sph |  | Cmd§2.18.1 | obj_type 0=流体 1=固体；fill_mode 0=全部 1=实体 2=面 3=线框；non_newton 5 参数非牛顿流体；init_veloci | GFE-Cmd |
| ① | SPH 对象类型设置 | sph.obj_type |  | UG§1.20 | 固体（固定边界）/流体/浮体（固体勾"设置为浮体"） | GFE-UserGuide |
| ① | SPH 流体动力对象创建 | GFE.Pre.sph 模块 |  | Cases§8.3 | SPH 区域（几何/网格/单元集）+对象类型 固体/流体+填充模式 全部/面+浮体及浮体密度 | GFE-Cases |
| ① | SPH 管理器 | sph.sph_mgr |  | Cmd§2.18.2 | manager() 或 sph_mgr() | GFE-Cmd |
| ① | SPH 非牛顿流体设置 | sph.non_newton 5 参数 |  | UG§1.20 | 密度、粘度、屈服应力、HBP m、HBP n 五参数 | GFE-UserGuide |
| ① | 不透水构件建模（普通单元当止水帷幕） | - |  | Imp§1.5.2 | 止水帷幕用普通 C3D4（无孔压自由度）实现不透水 | GFE-Implicit |
| ① | 二折线位移型阻尼器（BRB）模拟 | connector_plastic GFE HDN2 |  | Iso§1.2.2/§2.2.1图2.2.1.6 | 连接器行为=弹性(抗压刚度)+塑性(定义方式 GFE HDN2：屈服力+刚度折减系数) | GFE-Iso |
| ① | 二系悬挂简化多体轮轨力计算 | boundary if_mode/if_param 列车参数族 |  | Explicit§11.1 | 考虑车体-构架-轮对多体动力学相互影响，美国六级轨道不平顺作激励；GUI 面板含轮对/转向架/车厢质量+一二系悬挂刚度阻尼 | GFE-Explicit |
| ① | 冲击波属性 incident_wave_property | interaction.incident_wave_property |  | Cmd§2.13.13 | type 0=AirBlast 1=SurfaceBlast；data=[TNT等效质量, 质量→kg, 长度→m, 时间→s, 压力→Pa] 单位转换系数 | GFE-Cmd |
| ① | 冲击波属性管理器 | interaction.iw_prop_mgr |  | Cmd§2.13.14 | 文档名 incident_wave_property_manager()，示例用 iw_prop_mgr() | GFE-Cmd |
| ① | 冲击波属性（CONWEP 空气爆破） | incident_wave_property AirBlast |  | Cases§14.3 | 相互作用→冲击波属性，"定义"选空气爆破输 CONWEP 参数 | GFE-Cases |
| ① | 冲击波管理器 iw_mgr() | interaction.iw_mgr |  | Cmd§2.13.12 | 获取冲击波管理器 | GFE-Cmd |
| ① | 冲击波荷载 | incident_wave 命令流可建 |  | Cases§14.4 | 源点（齿轮图标选节点集）+迎爆面（箭头图标选表面集）+属性+起爆时间+数量放缩系数 | GFE-Cases |
| ① | 冲击波载荷 incident_wave | interaction.incident_wave |  | Cmd§2.13.11 | set_name/surf_name + time_detonation 起爆时间 + prop_name 挂属性；文档构造名 iw() 与示例 inciden | GFE-Cmd |
| ① | 列车荷载 | - |  | UG§1.11.10 | 轨道线移动节点力；静/动轮轨力；动轮轨力三法（直接输入/轨道不平顺/实测加速度）；可预览 | GFE-UserGuide |
| ① | 列车荷载复制 | - |  | Cases§15.13 | 树中右键复制已建列车荷载，仅改名称、区域集合、起点和终点即得另一轨道荷载 | GFE-Cases |
| ① | 列车荷载对象 | boundary.boundary |  | Cmd§2.10.2 | 复用 boundary 类：begin_end 起终点/track_id/track_coord/接口模式 if_* 系列（加速度路径、时间间隔、总时间、坡度、 | GFE-Cmd |
| ① | 列车荷载轨道起终点拾取 | - |  | Cases§15.13 | "基本"页：维度 3D/2D、视口拾取轨道起点/终点节点、缩放系数、列车速度(米/秒)、起始时间/位置、方向向量 | GFE-Cases |
| ① | 列车荷载（线荷载形式） | - |  | Explicit§6.2 | 施加于几何线集；时域/空间分布均标"-"（移动特性内部定义）；补块证实支持动轮轨力三种加载方式（轨道实测法/轨道不平顺法/直接输入） | GFE-Explicit |
| ① | 创建列车荷载 | - |  | Cases§15.13 | 树"边界条件与荷载"双击创建，类型选"列车荷载"，区域=轨道几何集 | GFE-Cases |
| ① | 动轮轨力三种方法 | boundary.if_mode 方法选择 |  | Cases§15.13 | 轨道实测加速度法 / 轨道不平顺法 / 直接输入 三选一 | GFE-Cases |
| ① | 土（固结/渗流）分析步 soils_step | step.soils_step |  | Cmd§2.14.8 | is_consolidation 固结开关，cetol/utol 容差，end 结束条件 | GFE-Cmd |
| ① | 声压 | - |  | UG§1.11.18 | 仅显式动力+AC3D4 单元 | GFE-UserGuide |
| ① | 天然橡胶支座模拟 | connector_elastic 线性刚度 |  | Iso§1.3.1/§2.2.1图2.2.1.8 | 纯弹性连接器行为，F1/F2 水平刚度 + F3 竖向刚度（抗拉/抗压可不等） | GFE-Iso |
| ① | 摩擦摆支座（FPB）模拟 | connector_plastic GFE PEND |  | Iso§1.3.3/§2.2.1图2.2.1.10 | 弹性+塑性(定义方式 GFE PEND：摩擦系数变化率/屈服位移/快摩擦系数/慢摩擦系数/等效半径，设在 F2/F3 剪切分量) | GFE-Iso |
| ① | 支座重力荷载截面力输出（竖向压应力验算用） | element_output SF 截面力请求 |  | Iso§5.2 p58 | 输出重力荷载代表值下隔震支座最大截面力（示例 1537kN），供人工按隔标 4.6.3 验算压应力 | GFE-Iso |
| ① | 流体动力分析步参数三页 | sph_step 全套参数命令流 |  | Cases§8.4 | 定义常量（粒子距离/重力/参考密度/声音系数/多方常数等）/对象顺序/求解参数（时长/输出间隔/移动系数/有效密度上下限等） | GFE-Cases |
| ① | 流体动力分析步（SPH） | - |  | Cases§8.4; UG§1.15.1(9) | 定义常量/对象顺序/求解参数/其他四页；参数必须 SI(m) 单位 | GFE-Cases+GFE-UserGuide |
| ① | 爆炸荷载分析（IWCON 输出） | incident_wave+输出请求命令流 |  | FAQ§4.5 | 支持爆炸荷载输入与响应输出 IWCON，需小场输出间隔 | GFE-FAQ |
| ① | 等效连续加载与多段折线/曲线连续加载 | boundary if_*/track_* 属性族 |  | Explicit§11.1 | 避免荷载突加效应；可实现列车出库-咽喉区变道全过程模拟 | GFE-Explicit |
| ① | 跌落工况仿真（初速度+重力+接触） | - |  | Explicit§2.9.1 | 触地初速度+重力的显式跌落分析 | GFE-Explicit |
| ① | 轨道实测加速度法参数输入 | boundary.if_acce/if_acce_path |  | Cases§15.13 | 加速度 txt 文件+时间间隔、构架/轮对/车辆质量、一系/二系悬挂刚度阻尼 | GFE-Cases |
| ① | 铅芯橡胶支座连接单元定义（隔震支座类型） | - |  | Iso§5.1图5.1.1(b) p56 | "连接单元定义"对话框，类型=隔震支座，按 U1/U2/U3 分量输入线性有效刚度/阻尼 + 非线性（初始刚度、屈服力、屈服后刚度比）——与连接器行为路径并存， | GFE-Iso |
| ① | 铅芯橡胶支座（LRB）模拟 | connector_plastic HALF CYCLE |  | Iso§1.3.2/§2.2.1图2.2.1.9 | 弹性+塑性(定义方式 HALF CYCLE：屈服力—塑性变形多行表) | GFE-Iso |
| ② | C3D4P 纯渗流分析（前处理阶段单独分析模式） | - |  | Imp§1.5.3 | 不做应力耦合的纯渗流稳态分析，输出 POR 与流量场 | GFE-Implicit |
| ② | SPH 粒子属性赋予与 xml 导出 | - | sph 属性可命令流;xml 导出无 API | UG§1.20 | 对几何/网格/单元集赋 SPH 粒子属性，导出 xml 模型文件；入口：模型树→流体动力 | GFE-UserGuide |
| ② | 轮轨力时程直接输出 | - | 轮轨力文件随 INPX 产出;预览 GUI | Explicit§11.2 | 软件直接输出计算的轮轨力时程（算例约 152000-158000 N，时长约 130s） | GFE-Explicit |
| ② | 静轮压力（含 GFE 预设） | - | 压力值可 boundary 设;预设库 GUI 选取 | Cases§15.13 | 轮轨力=静轮压力时"列车数据"页可加载 GFE 预设或按实际填写 | GFE-Cases |
| ③ | FEM-SPH 流固耦合全流程 | - |  | Cases§9.7 | FEM 预计算（算 ~1% 中止）出 fea+db → mk2inpmap.txt 手动放入预计算结果文件夹 → 批处理提交 xml（gfedatapath/g | GFE-Cases |
| ③ | SPH 批处理提交 | - |  | Cases§8.6 | _Def.xml 经批处理文件（改作业名+SPH 程序路径）双击提交，不走 GUI | GFE-Cases |
| ③ | 列车荷载曲线绘制预览 | - | 曲线预览为 GUI 绘图 | Cases§15.13 | 对话框内"绘制"按钮弹"列车荷载曲线绘制"窗口，按节点查看轨道节点受力时程 | GFE-Cases |
| ③ | 底部剪力比计算 | - | 后处理统计计算 GUI | Iso§5.3.2表5.3.2 p59-60 | 减震后/减震前上部结构剪力之比（X 0.28 / Y 0.26），用于隔标 6.1.3 降度判定 | GFE-Iso |
| ③ | 消能子结构一键转换 | - | 一键转换按钮 GUI,无 API 符号 | Iso§2.2.2图2.2.2 | 【土木工程】选项卡→【消能子结构】→图形区选构件；软件自动复制一份材料（如 C1_Mat30-1）并去除非线性参数转为弹性，赋给所选构件 | GFE-Iso |
| ③ | 消能子结构弹塑性→弹性一键转换 | - | 一键转换按钮 GUI,无 API 符号 | UG§1.18.11 | 减震大震工况下消能子结构构件转弹性本构；入口：前处理-土木工程-转换 | GFE-UserGuide |
| ③ | 消能子结构配筋验算 | - | 配筋验算报告 GUI | Iso§3.4.7/§4.4.7图4.4.7.1 p55 | 高亮消能子结构构件，大震工况按弹性本构进行配筋验算（高亮图顶部红字明示） | GFE-Iso |
| ③ | 连接单元库导入/导出 | - | 连接单元库管理为 GUI | Iso§5.1图5.1.1(b) p56 | 对话框底部「导入」「导出」「恢复默认」按钮，支持支座参数库复用 | GFE-Iso |
| ③ | 阻尼器验算（设计荷载/位移统计） | - | 验算统计报告 GUI | Iso§3.4.5/§4.4.5表4.4.5 p52-53/§5.4.4表5.4.4 p65-66 | 罕遇地震下统计阻尼器/隔震支座 SE（位移）/SF（力）最大值用于产品选型验算 | GFE-Iso |
| ③ | 附加阻尼比计算（时程能量法） | - | 时程能量法计算为后处理 GUI | Iso§3.3.4/§3.4.4/§4.4.4表4.4.4 p52 | 由阻尼器耗能与结构阻尼耗能按时程能量法统计附加阻尼比 | GFE-Iso |
| ③ | 隔震支座规范验算（位移限值/竖向应力） | - | 规范验算报告 GUI | Iso§5.4.4 p65 | 最大水平位移对照隔标 4.6.6 的 min(0.55D, 3Tr)；最大竖向压/拉应力对照隔标 6.2.1（手册示例为人工算式核对，非软件自动判定） | GFE-Iso |
| ③ | 隔震支座设计参数录入 | - | 设计参数录入对话框 | Iso§5.1图5.1.1(b) p56 | 连接单元对话框"设计参数"按钮进入：有效直径/中孔直径/橡胶总厚度/支座+连接板总高/一次·二次形状系数/考虑附加弯矩作用（带*四项必填） | GFE-Iso |

## D12 GUI工具与工程管理（95 项：①49 ②4 ③39 未知3）

| 层 | 能力 | API入口 | 断点/理由 | 出处 | 说明 | 源手册 |
|---|---|---|---|---|---|---|
| ① | 三类集合管理器获取 | set.gset_mgr/nset_mgr/elset_mgr |  | Cmd§2.7.6-2.7.8 | gset_mgr() / nset_mgr() / elset_mgr() | GFE-Cmd |
| ① | 几何管理器 add | geo_mgr.add |  | Cmd§2.3.3 | add(obj)，obj 为 TopoDS_Shape 或 Geometry 对象，返回 Geometry | GFE-Cmd |
| ① | 几何表面（面/线/点三种载体） | surface.geometry_surface |  | Cmd§2.8.2 | geometry_surface(name)，data=[parent,face,side] 三元组编码；可 to_node_surface 转节点表面 | GFE-Cmd |
| ① | 切换文档（UI 触发钩子） | document.set_application_by_ui |  | Cmd§2.2.1 | set_application_by_ui()，界面切换文档时自动调用，用户无需手调 | GFE-Cmd |
| ① | 删除对象（按名称列表） | manager.delete |  | Cmd§2.3.11 | delete(name_list)，参数必须是列表，可批量 | GFE-Cmd |
| ① | 删除所有对象 | manager.delete_all |  | Cmd§2.3.12 | delete_all() | GFE-Cmd |
| ① | 单元表面 | surface.element_surface |  | Cmd§2.8.3 | data=[[父ID,单元号,面号],…]，可由 elsets 单元集名列表定义（示例配错构造，见②） | GFE-Cmd |
| ① | 单元集合 elset | set.elset |  | Cmd§2.7.4 | elset()，name + data（单元 ID 列表）+ unsort | GFE-Cmd |
| ① | 基于索引获取文档 | document.get_document |  | Cmd§2.2.3 | get_document(index)，index 从 0 起；越界静默返回最后一个 | GFE-Cmd |
| ① | 基础几何集合 gset_basic | set.gset_basic |  | Cmd§2.7.2 | 构造 gset_basic(name)；set_shapes / set_shapes_id / get_shapes / get_shapes_id | GFE-Cmd |
| ① | 基础表面对象 | surface.surface |  | Cmd§2.8.1 | surface()，仅 name 属性 | GFE-Cmd |
| ① | 完整示例①：导入 YJK 恒荷载计算 | - |  | Cmd§8.1 | 端到端：模块导入→YJK 导入→土层材料→Soil1D 剖面→土体几何→布尔切割→边界/重力→Tie→网格→静力步→工况→INP 写出 | GFE-Cmd |
| ① | 完整示例②：隧道开挖监测 | - |  | Cmd§8.2 | 端到端：open_pre→几何平移/分割→按形心分区建集→材料/截面批量→网格→三步静力→单元生死开挖→INP 写出 | GFE-Cmd |
| ① | 对象计数（正常/隐藏/全部） | manager.count |  | Cmd§2.3.19-21 | count() / count_hidden() / count_all() | GFE-Cmd |
| ① | 引用几何集合 gset_ref | set.gset_ref |  | Cmd§2.7.3 | 构造 gset_ref(name)；add_ref / set_refs / get_refs 按名引用其他几何集 | GFE-Cmd |
| ① | 截面集合（按方向 X/Y） | - |  | Cases§5.2.3 | ctrl+shift 多选两侧截面建 Set-x/Set-y 边界集合 | GFE-Cases |
| ① | 拾取 | - |  | UG§1.17.4 | 按节点/单元编号选中（';' 分隔） | GFE-UserGuide |
| ① | 按 id 查找几何 | geo_mgr.find |  | Cmd§2.3.8 | geo_mgr().find(id) 返回 geometry_object | GFE-Cmd |
| ① | 按 id 查找网格 | mesh_mgr.find |  | Cmd§2.3.9 | 标题为网格查找，正文函数误写 geo_mgr，示例实用 MeshMgr.find(id) | GFE-Cmd |
| ① | 按名称查找对象 | manager.find |  | Cmd§2.3.7 | find(name)，未找到返回 None | GFE-Cmd |
| ① | 按形心空间分区批量归集 idiom | gset_mgr.add |  | Cmd§8.2 | 遍历 children 实体→形心落于 z_ranges×x_ranges×y_range 判断→f-string 命名分组 add 进 gset | GFE-Cmd |
| ① | 操作状态类 | status |  | Cmd§2.3.25 | status 类，属性 CODE（err_code）+ MESSAGE（字符串） | GFE-Cmd |
| ① | 查询 | - |  | UG§1.17.3 | 点坐标/距离/网格统计/节点/单元信息 | GFE-UserGuide |
| ① | 查询功能（坐标/距离/网格/节点/单元） | - |  | Cases§7.2.8 | 通用—查询，结果输出在界面输出框 | GFE-Cases |
| ① | 检查对象存在（正常/隐藏/全部） | manager.contains |  | Cmd§2.3.15-17 | contains(name) / contains_hidden(name) / contains_all(name) | GFE-Cmd |
| ① | 模块导入（import GFE / from GFE.Pre import *） | GFE |  | Cmd§1.3 | 使用命令流前必须导入 GFE 主模块；子模块导入大小写敏感 | GFE-Cmd |
| ① | 添加几何集合（名称+形状 ID 三元组） | gset_mgr.add |  | Cmd§2.3.6 | gset_mgr().add(name, shapes_id)，shapes_id=[[父ID,类型,自身ID],…] | GFE-Cmd |
| ① | 添加几何集合（名称+形状对象） | gset_mgr.add |  | Cmd§2.3.5 | gset_mgr().add(name, shapes, hidden=False, auto_name=False) | GFE-Cmd |
| ① | 激活/停用对象 | manager.activate |  | Cmd§2.3.18 | activate(name, state)；停用的对象在分析中被忽略 | GFE-Cmd |
| ① | 编辑对象 | manager.edit |  | Cmd§2.3.10 | edit(obj)，对象须已存在且已修改，改完调用 edit 才保存 | GFE-Cmd |
| ① | 网格管理器 add（带数据） | mesh_mgr.add |  | Cmd§2.3.4 | add(name, data)，data 为 shared_ptr<Gfe_MeshData> | GFE-Cmd |
| ① | 网格管理器 add（无参=添加参考节点） | mesh_mgr.add |  | Cmd§2.3.4 | mesh_mgr().add() 无参重载添加参考节点 ref_node | GFE-Cmd |
| ① | 自动命名 | manager.auto_name |  | Cmd§2.3.1 | auto_name(prefix, has0=False) 生成唯一名（Box-1, Box-2…） | GFE-Cmd |
| ① | 节点表面 | surface.node_surface |  | Cmd§2.8.4 | node_surface(name)，data=[[-1,节点号],…]，第一位固定 -1 | GFE-Cmd |
| ① | 节点集合 nset | set.nset |  | Cmd§2.7.5 | nset()，name + data（节点 ID 列表）+ unsort | GFE-Cmd |
| ① | 获取当前活动文档 | document.current_document |  | Cmd§2.2.2 | current_document() 返回 document 对象 | GFE-Cmd |
| ① | 获取有效标签 | manager.valid_tag |  | Cmd§2.3.22 | valid_tag() 返回标签字符串列表 | GFE-Cmd |
| ① | 获取正常对象名称列表 | manager.name_list |  | Cmd§2.3.13 | name_list() | GFE-Cmd |
| ① | 获取表面管理器 | surface.surf_mgr |  | Cmd§2.8.5 | surf_mgr() | GFE-Cmd |
| ① | 获取选中形状 ID get_selected_shape_id | geotool.get_selected_shape_id |  | Cmd§3.4.15 | 返回 [pid, shape_type, id] 三元组列表 | GFE-Cmd |
| ① | 获取选中形状 get_selected_shape | geotool.get_selected_shape |  | Cmd§3.4.14 | 按类型过滤当前 GUI 选中的形状 | GFE-Cmd |
| ① | 获取隐藏对象名称列表 | manager.name_hidden |  | Cmd§2.3.14 | name_hidden() | GFE-Cmd |
| ① | 表面集创建（几何/单元/节点方式选面） | - |  | Cases§2.2.4 | 具有正反属性的面集合；实体默认外表面，二维面选颜色（如"品红"）定向 | GFE-Cases |
| ① | 设置当前文档 | document.set_current |  | Cmd§2.2.4 | set_current(document_object)，返回 bool | GFE-Cmd |
| ① | 通用 add | manager.add |  | Cmd§2.3.2 | add(obj, inner=False, auto_name=False) 向管理器添加对象 | GFE-Cmd |
| ① | 重命名对象 | manager.rename |  | Cmd§2.3.23 | rename(old, new) 返回 err_code 枚举 | GFE-Cmd |
| ① | 错误码枚举 | err_code |  | Cmd§2.3.24 | err_code: UNDEFINED/SUCCESS/NAME_REPEATED/NAME_ILLEGAL/CHILD_NOT_EXIST/MISS_REFE | GFE-Cmd |
| ① | 集合创建（几何/节点/单元三类型） | - |  | Cases§1.2.x | 三类型独立命名空间；含 "Add to mesh entity" 与"保持选择节点/单元的顺序"选项；框选节点建集供批量建连接器 | GFE-Cases |
| ① | 顶层模块体系（GFE→Pre/geometry/io/soil/occ） | GFE |  | Cmd§1.1 | 命令流顶层 python 模块为 GFE，下分 5 个子模块 | GFE-Cmd |
| ② | 目录设置 | - | io.set_work_path 覆盖工作目录;其余对话框 | UG§1.16.2 | 各文件格式默认目录；工作目录变更单向联动专用目录 | GFE-UserGuide |
| ② | 系统设置 | - | 设置项存 config.txt 可脚本改;界面为对话框 | UG§1.16.1 | 语言（中/英）；自动保存开关+间隔（最小 10 分钟） | GFE-UserGuide |
| ② | 表面集转单元集 | - | 无专 API;可经 surface/set data 命令流间接转 | Cases§10.10 | 创建向导中选"转换为单元集"（人工边界前置）；Ctrl+Shift 框选土体四周外表面 | GFE-Cases |
| ② | 设置对话框-目录路径配置 | - | set_work_path 部分可达;其余路径仅对话框 | FAQ§5.2 | 设置对话框「目录」区含工作目录、导入/导出文件、导入/导出 Abaqus INP 等路径栏，底部「全部恢复默认」按钮（截图分辨率低，默认值不可辨） | GFE-FAQ |
| ③ | GUI 命令流输入框切换 | - |  | Cmd§1.3 | 前处理界面右侧 Output/python 两按钮，点 python 切到命令流输入框 | GFE-Cmd |
| ③ | Ribbon 长按弹出子选项菜单 | - |  | UG§1.1.1 | 图标右下角黑三角=长按弹出选项菜单（如圆弧三点/圆心切换） | GFE-UserGuide |
| ③ | View Cube 视角切换 | - |  | UG§1.1.2(6) | 点立方体面/边/角切换三维视角，带动画 | GFE-UserGuide |
| ③ | 中英文界面切换 | - |  | FAQ§5.2 | 设置-系统 切换简体中文/英文 | GFE-FAQ |
| ③ | 停靠窗口恢复（输出/模型树状列表） | - |  | FAQ§5.1 | 文件-视图-停靠窗口 重新打开误关的输出窗口/树状列表 | GFE-FAQ |
| ③ | 几何显示/隐藏/孤立/消隐 | - | 视图显示操作 GUI | Cases§1.2.1 | 树节点蓝色立方体图标/右键菜单控制显隐 | GFE-Cases |
| ③ | 几何集合基类 gset | set.gset |  | Cmd§2.7.1 | 仅作基类展示，无法创建调用；有 add_attribute(attr, value) | GFE-Cmd |
| ③ | 切割显示 | - |  | UG§1.17.5 | XYZ 预设面或自定义平面切片显示 | GFE-UserGuide |
| ③ | 切割视图（剖切检查） | - |  | Cases§1.2.1 | X/Y/Z 平面滑动剖切查内部；默认仅正方向 | GFE-Cases |
| ③ | 前/后处理界面切换 | - | 界面切换操作 | UG§1.1.1 | GFE PrePo 内前处理/后处理两套界面切换 | GFE-UserGuide |
| ③ | 前处理过滤器（按实体类别过滤/隐藏显示） | - | 过滤显示 GUI | FAQ§5.5 | 对几何体的角点、表面、内部实体分别做选择隐藏；仅隐藏「实体」类别时角点/表面仍显示 | GFE-FAQ |
| ③ | 前处理颜色设置 | - | 颜色设置 GUI | UG§1.19.1 | 默认 Default AllGeo / Default AllMesh 两条；区域 4 选项、类别 3 选项（All/Material/YJK Componen | GFE-UserGuide |
| ③ | 单选/增选/矩形框选/多边形框选 | - |  | UG§1.1.2(1)表1.1.2-1 | 左键单选、Ctrl+单击增选、Shift+拖动矩形框选、Ctrl+依次单击多边形框选（右键确认） | GFE-UserGuide |
| ③ | 对象类型选择（几何/网格两族 8 类） | - | 选择模式切换 GUI | UG§1.1.2(2) | 几何：点/线/面/实体/几何部件；网格：节点/单元/表面 | GFE-UserGuide |
| ③ | 工况预览 | - |  | UG§1.17.7 | 按分析步预览生死单元添加/移除效果 | GFE-UserGuide |
| ③ | 按角度选择（特征区域网格快速选择） | - | 交互选择 GUI | UG§1.1.2(7) | 以点击点为种子按相邻网格面法向夹角阈值扩展选择节点/单元/表面 | GFE-UserGuide |
| ③ | 搜索框过滤+替换显示 | - | 搜索框交互 GUI | Cases§14.2 | 搜索框键入关键词过滤树条目，Ctrl 多选后"替换"显示 | GFE-Cases |
| ③ | 显示截面（可视化） | - | 可视化显示 GUI | FAQ§1.9 | 以三维实体外观显示杆件截面，目测核对 | GFE-FAQ |
| ③ | 显示线/面截面（梁方向校核） | - | 可视化显示 GUI | Cases§15.10 | 视图勾选后以三维实形渲染梁/壳截面，检查梁方向是否正确 | GFE-Cases |
| ③ | 构件截面尺寸查看（双击/右键编辑） | - | 双击/右键交互 GUI | FAQ§1.9 | 查看杆件 a 值(沿1轴)、b 值(沿2轴)，点"数据"查 1 轴方向 | GFE-FAQ |
| ③ | 框选准则 2 种 | - |  | UG§1.1.2(5) | 包含（全在框内）/ 重叠（部分在框内即选） | GFE-UserGuide |
| ③ | 框选准则切换（重叠/包含） | - | 框选交互 GUI | Cases§3.1.3 | 全局开关：选边/柱用"重叠"+Shift，选梁用"包含" | GFE-Cases |
| ③ | 框选模式 2 种 | - |  | UG§1.1.2(4) | 矩形 / 多边形 | GFE-UserGuide |
| ③ | 检查引用关系 | - | 引用检查对话框 GUI | UG§1.17.8 | 检查树状项引用，失效已断引用的子项 | GFE-UserGuide |
| ③ | 模型局部细节查看（单独显示+框选替换显示） | - | 显示操作 GUI | Cases§7.2.7 | 单独显示某几何后框选局部替换显示 | GFE-Cases |
| ③ | 模型文件保存 / 另存 | - | 无 save API,仅文件菜单 | FAQ§5.6 | 常规保存与另存为；文件只读时保存被拒、仅能另存 | GFE-FAQ |
| ③ | 界面六区域布局 | - |  | UG§1.1.1 | 文件菜单、Ribbon 栏、工具栏、树状列表、图形窗口、输出窗口 | GFE-UserGuide |
| ③ | 直接拾取自动建 PickedSet-N | - | 拾取交互专属 | Cases§1.2.2 | 图形区直接拾取的副产品是持久化隐式集合 | GFE-Cases |
| ③ | 背景双色设置（前处理） | - | 背景设置 GUI | UG§1.19.1 | 渐变背景颜色1/颜色2 | GFE-UserGuide |
| ③ | 自动保存机制 | - |  | Cases§1.2 | 自动保存至 C:/Users/<user>/Documents/GFE/.PrePo.autosave-<PID>，崩溃恢复可用 | GFE-Cases |
| ③ | 自动生成集合（形心坐标聚类） | - | 聚类建集为 GUI 工具,无 API | Cases§7.2.7 | 区域类型+名称前缀+X/Y/Z 分类方向自动分组 | GFE-Cases |
| ③ | 视图设置-显示线/面截面 | - | 视图设置 GUI | UG§1.19.2(2) | 几何页勾选显示线/面对象截面形状 | GFE-UserGuide |
| ③ | 视图设置-渲染风格 | - | 视图设置 GUI | UG§1.19.2(1) | "自动的"（默认）/框线/阴影部分 | GFE-UserGuide |
| ③ | 视图设置-网格标签与梁壳截面显示 | - | 视图设置 GUI | UG§1.19.2(3) | 节点标签（粉）、单元标签（黄棕）及梁/壳截面；网格划分后才生效 | GFE-UserGuide |
| ③ | 过滤器（布尔显示） | - |  | UG§1.17.1 | 几何/单元/节点三级筛选+替换/添加/移除/相交显示 | GFE-UserGuide |
| ③ | 选择模式 4 种 | - |  | UG§1.1.2(3) | 默认/添加/移除/转换 | GFE-UserGuide |
| ③ | 选择移除（反选精化） | - |  | Cases§6.6.5 | 先框大范围再"选择移除"剔除多余 | GFE-Cases |
| ③ | 附录四 参考文献 | - |  | UG附录四 p311 | 仅 1 条：杨剑等《基于附加质量法水与水池壁板动力相互作用分析》2013 | GFE-UserGuide |
| ③ | 鼠标视图操作（旋转/平移/缩放） | - |  | UG§1.1.2(1)表1.1.2-1 | 左键长按拖动旋转、中键长按拖动平移、滚轮缩放 | GFE-UserGuide |
| 未知 | 修订记录（版本演化真值） | - |  | UG附录前 p268-272 | v0.48.0(2022.9)→1.0.0(2023.5)→1.5.0(2023.8)→2.6.0(2024.3)→2.11.0(2024.11)→2.11.5 | GFE-UserGuide |
| 未知 | 修订记录（版本演进表） | - |  | Cmd修订记录 | 2.15.2 (2025.07 首发) → 3.2.2 (2025.12) → 3.3.0 (2026.01) → 3.4.0 (2026.02)，逐版功能增量 | GFE-Cmd |
| 未知 | 工程页签功能总览 | - |  | Cases§6.4.2 | 快速建土/粘弹性人工边界/地震场地反应/非均匀土体/隧道设计器/施工助手/自动生成集合/阻尼比/土体材料/配筋/消能子结构 | GFE-Cases |

## 未知（判不动，待实测）共 9 条

- D02 材料级"质量系数"参数（出处 Explicit§12.2.1）
- D07 §7.1.2 后半 + §7.2 瑞利阻尼转换正文（出处 Explicit第7章）
- D07 土-结整体模型土压力考虑方式（修订记录线索）（出处 FAQ修订记录）
- D07 工程案例：组合壳综合管廊/地铁环境振动/核岛/大型交通枢纽（出处 Explicit第10-13章）
- D09 GFE 文件系统 10 种文件类型（出处 UG附录一 p273-274）
- D10 附录：梁和壳单元局部坐标与输出物理量定义（出处 Explicit附录）
- D12 修订记录（版本演化真值）（出处 UG附录前 p268-272）
- D12 修订记录（版本演进表）（出处 Cmd修订记录）
- D12 工程页签功能总览（出处 Cases§6.4.2）
