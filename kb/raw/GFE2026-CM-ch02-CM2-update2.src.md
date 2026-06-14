# GFE2026-CM-ch02-CM2-update2
> 来源：E:\GFE2026\典型案例与教程\第2章 钢骨混凝土静力及模态分析案例\CM2-update2.py（GFE2026 官方典型案例命令流，v3.x 代际金标准）。raw 不可变源副本，2026-06-11 入库。

```python
import GFE
from GFE import *
from GFE.Pre import *
from GFE.occ import *
import math
from GFE.geometry import geotool
GFE.Pre.document.set_application_by_ui()


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
plugin_dir2 = os.path.join(plugin_dir, "第2章")
inp_path_model = os.path.join(plugin_dir2, "CM2-Case-Model.inp")
inp_path_static = os.path.join(plugin_dir2, "CM2-case-Static.inp")
# 转为绝对路径
inp_path_model = os.path.abspath(inp_path_model)
inp_path_static = os.path.abspath(inp_path_static)

print(inp_path_model)
print(inp_path_static)

# ============ 参数定义 ==========
# 1. 模型参数
steel_size = 400            # 工字钢截面尺寸（400*400）
steel_thickness = 20        # 工字钢厚度
model_height = 4000         # 整体模型高度
concrete_size = 600		    # 混凝土截面尺寸（600*600）
stirrup_size = 500			# 箍筋截面尺寸（500*500）
stirrup_spacing = 100		# 箍筋间距
stirrup_num = int(model_height//stirrup_spacing)+1			# 箍筋数量
print(f"初始箍筋的数量是：{stirrup_num}")
reinforcing_height = model_height			# 主筋长度【同模型高度】
reinforcing_spacing = stirrup_size			# 主筋间距【箍筋截面尺寸】

# 2. 材料参数：(名称, 密度, 弹性杨模E, 弹性泊松比v)
materials = [
    ('Q345', 7.8e-09, 206000, 0.25),
    ('C40', 2.5e-09, 32500, 0.2)
]
# 3. 截面属性
stirrup_section_radius = 6.0				# 箍筋截面圆柱半径
reinforcing_section_radius = 12.5		    # 主筋截面圆柱半径
# 4. 压力荷载
pressure_value_steel = 2 				    # 工字钢上翼缘施加压力
pressure_value_concrete = 20 				# 混凝土柱截面上施加压力
# 5. 网格
mesh_size = float(50)						# 网格尺寸（必须浮点数）


# =========== 创建工字钢模型 ===========
# 定义一下参数
steel_out = steel_size / 2      # 工字外
steel_in = steel_out - steel_thickness # 工字内
steel_in_in = steel_thickness / 2       # 工字最内

# ------- 绘制 “工字”草图 ---------
GFE.draft.get_current().set_normal([0.0, 0.0, 0.0], [0.0, 0.0, 1.0], [1.0, 0.0, 0.0])
GFE.draft.get_current().set_snap_object(0)
GFE.draft.get_current().set_operate_mode(3)

# 下矩形
GFE.draft.get_current().input(-steel_out, -steel_out)
GFE.draft.get_current().input(steel_out, -steel_in)
# 上矩形
GFE.draft.get_current().input(-steel_out, steel_out)
GFE.draft.get_current().input(steel_out, steel_in)
# 中矩形
GFE.draft.get_current().input(steel_in_in, steel_in)
GFE.draft.get_current().input(-steel_in_in, -steel_in)

# 框选所有线
GFE.draft.get_current().set_snap_object(2)
GFE.draft.get_current().snap_object(-(steel_out+100), steel_out+100, steel_out+100, -(steel_out+100))       #框选“工字”区域
GFE.draft.get_current().select_snaped(True)
# 分段所有线
GFE.draft.get_current().split_selected()

# 删除矩形重合的线，形成“工字”
GFE.draft.get_current().snap_object(0.0, steel_in)
GFE.draft.get_current().select_snaped(False)
GFE.draft.get_current().remove_selected()
GFE.draft.get_current().snap_object(0.0, steel_in)     #两个矩形重合，有两条重合线，所有删两次
GFE.draft.get_current().select_snaped(False)
GFE.draft.get_current().remove_selected()
GFE.draft.get_current().snap_object(0.0, -steel_in)
GFE.draft.get_current().select_snaped(False)
GFE.draft.get_current().remove_selected()
GFE.draft.get_current().snap_object(0.0, -steel_in)     #两个矩形重合，有两条重合线，所有删两次
GFE.draft.get_current().select_snaped(False)
GFE.draft.get_current().remove_selected()


# 框选“工字”，填充区域
GFE.draft.get_current().snap_object(-(steel_out+100), steel_out+100, steel_out+100, -(steel_out+100))
GFE.draft.get_current().select_snaped(True)
GFE.draft.get_current().fill_selected()
GFE.draft.get_current().remove_selected()       #然后把线都删了，只剩下填充区域

#-----------创建“工字”模型----------
# 完成草图，创建二维模型“工字”
shape = GFE.draft.get_current().export()
if not shape.is_null() :
    mgr = GFE.Pre.geometry.geo_mgr()
    mgr.add('section-steel', shape)


# 拉伸“工字”形成三维模型
builder = GFE.geometry.geoprim.builder()
shapes = [GFE.Pre.geometry.geo_mgr().find('section-steel').shape()]
extruded = builder.extrude(shapes, [0.0, 0.0, model_height])
mgr = Pre.geometry.geo_mgr()
for sp in extruded :
    if not sp.is_null() :
        mgr.add('I-steel', sp)

# 阵列工字模型
builder = GFE.geometry.geoprim.builder()
shapes = [GFE.Pre.geometry.geo_mgr().find('I-steel').shape()]
new_shapes = builder.make_array(shapes, 2, 1, 1, [0.0, 0.0, 0.0])
mgr = Pre.geometry.geo_mgr()
for sp in new_shapes :
    if not sp.is_null() :
        mgr.add('I-steel-1', sp)


# 旋转和平移I-steel-1工字模型
builder = GFE.geometry.geoprim.builder()
builder.rotate(['I-steel-1'], [0.0, 0.0, 0.0], [1.0, 0.0, 0.0], 90.0, False)

# 查找两个钢骨的形心，计算向量差
steel_1_geo = GFE.Pre.geometry.geo_mgr().find("I-steel")
center1 = GFE.geometry.geotool.centre_of_mass(steel_1_geo.shape())
steel_2_geo = GFE.Pre.geometry.geo_mgr().find("I-steel-1")
center2 = GFE.geometry.geotool.centre_of_mass(steel_2_geo.shape())
# 计算两个钢骨之间的位移向量
trsf_vec = [center1[i] - center2[i] for i in range(3)]
# 平移钢骨
builder = GFE.geometry.geoprim.builder()
builder.translate(['I-steel-1'], trsf_vec, False)

# =========== 创建混凝土柱 ============
sp = occ.brep_prim.make_box(concrete_size, concrete_size, model_height)
if not sp.is_null() :
    mgr = Pre.geometry.geo_mgr()
    mgr.add('concrete-pillar', sp)


# 查找钢骨和混凝土的形心，计算向量差
steel_geo = GFE.Pre.geometry.geo_mgr().find("I-steel")
center1 = GFE.geometry.geotool.centre_of_mass(steel_geo.shape())
concrete_geo = GFE.Pre.geometry.geo_mgr().find("concrete-pillar")
center2 = GFE.geometry.geotool.centre_of_mass(concrete_geo.shape())
# 计算两个钢骨之间的位移向量
trsf_vec = [center1[i] - center2[i] for i in range(3)]
# 平移混凝土柱
builder = GFE.geometry.geoprim.builder()
builder.translate(['concrete-pillar'], trsf_vec, False)


# ============ 创建“箍筋”模型 ===============
# 清空草图，删除“工字”草图
GFE.draft.get_current().clear()

# 创建“箍筋”草图
GFE.draft.get_current().set_snap_object(0)
GFE.draft.get_current().set_operate_mode(3)
stirrup_size_center = stirrup_size / 2      # 尺寸一半
GFE.draft.get_current().input(-stirrup_size_center, -stirrup_size_center)
GFE.draft.get_current().input(stirrup_size_center, stirrup_size_center)

# 创建“箍筋”二维模型
shape = GFE.draft.get_current().export()
if not shape.is_null() :
    mgr = GFE.Pre.geometry.geo_mgr()
    mgr.add('stirrup', shape)


# 阵列“箍筋”二维模型，得到一组“箍筋”
stirrup_names = ["stirrup"]     # 记录所有箍筋名称，方便后续合并
builder = GFE.geometry.geoprim.builder()
shapes = [GFE.Pre.geometry.geo_mgr().find('stirrup').shape()]
new_shapes = builder.make_array(shapes, 1, 1, stirrup_num, [0.0, 0.0, stirrup_spacing])
mgr = Pre.geometry.geo_mgr()
for sp in new_shapes :
    if not sp.is_null() :
        name = mgr.auto_name('stirrup')
        mgr.add(name, sp)
        stirrup_names.append(name)

# ========== 移除首尾和中间重叠的“箍筋” ==========
# 记录需要删除的箍筋名称
delete_stirrup_names = [stirrup_names[0], stirrup_names[-1]]        # 初始化删除首尾
del stirrup_names[0]
del stirrup_names[-1]

# 计算中间钢骨的z轴高度范围
steel_2_minz = model_height/2 - steel_size/2
steel_2_maxz = model_height/2 + steel_size/2
print(f"需要删除的中间箍筋z轴范围：{steel_2_minz} 到 {steel_2_maxz}")

# 查找需要删除的中间部分
need_del_names = []
for name in stirrup_names:
    geo_obj = GFE.Pre.geometry.geo_mgr().find(name)
    if geo_obj is None:
        continue
    # 获取当前箍筋的质心z轴坐标
    current_z = GFE.geometry.geotool.centre_of_mass(geo_obj.shape())[2]
    if steel_2_minz - 0.1 < current_z < steel_2_maxz + 0.1:
        need_del_names.append(name)
# 删除中间部分
for del_name in need_del_names:
    if del_name in stirrup_names:
        stirrup_names.remove(del_name)
        delete_stirrup_names.append(del_name)
print(f"当前箍筋数量：{len(stirrup_names)}, 名称：{stirrup_names}")
print(f"已删除箍筋数量：{len(delete_stirrup_names)}, 名称：{delete_stirrup_names}")
GFE.Pre.geometry.geo_mgr().delete(delete_stirrup_names)
GFE.Pre.mesh.mesh_mgr().delete(delete_stirrup_names)


# ============== 创建“主筋”模型 ===============
# 清空草图，删除“箍筋”草图
GFE.draft.get_current().clear()

# 修改草图设置，改为xz平面反向
GFE.draft.get_current().set_normal([0.0, 0.0, 0.0], [0.0, -1.0, 0.0], [1.0, 0.0, 0.0])
# 创建“主筋”草图
GFE.draft.get_current().set_snap_object(0)
GFE.draft.get_current().set_operate_mode(1)
GFE.draft.get_current().input(0.0, 0.0)
GFE.draft.get_current().input(0.0, reinforcing_height)

# 创建“主筋”二维模型
shape = GFE.draft.get_current().export()
if not shape.is_null() :
    mgr = GFE.Pre.geometry.geo_mgr()
    mgr.add('reinforcing-bar', shape)


# 平移“主筋”
builder = GFE.geometry.geoprim.builder()
builder.translate(['reinforcing-bar'], [-(stirrup_size/2), -(stirrup_size/2), 0.0], False)

# 阵列“主筋”二维模型，得到一组“主筋”
reinforcing_bar_names = ["reinforcing-bar"]
builder = GFE.geometry.geoprim.builder()
shapes = [GFE.Pre.geometry.geo_mgr().find('reinforcing-bar').shape()]
new_shapes = builder.make_array(shapes, 2, 2, 1, [stirrup_size, stirrup_size, 0.0])
mgr = Pre.geometry.geo_mgr()
for sp in new_shapes :
    if not sp.is_null() :
        name = mgr.auto_name('reinforcing-bar')
        mgr.add(name, sp)
        reinforcing_bar_names.append(name)


# ========== 布尔运算 ============
# 裁剪混凝土柱，（裁剪对象，两个工字钢骨）
builder = GFE.geometry.geoprim.builder()
builder.cut('concrete-pillar', ['I-steel-1', 'I-steel'], False, 'concrete')

#合并两个工字钢骨
builder = GFE.geometry.geoprim.builder()
builder.merge(['I-steel', 'I-steel-1'], True, 'steel-steel')



# ======== 创建材料和截面属性 ===========
# materials[0]是第一个材料q345，[1]是第二个材料c40
# 钢筋材料
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
# 混凝土材料
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
obj.entries = [obj_density, obj_ela]
GFE.Pre.material.mat_mgr().add(obj)


# --------- 创建集合 -------------
# 混凝土集合
geo_obj = GFE.Pre.geometry.geo_mgr().find('concrete')
shapes = GFE.geometry.geotool.children(geo_obj.shape(), 2)
gset_basic = GFE.Pre.set.gset_basic('concrete')
gset_basic.set_shapes(shapes)
GFE.Pre.set.gset_mgr().add(gset_basic)

# 钢骨集合
geo_obj = GFE.Pre.geometry.geo_mgr().find('steel-steel')
shapes = GFE.geometry.geotool.children(geo_obj.shape(), 2)
gset_basic = GFE.Pre.set.gset_basic('steel-steel')
gset_basic.set_shapes(shapes)
GFE.Pre.set.gset_mgr().add(gset_basic)

# 箍筋集合
shapes = []
for name in stirrup_names:
	geo_obj = GFE.Pre.geometry.geo_mgr().find(name)
	if geo_obj is None:
		continue
	edges_sp = GFE.geometry.geotool.children(geo_obj.shape(), 6)
	for e in edges_sp:
		shapes.append(e)
gset_basic = GFE.Pre.set.gset_basic('stirrup')
gset_basic.set_shapes(shapes)
GFE.Pre.set.gset_mgr().add(gset_basic)

# 主筋集合
shapes = []
for name in reinforcing_bar_names:
    geo_obj = GFE.Pre.geometry.geo_mgr().find(name)
    if geo_obj is None:
        continue
    edges_sp = GFE.geometry.geotool.children(geo_obj.shape(), 6)
    for e in edges_sp:
        shapes.append(e)
gset_basic = GFE.Pre.set.gset_basic('reinforcing-bar')
gset_basic.set_shapes(shapes)
GFE.Pre.set.gset_mgr().add(gset_basic)

# ----------- 创建截面 ----------
# 混凝土截面
obj = GFE.Pre.section.property_solid()
obj.name = 'concrete'
obj.elset_name = 'concrete'
obj.mat_name = materials[1][0]
obj.has_thickness = False
obj.thickness = 1.0
GFE.Pre.section.sect_mgr().add(obj)

# 钢筋截面
obj = GFE.Pre.section.property_solid()
obj.name = 'steel-steel'
obj.elset_name = 'steel-steel'
obj.mat_name = materials[0][0]
obj.has_thickness = False
obj.thickness = 1.0
GFE.Pre.section.sect_mgr().add(obj)

# 箍筋截面
obj = GFE.Pre.section.property_beam()
obj.name = 'stirrup'
obj.elset_name = 'stirrup'
obj.shape = 3
obj.mat_name = materials[0][0]
obj.fiber_num = 1
obj.shape_params = [stirrup_section_radius]
obj.params = []
obj.direction = [0.0, 0.0, 1.0]
obj.shear = [8.3873e+06, 8.3873e+06]
obj.Ecc = [0.0, 0.0, 0.0, 0.0]
GFE.Pre.section.sect_mgr().add(obj)

# 主筋截面
obj = GFE.Pre.section.property_beam()
obj.name = 'reinforcing-bar'
obj.elset_name = 'reinforcing-bar'
obj.shape = 3
obj.mat_name = materials[0][0]
obj.fiber_num = 1
obj.shape_params = [reinforcing_section_radius]
obj.params = []
obj.direction = [1.0, 0.0, 0.0]
obj.shear = [3.64032e+07, 3.64032e+07]
obj.Ecc = [0.0, 0.0, 0.0, 0.0]
GFE.Pre.section.sect_mgr().add(obj)


# ============== 合并模型 ==============
# 合并混凝土和钢筋
builder = GFE.geometry.geoprim.builder()
builder.merge(['concrete', 'steel-steel'], True,'steel-concrete')

# 合并主筋和箍筋
merge_stirrup_reinforcing_names = []
merge_stirrup_reinforcing_names.extend(stirrup_names)   # 追加方式添加
merge_stirrup_reinforcing_names.extend(reinforcing_bar_names)   # 追加方式添加
builder = GFE.geometry.geoprim.builder()
builder.merge(merge_stirrup_reinforcing_names, True,'reinforcement-cage')


# ================= 边界与荷载 =================
# 创建底面集合
geo_obj = GFE.Pre.geometry.geo_mgr().find('steel-concrete')
minz = 1e10
bottom_face = []
# 遍历几何体的所有面
for f in GFE.geometry.geotool.children(geo_obj.shape(), 4):
	fz = GFE.geometry.geotool.centre_of_mass(f)[2] # 获取当前面 f 的 z 坐标(质心z值)
	if minz-0.1< fz < minz+0.1:     # 多个底面
		bottom_face.append(f)
	elif fz < minz-0.1:
		bottom_face = []
		minz = fz
		bottom_face.append(f)
# 将底面几何添加到集合
GFE.Pre.set.gset_mgr().add("bc-base", bottom_face)
print(f'底面的数量:{len(bottom_face)}')

# 创建底面约束
obj = GFE.Pre.boundary.boundary()
obj.name = 'BC-base'
obj.type = 0
obj.set = 'bc-base'
obj.valid_dof = 0
obj.value = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
obj.amplitude = ''
obj.value_im = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
obj.amplitude_im = ''
obj.distribution = ''
GFE.Pre.boundary.bc_mgr().add(obj)

# 创建整个模型集合（混凝土钢筋）
geo_obj = GFE.Pre.geometry.geo_mgr().find('steel-concrete')
shapes = GFE.geometry.geotool.children(geo_obj.shape(), 2)
gset_basic = GFE.Pre.set.gset_basic('All')
gset_basic.set_shapes(shapes)
GFE.Pre.set.gset_mgr().add(gset_basic)

# 创建惯性力
obj = GFE.Pre.boundary.boundary()
obj.name = 'GRA'
obj.type = 7
obj.set = 'All'
obj.valid_dof = 0
obj.value = [0.0, 0.0, -9.8]
obj.amplitude = ''
obj.value_im = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
obj.amplitude_im = ''
obj.distribution = ''
GFE.Pre.boundary.bc_mgr().add(obj)


# 压力1表面集
surf_mgr = GFE.Pre.surface.surf_mgr()
obj = GFE.Pre.surface.geometry_surface('pressure')
# 1.找到压力面的z值
# 已在移除中间部分箍筋代码处定义steel_2_maxz
# 2.查找两个压力面
need_faces_id = []
geo_obj = GFE.Pre.geometry.geo_mgr().find('steel-concrete')
for f in GFE.geometry.geotool.children(geo_obj.shape(), 4):
	fz = GFE.geometry.geotool.centre_of_mass(f)[2] # 获取当前面 f 的 z 坐标(质心z值)
	fy = GFE.geometry.geotool.centre_of_mass(f)[1] # 获取当前面 f 的 y 坐标(质心y值)
	if fz < steel_2_maxz+1 and fz > steel_2_maxz-1 and (fy < -(concrete_size/2) or fy > (concrete_size/2)):  #fz会因为精度问题找不到，需增加容差
        # 3.获取面形状id
		id = GFE.geometry.geotool.get_id_by_shape(f)
		need_faces_id.append(id)  	#添加
print(f'压力面1的数量：{len(need_faces_id)}，面id：{need_faces_id}')
# 4.配置obj.data
# 核心逻辑：几何体id+遍历need_faces_id每个子列表f，取f[-1]（最后一个元素），和0(面模式)，组成新列表
obj.data = [[geo_obj.id()] + [f[-1], 0] for f in need_faces_id]
surf_mgr.add(obj)


# 压力2表面集
surf_mgr = GFE.Pre.surface.surf_mgr()
obj = GFE.Pre.surface.geometry_surface('pressure-2')
from GFE.geometry import geotool
need_faces_id = []
geo_obj = GFE.Pre.geometry.geo_mgr().find('steel-concrete')
maxz = -1e10
# 1.找到压力面
for f in GFE.geometry.geotool.children(geo_obj.shape(), 4):
	fz = GFE.geometry.geotool.centre_of_mass(f)[2] # 获取当前面 f 的 z 坐标(质心z值)
	if maxz-0.1< fz < maxz+0.1:		# 多个面
		# 2.获取面形状id
		id = GFE.geometry.geotool.get_id_by_shape(f)
		need_faces_id.append(id)  #添加
	elif fz > maxz+0.1:
		need_faces_id = []
		maxz = fz
		id = GFE.geometry.geotool.get_id_by_shape(f)
		need_faces_id.append(id)  #添加
print(f'压力面2的数量:{len(need_faces_id)}, 面id:{need_faces_id}')
# 3.配置obj.data
obj.data = [[geo_obj.id()] + [f[-1], 0] for f in need_faces_id]
surf_mgr.add(obj)


# 压力1
obj = GFE.Pre.boundary.boundary()
obj.type = 6
obj.name = 'PRESSURE'
obj.set = 'pressure'
obj.valid_dof = 0
obj.value = [pressure_value_steel]
obj.amplitude = ''
obj.value_im = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
obj.amplitude_im = ''
obj.distribution = ''
GFE.Pre.boundary.bc_mgr().add(obj)

# 压力2
obj = GFE.Pre.boundary.boundary()
obj.type = 6
obj.name = 'PRESSURE-2'
obj.set = 'pressure-2'
obj.valid_dof = 0
obj.value = [pressure_value_concrete]
obj.amplitude = ''
obj.value_im = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
obj.amplitude_im = ''
obj.distribution = ''
GFE.Pre.boundary.bc_mgr().add(obj)


# =========== 静力场输出 =============
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

# ============ 分析步 ============
# 静力分析步
obj = GFE.Pre.step.static_general_step()
obj.name = 'Static-1'
obj.description = ''
obj.nlgeom = False
obj.init_inc = 1.0
obj.period = 1.0
obj.min_inc = 1e-05
obj.max_inc = 1.0
GFE.Pre.step.step_mgr().add(obj)

# 模态分析步
obj = GFE.Pre.step.frequency_step()
obj.name = 'Modal-1'
obj.description = ''
obj.nlgeom = False
obj.eigen = 10
GFE.Pre.step.step_mgr().add(obj)



# ============ 相互作用 ===========
# 创建钢筋笼集合（合并两个已有集合）
edges_id = []
find_stirrup_set = GFE.Pre.set.gset_mgr().find('stirrup')
id1 = find_stirrup_set.get_shapes_id()
find_reinforcing_set = GFE.Pre.set.gset_mgr().find('reinforcing-bar')
id2 = find_reinforcing_set.get_shapes_id()
for e in id1:
    edges_id.append(e)
for e in id2:
    edges_id.append(e)
gset_basic = GFE.Pre.set.gset_basic('reinforcement-cage')
gset_basic.set_shapes_id(edges_id)
GFE.Pre.set.gset_mgr().add(gset_basic)

# 创建嵌入区域
obj = GFE.Pre.interaction.embed()
obj.id = 1
obj.name = 'Embed-1'
obj.host_name = 'concrete'
obj.roundoff_tolerance = 1e-6
obj.exterior_tolerance = 0.05
obj.embedded_names = ['reinforcement-cage']
GFE.Pre.interaction.embed_mgr().add(obj)


# ============= 创建工况 ============
# 创建模态工况
obj = GFE.Pre.case.case()
obj.name = 'model'
obj.steps = ['Initial', 'Modal-1']
obj.bcs['Initial'] = ['BC-base']
obj.bcs['Modal-1'] = []
obj.initialConditions['Initial'] = []
obj.fieldReqs['Modal-1'] = ['FO-Static']
obj.histReqs['Modal-1'] = []
obj.elemAdd['Modal-1'] = []
obj.elemDel['Modal-1'] = []
GFE.Pre.case.case_mgr().add(obj)

# 创建静力工况
obj = GFE.Pre.case.case()
obj.name = 'static'
obj.steps = ['Initial', 'Static-1']
obj.bcs['Initial'] = ['BC-base']
obj.bcs['Static-1'] = ['GRA', 'PRESSURE-2', 'PRESSURE']
obj.initialConditions['Initial'] = []
obj.fieldReqs['Static-1'] = ['FO-Static']
obj.histReqs['Static-1'] = []
obj.elemAdd['Static-1'] = []
obj.elemDel['Static-1'] = []
GFE.Pre.case.case_mgr().add(obj)


# =========== 网格划分 ============
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

generator.mesh(['steel-concrete'], controller)
generator.mesh(['reinforcement-cage'], controller)


# ============ 作业管理器 ============
# 写出inp文件
from GFE.io import inpio
inpwriter = inpio.writer(inp_path_static)
inpwriter.set_case('static')
inpwriter.perform()

inpwriter = inpio.writer(inp_path_model)
inpwriter.set_case('model')
inpwriter.perform()
```
