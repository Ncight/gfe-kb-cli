# GFE2026-CM-ch03-CM3-update2
> 来源：E:\GFE2026\典型案例与教程\第3章 华夫板框架结构频响分析案例\CM3-update2.py（GFE2026 官方典型案例命令流，v3.x 代际金标准）。raw 不可变源副本，2026-06-11 入库。

```python
import GFE
from GFE import *
from GFE.Pre import *
from GFE.occ import *

from GFE.geometry import geotool

GFE.Pre.document.set_application_by_ui()

# 注意！！！若修改参数后，在网格划分好后，节点Set-cload有可能不存在，需适当调整参数

# =========== 路径定义 ==========
import os
import sys
# 获取当前exe路径
exe_file_path = os.path.abspath(sys.executable)
# 获取当前exe文件夹路径
exe_dir_path = os.path.dirname(exe_file_path)
# 获取上一级目录
parent_path = os.path.dirname(exe_dir_path)
# 增加文件/夹名称
plugin_dir = os.path.join(parent_path, "典型案例与教程")
plugin_dir2 = os.path.join(plugin_dir, "第3章")
inp_path = os.path.join(plugin_dir2, "CM3-Case-SSD.inp")
# 转为绝对路径
inp_path = os.path.abspath(inp_path)

print(inp_path)

# =========== 参数定义 ===========
# 1. 材料参数：(名称, 密度, 弹性杨模E, 弹性泊松比v)
materials = [
    ('C30', 2.5, 3e+07, 0.2)
]

# 2. 模型参数
wafer_length = 48.0			        # 华夫板长度---x轴
wafer_width = 48.0			        # 华夫板宽度---y轴
wafer_thickness = 0.5		        # 华夫板厚度
wafer_hole_group_x_num = 6		    # 华夫板圆孔一组x方向数量（必须能均分华夫板-长）
wafer_hole_group_y_num = 6		    # 华夫板圆孔一组y方向数量（必须能均分华夫板-宽）
wafer_hole_x_num = 8		        # 华夫板单组圆孔x方向数量
wafer_hole_y_num = 8		        # 华夫板单组圆孔y方向数量
wafer_hole_radius = 0.25		    # 华夫板圆孔半径

wafer_hole_spacing = wafer_hole_radius * 2 + 0.4      # 华夫板单组圆孔间距 (XY通用，可拓展为独立间距)
wafer_hole_group_spacing_x = wafer_length / wafer_hole_group_x_num  # X轴 圆孔组组间距
wafer_hole_group_spacing_y = wafer_width / wafer_hole_group_y_num   # Y轴 圆孔组组间距

wafer_hole_offset_x = (wafer_hole_group_spacing_x - (wafer_hole_x_num - 1)*wafer_hole_spacing) / 2    # X轴 第一个圆孔圆心偏移量
wafer_hole_offset_y = (wafer_hole_group_spacing_y - (wafer_hole_y_num - 1)*wafer_hole_spacing) / 2    # Y轴 第一个圆孔圆心偏移量
wafer_hole_offset_x = round(wafer_hole_offset_x, 4)     # 保留4位小数
wafer_hole_offset_y = round(wafer_hole_offset_y, 4)     # 保留4位小数

print(f"圆孔间距：{wafer_hole_spacing}\n"
      f"圆孔组X间距：{wafer_hole_group_spacing_x}, 圆孔组Y间距：{wafer_hole_group_spacing_y}\n"
      f"第一个圆孔X轴偏移量：{wafer_hole_offset_x}, Y轴偏移量：{wafer_hole_offset_y}")

raft_length = wafer_length		    # 筏板长度（与华夫板同）
raft_width = wafer_width			# 筏板宽度（与华夫板同）
raft_offset_z = 4.0				    # 筏板距华夫板底面（0,0,0）距离

roof_length = wafer_length			# 屋面板长度（与华夫板同）
roof_width = wafer_width			# 屋面板宽度（与华夫板同）
roof_lz_spacing_x = wafer_length / wafer_hole_group_x_num				# 梁柱x间距【长/圆孔组x数量】
roof_lz_spacing_y = wafer_width / wafer_hole_group_y_num				# 梁柱y间距【宽/圆孔组y方向数量】
roof_lz_spacing_x = round(roof_lz_spacing_x, 4)     # 保留4位小数
roof_lz_spacing_y = round(roof_lz_spacing_y, 4)     # 保留4位小数
print(f"屋面板梁柱x方向间距：{roof_lz_spacing_x}, y方向间距：{roof_lz_spacing_y}")
roof_lz_num_x = wafer_hole_group_x_num - 1
roof_lz_num_y = wafer_hole_group_y_num - 1
roof_offset_z = 4.0				    # 屋面板距华夫板底面（0,0,0）距离

col_height = raft_offset_z + roof_offset_z		# 立柱高度
col_spacing_x = roof_lz_spacing_x			        # 立柱x间距【同屋面板间距】
col_spacing_y = roof_lz_spacing_y			        # 立柱y间距【同屋面板间距】
x_col_num = wafer_hole_group_x_num + 1
y_col_num = wafer_hole_group_y_num + 1

# 3. 截面参数
raft_section_thickness = 0.3                # 筏板壳厚度
roof_section_thickness = 0.15               # 屋面板壳厚度
col_section_size = [0.6, 0.6]               # 矩形立柱截面尺寸
roof_lz_section_size = [0.8, 0.3]           # 矩形屋面板梁柱截面尺寸

# 4. 网格
mesh_size = 1.0			    # 网格尺寸
wafer_mesh_size = 0.5		# 华夫板0.5网格


# ========= 创建材料 ===========
# materials[0]是第一个材料c30
obj = GFE.Pre.material.material()
obj.name = materials[0][0]
obj_density = GFE.Pre.material.density()
obj_density.temp_dp = False
obj_density.n_param = 1
obj_density.params = [materials[0][1]]
obj_ela = GFE.Pre.material.elastic()
obj_ela.temp_dp = False
obj_ela.n_param = 2
obj_ela.type = 0
obj_ela.moduli_time_scale = 0
obj_ela.compression = False
obj_ela.tension = False
obj_ela.params = [materials[0][2], materials[0][3]]
obj.entries = [obj_density, obj_ela]
GFE.Pre.material.mat_mgr().add(obj)

# =========== 创建华夫板模型 ==========
# 设置草图xy
GFE.draft.get_current().set_normal([0.0, 0.0, 0.0], [0.0, 0.0, 1.0], [1.0, 0.0, 0.0])

# 设置选择矩形
GFE.draft.get_current().set_snap_object(0)
GFE.draft.get_current().set_operate_mode(3)
# 绘制矩形
GFE.draft.get_current().input(0.0, 0.0)
GFE.draft.get_current().input(wafer_length, wafer_width)

# 绘制圆形
GFE.draft.get_current().set_snap_object(0)
GFE.draft.get_current().set_operate_mode(7)
GFE.draft.get_current().input(wafer_hole_offset_x, wafer_hole_offset_y)
GFE.draft.get_current().input(wafer_hole_offset_x, wafer_hole_offset_y + wafer_hole_radius)

# 选择线模式
GFE.draft.get_current().set_operate_mode(-1)
GFE.draft.get_current().set_snap_object(2)
# 阵列圆形
GFE.draft.get_current().snap_object(wafer_hole_offset_x, wafer_hole_offset_y + wafer_hole_radius)
GFE.draft.get_current().select_snaped(False)
GFE.draft.get_current().set_operate_mode(14)
GFE.draft.get_current().array_selected(wafer_hole_x_num, wafer_hole_y_num, wafer_hole_spacing, wafer_hole_spacing)
# 再次阵列圆形组
x_min_range = wafer_hole_offset_x - wafer_hole_radius - 0.01
y_min_range = wafer_hole_offset_y - wafer_hole_radius - 0.01
x_max_range = wafer_hole_offset_x + wafer_hole_spacing * (wafer_hole_x_num-1) + wafer_hole_radius + 0.01
y_max_range = wafer_hole_offset_y + wafer_hole_spacing * (wafer_hole_y_num-1) + wafer_hole_radius + 0.01
GFE.draft.get_current().snap_object(x_min_range, x_max_range, y_min_range, y_max_range)
GFE.draft.get_current().select_snaped(False)
GFE.draft.get_current().array_selected(wafer_hole_group_x_num, wafer_hole_group_y_num, wafer_hole_group_spacing_x, wafer_hole_group_spacing_y)

# 填充区域
GFE.draft.get_current().snap_object(-1.0, wafer_length+10, -1.0, wafer_width+10)
GFE.draft.get_current().select_snaped(False)
GFE.draft.get_current().fill_selected()

# 选中面模式，框选所有圆形区域，删除
GFE.draft.get_current().set_snap_object(4)
GFE.draft.get_current().snap_object(0.1, wafer_length-0.1, 0.1, wafer_width-0.1)
GFE.draft.get_current().select_snaped(False)
GFE.draft.get_current().remove_selected()

# 完成草图，生成二维模型
shape = GFE.draft.get_current().export()
if not shape.is_null() :
    mgr = GFE.Pre.geometry.geo_mgr()
    mgr.add('wafer-base', shape)

# 拉伸模型生成三维模型
builder = GFE.geometry.geoprim.builder()
shapes = [GFE.Pre.geometry.geo_mgr().find('wafer-base').shape()]
extruded = builder.extrude(shapes, [0.0, 0.0, wafer_thickness])
mgr = Pre.geometry.geo_mgr()
for sp in extruded :
    if not sp.is_null() :
        mgr.add('wafer', sp)


# ============= 创建筏板模型 ============
# 清空草图
GFE.draft.get_current().clear()

# 绘制矩形
GFE.draft.get_current().set_snap_object(0)
GFE.draft.get_current().set_operate_mode(3)
GFE.draft.get_current().input(0.0, 0.0)
GFE.draft.get_current().input(raft_length, raft_width)
# 填充矩形
GFE.draft.get_current().set_snap_object(2)
GFE.draft.get_current().snap_object(-1, raft_length+10, -1, raft_width+10)
GFE.draft.get_current().select_snaped(False)
GFE.draft.get_current().fill_selected()

# 完成草图，创建二维模型
shape = GFE.draft.get_current().export()
if not shape.is_null() :
    mgr = GFE.Pre.geometry.geo_mgr()
    mgr.add('raft', shape)

# 平移筏板
builder = GFE.geometry.geoprim.builder()
builder.translate(['raft'], [0.0, 0.0, -raft_offset_z], False)

# ========== 创建屋面板模型 ===========
# 在筏板草图基础上，增加梁柱，绘制直线（竖线）
GFE.draft.get_current().set_snap_object(0)
GFE.draft.get_current().set_operate_mode(1)
GFE.draft.get_current().input(roof_lz_spacing_x, 0.0)
GFE.draft.get_current().input(roof_lz_spacing_x, roof_width)

# 阵列直线
GFE.draft.get_current().set_operate_mode(-1)
GFE.draft.get_current().set_snap_object(2)
GFE.draft.get_current().snap_object(roof_lz_spacing_x, 1.0)
GFE.draft.get_current().select_snaped(False)
GFE.draft.get_current().set_operate_mode(14)
GFE.draft.get_current().array_selected(roof_lz_num_x, 1, roof_lz_spacing_x, 0.0)

# 绘制直线（横线）
GFE.draft.get_current().set_snap_object(0)
GFE.draft.get_current().set_operate_mode(1)
GFE.draft.get_current().input(0.0, roof_lz_spacing_y)
GFE.draft.get_current().input(roof_length, roof_lz_spacing_y)

# 阵列直线
GFE.draft.get_current().set_operate_mode(-1)
GFE.draft.get_current().set_snap_object(2)
GFE.draft.get_current().snap_object(1.0, roof_lz_spacing_y)
GFE.draft.get_current().select_snaped(False)
GFE.draft.get_current().set_operate_mode(14)
GFE.draft.get_current().array_selected(1, roof_lz_num_y, 0.0, roof_lz_spacing_y)

# 完成草图，创建屋面板二维模型
shape = GFE.draft.get_current().export()
if not shape.is_null() :
    mgr = GFE.Pre.geometry.geo_mgr()
    mgr.add('roof', shape)

# 平移屋面板
builder = GFE.geometry.geoprim.builder()
builder.translate(['roof'], [0.0, 0.0, roof_offset_z], False)

# ============ 创建框架柱 ===========
# 清空草图
GFE.draft.get_current().clear()

# 设置草图为xz平面
GFE.draft.get_current().set_normal([0.0, 0.0, 0.0], [0.0, -1.0, 0.0], [1.0, 0.0, 0.0])

# 绘制直线
GFE.draft.get_current().set_snap_object(0)
GFE.draft.get_current().set_operate_mode(1)
GFE.draft.get_current().input(0.0, roof_offset_z)
GFE.draft.get_current().input(0.0, -raft_offset_z)

# 完成草图，创建框架柱
shape = GFE.draft.get_current().export()
if not shape.is_null() :
    mgr = GFE.Pre.geometry.geo_mgr()
    mgr.add('column', shape)

# 阵列框架柱
col_names = ["column"]
builder = GFE.geometry.geoprim.builder()
shapes = [GFE.Pre.geometry.geo_mgr().find('column').shape()]
new_shapes = builder.make_array(shapes, x_col_num, y_col_num, 1, [col_spacing_x, col_spacing_y, 0.0])
mgr = Pre.geometry.geo_mgr()
for sp in new_shapes :
    if not sp.is_null() :
        name = mgr.auto_name('column')
        mgr.add(name, sp)
        col_names.append(name)


# =========== 创建集合 =============
# 创建华夫板集合
geo_obj = GFE.Pre.geometry.geo_mgr().find('wafer')
shapes = GFE.geometry.geotool.children(geo_obj.shape(), 2)
gset_basic = GFE.Pre.set.gset_basic('wafer')
gset_basic.set_shapes(shapes)
GFE.Pre.set.gset_mgr().add(gset_basic)

# 筏板集合
geo_obj = GFE.Pre.geometry.geo_mgr().find('raft')
shapes = GFE.geometry.geotool.children(geo_obj.shape(), 4)
gset_basic = GFE.Pre.set.gset_basic('raft')
gset_basic.set_shapes(shapes)
GFE.Pre.set.gset_mgr().add(gset_basic)

# 屋面板集合
geo_obj = GFE.Pre.geometry.geo_mgr().find('roof')
roof_faces = []
# 遍历几何体的所有面
for f in GFE.geometry.geotool.children(geo_obj.shape(), 4):
	roof_faces.append(f)
GFE.Pre.set.gset_mgr().add('roof', roof_faces)

# 框架柱集合
shapes = []
for name in col_names:
    geo_obj = GFE.Pre.geometry.geo_mgr().find(name)
    if geo_obj is None:
        continue
    edges_sp = GFE.geometry.geotool.children(geo_obj.shape(), 6)
    for e in edges_sp:
        shapes.append(e)
gset_basic = GFE.Pre.set.gset_basic('col')
gset_basic.set_shapes(shapes)
GFE.Pre.set.gset_mgr().add(gset_basic)

# 屋面板梁柱集合
geo_obj = GFE.Pre.geometry.geo_mgr().find('roof')
beam_edges = []
# 遍历几何体的所有边
for e in GFE.geometry.geotool.children(geo_obj.shape(), 6):
	beam_edges.append(e)
GFE.Pre.set.gset_mgr().add('beam', beam_edges)


# ================ 创建截面属性 ===============
# 华夫板截面
obj = GFE.Pre.section.property_solid()
obj.name = 'wafer'
obj.elset_name = 'wafer'
obj.mat_name = materials[0][0]
obj.has_thickness = False
obj.thickness = 1.0
GFE.Pre.section.sect_mgr().add(obj)

# 筏板截面
obj = GFE.Pre.section.property_shell()
obj.name = 'raft'
obj.elset_name = 'raft'
obj.mat_name = materials[0][0]
obj.thickness = raft_section_thickness
obj.integral_point = 5
obj.layer_num = 1
obj.params = []
obj.has_rebar = False
obj.Ecc = [0.0, 0.0, 0.0, 0.0]
GFE.Pre.section.sect_mgr().add(obj)

# 屋面板截面
obj = GFE.Pre.section.property_shell()
obj.name = 'roof'
obj.elset_name = 'roof'
obj.mat_name = materials[0][0]
obj.thickness = roof_section_thickness
obj.integral_point = 5
obj.layer_num = 1
obj.params = []
obj.has_rebar = False
obj.Ecc = [0.0, 0.0, 0.0, 0.0]
GFE.Pre.section.sect_mgr().add(obj)

# 框架柱截面
obj = GFE.Pre.section.property_beam()
obj.name = 'col'
obj.elset_name = 'col'
obj.shape = 0
obj.mat_name = materials[0][0]
obj.fiber_num = 1
obj.shape_params = col_section_size
obj.params = []
obj.direction = [1.0, 0.0, 0.0]
obj.shear = [3.75e+06, 3.75e+06]
obj.Ecc = [0.0, 0.0, 0.0, 0.0]
GFE.Pre.section.sect_mgr().add(obj)

# 屋面板梁柱截面
obj = GFE.Pre.section.property_beam()
obj.name = 'beam'
obj.elset_name = 'beam'
obj.shape = 0
obj.mat_name = materials[0][0]
obj.fiber_num = 1
obj.shape_params = roof_lz_section_size
obj.params = []
obj.direction = [0.0, 0.0, 1.0]
obj.shear = [2.5e+06, 2.5e+06]
obj.Ecc = [0.0, 0.0, 0.0, 0.0]
GFE.Pre.section.sect_mgr().add(obj)

# ============= 布尔运算 ==============
# 合并整个模型
merge_names = ["wafer", "raft", "roof"]
merge_names.extend(col_names)
builder = GFE.geometry.geoprim.builder()
builder.merge(merge_names, True,'')


# =========== 网格划分 ==============
# 在网格划分的全局参数中，我们将整体模型的网格尺寸控制在1m。考虑到模型中的华夫板部分计算精度要求较高，
# 需要更加精细的网格尺寸，我们可以使用软件的“线控制”功能，单独控制华夫板部分的网格尺寸在0.5m，
# 华夫板0.5mesh集合
geo_obj = GFE.Pre.geometry.geo_mgr().find('Merge-1')
need_edges = []
need_edges_id = []
for e in GFE.geometry.geotool.children(geo_obj.shape(), 6):
	ez = GFE.geometry.geotool.centre_of_mass(e)[2] # 获取当前面 f 的 z 坐标(质心z值)
	if ez > -0.1 and ez < wafer_thickness + 0.1:
		need_edges.append(e)
		id = GFE.geometry.geotool.get_id_by_shape(e)
		need_edges_id.append(id)
print(f'0.5mesh边的数量：{len(need_edges_id)}')
#print(f'边：{need_edges_id}')
GFE.Pre.set.gset_mgr().add('0.5mesh', need_edges)


# 划分网格
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
'GFE.DefaultSize' : mesh_size,
'GFE.Optimize' : False,
'GFE.Recombine2D' : False,
}
curvesize_1 = mesh_generator.curve_control()
curvesize_1.set_name = '0.5mesh'
# 这里根据0.5mesh集合的id进行转换(need_edges_id)
result_dict = {}
key = need_edges_id[0][0]
result_dict[key] = []
for e in need_edges_id:
    result_dict[key].append(e[-1])
#print(result_dict)
curvesize_1.edges = result_dict
curvesize_1.density = wafer_mesh_size
controller.size_option = [curvesize_1]
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
generator.mesh(['Merge-1'], controller)

# 目前GFE软件在进行网格划分时，平面内部的线条不会划分好梁单元，
# 所以我们需要用“复制网格”功能，创建出屋面板内部的B31屋面梁单元集
from GFE.geometry import geotool
GFE.geometry.geotool.copy_mesh(
    name="beam",
    origin_node=True,
    as_source=True,
    type_name="B31",
    new_set_name="beamb31-1"
)

# 修改截面beam的单元集设置
sect_mgr = GFE.Pre.section.sect_mgr()
obj = sect_mgr.find('beam')
obj.elset_name = 'beamb31-1'
sect_mgr.edit(obj)


# =============== 边界与荷载 ===============
# 底部集合
geo_obj = GFE.Pre.geometry.geo_mgr().find('Merge-1')
minz = 1e10
bottom_face = []
for f in GFE.geometry.geotool.children(geo_obj.shape(), 4):
	fz = GFE.geometry.geotool.centre_of_mass(f)[2]
	if fz < minz:
		minz = fz
		bottom_face = [f]
GFE.Pre.set.gset_mgr().add('base', bottom_face)

# 底部全约束
obj = GFE.Pre.boundary.boundary()
obj.type = 0
obj.name = 'BC-base'
obj.set = 'base'
obj.valid_dof = 0
obj.value = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
obj.amplitude = ''
obj.value_im = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
obj.amplitude_im = ''
obj.distribution = ''
GFE.Pre.boundary.bc_mgr().add(obj)

# 创建华夫板正中央处节点集
obj = GFE.Pre.set.nset()
obj.name = 'Set-cload'
# 1.查找网格获取所有节点数据
findmesh = GFE.Pre.mesh.mesh_mgr().find('Merge-1')
node_data = findmesh.node_data()
# 2.获取华夫板上表面的质心坐标(lx,ly,lz)
geo_obj = GFE.Pre.geometry.geo_mgr().find('wafer')
maxz = -1e10
top_face = None
# 遍历几何体的所有面
for f in GFE.geometry.geotool.children(geo_obj.shape(), 4):
	fz = GFE.geometry.geotool.centre_of_mass(f)[2]
	if fz > maxz:
		maxz = fz
		top_face = f
lx, ly, lz = GFE.geometry.geotool.centre_of_mass(top_face)
print(f'华夫板上表面质心坐标：{lx,ly,lz}')
# 3.查找需要的节点
count = 0
need_nodes = []
for n in node_data[1]:
	nx, ny, nz = n
	if lx-0.1 < nx < lx+0.1 and ly-0.1 < ny < ly+0.1 and lz-0.1 < nz < lz+0.1: # 质心获取存在容差问题
		need_nodes.append(node_data[0][count])
	count += 1
print(f'华夫板中心节点数据：{need_nodes}')
obj.data = need_nodes
obj.unsort = True
GFE.Pre.set.nset_mgr().add(obj)


# 创建荷载
obj = GFE.Pre.boundary.boundary()
obj.type = 5
obj.name = 'BC-cload'
obj.set = 'Set-cload'
obj.valid_dof = 4
obj.value = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
obj.amplitude = ''
obj.value_im = [0.0, 0.0, 1.0, 0.0, 0.0, 0.0]
obj.amplitude_im = ''
obj.distribution = ''
GFE.Pre.boundary.bc_mgr().add(obj)


# ============== 场输出 ===================
obj = GFE.Pre.output.output_request()
obj.name = 'FieldOutput-1'
obj.step = ''
obj.type = 0
obj.method = 0
obj.time_type = 2
obj.time_interval = 0.0
obj.number_interval = 0
obj.frequency = 1
obj.var_option = -1
obj.time_points = ''
obj_sub1 = GFE.Pre.output.node_output()
obj_sub1.name = 'SubOut-1'
obj_sub1.variables = ['U']
obj_sub1.var_option = -1
obj_sub1.reg_type = -1
obj_sub1.nset = ''
obj.sub_output = [obj_sub1]
GFE.Pre.output.field_mgr().add(obj)


# ================ 分析步 ================
# 频响分析步
obj = GFE.Pre.step.steady_dyn_step()
obj.name = 'SSD-1'
obj.description = ''
obj.nlgeom = False
obj.direct = True
obj.interval = 1
obj.scale = 1
obj.data = [[1.0, 50.0, 10.0, 1.0, 1.0, 0.1]]
obj_gd = GFE.Pre.step.global_damping()
obj_gd.alpha = 0.0
obj_gd.beta = 0.0
obj_gd.field = 0
obj_gd.structual = 0.02
obj.global_damping = obj_gd
GFE.Pre.step.step_mgr().add(obj)

# ================ 工况 ==================
# 频响工况
obj = GFE.Pre.case.case()
obj.name = 'ssd'
obj.steps = ['Initial', 'SSD-1']
obj.bcs['Initial'] = ['BC-base']
obj.bcs['SSD-1'] = ['BC-cload']
obj.initialConditions['Initial'] = []
obj.fieldReqs['SSD-1'] = ['FieldOutput-1']
obj.histReqs['SSD-1'] = []
obj.elemAdd['SSD-1'] = []
obj.elemDel['SSD-1'] = []
GFE.Pre.case.case_mgr().add(obj)


# ============== 作业管理器 ================
# 写出inp文件
from GFE.io import inpio
inpwriter = inpio.writer(inp_path)
inpwriter.set_case('ssd')
inpwriter.perform()

```
