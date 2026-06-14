# GFE2026-CM-ch04-CM4-update2
> 来源：E:\GFE2026\典型案例与教程\第4章 核电站土-结构动力分析案例\CM4-update2.py（GFE2026 官方典型案例命令流，v3.x 代际金标准）。raw 不可变源副本，2026-06-11 入库。

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
plugin_dir2 = os.path.join(plugin_dir, "第4章")
gmat_path = os.path.join(plugin_dir2, "nol-soil.gmat")
inp_path = os.path.join(plugin_dir2, "CM4-Case-Dyna.inp")
# 转为绝对路径
gmat_path = os.path.abspath(gmat_path)
inp_path = os.path.abspath(inp_path)

print(inp_path)


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
# 土体材料（需通过gmat文件导入）
soil_material_path = gmat_path
soil_materials = ['sutiantu','lizhinianxingtu','quanfenghuahuagangyan','qiangfenghuahuagangyan']
soil_depth = [2.42, 32.4, 4.0, 23.8]		# 各土层厚度
plant_basement_depth = 16.0		# 工厂地下室深度
soil_length = 300 				# 土体长度
soil_width = 300				# 土体宽度
soil_mesh = 8.0				# 土体网格尺寸

# 7. 分析步
step_total_time = 20.0			# 显式动力分析步总时长
step_target_time = 5e-05		# 分析步目标时间增量


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


# =============== 导入土体材料 ==================
import GFE.io
io_instance = GFE.io.get_current()
io_instance.import_mat(soil_material_path)

# =============== 创建一维土层 ==============
obj = GFE.Pre.soil.soil()
obj.name = 'Soil1D-1'
obj.depth = soil_depth
obj.materials = soil_materials
obj.bedrock_mat = soil_materials[-1]
obj.depth_dir = 2
GFE.Pre.soil.soil_mgr().add(obj)

# ============= 拉伸底板-创建地下室 ============
builder = GFE.geometry.geoprim.builder()
shapes = [GFE.Pre.geometry.geo_mgr().find('raft').shape()]
extruded = builder.extrude(shapes, [0.0, 0.0, plant_basement_depth])
mgr = Pre.geometry.geo_mgr()
for sp in extruded :
    if not sp.is_null() :
        mgr.add('plant-basement', sp)

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


# ============= 平移与裁剪土体 ==============
# 查找土体和地下室的形心，计算向量差
soil_geo = GFE.Pre.geometry.geo_mgr().find('Soil-1')
max_z = -1e10
top_face = None
for f in GFE.geometry.geotool.children(soil_geo.shape(), 4):
    fz = GFE.geometry.geotool.centre_of_mass(f)[2]
    if fz > max_z:
        max_z = fz
        top_face = f
center1 = GFE.geometry.geotool.centre_of_mass(top_face)
# 地下室形心
center2 = [0.0, 0.0, plant_basement_depth]
# 计算向量差
trsf_vec = [center2[i] - center1[i] for i in range(3)]
# 平移土体
builder = GFE.geometry.geoprim.builder()
builder.translate(['Soil-1'], trsf_vec, False)

# 裁剪土体
builder = GFE.geometry.geoprim.builder()
builder.cut('Soil-1', ['plant-basement'], True)


# ============== 相互作用-土体与核电站 =============
# 找到接触対
search_list = []
search_list.append(['Soil-1', 'plant'])
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

# 创建绑定约束
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

# ============= 创建土体四周和底面表面集（创建人工边界） =================
# 1. 边界条件设置（人工边界）
from GFE.Pre.geometry import geo_mgr
from GFE.Pre.set import gset_mgr

geo_obj = geo_mgr().find('Soil-1')
if not geo_obj:
    raise ValueError("未找到几何体'Soil-1'！")
shape = geo_obj.shape()

# 获取包围盒
box_range = geotool.get_shape_box_range(shape, 0.0)
x_min, y_min, z_min, x_max, y_max, z_max = box_range
# 容差设置
tolerance = 1
# 边界信息配置
boundary_info = {
    "front": {"gset_name": "front_boundary", "axis": 1, "extreme": y_min},
    "back": {"gset_name": "back_boundary", "axis": 1, "extreme": y_max},
    "left": {"gset_name": "left_boundary", "axis": 0, "extreme": x_min},
    "right": {"gset_name": "right_boundary", "axis": 0, "extreme": x_max},
    "bottom": {"gset_name": "bottom_boundary", "axis": 2, "extreme": z_min}
}
# 存储所有转换后的ID
all_converted_ids = {}

# 2. 核心函数
def get_face_centroid(face):
    """获取面的质心坐标"""
    return geotool.centre_of_mass(face)

def judge_boundary_by_centroid(centroid):
    """通过质心判断边界类型"""
    for btype, info in boundary_info.items():
        if abs(centroid[info["axis"]] - info["extreme"]) < tolerance:
            return btype
    return None

def get_and_convert_ids(gset_name):
    """从几何集中获取ID并转换格式为[[x,y,0], ...]"""
    gset = gset_mgr().find(gset_name)
    if not gset:
        return []
    # 直接使用get_shapes_id()获取原始ID（修正关键处）
    original_ids = gset.get_shapes_id()
    # 转换格式：保留前两个元素，第三个元素改为0
    converted_ids = [[id_tuple[0], id_tuple[2], 0] for id_tuple in original_ids]
    return converted_ids


# 3. 筛选边界并添加到几何集
boundary_faces = {btype: [] for btype in boundary_info.keys()}
# 筛选外边界面
for face in geotool.children(shape, 4):
    centroid = get_face_centroid(face)
    btype = judge_boundary_by_centroid(centroid)
    if btype:
        boundary_faces[btype].append(face)
# 添加到几何集并处理ID
for btype, faces in boundary_faces.items():
    info = boundary_info[btype]
    gset_name = info["gset_name"]

    if faces:
        # 先清空已存在的同名几何集（避免重复）
        if gset_mgr().find(gset_name):
            gset_mgr().delete([gset_name])
        # 添加新的面到几何集
        gset_mgr().add(gset_name, faces)
        # 获取并转换ID
        converted_ids = get_and_convert_ids(gset_name)
        all_converted_ids[gset_name] = converted_ids
        print(f"已添加{len(faces)}个{btype}面到几何集'{gset_name}'")
    else:
        print(f"未找到{btype}面，未创建几何集'{gset_name}'")
        all_converted_ids[gset_name] = []

# 4. 结果输出（便于后续使用）
print("\n所有边界的转换后ID汇总：")
for gset_name, ids in all_converted_ids.items():
    print(f"{gset_name}: {ids}")
# 创建表面集
surf_mgr = GFE.Pre.surface.surf_mgr()
obj = GFE.Pre.surface.geometry_surface('TUTIAROUND')
obj.name = 'TUTIAROUND'
obj.data = [id for ids in all_converted_ids.values() for id in ids]
surf_mgr.add(obj)
# 创建人工边界
arc_mgr = GFE.Pre.artbc.artbc_mgr()
obj = GFE.Pre.artbc.art_bc()
obj.name = 'ArtBC-1'
obj.structure = 'plant'
obj.surface = 'TUTIAROUND'
obj.centered = False
obj.center = []
GFE.Pre.artbc.artbc_mgr().add(obj)


# ============= 土体网格划分 ===================
from GFE.geometry import mesh_generator
generator = mesh_generator.generator()
controller = mesh_generator.controller()
controller.number_option = {
'General.ExpertMode' : 1.0,
'General.NumThreads' : 0.0,
'General.Terminal' : 1.0,
'Mesh.Algorithm' : 2.0,
'Mesh.Algorithm3D' : 1.0,
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
generator.mesh(['Soil-1'], controller)

# ============ 计算阻尼比==========
# 已在创建材料时添加

# ============= 创建幅值函数 ==============
obj = GFE.Pre.amplitude.amplitude()
obj.type = 0
obj.name = '25_RH1TG025_(RenGong_T_025)_x_Zhu'
obj.spectrum_type = -1
obj.gravity = 0.0
obj.value = [0.0, 0.0048, 0.02, 0.0053, 0.04, 0.0036, 0.06, 0.0066,
0.08, 0.0028, 0.1, 0.0108, 0.12, -0.007, 0.14, 0.0123,
0.16, 0.0141, 0.18, -0.0115, 0.2, 0.0146, 0.22, -0.007,
0.24, 0.0235, 0.26, -0.0089, 0.28, -0.0058, 0.3, -0.0134,
0.32, 0.0549, 0.34, 0.1159, 0.36, -0.1744, 0.38, 0.0285,
0.4, -0.0087, 0.42, -0.0436, 0.44, 0.3132, 0.46, 0.0033,
0.48, -0.425, 0.5, 0.0057, 0.52, 0.2274, 0.54, 0.1854,
0.56, 0.1567, 0.58, 0.0175, 0.6, -0.3347, 0.62, 0.1046,
0.64, 0.2089, 0.66, -0.16, 0.68, -0.2667, 0.7, -0.1404,
0.72, 0.0099, 0.74, 0.624, 0.76, 0.3116, 0.78, 0.0924,
0.8, -0.1697, 0.82, -0.2051, 0.84, -0.0219, 0.86, 0.2443,
0.88, 0.0108, 0.9, 0.0633, 0.92, 0.1923, 0.94, 0.1552,
0.96, -0.1149, 0.98, 0.1314, 1.0, 0.1962, 1.02, 0.1054,
1.04, -0.0861, 1.06, -0.0045, 1.08, 0.3072, 1.1, 0.5559,
1.12, 0.667, 1.14, -0.0331, 1.16, -0.112, 1.18, 0.1427,
1.2, 0.1747, 1.22, -0.1515, 1.24, -0.5699, 1.26, -0.3213,
1.28, -0.1465, 1.3, -0.4254, 1.32, -0.0669, 1.34, -0.032,
1.36, -0.0123, 1.38, 0.2461, 1.4, -0.0898, 1.42, 0.0795,
1.44, 0.2069, 1.46, -0.5153, 1.48, -0.7663, 1.5, -0.8759,
1.52, -0.569, 1.54, 0.1915, 1.56, 0.1717, 1.58, 0.0193,
1.6, 0.043, 1.62, 0.0652, 1.64, 0.1482, 1.66, 0.2549,
1.68, 0.099, 1.7, 0.0252, 1.72, 0.225, 1.74, 0.5639,
1.76, 0.2589, 1.78, 0.3535, 1.8, 0.4194, 1.82, -0.2403,
1.84, -0.1335, 1.86, 0.3995, 1.88, 0.1631, 1.9, 0.1407,
1.92, 0.1851, 1.94, 0.1465, 1.96, 0.0026, 1.98, -0.2862,
2.0, -0.1572, 2.02, -0.0425, 2.04, -0.285, 2.06, -0.4391,
2.08, 0.2803, 2.1, 0.4105, 2.12, -0.2015, 2.14, 0.6052,
2.16, 0.1738, 2.18, 0.5491, 2.2, 0.6057, 2.22, 0.4077,
2.24, 0.2487, 2.26, 0.3684, 2.28, -0.037, 2.3, 0.1936,
2.32, 0.0099, 2.34, -0.4393, 2.36, -0.1747, 2.38, 0.462,
2.4, 0.1767, 2.42, 0.4866, 2.44, 0.149, 2.46, -0.3957,
2.48, 0.0799, 2.5, 0.0801, 2.52, -0.2076, 2.54, -0.3068,
2.56, -0.24, 2.58, 0.4366, 2.6, 0.5224, 2.62, -0.1683,
2.64, -0.2287, 2.66, -0.2996, 2.68, -0.3218, 2.7, -0.5919,
2.72, -0.2597, 2.74, 0.6991, 2.76, 0.0704, 2.78, -0.0326,
2.8, 0.535, 2.82, -0.1661, 2.84, -0.1397, 2.86, -0.1462,
2.88, -0.2282, 2.9, -0.6097, 2.92, -0.273, 2.94, 0.1939,
2.96, 0.3191, 2.98, 0.089, 3.0, -0.0619, 3.02, 0.1193,
3.04, 0.3227, 3.06, 0.0752, 3.08, -0.23, 3.1, -0.0065,
3.12, -0.3515, 3.14, -0.2114, 3.16, 0.196, 3.18, 0.1168,
3.2, -0.1349, 3.22, -0.0437, 3.24, -0.5775, 3.26, 0.0,
3.28, 0.2475, 3.3, 0.0778, 3.32, 0.2624, 3.34, -0.3733,
3.36, -0.5076, 3.38, -0.2433, 3.4, -0.207, 3.42, -0.1261,
3.44, -0.0877, 3.46, -0.0239, 3.48, -0.6927, 3.5, -0.6039,
3.52, -0.4597, 3.54, -0.5917, 3.56, -0.464, 3.58, 0.1156,
3.6, 0.156, 3.62, 0.1636, 3.64, 0.0004, 3.66, 0.267,
3.68, 0.4183, 3.7, 0.3289, 3.72, 0.1749, 3.74, 0.0312,
3.76, -0.1897, 3.78, -0.1595, 3.8, -0.283, 3.82, -1.0,
3.84, -0.4813, 3.86, -0.1781, 3.88, -0.0641, 3.9, 0.2745,
3.92, 0.5519, 3.94, 0.2718, 3.96, -0.2636, 3.98, -0.6136,
4.0, -0.177, 4.02, -0.059, 4.04, -0.3732, 4.06, -0.0078,
4.08, 0.0882, 4.1, 0.0783, 4.12, 0.8838, 4.14, 0.1991,
4.16, -0.1363, 4.18, -0.0573, 4.2, -0.0506, 4.22, 0.2058,
4.24, -0.1331, 4.26, -0.4127, 4.28, -0.254, 4.3, -0.022,
4.32, -0.1364, 4.34, -0.1797, 4.36, -0.0375, 4.38, 0.0442,
4.4, 0.2366, 4.42, 0.3819, 4.44, 0.2626, 4.46, 0.0724,
4.48, -0.0281, 4.5, -0.5888, 4.52, -0.1418, 4.54, -0.2117,
4.56, -0.5521, 4.58, -0.3699, 4.6, -0.2164, 4.62, -0.089,
4.64, 0.0608, 4.66, 0.0531, 4.68, 0.1107, 4.7, 0.366,
4.72, 0.3511, 4.74, 0.0677, 4.76, -0.1264, 4.78, -0.3079,
4.8, -0.253, 4.82, 0.0298, 4.84, -0.1567, 4.86, -0.1099,
4.88, -0.0519, 4.9, -0.2668, 4.92, 0.0639, 4.94, 0.0304,
4.96, -0.3216, 4.98, -0.1368, 5.0, 0.193, 5.02, 0.3683,
5.04, 0.7066, 5.06, 0.5032, 5.08, 0.2419, 5.1, -0.0913,
5.12, -0.03, 5.14, 0.0557, 5.16, -0.0034, 5.18, 0.001,
5.2, 0.1852, 5.22, 0.4616, 5.24, 0.3765, 5.26, -0.0282,
5.28, -0.2395, 5.3, -0.4713, 5.32, -0.3605, 5.34, -0.172,
5.36, -0.3659, 5.38, 0.0159, 5.4, 0.3463, 5.42, 0.0365,
5.44, 0.1741, 5.46, 0.2197, 5.48, 0.0107, 5.5, 0.1394,
5.52, 0.3466, 5.54, 0.2831, 5.56, 0.1228, 5.58, 0.2789,
5.6, 0.4788, 5.62, 0.2297, 5.64, -0.4129, 5.66, -0.6015,
5.68, -0.2626, 5.7, -0.1627, 5.72, -0.0962, 5.74, 0.0491,
5.76, -0.0359, 5.78, -0.1606, 5.8, 0.1095, 5.82, 0.2358,
5.84, 0.2525, 5.86, -0.2064, 5.88, -0.4394, 5.9, -0.1104,
5.92, -0.0043, 5.94, -0.1124, 5.96, -0.2774, 5.98, -0.2671,
6.0, 0.1041, 6.02, 0.2876, 6.04, 0.2158, 6.06, 0.0066,
6.08, -0.079, 6.1, -0.1376, 6.12, -0.2956, 6.14, -0.1759,
6.16, -0.2884, 6.18, -0.5277, 6.2, -0.2744, 6.22, 0.2282,
6.24, 0.431, 6.26, 0.2937, 6.28, 0.0212, 6.3, -0.1073,
6.32, 0.0569, 6.34, 0.2165, 6.36, 0.1695, 6.38, -0.0095,
6.4, 0.035, 6.42, 0.1935, 6.44, 0.2818, 6.46, 0.2242,
6.48, -0.0998, 6.5, -0.4544, 6.52, -0.5194, 6.54, -0.2848,
6.56, -0.049, 6.58, -0.2457, 6.6, -0.4441, 6.62, -0.2534,
6.64, -0.0932, 6.66, 0.0486, 6.68, 0.142, 6.7, -0.0621,
6.72, -0.3707, 6.74, -0.1837, 6.76, -0.0322, 6.78, 0.1509,
6.8, 0.0475, 6.82, -0.0494, 6.84, 0.0656, 6.86, 0.104,
6.88, 0.1433, 6.9, 0.0628, 6.92, -0.1382, 6.94, -0.3328,
6.96, -0.3859, 6.98, -0.2394, 7.0, -0.0279, 7.02, 0.0204,
7.04, 0.0493, 7.06, -0.0291, 7.08, 0.0634, 7.1, 0.0278,
7.12, 0.0162, 7.14, 0.0077, 7.16, -0.0101, 7.18, 0.2378,
7.2, 0.3526, 7.22, 0.3077, 7.24, 0.2849, 7.26, -0.027,
7.28, -0.2922, 7.3, -0.2394, 7.32, -0.1854, 7.34, -0.1062,
7.36, -0.1295, 7.38, 0.0474, 7.4, 0.3888, 7.42, 0.4295,
7.44, 0.2907, 7.46, 0.1784, 7.48, 0.0233, 7.5, -0.0539,
7.52, 0.0309, 7.54, 0.2266, 7.56, 0.2869, 7.58, 0.1824,
7.6, 0.2038, 7.62, 0.194, 7.64, -0.0058, 7.66, -0.1138,
7.68, -0.0488, 7.7, 0.0344, 7.72, 0.0322, 7.74, 0.2363,
7.76, 0.2899, 7.78, 0.0328, 7.8, -0.1404, 7.82, -0.2019,
7.84, -0.312, 7.86, -0.1889, 7.88, 0.0216, 7.9, 0.0323,
7.92, 0.1124, 7.94, 0.2051, 7.96, 0.2562, 7.98, 0.165,
8.0, 0.0465, 8.02, -0.0774, 8.04, -0.1928, 8.06, -0.1696,
8.08, -0.1139, 8.1, -0.1214, 8.12, -0.029, 8.14, 0.0781,
8.16, 0.2363, 8.18, 0.2165, 8.2, 0.1211, 8.22, 0.0871,
8.24, -0.0544, 8.26, -0.0118, 8.28, 0.1479, 8.3, 0.017,
8.32, -0.0048, 8.34, 0.0928, 8.36, 0.1977, 8.38, 0.1952,
8.4, 0.082, 8.42, -0.0305, 8.44, -0.0987, 8.46, -0.0868,
8.48, 0.0074, 8.5, 0.0106, 8.52, 0.0045, 8.54, 0.0229,
8.56, 0.0977, 8.58, 0.1492, 8.6, 0.0778, 8.62, -0.0172,
8.64, -0.0681, 8.66, -0.0646, 8.68, -0.0206, 8.7, 0.0862,
8.72, 0.1244, 8.74, 0.2443, 8.76, 0.3338, 8.78, 0.2681,
8.8, 0.1805, 8.82, 0.1166, 8.84, 0.0294, 8.86, -0.0081,
8.88, -0.0084, 8.9, -0.0053, 8.92, 0.0626, 8.94, 0.1374,
8.96, 0.1597, 8.98, 0.08, 9.0, -0.0143, 9.02, -0.0907,
9.04, -0.0922, 9.06, -0.0832, 9.08, -0.0627, 9.1, 0.0971,
9.12, 0.2147, 9.14, 0.2406, 9.16, 0.3131, 9.18, 0.23,
9.2, 0.0504, 9.22, -0.0072, 9.24, -0.0813, 9.26, -0.0491,
9.28, 0.1014, 9.3, 0.1766, 9.32, 0.1803, 9.34, 0.1315,
9.36, 0.1027, 9.38, 0.0993, 9.4, 0.1016, 9.42, -0.008,
9.44, -0.0584, 9.46, 0.1093, 9.48, 0.2492, 9.5, 0.2745,
9.52, 0.3133, 9.54, 0.2117, 9.56, 0.107, 9.58, 0.1219,
9.6, 0.153, 9.62, 0.1593, 9.64, 0.0802, 9.66, 0.0745,
9.68, 0.111, 9.7, 0.1308, 9.72, 0.1044, 9.74, -0.0126,
9.76, -0.1136, 9.78, -0.1206, 9.8, -0.0837, 9.82, 0.0004,
9.84, 0.0299, 9.86, 0.0233, 9.88, 0.0772, 9.9, 0.107,
9.92, 0.1113, 9.94, 0.0735, 9.96, -0.0373, 9.98, -0.0599,
10.0, 0.0165, 10.02, 0.0228, 10.04, -0.0331, 10.06, -0.0102,
10.08, -0.0193, 10.1, -0.0334, 10.12, -0.0549, 10.14, -0.1416,
10.16, -0.1797, 10.18, -0.1559, 10.2, -0.1045, 10.22, -0.1081,
10.24, -0.132, 10.26, -0.0915, 10.28, -0.0506, 10.3, -0.0698,
10.32, -0.0943, 10.34, -0.0755, 10.36, -0.0644, 10.38, -0.0771,
10.4, -0.0905, 10.42, -0.0665, 10.44, -0.0696, 10.46, -0.0993,
10.48, -0.1291, 10.5, -0.1223, 10.52, -0.1387, 10.54, -0.169,
10.56, -0.1708, 10.58, -0.1566, 10.6, -0.1006, 10.62, -0.0505,
10.64, -0.0448, 10.66, -0.0433, 10.68, -0.06, 10.7, -0.0565,
10.72, -0.0493, 10.74, -0.0681, 10.76, -0.1153, 10.78, -0.1119,
10.8, -0.0863, 10.82, -0.0714, 10.84, -0.0697, 10.86, -0.0754,
10.88, -0.0861, 10.9, -0.0895, 10.92, -0.0843, 10.94, -0.0645,
10.96, -0.0742, 10.98, -0.1069, 11.0, -0.0842, 11.02, -0.0822,
11.04, -0.0807, 11.06, -0.061, 11.08, -0.067, 11.1, -0.041,
11.12, 0.013, 11.14, 0.0316, 11.16, 0.0097, 11.18, -0.0337,
11.2, -0.0603, 11.22, -0.0554, 11.24, -0.0065, 11.26, -0.0052,
11.28, -0.0505, 11.3, -0.0866, 11.32, -0.0952, 11.34, -0.0803,
11.36, -0.0619, 11.38, -0.0765, 11.4, -0.0786, 11.42, -0.0504,
11.44, -0.0134, 11.46, 0.0563, 11.48, 0.0792, 11.5, 0.0322,
11.52, -0.0244, 11.54, -0.0707, 11.56, -0.0801, 11.58, -0.0448,
11.6, -0.0489, 11.62, -0.0449, 11.64, -0.0349, 11.66, -0.0229,
11.68, -0.0389, 11.7, -0.0916, 11.72, -0.1154, 11.74, -0.1457,
11.76, -0.1203, 11.78, -0.0793, 11.8, -0.0802, 11.82, -0.098,
11.84, -0.1043, 11.86, -0.0988, 11.88, -0.0721, 11.9, -0.057,
11.92, -0.059, 11.94, -0.0425, 11.96, -0.0027, 11.98, 0.0166,
12.0, -0.0052, 12.02, -0.046, 12.04, -0.1089, 12.06, -0.1125,
12.08, -0.0939, 12.1, -0.1131, 12.12, -0.1449, 12.14, -0.1749,
12.16, -0.1637, 12.18, -0.1182, 12.2, -0.1145, 12.22, -0.1219,
12.24, -0.1164, 12.26, -0.0754, 12.28, -0.033, 12.3, -0.018,
12.32, -0.0293, 12.34, -0.0617, 12.36, -0.0744, 12.38, -0.0521,
12.4, -0.0494, 12.42, -0.0748, 12.44, -0.0738, 12.46, -0.0461,
12.48, -0.0086, 12.5, 0.006, 12.52, -0.0018, 12.54, -0.0205,
12.56, -0.039, 12.58, -0.0145, 12.6, 0.0239, 12.62, 0.0416,
12.64, 0.0355, 12.66, 0.0283, 12.68, 0.0481, 12.7, 0.0492,
12.72, 0.0448, 12.74, 0.0528, 12.76, 0.051, 12.78, 0.067,
12.8, 0.0765, 12.82, 0.072, 12.84, 0.0598, 12.86, 0.0487,
12.88, 0.0523, 12.9, 0.0621, 12.92, 0.0703, 12.94, 0.0812,
12.96, 0.0918, 12.98, 0.0923, 13.0, 0.0874, 13.02, 0.0819,
13.04, 0.0835, 13.06, 0.0932, 13.08, 0.1102, 13.1, 0.1192,
13.12, 0.1187, 13.14, 0.1202, 13.16, 0.1167, 13.18, 0.0901,
13.2, 0.058, 13.22, 0.0216, 13.24, -0.0013, 13.26, 0.0041,
13.28, 0.0315, 13.3, 0.0496, 13.32, 0.0588, 13.34, 0.0759,
13.36, 0.0736, 13.38, 0.0689, 13.4, 0.0687, 13.42, 0.0581,
13.44, 0.0459, 13.46, 0.0343, 13.48, 0.0459, 13.5, 0.0733,
13.52, 0.0779, 13.54, 0.063, 13.56, 0.0503, 13.58, 0.0449,
13.6, 0.0457, 13.62, 0.0427, 13.64, 0.0464, 13.66, 0.0406,
13.68, 0.0324, 13.7, 0.0352, 13.72, 0.0346, 13.74, 0.032,
13.76, 0.0212, 13.78, 0.0132, 13.8, 0.0228, 13.82, 0.0374,
13.84, 0.0554, 13.86, 0.0587, 13.88, 0.0565, 13.9, 0.0589,
13.92, 0.0624, 13.94, 0.0632, 13.96, 0.0574, 13.98, 0.0397,
14.0, 0.0388, 14.02, 0.0472, 14.04, 0.051, 14.06, 0.0342,
14.08, 0.0314, 14.1, 0.0357, 14.12, 0.0316, 14.14, 0.0311,
14.16, 0.0346, 14.18, 0.0361, 14.2, 0.0393, 14.22, 0.0501,
14.24, 0.0509, 14.26, 0.0459, 14.28, 0.0361, 14.3, 0.0337,
14.32, 0.0378, 14.34, 0.0452, 14.36, 0.0409, 14.38, 0.039,
14.4, 0.0469, 14.42, 0.0625, 14.44, 0.0685, 14.46, 0.0676,
14.48, 0.0635, 14.5, 0.0652, 14.52, 0.0718, 14.54, 0.0778,
14.56, 0.0764, 14.58, 0.0737, 14.6, 0.0658, 14.62, 0.069,
14.64, 0.0718, 14.66, 0.0601, 14.68, 0.0517, 14.7, 0.053,
14.72, 0.0553, 14.74, 0.045, 14.76, 0.0266, 14.78, 0.0271,
14.8, 0.0292, 14.82, 0.0241, 14.84, 0.0187, 14.86, 0.0151,
14.88, 0.0099, 14.9, 0.0062, 14.92, 0.0061, 14.94, 0.0045,
14.96, -0.0025, 14.98, -0.0011, 15.0, 0.0095, 15.02, 0.02,
15.04, 0.0246, 15.06, 0.0149, 15.08, 0.0004, 15.1, -0.0064,
15.12, -0.0093, 15.14, -0.0144, 15.16, -0.0288, 15.18, -0.04,
15.2, -0.0459, 15.22, -0.0475, 15.24, -0.0468, 15.26, -0.0524,
15.28, -0.0608, 15.3, -0.0607, 15.32, -0.0484, 15.34, -0.0355,
15.36, -0.0324, 15.38, -0.032, 15.4, -0.0292, 15.42, -0.0249,
15.44, -0.0171, 15.46, -0.0081, 15.48, -0.0064, 15.5, -0.005,
15.52, -0.0027, 15.54, -0.0035, 15.56, -0.0065, 15.58, -0.012,
15.6, -0.019, 15.62, -0.0223, 15.64, -0.0215, 15.66, -0.0218,
15.68, -0.0223, 15.7, -0.0222, 15.72, -0.0177, 15.74, -0.0178,
15.76, -0.0203, 15.78, -0.0237, 15.8, -0.027, 15.82, -0.0296,
15.84, -0.0303, 15.86, -0.0267, 15.88, -0.0266, 15.9, -0.0261,
15.92, -0.0219, 15.94, -0.0229, 15.96, -0.0262, 15.98, -0.0248,
16.0, -0.0247, 16.02, -0.0233, 16.04, -0.0224, 16.06, -0.0281,
16.08, -0.0299, 16.1, -0.0266, 16.12, -0.0238, 16.14, -0.0205,
16.16, -0.0182, 16.18, -0.0214, 16.2, -0.0236, 16.22, -0.0211,
16.24, -0.0213, 16.26, -0.0247, 16.28, -0.0315, 16.3, -0.0367,
16.32, -0.0398, 16.34, -0.0467, 16.36, -0.0512, 16.38, -0.0503,
16.4, -0.0488, 16.42, -0.0435, 16.44, -0.0322, 16.46, -0.0229,
16.48, -0.0194, 16.5, -0.0203, 16.52, -0.0219, 16.54, -0.0237,
16.56, -0.0275, 16.58, -0.0307, 16.6, -0.0323, 16.62, -0.0328,
16.64, -0.0317, 16.66, -0.0312, 16.68, -0.0287, 16.7, -0.0275,
16.72, -0.0275, 16.74, -0.0263, 16.76, -0.0292, 16.78, -0.032,
16.8, -0.0295, 16.82, -0.0287, 16.84, -0.0314, 16.86, -0.0369,
16.88, -0.0437, 16.9, -0.047, 16.92, -0.046, 16.94, -0.044,
16.96, -0.0446, 16.98, -0.0454, 17.0, -0.0432, 17.02, -0.0381,
17.04, -0.0356, 17.06, -0.0394, 17.08, -0.0423, 17.1, -0.0435,
17.12, -0.0421, 17.14, -0.0376, 17.16, -0.0376, 17.18, -0.0408,
17.2, -0.0375, 17.22, -0.0288, 17.24, -0.0198, 17.26, -0.013,
17.28, -0.0103, 17.3, -0.0108, 17.32, -0.0091, 17.34, -0.0073,
17.36, -0.0086, 17.38, -0.0108, 17.4, -0.0109, 17.42, -0.0077,
17.44, -0.0008, 17.46, 0.0041, 17.48, 0.0057, 17.5, 0.0049,
17.52, 0.0036, 17.54, 0.0039, 17.56, 0.0056, 17.58, 0.0066,
17.6, 0.0078, 17.62, 0.0095, 17.64, 0.0107, 17.66, 0.011,
17.68, 0.0121, 17.7, 0.0136, 17.72, 0.0145, 17.74, 0.0148,
17.76, 0.0159, 17.78, 0.0187, 17.8, 0.0227, 17.82, 0.026,
17.84, 0.0262, 17.86, 0.0254, 17.88, 0.0252, 17.9, 0.0245,
17.92, 0.022, 17.94, 0.0181, 17.96, 0.0149, 17.98, 0.0125,
18.0, 0.01, 18.02, 0.0087, 18.04, 0.008, 18.06, 0.0077,
18.08, 0.0079, 18.1, 0.0073, 18.12, 0.0068, 18.14, 0.0059,
18.16, 0.0026, 18.18, -0.0019, 18.2, -0.0061, 18.22, -0.0085,
18.24, -0.0083, 18.26, -0.0075, 18.28, -0.0071, 18.3, -0.0066,
18.32, -0.0059, 18.34, -0.0048, 18.36, -0.0036, 18.38, -0.0027,
18.4, -0.0019, 18.42, -0.0004, 18.44, 0.0018, 18.46, 0.0033,
18.48, 0.0048, 18.5, 0.0059, 18.52, 0.0055, 18.54, 0.0054,
18.56, 0.0064, 18.58, 0.0071, 18.6, 0.0075, 18.62, 0.0079,
18.64, 0.0081, 18.66, 0.0077, 18.68, 0.0066, 18.7, 0.0058,
18.72, 0.0052, 18.74, 0.0042, 18.76, 0.0034, 18.78, 0.0042,
18.8, 0.0053, 18.82, 0.0057, 18.84, 0.0073, 18.86, 0.0086,
18.88, 0.0104, 18.9, 0.0123, 18.92, 0.0135, 18.94, 0.0144,
18.96, 0.015, 18.98, 0.015, 19.0, 0.0151, 19.02, 0.0147,
19.04, 0.0136, 19.06, 0.0133, 19.08, 0.0141, 19.1, 0.0147,
19.12, 0.0155, 19.14, 0.0155, 19.16, 0.0146, 19.18, 0.0143,
19.2, 0.0141, 19.22, 0.0133, 19.24, 0.0124, 19.26, 0.012,
19.28, 0.0127, 19.3, 0.0134, 19.32, 0.0128, 19.34, 0.0119,
19.36, 0.0109, 19.38, 0.0097, 19.4, 0.0085, 19.42, 0.0081,
19.44, 0.0091, 19.46, 0.0095, 19.48, 0.0096, 19.5, 0.0102,
19.52, 0.0098, 19.54, 0.0093, 19.56, 0.0087, 19.58, 0.0078,
19.6, 0.0066, 19.62, 0.0061, 19.64, 0.0064, 19.66, 0.007,
19.68, 0.0072, 19.7, 0.0072, 19.72, 0.0075, 19.74, 0.0079,
19.76, 0.0079, 19.78, 0.0074, 19.8, 0.0071, 19.82, 0.0064,
19.84, 0.006, 19.86, 0.0062, 19.88, 0.0062, 19.9, 0.0059,
19.92, 0.0055, 19.94, 0.0046, 19.96, 0.0045, 19.98, -0.0146,
20.0, 0.0049]
GFE.Pre.amplitude.amp_mgr().add(obj)

# =============== 地震波场反应 ================
obj = GFE.Pre.vibration.vibra_load()
obj.name = 'VibLoad-1'
obj.amp_bottom_x = '25_RH1TG025_(RenGong_T_025)_x_Zhu'
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


# ================ 分析步 ==================
# 动力分析步
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


# =============== 场输出 ==================
# 创建动力场输出
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

# ================= 工况 ================
# 动力工况
obj = GFE.Pre.case.case()
obj.name = 'Dyna'
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


# ============== 作业管理器 ==============
# 写出inp文件
from GFE.io import inpio
inpwriter = inpio.writer(inp_path)
inpwriter.set_case('Dyna')
inpwriter.perform()

```
