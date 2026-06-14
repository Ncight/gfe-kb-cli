# GFE2026-CM-ch05-CM5-update2
> 来源：E:\GFE2026\典型案例与教程\第5章 非均匀场地建模案例\CM5-update2.py（GFE2026 官方典型案例命令流，v3.x 代际金标准）。raw 不可变源副本，2026-06-11 入库。

```python
import GFE
from GFE import *
from GFE.Pre import *
from GFE.occ import *

from GFE.geometry import geotool
import math

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
plugin_dir2 = os.path.join(plugin_dir, "第5章")
gmat_path = os.path.join(plugin_dir2, "nol-soil.gmat")
borehole_data_path = os.path.join(plugin_dir2, "SoilSamples.txt")
inp_path_static = os.path.join(plugin_dir2, "CM5-Case-Static.inp")
inp_path_model = os.path.join(plugin_dir2, "CM5-Case-Model.inp")
inp_path_dyna = os.path.join(plugin_dir2, "CM5-Case-Dyna.inp")
# 转为绝对路径
gmat_path = os.path.abspath(gmat_path)
borehole_data_path = os.path.abspath(borehole_data_path)
inp_path_static = os.path.abspath(inp_path_static)
inp_path_model = os.path.abspath(inp_path_model)
inp_path_dyna = os.path.abspath(inp_path_dyna)

# ============== 参数定义 ==============
# 1. 工厂模型
plant_core_radius = 25.0		# 工厂核心半径
plant_down_num = 5			    # 工厂下层数量
plant_up_num = 3			    # 工厂上层数量
plant_down_height = 8.0		    # 工厂下层高度
plant_up_height = 6.0		    # 工厂上层高度

plant_down_out_wall_points = [       # 工厂1-5层外围墙体---多折线
    (-50, 50), (50, 50), (50, 37), (65, 37), (65, 0), (65, -20),
    (38, -20), (38, -65), (0, -65), (-30, -65), (-30, 0), (-50, 0),
    (-50, 50)
]

plant_down_in_wall_points = [        # 工厂1-5层内部墙体---直线
    (-30,0), (-25,0),  (25,0),  (65,0),  (0,25),  (0,37),  (0,37),  (0,50),
    (0,-25), (0,-65),  (-30,0), (-30,50),(50,37), (0,37),   (0,37),  (-50,37),
    (50,37), (50,0),   (50,0),  (50,-20),(38,-20), (38,0),   (38,0),  (38,37),
    (38,37), (38,50),  (-30,-50),(0,-50),(0,-50),  (38,-50), (-30,-30),(0,-30),
    (0,-30), (38,-30), (30,-65), (30,0), (30,0),   (30,37),  (30,37), (30,50)
]

plant_up_out_wall_points_1 = [      # 工厂6-8层 1外墙体---直线
    (0, 25), (0, 37), (0, 37), (30, 37),
    (30, 37), (38, 37), (38, 37), (50, 37),
    (50, 37), (65, 37), (65, 37), (65, 0),
    (65, 0), (50, 0), (50, 0), (38, 0),
    (38, 0), (30, 0), (30, 0), (25, 0)
]

plant_up_in_wall_points_1 = [       # 工厂6-8层 1内墙体---直线
    (30, 37), (30, 0), (38, 37), (38, 0),
    (50, 37), (50, 0)
]

plant_up_out_wall_points_2 = [      # 工厂6-8层 2外墙体---直线
    (-25, 0), (-30, 0), (-30, 0), (-30, -30),
    (-30, -30), (-30, -50), (-30, -50), (-30, -65),
    (-30, -65), (0, -65), (0, -65), (0, -50),
    (0, -50), (0, -30), (0, -30), (0, -25)
]

plant_up_in_wall_points_2 = [       # 工厂6-8层 2内墙体---直线
    (-30, -30), (0, -30), (-30, -50), (0, -50)
]

plant_up_wall_arc_points=[      # 工厂6-8层墙体补充---圆弧
    (0, 0), (25, 0), (0, 25),   # 厂房1
    (0, 0), (-25, 0), (0, -25)  # 厂房2
]

# 2. 材料（名称，密度，弹性模量，泊松比，阻尼α，阻尼β）
materials = [
    ('C40_PLANT', 2.6, 3.25e+07, 0.2, 0.948805, 0.0),
    ('C60_PLANT', 2.6, 3.6e+07, 0.2, 0.948805, 0.0)
]

# 3. 截面属性
wall_thickness = 2			# 墙体厚度
slab_thickness = 1.8		# 楼板厚度
raft_thickness = 3.5		# 底板厚度

# 4. 网格
plant_mesh = 1.0			# 厂房网格尺寸

# 5. 保护壳模型
shell_points_1 = [(0, 0), (24, 0), (24, 55)]		# 保护壳---多折线绘制
shell_points_2 = [(24, 55), (18, 70), (0, 78)]		# 保护壳---圆弧绘制
shell_thickness = 1.5		# 保护壳厚度
shell_mesh = 1.0			# 保护壳网格尺寸

# 6. 土体参数
file_path = borehole_data_path		# 钻孔数据
# 土体材料（需通过gmat文件导入）
soil_materials_path = gmat_path
soil_materials = ['qiangfenghuahuagangyan', 'quanfenghuahuagangyan', 'lizhinianxingtu', 'sutiantu']
plant_basement_depth = 16.0		# 工厂地下室深度
soil_mesh = 6.0
soil_depth = [7.0, 11.0, 8.0, 36.0]		# 土层厚度--用于地震波

# 7. 分析步
step_total_time = 20.0			# 显式动力分析步总时长
step_target_time = 3e-05		# 分析步目标时间增量


# =========== 绘制厂房通用墙体（1-5层）=============
# 设置xy平面
GFE.draft.get_current().set_normal([0.0, 0.0, 0.0], [0.0, 0.0, 1.0], [1.0, 0.0, 0.0])
# 绘制核心-圆形
GFE.draft.get_current().set_snap_object(0)
GFE.draft.get_current().set_operate_mode(7)
GFE.draft.get_current().input(0.0, 0.0)
GFE.draft.get_current().input(plant_core_radius, 0.0)

# 绘制厂房外围墙体-多折线
GFE.draft.get_current().set_snap_object(0)
GFE.draft.get_current().set_operate_mode(2)
for point in plant_down_out_wall_points:
    GFE.draft.get_current().input(point[0], point[1])


# 绘制厂房内部墙体-直线
GFE.draft.get_current().set_snap_object(0)
GFE.draft.get_current().set_operate_mode(1)
# 核心遍历逻辑：步长为2，两两取点，绘制直线
for i in range(0, len(plant_down_in_wall_points), 2):
    # 取出一组的两个点
    point1 = plant_down_in_wall_points[i]
    point2 = plant_down_in_wall_points[i+1]
    GFE.draft.get_current().input(point1[0], point1[1])
    GFE.draft.get_current().input(point2[0], point2[1])
    print(f"绘制厂房下层内部直线: {point1} → {point2}")

# 完成草图，创建二维模型
shape = GFE.draft.get_current().export()
if not shape.is_null() :
    mgr = GFE.Pre.geometry.geo_mgr()
    mgr.add('plant-down-wall-base', shape)

# ========== 创建厂房底板 =============
# 计算两点的中点
def calc_mid_point(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return ( (x1 + x2)/2, (y1 + y2)/2 )  # 求两点中点
last_point = None   # 上一个点

# 多选外围墙体
GFE.draft.get_current().set_snap_object(2)
for point in plant_down_out_wall_points:
    if last_point is not None:
        mid_point = calc_mid_point(last_point, point)
        GFE.draft.get_current().snap_object(mid_point[0], mid_point[1])
        GFE.draft.get_current().select_snaped(True)
    last_point = point
# 填充后，完成草图，创建底板（1层）二维模型
GFE.draft.get_current().fill_selected()
shape = GFE.draft.get_current().export()
if not shape.is_null() :
    mgr = GFE.Pre.geometry.geo_mgr()
    mgr.add('raft', shape)

# ============ 创建厂房6-8层通用墙体 ============
#！！！！！！！！！这里进行了优化，跟案例手册操作不一样！！！！！！！！！！！
# 手册里是选面和线删除。---------优化为--------直接清空草图，然后重新创建线条
# 清空草图
GFE.draft.get_current().clear()

# 绘制墙线---直线
GFE.draft.get_current().set_snap_object(0)
GFE.draft.get_current().set_operate_mode(1)
# 厂房1外墙体
for i in range(0, len(plant_up_out_wall_points_1), 2):
    # 取出一组的两个点
    point1 = plant_up_out_wall_points_1[i]
    point2 = plant_up_out_wall_points_1[i+1]
    GFE.draft.get_current().input(point1[0], point1[1])
    GFE.draft.get_current().input(point2[0], point2[1])
    print(f"绘制厂房上层1外部直线: {point1} → {point2}")
# 厂房1内墙体
for i in range(0, len(plant_up_in_wall_points_1), 2):
    # 取出一组的两个点
    point1 = plant_up_in_wall_points_1[i]
    point2 = plant_up_in_wall_points_1[i+1]
    GFE.draft.get_current().input(point1[0], point1[1])
    GFE.draft.get_current().input(point2[0], point2[1])
    print(f"绘制厂房上层1内部直线: {point1} → {point2}")
# 厂房2外墙体
for i in range(0, len(plant_up_out_wall_points_2), 2):
    # 取出一组的两个点
    point1 = plant_up_out_wall_points_2[i]
    point2 = plant_up_out_wall_points_2[i+1]
    GFE.draft.get_current().input(point1[0], point1[1])
    GFE.draft.get_current().input(point2[0], point2[1])
    print(f"绘制厂房上层2外部直线: {point1} → {point2}")
# 厂房2内墙体
for i in range(0, len(plant_up_in_wall_points_2), 2):
    # 取出一组的两个点
    point1 = plant_up_in_wall_points_2[i]
    point2 = plant_up_in_wall_points_2[i+1]
    GFE.draft.get_current().input(point1[0], point1[1])
    GFE.draft.get_current().input(point2[0], point2[1])
    print(f"绘制厂房上层2内部直线: {point1} → {point2}")

# 绘制圆弧(补充墙面)
GFE.draft.get_current().set_snap_object(0)
GFE.draft.get_current().set_operate_mode(5)
# 遍历补充墙体圆弧列表，步长为3
for i in range(0, len(plant_up_wall_arc_points), 3):
    # 取出一组的三个点
    point1 = plant_up_wall_arc_points[i]
    point2 = plant_up_wall_arc_points[i+1]
    point3 = plant_up_wall_arc_points[i+2]
    GFE.draft.get_current().input(point1[0], point1[1])
    GFE.draft.get_current().input(point2[0], point2[1])
    GFE.draft.get_current().input(point3[0], point3[1])
    print(f"绘制厂房上层圆弧外墙: 圆心{point1} → 【{point2}和{point3}】")

# 设置偏移量,完成草图，创建二维模型-通用墙体（6-8层）
# 偏移量 = 厂房下层数量 * 厂房下层高度
plant_up_wall_offset = plant_down_num * plant_down_height
print(f"厂房上层偏移量为：{plant_up_wall_offset}")
GFE.draft.get_current().set_normal([0.0, 0.0, plant_up_wall_offset], [0.0, 0.0, 1.0], [1.0, 0.0, 0.0])
shape = GFE.draft.get_current().export()
if not shape.is_null() :
    mgr = GFE.Pre.geometry.geo_mgr()
    mgr.add('plant-up-wall-base', shape)


# ============ 创建6-8层楼板 =================
def calc_mid_point(p1, p2):
    """ 计算两点的中点 """
    x1, y1 = p1
    x2, y2 = p2
    return ( (x1 + x2)/2, (y1 + y2)/2 )  # 求两点中点

def get_arc_mid_point(arc_3points):
    """
    计算GFE圆弧（圆心, 起点, 终点）的弧线上的中点
    - 参数: arc_3points: GFE圆弧三点列表 [圆心, 起点, 终点]
    - return: 弧中点坐标 (x, y)（保留2位小数）
    """
    # 解析GFE三点：圆心、起点、终点
    center, start, end = arc_3points
    cx, cy = center  # 圆弧圆心
    sx, sy = start  # 圆弧起点
    ex, ey = end  # 圆弧终点

    # 计算半径（起点到圆心的距离，GFE圆弧半径固定）
    r = math.hypot(sx - cx, sy - cy)

    # 计算起点、终点相对于圆心的极角（弧度）
    angle_start = math.atan2(sy - cy, sx - cx)  # 起点极角
    angle_end = math.atan2(ey - cy, ex - cx)  # 终点极角

    # 处理角度跨0°的情况（保证中点角度在圆弧范围内）
    if angle_end < angle_start:
        angle_end += 2 * math.pi

    # 计算弧中点的极角（圆心角的平均值）
    angle_mid = (angle_start + angle_end) / 2

    # 极坐标转直角坐标（得到弧中点）
    x_mid = cx + r * math.cos(angle_mid)
    y_mid = cy + r * math.sin(angle_mid)

    # 保留2位小数，适配GFE绘图精度
    return (round(x_mid, 2), round(y_mid, 2))

# 拆分两个圆弧的三点组
arc1_gfe_points = plant_up_wall_arc_points[0:3]  # 圆弧1的圆心+起点+终点
arc2_gfe_points = plant_up_wall_arc_points[3:6]  # 圆弧2的圆心+起点+终点

# 计算两个圆弧的弧中点
arc1_mid = get_arc_mid_point(arc1_gfe_points)
arc2_mid = get_arc_mid_point(arc2_gfe_points)

# 多选并填充6-8层两个楼板外围线条
GFE.draft.get_current().set_operate_mode(-1)
GFE.draft.get_current().set_snap_object(2)
# --------- 厂房1 -----------
last_point = None   # 上一个点
for point in plant_up_out_wall_points_1:
    if last_point is not None:
        mid_point = calc_mid_point(last_point, point)
        GFE.draft.get_current().snap_object(mid_point[0], mid_point[1])
        GFE.draft.get_current().select_snaped(True)
    last_point = point
# 补充厂房1的圆弧
GFE.draft.get_current().snap_object(arc1_mid[0], arc1_mid[1])
GFE.draft.get_current().select_snaped(True)
GFE.draft.get_current().fill_selected()     # 填充
# 清除选中状态
GFE.draft.get_current().snap_object(0, 0)#取消选择，选择第二个楼板
GFE.draft.get_current().select_snaped(False)

# --------- 厂房2 -----------
last_point = None   # 上一个点
for point in plant_up_out_wall_points_2:
    if last_point is not None:
        mid_point = calc_mid_point(last_point, point)
        GFE.draft.get_current().snap_object(mid_point[0], mid_point[1])
        GFE.draft.get_current().select_snaped(True)
    last_point = point
# 补充厂房2的圆弧
GFE.draft.get_current().snap_object(arc2_mid[0], arc2_mid[1])
GFE.draft.get_current().select_snaped(True)
GFE.draft.get_current().fill_selected()     # 填充

# 设置偏移量,完成草图，创建二维模型通用楼板（6-8层）
# 偏移量 = 厂房下层数量 * 厂房下层高度 + 上层高度
plant_up_slab_offset = plant_down_num * plant_down_height + plant_up_height
print(f"厂房上层楼板偏移量：{plant_up_slab_offset}")
GFE.draft.get_current().set_normal([0.0, 0.0, plant_up_slab_offset], [0.0, 0.0, 1.0], [1.0, 0.0, 0.0])
shape = GFE.draft.get_current().export()
if not shape.is_null() :
    mgr = GFE.Pre.geometry.geo_mgr()
    mgr.add('plant-up-slab', shape)


# ============= 创建三维墙体 ================
plant_down_wall_names = []
plant_up_wall_names = []
# 拉伸厂房通用墙体(1-5层)，创建三维模型
builder = GFE.geometry.geoprim.builder()
shapes = [GFE.Pre.geometry.geo_mgr().find('plant-down-wall-base').shape()]
extruded = builder.extrude(shapes, [0.0, 0.0, plant_down_height])
mgr = Pre.geometry.geo_mgr()
for sp in extruded :
    if not sp.is_null() :
        mgr.add('plant-down-wall', sp)
        plant_down_wall_names.append('plant-down-wall')

# 阵列厂房通用墙体(1-5层)
builder = GFE.geometry.geoprim.builder()
shapes = [GFE.Pre.geometry.geo_mgr().find('plant-down-wall').shape()]
new_shapes = builder.make_array(shapes, 1, 1, plant_down_num, [0.0, 0.0, plant_down_height])
mgr = Pre.geometry.geo_mgr()
for sp in new_shapes :
    if not sp.is_null() :
        name = mgr.auto_name('plant-down-wall')
        mgr.add(name, sp)
        plant_down_wall_names.append(name)

# 拉伸厂房通用墙体(6-8层)，创建三维模型
builder = GFE.geometry.geoprim.builder()
shapes = [GFE.Pre.geometry.geo_mgr().find('plant-up-wall-base').shape()]
extruded = builder.extrude(shapes, [0.0, 0.0, plant_up_height])
mgr = Pre.geometry.geo_mgr()
for sp in extruded :
    if not sp.is_null() :
        mgr.add('plant-up-wall', sp)
        plant_up_wall_names.append('plant-up-wall')

# 阵列厂房通用墙体(6-8层)
builder = GFE.geometry.geoprim.builder()
shapes = [GFE.Pre.geometry.geo_mgr().find('plant-up-wall').shape()]
new_shapes = builder.make_array(shapes, 1, 1, plant_up_num, [0.0, 0.0, plant_up_height])
mgr = Pre.geometry.geo_mgr()
for sp in new_shapes :
    if not sp.is_null() :
        name = mgr.auto_name('plant-up-wall')
        mgr.add(name, sp)
        plant_up_wall_names.append(name)

# 创建厂房所有墙体集合
shapes = []
for name in plant_down_wall_names:
	geo_obj = GFE.Pre.geometry.geo_mgr().find(name)
	faces_sp = GFE.geometry.geotool.children(geo_obj.shape(), 4)
	for f in faces_sp:
		shapes.append(f)
for name in plant_up_wall_names:
	geo_obj = GFE.Pre.geometry.geo_mgr().find(name)
	faces_sp = GFE.geometry.geotool.children(geo_obj.shape(), 4)
	for f in faces_sp:
		shapes.append(f)
gset_basic = GFE.Pre.set.gset_basic('PLANT-WALL')
gset_basic.set_shapes(shapes)
GFE.Pre.set.gset_mgr().add(gset_basic)


# ============ 处理1-5层楼板 =============
# 阵列底板作为1层楼板初型基础
builder = GFE.geometry.geoprim.builder()
shapes = [GFE.Pre.geometry.geo_mgr().find('raft').shape()]
new_shapes = builder.make_array(shapes, 1, 1, 2, [0.0, 0.0, plant_down_height])
mgr = Pre.geometry.geo_mgr()
for sp in new_shapes :
    if not sp.is_null() :
        mgr.add('plant-down-slab', sp)

# 回到草图，清空草图
GFE.draft.get_current().clear()
# 绘制圆形
GFE.draft.get_current().set_snap_object(0)
GFE.draft.get_current().set_operate_mode(7)
GFE.draft.get_current().input(0.0, 0.0)
GFE.draft.get_current().input(0.0, plant_core_radius)

# 填充圆形
GFE.draft.get_current().set_operate_mode(-1)
GFE.draft.get_current().set_snap_object(2)
GFE.draft.get_current().snap_object(0.0, plant_core_radius)
GFE.draft.get_current().select_snaped(True)
GFE.draft.get_current().fill_selected()
# 设置草图偏移8，完成草图，创建二维模型
GFE.draft.get_current().set_normal([0.0, 0.0, plant_down_height], [0.0, 0.0, 1.0], [1.0, 0.0, 0.0])
shape = GFE.draft.get_current().export()
if not shape.is_null() :
    mgr = GFE.Pre.geometry.geo_mgr()
    mgr.add('plant-down-slab-cut', shape)

# 获取第2层楼板---用第2层楼板基础裁剪圆形得到
builder = GFE.geometry.geoprim.builder()
builder.cut('plant-down-slab', ['plant-down-slab-cut'], True)   # 替换原图形

# =============== 创建厂房楼板模型及集合 =============
# 上下层楼板名称
plant_down_slab_names = ['plant-down-slab']
plant_up_slab_names = ['plant-up-slab']

# 阵列通用楼板（1-5层）
builder = GFE.geometry.geoprim.builder()
shapes = [GFE.Pre.geometry.geo_mgr().find('plant-down-slab').shape()]
new_shapes = builder.make_array(shapes, 1, 1, plant_down_num, [0.0, 0.0, plant_down_height])
mgr = Pre.geometry.geo_mgr()
for sp in new_shapes :
    if not sp.is_null() :
        name = mgr.auto_name('plant-down-slab')
        mgr.add(name, sp)
        plant_down_slab_names.append(name)

# 阵列通用楼板（6-8层）
builder = GFE.geometry.geoprim.builder()
shapes = [GFE.Pre.geometry.geo_mgr().find('plant-up-slab').shape()]
new_shapes = builder.make_array(shapes, 1, 1, plant_up_num, [0.0, 0.0, plant_up_height])
mgr = Pre.geometry.geo_mgr()
for sp in new_shapes :
    if not sp.is_null() :
        name = mgr.auto_name('plant-up-slab')
        mgr.add(name, sp)
        plant_up_slab_names.append(name)

# 创建所有楼板集合（1-8层）
shapes = []
for name in plant_down_slab_names:
	geo_obj = GFE.Pre.geometry.geo_mgr().find(name)
	faces_sp = GFE.geometry.geotool.children(geo_obj.shape(), 4)
	for f in faces_sp:
		shapes.append(f)
for name in plant_up_slab_names:
	geo_obj = GFE.Pre.geometry.geo_mgr().find(name)
	faces_sp = GFE.geometry.geotool.children(geo_obj.shape(), 4)
	for f in faces_sp:
		shapes.append(f)
gset_basic = GFE.Pre.set.gset_basic('PLANT-SLAB')
gset_basic.set_shapes(shapes)
GFE.Pre.set.gset_mgr().add(gset_basic)

# ============= 创建底板集合 =============
geo_obj = GFE.Pre.geometry.geo_mgr().find('raft')
shapes = GFE.geometry.geotool.children(geo_obj.shape(), 4)
gset_basic = GFE.Pre.set.gset_basic('RAFT')
gset_basic.set_shapes(shapes)
GFE.Pre.set.gset_mgr().add(gset_basic)


# ============== 创建材料 =============
# materials[0]是第一个材料C40_PLANT，materials[1]是第二个材料C60_PLANT，
# C40_PLANT材料
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
# 添加阻尼
obj_damping= GFE.Pre.material.damping()
obj_damping.n_param = 2
obj_damping.params = [materials[0][4], materials[0][5]]    #阻尼值不一定一样
obj.entries = [obj_density, obj_ela, obj_damping]
GFE.Pre.material.mat_mgr().add(obj)

# C60_PLANT材料
obj = GFE.Pre.material.material()
obj.name = materials[1][0]
obj_density = GFE.Pre.material.density()
obj_density.temp_dp = False
obj_density.n_param = 1
obj_density.params = [materials[1][1]]
obj_ela = GFE.Pre.material.elastic()
obj_ela.temp_dp = False
obj_ela.n_param = 2
obj_ela.type = 0
obj_ela.moduli_time_scale = 0
obj_ela.compression = False
obj_ela.tension = False
obj_ela.params = [materials[1][2], materials[1][3]]
# 添加阻尼
obj_damping= GFE.Pre.material.damping()
obj_damping.n_param = 2
obj_damping.params = [materials[1][4], materials[1][5]]    #阻尼值不一定一样
obj.entries = [obj_density, obj_ela, obj_damping]
GFE.Pre.material.mat_mgr().add(obj)

# ============= 截面属性 ==============
# 墙体截面
obj = GFE.Pre.section.property_shell()
obj.name = 'PLANT-WALL'
obj.elset_name = 'PLANT-WALL'
obj.mat_name = materials[0][0]
obj.thickness = wall_thickness
obj.integral_point = 5
obj.layer_num = 1
obj.params = []
obj.has_rebar = False
obj.Ecc = [0.0, 0.0, 0.0, 0.0]
GFE.Pre.section.sect_mgr().add(obj)

# 楼板截面
obj = GFE.Pre.section.property_shell()
obj.name = 'PLANT-SLAB'
obj.elset_name = 'PLANT-SLAB'
obj.mat_name = materials[0][0]
obj.thickness = slab_thickness
obj.integral_point = 5
obj.layer_num = 1
obj.params = []
obj.has_rebar = False
obj.Ecc = [0.0, 0.0, 0.0, 0.0]
GFE.Pre.section.sect_mgr().add(obj)

# 底板截面
obj = GFE.Pre.section.property_shell()
obj.name = 'RAFT'
obj.elset_name = 'RAFT'
obj.mat_name = materials[0][0]
obj.thickness = raft_thickness
obj.integral_point = 5
obj.layer_num = 1
obj.params = []
obj.has_rebar = False
obj.Ecc = [0.0, 0.0, 0.0, 0.0]
GFE.Pre.section.sect_mgr().add(obj)


# ================ 合并整个厂房 ===============
merge_names = ['raft']
merge_names.extend(plant_down_wall_names)           # 追加下层墙体
merge_names.extend(plant_down_slab_names)           # 追加下层楼板
merge_names.extend(plant_up_wall_names)             # 追加上层墙体
merge_names.extend(plant_up_slab_names)             # 追加上层楼板

builder = GFE.geometry.geoprim.builder()
builder.merge(merge_names, True, 'plant')


# ============= 网格划分 ================
# 划分整个厂房模型
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
'GFE.DefaultSize' : plant_mesh,
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
generator.mesh(['plant'], controller)


# ============= 创建保护壳 ===============
# --------- 创建模型 ----------
# 清空草图
GFE.draft.get_current().clear()
#绘制保护壳-多段折线+圆弧
GFE.draft.get_current().set_snap_object(0)
GFE.draft.get_current().set_operate_mode(2)     # 多段折线
for point in shell_points_1:
    GFE.draft.get_current().input(point[0], point[1])
GFE.draft.get_current().set_operate_mode(4)     # 圆弧
for point in shell_points_2:
    GFE.draft.get_current().input(point[0], point[1])

# 设置为xz平面，完成草图，创建保护壳二维模型
GFE.draft.get_current().set_normal([0.0, 0.0, 0.0], [0.0, -1.0, 0.0], [1.0, 0.0, 0.0])
shape = GFE.draft.get_current().export()
if not shape.is_null() :
    mgr = GFE.Pre.geometry.geo_mgr()
    mgr.add('shell-base', shape)

# 旋转建模，生成保护壳三维模型
builder = GFE.geometry.geoprim.builder()
shapes = [GFE.Pre.geometry.geo_mgr().find('shell-base').shape()]
revolved = builder.revolve(shapes, [0.0, 0.0, 0.0], [0.0, 0.0, 1.0], 6.28319)
mgr = Pre.geometry.geo_mgr()
for sp in revolved :
    if not sp.is_null() :
        mgr.add('shell', sp)

# ----------- 创建保护壳集合 --------------
geo_obj = GFE.Pre.geometry.geo_mgr().find('shell')
shapes = GFE.geometry.geotool.children(geo_obj.shape(), 4)
gset_basic = GFE.Pre.set.gset_basic('SHELL')
gset_basic.set_shapes(shapes)
GFE.Pre.set.gset_mgr().add(gset_basic)

# ---------- 保护壳截面 ---------------
obj = GFE.Pre.section.property_shell()
obj.name = 'SHELL'
obj.elset_name = 'SHELL'
obj.mat_name = materials[1][0]
obj.thickness = 1.5
obj.integral_point = 5
obj.layer_num = 1
obj.params = []
obj.has_rebar = False
obj.Ecc = [0.0, 0.0, 0.0, 0.0]
GFE.Pre.section.sect_mgr().add(obj)

# ---------- 保护壳网格划分 -----------
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
'GFE.DefaultSize' : shell_mesh,
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
generator.mesh(['shell'], controller)


# ============== 创建相互作用 ================
# 找到厂房和保护壳接触的面
search_list = []
search_list.append(['plant', 'shell'])
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

# 创建相互作用-绑定约束
geo_mgr = GFE.Pre.geometry.geo_mgr()
surf_mgr = GFE.Pre.surface.surface_mgr()
tie_mgr = GFE.Pre.interaction.tie_mgr()
for i in range(len(search_result)):
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


# =============== 导入土体材料 =================
import GFE.io
io_instance = GFE.io.get_current()
io_instance.import_mat(soil_materials_path)


#拉伸底板-创建地下室
builder = GFE.geometry.geoprim.builder()
shapes = [GFE.Pre.geometry.geo_mgr().find('raft').shape()]
extruded = builder.extrude(shapes, [0.0, 0.0, plant_basement_depth])
mgr = Pre.geometry.geo_mgr()
for sp in extruded :
    if not sp.is_null() :
        mgr.add('plant-basement', sp)

# =============== 创建非均匀土体 =============
import os
from typing import List
# 校验文件是否存在
if not os.path.exists(file_path):
	raise FileNotFoundError(f"文件不存在：{file_path}")
soil_data = []  #二维数组
with open(file_path, "r", encoding="utf-8") as f:
    # 以换行为结尾，区分一组数据
	for line_num, line in enumerate(f, 1):
		# 去除行首尾空白（换行符、空格等）
		line_stripped = line.strip()
		if not line_stripped:  # 跳过空行
			continue
		# 按制表符\t分割元素，转换为浮点数
		try:
			row = [float(elem) for elem in line_stripped.split("\t")]
			soil_data.append(row)
		except ValueError as e:
			raise ValueError(f"第{line_num}行数据格式错误（需为数字，tab分隔）：{e}")
print(f'成功读取钻孔数据文件，共解析{len(soil_data)}行数据')

# 创建土体钻孔实例
soil_samples = []
for row_num, row in enumerate(soil_data, 1):
	# 校验每行元素数量（需7个：x,y + 5个depth值）
	if len(row) != 7:
		raise ValueError(f"第{row_num}行元素数量错误，数量为：{row}")
	# 配置soil_samples
	sample = GFE.geometry.geotool.SoilSample(x=row[0], y=row[1], depth=row[2:])# [2:]是从[2]一直到[-1]
	soil_samples.append(sample)
print(f'成功创建{len(soil_samples)}个SoilSample实例')

# 创建非均匀土体
GFE.geometry.geotool.build_non_uniform_soil(
	dim = 0,
	materials = soil_materials,
	samples = soil_samples
)

# ============== 平移和裁剪土体 =============
# 查找土体和地下室的形心，计算向量差
soil_geo = GFE.Pre.geometry.geo_mgr().find('NU-Soil-1')
soil_x, soil_y, soil_z = GFE.geometry.geotool.centre_of_mass(soil_geo.shape())
print(f"非均匀土体初始形心坐标{soil_x, soil_y, soil_z}")
center1 = [soil_x, soil_y, 0.0]# 生成的土体上表面z坐标一定是0
# 地下室形心
center2 = [0.0, 0.0, plant_basement_depth]
# 计算向量差
trsf_vec = [center2[i] - center1[i] for i in range(3)]
# 平移土体
builder = GFE.geometry.geoprim.builder()
builder.translate(['NU-Soil-1'], trsf_vec, False)


# 裁剪土体----裁剪对象（地下室）
builder = GFE.geometry.geoprim.builder()
builder.cut('NU-Soil-1', ['plant-basement'], True)

# ============ 土体网格划分 ============
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
'GFE.DefaultSize' : soil_mesh,
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
generator.mesh(['NU-Soil-1'], controller)

# ============== 边界 =================
# 土体底面集合
geo_obj = GFE.Pre.geometry.geo_mgr().find('NU-Soil-1')
minz = 1e10  # 最低的面的z坐标
bottom_faces = []  # 存储底面几何
for f in GFE.geometry.geotool.children(geo_obj.shape(), 4):	#2实体，4面，6边
	fz = GFE.geometry.geotool.centre_of_mass(f)[2]
	if fz < minz-0.1: # 当前面fz小于最低z值
		bottom_faces = []	#清空
		minz = fz # 更新最小 z 值
		bottom_faces.append(f)
	elif minz-0.1 < fz < minz+0.1: #等于
		bottom_faces.append(f)
GFE.Pre.set.gset_mgr().add('Set-base', bottom_faces)

# X方向土面集合
geo_obj = GFE.Pre.geometry.geo_mgr().find('NU-Soil-1')
minx = 1e10
maxx = -1e10
left_faces, right_faces = [],[]
for f in GFE.geometry.geotool.children(geo_obj.shape(), 4):	#2实体，4面，6边
	fx = GFE.geometry.geotool.centre_of_mass(f)[0]
	#存在质心容差问题
	if minx-0.1 < fx < minx+0.1:
		left_faces.append(f)
	elif fx < minx-0.1:
		left_faces = []
		minx = fx
		left_faces.append(f)
	if maxx-0.1 < fx < maxx+0.1:
		right_faces.append(f)
	elif fx > maxx+0.1:
		right_faces = []
		maxx = fx
		right_faces.append(f)
x_faces = left_faces + right_faces
GFE.Pre.set.gset_mgr().add('Set-x', x_faces)

# Y方向土面集合
geo_obj = GFE.Pre.geometry.geo_mgr().find('NU-Soil-1')
miny = 1e10
maxy = -1e10
front_faces, back_faces = [],[]
for f in GFE.geometry.geotool.children(geo_obj.shape(), 4):	#2实体，4面，6边
	fy = GFE.geometry.geotool.centre_of_mass(f)[1]
	#存在质心容差问题
	if miny-0.1 < fy < miny+0.1:
		front_faces.append(f)
	elif fy < miny-0.1:
		front_faces = []
		miny = fy
		front_faces.append(f)
	if maxy-0.1 < fy < maxy+0.1:
		back_faces.append(f)
	elif fy > maxy+0.1:
		back_faces = []
		maxy = fy
		back_faces.append(f)
y_faces = front_faces + back_faces
GFE.Pre.set.gset_mgr().add('Set-y', y_faces)

# ============= 创建土体四周及地面的表面集 =============
# 创建表面集
obj = GFE.Pre.surface.geometry_surface('soil-around')
# 1.获取面形状id
need_faces_sp = bottom_faces + x_faces + y_faces
need_faces_id = []
for f in need_faces_sp:
    id = GFE.geometry.geotool.get_id_by_shape(f)
    need_faces_id.append(id)  # 添加
#print(f'面的数量：{len(need_faces_id)}，面：{need_faces_id}')
# 2.配置obj.data
# 核心逻辑：几何体id+遍历need_faces_id每个子列表f，取f[-1]（最后一个元素），和0(面模式)，组成新列表
obj.data = [[geo_obj.id()] + [f[-1], 0] for f in need_faces_id]
obj.to_node_surface = False
GFE.Pre.surface.surface_mgr().add(obj)


# ============== 建立相互作用 ==============
# 搜索接触面
search_list = []
search_list.append(['NU-Soil-1', 'plant'])
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

# 创建相互作用-绑定约束
geo_mgr = GFE.Pre.geometry.geo_mgr()
surf_mgr = GFE.Pre.surface.surface_mgr()
tie_mgr = GFE.Pre.interaction.tie_mgr()
for i in range(len(search_result)):
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

# =============== 创建荷载 ==============
# 底部约束
obj = GFE.Pre.boundary.boundary()
obj.type = 0
obj.name = 'BC-base'
obj.set = 'Set-base'
obj.valid_dof = 0
obj.value = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
obj.amplitude = ''
obj.value_im = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
obj.amplitude_im = ''
obj.distribution = ''
GFE.Pre.boundary.bc_mgr().add(obj)

# x方向约束
obj = GFE.Pre.boundary.boundary()
obj.type = 1
obj.name = 'BC-x'
obj.set = 'Set-x'
obj.valid_dof = 1
obj.value = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
obj.amplitude = ''
obj.value_im = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
obj.amplitude_im = ''
obj.distribution = ''
GFE.Pre.boundary.bc_mgr().add(obj)

# y方向约束
obj = GFE.Pre.boundary.boundary()
obj.type = 1
obj.name = 'BC-y'
obj.set = 'Set-y'
obj.valid_dof = 2
obj.value = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
obj.amplitude = ''
obj.value_im = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
obj.amplitude_im = ''
obj.distribution = ''
GFE.Pre.boundary.bc_mgr().add(obj)

# 惯性力
obj = GFE.Pre.boundary.boundary()
obj.type = 7
obj.name = 'GRA'
obj.set = ''
obj.valid_dof = 0
obj.value = [0.0, 0.0, -9.8]
obj.amplitude = ''
obj.value_im = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
obj.amplitude_im = ''
obj.distribution = ''
GFE.Pre.boundary.bc_mgr().add(obj)


# ============ 场输出 ===============
# 静力场输出
obj = GFE.Pre.output.output_request()
obj.name = 'FO-Static'
obj.step = 'Step-1'
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
obj_sub1.variables = ['U', 'UR', 'RF', 'RM']
obj_sub1.var_option = -1
obj_sub1.reg_type = -1
obj_sub1.nset = ''
obj_sub2 = GFE.Pre.output.element_output()
obj_sub2.name = 'SubOut-2'
obj_sub2.variables = ['E', 'S', 'SF', 'SM']
obj_sub2.var_option = -1
obj_sub2.reg_type = -1
obj_sub2.elset = ''
obj.sub_output = [obj_sub1, obj_sub2]
GFE.Pre.output.field_mgr().add(obj)


# =============== 分析步 ================
# 模态分析步
obj = GFE.Pre.step.frequency_step()
obj.name = 'Modal-1'
obj.description = ''
obj.nlgeom = False
obj.eigen = 10
GFE.Pre.step.step_mgr().add(obj)

# 静力分析步
obj = GFE.Pre.step.static_general_step()
obj.name = 'Static-1'
obj.init_inc = 0.1
obj.period = 1.0
obj.min_inc = 1e-5
obj.max_inc = 0.1
GFE.Pre.step.step_mgr().add(obj)


# =============== 工况 ===============
# 模态工况
obj = GFE.Pre.case.case()
obj.name = 'model'
obj.steps = ['Initial', 'Modal-1']
obj.bcs['Initial'] = ['BC-base', 'BC-x', 'BC-y']
obj.bcs['Modal-1'] = []
obj.initialConditions['Initial'] = []
obj.fieldReqs['Modal-1'] = ['FO-Static']
obj.histReqs['Modal-1'] = []
obj.elemAdd['Modal-1'] = []
obj.elemDel['Modal-1'] = []
GFE.Pre.case.case_mgr().add(obj)

# 静力工况
obj = GFE.Pre.case.case()
obj.name = 'static'
obj.steps = ['Initial', 'Static-1']
obj.bcs['Initial'] = ['BC-base', 'BC-x', 'BC-y']
obj.bcs['Static-1'] = ['GRA']
obj.initialConditions['Initial'] = []
obj.fieldReqs['Static-1'] = ['FO-Static']
obj.histReqs['Static-1'] = []
obj.elemAdd['Static-1'] = []
obj.elemDel['Static-1'] = []
GFE.Pre.case.case_mgr().add(obj)


# ============= 计算阻尼比 ===============
# 为材料添加阻尼--------------在第4章就已添加

# ============= 一维土层（用于地震波）================
obj = GFE.Pre.soil.soil()
obj.name = 'Soil1D-1'
obj.depth = soil_depth
obj.materials = ['sutiantu', 'lizhinianxingtu', 'quanfenghuahuagangyan', 'qiangfenghuahuagangyan']
obj.bedrock_mat = 'qiangfenghuahuagangyan'
obj.depth_dir = 2
GFE.Pre.soil.soil_mgr().add(obj)

# ============ 创建人工边界 ===============
obj = GFE.Pre.artbc.art_bc()
obj.name = 'ArtBC-1'
obj.structure = 'plant'
obj.surface = 'soil-around'
obj.centered = False
obj.center = []
GFE.Pre.artbc.artbc_mgr().add(obj)

# ============= 幅值函数 =============
obj = GFE.Pre.amplitude.amplitude()
obj.type = 0
obj.name = 'KOBE_JAPAN_1-16-1995_MORIGAWACHI_x'
obj.spectrum_type = -1
obj.gravity = 0.0
obj.value = [0.0, 0.000137356, 0.02, -0.00124718, 0.04, -0.000800188, 0.06, 0.000626556,
0.08, -0.000417312, 0.1, 0.000243576, 0.12, -0.000304554, 0.14, 0.000221261,
0.16, -0.000886168, 0.18, -0.000828558, 0.2, 0.000719363, 0.22, -0.00227289,
0.24, 0.00083764, 0.26, 0.00224413, 0.28, -1.52616e-05, 0.3, -0.000608686,
0.32, -0.00144458, 0.34, 0.000292153, 0.36, 0.000956816, 0.38, -0.00222718,
0.4, 0.000209636, 0.42, -0.000355056, 0.44, -0.00271494, 0.46, 0.00295845,
0.48, 0.00292676, 0.5, -0.000759398, 0.52, -0.00200486, 0.54, -0.00315635,
0.56, -0.00714637, 0.58, -0.000915288, 0.6, 0.00586464, 0.62, 0.00784185,
0.64, 0.00442727, 0.66, -0.00694835, 0.68, -0.00224036, 0.7, -0.00112093,
0.72, -0.00599555, 0.74, 0.00190257, 0.76, 0.011638, 0.78, -0.0103832,
0.8, -0.0150454, 0.82, 0.000680804, 0.84, -0.00291429, 0.86, -6.81682e-05,
0.88, 0.00209686, 0.9, -0.00402892, 0.92, -0.00208365, 0.94, 0.00644689,
0.96, -0.00338222, 0.98, 0.00528649, 1.0, 0.0139091, 1.02, 0.000771768,
1.04, -0.000407398, 1.06, 0.0116753, 1.08, 0.00753324, 1.1, -0.017626,
1.12, -0.0112225, 1.14, 0.000759229, 1.16, -0.00201084, 1.18, -0.0027439,
1.2, -0.00242311, 1.22, 0.000933741, 1.24, -0.00981382, 1.26, 0.0131638,
1.28, 0.00378812, 1.3, 4.11353e-05, 1.32, 0.000196011, 1.34, 0.0270285,
1.36, -0.0078602, 1.38, -0.0142516, 1.4, -0.00573951, 1.42, 0.0114243,
1.44, 0.000639832, 1.46, -0.0128267, 1.48, -0.00283028, 1.5, 0.00863497,
1.52, -0.016416, 1.54, -0.033755, 1.56, -0.0167496, 1.58, -0.00416852,
1.6, -0.0285593, 1.62, -0.03066, 1.64, -0.017124, 1.66, 0.00741906,
1.68, 0.0308931, 1.7, 0.0311399, 1.72, 0.0183516, 1.74, -0.00837635,
1.76, -0.0291583, 1.78, -0.00392413, 1.8, 0.0291608, 1.82, 0.00614439,
1.84, -0.0274411, 1.86, -0.042438, 1.88, -0.00953891, 1.9, 0.0361962,
1.92, 0.0306205, 1.94, -0.0496919, 1.96, -0.0837744, 1.98, -0.0949335,
2.0, -0.0513041, 2.02, -0.0254969, 2.04, 0.0336232, 2.06, -0.000565926,
2.08, -0.0338982, 2.1, -0.114712, 2.12, -0.00127657, 2.14, 0.0554689,
2.16, 0.0925587, 2.18, 0.00298161, 2.2, -0.0597871, 2.22, -0.0872517,
2.24, 0.0130299, 2.26, 0.0942805, 2.28, 0.0917984, 2.3, 0.00335964,
2.32, -0.0501278, 2.34, -0.00203671, 2.36, 0.0735781, 2.38, 0.105378,
2.4, 0.0470057, 2.42, -0.034893, 2.44, -0.084078, 2.46, 0.0271395,
2.48, 0.141012, 2.5, 0.117842, 2.52, 0.0427215, 2.54, -0.00530391,
2.56, -0.0123816, 2.58, 0.00878268, 2.6, 0.0879532, 2.62, 0.0278654,
2.64, -0.104178, 2.66, -0.179181, 2.68, -0.0980113, 2.7, 0.0211969,
2.72, 0.061048, 2.74, 0.0432453, 2.76, -0.0295669, 2.78, -0.118561,
2.8, -0.0607769, 2.82, -0.0114726, 2.84, -0.067931, 2.86, -0.143655,
2.88, -0.0654068, 2.9, 0.0178233, 2.92, 0.0249613, 2.94, 0.0745052,
2.96, 0.173459, 2.98, 0.0287872, 3.0, -0.0624897, 3.02, 0.000200673,
3.04, 0.0683115, 3.06, 0.0749287, 3.08, 0.0243546, 3.1, -0.0356565,
3.12, -0.190185, 3.14, -0.112479, 3.16, 0.0951394, 3.18, 0.0631807,
3.2, -0.14549, 3.22, -0.171996, 3.24, -0.110598, 3.26, -0.038859,
3.28, -0.0497665, 3.3, 0.0107219, 3.32, -0.0534429, 3.34, -0.135445,
3.36, -0.0890526, 3.38, -0.00831703, 3.4, 0.159023, 3.42, 0.0543393,
3.44, 0.0289238, 3.46, 0.0530707, 3.48, 0.0982747, 3.5, 0.147817,
3.52, 0.189559, 3.54, 0.126083, 3.56, -0.0293328, 3.58, 0.0189419,
3.6, 0.194627, 3.62, 0.153009, 3.64, 0.146838, 3.66, 0.137259,
3.68, 0.0728166, 3.7, 0.0317287, 3.72, 0.0642282, 3.74, 0.122757,
3.76, -0.0101831, 3.78, -0.168255, 3.8, -0.119527, 3.82, 0.0154732,
3.84, -0.0064803, 3.86, -0.0413309, 3.88, -0.111966, 3.9, -0.175218,
3.92, -0.140937, 3.94, 0.0876391, 3.96, -0.00357148, 3.98, -0.0672201,
4.0, -0.086891, 4.02, -0.135935, 4.04, 0.0260612, 4.06, 0.13384,
4.08, 0.131946, 4.1, 0.0277485, 4.12, -0.0385162, 4.14, 0.165217,
4.16, 0.217338, 4.18, 0.0375253, 4.2, -0.165414, 4.22, 0.107632,
4.24, 0.0622954, 4.26, 0.0104255, 4.28, -0.0116258, 4.3, -0.0303827,
4.32, 0.00958108, 4.34, -0.0680583, 4.36, -0.108012, 4.38, -0.0679315,
4.4, -0.070529, 4.42, -0.214188, 4.44, -0.137649, 4.46, -0.0943776,
4.48, -0.289393, 4.5, 0.0493819, 4.52, 0.136124, 4.54, -0.0909087,
4.56, -0.291816, 4.58, -0.0976544, 4.6, -0.0261528, 4.62, -0.174725,
4.64, 0.00788938, 4.66, 0.095024, 4.68, 0.258242, 4.7, 0.230979,
4.72, 0.215087, 4.74, 0.226566, 4.76, 0.000425018, 4.78, 0.0575134,
4.8, 0.111989, 4.82, 0.0565368, 4.84, -0.132114, 4.86, -0.0743335,
4.88, -0.00336824, 4.9, -0.0280284, 4.92, -0.0831398, 4.94, -0.0890154,
4.96, -0.06632, 4.98, -0.269696, 5.0, 0.0257476, 5.02, 0.00645417,
5.04, -0.215947, 5.06, -0.30491, 5.08, 0.0254834, 5.1, 0.0614546,
5.12, -0.138401, 5.14, -0.0561093, 5.16, 0.127385, 5.18, 0.209004,
5.2, 0.0820527, 5.22, 0.237366, 5.24, 0.351381, 5.26, 0.0192687,
5.28, -0.108842, 5.3, -0.0232987, 5.32, 0.12913, 5.34, 0.134868,
5.36, 0.0325745, 5.38, 0.194539, 5.4, 0.134146, 5.42, 0.0910946,
5.44, -0.003726, 5.46, -0.188506, 5.48, -0.137845, 5.5, 0.163966,
5.52, 0.204633, 5.54, 0.156509, 5.56, -0.125835, 5.58, -0.264529,
5.6, -0.0564178, 5.62, -0.0557818, 5.64, -0.103486, 5.66, -0.0599483,
5.68, 0.0605812, 5.7, -0.0499711, 5.72, -0.0807829, 5.74, 0.11518,
5.76, 0.0984491, 5.78, 0.143003, 5.8, 0.383772, 5.82, 0.249739,
5.84, -0.128535, 5.86, -0.335272, 5.88, -0.0577969, 5.9, 0.112197,
5.92, -0.00951377, 5.94, 0.013924, 5.96, 0.154968, 5.98, -0.140506,
6.0, -0.150271, 6.02, 0.0231144, 6.04, -0.121986, 6.06, -0.22467,
6.08, -0.024164, 6.1, 0.0776503, 6.12, -0.0230916, 6.14, -0.125914,
6.16, -0.066433, 6.18, -0.184463, 6.2, -0.187597, 6.22, -0.0338132,
6.24, 0.0277133, 6.26, 0.127767, 6.28, 0.274899, 6.3, 0.12449,
6.32, -0.0229297, 6.34, 0.0136857, 6.36, 0.0757586, 6.38, 0.253363,
6.4, 0.222447, 6.42, 0.061096, 6.44, 0.175601, 6.46, 0.0789497,
6.48, -0.00447601, 6.5, -0.059163, 6.52, -0.148032, 6.54, 0.00165725,
6.56, 0.00677023, 6.58, -0.0659092, 6.6, 0.0160486, 6.62, 0.00577343,
6.64, -0.073846, 6.66, -0.244641, 6.68, -0.208498, 6.7, -0.16451,
6.72, -0.024842, 6.74, 0.0843602, 6.76, -0.00993374, 6.78, 0.000666143,
6.8, 0.0852293, 6.82, -0.0162353, 6.84, -0.0078253, 6.86, 0.102744,
6.88, 0.0946781, 6.9, 0.0716255, 6.92, 0.00630227, 6.94, -0.0908996,
6.96, 0.179361, 6.98, 0.238564, 7.0, 0.0415455, 7.02, -0.120828,
7.04, 0.0603288, 7.06, 0.15005, 7.08, 0.111659, 7.1, 0.0586774,
7.12, -0.0202462, 7.14, -0.285404, 7.16, -0.449607, 7.18, -0.244123,
7.2, 0.0553335, 7.22, 0.0515587, 7.24, -0.0744412, 7.26, 0.0447528,
7.28, 0.0756128, 7.3, 0.0850678, 7.32, 0.270954, 7.34, 0.409262,
7.36, 0.462053, 7.38, 0.371177, 7.4, 0.312396, 7.42, 0.234201,
7.44, 0.35066, 7.46, 0.382922, 7.48, 0.28986, 7.5, 0.43572,
7.52, 0.529733, 7.54, 0.60569, 7.56, 0.507504, 7.58, 0.336701,
7.6, 0.0875949, 7.62, 0.155755, 7.64, 0.342697, 7.66, 0.418844,
7.68, 0.280521, 7.7, 0.014669, 7.72, -0.0756004, 7.74, -0.3717,
7.76, -0.618447, 7.78, -0.830481, 7.8, -0.78203, 7.82, -0.740095,
7.84, -0.82587, 7.86, -0.879739, 7.88, -1.0124, 7.9, -0.920847,
7.92, -0.92699, 7.94, -0.793093, 7.96, -0.465459, 7.98, -0.115055,
8.0, 0.0430105, 8.02, 0.133541, 8.04, 0.290403, 8.06, 0.414347,
8.08, 0.689773, 8.1, 0.73456, 8.12, 0.783355, 8.14, 1.02438,
8.16, 1.19403, 8.18, 0.981902, 8.2, 0.818435, 8.22, 0.835992,
8.24, 0.89274, 8.26, 0.879329, 8.28, 0.774281, 8.3, 0.647838,
8.32, 0.607033, 8.34, 0.610042, 8.36, 0.485797, 8.38, 0.247144,
8.4, 0.0217359, 8.42, -0.218181, 8.44, -0.491495, 8.46, -0.813864,
8.48, -1.22177, 8.5, -1.51407, 8.52, -1.61635, 8.54, -1.60849,
8.56, -1.65038, 8.58, -1.62643, 8.6, -1.58692, 8.62, -1.55919,
8.64, -1.40884, 8.66, -0.862257, 8.68, -0.33482, 8.7, 0.0362211,
8.72, 0.302883, 8.74, 0.563136, 8.76, 0.638539, 8.78, 0.660375,
8.8, 0.819056, 8.82, 0.859304, 8.84, 0.477863, 8.86, 0.0390612,
8.88, -0.2044, 8.9, -0.265385, 8.92, -0.240296, 8.94, -0.0573324,
8.96, -0.165373, 8.98, -0.462624, 9.0, -0.671289, 9.02, -0.803582,
9.04, -0.849072, 9.06, -0.86888, 9.08, -0.759346, 9.1, -0.540383,
9.12, -0.357561, 9.14, 0.0559237, 9.16, 0.340395, 9.18, 0.418637,
9.2, 0.646452, 9.22, 0.85611, 9.24, 0.933783, 9.26, 0.769966,
9.28, 0.623666, 9.3, 0.498305, 9.32, 0.435951, 9.34, 0.556335,
9.36, 0.766775, 9.38, 0.844079, 9.4, 0.61152, 9.42, 0.249399,
9.44, 0.168757, 9.46, 0.00432534, 9.48, -0.43294, 9.5, -0.887288,
9.52, -0.823336, 9.54, -0.77523, 9.56, -0.702743, 9.58, -0.768148,
9.6, -0.981457, 9.62, -0.975218, 9.64, -0.669496, 9.66, -0.394853,
9.68, -0.344396, 9.7, -0.451461, 9.72, -0.70228, 9.74, -0.939803,
9.76, -0.747042, 9.78, 0.0600421, 9.8, 0.640754, 9.82, 0.972915,
9.84, 1.07157, 9.86, 1.26903, 9.88, 1.32747, 9.9, 1.22566,
9.92, 1.11855, 9.94, 1.13638, 9.96, 1.11176, 9.98, 0.700427,
10.0, 0.268199, 10.02, 0.22373, 10.04, 0.389174, 10.06, 0.18301,
10.08, -0.431642, 10.1, -0.914817, 10.12, -0.978383, 10.14, -0.955642,
10.16, -1.08464, 10.18, -1.33992, 10.2, -1.49226, 10.22, -1.63021,
10.24, -1.75245, 10.26, -1.57248, 10.28, -1.44411, 10.3, -1.11739,
10.32, -0.729328, 10.34, -0.429409, 10.36, -0.10707, 10.38, 0.598967,
10.4, 1.18958, 10.42, 1.30386, 10.44, 1.37795, 10.46, 1.49192,
10.48, 1.46302, 10.5, 1.18319, 10.52, 1.23728, 10.54, 1.49284,
10.56, 1.68158, 10.58, 1.49841, 10.6, 1.2872, 10.62, 1.15227,
10.64, 1.04899, 10.66, 0.919607, 10.68, 0.870921, 10.7, 0.836662,
10.72, 0.803766, 10.74, 0.793665, 10.76, 0.756249, 10.78, 0.599262,
10.8, 0.420128, 10.82, 0.266776, 10.84, 0.131292, 10.86, 0.121067,
10.88, 0.171501, 10.9, -0.00351813, 10.92, -0.326778, 10.94, -0.705656,
10.96, -0.821996, 10.98, -0.98166, 11.0, -1.18826, 11.02, -1.2115,
11.04, -1.29669, 11.06, -1.45111, 11.08, -1.68812, 11.1, -1.68624,
11.12, -1.45245, 11.14, -1.13276, 11.16, -1.0358, 11.18, -1.03695,
11.2, -0.830001, 11.22, -0.569566, 11.24, -0.379223, 11.26, -0.172665,
11.28, 0.184728, 11.3, 0.444761, 11.32, 0.392591, 11.34, 0.500265,
11.36, 0.712294, 11.38, 0.932482, 11.4, 1.07602, 11.42, 1.21322,
11.44, 1.33713, 11.46, 1.26368, 11.48, 1.07265, 11.5, 0.941462,
11.52, 0.923705, 11.54, 1.00052, 11.56, 1.13648, 11.58, 1.19068,
11.6, 1.07365, 11.62, 0.988441, 11.64, 1.00411, 11.66, 1.03719,
11.68, 1.02072, 11.7, 0.775359, 11.72, 0.318015, 11.74, -0.159475,
11.76, -0.501371, 11.78, -0.640995, 11.8, -0.666507, 11.82, -0.739151,
11.84, -0.948941, 11.86, -1.157, 11.88, -1.24746, 11.9, -1.25996,
11.92, -1.4521, 11.94, -1.7409, 11.96, -2.05112, 11.98, -2.14103,
12.0, -2.0898, 12.02, -2.05951, 12.04, -1.85974, 12.06, -1.42284,
12.08, -1.09736, 12.1, -0.766902, 12.12, -0.556481, 12.14, -0.379736,
12.16, -0.148094, 12.18, 0.0536099, 12.2, 0.0619522, 12.22, -0.0490264,
12.24, -0.0638008, 12.26, -0.00499448, 12.28, 0.138528, 12.3, 0.300552,
12.32, 0.5954, 12.34, 0.930812, 12.36, 1.06137, 12.38, 0.986779,
12.4, 1.00736, 12.42, 1.30256, 12.44, 1.63195, 12.46, 1.8083,
12.48, 1.77503, 12.5, 1.4885, 12.52, 1.14379, 12.54, 0.923679,
12.56, 0.688219, 12.58, 0.440421, 12.6, 0.266387, 12.62, 0.159992,
12.64, 0.043015, 12.66, -0.0675965, 12.68, -0.0831065, 12.7, -0.079918,
12.72, 0.0663639, 12.74, 0.354433, 12.76, 0.523838, 12.78, 0.490153,
12.8, 0.383965, 12.82, 0.479257, 12.84, 0.722477, 12.86, 0.77628,
12.88, 0.682164, 12.9, 0.524841, 12.92, 0.37688, 12.94, 0.322432,
12.96, 0.314991, 12.98, 0.241044, 13.0, 0.153659, 13.02, 0.00596722,
13.04, -0.220976, 13.06, -0.420028, 13.08, -0.514725, 13.1, -0.496492,
13.12, -0.450403, 13.14, -0.448764, 13.16, -0.361504, 13.18, -0.296268,
13.2, -0.375091, 13.22, -0.422547, 13.24, -0.602329, 13.26, -0.772641,
13.28, -0.696297, 13.3, -0.544255, 13.32, -0.536148, 13.34, -0.625273,
13.36, -0.650197, 13.38, -0.567209, 13.4, -0.557029, 13.42, -0.488417,
13.44, -0.320964, 13.46, -0.333075, 13.48, -0.221622, 13.5, 0.0441308,
13.52, 0.18161, 13.54, 0.113393, 13.56, 0.0973012, 13.58, 0.239009,
13.6, 0.316534, 13.62, 0.377868, 13.64, 0.377719, 13.66, 0.281708,
13.68, 0.258961, 13.7, 0.442769, 13.72, 0.649236, 13.74, 0.537885,
13.76, 0.303218, 13.78, 0.113914, 13.8, -0.0034518, 13.82, -0.0997959,
13.84, -0.150503, 13.86, -0.261754, 13.88, -0.385832, 13.9, -0.509458,
13.92, -0.626381, 13.94, -0.755168, 13.96, -0.767943, 13.98, -0.66884,
14.0, -0.588813, 14.02, -0.613786, 14.04, -0.611432, 14.06, -0.562635,
14.08, -0.467754, 14.1, -0.382222, 14.12, -0.254216, 14.14, -0.183208,
14.16, -0.273902, 14.18, -0.444462, 14.2, -0.490811, 14.22, -0.330733,
14.24, -0.0603951, 14.26, 0.302377, 14.28, 0.438438, 14.3, 0.25963,
14.32, 0.0326912, 14.34, 0.00734035, 14.36, 0.188426, 14.38, 0.252632,
14.4, 0.0364121, 14.42, -0.286891, 14.44, -0.449737, 14.46, -0.502943,
14.48, -0.478109, 14.5, -0.332451, 14.52, -0.160536, 14.54, -0.0701335,
14.56, -0.0394684, 14.58, -0.0278381, 14.6, -0.136951, 14.62, -0.242538,
14.64, -0.0919814, 14.66, 0.100421, 14.68, 0.272007, 14.7, 0.425393,
14.72, 0.598716, 14.74, 0.768393, 14.76, 0.887597, 14.78, 0.879939,
14.8, 0.872578, 14.82, 0.940653, 14.84, 0.947332, 14.86, 0.799951,
14.88, 0.667591, 14.9, 0.689694, 14.92, 0.610674, 14.94, 0.480861,
14.96, 0.366815, 14.98, 0.30159, 15.0, 0.317366, 15.02, 0.321431,
15.04, 0.30001, 15.06, 0.171571, 15.08, -0.00275617, 15.1, -0.222296,
15.12, -0.399556, 15.14, -0.523364, 15.16, -0.637581, 15.18, -0.764263,
15.2, -0.844175, 15.22, -0.783798, 15.24, -0.669348, 15.26, -0.652824,
15.28, -0.646703, 15.3, -0.624188, 15.32, -0.650432, 15.34, -0.693851,
15.36, -0.795079, 15.38, -0.900429, 15.4, -0.937145, 15.42, -0.873341,
15.44, -0.770813, 15.46, -0.673176, 15.48, -0.50676, 15.5, -0.312431,
15.52, -0.177832, 15.54, -0.0593421, 15.56, 0.0293145, 15.58, 0.0887374,
15.6, 0.159432, 15.62, 0.191446, 15.64, 0.279932, 15.66, 0.427718,
15.68, 0.466583, 15.7, 0.380868, 15.72, 0.38689, 15.74, 0.550149,
15.76, 0.705924, 15.78, 0.728153, 15.8, 0.623378, 15.82, 0.465775,
15.84, 0.435246, 15.86, 0.536383, 15.88, 0.668534, 15.9, 0.683825,
15.92, 0.666447, 15.94, 0.676067, 15.96, 0.671473, 15.98, 0.674276,
16.0, 0.716296, 16.02, 0.665111, 16.04, 0.461933, 16.06, 0.294444,
16.08, 0.184207, 16.1, 0.0165025, 16.12, -0.156162, 16.14, -0.339643,
16.16, -0.634368, 16.18, -0.902757, 16.2, -1.01386, 16.22, -1.03324,
16.24, -1.07514, 16.26, -1.12357, 16.28, -1.13453, 16.3, -1.18867,
16.32, -1.13949, 16.34, -1.04764, 16.36, -0.916317, 16.38, -0.819601,
16.4, -0.711108, 16.42, -0.552945, 16.44, -0.318253, 16.46, -0.0941467,
16.48, 0.118689, 16.5, 0.303926, 16.52, 0.339935, 16.54, 0.204766,
16.56, 0.0617374, 16.58, 0.0386436, 16.6, 0.0345882, 16.62, 0.0393744,
16.64, 0.0249612, 16.66, -0.0154815, 16.68, -0.10237, 16.7, -0.0914724,
16.72, -0.0473318, 16.74, 0.0692567, 16.76, 0.236102, 16.78, 0.365999,
16.8, 0.335369, 16.82, 0.261962, 16.84, 0.259692, 16.86, 0.267486,
16.88, 0.353564, 16.9, 0.467712, 16.92, 0.517798, 16.94, 0.504289,
16.96, 0.482066, 16.98, 0.472418, 17.0, 0.49633, 17.02, 0.567616,
17.04, 0.680233, 17.06, 0.73113, 17.08, 0.709691, 17.1, 0.704989,
17.12, 0.668968, 17.14, 0.639147, 17.16, 0.673146, 17.18, 0.710764,
17.2, 0.701773, 17.22, 0.720791, 17.24, 0.731471, 17.26, 0.732711,
17.28, 0.764231, 17.3, 0.700611, 17.32, 0.463731, 17.34, 0.253063,
17.36, 0.162252, 17.38, 0.128284, 17.4, 0.0499296, 17.42, -0.100182,
17.44, -0.224798, 17.46, -0.302444, 17.48, -0.324242, 17.5, -0.379057,
17.52, -0.362743, 17.54, -0.289011, 17.56, -0.310123, 17.58, -0.309271,
17.6, -0.196836, 17.62, -0.0676864, 17.64, 0.0467097, 17.66, 0.150608,
17.68, 0.229149, 17.7, 0.321381, 17.72, 0.474381, 17.74, 0.554244,
17.76, 0.544048, 17.78, 0.593248, 17.8, 0.642094, 17.82, 0.613196,
17.84, 0.601251, 17.86, 0.568345, 17.88, 0.364338, 17.9, 0.174924,
17.92, 0.160053, 17.94, 0.197865, 17.96, 0.182074, 17.98, 0.136663,
18.0, 0.0490132, 18.02, -0.073762, 18.04, -0.19991, 18.06, -0.291525,
18.08, -0.406603, 18.1, -0.612557, 18.12, -0.831943, 18.14, -0.948045,
18.16, -0.951609, 18.18, -0.916423, 18.2, -0.844202, 18.22, -0.807448,
18.24, -0.855566, 18.26, -0.833264, 18.28, -0.739894, 18.3, -0.713729,
18.32, -0.674357, 18.34, -0.631868, 18.36, -0.586309, 18.38, -0.528039,
18.4, -0.425688, 18.42, -0.232049, 18.44, 0.00617082, 18.46, 0.213349,
18.48, 0.37915, 18.5, 0.425112, 18.52, 0.388901, 18.54, 0.319619,
18.56, 0.195734, 18.58, 0.122195, 18.6, 0.164506, 18.62, 0.224509,
18.64, 0.156098, 18.66, 0.0422218, 18.68, 0.0755746, 18.7, 0.162754,
18.72, 0.0917558, 18.74, -0.0591931, 18.76, -0.256525, 18.78, -0.505668,
18.8, -0.711462, 18.82, -0.872616, 18.84, -1.02314, 18.86, -1.14044,
18.88, -1.19716, 18.9, -1.12663, 18.92, -1.01017, 18.94, -0.84416,
18.96, -0.669, 18.98, -0.55082, 19.0, -0.476949, 19.02, -0.406938,
19.04, -0.334487, 19.06, -0.209495, 19.08, -0.0269667, 19.1, 0.147566,
19.12, 0.299501, 19.14, 0.429865, 19.16, 0.569976, 19.18, 0.719647,
19.2, 0.867549, 19.22, 0.979813, 19.24, 1.00732, 19.26, 0.972158,
19.28, 0.945703, 19.3, 0.944915, 19.32, 0.967971, 19.34, 0.910043,
19.36, 0.753772, 19.38, 0.636995, 19.4, 0.566493, 19.42, 0.457088,
19.44, 0.334983, 19.46, 0.292283, 19.48, 0.297093, 19.5, 0.189937,
19.52, 0.0492152, 19.54, -0.0952768, 19.56, -0.219805, 19.58, -0.379068,
19.6, -0.470696, 19.62, -0.507471, 19.64, -0.521288, 19.66, -0.528651,
19.68, -0.544379, 19.7, -0.534282, 19.72, -0.454864, 19.74, -0.313006,
19.76, -0.216163, 19.78, -0.141267, 19.8, -0.0432631, 19.82, 0.111295,
19.84, 0.215861, 19.86, 0.255382, 19.88, 0.26375, 19.9, 0.291565,
19.92, 0.31979, 19.94, 0.352998, 19.96, 0.397431, 19.98, 0.361018,
20.0, 0.293275, 20.02, 0.29263, 20.04, 0.353655, 20.06, 0.407714,
20.08, 0.360831, 20.1, 0.193404, 20.12, -0.005235, 20.14, -0.177876,
20.16, -0.220553, 20.18, -0.190892, 20.2, -0.108188, 20.22, -0.06971,
20.24, -0.131899, 20.26, -0.203859, 20.28, -0.260455, 20.3, -0.273707,
20.32, -0.263244, 20.34, -0.274224, 20.36, -0.304675, 20.38, -0.368044,
20.4, -0.46186, 20.42, -0.510018, 20.44, -0.473828, 20.46, -0.404039,
20.48, -0.359619, 20.5, -0.351159, 20.52, -0.312058, 20.54, -0.244406,
20.56, -0.183294, 20.58, -0.0265178, 20.6, 0.113486, 20.62, 0.140035,
20.64, 0.135604, 20.66, 0.0845794, 20.68, 0.0459429, 20.7, 0.0147684,
20.72, -0.0526282, 20.74, -0.150378, 20.76, -0.25233, 20.78, -0.341066,
20.8, -0.412976, 20.82, -0.494915, 20.84, -0.579266, 20.86, -0.601909,
20.88, -0.604255, 20.9, -0.591732, 20.92, -0.520903, 20.94, -0.433627,
20.96, -0.407586, 20.98, -0.357335, 21.0, -0.245234, 21.02, -0.148624,
21.04, -0.0323595, 21.06, 0.0694469, 21.08, 0.136858, 21.1, 0.200579,
21.12, 0.248449, 21.14, 0.259918, 21.16, 0.284751, 21.18, 0.338045,
21.2, 0.395208, 21.22, 0.398331, 21.24, 0.409008, 21.26, 0.404516,
21.28, 0.353152, 21.3, 0.274938, 21.32, 0.259829, 21.34, 0.32399,
21.36, 0.381227, 21.38, 0.40378, 21.4, 0.410624, 21.42, 0.429484,
21.44, 0.443445, 21.46, 0.443622, 21.48, 0.431942, 21.5, 0.386039,
21.52, 0.290669, 21.54, 0.202755, 21.56, 0.150418, 21.58, 0.130016,
21.6, 0.133018, 21.62, 0.182326, 21.64, 0.249439, 21.66, 0.256621,
21.68, 0.224706, 21.7, 0.228251, 21.72, 0.262176, 21.74, 0.254811,
21.76, 0.255908, 21.78, 0.318256, 21.8, 0.425461, 21.82, 0.479811,
21.84, 0.464104, 21.86, 0.442879, 21.88, 0.448313, 21.9, 0.465509,
21.92, 0.442147, 21.94, 0.416578, 21.96, 0.396911, 21.98, 0.380946,
22.0, 0.355179, 22.02, 0.302914, 22.04, 0.232791, 22.06, 0.159778,
22.08, 0.133825, 22.1, 0.139528, 22.12, 0.0958919, 22.14, 0.00373146,
22.16, -0.0882335, 22.18, -0.181091, 22.2, -0.263787, 22.22, -0.263459,
22.24, -0.205066, 22.26, -0.184448, 22.28, -0.187725, 22.3, -0.224812,
22.32, -0.298853, 22.34, -0.336437, 22.36, -0.325864, 22.38, -0.323242,
22.4, -0.313298, 22.42, -0.273483, 22.44, -0.203706, 22.46, -0.132673,
22.48, -0.0811478, 22.5, -0.0512283, 22.52, -0.0478276, 22.54, -0.0351581,
22.56, -0.0285768, 22.58, -0.0444891, 22.6, -0.0669568, 22.62, -0.058637,
22.64, 0.00139928, 22.66, 0.0641682, 22.68, 0.12235, 22.7, 0.183473,
22.72, 0.215439, 22.74, 0.206983, 22.76, 0.197142, 22.78, 0.206622,
22.8, 0.227389, 22.82, 0.214954, 22.84, 0.156763, 22.86, 0.0795396,
22.88, 0.010826, 22.9, -0.0591042, 22.92, -0.170827, 22.94, -0.266396,
22.96, -0.324701, 22.98, -0.391131, 23.0, -0.458645, 23.02, -0.469535,
23.04, -0.475817, 23.06, -0.492288, 23.08, -0.506764, 23.1, -0.533832,
23.12, -0.524921, 23.14, -0.451937, 23.16, -0.31945, 23.18, -0.199775,
23.2, -0.125254, 23.22, -0.0422784, 23.24, 0.0562247, 23.26, 0.121386,
23.28, 0.155995, 23.3, 0.158596, 23.32, 0.18789, 23.34, 0.263943,
23.36, 0.3389, 23.38, 0.363319, 23.4, 0.389541, 23.42, 0.388729,
23.44, 0.375008, 23.46, 0.341784, 23.48, 0.270228, 23.5, 0.190949,
23.52, 0.130578, 23.54, 0.0378547, 23.56, -0.0549017, 23.58, -0.0973213,
23.6, -0.106874, 23.62, -0.120826, 23.64, -0.154633, 23.66, -0.171117,
23.68, -0.170224, 23.7, -0.1811, 23.72, -0.217348, 23.74, -0.273302,
23.76, -0.286276, 23.78, -0.239602, 23.8, -0.174671, 23.82, -0.158362,
23.84, -0.157362, 23.86, -0.14681, 23.88, -0.163367, 23.9, -0.189243,
23.92, -0.197836, 23.94, -0.16734, 23.96, -0.139375, 23.98, -0.145901,
24.0, -0.153399, 24.02, -0.132791, 24.04, -0.0617877, 24.06, 0.00819483,
24.08, 0.0343707, 24.1, 0.03536, 24.12, 0.0433027, 24.14, 0.0737391,
24.16, 0.113728, 24.18, 0.195046, 24.2, 0.270529, 24.22, 0.336171,
24.24, 0.3993, 24.26, 0.44034, 24.28, 0.431008, 24.3, 0.381377,
24.32, 0.338571, 24.34, 0.291205, 24.36, 0.218115, 24.38, 0.107021,
24.4, -0.042333, 24.42, -0.213211, 24.44, -0.320924, 24.46, -0.381665,
24.48, -0.436813, 24.5, -0.471897, 24.52, -0.475187, 24.54, -0.464095,
24.56, -0.443738, 24.58, -0.397764, 24.6, -0.336002, 24.62, -0.317699,
24.64, -0.332754, 24.66, -0.293741, 24.68, -0.233018, 24.7, -0.184374,
24.72, -0.133538, 24.74, -0.06275, 24.76, 0.0207402, 24.78, 0.0805955,
24.8, 0.108149, 24.82, 0.135002, 24.84, 0.178719, 24.86, 0.239203,
24.88, 0.268571, 24.9, 0.274956, 24.92, 0.264741, 24.94, 0.232594,
24.96, 0.210663, 24.98, 0.191447, 25.0, 0.191394, 25.02, 0.173726,
25.04, 0.147216, 25.06, 0.113763, 25.08, 0.0840156, 25.1, 0.0637771,
25.12, 0.0256027, 25.14, 0.0106251, 25.16, 0.0109352, 25.18, -0.00747655,
25.2, -0.0399706, 25.22, -0.0330005, 25.24, -0.0025992, 25.26, 0.0239076,
25.28, 0.0213516, 25.3, -0.0271382, 25.32, -0.0640118, 25.34, -0.0738556,
25.36, -0.0536658, 25.38, -0.0215303, 25.4, 0.0238979, 25.42, 0.0592697,
25.44, 0.0908703, 25.46, 0.118942, 25.48, 0.156749, 25.5, 0.206265,
25.52, 0.247496, 25.54, 0.260214, 25.56, 0.251848, 25.58, 0.231696,
25.6, 0.228317, 25.62, 0.266535, 25.64, 0.30121, 25.66, 0.287833,
25.68, 0.213628, 25.7, 0.136085, 25.72, 0.0755272, 25.74, 0.034938,
25.76, -0.00203643, 25.78, -0.0124534, 25.8, -0.0595557, 25.82, -0.134443,
25.84, -0.191349, 25.86, -0.213863, 25.88, -0.23379, 25.9, -0.262505,
25.92, -0.259143, 25.94, -0.213823, 25.96, -0.177984, 25.98, -0.167507,
26.0, -0.170883, 26.02, -0.173288, 26.04, -0.170362, 26.06, -0.164271,
26.08, -0.126431, 26.1, -0.106006, 26.12, -0.102184, 26.14, -0.111196,
26.16, -0.1342, 26.18, -0.150965, 26.2, -0.182917, 26.22, -0.210982,
26.24, -0.242004, 26.26, -0.281848, 26.28, -0.320754, 26.3, -0.346361,
26.32, -0.346131, 26.34, -0.339397, 26.36, -0.339027, 26.38, -0.353356,
26.4, -0.357977, 26.42, -0.338365, 26.44, -0.289752, 26.46, -0.227214,
26.48, -0.162802, 26.5, -0.125479, 26.52, -0.104287, 26.54, -0.0866678,
26.56, -0.0785765, 26.58, -0.0685637, 26.6, -0.0711895, 26.62, -0.079432,
26.64, -0.0576451, 26.66, -0.0401604, 26.68, -0.0701676, 26.7, -0.139139,
26.72, -0.174206, 26.74, -0.182404, 26.76, -0.19696, 26.78, -0.179654,
26.8, -0.144037, 26.82, -0.109972, 26.84, -0.0863957, 26.86, -0.0554226,
26.88, 0.0149019, 26.9, 0.110266, 26.92, 0.176054, 26.94, 0.197452,
26.96, 0.191113, 26.98, 0.193881, 27.0, 0.206854, 27.02, 0.225735,
27.04, 0.232442, 27.06, 0.229203, 27.08, 0.248675, 27.1, 0.286112,
27.12, 0.330263, 27.14, 0.383886, 27.16, 0.432305, 27.18, 0.465902,
27.2, 0.477118, 27.22, 0.462054, 27.24, 0.425772, 27.26, 0.400221,
27.28, 0.385939, 27.3, 0.373462, 27.32, 0.35201, 27.34, 0.339758,
27.36, 0.337163, 27.38, 0.301894, 27.4, 0.265924, 27.42, 0.23728,
27.44, 0.173851, 27.46, 0.11279, 27.48, 0.0754444, 27.5, 0.042057,
27.52, 0.00886351, 27.54, -0.0259537, 27.56, -0.0524145, 27.58, -0.0820148,
27.6, -0.105988, 27.62, -0.131966, 27.64, -0.134613, 27.66, -0.119373,
27.68, -0.0990434, 27.7, -0.0842041, 27.72, -0.0776274, 27.74, -0.0646605,
27.76, -0.0448648, 27.78, -0.0103826, 27.8, 0.0106164, 27.82, 0.016252,
27.84, 0.0112451, 27.86, 0.0253575, 27.88, 0.0238686, 27.9, -0.000318952,
27.92, -0.0355591, 27.94, -0.0601195, 27.96, -0.0795026, 27.98, -0.0888911,
28.0, -0.0681598, 28.02, -0.0475989, 28.04, -0.0427349, 28.06, -0.0595957,
28.08, -0.069637, 28.1, -0.0573519, 28.12, -0.02577, 28.14, 0.00571575,
28.16, 0.0518939, 28.18, 0.105594, 28.2, 0.155724, 28.22, 0.187647,
28.24, 0.197039, 28.26, 0.210063, 28.28, 0.218373, 28.3, 0.214071,
28.32, 0.212961, 28.34, 0.222933, 28.36, 0.218463, 28.38, 0.204836,
28.4, 0.18947, 28.42, 0.184706, 28.44, 0.177399, 28.46, 0.169043,
28.48, 0.139785, 28.5, 0.0889229, 28.52, 0.0484426, 28.54, 0.0316972,
28.56, 0.0310215, 28.58, 0.0144705, 28.6, -0.0403986, 28.62, -0.115214,
28.64, -0.159705, 28.66, -0.155236, 28.68, -0.115293, 28.7, -0.0571291,
28.72, -0.0107605, 28.74, 0.012124, 28.76, 0.0109977, 28.78, 0.0283074,
28.8, 0.0429257, 28.82, 0.0373557, 28.84, 0.0335947, 28.86, 0.0414264,
28.88, 0.0541713, 28.9, 0.053536, 28.92, 0.0163121, 28.94, -0.052886,
28.96, -0.132456, 28.98, -0.192357, 29.0, -0.237867, 29.02, -0.27735,
29.04, -0.298441, 29.06, -0.311317, 29.08, -0.33786, 29.1, -0.352876,
29.12, -0.330693, 29.14, -0.310803, 29.16, -0.302706, 29.18, -0.282212,
29.2, -0.247113, 29.22, -0.21076, 29.24, -0.150427, 29.26, -0.0893094,
29.28, -0.0357457, 29.3, 0.0125036, 29.32, 0.0477282, 29.34, 0.0617421,
29.36, 0.0754012, 29.38, 0.108767, 29.4, 0.142573, 29.42, 0.18628,
29.44, 0.216269, 29.46, 0.217215, 29.48, 0.185098, 29.5, 0.15035,
29.52, 0.11332, 29.54, 0.0890269, 29.56, 0.0741685, 29.58, 0.0618652,
29.6, 0.0400042, 29.62, 0.0124511, 29.64, -0.0279066, 29.66, -0.0730995,
29.68, -0.0940972, 29.7, -0.110234, 29.72, -0.111682, 29.74, -0.123135,
29.76, -0.135243, 29.78, -0.150436, 29.8, -0.155134, 29.82, -0.134909,
29.84, -0.118665, 29.86, -0.0897019, 29.88, -0.0596084, 29.9, -0.030215,
29.92, -0.00630639, 29.94, 0.0231023, 29.96, 0.0378836, 29.98, 0.0546884,
30.0, 0.0775272, 30.02, 0.111084, 30.04, 0.137432, 30.06, 0.135349,
30.08, 0.0980347, 30.1, 0.0504347, 30.12, 0.0117351, 30.14, -0.0263502,
30.16, -0.0812805, 30.18, -0.141799, 30.2, -0.179879, 30.22, -0.208229,
30.24, -0.215416, 30.26, -0.204183, 30.28, -0.181348, 30.3, -0.197159,
30.32, -0.2188, 30.34, -0.209884, 30.36, -0.178051, 30.38, -0.126323,
30.4, -0.0533754, 30.42, 0.0122119, 30.44, 0.0373431, 30.46, 0.0492149,
30.48, 0.0616054, 30.5, 0.0619097, 30.52, 0.0502653, 30.54, 0.0410973,
30.56, 0.0309672, 30.58, 0.00984675, 30.6, -0.0017998, 30.62, 0.000902858,
30.64, 0.00970106, 30.66, 5.71496e-05, 30.68, -0.0186795, 30.7, -0.0182207,
30.72, -0.00415068, 30.74, -0.00403225, 30.76, -0.00679234, 30.78, -0.0200761,
30.8, -0.0430782, 30.82, -0.0697687, 30.84, -0.0763734, 30.86, -0.0702635,
30.88, -0.0688612, 30.9, -0.0436265, 30.92, -0.0177102, 30.94, -0.00430213,
30.96, -0.0089226, 30.98, -0.010217, 31.0, -0.0105781, 31.02, -0.0184629,
31.04, -0.0194137, 31.06, -0.0019907, 31.08, 0.0117481, 31.1, 0.0255608,
31.12, 0.0422863, 31.14, 0.0553923, 31.16, 0.0568912, 31.18, 0.0594626,
31.2, 0.0670675, 31.22, 0.0878654, 31.24, 0.128111, 31.26, 0.157086,
31.28, 0.174722, 31.3, 0.180439, 31.32, 0.178848, 31.34, 0.166934,
31.36, 0.146737, 31.38, 0.138109, 31.4, 0.146734, 31.42, 0.151645,
31.44, 0.140671, 31.46, 0.122487, 31.48, 0.0860436, 31.5, 0.0501181,
31.52, 0.0333727, 31.54, 0.0392594, 31.56, 0.0602777, 31.58, 0.083579,
31.6, 0.101583, 31.62, 0.108838, 31.64, 0.113641, 31.66, 0.125091,
31.68, 0.124415, 31.7, 0.11861, 31.72, 0.121286, 31.74, 0.129314,
31.76, 0.137143, 31.78, 0.137602, 31.8, 0.121278, 31.82, 0.0788997,
31.84, 0.0422657, 31.86, 0.00863538, 31.88, -0.0334914, 31.9, -0.0769094,
31.92, -0.113308, 31.94, -0.157794, 31.96, -0.203231, 31.98, -0.244876,
32.0, -0.282399, 32.02, -0.317838, 32.04, -0.339111, 32.06, -0.345443,
32.08, -0.358984, 32.1, -0.35058, 32.12, -0.323715, 32.14, -0.288494,
32.16, -0.267903, 32.18, -0.256788, 32.2, -0.254981, 32.22, -0.238729,
32.24, -0.202395, 32.26, -0.174394, 32.28, -0.150636, 32.3, -0.13453,
32.32, -0.0908551, 32.34, -0.055143, 32.36, -0.0251737, 32.38, 0.000165424,
32.4, 0.0343788, 32.42, 0.0728853, 32.44, 0.103562, 32.46, 0.133989,
32.48, 0.152414, 32.5, 0.158587, 32.52, 0.161276, 32.54, 0.161674,
32.56, 0.166388, 32.58, 0.171863, 32.6, 0.172379, 32.62, 0.181224,
32.64, 0.185078, 32.66, 0.182097, 32.68, 0.175726, 32.7, 0.173605,
32.72, 0.158574, 32.74, 0.143509, 32.76, 0.145275, 32.78, 0.158577,
32.8, 0.17539, 32.82, 0.183478, 32.84, 0.17942, 32.86, 0.155813,
32.88, 0.133373, 32.9, 0.101604, 32.92, 0.0676219, 32.94, 0.031778,
32.96, 0.00578944, 32.98, -0.0137028, 33.0, -0.0207534, 33.02, -0.0200347,
33.04, -0.0237801, 33.06, -0.0183438, 33.08, -0.00765847, 33.1, 0.0170036,
33.12, 0.0303393, 33.14, 0.0490008, 33.16, 0.0708857, 33.18, 0.102767,
33.2, 0.125092, 33.22, 0.136024, 33.24, 0.134106, 33.26, 0.110781,
33.28, 0.0804167, 33.3, 0.0602375, 33.32, 0.0609978, 33.34, 0.0611546,
33.36, 0.057592, 33.38, 0.0500659, 33.4, 0.0480544, 33.42, 0.0649242,
33.44, 0.101086, 33.46, 0.136755, 33.48, 0.163786, 33.5, 0.18043,
33.52, 0.205698, 33.54, 0.225709, 33.56, 0.241168, 33.58, 0.244785,
33.6, 0.242037, 33.62, 0.240993, 33.64, 0.220714, 33.66, 0.193486,
33.68, 0.169927, 33.7, 0.153285, 33.72, 0.130394, 33.74, 0.106777,
33.76, 0.0841553, 33.78, 0.0681512, 33.8, 0.0487574, 33.82, 0.0288442,
33.84, 0.0140417, 33.86, 0.0063277, 33.88, 0.00299086, 33.9, 0.00787042,
33.92, 0.0111707, 33.94, 0.0108267, 33.96, 0.0175065, 33.98, 0.012769,
34.0, -0.0115056, 34.02, -0.046874, 34.04, -0.0686297, 34.06, -0.0849394,
34.08, -0.10138, 34.1, -0.0996336, 34.12, -0.0905843, 34.14, -0.082705,
34.16, -0.0873892, 34.18, -0.0989264, 34.2, -0.119382, 34.22, -0.135871,
34.24, -0.151105, 34.26, -0.171002, 34.28, -0.187195, 34.3, -0.201956,
34.32, -0.223023, 34.34, -0.249656, 34.36, -0.27007, 34.38, -0.289434,
34.4, -0.307888, 34.42, -0.312466, 34.44, -0.315298, 34.46, -0.318863,
34.48, -0.319322, 34.5, -0.321941, 34.52, -0.319508, 34.54, -0.307926,
34.56, -0.288273, 34.58, -0.268458, 34.6, -0.244353, 34.62, -0.215777,
34.64, -0.185616, 34.66, -0.16118, 34.68, -0.147947, 34.7, -0.133705,
34.72, -0.110577, 34.74, -0.0650728, 34.76, -0.0169538, 34.78, 0.035918,
34.8, 0.0841936, 34.82, 0.121873, 34.84, 0.149748, 34.86, 0.165142,
34.88, 0.184561, 34.9, 0.200201, 34.92, 0.205359, 34.94, 0.18723,
34.96, 0.163359, 34.98, 0.138856, 35.0, 0.12017, 35.02, 0.0997893,
35.04, 0.0846333, 35.06, 0.0729506, 35.08, 0.0527033, 35.1, 0.0229337,
35.12, 0.00250342, 35.14, -0.00225138, 35.16, -0.00545465, 35.18, -0.00736109,
35.2, -0.00717113, 35.22, -0.00568949, 35.24, -0.0246716, 35.26, -0.0505937,
35.28, -0.0737428, 35.3, -0.0770554, 35.32, -0.0722552, 35.34, -0.0800185,
35.36, -0.08701, 35.38, -0.101636, 35.4, -0.109923, 35.42, -0.111671,
35.44, -0.104606, 35.46, -0.108441, 35.48, -0.13255, 35.5, -0.169072,
35.52, -0.200473, 35.54, -0.231281, 35.56, -0.254316, 35.58, -0.284789,
35.6, -0.315734, 35.62, -0.335011, 35.64, -0.330213, 35.66, -0.304397,
35.68, -0.258557, 35.7, -0.220744, 35.72, -0.205927, 35.74, -0.181785,
35.76, -0.146329, 35.78, -0.103916, 35.8, -0.0656051, 35.82, -0.026534,
35.84, 0.0142945, 35.86, 0.0560024, 35.88, 0.0930106, 35.9, 0.121418,
35.92, 0.141985, 35.94, 0.157267, 35.96, 0.174503, 35.98, 0.186783,
36.0, 0.19429, 36.02, 0.192842, 36.04, 0.178534, 36.06, 0.152799,
36.08, 0.12318, 36.1, 0.0968947, 36.12, 0.0759612, 36.14, 0.0477121,
36.16, 0.0268723, 36.18, 0.00681029, 36.2, -0.0124899, 36.22, -0.0225608,
36.24, -0.0217087, 36.26, -0.0283796, 36.28, -0.0427678, 36.3, -0.0669488,
36.32, -0.0920856, 36.34, -0.107314, 36.36, -0.101167, 36.38, -0.0877204,
36.4, -0.0673003, 36.42, -0.0377959, 36.44, -0.0128101, 36.46, 0.0135434,
36.48, 0.0411809, 36.5, 0.0661374, 36.52, 0.097168, 36.54, 0.125501,
36.56, 0.138123, 36.58, 0.143486, 36.6, 0.145913, 36.62, 0.132311,
36.64, 0.112888, 36.66, 0.0931906, 36.68, 0.0775964, 36.7, 0.0629751,
36.72, 0.0483933, 36.74, 0.0357589, 36.76, 0.026253, 36.78, 0.0193318,
36.8, 0.00434753, 36.82, -0.0132919, 36.84, -0.0234791, 36.86, -0.0298739,
36.88, -0.0393412, 36.9, -0.0468649, 36.92, -0.0552509, 36.94, -0.0651906,
36.96, -0.0733573, 36.98, -0.0722722, 37.0, -0.0721514, 37.02, -0.0663941,
37.04, -0.0579024, 37.06, -0.0448054, 37.08, -0.028145, 37.1, -0.0107599,
37.12, 0.012112, 37.14, 0.0145905, 37.16, 0.0182693, 37.18, 0.0206606,
37.2, 0.0332723, 37.22, 0.0569896, 37.24, 0.0721633, 37.26, 0.0879336,
37.28, 0.094017, 37.3, 0.102749, 37.32, 0.106368, 37.34, 0.11189,
37.36, 0.130578, 37.38, 0.175895, 37.4, 0.221637, 37.42, 0.259888,
37.44, 0.294627, 37.46, 0.334061, 37.48, 0.367879, 37.5, 0.389476,
37.52, 0.406838, 37.54, 0.411428, 37.56, 0.408768, 37.58, 0.387668,
37.6, 0.366371, 37.62, 0.336769, 37.64, 0.297147, 37.66, 0.253524,
37.68, 0.22676, 37.7, 0.200807, 37.72, 0.173178, 37.74, 0.140878,
37.76, 0.119137, 37.78, 0.0967148, 37.8, 0.073695, 37.82, 0.0547653,
37.84, 0.0420162, 37.86, 0.0337719, 37.88, 0.015733, 37.9, 0.000732902,
37.92, -0.0183284, 37.94, -0.039343, 37.96, -0.0611844, 37.98, -0.0952259,
38.0, -0.129141, 38.02, -0.16122, 38.04, -0.181858, 38.06, -0.188752,
38.08, -0.175204, 38.1, -0.151174, 38.12, -0.135155, 38.14, -0.131901,
38.16, -0.129567, 38.18, -0.127131, 38.2, -0.113023, 38.22, -0.0888258,
38.24, -0.069105, 38.26, -0.0587121, 38.28, -0.0638346, 38.3, -0.0706861,
38.32, -0.0779505, 38.34, -0.0776206, 38.36, -0.0804857, 38.38, -0.0959953,
38.4, -0.120549, 38.42, -0.130106, 38.44, -0.124821, 38.46, -0.110038,
38.48, -0.109745, 38.5, -0.106033, 38.52, -0.0932668, 38.54, -0.073321,
38.56, -0.0562622, 38.58, -0.0601994, 38.6, -0.0661166, 38.62, -0.0831057,
38.64, -0.0985364, 38.66, -0.110297, 38.68, -0.112951, 38.7, -0.12239,
38.72, -0.123664, 38.74, -0.115623, 38.76, -0.10315, 38.78, -0.102069,
38.8, -0.112304, 38.82, -0.121432, 38.84, -0.122618, 38.86, -0.114614,
38.88, -0.104903, 38.9, -0.0963185, 38.92, -0.0943551, 38.94, -0.0905769,
38.96, -0.0885172, 38.98, -0.0847901, 39.0, -0.0782387, 39.02, -0.0589715,
39.04, -0.0417165, 39.06, -0.0207037, 39.08, 0.019739, 39.1, 0.0581696,
39.12, 0.0823063, 39.14, 0.104772, 39.16, 0.135323, 39.18, 0.164738,
39.2, 0.196903, 39.22, 0.219096, 39.24, 0.220958, 39.26, 0.207118,
39.28, 0.212488, 39.3, 0.210518, 39.32, 0.203017, 39.34, 0.190967,
39.36, 0.176637, 39.38, 0.168416, 39.4, 0.164885, 39.42, 0.170432,
39.44, 0.167002, 39.46, 0.1591, 39.48, 0.156108, 39.5, 0.158942,
39.52, 0.156459, 39.54, 0.159987, 39.56, 0.171115, 39.58, 0.181591,
39.6, 0.196167, 39.62, 0.19619, 39.64, 0.187318, 39.66, 0.159937,
39.68, 0.122613, 39.7, 0.0848896, 39.72, 0.0576924, 39.74, 0.0359015,
39.76, 0.0105113, 39.78, -0.012859, 39.8, -0.0289872, 39.82, -0.0466541,
39.84, -0.0663115, 39.86, -0.0828223, 39.88, -0.0889317, 39.9, -0.101848,
39.92, -0.0992651, 39.94, -0.0966539, 39.96, -0.113137, 39.98, -0.126052,
40.0, -0.132867, 40.02, -0.133802, 40.04, -0.13743, 40.06, -0.140222,
40.08, -0.136303, 40.1, -0.124048, 40.12, -0.115929, 40.14, -0.111682,
40.16, -0.103049, 40.18, -0.0873, 40.2, -0.0608681, 40.22, -0.0363683,
40.24, -0.0155847, 40.26, -0.00446732, 40.28, -0.0087389, 40.3, -0.0263603,
40.32, -0.0496446, 40.34, -0.0663169, 40.36, -0.0867265, 40.38, -0.107832,
40.4, -0.126118, 40.42, -0.149339, 40.44, -0.16741, 40.46, -0.176239,
40.48, -0.182016, 40.5, -0.192727, 40.52, -0.204142, 40.54, -0.217613,
40.56, -0.228648, 40.58, -0.232799, 40.6, -0.224908, 40.62, -0.216691,
40.64, -0.213305, 40.66, -0.220051, 40.68, -0.223227, 40.7, -0.219111,
40.72, -0.212162, 40.74, -0.214994, 40.76, -0.212239, 40.78, -0.19718,
40.8, -0.16259, 40.82, -0.127924, 40.84, -0.0934896, 40.86, -0.063756,
40.88, -0.0266634, 40.9, 0.0197302, 40.92, 0.0574115, 40.94, 0.0847975,
40.96, 0.110593, 40.98, 0.134026, 41.0, 0.157371, 41.02, 0.17443,
41.04, 0.181185, 41.06, 0.182213, 41.08, 0.176572, 41.1, 0.172514,
41.12, 0.162881, 41.14, 0.152752, 41.16, 0.137925, 41.18, 0.121394,
41.2, 0.103914, 41.22, 0.0751076, 41.24, 0.0381805, 41.26, 0.00550423,
41.28, -0.028551, 41.3, -0.0627034, 41.32, -0.0954392, 41.34, -0.124951,
41.36, -0.146831, 41.38, -0.156078, 41.4, -0.161407, 41.42, -0.164786,
41.44, -0.164401, 41.46, -0.152044, 41.48, -0.136231, 41.5, -0.114381,
41.52, -0.100034, 41.54, -0.0842092, 41.56, -0.0807235, 41.58, -0.0708735,
41.6, -0.0599813, 41.62, -0.0415582, 41.64, -0.0312861, 41.66, -0.0289362,
41.68, -0.0241855, 41.7, -0.0107676, 41.72, -0.00316858, 41.74, 0.00398391,
41.76, 0.00879361, 41.78, 0.0131542, 41.8, 0.0253042, 41.82, 0.04208,
41.84, 0.0680554, 41.86, 0.088008, 41.88, 0.102299, 41.9, 0.110057,
41.92, 0.12032, 41.94, 0.139605, 41.96, 0.154112, 41.98, 0.157743,
42.0, 0.15569, 42.02, 0.165018, 42.04, 0.170746, 42.06, 0.166493,
42.08, 0.151002, 42.1, 0.142566, 42.12, 0.137176, 42.14, 0.131322,
42.16, 0.117194, 42.18, 0.103038, 42.2, 0.0826023, 42.22, 0.0681201,
42.24, 0.0597062, 42.26, 0.0548133, 42.28, 0.0517991, 42.3, 0.0408398,
42.32, 0.029859, 42.34, 0.0157729, 42.36, 0.0165523, 42.38, 0.0174531,
42.4, 0.0248223, 42.42, 0.0312939, 42.44, 0.0408241, 42.46, 0.0496067,
42.48, 0.0606566, 42.5, 0.0740827, 42.52, 0.0970056, 42.54, 0.120456,
42.56, 0.140448, 42.58, 0.164712, 42.6, 0.175855, 42.62, 0.1902,
42.64, 0.210296, 42.66, 0.230383, 42.68, 0.245298, 42.7, 0.258454,
42.72, 0.265847, 42.74, 0.26789, 42.76, 0.273107, 42.78, 0.263742,
42.8, 0.23875, 42.82, 0.208253, 42.84, 0.191211, 42.86, 0.166501,
42.88, 0.14207, 42.9, 0.108863, 42.92, 0.087351, 42.94, 0.0681874,
42.96, 0.0479673, 42.98, 0.0264879, 43.0, -0.00185541, 43.02, -0.0292491,
43.04, -0.0491857, 43.06, -0.0654034, 43.08, -0.0812338, 43.1, -0.0957307,
43.12, -0.116998, 43.14, -0.135819, 43.16, -0.146691, 43.18, -0.149692,
43.2, -0.152944, 43.22, -0.16101, 43.24, -0.176485, 43.26, -0.193415,
43.28, -0.208879, 43.3, -0.218833, 43.32, -0.228251, 43.34, -0.241927,
43.36, -0.254348, 43.38, -0.264233, 43.4, -0.267965, 43.42, -0.268791,
43.44, -0.27042, 43.46, -0.263785, 43.48, -0.25234, 43.5, -0.237525,
43.52, -0.226873, 43.54, -0.216623, 43.56, -0.196656, 43.58, -0.178174,
43.6, -0.159902, 43.62, -0.13503, 43.64, -0.109284, 43.66, -0.082238,
43.68, -0.064848, 43.7, -0.0457431, 43.72, -0.0235606, 43.74, -0.00939563,
43.76, -0.0130979, 43.78, -0.0131563, 43.8, -0.0105276, 43.82, 0.00706837,
43.84, 0.0230045, 43.86, 0.0414532, 43.88, 0.0589169, 43.9, 0.0724983,
43.92, 0.0893022, 43.94, 0.0997517, 43.96, 0.114042, 43.98, 0.128688,
44.0, 0.142552, 44.02, 0.167614, 44.04, 0.193367, 44.06, 0.213998,
44.08, 0.224998, 44.1, 0.229273, 44.12, 0.225203, 44.14, 0.221841,
44.16, 0.216796, 44.18, 0.204083, 44.2, 0.186828, 44.22, 0.165805,
44.24, 0.139954, 44.26, 0.118247, 44.28, 0.0960074, 44.3, 0.0793893,
44.32, 0.058126, 44.34, 0.0324762, 44.36, 0.0124738, 44.38, -0.000185438,
44.4, -0.0127051, 44.42, -0.0256984, 44.44, -0.0345422, 44.46, -0.0558248,
44.48, -0.0698918, 44.5, -0.0812575, 44.52, -0.0994373, 44.54, -0.11526,
44.56, -0.129472, 44.58, -0.147619, 44.6, -0.167233, 44.62, -0.178056,
44.64, -0.186931, 44.66, -0.19374, 44.68, -0.198346, 44.7, -0.193151,
44.72, -0.190504, 44.74, -0.185109, 44.76, -0.178397, 44.78, -0.159521,
44.8, -0.135767, 44.82, -0.114715, 44.84, -0.100523, 44.86, -0.0906404,
44.88, -0.0825677, 44.9, -0.0740197, 44.92, -0.063133, 44.94, -0.0642681,
44.96, -0.0724699, 44.98, -0.0877706, 45.0, -0.10009, 45.02, -0.105881,
45.04, -0.116792, 45.06, -0.131118, 45.08, -0.14644, 45.1, -0.149938,
45.12, -0.140197, 45.14, -0.120281, 45.16, -0.102062, 45.18, -0.0821225,
45.2, -0.0628424, 45.22, -0.0336853, 45.24, 0.0040452, 45.26, 0.0441869,
45.28, 0.0758093, 45.3, 0.101395, 45.32, 0.102446, 45.34, 0.110615,
45.36, 0.115083, 45.38, 0.116235, 45.4, 0.111361, 45.42, 0.10114,
45.44, 0.0975694, 45.46, 0.0827365, 45.48, 0.0704041, 45.5, 0.0530257,
45.52, 0.0391886, 45.54, 0.0282864, 45.56, 0.026495, 45.58, 0.0179388,
45.6, 0.00340022, 45.62, -0.0119136, 45.64, -0.0137608, 45.66, -0.0120318,
45.68, -0.0181459, 45.7, -0.016593, 45.72, -0.0168931, 45.74, -0.0249679,
45.76, -0.0356736, 45.78, -0.0434026, 45.8, -0.0386635, 45.82, -0.0367952,
45.84, -0.0352403, 45.86, -0.0350277, 45.88, -0.0347943, 45.9, -0.0306846,
45.92, -0.0280751, 45.94, -0.0270779, 45.96, -0.0336295, 45.98, -0.0393377,
46.0, -0.0368941, 46.02, -0.0381896, 46.04, -0.0417761, 46.06, -0.0577387,
46.08, -0.0781778, 46.1, -0.0961805, 46.12, -0.10041, 46.14, -0.0955124,
46.16, -0.0881758, 46.18, -0.0708013, 46.2, -0.0515276, 46.22, -0.027705,
46.24, -0.00160303, 46.26, 0.0294514, 46.28, 0.0631477, 46.3, 0.0996609,
46.32, 0.1361, 46.34, 0.168238, 46.36, 0.199249, 46.38, 0.231338,
46.4, 0.258336, 46.42, 0.280682, 46.44, 0.298069, 46.46, 0.308573,
46.48, 0.320719, 46.5, 0.334883, 46.52, 0.341959, 46.54, 0.336811,
46.56, 0.330138, 46.58, 0.317964, 46.6, 0.301864, 46.62, 0.275385,
46.64, 0.247991, 46.66, 0.222309, 46.68, 0.200739, 46.7, 0.179399,
46.72, 0.156166, 46.74, 0.136514, 46.76, 0.115784, 46.78, 0.0921281,
46.8, 0.0638663, 46.82, 0.0429565, 46.84, 0.0256509, 46.86, 0.00932126,
46.88, -0.00851816, 46.9, -0.01936, 46.92, -0.0340511, 46.94, -0.0492312,
46.96, -0.0607969, 46.98, -0.0704649, 47.0, -0.0656682, 47.02, -0.0617462,
47.04, -0.0569799, 47.06, -0.0493497, 47.08, -0.0390593, 47.1, -0.0235474,
47.12, -0.0102417, 47.14, -0.000145587, 47.16, 0.0149285, 47.18, 0.0322438,
47.2, 0.0549515, 47.22, 0.0834695, 47.24, 0.106852, 47.26, 0.117633,
47.28, 0.123942, 47.3, 0.130346, 47.32, 0.13015, 47.34, 0.120688,
47.36, 0.0968329, 47.38, 0.0665012, 47.4, 0.0386514, 47.42, 0.0192359,
47.44, -0.00787992, 47.46, -0.0310488, 47.48, -0.0502, 47.5, -0.0682209,
47.52, -0.0843936, 47.54, -0.0968315, 47.56, -0.110555, 47.58, -0.12934,
47.6, -0.145515, 47.62, -0.166669, 47.64, -0.184411, 47.66, -0.206385,
47.68, -0.225258, 47.7, -0.2463, 47.72, -0.259844, 47.74, -0.268622,
47.76, -0.267488, 47.78, -0.273481, 47.8, -0.277643, 47.82, -0.283885,
47.84, -0.287659, 47.86, -0.288238, 47.88, -0.288081, 47.9, -0.277262,
47.92, -0.268416, 47.94, -0.259329, 47.96, -0.251746, 47.98, -0.243521,
48.0, -0.240366, 48.02, -0.238057, 48.04, -0.231646, 48.06, -0.219619,
48.08, -0.198012, 48.1, -0.167908, 48.12, -0.135842, 48.14, -0.105518,
48.16, -0.0705824, 48.18, -0.032404, 48.2, 0.0135795, 48.22, 0.0645652,
48.24, 0.115138, 48.26, 0.165799, 48.28, 0.219821, 48.3, 0.271793,
48.32, 0.319584, 48.34, 0.361795, 48.36, 0.389814, 48.38, 0.411869,
48.4, 0.425584, 48.42, 0.431188, 48.44, 0.423702, 48.46, 0.413405,
48.48, 0.402873, 48.5, 0.390169, 48.52, 0.379092, 48.54, 0.358909,
48.56, 0.340013, 48.58, 0.3156, 48.6, 0.284989, 48.62, 0.244636,
48.64, 0.211355, 48.66, 0.179243, 48.68, 0.142846, 48.7, 0.107095,
48.72, 0.07613, 48.74, 0.0374143, 48.76, 0.00111987, 48.78, -0.0312388,
48.8, -0.0569868, 48.82, -0.0827716, 48.84, -0.102869, 48.86, -0.13222,
48.88, -0.162425, 48.9, -0.18929, 48.92, -0.211799, 48.94, -0.227226,
48.96, -0.238179, 48.98, -0.243958, 49.0, -0.250571, 49.02, -0.254376,
49.04, -0.261143, 49.06, -0.270509, 49.08, -0.276614, 49.1, -0.281817,
49.12, -0.279695, 49.14, -0.285402, 49.16, -0.289784, 49.18, -0.286826,
49.2, -0.278102, 49.22, -0.26473, 49.24, -0.244326, 49.26, -0.228024,
49.28, -0.215493, 49.3, -0.200451, 49.32, -0.185678, 49.34, -0.163687,
49.36, -0.144122, 49.38, -0.11766, 49.4, -0.10031, 49.42, -0.0891439,
49.44, -0.0775003, 49.46, -0.0625952, 49.48, -0.0554351, 49.5, -0.0515343,
49.52, -0.0534974, 49.54, -0.0510609, 49.56, -0.0468647, 49.58, -0.0435826,
49.6, -0.0439178, 49.62, -0.0515619, 49.64, -0.0573561, 49.66, -0.0638859,
49.68, -0.0658413, 49.7, -0.0744166, 49.72, -0.0794318, 49.74, -0.0805038,
49.76, -0.07958, 49.78, -0.0803191, 49.8, -0.0811406, 49.82, -0.0853884,
49.84, -0.0844476, 49.86, -0.0869371, 49.88, -0.0857142, 49.9, -0.0897116,
49.92, -0.0969328, 49.94, -0.101339, 49.96, -0.0979545, 49.98, -0.0969695,
50.0, -0.0922048, 50.02, -0.08652, 50.04, -0.0764437, 50.06, -0.060834,
50.08, -0.0473336, 50.1, -0.0226964, 50.12, 0.00104663, 50.14, 0.0243084,
50.16, 0.0499782, 50.18, 0.0659518, 50.2, 0.0842848, 50.22, 0.108368,
50.24, 0.137447, 50.26, 0.155239, 50.28, 0.179261, 50.3, 0.202375,
50.32, 0.224814, 50.34, 0.243064, 50.36, 0.262622, 50.38, 0.28014,
50.4, 0.294274, 50.42, 0.313653, 50.44, 0.332393, 50.46, 0.338882,
50.48, 0.345127, 50.5, 0.351769, 50.52, 0.355013, 50.54, 0.360364,
50.56, 0.354018, 50.58, 0.353616, 50.6, 0.346638, 50.62, 0.343945,
50.64, 0.331634, 50.66, 0.322998, 50.68, 0.31084, 50.7, 0.296834,
50.72, 0.283941, 50.74, 0.268932, 50.76, 0.259008, 50.78, 0.238458,
50.8, 0.219637, 50.82, 0.200909, 50.84, 0.18728, 50.86, 0.178557,
50.88, 0.173933, 50.9, 0.166415, 50.92, 0.160032, 50.94, 0.149871,
50.96, 0.136401, 50.98, 0.123457, 51.0, 0.112139, 51.02, 0.0954569,
51.04, 0.0801882, 51.06, 0.0555041, 51.08, 0.0340334, 51.1, 0.0123024,
51.12, -0.00125575, 51.14, -0.0179176, 51.16, -0.0365104, 51.18, -0.0570633,
51.2, -0.0734401, 51.22, -0.086694, 51.24, -0.094628, 51.26, -0.0998059,
51.28, -0.100004, 51.3, -0.0974903, 51.32, -0.0940466, 51.34, -0.0879302,
51.36, -0.089489, 51.38, -0.088301, 51.4, -0.0921395, 51.42, -0.0896674,
51.44, -0.0882413, 51.46, -0.0910959, 51.48, -0.10045, 51.5, -0.10742,
51.52, -0.119772, 51.54, -0.129405, 51.56, -0.140647, 51.58, -0.154142,
51.6, -0.17145, 51.62, -0.186802, 51.64, -0.196673, 51.66, -0.205835,
51.68, -0.216065, 51.7, -0.22608, 51.72, -0.237978, 51.74, -0.249838,
51.76, -0.254473, 51.78, -0.257947, 51.8, -0.25365, 51.82, -0.249697,
51.84, -0.237104, 51.86, -0.226535, 51.88, -0.213134, 51.9, -0.203708,
51.92, -0.192416, 51.94, -0.181351, 51.96, -0.163082, 51.98, -0.14403,
52.0, -0.134086, 52.02, -0.120371, 52.04, -0.116613, 52.06, -0.110947,
52.08, -0.108624, 52.1, -0.102385, 52.12, -0.100811, 52.14, -0.0961633,
52.16, -0.0903022, 52.18, -0.0853427, 52.2, -0.0818258, 52.22, -0.0800427,
52.24, -0.0778282, 52.26, -0.0754209, 52.28, -0.073137, 52.3, -0.0746226,
52.32, -0.0685506, 52.34, -0.063551, 52.36, -0.0536025, 52.38, -0.0429239,
52.4, -0.0285926, 52.42, -0.0113613, 52.44, 0.0103332, 52.46, 0.0279683,
52.48, 0.0496113, 52.5, 0.0642243, 52.52, 0.0787807, 52.54, 0.0951087,
52.56, 0.102564, 52.58, 0.112081, 52.6, 0.118806, 52.62, 0.133103,
52.64, 0.149694, 52.66, 0.161012, 52.68, 0.168742, 52.7, 0.17358,
52.72, 0.172276, 52.74, 0.172637, 52.76, 0.17134, 52.78, 0.165492,
52.8, 0.156214, 52.82, 0.143844, 52.84, 0.131308, 52.86, 0.118668,
52.88, 0.106264, 52.9, 0.0959339, 52.92, 0.0834188, 52.94, 0.0664515,
52.96, 0.0525006, 52.98, 0.0406679, 53.0, 0.0223792, 53.02, 0.00733548,
53.04, -0.0155505, 53.06, -0.0400597, 53.08, -0.067746, 53.1, -0.0891702,
53.12, -0.110352, 53.14, -0.128432, 53.16, -0.152395, 53.18, -0.173002,
53.2, -0.189864, 53.22, -0.203303, 53.24, -0.212956, 53.26, -0.219825,
53.28, -0.221625, 53.3, -0.217337, 53.32, -0.212503, 53.34, -0.207587,
53.36, -0.19896, 53.38, -0.18663, 53.4, -0.167295, 53.42, -0.148782,
53.44, -0.130042, 53.46, -0.118496, 53.48, -0.0995799, 53.5, -0.0858748,
53.52, -0.0746772, 53.54, -0.0605877, 53.56, -0.0478663, 53.58, -0.034599,
53.6, -0.0260815, 53.62, -0.0179323, 53.64, -0.018575, 53.66, -0.0195949,
53.68, -0.0178976, 53.7, -0.0132321, 53.72, -0.0152231, 53.74, -0.0190812,
53.76, -0.022983, 53.78, -0.0273134, 53.8, -0.0300587, 53.82, -0.0318798,
53.84, -0.0353033, 53.86, -0.0411166, 53.88, -0.0415555, 53.9, -0.0441483,
53.92, -0.0319796, 53.94, -0.0245182, 53.96, -0.0135545, 53.98, -0.00749258,
54.0, -0.0016186, 54.02, 0.00445032, 54.04, 0.0160014, 54.06, 0.0189276,
54.08, 0.0287208, 54.1, 0.0348233, 54.12, 0.0378897, 54.14, 0.0425459,
54.16, 0.0436968, 54.18, 0.0409963, 54.2, 0.0362217, 54.22, 0.0333912,
54.24, 0.0312451, 54.26, 0.0301663, 54.28, 0.0276097, 54.3, 0.030943,
54.32, 0.035367, 54.34, 0.0448642, 54.36, 0.0530158, 54.38, 0.0571669,
54.4, 0.0693671, 54.42, 0.0728859, 54.44, 0.0821062, 54.46, 0.0933054,
54.48, 0.105305, 54.5, 0.110908, 54.52, 0.120089, 54.54, 0.126361,
54.56, 0.133017, 54.58, 0.138657, 54.6, 0.143327, 54.62, 0.148925,
54.64, 0.155342, 54.66, 0.16885, 54.68, 0.183007, 54.7, 0.199472,
54.72, 0.210597, 54.74, 0.228821, 54.76, 0.237605, 54.78, 0.245526,
54.8, 0.250809, 54.82, 0.257524, 54.84, 0.257005, 54.86, 0.257125,
54.88, 0.257774, 54.9, 0.247984, 54.92, 0.243787, 54.94, 0.235549,
54.96, 0.226164, 54.98, 0.216706, 55.0, 0.209456, 55.02, 0.19976,
55.04, 0.186856, 55.06, 0.17912, 55.08, 0.170883, 55.1, 0.162881,
55.12, 0.155649, 55.14, 0.150246, 55.16, 0.147114, 55.18, 0.147866,
55.2, 0.145138, 55.22, 0.139108, 55.24, 0.13536, 55.26, 0.133312,
55.28, 0.122604, 55.3, 0.110505, 55.32, 0.101252, 55.34, 0.0952119,
55.36, 0.0921465, 55.38, 0.0914031, 55.4, 0.0925453, 55.42, 0.0923844,
55.44, 0.0909047, 55.46, 0.0891787, 55.48, 0.0853381, 55.5, 0.0803417,
55.52, 0.074151, 55.54, 0.067003, 55.56, 0.0597654, 55.58, 0.057561,
55.6, 0.0567374, 55.62, 0.0541084, 55.64, 0.0500366, 55.66, 0.0392165,
55.68, 0.0285185, 55.7, 0.0226356, 55.72, 0.0198196, 55.74, 0.0157956,
55.76, 0.00829442, 55.78, 0.00884946, 55.8, 0.00801286, 55.82, 0.00550458,
55.84, -0.000176955, 55.86, -0.002942, 55.88, -0.00754138, 55.9, -0.0131194,
55.92, -0.0190704, 55.94, -0.0318165, 55.96, -0.0439291, 55.98, -0.0547707,
56.0, -0.0617552, 56.02, -0.0692437, 56.04, -0.0765088, 56.06, -0.0881168,
56.08, -0.097465, 56.1, -0.110084, 56.12, -0.118535, 56.14, -0.130087,
56.16, -0.145459, 56.18, -0.159324, 56.2, -0.175117, 56.22, -0.188606,
56.24, -0.206829, 56.26, -0.21818, 56.28, -0.229226, 56.3, -0.238268,
56.32, -0.251537, 56.34, -0.256998, 56.36, -0.268129, 56.38, -0.27668,
56.4, -0.284165, 56.42, -0.292528, 56.44, -0.29833, 56.46, -0.301654,
56.48, -0.303339, 56.5, -0.302923, 56.52, -0.304313, 56.54, -0.303133,
56.56, -0.299108, 56.58, -0.298187, 56.6, -0.294272, 56.62, -0.286466,
56.64, -0.275936, 56.66, -0.265029, 56.68, -0.255753, 56.7, -0.247926,
56.72, -0.242719, 56.74, -0.236014, 56.76, -0.226095, 56.78, -0.214712,
56.8, -0.202267, 56.82, -0.18921, 56.84, -0.179707, 56.86, -0.16635,
56.88, -0.159055, 56.9, -0.145541, 56.92, -0.135277, 56.94, -0.120518,
56.96, -0.105552, 56.98, -0.09522, 57.0, -0.0807986, 57.02, -0.0637626,
57.04, -0.0483875, 57.06, -0.03018, 57.08, -0.0171255, 57.1, -0.00249433,
57.12, 0.0137637, 57.14, 0.0326401, 57.16, 0.0437081, 57.18, 0.0486608,
57.2, 0.0517946, 57.22, 0.0518355, 57.24, 0.0498557, 57.26, 0.045692,
57.28, 0.0420708, 57.3, 0.0346285, 57.32, 0.0278142, 57.34, 0.0254155,
57.36, 0.0220803, 57.38, 0.0227009, 57.4, 0.0223398, 57.42, 0.0218035,
57.44, 0.0306492, 57.46, 0.0338614, 57.48, 0.0372163, 57.5, 0.0398021,
57.52, 0.0388764, 57.54, 0.0383216, 57.56, 0.0386145, 57.58, 0.0390382,
57.6, 0.0405221, 57.62, 0.0418935, 57.64, 0.0467439, 57.66, 0.0492422,
57.68, 0.0540898, 57.7, 0.0575195, 57.72, 0.0635494, 57.74, 0.0672768,
57.76, 0.0702577, 57.78, 0.0729716, 57.8, 0.0727847, 57.82, 0.0742112,
57.84, 0.0649396, 57.86, 0.0565123, 57.88, 0.0427127, 57.9, 0.0316902,
57.92, 0.0234888, 57.94, 0.0127255, 57.96, 0.00116472, 57.98, -0.0105186,
58.0, -0.0187181]
GFE.Pre.amplitude.amp_mgr().add(obj)

# ============== 地震场地反应 =================
obj = GFE.Pre.vibration.vibra_load()
obj.name = 'VibLoad-1'
obj.amp_bottom_x = "KOBE_JAPAN_1-16-1995_MORIGAWACHI_x"
obj.amp_bottom_y = ''
obj.amp_bottom_z = ''
obj.pwave_dir = 2
obj.soil = 'Soil1D-1'
obj.is_outcrop = True
obj.input_loc = -1
obj.level = 0
obj.set_parameter('DampConvOrder', '1')
obj.set_parameter('DampScale', '1')
obj.set_parameter('MaxIter', '100')
obj.set_parameter('N', '4096')
obj.set_parameter('Rr', '0.5')
obj.set_parameter('SubLayerHeight', '1')
obj.set_parameter('TimeInterval', '0.02')
obj.set_parameter('Tol', '1e-2')
obj.set_parameter('UI_ARBot', '')
obj.set_parameter('UI_ARTop', '')
obj.set_parameter('UI_Method', '0')
obj.set_parameter('UseAmp', 'true')
obj.set_parameter('UseEERAMat', 'true')
obj.set_parameter('UseIntgOutp', 'true')
GFE.Pre.vibration.vib_mgr().add(obj)

# ============= 动力场输出 ==============
obj = GFE.Pre.output.output_request()
obj.name = 'FO-DynaEla-All'
obj.step = ''
obj.type = 0
obj.method = 0
obj.time_type = 0
obj.time_interval = 0.1
obj.number_interval = 0
obj.frequency = 0
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


# =============== 动力分析步 ===============
obj = GFE.Pre.step.dynamic_explicit_step()
obj.name = 'Dyna-1'
obj.description = ''
obj.nlgeom = False
obj.period = step_total_time
obj_ms1 = GFE.Pre.step.mass_scaling()
obj_ms1.region = '*'
obj_ms1.type = 1
obj_ms1.frequency = 100
obj_ms1.target_time = step_target_time
obj.mass_scaling = [obj_ms1]
GFE.Pre.step.step_mgr().add(obj)

# ============ 动力工况 ===============
obj = GFE.Pre.case.case()
obj.name = 'dyna'
obj.steps = ['Initial', 'Dyna-1']
obj.bcs['Dyna-1'] = []
obj.bcs['Initial'] = []
obj.initialConditions['Initial'] = []
obj.vload['Dyna-1'] = ['VibLoad-1']
obj.artbc['Dyna-1'] = ['ArtBC-1']
obj.fieldReqs['Dyna-1'] = ['FO-DynaEla-All']
obj.histReqs['Dyna-1'] = []
obj.elemAdd['Dyna-1'] = []
obj.elemDel['Dyna-1'] = []
GFE.Pre.case.case_mgr().add(obj)


# ================ 作业管理器 =================
# 写出inp文件
from GFE.io import inpio
inpwriter = inpio.writer(inp_path_static)
inpwriter.set_case('static')
inpwriter.perform()

inpwriter = inpio.writer(inp_path_model)
inpwriter.set_case('model')
inpwriter.perform()

inpwriter = inpio.writer(inp_path_dyna)
inpwriter.set_case('dyna')
inpwriter.perform()


```
