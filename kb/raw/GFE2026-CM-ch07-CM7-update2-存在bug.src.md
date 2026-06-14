# GFE2026-CM-ch07-CM7-update2-存在bug
> 来源：E:\GFE2026\典型案例与教程\第7章 锚杆隧道施工模拟案例\CM7-update2-存在bug.py（GFE2026 官方典型案例命令流，v3.x 代际金标准）。raw 不可变源副本，2026-06-11 入库。

```python
import GFE
from GFE import *
from GFE.Pre import *
from GFE.occ import *
GFE.Pre.document.set_application_by_ui()

import math

# 存在每次打开gfe，数据不一致的情况
def Bug_Check():
    # 问题描述：重新打开GFE导入代码，获取的Soil子几何体实体参数不同，有两种情况结果
    # 1.正常情况：每个列表第一个元素都是1，即父几何是Soil
    # 2.bug情况：后面有些列表存在第一个元素都是3，即父几何是Tunnel-Boundary
    soil_obj = GFE.Pre.geometry.geo_mgr().find('Soil-1')
    shapes = GFE.geometry.geotool.children(soil_obj.shape(), 2)
    id = []
    for sp in shapes:
        id.append(GFE.geometry.geotool.get_id_by_shape(sp))
    print(f'存在bug分割隧道后土体id：{id}')

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
plugin_dir2 = os.path.join(plugin_dir, "第7章")
gmat_path = os.path.join(plugin_dir2, "cm7.gmat")
inp_path = os.path.join(plugin_dir2, "CM7-Case-suidaokaiwa.inp")
# 转为绝对路径
gmat_path = os.path.abspath(gmat_path)
inp_path = os.path.abspath(inp_path)

# ============= 参数定义 ================
# 材料路径
materials_path = gmat_path

# 土体参数
soil_depth = [5.0, 13.0, 42.0]		# 土层厚度
soil_material_path = gmat_path      # 材料路径
# 这个材料需通过gmat文件导入
soil_materials = ['fenghuatu', 'fenghuayan', 'ruanyan'] # 这个数量需跟土层厚度数量一致
soil_length = 90			# 土体长度
soil_width = 20			    # 土体宽度

# 隧道参数
tunnel_top_arc_radius = 5.5			# 3心圆-顶部圆弧-半径
tunnel_top_arc_angle = 90			# 3心圆-顶部圆弧-弧度
tunnel_both_sides_arc_radius = 9	# 3心圆-两边圆弧-半径
tunnel_both_sides_arc_angle = 25	# 3心圆-两边圆弧-弧度

maogan_num = 13			    # 锚杆数量
maogan_length = 4			# 锚杆长度
maogan_arc_length = 1.8		# 锚杆弧长
maogan_out_offset = 0.2		# 锚杆向外偏移量

tunnel_length = 20			    # 隧道长度【土体宽度】
tunnel_layer_spacing = 2		# 隧道每段间隔
maogan_embed_offset = 0.2       # 锚杆嵌入土体偏移量【小于隧道每段间隔】

tunnel_layer_num = int(tunnel_length / tunnel_layer_spacing)     # 隧道段数（锚杆段数）

# 网格
soil_mesh_size = 1.5			# 土体网格尺寸
# 隧道土-网格线控制-节点数（注意！！！当【土层线】和【隧道】交叉时，这里就会出问题）
soil_mesh_control_line_num = 3			# 隧道长直线
soil_mesh_control_both_arc_num = 5		# 两边圆弧
soil_mesh_control_bottom_num = 10		# 底部直线
soil_mesh_control_top_arc_num = 18		# 顶部圆弧
maogan_mesh_size = 1.0		# 锚杆网格尺寸

# 截面属性
maogan_section_radius = 0.0125			    # 锚杆截面圆柱半径
tunnel_section_shell_thickness = 0.15		# 隧道壳厚度


# ================ 计算三心圆隧道形心到顶面、底面的垂直距离 ==============
def calc_centroid_to_top_bottom(R, r, alpha_deg, beta_deg):
    """
    计算三心圆隧道截面形心到顶面、底面的垂直距离（工程规范版）
    参数说明：
        R: 顶部大圆弧半径（如5.5）
        r: 侧面小圆弧半径（如9）
        alpha_deg: 大圆弧半圆心角（角度制，如90）
        beta_deg: 小圆弧半圆心角（角度制，如25）
    返回值：
        (d_top, d_bottom): 形心到顶面、底面的距离（保留4位小数）
    """
    # 合法性校验
    if R <= 0 or r <= 0 or alpha_deg <= 0 or beta_deg <= 0:
        raise ValueError("半径和角度必须为正数")

    # 步骤1：角度转弧度
    alpha = math.radians(alpha_deg)
    beta = math.radians(beta_deg)

    # 步骤2：计算小圆弧圆心坐标（O2，z轴向上，O1为原点）
    delta = R - r  # 大/小圆心间距
    O2_x = -delta * math.sin(alpha)
    O2_z = delta * math.cos(alpha)

    # 步骤3：计算闭合三心圆截面的面积（核心修正：扇区→闭合面积）
    # 顶部大圆弧段面积
    S1 = R ** 2 * alpha - 0.5 * R ** 2 * math.sin(2 * alpha)
    # 单侧小圆弧段面积
    S2 = r ** 2 * beta - 0.5 * r ** 2 * math.sin(2 * beta) - delta * r * math.sin(alpha + beta)
    S_total = S1 + 2 * S2

    # 步骤4：计算各段形心z坐标
    # 顶部段形心z
    denominator1 = 3 * (2 * alpha - math.sin(2 * alpha))
    z1 = (4 * R * math.sin(alpha) ** 3) / denominator1 if denominator1 != 0 else R
    # 单侧小圆弧段形心z
    denominator2 = 3 * (2 * beta - math.sin(2 * beta))
    z2 = O2_z - (4 * r * math.sin(beta) ** 3) / denominator2 if denominator2 != 0 else O2_z

    # 步骤5：整体形心相对大圆心的z坐标
    cz_rel = (S1 * z1 + 2 * S2 * z2) / S_total if S_total != 0 else 0

    # 步骤6：顶/底面相对大圆心的z坐标（工程准确版）
    z_top = R  # 顶面（大圆弧顶点）
    z_bottom = O2_z - r * math.sin(alpha + beta)  # 底面（小圆弧最低点）

    # 步骤7：计算形心到顶/底面的距离
    d_top = abs(z_top - cz_rel)
    d_bottom = abs(cz_rel - z_bottom)

    return round(d_top, 4), round(d_bottom, 4)


# ============= 创建材料 ===============
# 导入材料
import GFE.io
io_instance = GFE.io.get_current()
result = io_instance.import_mat(soil_material_path)

# =========== 创建一维土层 ============
obj = GFE.Pre.soil.soil()
obj.name = 'Soil1D-1'
obj.depth = soil_depth
obj.materials = soil_materials
obj.bedrock_mat = soil_materials[-1]
obj.depth_dir = 2
GFE.Pre.soil.soil_mgr().add(obj)

# =========== 创建三维土体 ============
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


# ============= 创建隧道 =================
# 隧道设计可通过“工程-隧道设计器”功能进行设计
[a,b,c] = GFE.geometry.geotool.build_tunnel_shape(1, [tunnel_top_arc_radius, tunnel_both_sides_arc_radius],
                                                  [tunnel_top_arc_angle, tunnel_both_sides_arc_angle],
                                                  False,0,0,True,True,
                                                  [maogan_num,  maogan_length, maogan_arc_length, maogan_out_offset],
                                                  True, tunnel_length,[tunnel_layer_spacing],[tunnel_layer_spacing],0,False,None)
mgr = Pre.geometry.geo_mgr()
mgr.add('Tunnel', a)            # 隧道
mgr.add('Tunnel-Boundary', b)   # 隧道土
mgr.add('Tunnel-Rockbelt', c)   # 锚杆


# ============= 创建锚杆的各部分集合 =============
# 1.初始化空列表
edges_list = [[] for _ in range(tunnel_layer_num)]
geo_obj = GFE.Pre.geometry.geo_mgr().find('Tunnel-Rockbelt')
# 2.查找并添加边
for e in GFE.geometry.geotool.children(geo_obj.shape(), 6):
	ey = GFE.geometry.geotool.centre_of_mass(e)[1]
	index = round(ey) // tunnel_layer_spacing	# 计算索引
	edges_list[index].append(e)
# 3.把edges_list添加到管理器
for index, shapes in enumerate(edges_list, 1):
	GFE.Pre.set.gset_mgr().add(f'Tunnel-rockseg-{index}', shapes)


# ============ 平移隧道 =============
# 计算隧道和土体形心
tunnel_obj = GFE.Pre.geometry.geo_mgr().find('Tunnel-Boundary')
tunnel_center = GFE.geometry.geotool.centre_of_mass(tunnel_obj.shape())
soil_obj = GFE.Pre.geometry.geo_mgr().find('Soil-1')
soil_center = GFE.geometry.geotool.centre_of_mass(soil_obj.shape())
# 平移隧道
trsf_vec = [soil_center[i] - tunnel_center[i] for i in range(3)]
builder = GFE.geometry.geoprim.builder()
builder.translate(['Tunnel', 'Tunnel-Boundary', 'Tunnel-Rockbelt'], trsf_vec, False)

# 平移锚杆，使其嵌入土体
builder = GFE.geometry.geoprim.builder()
builder.translate(['Tunnel-Rockbelt'], [0.0, maogan_embed_offset, 0.0], False)

""" ----------------- 测bug ------------------ """
print("----------------- 测bug ------------------")
Bug_Check()
print("----------------- 测bug ------------------")
""" ----------------- 测bug ------------------ """
# 分割土体
builder = GFE.geometry.geoprim.builder()
builder.split('Soil-1', ['Tunnel-Boundary'], True)


""" ----------------- 测bug ------------------ """
print("----------------- 测bug ------------------")
Bug_Check()
print("----------------- 测bug ------------------")
""" ----------------- 测bug ------------------ """



# ============== 创建土-隧道集合 ===============
# ----------- 获取参数 ------------
# 获取隧道的质心坐标
obj_suidao = GFE.Pre.geometry.geo_mgr().find('Tunnel-Boundary')
lx,ly,lz =  GFE.geometry.geotool.centre_of_mass(obj_suidao.shape())
print(f'土体内-隧道形心坐标x:{lx}, y:{ly}, z:{lz}')

# 计算三心圆隧道形心到顶面、底面的垂直距离
d_top, d_bottom = calc_centroid_to_top_bottom(tunnel_top_arc_radius, tunnel_both_sides_arc_radius, tunnel_top_arc_angle, tunnel_both_sides_arc_angle)
print(f"土体内-隧道形心到顶面距离：{d_top}, 到底面距离：{d_bottom}")

# 土体内-隧道范围
left_pos = lx - tunnel_top_arc_radius
right_pos = lx + tunnel_top_arc_radius
bottom_pos = lz - d_bottom
top_pos = lz + d_top
print(f"土体内-隧道范围坐标：左{left_pos}，右{right_pos}，底{bottom_pos}，顶{top_pos}")


# ----------------- 隧道土集合 ----------------
# 1. 查找隧道土实体
solid_list = {}
obj_tuti = GFE.Pre.geometry.geo_mgr().find('Soil-1')
for s in GFE.geometry.geotool.children(obj_tuti.shape(), 2):
    sx, sy, sz = GFE.geometry.geotool.centre_of_mass(s)
    # 该实体是隧道土之一
    if left_pos-0.1 < sx < right_pos+0.1 and bottom_pos-0.1 < sz < top_pos+0.1:
        index = (round(sy) + 1) // tunnel_layer_spacing
        solid_list[index] = s

# 2.创建集合（按顺序）
for index in sorted(solid_list.keys()):
    shape = solid_list[index]
    GFE.Pre.set.gset_mgr().add(f'suidaotu-{index}', [shape])


# -------------- 隧道壳集合 --------------
"""这个创建方法需要优化:
- （1）当 土体的面y负方向最值y坐标不是0时，会出问题
- （2）排除[土层线]和[隧道]交叉产生的面，这个比较困难，未实现，先锁定x值在中心的面，然后判断z值，但是->
- ->因为顶部曲面的质心z值是小于隧道顶面z值的，也就是说不能通过判定当前面质心z值 == 顶面z值而筛选
"""
# 1.查找隧道壳相关面
# 初始化n个空列表faces
faces_list = [[] for _ in range(tunnel_layer_num)]
obj_tuti = GFE.Pre.geometry.geo_mgr().find('Soil-1')
for f in GFE.geometry.geotool.children(obj_tuti.shape(), 4):
	fx,fy,fz = GFE.geometry.geotool.centre_of_mass(f)
    # 判定是隧道土内的面
	if left_pos-0.1 < fx < right_pos+0.1 and bottom_pos-0.1 < fz < top_pos+0.1:
		# 判定是隧道侧面，而不是隧道正面
		if abs((round(fy) % tunnel_layer_spacing) - (tunnel_layer_spacing/2)) < 1e-9:
			# 获取对应索引
			index = (round(fy) // tunnel_layer_spacing) + 1
			faces_list[index - 1].append(f)
            
# 2.将faces列表对应集合添加到管理器
for index, shapes in enumerate(faces_list, 1):
	GFE.Pre.set.gset_mgr().add(f'suidaoqiao-{index}', shapes)


# =============== 网格划分 ==============
# 线控制集合
# 1.获取隧道的质心坐标，已在上面获取lx,ly,lz
# 2.查找并分配隧道各边
need_edges_sp_1, need_edges_sp_2, need_edges_sp_3, need_edges_sp_4 = [],[],[],[]
need_edges_id_1, need_edges_id_2, need_edges_id_3, need_edges_id_4 = [],[],[],[]
obj_tuti = GFE.Pre.geometry.geo_mgr().find('Soil-1')
for e in GFE.geometry.geotool.children(obj_tuti.shape(), 6):
	ex,ey,ez = GFE.geometry.geotool.centre_of_mass(e)
	if left_pos-0.1 < ex < right_pos+0.1 and bottom_pos-0.1 < ez < top_pos+0.1:	 # 当前边是隧道土之一
		if abs((round(ey) % tunnel_layer_spacing) - (tunnel_layer_spacing/2)) < 1e-9:	# 如果ey为奇数就是-隧道长直线的边
			need_edges_sp_1.append(e)
			need_edges_id_1.append(GFE.geometry.geotool.get_id_by_shape(e))
		else:
			if ez > lz:							# 顶部圆弧的边
				need_edges_sp_4.append(e)
				need_edges_id_4.append(GFE.geometry.geotool.get_id_by_shape(e))
			elif ez<lz and lx-0.1< ex <lx+0.1:	# 底部直线的边
				need_edges_sp_3.append(e)
				need_edges_id_3.append(GFE.geometry.geotool.get_id_by_shape(e))
			else:								# 两边圆弧的边
				need_edges_sp_2.append(e)
				need_edges_id_2.append(GFE.geometry.geotool.get_id_by_shape(e))
GFE.Pre.set.gset_mgr().add('Set-mesh_control_line', need_edges_sp_1)
GFE.Pre.set.gset_mgr().add('Set-mesh_control_both_arc', need_edges_sp_2)
GFE.Pre.set.gset_mgr().add('Set-mesh_control_bottom', need_edges_sp_3)
GFE.Pre.set.gset_mgr().add('Set-mesh_control_top_arc', need_edges_sp_4)


# ---------- 土体网格划分 -----------
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
curvesize_1 = mesh_generator.curve_control()
curvesize_1.set_name = 'Set-mesh_control_line'
# 基于need_edges_id配置线控制
# 核心逻辑：取几何体id为键，need_edges_id每个列表的最后一个元素e[-1]为值
result_dict = {}
key = need_edges_id_1[0][0]	#几何id作为键
result_dict[key] = []
for e in need_edges_id_1:
    result_dict[key].append(e[-1])	#添加值
# print(f'线控制-侧边直线：{result_dict}')
curvesize_1.edges = result_dict
curvesize_1.count = 3

curvesize_2 = mesh_generator.curve_control()
curvesize_2.set_name = 'Set-mesh_control_both_arc'
# 基于need_edges_id配置线控制
result_dict = {}
key = need_edges_id_2[0][0]
result_dict[key] = []
for e in need_edges_id_2:
    result_dict[key].append(e[-1])
# print(f'线控制-两边圆弧：{result_dict}')
curvesize_2.edges = result_dict
curvesize_2.count = 5

curvesize_3 = mesh_generator.curve_control()
curvesize_3.set_name = 'Set-mesh_control_bottom'
# 基于need_edges_id配置线控制
result_dict = {}
key = need_edges_id_3[0][0]
result_dict[key] = []
for e in need_edges_id_3:
    result_dict[key].append(e[-1])
# print(f'线控制-底面直线：{result_dict}')
curvesize_3.edges = result_dict
curvesize_3.count = 10

curvesize_4 = mesh_generator.curve_control()
curvesize_4.set_name = 'Set-mesh_control_top_arc'
# 基于need_edges_id配置线控制
result_dict = {}
key = need_edges_id_4[0][0]
result_dict[key] = []
for e in need_edges_id_4:
    result_dict[key].append(e[-1])
# print(f'线控制-顶部圆弧：{result_dict}')
curvesize_4.edges = result_dict
curvesize_4.count = 18

controller.size_option = [curvesize_1, curvesize_2, curvesize_3, curvesize_4]
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


# ----------- 锚杆网格划分 ----------
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
'GFE.DefaultSize' : maogan_mesh_size,
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
generator.mesh(['Tunnel-Rockbelt'], controller)


# 网格复制-隧道壳
for i in range(1,tunnel_layer_num+1):
	GFE.geometry.geotool.copy_mesh(
		name = f'suidaoqiao-{i}',
		origin_node = True,
		as_source = True,
		type_name = 'S3',
		new_set_name = f'CpMsh-{i}'
	)


# ======== 隧道壳（衬砌）整体单元集合并 ==========
need_data = []
for i in range(1,tunnel_layer_num+1):
	findelset = GFE.Pre.set.elset_mgr().find(f'CpMsh-{i}')
	need_data += findelset.data
obj = GFE.Pre.set.elset()
obj.name = 'Set-CpMsh'
obj.data = need_data
obj.unsort = False
GFE.Pre.set.elset_mgr().add(obj)

# ============ 锚杆几何集创建 ==============
geo_obj = GFE.Pre.geometry.geo_mgr().find('Tunnel-Rockbelt')
shapes = GFE.geometry.geotool.children(geo_obj.shape(), 6)
gset_basic = GFE.Pre.set.gset_basic('Set-maogan')
gset_basic.set_shapes(shapes)
GFE.Pre.set.gset_mgr().add(gset_basic)

# =============== 截面属性 ===========
# 锚杆
prop = GFE.Pre.section.property_beam()
prop.name = 'Propery-maogan'
prop.elset_name = 'Set-maogan'
prop.shape = 3
prop.mat_name = 'maogan'
prop.fiber_num = 1
prop.shape_params = [maogan_section_radius]
prop.params = []
prop.direction = [0.0, 1.0, 0.0]
prop.shear = [35682.8, 35682.8]
prop.Ecc = [0.0, 0.0, 0.0, 0.0]
GFE.Pre.section.sect_mgr().add(prop)

# 衬砌（隧道壳）
prop = GFE.Pre.section.property_shell()
prop.name = 'Propery-CpMsh'
prop.elset_name = 'Set-CpMsh'
prop.mat_name = 'penhun'
prop.thickness = tunnel_section_shell_thickness
prop.integral_point = 5
prop.layer_num = 1
prop.params = []
prop.has_rebar = False
prop.rebar = GFE.Pre.section.rebar_layer()
prop.Ecc = [0.0, 0.0, 0.0, 0.0]
GFE.Pre.section.sect_mgr().add(prop)

# ============== 相互作用 ==============
# 创建整个土体集合
geo_obj = GFE.Pre.geometry.geo_mgr().find('Soil-1')
shapes = GFE.geometry.geotool.children(geo_obj.shape(), 2)
gset_basic = GFE.Pre.set.gset_basic('Set-tuti')
gset_basic.set_shapes(shapes)
GFE.Pre.set.gset_mgr().add(gset_basic)

# 创建嵌入区域
embed = GFE.Pre.interaction.embed()
embed.id = 0
embed.name = 'Embed-1'
embed.host_name = 'Set-tuti'
embed.roundoff_tolerance = 1e-06
embed.exterior_tolerance = 0.05
embed.embedded_names = ['Set-maogan']
GFE.Pre.interaction.embed_mgr().add(embed)

# ================ 边界与荷载 ==================
# 创建土体底面及侧面x和y方向集合
geo_obj = GFE.Pre.geometry.geo_mgr().find('Soil-1')
minx = miny = minz = 1e10
maxx = maxy =-1e10
bottom_face = []
left_faces, right_faces = [],[]
front_faces, back_faces = [],[]
for f in GFE.geometry.geotool.children(geo_obj.shape(), 4):
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
GFE.Pre.set.gset_mgr().add('bc-base', bottom_face)
GFE.Pre.set.gset_mgr().add('bc-x', x_faces)
GFE.Pre.set.gset_mgr().add('bc-y', y_faces)

# 创建约束
obj = GFE.Pre.boundary.boundary()
obj.type = 0
obj.name = 'BC-base'
obj.set = 'bc-base'
obj.valid_dof = 0
obj.value = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
obj.amplitude = ''
obj.value_im = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
obj.amplitude_im = ''
obj.distribution = ''
obj.track_id = []
obj.track_coord = []
obj.has_if = False
obj.if_mode = 0
obj.if_acce_path = ''
obj.if_acce = []
obj.if_param = []
obj.if_itv = 0.0
obj.if_tot = 0.0
obj.if_grade = 0
obj.if_force = []
GFE.Pre.boundary.bc_mgr().add(obj)

obj = GFE.Pre.boundary.boundary()
obj.type = 1
obj.name = 'BC-X'
obj.set = 'bc-x'
obj.valid_dof = 1
obj.value = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
obj.amplitude = ''
obj.value_im = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
obj.amplitude_im = ''
obj.distribution = ''
obj.track_id = []
obj.track_coord = []
obj.has_if = False
obj.if_mode = 0
obj.if_acce_path = ''
obj.if_acce = []
obj.if_param = []
obj.if_itv = 0.0
obj.if_tot = 0.0
obj.if_grade = 0
obj.if_force = []
GFE.Pre.boundary.bc_mgr().add(obj)

obj = GFE.Pre.boundary.boundary()
obj.type = 1
obj.name = 'BC-Y'
obj.set = 'bc-y'
obj.valid_dof = 2
obj.value = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
obj.amplitude = ''
obj.value_im = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
obj.amplitude_im = ''
obj.distribution = ''
obj.track_id = []
obj.track_coord = []
obj.has_if = False
obj.if_mode = 0
obj.if_acce_path = ''
obj.if_acce = []
obj.if_param = []
obj.if_itv = 0.0
obj.if_tot = 0.0
obj.if_grade = 0
obj.if_force = []
GFE.Pre.boundary.bc_mgr().add(obj)

# 惯性力
obj = GFE.Pre.boundary.boundary()
obj.type = 7
obj.name = 'G-whole'
obj.set = ''
obj.valid_dof = 0
obj.value = [0.0, 0.0, -9.8]
obj.amplitude = ''
obj.value_im = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
obj.amplitude_im = ''
obj.distribution = ''
obj.track_id = []
obj.track_coord = []
obj.has_if = False
obj.if_mode = 0
obj.if_acce_path = ''
obj.if_acce = []
obj.if_param = []
obj.if_itv = 0.0
obj.if_tot = 0.0
obj.if_grade = 0
obj.if_force = []
GFE.Pre.boundary.bc_mgr().add(obj)


# ============= 分析步 ===========
obj = GFE.Pre.step.static_general_step()
obj.name = 'Static-1'
obj.description = ''
obj.nlgeom = False
obj.init_inc = 1.0
obj.period = 1.0
obj.min_inc = 1e-05
obj.max_inc = 1.0
GFE.Pre.step.step_mgr().add(obj)

# ============ 场输出 =============
obj = GFE.Pre.output.output_request()
obj.name = 'FieldOutput-1'
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
obj_sub1.variables = ['U', 'UR']
obj_sub1.var_option = -1
obj_sub1.reg_type = -1
obj_sub1.nset = ''
obj_sub2 = GFE.Pre.output.element_output()
obj_sub2.name = 'SubOut-2'
obj_sub2.variables = ['E', 'PE', 'S']
obj_sub2.var_option = -1
obj_sub2.reg_type = -1
obj_sub2.elset = ''
obj.sub_output = [obj_sub1, obj_sub2]
GFE.Pre.output.field_mgr().add(obj)

# ============= 工况 ============
# 直接优化为施工助手操作后的工况（只写最后一次编辑完成的工况）
steps = ['Initial', 'Static-1']
# 施工助手-创建分析步
for i in range(1,tunnel_layer_num+2):
    obj = GFE.Pre.step.static_general_step()
    obj.name = f'Stage-{i}'
    obj.description = ''
    obj.nlgeom = True
    obj.init_inc = 1.0
    obj.period = 1.0
    obj.min_inc = 1e-05
    obj.max_inc = 1.0
    GFE.Pre.step.step_mgr().add(obj)
    # 添加分析步名称
    steps.append(obj.name)


# 创建工况
case_obj = GFE.Pre.case.case()
case_obj.name = 'suidaokaiwa'
case_obj.steps = steps
case_obj.bcs['Initial'] = ['BC-base', 'BC-X', 'BC-Y']
case_obj.bcs['Static-1'] = ['G-whole']
case_obj.initialConditions['Initial'] = []
case_obj.fieldReqs['Static-1'] = ['FieldOutput-1']
case_obj.histReqs['Static-1'] = []

for i in range(1, tunnel_layer_num + 2):  # i从1到11（tunnel_layer_num=10）
    stage_name = f'Stage-{i}'
    if i == 1:
        # Stage-1 只有Tunnel-rockseg
        case_obj.elemAdd[stage_name] = [f'Tunnel-rockseg-{i}']
    elif 2 <= i <= tunnel_layer_num:
        # Stage-2 到 Stage-n-1
        tunnel_name = f'Tunnel-rockseg-{i}'
        cpmsh_name = f'CpMsh-{i-1}'
        case_obj.elemAdd[stage_name] = [tunnel_name, cpmsh_name]
    elif i == tunnel_layer_num + 1:
        # Stage-n 只有CpMsh
        case_obj.elemAdd[stage_name] = [f'CpMsh-{i-1}']

# 1. Stage-1到Stage-n：每个Stage删除对应的suidaotu-i
for i in range(1, tunnel_layer_num + 1):
    stage_name = f'Stage-{i}'
    case_obj.elemDel[stage_name] = [f'suidaotu-{i}']

# 2. Static-1：删除所有CpMsh和Tunnel-rockseg
cpmsh_del_list = [f'CpMsh-{i}' for i in range(1, tunnel_layer_num + 1)]
tunnel_del_list = [f'Tunnel-rockseg-{i}' for i in range(1, tunnel_layer_num + 1)]
case_obj.elemDel['Static-1'] = cpmsh_del_list + tunnel_del_list

GFE.Pre.case.case_mgr().add(case_obj)

# ============= 作业管理器 =============
# 写出inp文件
from GFE.io import inpio
inpwriter = inpio.writer(inp_path)
inpwriter.set_case('suidaokaiwa')
inpwriter.perform()
```
