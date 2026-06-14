# GFE2026-CM-ch01-CM1
> 来源：E:\GFE2026\典型案例与教程\第1章 球铰支座静力及模态分析案例\CM1.py（GFE2026 官方典型案例命令流，v3.x 代际金标准）。raw 不可变源副本，2026-06-11 入库。

```python
import GFE
from GFE import *
from GFE.Pre import *
from GFE.occ import *
GFE.Pre.document.set_application_by_ui()
GFE.Pre.document.set_application_by_ui()
import GFE
from GFE import *
from GFE.Pre import *
from GFE.occ import *
GFE.Pre.document.set_application_by_ui()
GFE.Pre.document.set_application_by_ui()
GFE.Pre.document.set_application_by_ui()
GFE.Pre.document.set_application_by_ui()
GFE.Pre.document.set_application_by_ui()
import GFE
from GFE import *
from GFE.Pre import *
from GFE.occ import *
import GFE
from GFE import *
from GFE.Pre import *
from GFE.occ import *
import GFE
from GFE import *
from GFE.Pre import *
from GFE.occ import *
import GFE
from GFE import *
from GFE.Pre import *
from GFE.occ import *

import os
import sys

os.environ['PYTHONUTF8'] = '1'
os.environ['PYTHONIOENCODING'] = 'utf-8'
# 强制设置C++运行时的系统编码为UTF8
if sys.platform == "win32":
    os.system('chcp 65001 >nul 2>&1')
# 获取当前exe目录
current_path = os.path.abspath(sys.executable)
# 获取上一级目录
parent_path = os.path.dirname(current_path)
parent_path = os.path.dirname(parent_path)
plugin_dir = os.path.join(parent_path, "典型案例与教程")
plugin_dir2 = os.path.join(plugin_dir, "第1章")
inp_path1 = os.path.join(plugin_dir2, "Model-1-modal-2.inp")
inp_path1 = os.path.abspath(inp_path1)
inp_path2 = os.path.join(plugin_dir2, "Case-dyna.inp")
inp_path2 = os.path.abspath(inp_path2)


# Make sphere
sp = occ.brep_prim.make_sphere(200)
if not sp.is_null() :
    mgr = Pre.geometry.geo_mgr()
    name = mgr.auto_name('Sphere')
    mgr.add(name, sp)
# Make sphere
sp = occ.brep_prim.make_sphere(160)
if not sp.is_null() :
    mgr = Pre.geometry.geo_mgr()
    name = mgr.auto_name('Sphere')
    mgr.add(name, sp)
GFE.Pre.geometry.geo_mgr().rename('Sphere-1', 'ball-200')

GFE.Pre.mesh.mesh_mgr().rename('Sphere-1', 'ball-200')

GFE.Pre.geometry.geo_mgr().rename('Sphere-2', 'ball-160')

GFE.Pre.mesh.mesh_mgr().rename('Sphere-2', 'ball-160')


# cut
builder = GFE.geometry.geoprim.builder()
builder.cut('ball-200', ['ball-160'], False)

GFE.Pre.geometry.geo_mgr().rename('BoolCut-1', 'ball')

GFE.Pre.mesh.mesh_mgr().rename('BoolCut-1', 'ball')

# Make cylinder
sp = occ.brep_prim.make_cylinder(80, 400)
if not sp.is_null() :
    mgr = Pre.geometry.geo_mgr()
    name = mgr.auto_name('Cylinder')
    mgr.add(name, sp)
GFE.Pre.geometry.geo_mgr().rename('Cylinder-1', 'columu-80-400')

GFE.Pre.mesh.mesh_mgr().rename('Cylinder-1', 'columu-80-400')

# Make cylinder
sp = occ.brep_prim.make_cylinder(100, 400)
if not sp.is_null() :
    mgr = Pre.geometry.geo_mgr()
    name = mgr.auto_name('Cylinder')
    mgr.add(name, sp)
GFE.Pre.geometry.geo_mgr().rename('Cylinder-1', 'columu-100-400')

GFE.Pre.mesh.mesh_mgr().rename('Cylinder-1', 'columu-100-400')


# cut
builder = GFE.geometry.geoprim.builder()
builder.cut('columu-100-400', ['columu-80-400'], False)

GFE.Pre.geometry.geo_mgr().rename('BoolCut-1', 'pipe-1')

GFE.Pre.mesh.mesh_mgr().rename('BoolCut-1', 'pipe-1')

GFE.Pre.geometry.geo_mgr().rename('pipe-1', 'pipe1')

GFE.Pre.mesh.mesh_mgr().rename('pipe-1', 'pipe1')


# cut
builder = GFE.geometry.geoprim.builder()
builder.cut('pipe1', ['ball-200'], False)

GFE.Pre.geometry.geo_mgr().rename('BoolCut-1', 'pipe1-1')

GFE.Pre.mesh.mesh_mgr().rename('BoolCut-1', 'pipe1-1')

# Array selected shape
shape_ids = [[7, 0, 1]]
builder = GFE.geometry.geoprim.builder()
gt = GFE.geometry.geotool
shapes = [gt.get_shape_by_id(id[0], id[1], id[2]) for id in shape_ids]
new_shapes = builder.make_round_array(shapes, 2, -0.785398, [0.0, 0.0, 0.0], [1.0, 0.0, 0.0])
mgr = Pre.geometry.geo_mgr()
for sp in new_shapes :
    if not sp.is_null() :
        mgr.add(mgr.auto_name('Array'), sp)


# Array selected shape
shape_ids = [[7, 0, 1]]
builder = GFE.geometry.geoprim.builder()
gt = GFE.geometry.geotool
shapes = [gt.get_shape_by_id(id[0], id[1], id[2]) for id in shape_ids]
new_shapes = builder.make_round_array(shapes, 2, 0.785398, [0.0, 0.0, 0.0], [1.0, 0.0, 0.0])
mgr = Pre.geometry.geo_mgr()
for sp in new_shapes :
    if not sp.is_null() :
        mgr.add(mgr.auto_name('Array'), sp)


GFE.Pre.geometry.geo_mgr().rename('Array-1', 'pipe1-2')

GFE.Pre.mesh.mesh_mgr().rename('Array-1', 'pipe1-2')

GFE.Pre.geometry.geo_mgr().rename('Array-2', 'pipe1-3')

GFE.Pre.mesh.mesh_mgr().rename('Array-2', 'pipe1-3')

# Array selected shape
shape_ids = [[7, 0, 1]]
builder = GFE.geometry.geoprim.builder()
gt = GFE.geometry.geotool
shapes = [gt.get_shape_by_id(id[0], id[1], id[2]) for id in shape_ids]
new_shapes = builder.make_round_array(shapes, 2, -1.0472, [0.0, 0.0, 0.0], [0.0, 1.0, 0.0])
mgr = Pre.geometry.geo_mgr()
for sp in new_shapes :
    if not sp.is_null() :
        mgr.add(mgr.auto_name('Array'), sp)


GFE.Pre.geometry.geo_mgr().rename('Array-1', 'pipe1-4')

GFE.Pre.mesh.mesh_mgr().rename('Array-1', 'pipe1-4')

# Array selected shape
shape_ids = [[10, 0, 1]]
builder = GFE.geometry.geoprim.builder()
gt = GFE.geometry.geotool
shapes = [gt.get_shape_by_id(id[0], id[1], id[2]) for id in shape_ids]
new_shapes = builder.make_round_array(shapes, 2, 0.785398, [0.0, 0.0, 0.0], [0.0, 0.0, 1.0])
mgr = Pre.geometry.geo_mgr()
for sp in new_shapes :
    if not sp.is_null() :
        mgr.add(mgr.auto_name('Array'), sp)


# Array selected shape
shape_ids = [[10, 0, 1]]
builder = GFE.geometry.geoprim.builder()
gt = GFE.geometry.geotool
shapes = [gt.get_shape_by_id(id[0], id[1], id[2]) for id in shape_ids]
new_shapes = builder.make_round_array(shapes, 2, -0.785398, [0.0, 0.0, 0.0], [0.0, 0.0, 1.0])
mgr = Pre.geometry.geo_mgr()
for sp in new_shapes :
    if not sp.is_null() :
        mgr.add(mgr.auto_name('Array'), sp)


GFE.Pre.geometry.geo_mgr().rename('Array-1', 'pipe1-5')

GFE.Pre.mesh.mesh_mgr().rename('Array-1', 'pipe1-5')

GFE.Pre.geometry.geo_mgr().rename('Array-2', 'pipe1-6')

GFE.Pre.mesh.mesh_mgr().rename('Array-2', 'pipe1-6')

# Make cylinder
sp = occ.brep_prim.make_cylinder(100, 300)
if not sp.is_null() :
    mgr = Pre.geometry.geo_mgr()
    name = mgr.auto_name('Cylinder')
    mgr.add(name, sp)
GFE.Pre.geometry.geo_mgr().rename('Cylinder-1', 'columu2-100-300')

GFE.Pre.mesh.mesh_mgr().rename('Cylinder-1', 'columu2-100-300')

# Make cylinder
sp = occ.brep_prim.make_cylinder(80, 300)
if not sp.is_null() :
    mgr = Pre.geometry.geo_mgr()
    name = mgr.auto_name('Cylinder')
    mgr.add(name, sp)
GFE.Pre.geometry.geo_mgr().rename('Cylinder-1', 'columu2-80-300')

GFE.Pre.mesh.mesh_mgr().rename('Cylinder-1', 'columu2-80-300')


# cut
builder = GFE.geometry.geoprim.builder()
builder.cut('columu2-100-300', ['columu2-80-300'], False)

GFE.Pre.geometry.geo_mgr().rename('BoolCut-1', 'pipe2')

GFE.Pre.mesh.mesh_mgr().rename('BoolCut-1', 'pipe2')


# translate
builder = GFE.geometry.geoprim.builder()
builder.translate(['pipe2'], [0.0, 0.0, 300.0], False)


# translate
builder = GFE.geometry.geoprim.builder()
builder.translate(['pipe2'], [0.0, 0.0, -300.0], False)


# translate
builder = GFE.geometry.geoprim.builder()
builder.translate(['pipe2'], [0.0, 0.0, -300.0], False)


# cut
builder = GFE.geometry.geoprim.builder()
builder.cut('pipe2', ['ball-200'], False)

GFE.Pre.geometry.geo_mgr().rename('BoolCut-1', 'pipe2-1')

GFE.Pre.mesh.mesh_mgr().rename('BoolCut-1', 'pipe2-1')

# Make cylinder
sp = occ.brep_prim.make_cylinder(75, 400)
if not sp.is_null() :
    mgr = Pre.geometry.geo_mgr()
    name = mgr.auto_name('Cylinder')
    mgr.add(name, sp)
GFE.Pre.geometry.geo_mgr().rename('Cylinder-1', 'columu3-75-400')

GFE.Pre.mesh.mesh_mgr().rename('Cylinder-1', 'columu3-75-400')

# Make cylinder
sp = occ.brep_prim.make_cylinder(60, 400)
if not sp.is_null() :
    mgr = Pre.geometry.geo_mgr()
    name = mgr.auto_name('Cylinder')
    mgr.add(name, sp)
GFE.Pre.geometry.geo_mgr().rename('Cylinder-1', 'columu60-400')

GFE.Pre.mesh.mesh_mgr().rename('Cylinder-1', 'columu60-400')

GFE.Pre.geometry.geo_mgr().rename('columu60-400', 'columu3-60-400')

GFE.Pre.mesh.mesh_mgr().rename('columu60-400', 'columu3-60-400')


# cut
builder = GFE.geometry.geoprim.builder()
builder.cut('columu3-75-400', ['columu3-60-400'], False)

GFE.Pre.geometry.geo_mgr().rename('BoolCut-1', 'pipe3')

GFE.Pre.mesh.mesh_mgr().rename('BoolCut-1', 'pipe3')


# cut
builder = GFE.geometry.geoprim.builder()
builder.cut('pipe3', ['ball-200'], False)

GFE.Pre.geometry.geo_mgr().rename('BoolCut-1', 'pipe3-1')

GFE.Pre.mesh.mesh_mgr().rename('BoolCut-1', 'pipe3-1')

GFE.draft.get_current().set_snap_tolerance(0.460829)
GFE.draft.get_current().set_snap_tolerance(0.437637)
# Array selected shape
shape_ids = [[20, 0, 1]]
builder = GFE.geometry.geoprim.builder()
gt = GFE.geometry.geotool
shapes = [gt.get_shape_by_id(id[0], id[1], id[2]) for id in shape_ids]
new_shapes = builder.make_round_array(shapes, 2, 1.5708, [0.0, 0.0, 0.0], [0.0, 1.0, 0.0])
mgr = Pre.geometry.geo_mgr()
for sp in new_shapes :
    if not sp.is_null() :
        mgr.add(mgr.auto_name('Array'), sp)


GFE.Pre.geometry.geo_mgr().rename('Array-1', 'pipe3-1-real')

GFE.Pre.mesh.mesh_mgr().rename('Array-1', 'pipe3-1-real')

# Make cylinder
sp = occ.brep_prim.make_cylinder(50, 400)
if not sp.is_null() :
    mgr = Pre.geometry.geo_mgr()
    name = mgr.auto_name('Cylinder')
    mgr.add(name, sp)
GFE.Pre.geometry.geo_mgr().rename('Cylinder-1', 'columu4-50-400')

GFE.Pre.mesh.mesh_mgr().rename('Cylinder-1', 'columu4-50-400')

# Make cylinder
sp = occ.brep_prim.make_cylinder(40, 400)
if not sp.is_null() :
    mgr = Pre.geometry.geo_mgr()
    name = mgr.auto_name('Cylinder')
    mgr.add(name, sp)
GFE.Pre.geometry.geo_mgr().rename('Cylinder-1', 'columu4-40-400')

GFE.Pre.mesh.mesh_mgr().rename('Cylinder-1', 'columu4-40-400')


# cut
builder = GFE.geometry.geoprim.builder()
builder.cut('columu4-50-400', ['columu4-40-400'], False)

GFE.Pre.geometry.geo_mgr().rename('BoolCut-1', 'pipe4')

GFE.Pre.mesh.mesh_mgr().rename('BoolCut-1', 'pipe4')


# cut
builder = GFE.geometry.geoprim.builder()
builder.cut('pipe4', ['ball-200'], False)

GFE.Pre.geometry.geo_mgr().rename('BoolCut-1', 'pipe4-or')

GFE.Pre.mesh.mesh_mgr().rename('BoolCut-1', 'pipe4-or')
GFE.Pre.geometry.geo_mgr().rename('pipe3-1', 'pipe3-1-or')

GFE.Pre.mesh.mesh_mgr().rename('pipe3-1', 'pipe3-1-or')

GFE.Pre.geometry.geo_mgr().rename('pipe3-1-real', 'pipe3-1')

GFE.Pre.mesh.mesh_mgr().rename('pipe3-1-real', 'pipe3-1')

# Array selected shape
shape_ids = [[24, 0, 1]]
builder = GFE.geometry.geoprim.builder()
gt = GFE.geometry.geotool
shapes = [gt.get_shape_by_id(id[0], id[1], id[2]) for id in shape_ids]
new_shapes = builder.make_round_array(shapes, 2, 1.5708, [0.0, 0.0, 0.0], [0.0, 0.0, 1.0])
mgr = Pre.geometry.geo_mgr()
for sp in new_shapes :
    if not sp.is_null() :
        mgr.add(mgr.auto_name('Array'), sp)


GFE.Pre.mesh.mesh_mgr().delete(['Array-1'])

GFE.Pre.geometry.geo_mgr().delete(['Array-1'])

# Array selected shape
shape_ids = [[24, 0, 1]]
builder = GFE.geometry.geoprim.builder()
gt = GFE.geometry.geotool
shapes = [gt.get_shape_by_id(id[0], id[1], id[2]) for id in shape_ids]
new_shapes = builder.make_round_array(shapes, 2, 1.5708, [0.0, 0.0, 0.0], [1.0, 0.0, 0.0])
mgr = Pre.geometry.geo_mgr()
for sp in new_shapes :
    if not sp.is_null() :
        mgr.add(mgr.auto_name('Array'), sp)


# Array selected shape
shape_ids = [[24, 0, 1]]
builder = GFE.geometry.geoprim.builder()
gt = GFE.geometry.geotool
shapes = [gt.get_shape_by_id(id[0], id[1], id[2]) for id in shape_ids]
new_shapes = builder.make_round_array(shapes, 2, -1.5708, [0.0, 0.0, 0.0], [1.0, 0.0, 0.0])
mgr = Pre.geometry.geo_mgr()
for sp in new_shapes :
    if not sp.is_null() :
        mgr.add(mgr.auto_name('Array'), sp)



# cut
builder = GFE.geometry.geoprim.builder()
builder.cut('Array-1', ['ball-200'], False)

GFE.Pre.geometry.geo_mgr().rename('BoolCut-1', 'pipe4-1')

GFE.Pre.mesh.mesh_mgr().rename('BoolCut-1', 'pipe4-1')


# cut
builder = GFE.geometry.geoprim.builder()
builder.cut('Array-2', ['ball-200'], False)

GFE.Pre.geometry.geo_mgr().rename('BoolCut-1', 'pipe4-2')

GFE.Pre.mesh.mesh_mgr().rename('BoolCut-1', 'pipe4-2')


# rotate
builder = GFE.geometry.geoprim.builder()
builder.rotate(['columu4-50-400'], [0.0, 0.0, 0.0], [1.0, 0.0, 0.0], 90.0, True)


# rotate
builder = GFE.geometry.geoprim.builder()
builder.rotate(['columu4-50-400'], [0.0, 0.0, 0.0], [1.0, 0.0, 0.0], -90.0, True)

GFE.Pre.geometry.geo_mgr().rename('Trsf-columu4-50-400-1', 'pipe4-1out')

GFE.Pre.mesh.mesh_mgr().rename('Trsf-columu4-50-400-1', 'pipe4-1out')

GFE.Pre.geometry.geo_mgr().rename('Trsf-columu4-50-400-2', 'pipe4-2out')

GFE.Pre.mesh.mesh_mgr().rename('Trsf-columu4-50-400-2', 'pipe4-2out')
GFE.draft.get_current().set_snap_tolerance(0.439078)
GFE.draft.get_current().set_snap_tolerance(0.417973)
# Make box
sp = occ.brep_prim.make_box(800, 30, 300)
if not sp.is_null() :
    mgr = Pre.geometry.geo_mgr()
    name = mgr.auto_name('Box')
    mgr.add(name, sp)

# translate
builder = GFE.geometry.geoprim.builder()
builder.translate(['Box-1'], [-400.0, -15.0, -300.0], False)

# Make wedge
sp = occ.brep_prim.make_wedge(30, 120, 120, 0, 30, 0, 0)
if not sp.is_null() :
    mgr = Pre.geometry.geo_mgr()
    name = mgr.auto_name('Wedge')
    mgr.add(name, sp)

# rotate
builder = GFE.geometry.geoprim.builder()
builder.rotate(['Wedge-1'], [0.0, 0.0, 0.0], [0.0, 0.0, 1.0], -90.0, False)


# rotate
builder = GFE.geometry.geoprim.builder()
builder.rotate(['Wedge-1'], [0.0, 0.0, 0.0], [0.0, 1.0, 0.0], 180.0, False)


# translate
builder = GFE.geometry.geoprim.builder()
builder.translate(['Wedge-1'], [440.0, 15.0, 40.0], False)


# translate
builder = GFE.geometry.geoprim.builder()
builder.translate(['Wedge-1'], [-40.0, 0.0, -40.0], False)


# cut
builder = GFE.geometry.geoprim.builder()
builder.cut('Box-1', ['Wedge-1'], False)


# rotate
builder = GFE.geometry.geoprim.builder()
builder.rotate(['Wedge-1'], [0.0, 0.0, 0.0], [0.0, 0.0, 1.0], 180.0, False)


# cut
builder = GFE.geometry.geoprim.builder()
builder.cut('BoolCut-1', ['Wedge-1'], False)

GFE.Pre.geometry.geo_mgr().rename('BoolCut-2', 'base1')

GFE.Pre.mesh.mesh_mgr().rename('BoolCut-2', 'base1')


# rotate
builder = GFE.geometry.geoprim.builder()
builder.rotate(['base1'], [0.0, 0.0, 0.0], [0.0, 0.0, 1.0], -45.0, False)

# Array selected shape
shape_ids = [[36, 0, 1]]
builder = GFE.geometry.geoprim.builder()
gt = GFE.geometry.geotool
shapes = [gt.get_shape_by_id(id[0], id[1], id[2]) for id in shape_ids]
new_shapes = builder.make_round_array(shapes, 2, 1.5708, [0.0, 0.0, 0.0], [0.0, 0.0, 1.0])
mgr = Pre.geometry.geo_mgr()
for sp in new_shapes :
    if not sp.is_null() :
        mgr.add(mgr.auto_name('Array'), sp)


GFE.Pre.geometry.geo_mgr().rename('Array-3', 'base1-1')

GFE.Pre.mesh.mesh_mgr().rename('Array-3', 'base1-1')

# Make box
sp = occ.brep_prim.make_box(800, 30, 215)
if not sp.is_null() :
    mgr = Pre.geometry.geo_mgr()
    name = mgr.auto_name('Box')
    mgr.add(name, sp)

# translate
builder = GFE.geometry.geoprim.builder()
builder.translate(['Box-2'], [-400.0, -15.0, -385.0], False)

GFE.draft.get_current().set_snap_tolerance(0.439078)
GFE.draft.get_current().set_snap_tolerance(0.417973)

# translate
builder = GFE.geometry.geoprim.builder()
builder.translate(['Box-2'], [0.0, 0.0, 85.0], False)


# translate
builder = GFE.geometry.geoprim.builder()
builder.translate(['Wedge-1'], [0.0, 0.0, -85.0], False)


# cut
builder = GFE.geometry.geoprim.builder()
builder.cut('Box-2', ['Wedge-1'], False)


# rotate
builder = GFE.geometry.geoprim.builder()
builder.rotate(['Wedge-1'], [0.0, 0.0, 0.0], [0.0, 0.0, 1.0], 180.0, False)


# cut
builder = GFE.geometry.geoprim.builder()
builder.cut('BoolCut-2', ['Wedge-1'], False)

GFE.Pre.geometry.geo_mgr().rename('BoolCut-3', 'base2')

GFE.Pre.mesh.mesh_mgr().rename('BoolCut-3', 'base2')

# Array selected shape
shape_ids = [[40, 0, 1]]
builder = GFE.geometry.geoprim.builder()
gt = GFE.geometry.geotool
shapes = [gt.get_shape_by_id(id[0], id[1], id[2]) for id in shape_ids]
new_shapes = builder.make_round_array(shapes, 2, 1.5708, [0.0, 0.0, 0.0], [0.0, 0.0, 1.0])
mgr = Pre.geometry.geo_mgr()
for sp in new_shapes :
    if not sp.is_null() :
        mgr.add(mgr.auto_name('Array'), sp)


GFE.Pre.geometry.geo_mgr().rename('Array-3', 'base2-1')

GFE.Pre.mesh.mesh_mgr().rename('Array-3', 'base2-1')


# translate
builder = GFE.geometry.geoprim.builder()
builder.translate(['columu2-100-300'], [0.0, 0.0, -300.0], True)

GFE.Pre.geometry.geo_mgr().rename('Trsf-columu2-100-300-1', 'columu2-100-xia')

GFE.Pre.mesh.mesh_mgr().rename('Trsf-columu2-100-300-1', 'columu2-100-xia')


# cut
builder = GFE.geometry.geoprim.builder()
builder.cut('base1-1', ['columu2-100-xia', 'ball-200'], False)

GFE.Pre.geometry.geo_mgr().rename('BoolCut-3', 'base1-real')

GFE.Pre.mesh.mesh_mgr().rename('BoolCut-3', 'base1-real')

GFE.Pre.geometry.geo_mgr().rename('base1-real', 'base1-1-real')

GFE.Pre.mesh.mesh_mgr().rename('base1-real', 'base1-1-real')


# cut
builder = GFE.geometry.geoprim.builder()
builder.cut('base1', ['columu2-100-xia', 'ball-200'], False)

GFE.Pre.geometry.geo_mgr().rename('BoolCut-3', 'base1-real')

GFE.Pre.mesh.mesh_mgr().rename('BoolCut-3', 'base1-real')


# cut
builder = GFE.geometry.geoprim.builder()
builder.cut('base2', ['columu2-100-xia', 'ball-200'], False)

GFE.Pre.geometry.geo_mgr().rename('BoolCut-3', 'base2-real')

GFE.Pre.mesh.mesh_mgr().rename('BoolCut-3', 'base2-real')


# cut
builder = GFE.geometry.geoprim.builder()
builder.cut('base2-1', ['columu2-100-xia', 'ball-200'], False)

GFE.Pre.geometry.geo_mgr().rename('BoolCut-3', 'base2-1-real')

GFE.Pre.mesh.mesh_mgr().rename('BoolCut-3', 'base2-1-real')


# merge
builder = GFE.geometry.geoprim.builder()
builder.merge(['base2-1-real', 'base2-real', 'base1-real', 'base1-1-real', 'pipe4-2', 'pipe4-1', 'pipe3-1', 'pipe2-1',
'pipe1-6', 'pipe1-5', 'pipe1-4', 'pipe1-3', 'pipe1-2', 'pipe1-1', 'ball'], False)

GFE.Pre.geometry.geo_mgr().rename('Merge-1', 'qiujiao')

GFE.Pre.mesh.mesh_mgr().rename('Merge-1', 'qiujiao')

#mesh
from GFE.geometry import mesh_generator
generator = mesh_generator.generator()
controller = mesh_generator.controller()
controller.number_option = {
'General.ExpertMode' : 1.0,
'General.NumThreads' : 0.0,
'General.Terminal' : 1.0,
'Mesh.Algorithm' : 6.0,
'Mesh.Algorithm3D' : 4.0,
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
'GFE.DefaultSize' : 10.0,
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

generator.mesh(['qiujiao'], controller)
obj = GFE.Pre.material.material()
obj.name = 'Q345'
obj_density = GFE.Pre.material.density()
obj_density.temp_dp = False
obj_density.n_param = 1
obj_density.params = [7.8e-09]
obj_ela = GFE.Pre.material.elastic()
obj_ela.temp_dp = False
obj_ela.n_param = 2
obj_ela.type = 0
obj_ela.moduli_time_scale = 0
obj_ela.compression = False
obj_ela.tension = False
obj_ela.params = [206000.0, 0.25]
obj.entries = [obj_density, obj_ela]
GFE.Pre.material.mat_mgr().add(obj)

#---------手动建模qiujiao全集的代码
# gset_id = [[47, 2, 1], [47, 2, 2], [47, 2, 3], [47, 2, 4], [47, 2, 5], [47, 2, 6], [47, 2, 7], [47, 2, 8],
# [47, 2, 9], [47, 2, 10], [47, 2, 11], [47, 2, 12], [47, 2, 13], [47, 2, 14], [47, 2, 15], [47, 2, 16],
# [47, 2, 17], [47, 2, 18], [47, 2, 19], [47, 2, 20], [47, 2, 21], [47, 2, 22], [47, 2, 23], [47, 2, 24],
# [47, 2, 25], [47, 2, 26], [47, 2, 27], [47, 2, 28], [47, 2, 29], [47, 2, 30], [47, 2, 31], [47, 2, 32],
# [47, 2, 33], [47, 2, 34], [47, 2, 35], [47, 2, 36], [47, 2, 37], [47, 2, 38], [47, 2, 39]]
# gset = GFE.Pre.set.gset_basic('qiujiao')
# gset.set_shapes_id(gset_id)
# GFE.Pre.set.gset_mgr().add(gset)


#创建整个模型集合（qiujiao）-------------
from GFE.geometry import geotool
geo_obj = GFE.Pre.geometry.geo_mgr().find('qiujiao')
shapes = GFE.geometry.geotool.children(geo_obj.shape(), 2)
gset_basic = GFE.Pre.set.gset_basic('qiujiao')
gset_basic.set_shapes(shapes)
GFE.Pre.set.gset_mgr().add(gset_basic)

obj = GFE.Pre.section.property_solid()
obj.name = 'qiujiao'
obj.elset_name = 'qiujiao'
obj.mat_name = 'Q345'
obj.has_thickness = False
obj.thickness = 1.0
GFE.Pre.section.sect_mgr().add(obj)

#--------------手动建模得到base的代码-------------
#gset_id = [[47, 4, 5], [47, 4, 95], [47, 4, 52], [47, 4, 31], [47, 4, 71], [47, 4, 15], [47, 4, 39], [47, 4, 21],
#[47, 4, 58]]
#gset = GFE.Pre.set.gset_basic('base')
#gset.set_shapes_id(gset_id)
#GFE.Pre.set.gset_mgr().add(gset)


#-------------------------------------边界与荷载--------------------------------------------
#创建底面集合-------------
from GFE.geometry import geotool
geo_obj = GFE.Pre.geometry.geo_mgr().find('qiujiao')  #找到几何
minz = -300  # 最低的面的z坐标
bottom_face = []  # 存储底面几何
# 遍历几何体的所有面
for f in GFE.geometry.geotool.children(geo_obj.shape(), 4):
	fz = GFE.geometry.geotool.centre_of_mass(f)[2] # 获取当前面 f 的 z 坐标(质心z值)
	if fz < minz + 1e-5: # 当前面fz小于最低z值
		#bottom_face = []	#清空
		#minz = fz # 更新最小 z 值
		bottom_face.append(f) # 添加
	#elif abs(fz - minz) <= 1e-6: #等于
	#	bottom_face.append(f) #添加
# 将底面几何添加到集合
GFE.Pre.set.gset_mgr().add("base", bottom_face)
print(f'底面的数量:{len(bottom_face)}')


obj = GFE.Pre.boundary.boundary()
obj.name = 'BC-base'
obj.type = 0
obj.name = 'BC-base'
obj.set = 'base'
obj.valid_dof = 0
obj.value = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
obj.amplitude = ''
obj.value_im = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
obj.amplitude_im = ''
obj.distribution = ''
obj.node_id = []
obj.is_node_set = True
GFE.Pre.boundary.bc_mgr().add(obj)


#--------------手动建模得到PRESSURE集合的代码--------------
# obj = GFE.Pre.surface.geometry_surface('PRESSURE')
# obj.data = [[47, 79, 0], [47, 128, 0], [47, 164, 0], [47, 151, 0], [47, 199, 0], [47, 182, 0], [47, 103, 0], [47, 75, 0],
# [47, 84, 0]]
# obj.to_node_surface = False
# GFE.Pre.surface.surface_mgr().add(obj)

#创建PRESSURE集合-------------
from GFE.geometry import geotool

surf_mgr = GFE.Pre.surface.surf_mgr()
obj = GFE.Pre.surface.geometry_surface('PRESSURE')
geo_obj = GFE.Pre.geometry.geo_mgr().find('qiujiao')  #找到几何
awayR = 400  # 距离球心的面的距离
PRESSURE_face_id = []  # 存储压面几何
# 遍历几何体的所有面
for f in GFE.geometry.geotool.children(geo_obj.shape(), 4):
    fx = GFE.geometry.geotool.centre_of_mass(f)[0] # 获取当前面 f 的 z 坐标(质心z值)
    fy = GFE.geometry.geotool.centre_of_mass(f)[1] # 获取当前面 f 的 z 坐标(质心z值)
    fz = GFE.geometry.geotool.centre_of_mass(f)[2] # 获取当前面 f 的 z 坐标(质心z值)
    faway=(fx**2+fy**2+fz**2)**0.5
    if abs(faway-awayR) < 1e-5: # 距离球心距离400，每根管子都是400长
		#bottom_face = []	#清空
		#minz = fz # 更新最小 z 值
        id = GFE.geometry.geotool.get_id_by_shape(f)
        PRESSURE_face_id.append(id) # 添加
	#elif abs(fz - minz) <= 1e-6: #等于
	#	bottom_face.append(f) #添加
# 将压面几何添加到集合
#GFE.Pre.set.gset_mgr().add("PRESSURE", PRESSURE_face_id)
# 核心逻辑：几何体id+遍历need_faces_id每个子列表f，取f[-1]（最后一个元素），和0(面模式)，组成新列表
obj.data = [[geo_obj.id()] + [f[-1], 0] for f in PRESSURE_face_id]
surf_mgr.add(obj)
print(f'压面的数量:{len(PRESSURE_face_id)}')


obj = GFE.Pre.boundary.boundary()
obj.name = 'PRESSURE'
obj.type = 6
obj.name = 'PRESSURE'
obj.set = 'PRESSURE'
obj.valid_dof = 0
obj.value = [50.0]
obj.amplitude = ''
obj.value_im = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
obj.amplitude_im = ''
obj.distribution = ''
obj.node_id = []
obj.is_node_set = True
GFE.Pre.boundary.bc_mgr().add(obj)

obj = GFE.Pre.boundary.boundary()
obj.name = 'GRA'
obj.type = 7
obj.name = 'GRA'
obj.set = 'qiujiao'
obj.valid_dof = 0
obj.value = [0.0, 0.0, -9800.0]
obj.amplitude = ''
obj.value_im = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
obj.amplitude_im = ''
obj.distribution = ''
obj.node_id = []
obj.is_node_set = True
GFE.Pre.boundary.bc_mgr().add(obj)

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
obj_sub1.name = 'output'
obj_sub1.variables = ['U', 'UR']
obj_sub1.var_option = -1
obj_sub1.reg_type = -1
obj_sub1.nset = ''
obj_sub2 = GFE.Pre.output.element_output()
obj_sub2.name = 'output1'
obj_sub2.variables = ['E', 'S']
obj_sub2.var_option = -1
obj_sub2.reg_type = -1
obj_sub2.elset = ''
obj.sub_output = [obj_sub1, obj_sub2]
GFE.Pre.output.field_mgr().add(obj)

obj = GFE.Pre.step.frequency_step()
obj.name = 'MODAL'
obj.description = ''
obj.nlgeom = False
obj.eigen = 1
GFE.Pre.step.step_mgr().add(obj)

obj = GFE.Pre.step.static_general_step()
obj.name = 'STATIC'
obj.description = ''
#obj.nlgeom = False
obj.init_inc = 1.0
obj.period = 1.0
obj.min_inc = 1e-05
obj.max_inc = 1.0
#obj.gfe_linear = False
GFE.Pre.step.step_mgr().add(obj)

obj = GFE.Pre.case.case()
obj.name = 'modal'
obj.steps = ['Initial', 'MODAL']
obj.bcs['Initial'] = ['BC-base']
obj.bcs['MODAL'] = []
obj.initialConditions['Initial'] = []
obj.fieldReqs['MODAL'] = ['FieldOutput-1']
obj.histReqs['MODAL'] = []
obj.elemAdd['MODAL'] = []
obj.elemDel['MODAL'] = []
GFE.Pre.case.case_mgr().add(obj)

obj = GFE.Pre.case.case()
obj.name = 'static'
obj.steps = ['Initial', 'STATIC']
obj.bcs['Initial'] = ['BC-base']
obj.bcs['STATIC'] = ['PRESSURE', 'GRA']
obj.initialConditions['Initial'] = []
obj.fieldReqs['STATIC'] = ['FieldOutput-1']
obj.histReqs['STATIC'] = []
obj.elemAdd['STATIC'] = []
obj.elemDel['STATIC'] = []
GFE.Pre.case.case_mgr().add(obj)

# write inp
from GFE.io import inpio
inpwriter = inpio.writer(inp_path1)
inpwriter.set_case('modal')
inpwriter.perform()

# write inp
from GFE.io import inpio
inpwriter = inpio.writer(inp_path2)
inpwriter.set_case('static')
inpwriter.perform()
```
