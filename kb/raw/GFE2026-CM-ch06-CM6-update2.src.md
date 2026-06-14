# GFE2026-CM-ch06-CM6-update2
> 来源：E:\GFE2026\典型案例与教程\第6章 深基坑施工开挖模拟案例\CM6-update2.py（GFE2026 官方典型案例命令流，v3.x 代际金标准）。raw 不可变源副本，2026-06-11 入库。

```python
import GFE
from GFE import *
from GFE.Pre import *
from GFE.occ import *

from GFE.geometry import geotool
GFE.Pre.document.set_application_by_ui()

# =========== 路径定义 ==========
import os
import sys
# 获取程序exe路径
exe_file_path = os.path.abspath(sys.executable)
# 获取当前exe文件夹路径
exe_dir_path = os.path.dirname(exe_file_path)
# 获取上一级目录
parent_path = os.path.dirname(exe_dir_path)
# 增加文件/夹名称
plugin_dir = os.path.join(parent_path, "典型案例与教程")
plugin_dir2 = os.path.join(plugin_dir, "第6章")
yjk_path = os.path.join(plugin_dir2, "施工图\施工图")
gmat_path = os.path.join(plugin_dir2, "cm6.gmat")
inp_path = os.path.join(plugin_dir2, "CM6-Case-jikengkaiwa.inp")
# 转为绝对路径
yjk_path = os.path.abspath(yjk_path)
gmat_path = os.path.abspath(gmat_path)
inp_path = os.path.abspath(inp_path)

# ============== 参数定义 ===============
# 模型参数
fangpo_up_face_length = 42.0            # 放坡上表面长度
fangpo_up_face_width = 27.0             # 放坡上表面宽度
fangpo_height = 1.0                     # 放坡高度
fangpo_down_face_spacing = 1.0          # 放坡下表面内陷间距
# fangpo_x_base_points =[(0, 0), (27, 0), (26, -1), (1, -1), (0, 0)]		# 放坡x方向初型基础面---多折线
# fangpo_y_base_points =[(0, 0), (42, 0), (41, -1), (1, -1), (0, 0)]		# 放坡y方向初型基础面---多折线
fangpo_x_base_points =[(0, 0), (fangpo_up_face_width, 0), (fangpo_up_face_width-fangpo_down_face_spacing, -fangpo_height),
                       (fangpo_down_face_spacing, -fangpo_height), (0, 0)]
fangpo_y_base_points =[(0, 0), (fangpo_up_face_length, 0), (fangpo_up_face_length-fangpo_down_face_spacing, -fangpo_height),
                       (fangpo_down_face_spacing, -fangpo_height), (0, 0)]

kaiwa_num = 4                       # 开挖数量必须大于2
kaiwa_1_depth = 1.0 				# 开挖1的深度
kaiwa_2_n_depth = 2.0 			    # 开挖2到n的深度

neizhicheng_out_length = fangpo_up_face_length - 2*fangpo_down_face_spacing			# 内支撑（外矩形）长度40
neizhicheng_out_width = fangpo_up_face_width - 2*fangpo_down_face_spacing			# 内支撑（外矩形）宽度25
neizhicheng_spacing = 5.0               # 内支撑钢筋间距
neizhicheng_in_length = neizhicheng_out_length - 2*neizhicheng_spacing			    # 内支撑（内矩形）长度30
neizhicheng_in_width = neizhicheng_out_width - 2*neizhicheng_spacing			    # 内支撑（内矩形）宽度15
# 这个内部线条要跟neizhicheng_spacing【内支撑钢筋间距】对应
neizhicheng_in_lines = [		# 内支撑内部线条---直线
    (0, 25), (5, 20), (40, 25), (35, 20), (40, 0), (35, 5), (0, 0), (5, 5),		# 第一组

    (35, 25), (40, 20), (30, 25), (40, 15), (5, 25), (0, 20), (10, 25), (0, 15),		# 第二组
    (40, 5), (35, 0), (40, 10), (30, 0), (5, 0), (0, 5), (10, 0), (0, 10),

    (10, 25), (10, 20), (30, 25),(30, 20),(10, 5), (10, 0), (30, 5),(30, 0), 		# 第三组
    (0, 15), (5, 15), (0, 10),(5, 10), (35, 15),(40, 15), (35, 10), (40, 10),

    (15, 20), (15, 25), (20, 20), (20, 25), (25,20), (25, 25),			# 第四组
    (15, 0), (15, 5), (20, 0), (20, 5), (25,0), (25, 5),

    (10, 25), (15, 20), (15, 20), (20, 25), (20, 25), (25, 20), (25, 20), (30, 25),	# 第五组
    (10, 0), (15, 5), (15, 5), (20, 0), (20, 0), (25, 5), (25, 5), (30, 0),

    (0, 15), (5, 10), (40, 15), (35, 10)			#第六组
]

lizhu_height = 12.0				# 立柱高度

# 材料
material = ['C35', 2.5, 3.15e+07, 0.2]		# 材料
# 土体参数
soil_materials_path = gmat_path
# 土层材料（通过gmat文件导入）
soil_materials = ['zatiantu', 'niantu', 'fenzhiniantu', 'shazhinianxingtu', 'qiangfenghuahuagangyan']
soil_depth = [2.0, 4.0, 6.0, 4.0, 9.0]		# 土层厚度
soil_length = 120		# 土层长度
soil_width = 120		# 土层宽度
jikeng_soil_boundary_spacing = 24.0         # 基坑边界与土体边界的间距（用于平移基坑）

# YJK模型
yjk_file_path = yjk_path
yjk_soil_boundary_spacing = 30.0         # yjk地下室边界与土体边界的间距（用于平移基坑）

# 网格
yjk_mesh_size = 2.0
soil_mesh_size = 3.0

# 截面属性
fangpo_thickness = 0.2                      # 放坡-壳-厚度
dilianqiang_thickness = 0.5                 # 地连墙-壳-厚度
lizhu_radius = 0.5                          # 立柱-梁-圆形半径
neizhicheng_section_params = [0.4, 0.8, 0.5, 0.5, 0.05, 0.05, 0.05]		# 内支撑-梁-工字形参数



# ================= 基坑-放坡建模 ================
# ---------- 绘制放坡x方向-多折线绘制 --------------
GFE.draft.get_current().set_snap_object(0)
GFE.draft.get_current().set_operate_mode(2)
for point in fangpo_x_base_points:
    GFE.draft.get_current().input(point[0], point[1])
# 填充区域
GFE.draft.get_current().set_operate_mode(-1)
GFE.draft.get_current().set_snap_object(2)
GFE.draft.get_current().snap_object(-10, fangpo_up_face_width+10, 10, -fangpo_height-10)
GFE.draft.get_current().select_snaped(True)
GFE.draft.get_current().fill_selected()
# 删除所有线
GFE.draft.get_current().remove_selected()

# 设置yz平面
GFE.draft.get_current().set_normal([0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0])
# 完成草图，创建放坡土体二维模型
shape = GFE.draft.get_current().export()
if not shape.is_null() :
    mgr = GFE.Pre.geometry.geo_mgr()
    mgr.add('fangpo-x-base-face', shape)

# 拉伸模型
builder = GFE.geometry.geoprim.builder()
shapes = [GFE.Pre.geometry.geo_mgr().find('fangpo-x-base-face').shape()]
extruded = builder.extrude(shapes, [fangpo_up_face_length, 0.0, 0.0])
mgr = Pre.geometry.geo_mgr()
for sp in extruded :
    if not sp.is_null() :
        mgr.add('fangpo-x-base', sp)

# ---------- 绘制放坡y方向-多折线绘制 --------------
# 清空草图
GFE.draft.get_current().clear()
GFE.draft.get_current().set_snap_object(0)
GFE.draft.get_current().set_operate_mode(2)
for point in fangpo_y_base_points:
    GFE.draft.get_current().input(point[0], point[1])

# 填充区域，删除线
GFE.draft.get_current().set_operate_mode(-1)
GFE.draft.get_current().set_snap_object(2)
GFE.draft.get_current().snap_object(-10, fangpo_up_face_length+10, 10, -fangpo_height-10)
GFE.draft.get_current().select_snaped(True)
GFE.draft.get_current().fill_selected()
GFE.draft.get_current().remove_selected()

# 设置xz平面，完成草图创建二维模型
GFE.draft.get_current().set_normal([0.0, 0.0, 0.0], [0.0, -1.0, 0.0], [1.0, 0.0, 0.0])
shape = GFE.draft.get_current().export()
if not shape.is_null() :
    mgr = GFE.Pre.geometry.geo_mgr()
    mgr.add('fangpo-y-base-face', shape)

# 拉伸模型，创建三维模型
builder = GFE.geometry.geoprim.builder()
shapes = [GFE.Pre.geometry.geo_mgr().find('fangpo-y-base-face').shape()]
extruded = builder.extrude(shapes, [0.0, fangpo_up_face_width, 0.0])
mgr = Pre.geometry.geo_mgr()
for sp in extruded :
    if not sp.is_null() :
        mgr.add('fangpo-y-base', sp)

# -------------- 取交两个基础模型，生成基坑-放坡模型 --------------
builder = GFE.geometry.geoprim.builder()
builder.common(['fangpo-x-base', 'fangpo-y-base'],'fangpo')


# ============== 基坑-开挖建模 =============
kaiwa_names = []
# 拉伸底面
geo_obj = GFE.Pre.geometry.geo_mgr().find('fangpo')
minz = 1e10
bottom_face = []
for f in GFE.geometry.geotool.children(geo_obj.shape(), 4):
	fz = GFE.geometry.geotool.centre_of_mass(f)[2]
	if fz < minz:
		minz = fz
		bottom_face = [f]
builder = GFE.geometry.geoprim.builder()
extruded = builder.extrude(bottom_face, [0.0, 0.0, -kaiwa_1_depth])
mgr = Pre.geometry.geo_mgr()
for sp in extruded :
    if not sp.is_null() :
        mgr.add('kaiwa-1', sp)
        kaiwa_names.append('kaiwa-1')

# 多次拉伸底面生成
for i in range(1, kaiwa_num):
	geo_obj = GFE.Pre.geometry.geo_mgr().find(f'kaiwa-{i}')     # kaiwa-123
	minz = 1e10
	bottom_face = []
	for f in GFE.geometry.geotool.children(geo_obj.shape(), 4):
		fz = GFE.geometry.geotool.centre_of_mass(f)[2]
		if fz < minz:
			minz = fz
			bottom_face = [f]
	builder = GFE.geometry.geoprim.builder()
	extruded = builder.extrude(bottom_face, [0.0, 0.0, -kaiwa_2_n_depth])
	mgr = Pre.geometry.geo_mgr()
	for sp in extruded:
		if not sp.is_null():
			name = mgr.auto_name('kaiwa')  # kaiwa-234
			mgr.add(name, sp)
			kaiwa_names.append(name)


# ================== 基坑-内支撑建模 ================
# 清空草图
GFE.draft.get_current().clear()
# 绘制矩形
GFE.draft.get_current().set_snap_object(0)
GFE.draft.get_current().set_operate_mode(3)
# 外矩形
GFE.draft.get_current().input(0.0, 0.0)
GFE.draft.get_current().input(neizhicheng_out_length, neizhicheng_out_width)
x1 = (neizhicheng_out_length - neizhicheng_in_length) / 2
y1 = (neizhicheng_out_width - neizhicheng_in_width) / 2
x2 = neizhicheng_out_length - x1
y2 = neizhicheng_out_width - y1
# 内矩形
GFE.draft.get_current().input(x1, y1)
GFE.draft.get_current().input(x2, y2)

# 绘制内部线条----直线
GFE.draft.get_current().set_snap_object(0)
GFE.draft.get_current().set_operate_mode(1)
# 遍历点集，步长为2，两点一线
for i in range(0, len(neizhicheng_in_lines), 2):
    point1 = neizhicheng_in_lines[i]
    point2 = neizhicheng_in_lines[i+1]
    GFE.draft.get_current().input(point1[0], point1[1])
    GFE.draft.get_current().input(point2[0], point2[1])

# 设置草图xy平面，完成草图，创建内支撑二维模型
GFE.draft.get_current().set_normal([0.0, 0.0, 0.0], [0.0, 0.0, 1.0], [1.0, 0.0, 0.0])
shape = GFE.draft.get_current().export()
if not shape.is_null() :
    mgr = GFE.Pre.geometry.geo_mgr()
    mgr.add('neizhicheng-1', shape)

# 平移内支撑
builder = GFE.geometry.geoprim.builder()
builder.translate(['neizhicheng-1'], [fangpo_down_face_spacing, fangpo_down_face_spacing, -fangpo_height], False)

# 阵列内支撑
builder = GFE.geometry.geoprim.builder()
shapes = [GFE.Pre.geometry.geo_mgr().find('neizhicheng-1').shape()]
new_shapes = builder.make_array(shapes, 1, 1, 2, [0.0, 0.0, -(kaiwa_1_depth + kaiwa_2_n_depth)])
mgr = Pre.geometry.geo_mgr()
for sp in new_shapes :
    if not sp.is_null() :
        mgr.add('neizhicheng-2', sp)


# =================== 基坑-立柱建模 ===================
lizhu_names = []
# 拉伸内支撑顶点生成立柱
# 已知内支撑的x最值为1和41，y最值为1和26
min_x = fangpo_down_face_spacing
max_x = fangpo_up_face_length - fangpo_down_face_spacing
min_y = fangpo_down_face_spacing
max_y = fangpo_up_face_width - fangpo_down_face_spacing
need_nodes_sp = []
geo_obj = GFE.Pre.geometry.geo_mgr().find('neizhicheng-1')
for n in GFE.geometry.geotool.children(geo_obj.shape(), 7):
	nx, ny, nz = GFE.geometry.geotool.centre_of_mass(n)
    # 取范围内顶点（增加容差）
	if min_x+0.1 < nx < max_x-0.1 and min_y+0.1 < ny < max_y-0.1:
		need_nodes_sp.append(n)
builder = GFE.geometry.geoprim.builder()
extruded = builder.extrude(need_nodes_sp, [0.0, 0.0, -lizhu_height])
mgr = Pre.geometry.geo_mgr()
for sp in extruded :
	if not sp.is_null() :
		name = mgr.auto_name('lizhu')
		mgr.add(name, sp)
		lizhu_names.append(name)

# ============== 合并模型 ==============
merge_names = ['fangpo', 'neizhicheng-1', 'neizhicheng-2']
merge_names.extend(kaiwa_names)     # 追加开挖
merge_names.extend(lizhu_names)     # 追加立柱

builder = GFE.geometry.geoprim.builder()
builder.merge(merge_names, False,'')

# #移除几何
# delete_names = ['fangpo-x-base-face', 'fangpo-y-base-face', 'fangpo-x-base', 'fangpo-y-base']
# delete_names.extend(merge_names)    # 追加
# GFE.Pre.geometry.geo_mgr().delete(delete_names)


# =================== 创建材料 =================
# 创建材料
obj = GFE.Pre.material.material()
obj.name = material[0]
obj_density = GFE.Pre.material.density()
obj_density.temp_dp = False
obj_density.n_param = 1
obj_density.params = [material[1]]
obj_ela = GFE.Pre.material.elastic()
obj_ela.temp_dp = False
obj_ela.n_param = 2
obj_ela.type = 0
obj_ela.moduli_time_scale = 0
obj_ela.compression = False
obj_ela.tension = False
obj_ela.params = [material[2], material[3]]
obj.entries = [obj_density, obj_ela]
GFE.Pre.material.mat_mgr().add(obj)

# 导入土体材料
import GFE.io
io_instance = GFE.io.get_current()
io_instance.import_mat(soil_materials_path)

# ============== 创建一维土层 ===============
obj = GFE.Pre.soil.soil()
obj.name = 'Soil1D-1'
obj.depth = soil_depth
obj.materials = soil_materials
obj.bedrock_mat = soil_materials[-1]
obj.depth_dir = 2
GFE.Pre.soil.soil_mgr().add(obj)

# ============ 创建三维土体 =============
builder = GFE.soil.box_builder()
soil = GFE.Pre.soil.soil_mgr().find('Soil1D-1')
builder.set_height(soil.depth, soil.depth_dir)
builder.set_parameter(soil_length, soil_width)
soil_shape = builder.build()
builder2 = GFE.soil.data_builder()
builder2.dimension = 3
builder2.name = 'Soil-1'
builder2.layer_shape = soil_shape
builder2.layer_material = soil.materials
builder2.build()

# --------- 平移基坑 ---------
# 计算【基坑上表面y负方向边界线】和【土体上表面y负方向边界线】形心向量差
center1 = [fangpo_up_face_length / 2, 0, 0]
# 获取土体上表面y负方向边界线形心
top_face_x = None
front_face_y = 1e10
top_face_z = -1e10
geo_obj = GFE.Pre.geometry.geo_mgr().find('Soil-1')
for f in GFE.geometry.geotool.children(geo_obj.shape(), 4):
	fx, fy, fz = GFE.geometry.geotool.centre_of_mass(f)
	if fz > top_face_z:
		top_face_z = fz
		top_face_x = fx
	if fy < front_face_y:
		front_face_y = fy
center2 = [top_face_x, front_face_y, top_face_z]
print(f"基坑上表面y负方向边界线形心坐标：{center1}")
print(f"土体上表面y负方向边界线形心坐标：{center2}")

trsf_vec = [center2[i] - center1[i] for i in range(3)]
builder = GFE.geometry.geoprim.builder()
builder.translate(['Merge-1'], trsf_vec, False)
builder = GFE.geometry.geoprim.builder()
builder.translate(['Merge-1'], [0.0, jikeng_soil_boundary_spacing, 0.0], False)

# -------- 分割土体模型 --------
builder = GFE.geometry.geoprim.builder()
builder.split('Soil-1', ['Merge-1'], True)


# ============== 导入YJK模型 ===============
from GFE import io as gfeio
yjk_para = [1, 1, 0, 1, 1, 1, 1, 1,
300, 5, 800, 0, 600, 2800, 200, 610,
150, 3, 1, 0, 5, 250, 0, 0,
1, 0, 10, 300, 140, 260, 80, 160,
400, 0, 310, 50, 0, 260, 0, 100,
0, 0, 0]
yjk_para2 = ['', '']
gfeio.get_current().import_yjk(yjk_file_path, yjk_para, yjk_para2, True, '', False)
GFE.Pre.document.set_application_by_ui()


# ============= 平移和裁剪土体 ================
# 计算【土体上表面y正方向边界线】和【yjk地下室上表面y正方向边界线】形心向量差
# 获取土体上表面y正方向边界线形心
top_face_x = None
back_face_y = -1e10
top_face_z = -1e10
geo_obj = GFE.Pre.geometry.geo_mgr().find('Soil-1')
for f in GFE.geometry.geotool.children(geo_obj.shape(), 4):
	fx, fy, fz = GFE.geometry.geotool.centre_of_mass(f)
	if fz > top_face_z:
		top_face_z = fz
		top_face_x = fx
	if fy > back_face_y:
		back_face_y = fy
center1 = [top_face_x, back_face_y, top_face_z]

# 获取yjk地下室上表面y正方向边界线形心
top_face_x = None
back_face_y = -1e10
top_face_z = -1e10
geo_obj = GFE.Pre.geometry.geo_mgr().find('BasementBoundary')
for f in GFE.geometry.geotool.children(geo_obj.shape(), 4):
	fx, fy, fz = GFE.geometry.geotool.centre_of_mass(f)
	if fz > top_face_z:
		top_face_z = fz
		top_face_x = fx
	if fy > back_face_y:
		back_face_y = fy
center2 = [top_face_x, back_face_y, top_face_z]
print(f"土体上表面y正方向边界线形心坐标：{center1}")
print(f"yjk地下室上表面y正方向边界线形心坐标：{center2}")

trsf_vec = [center2[i] - center1[i] for i in range(3)]
builder = GFE.geometry.geoprim.builder()
builder.translate(['Soil-1'], trsf_vec, False)
# 平移结构
builder = GFE.geometry.geoprim.builder()
builder.translate(['SuperStru', 'BasementBoundary'], [0.0, -yjk_soil_boundary_spacing, 0.0], False)

# 裁剪土体-结构
builder = GFE.geometry.geoprim.builder()
builder.cut('Soil-1', ['BasementBoundary'], True)

# =============== 创建土体-【放坡和开挖】的集合 ================
# 1.获取土体上表面y负方向边界线形心
soil_top_front_x = None
soil_top_front_y = 1e10
soil_top_front_z = -1e10
soil_obj = GFE.Pre.geometry.geo_mgr().find('Soil-1')
for f in GFE.geometry.geotool.children(soil_obj.shape(), 4):
	fx, fy, fz = GFE.geometry.geotool.centre_of_mass(f)
	if fz > soil_top_front_z:
		soil_top_front_z = fz
		soil_top_front_x = fx
	if fy < soil_top_front_y:
		soil_top_front_y = fy
soil_top_front_center = [soil_top_front_x, soil_top_front_y, soil_top_front_z]
print(f"最终土体上表面y负方向边界线坐标：{soil_top_front_center}")

# 2. 计算土体里的基坑范围
jikeng_min_x = soil_top_front_x - fangpo_up_face_length/2
jikeng_max_x = soil_top_front_x + fangpo_up_face_length/2
jikeng_min_y = soil_top_front_y + jikeng_soil_boundary_spacing
jikeng_max_y = soil_top_front_y + jikeng_soil_boundary_spacing + fangpo_up_face_width
print(f"土体里的基坑范围：x方向[ {jikeng_min_x} 到 {jikeng_max_x} ]，y方向[ {jikeng_min_y} 到 {jikeng_max_y} ]")
# 3. 创建集合
for s in GFE.geometry.geotool.children(soil_obj.shape(), 2):
    sx, sy, sz = GFE.geometry.geotool.centre_of_mass(s)
    # 判定当前实体是基坑结构之一
    if jikeng_min_x-0.1 < sx < jikeng_max_x+0.1 and jikeng_min_y-0.1 < sy < jikeng_max_y+0.1:
        # 1. 放坡层：固定范围
        if -fangpo_height < sz < 0:
            GFE.Pre.set.gset_mgr().add('Set-fangpo', [s])
        # 2. 开挖1层：固定范围
        elif -(fangpo_height + kaiwa_1_depth) < sz < -fangpo_height:
            GFE.Pre.set.gset_mgr().add('Set-kaiwa1', [s])
        # 3. 开挖2到kaiwa_num层：动态循环判断（核心优化）
        else:
            # 计算开挖1层的结束深度（作为后续开挖层的起始基准）
            base_depth = fangpo_height + kaiwa_1_depth
            # 循环处理开挖2到kaiwa_num层（i从2到kaiwa_num）
            for i in range(2, kaiwa_num + 1):
                # 计算当前开挖层的上边界（前一层的下边界）
                upper_bound = -(base_depth + kaiwa_2_n_depth * (i - 2))
                # 计算当前开挖层的下边界
                lower_bound = -(base_depth + kaiwa_2_n_depth * (i - 1))
                # 判断sz是否在当前开挖层范围内
                if lower_bound < sz < upper_bound:
                    set_name = f'Set-kaiwa{i}'  # 动态生成集合名称
                    GFE.Pre.set.gset_mgr().add(set_name, [s])
                    break  # 找到匹配层后退出循环，避免重复判断


# ================ 创建喷射混凝土集合 ===============
need_faces_sp = []
geo_obj = GFE.Pre.geometry.geo_mgr().find('Soil-1')
for f in GFE.geometry.geotool.children(geo_obj.shape(), 4):
	fx, fy, fz = GFE.geometry.geotool.centre_of_mass(f)
	if jikeng_min_x - 0.1 < fx < jikeng_max_x + 0.1 and jikeng_min_y - 0.1 < fy < jikeng_max_y + 0.1:  # 判定当前实体是基坑结构之一
		if -fangpo_height < fz < 0:
			need_faces_sp.append(f)
GFE.Pre.set.gset_mgr().add('Set-pshnt', need_faces_sp)


# ============== 创建地连墙集合 ===============
dlq_left_pos = jikeng_min_x + fangpo_down_face_spacing
dlq_right_pos = jikeng_max_x - fangpo_down_face_spacing
dlq_front_pos = jikeng_min_y + fangpo_down_face_spacing
dlq_back_pos = jikeng_max_y - fangpo_down_face_spacing
need_faces_sp = []
geo_obj = GFE.Pre.geometry.geo_mgr().find('Soil-1')
for f in GFE.geometry.geotool.children(geo_obj.shape(), 4):
	fx, fy, fz = GFE.geometry.geotool.centre_of_mass(f)
	if dlq_left_pos-0.1 < fx < dlq_left_pos+0.1:    # 质心存在精度问题
		need_faces_sp.append(f)
	if dlq_right_pos-0.1 < fx < dlq_right_pos+0.1:
		need_faces_sp.append(f)
	if dlq_front_pos-0.1 < fy < dlq_front_pos+0.1:
		need_faces_sp.append(f)
	if dlq_back_pos-0.1 < fy < dlq_back_pos+0.1:
		need_faces_sp.append(f)
GFE.Pre.set.gset_mgr().add('Set-dilianqiang', need_faces_sp)

# ================ 创建内支撑集合1 ==============
# 注意！！！需要移除边框
need_edges_sp = []
geo_obj = GFE.Pre.geometry.geo_mgr().find('Soil-1')
for e in GFE.geometry.geotool.children(geo_obj.shape(), 6):
	ex, ey, ez = GFE.geometry.geotool.centre_of_mass(e)
	if -fangpo_height-0.1 < ez < -fangpo_height+0.1:
		if dlq_left_pos+0.1 < ex < dlq_right_pos-0.1 and dlq_front_pos+0.1 < ey < dlq_back_pos-0.1: # 移除边框
			need_edges_sp.append(e)
GFE.Pre.set.gset_mgr().add('Set-neizhicheng1', need_edges_sp)

# =============== 创建内支撑集合2 ================
# 注意！！！需要移除边框
need_edges_sp_nzc2 = []
geo_obj = GFE.Pre.geometry.geo_mgr().find('Soil-1')
for e in GFE.geometry.geotool.children(geo_obj.shape(), 6):
	ex, ey, ez = GFE.geometry.geotool.centre_of_mass(e)
	if -(fangpo_height + kaiwa_1_depth + kaiwa_2_n_depth)-0.1 < ez < -(fangpo_height + kaiwa_1_depth + kaiwa_2_n_depth)+0.1:
		if dlq_left_pos+0.1 < ex < dlq_right_pos-0.1 and dlq_front_pos+0.1 < ey < dlq_back_pos-0.1: # 移除边框
			need_edges_sp_nzc2.append(e)
GFE.Pre.set.gset_mgr().add('Set-neizhicheng2', need_edges_sp_nzc2)

# ============== 创建立柱集合 =============
# 已知立柱是内支撑1内节点拉伸可得，所以z轴坐标是小于-fangpo_height，xy范围是内支撑内部
# 注意！！！！！！要去除内支撑2的边
need_edges_sp_lz = []
geo_obj = GFE.Pre.geometry.geo_mgr().find('Soil-1')
# 1.初步获取内支撑范围内所有边
for e in GFE.geometry.geotool.children(geo_obj.shape(), 6):
	ex, ey, ez = GFE.geometry.geotool.centre_of_mass(e)
	if ez <-fangpo_height-0.1:
		if dlq_left_pos+0.1 < ex < dlq_right_pos-0.1 and dlq_front_pos+0.1 < ey < dlq_back_pos-0.1: # 内支撑范围内
			need_edges_sp_lz.append(e)
# 2.去除多选的内支撑2的边，得到立柱所有边
need_edges_sp_lz = [x for x in need_edges_sp_lz if x not in need_edges_sp_nzc2]
GFE.Pre.set.gset_mgr().add('Set-lizhu', need_edges_sp_lz)


# ============== 网格划分 =============
# 结构网格划分
from GFE.geometry import mesh_generator
generator = mesh_generator.generator()
controller = mesh_generator.controller()
controller.number_option = {
'General.ExpertMode' : 1.0,
'General.NumThreads' : 0.0,
'General.Terminal' : 1.0,
'Mesh.Algorithm' : 8.0,
'Mesh.Algorithm3D' : 10.0,
'Mesh.AngleToleranceFacetOverlap' : 0.001,
'Mesh.ElementOrder' : 1.0,
'Mesh.MeshSizeExtendFromBoundary' : 1.0,
'Mesh.MeshSizeFromCurvature' : 0.0,
'Mesh.MeshSizeFromPoints' : 1.0,
'Mesh.MeshSizeMax' : 1e+22,
'Mesh.MeshSizeMin' : 0.0,
'Mesh.Optimize' : 1.0,
'Mesh.RecombinationAlgorithm' : 0.0,
}
controller.string_option = {}
controller.user_option = {
'GFE.AutoTransfinite' : True,
'GFE.DefaultSize' : yjk_mesh_size,
'GFE.Optimize' : False,
'GFE.Recombine2D' : False,
}
controller.geom_to_type = {
0 : 0,
1 : 5,
2 : 9,
3 : 14,
4 : 17,
5 : 19,
6 : 20,
7 : 22,
8 : 17,
}
controller.generate_dim = 3
controller.auto_transfinite = True
generator.mesh(['SuperStru'], controller)

# 土体网格划分
from GFE.geometry import mesh_generator
generator = mesh_generator.generator()
controller = mesh_generator.controller()
controller.number_option = {
'General.ExpertMode' : 1.0,
'General.NumThreads' : 0.0,
'General.Terminal' : 1.0,
'Mesh.Algorithm' : 2.0,
'Mesh.Algorithm3D' : 10.0,
'Mesh.AngleToleranceFacetOverlap' : 0.001,
'Mesh.ElementOrder' : 1.0,
'Mesh.MeshSizeExtendFromBoundary' : 1.0,
'Mesh.MeshSizeFromCurvature' : 0.0,
'Mesh.MeshSizeFromPoints' : 1.0,
'Mesh.MeshSizeMax' : 1e+22,
'Mesh.MeshSizeMin' : 0.0,
'Mesh.Optimize' : 1.0,
'Mesh.RecombinationAlgorithm' : 0.0,
}
controller.string_option = {}
controller.user_option = {
'GFE.AutoTransfinite' : True,
'GFE.DefaultSize' : soil_mesh_size,
'GFE.Optimize' : False,
'GFE.Recombine2D' : False,
}
controller.geom_to_type = {
0 : 0,
1 : 5,
2 : 9,
3 : 14,
4 : 17,
5 : 19,
6 : 20,
7 : 22,
8 : 17,
}
controller.generate_dim = 3
controller.auto_transfinite = True
generator.mesh(['Soil-1'], controller)


# ============= 网格复制 ==============
# 喷射混凝土
from GFE.geometry import geotool
GFE.geometry.geotool.copy_mesh(
    name="Set-pshnt",
    origin_node=True,
    as_source=False,
    type_name="S3",
    new_set_name="pshnt-1"
)
# 地连墙
GFE.geometry.geotool.copy_mesh(
    name="Set-dilianqiang",
    origin_node=True,
    as_source=False,
    type_name="S3",
    new_set_name="dilianqiang-1"
)
# 内支撑1
GFE.geometry.geotool.copy_mesh(
    name="Set-neizhicheng1",
    origin_node=True,
    as_source=False,
    type_name="B31",
    new_set_name="neizhicheng1-1"
)
# 内支撑2
GFE.geometry.geotool.copy_mesh(
    name="Set-neizhicheng2",
    origin_node=True,
    as_source=False,
    type_name="B31",
    new_set_name="neizhicheng2-1"
)
# 立柱
GFE.geometry.geotool.copy_mesh(
    name="Set-lizhu",
    origin_node=True,
    as_source=False,
    type_name="B31",
    new_set_name="lizhu-1"
)


# ============= 截面属性 ===============
# 放坡
prop = GFE.Pre.section.property_shell()
prop.name = 'pshnt'
prop.elset_name = 'pshnt-1'
prop.mat_name = 'C35'
prop.thickness = fangpo_thickness
prop.integral_point = 5
prop.layer_num = 1
prop.params = []
prop.has_rebar = False
prop.rebar = GFE.Pre.section.rebar_layer()
prop.Ecc = [0.0, 0.0, 0.0, 0.0]
GFE.Pre.section.sect_mgr().add(prop)

# 地连墙
prop = GFE.Pre.section.property_shell()
prop.name = 'diliamqiang'
prop.elset_name = 'dilianqiang-1'
prop.mat_name = 'C35'
prop.thickness = dilianqiang_thickness
prop.integral_point = 5
prop.layer_num = 1
prop.params = []
prop.has_rebar = False
prop.rebar = GFE.Pre.section.rebar_layer()
prop.Ecc = [0.0, 0.0, 0.0, 0.0]
GFE.Pre.section.sect_mgr().add(prop)

# 立柱
prop = GFE.Pre.section.property_beam()
prop.name = 'lizhu'
prop.elset_name = 'lizhu-1'
prop.shape = 3
prop.mat_name = 'C35'
prop.fiber_num = 1
prop.shape_params = [lizhu_radius]
prop.params = []
prop.direction = [1.0, 0.0, 0.0]
prop.shear = [9.27752e+06, 9.27752e+06]
prop.Ecc = [0.0, 0.0, 0.0, 0.0]
GFE.Pre.section.sect_mgr().add(prop)

# 内支撑1
prop = GFE.Pre.section.property_beam()
prop.name = 'neizhicheng1'
prop.elset_name = 'neizhicheng1-1'
prop.shape = 2
prop.mat_name = 'Q345'
prop.fiber_num = 1
prop.shape_params = neizhicheng_section_params
prop.params = []
prop.direction = [0.0, 0.0, 1.0]
prop.shear = [3.43333e+06, 3.296e+06]
prop.Ecc = [0.0, 0.0, 0.0, 0.0]
GFE.Pre.section.sect_mgr().add(prop)

# 内支撑2
prop = GFE.Pre.section.property_beam()
prop.name = 'neizhicheng2'
prop.elset_name = 'neizhicheng2-1'
prop.shape = 2
prop.mat_name = 'Q345'
prop.fiber_num = 1
prop.shape_params = neizhicheng_section_params
prop.params = []
prop.direction = [0.0, 0.0, 1.0]
prop.shear = [3.43333e+06, 3.296e+06]
prop.Ecc = [0.0, 0.0, 0.0, 0.0]
GFE.Pre.section.sect_mgr().add(prop)


# ============= 绑定约束 =============
# 搜索接触対
search_list = []
search_list.append(['Soil-1', 'SuperStru'])
from GFE.geometry import contact_pair as cp
search_result = []
for pair in search_list :
    masterid = GFE.Pre.geometry.geo_mgr().find(pair[0]).id()
    slaveid = GFE.Pre.geometry.geo_mgr().find(pair[1]).id()
    cplist = cp.search_face(pair[0], pair[1], 0.01)
    for pairs in cplist :
        master = [[masterid] + list(x) for x in pairs[0]]
        slave = [[slaveid] + list(x) for x in pairs[1]]
        search_result.append([master, slave])

# 绑定约束
geo_mgr = GFE.Pre.geometry.geo_mgr()
surf_mgr = GFE.Pre.surface.surface_mgr()
tie_mgr = GFE.Pre.interaction.tie_mgr()
for i in range(len(search_result)) :
    result = search_result[i]
    geo1_name = geo_mgr.find(result[0][0][0]).name
    geo2_name = geo_mgr.find(result[1][0][0]).name
    master_name = 'CP-' + geo1_name + '-' + geo2_name + '-' + str(i + 1) + '-master'
    master = GFE.Pre.surface.geometry_surface(master_name)
    slave_name = 'CP-' + geo1_name + '-' + geo2_name + '-' + str(i + 1) + '-slave'
    slave = GFE.Pre.surface.geometry_surface(slave_name)
    master.data = result[0]
    slave.data = result[1]
    surf_mgr.add(master)
    surf_mgr.add(slave)
    surfpair = GFE.Pre.interaction.surface_pair()
    surfpair.name = tie_mgr.auto_name('Tie')
    surfpair.first_surf = master.name
    surfpair.second_surf = slave.name
    surfpair.param_number = 1
    surfpair.parameters = [0.01]
    tie_mgr.add(surfpair)

# ================== 边界与荷载 ====================
# 创建土体底面及侧面x和y方向集合
geo_obj = GFE.Pre.geometry.geo_mgr().find('Soil-1')
minx = miny = minz = 1e10
maxx = maxy =-1e10
bottom_face = []
left_faces, right_faces = [],[]
front_faces, back_faces = [],[]
for f in GFE.geometry.geotool.children(geo_obj.shape(), 4):	#2实体，4面，6边
	fx, fy, fz = GFE.geometry.geotool.centre_of_mass(f)
	if fz < minz:		#底
		minz = fz
		bottom_face = [f]
	if minx-0.1< fx <minx+0.1:		#左
		left_faces.append(f)
	elif fx < minx-0.1:
		left_faces = []
		minx = fx
		left_faces.append(f)
	if maxx-0.1< fx <maxx+0.1:		#右
		right_faces.append(f)
	elif fx >maxx+0.1:
		right_faces = []
		maxx = fx
		right_faces.append(f)
	if miny-0.1< fy <miny+0.1:		#前
		front_faces.append(f)
	elif fy <miny-0.1:
		front_faces = []
		miny = fy
		front_faces.append(f)
	if maxy-0.1< fy <maxy+0.1:		#后
		back_faces.append(f)
	elif fy >maxy+0.1:
		back_faces = []
		maxy = fy
		back_faces.append(f)
x_faces = left_faces + right_faces
y_faces = front_faces + back_faces
GFE.Pre.set.gset_mgr().add('bc-z', bottom_face)
GFE.Pre.set.gset_mgr().add('bc-x', x_faces)
GFE.Pre.set.gset_mgr().add('bc-y', y_faces)

# 创建约束
obj = GFE.Pre.boundary.boundary()
obj.type = 0
obj.name = 'BC-z'
obj.set = 'bc-z'
obj.valid_dof = 0
obj.value = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
obj.amplitude = ''
obj.value_im = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
obj.amplitude_im = ''
obj.distribution = ''
GFE.Pre.boundary.bc_mgr().add(obj)

obj = GFE.Pre.boundary.boundary()
obj.type = 1
obj.name = 'BC-x'
obj.set = 'bc-x'
obj.valid_dof = 1
obj.value = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
obj.amplitude = ''
obj.value_im = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
obj.amplitude_im = ''
obj.distribution = ''
GFE.Pre.boundary.bc_mgr().add(obj)

obj = GFE.Pre.boundary.boundary()
obj.type = 1
obj.name = 'BC-y'
obj.set = 'bc-y'
obj.valid_dof = 2
obj.value = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
obj.amplitude = ''
obj.value_im = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
obj.amplitude_im = ''
obj.distribution = ''
GFE.Pre.boundary.bc_mgr().add(obj)



# ============== 场输出 =============
obj = GFE.Pre.output.output_request()
obj.name = 'FO-Static'
obj.step = ''
obj.type = 0
obj.method = 0
obj.time_type = 0
obj.time_interval = 1.0
obj.number_interval = 0
obj.frequency = 0
obj.var_option = -1
obj.time_points = ''
obj_sub1 = GFE.Pre.output.node_output()
obj_sub1.name = 'SubOut-1'
obj_sub1.variables = ['RF', 'RM', 'U', 'UR']
obj_sub1.var_option = -1
obj_sub1.reg_type = -1
obj_sub1.nset = ''
obj_sub2 = GFE.Pre.output.element_output()
obj_sub2.name = 'SubOut-2'
obj_sub2.variables = ['E', 'PE', 'PEEQ', 'S', 'SF', 'SM']
obj_sub2.var_option = -1
obj_sub2.reg_type = -1
obj_sub2.elset = ''
obj.sub_output = [obj_sub1, obj_sub2]
GFE.Pre.output.field_mgr().edit(obj)

# ================ 分析步 ================
# 静力（地应力平衡）
obj = GFE.Pre.step.geo_static_step()
obj.name = 'GeoStatic-1'
obj.description = ''
obj.nlgeom = True
obj.init_inc = 1.0
obj.period = 1.0
obj.min_inc = 1e-05
obj.max_inc = 1.0
GFE.Pre.step.step_mgr().add(obj)

# 静力（放坡）
obj = GFE.Pre.step.static_general_step()
obj.name = 'fangpo'
obj.description = ''
obj.nlgeom = True
obj.init_inc = 1.0
obj.period = 1.0
obj.min_inc = 1e-05
obj.max_inc = 1.0
GFE.Pre.step.step_mgr().add(obj)

steps = ['Initial', 'GeoStatic-1', 'fangpo']
# 静力（开挖）
for i in range(1, kaiwa_num+1):
    obj = GFE.Pre.step.static_general_step()
    obj.name = f'kaiwa{i}'
    obj.description = ''
    obj.nlgeom = True
    obj.init_inc = 1.0
    obj.period = 1.0
    obj.min_inc = 1e-05
    obj.max_inc = 1.0
    GFE.Pre.step.step_mgr().add(obj)
    # 添加开挖
    steps.append(obj.name)


# =============== 工况 ==============
case_obj = GFE.Pre.case.case()
case_obj.name = 'jikengkaiwa'
case_obj.steps = steps

case_obj.bcs['Initial'] = ['BC-z', 'BC-x', 'BC-y']
case_obj.bcs['GeoStatic-1'] = ['AllGrav']
case_obj.initialConditions['Initial'] = []
case_obj.fieldReqs['GeoStatic-1'] = ['FO-Static']
case_obj.fieldReqs['fangpo'] = ['FO-Static']
case_obj.elemAdd['fangpo'] = ['pshnt-1', 'dilianqiang-1', 'neizhicheng1-1', 'lizhu-1']
case_obj.elemDel['GeoStatic-1'] = ['pshnt-1', 'dilianqiang-1', 'neizhicheng1-1', 'neizhicheng2-1', 'lizhu-1']
case_obj.elemDel['fangpo'] = ['Set-fangpo']

for i in range(1, kaiwa_num + 1):
    kaiwa_name = f'kaiwa{i}'
    case_obj.fieldReqs[kaiwa_name] = ['FO-Static']
    case_obj.elemDel[kaiwa_name] = [f'Set-kaiwa{i}']
    # 当开挖进度到2时，增加内支撑2
    if i == 2:
        case_obj.elemAdd[kaiwa_name] = ['neizhicheng2-1']

GFE.Pre.case.case_mgr().add(case_obj)


# ============== 创建作业 ==============
# 写出inp文件
from GFE.io import inpio
inpwriter = inpio.writer(inp_path)
inpwriter.set_case('jikengkaiwa')
inpwriter.perform()
```
