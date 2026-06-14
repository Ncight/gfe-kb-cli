# GFE 命令流工具脚本与实时桥（反编译 / 参数化建模 / 桥）
> 来源：D:\GFE\GFE_KB（gfe-command-stream skill 维护的命令流知识库）。本文件为 raw 检索源副本。


---

## 参数化建模 build_model.py
`03_工具脚本_Bridge\build_model.py`

```python
# ==== build_model.py ====
# -*- coding: utf-8 -*-
# 参数化建模脚本 (ch15 复刻 / SSI 模板)
# 用法: 在 PrePo 命令框 exec(open(r"D:\GFE\build_model.py", encoding="utf-8").read())
#       构建完成后 File→Save 存 .pre (命令流无 save API, 存盘一次点击)。
# "只动细节" = 改下面 PARAMS 区, 重跑即重建。
# 状态标记: [OK]=范式已验证可跑   [TODO]=待逐块实跑验证后再启用
import GFE
import GFE.Pre.material, GFE.Pre.soil, GFE.soil          # 显式导子模块(否则可能漏属性)
GFE.Pre.document.set_application_by_ui()

# ==================== PARAMS (只动这里) ====================
# 土层 (名, ρ[t/m³], E[kPa], ν)  —— 单位制 m-t-kPa, 与 YJK 导入的结构材料一致
SOIL_LAYERS = [
    ('4-3',  1.92, 155152.0,   0.35),
    ('5H-2', 1.94, 278958.0,   0.28),
    ('6H',   1.93, 649522.0,   0.27),
    ('7H-A', 1.91, 988544.0,   0.25),
    ('7H-B', 1.95, 2844141.0,  0.23),
    ('8H',   2.45, 4228332.0,  0.20),
    ('9H',   2.63, 17937652.0, 0.18),
]
SOIL_DEPTH   = [4.72, 9.5, 11.5, 9.5, 1.9, 5.1, 40.0]   # 各层厚度(m), 对应 SOIL_LAYERS
BEDROCK_MAT  = '9H'
DEPTH_DIR    = 2                 # 2 = Z 向
SOIL_PLANE   = (300.0, 300.0)    # 三维土体平面尺寸 L×W (m), 需罩住结构+隧道
SOIL1D_NAME  = 'Soil1D-1'
SOIL3D_NAME  = 'Soil-1'
# =========================================================

# -------- Block 1 [OK]: 土体材料 --------
def _add_soil_mat(name, rho, E, nu):
    m = GFE.Pre.material.material(); m.name = name
    d = GFE.Pre.material.density();  d.temp_dp = False; d.n_param = 1; d.params = [rho]
    e = GFE.Pre.material.elastic();  e.params = [E, nu]       # type 默认 0 线弹性
    m.entries = [e, d]
    GFE.Pre.material.mat_mgr().add(m)

for _n, _r, _e, _v in SOIL_LAYERS:
    _add_soil_mat(_n, _r, _e, _v)

# -------- Block 2 [OK]: 一维土层 + 三维土体 --------
s = GFE.Pre.soil.soil(); s.name = SOIL1D_NAME
s.depth = SOIL_DEPTH
s.materials = [L[0] for L in SOIL_LAYERS]
s.bedrock_mat = BEDROCK_MAT
s.depth_dir = DEPTH_DIR
GFE.Pre.soil.soil_mgr().add(s)

_bb = GFE.soil.box_builder()
_bb.set_height(s.depth, s.depth_dir)
_bb.set_parameter(SOIL_PLANE[0], SOIL_PLANE[1])
_shape = _bb.build()
_dbd = GFE.soil.data_builder()
_dbd.dimension = 3
_dbd.name = SOIL3D_NAME
_dbd.layer_shape = _shape
_dbd.layer_material = s.materials
_dbd.build()

print("[build_model] Block1+2 done: %d soil mats + %s + %s" % (len(SOIL_LAYERS), SOIL1D_NAME, SOIL3D_NAME))

# ============ 以下为待验证块 (逐块实跑确认后从注释启用) ============
# Block 3 [TODO 几何]: 隧道/道床/轨道 —— 草图器 GFE.draft 未实证, 建议先 GUI 画好再继续
# Block 4 [TODO]: 土体定位 geoprim.builder().translate([SOIL3D_NAME], vec)  + 裁剪 .cut(SOIL3D_NAME, ['BasementBoundary'], True)
# Block 5 [TODO]: 集合 gset_mgr (隧道/道床/左右轨, ⚠按名或几何选)
# Block 6 [TODO]: 钢轨等截面属性 sect_mgr
# Block 7 [TODO]: 相互作用 —— orientation(data=[1,0,0,0,1,0,0,0,0]) + connector_behavior(behaviors=[connector_elastic, connector_damping]) + connector_section + tie(contact_pair.search_face)
# Block 8 [TODO]: 列车荷载 boundary(type=9, value=[1,车速,...], track_coord) + 轨道两端全约束
# Block 9 [TODO]: 网格 mesh_generator (主体~1 / 土~3 / 隧道~1 / 道床~0.6扫掠 / 钢轨)
# Block 10[TODO]: 人工边界 artbc.art_bc(structure=SUPERSTRU, surface=<边界面集>)
# Block 11[TODO]: 分析步 dynamic_explicit_step(period=15, mass_scaling(target_time=5e-5,frequency=100,type=1))
# Block 12[TODO]: 场输出(节点U) + 工况 case(steps=['Initial','Dyna-1'], set_bcs/set_artbc/set_fieldReqs(步,[名]))
# 完成后 File→Save 存 .pre

```


---

## 模型反编译器 gfe_decompile.py
`03_工具脚本_Bridge\gfe_decompile.py`

```python
# ==== gfe_decompile.py ====
# -*- coding: utf-8 -*-
# GFE 模型反编译器 v2(防闪退) —— 读"当前已加载模型"状态, dump 成等价命令流素材
# 用法(每章一次): 在 PrePo 打开该章 .pre, 命令框执行:
#     MODEL='ch01_Chapter1'; exec(open(r"D:\GFE\gfe_decompile.py", encoding="utf-8").read())
# 产出: D:\GFE\decomp\<MODEL>.txt  (每行即时 flush, 即便崩溃也能定位崩在哪一步)
# 安全策略: 只调名字像管理器的 getter(*_mgr/*_manager), 不盲调任意函数;
#           geometry/mesh 管理器只列名(其对象属性重/易崩, 不深读); 每步 try 保护。

import os, types, builtins as _b
_ga, _dir, _str, _call, _iss, _ty, _rp, _ls, _len, _has, _id = (
    _b.getattr, _b.dir, _b.str, _b.callable, _b.isinstance,
    _b.type, _b.repr, _b.list, _b.len, _b.hasattr, _b.id)
_set, _int, _float, _bool, _open = _b.set, _b.int, _b.float, _b.bool, _b.open

try:
    import GFE
except Exception as e:
    print("必须在 PrePo 命令框内运行:", e); raise

try: _name = MODEL
except NameError: _name = "model"

try: GFE.Pre.document.set_application_by_ui()
except Exception: pass

os.makedirs(r"D:\GFE\decomp", exist_ok=True)
_fh = _open(r"D:\GFE\decomp\%s.txt" % _name, "w", encoding="utf-8")
def w(s):
    _fh.write(s + "\n"); _fh.flush()          # 即时落盘 -> 崩溃可定位

w("# GFE decompile dump: %s" % _name)

def looks_getter(name):
    n = name.lower()
    return n.endswith("_mgr") or n.endswith("_manager")

def is_prim(v):
    return v is None or _iss(v, (_int, _float, _bool, _str))

def fmt(v, depth=0):
    try:
        if is_prim(v): return _rp(v)
        if _iss(v, (list, tuple)):
            if _len(v) > 100: return "<list len %d>" % _len(v)
            return "[" + ", ".join(fmt(x, depth+1) for x in v) + "]"
        m = _ga(_ty(v), "__module__", "") or ""
        if m.startswith("GFE") and depth < 2:        # 下钻 2 层(展开 entries 里的 elastic/density 等)
            parts = []
            for pn in _dir(v):
                if pn.startswith("_"): continue
                try: pv = _ga(v, pn)
                except Exception: continue
                if _call(pv): continue
                parts.append("%s=%s" % (pn, fmt(pv, depth+1)))
            return "%s(%s)" % (_ty(v).__name__, ", ".join(parts))
        return "<%s>" % _ty(v).__name__
    except Exception:
        return "<?>"

# 显式 import 全部子模块(包的子模块需 import 才成为属性, 否则会漏扫)
import importlib
mods = []
_SUBS = ["GFE.Pre.document", "GFE.Pre.geometry", "GFE.Pre.mesh", "GFE.Pre.material",
         "GFE.Pre.set", "GFE.Pre.section", "GFE.Pre.step", "GFE.Pre.boundary",
         "GFE.Pre.interaction", "GFE.Pre.amplitude", "GFE.Pre.surface", "GFE.Pre.output",
         "GFE.Pre.vibration", "GFE.Pre.artbc", "GFE.Pre.soil", "GFE.Pre.case",
         "GFE.Pre.orientation", "GFE.Pre.initial_condition", "GFE.Pre.field", "GFE.Pre.sph",
         "GFE.soil"]
for s in _SUBS:
    try:
        mods.append((s, importlib.import_module(s))); w("# import ok: %s" % s)
    except BaseException as e:
        w("# import FAIL %s: %s" % (s, _ty(e).__name__))
w("# imported %d / %d submodules\n" % (_len(mods), _len(_SUBS)))

SEEN = _set()
nmgr = 0
for modname, mod in mods:
    w("## SCAN %s" % modname)                                # 检查点(即时落盘): 崩溃定位
    heavy = ("geometry" in modname) or ("mesh" in modname)   # 这两类只列名不深读
    for n in _dir(mod):
        if n.startswith("_") or not looks_getter(n): continue
        base = n.lower()
        for _suf in ("_manager", "manager", "_mgr", "mgr"):
            if base.endswith(_suf): base = base[:-_len(_suf)]; break
        key = (modname, base.strip("_"))          # 按名去重(别名归一), 不用 id(会复用)
        if key in SEEN: continue
        SEEN.add(key)
        try: f = _ga(mod, n)
        except Exception: continue
        if not _call(f): continue
        try: mgr = f()
        except BaseException as e:
            w("#   getter %s() threw %s" % (n, _ty(e).__name__)); continue
        if not (_has(mgr, "name_list") and _has(mgr, "find")):
            w("#   getter %s() -> not-mgr(%s)" % (n, _ty(mgr).__name__)); continue
        nmgr += 1
        try: names = _ls(mgr.name_list())
        except Exception:
            try: names = _ls(mgr.name_all())
            except Exception: names = []
        w("\n### MANAGER %s.%s()  -> %d objects%s" % (modname, n, _len(names), "  [仅列名]" if heavy else ""))
        for nm in names:
            if heavy:
                w("  OBJ '%s'" % nm); continue
            try: obj = mgr.find(nm)
            except Exception as e:
                w("  [find('%s') fail: %s]" % (nm, _ty(e).__name__)); continue
            w("  OBJ '%s' : %s" % (nm, _ty(obj).__name__))
            for pn in _dir(obj):
                if pn.startswith("_"): continue
                try:
                    pv = _ga(obj, pn)
                    if _call(pv): continue
                    w("    .%s = %s" % (pn, fmt(pv)))
                except Exception:
                    w("    .%s = <read-fail>" % pn)

w("\n# done. managers=%d" % nmgr)
_fh.close()
print("完成: D:\\GFE\\decomp\\%s.txt  (managers=%d)" % (_name, nmgr))

```


---

## API 自省 gfe_introspect.py
`03_工具脚本_Bridge\gfe_introspect.py`

```python
# ==== gfe_introspect.py ====
# -*- coding: utf-8 -*-
# GFE 命令流「文法」自省器 —— Route A  (v2: 内置函数全部别名化, 防 from GFE.* import * 覆盖)
# 用法: 在 GFE Pre 命令框点 "python", 粘贴执行:
#     exec(open(r"D:\GFE\gfe_introspect.py", encoding="utf-8").read())
# 产出: D:\GFE\gfe_api_spec.txt = 模块/类/方法/属性/枚举 + TypeError 逼出的类型签名
# 建议在【空白/草稿文档】下运行(脚本对疑似"会改模型"的零参函数不实际调用)。

import types, inspect
import builtins as _b
# GFE.Pre 的子模块 set/... 会覆盖内置名, 故全部走私有别名
_set, _dir, _id, _getattr, _callable, _type = _b.set, _b.dir, _b.id, _b.getattr, _b.callable, _b.type
_sorted, _list, _len, _open, _isinstance, _str, _any = _b.sorted, _b.list, _b.len, _b.open, _b.isinstance, _b.str, _b.any

try:
    import GFE
except Exception as e:
    print("无法 import GFE —— 必须在 PrePo 的 python 命令框内运行。", e)
    raise

OUT = []
SEEN = _set()
MUT = ("run", "solve", "generate", "mesh", "save", "export", "import",
       "close", "new", "clear", "reset", "delete", "remove", "commit",
       "apply", "regenerate", "update", "set_current", "set_application")

def _looks_mutating(name):
    n = name.lower()
    return _any(k in n for k in MUT)

def _typename(o):
    t = _type(o)
    mod = _getattr(t, "__module__", "") or ""
    return (mod + "." if mod and mod != "builtins" else "") + t.__name__

def probe(fn, name):
    if _looks_mutating(name):
        return "(疑似改模型, 未实调用)"
    try:
        r = fn()                              # 需参数者: 这里抛 TypeError, 函数体不执行
        return "() -> %s" % _typename(r)      # 零参成功者(getter/单例): 记录返回类型
    except TypeError as e:
        m = _str(e)
        sigs = [l.strip() for l in m.splitlines() if "->" in l]
        if sigs:
            return " ; ".join(sigs)
        return ("TypeError: " + m.splitlines()[0]) if m else "TypeError"
    except Exception as e:
        return "(需上下文/异常: %s)" % _type(e).__name__

def walk(obj, qual, depth=0):
    if _id(obj) in SEEN or depth > 7:
        return
    SEEN.add(_id(obj))
    for name in _sorted(_dir(obj)):
        if name.startswith("_"):
            continue
        try:
            attr = _getattr(obj, name)
        except Exception:
            continue
        q = qual + "." + name
        try:
            if _isinstance(attr, types.ModuleType):
                OUT.append("[mod]   " + q)
                walk(attr, q, depth + 1)
            elif inspect.isclass(attr):
                mem = _getattr(attr, "__members__", None)        # pybind 枚举
                if mem:
                    OUT.append("[enum]  " + q + "  = " + ", ".join(_list(mem)))
                else:
                    OUT.append("[class] " + q)
                    walk(attr, q, depth + 1)                     # 进类拿方法/属性
            elif _callable(attr):
                OUT.append("[func]  " + q + "    " + probe(attr, name))
            elif _type(attr).__name__ in ("property", "getset_descriptor", "member_descriptor"):
                OUT.append("[prop]  " + q)
            else:
                OUT.append("[attr]  " + q + " = <%s>" % _type(attr).__name__)
        except Exception:
            OUT.append("[err]   " + q)

walk(GFE, "GFE")

path = r"D:\GFE\gfe_api_spec.txt"
with _open(path, "w", encoding="utf-8") as f:
    f.write("# GFE 命令流 API 规格 (运行时自省 + TypeError 逼签名)\n")
    f.write("# 共 %d 条符号\n\n" % _len(OUT))
    f.write("\n".join(OUT))
print("完成: %d 条符号 -> %s" % (_len(OUT), path))

```


---

## 装配点探针 gfe_probe_assembly.py
`03_工具脚本_Bridge\gfe_probe_assembly.py`

```python
# ==== gfe_probe_assembly.py ====
# -*- coding: utf-8 -*-
# 动力SSI 装配点探针(只读) —— 坐实 构造器签名 / 连接器嵌套 / 列车荷载type / case回读
# 建议在 PrePo 打开 ch15(15.pre, 含连接器+列车荷载+土) 后执行:
#   exec(open(r"D:\GFE\gfe_probe_assembly.py", encoding="utf-8").read())
# 产出: D:\GFE\decomp\_probe_assembly.txt
# 安全: 构造器用7哨兵逼 TypeError(无匹配则不创建实例); 即便创建也是游离对象不add入模型; 其余全为读取。

import os, builtins as _b
_ga,_dir,_open,_str,_call,_ty,_len,_list = (
    _b.getattr,_b.dir,_b.open,_b.str,_b.callable,_b.type,_b.len,_b.list)
import importlib
import GFE
try: GFE.Pre.document.set_application_by_ui()
except Exception: pass
for s in ("GFE.Pre.vibration","GFE.Pre.artbc","GFE.Pre.interaction","GFE.Pre.orientation",
          "GFE.Pre.boundary","GFE.Pre.case"):
    try: importlib.import_module(s)
    except Exception: pass

OUT=[]
def w(s): OUT.append(s)
class _S: pass

def ctor_sig(cls):
    try:
        cls(*[_S() for _ in range(7)])
        return "(7哨兵构造成功? 可能接受*args/全object参数)"
    except TypeError as e:
        m=_str(e); sig=[l.strip() for l in m.splitlines() if ("->" in l or "__init__" in l)]
        return " ; ".join(sig) if sig else (m.splitlines()[0] if m else "TypeError")
    except Exception as e:
        return "(%s)"%_ty(e).__name__

# ---- 1) 关键类构造器签名 + 成员名 ----
w("##### 1. 构造器签名 + 成员")
TARGETS=[("vibration","vibra_load"),("artbc","art_bc"),
         ("interaction","connector_behavior"),("interaction","connector_section"),
         ("interaction","connector_elastic"),("interaction","connector_damping"),
         ("orientation","orientation"),("boundary","boundary"),("case","case")]
for modn,cname in TARGETS:
    mod=_ga(GFE.Pre, modn, None)
    cls=_ga(mod, cname, None) if mod else None
    if cls is None: w("\n[%s.%s] 不存在"%(modn,cname)); continue
    members=[n for n in _dir(cls) if not n.startswith("_")]
    w("\n[%s.%s] ctor: %s"%(modn,cname, ctor_sig(cls)))
    w("  members: "+", ".join(members))

# ---- 2) 现有 case 的方法(找 get_* 回读 set_*) ----
w("\n\n##### 2. 现有 case 方法 + 回读尝试")
try:
    cm=GFE.Pre.case.case_mgr(); names=_list(cm.name_list()); w("cases: %s"%names)
    if names:
        c=cm.find(names[-1]); steps=_ga(c,"steps",[])
        w("case '%s' steps=%s methods=%s"%(names[-1], steps,
            ", ".join(n for n in _dir(c) if not n.startswith("_"))))
        for gm in ("get_bcs","get_vload","get_artbc","get_fieldReqs","get_histReqs","get_initialConditions"):
            fn=_ga(c, gm, None)
            if _call(fn) and steps:
                try: w("  %s('%s')=%r"%(gm, steps[-1], fn(steps[-1])))
                except Exception as e: w("  %s: %s"%(gm,_ty(e).__name__))
except Exception as e:
    w("case 探测失败: %s"%_ty(e).__name__)

# ---- 3) 列车荷载边界(track 非空) ----
w("\n\n##### 3. 列车荷载边界(扫 track 非空, 最多3个)")
try:
    bm=GFE.Pre.boundary.bc_mgr(); found=0; scanned=0
    for nm in bm.name_list():
        scanned+=1
        try: o=bm.find(nm)
        except Exception: continue
        tc=_ga(o,"track_coord",None); ti=_ga(o,"track_id",None)
        if (tc and _len(tc)>0) or (ti and _len(ti)>0):
            w("  '%s' type=%s valid_dof=%s value=%r track_id=%r track_coord_len=%s"%(
                nm,_ga(o,"type",None),_ga(o,"valid_dof",None),_ga(o,"value",None),
                ti,(_len(tc) if tc else 0)))
            found+=1
            if found>=3: break
    w("  (扫描 %d 个边界, track非空 %d 个%s)"%(scanned,found," — 本模型非列车" if found==0 else ""))
except Exception as e:
    w("boundary 探测失败: %s"%_ty(e).__name__)

os.makedirs(r"D:\GFE\decomp", exist_ok=True)
_open(r"D:\GFE\decomp\_probe_assembly.txt","w",encoding="utf-8").write("\n".join(OUT))
print("完成 -> D:\\GFE\\decomp\\_probe_assembly.txt (%d 行)"%_len(OUT))

```


---

## 改模型逼签名 gfe_fill_mutating.py
`03_工具脚本_Bridge\gfe_fill_mutating.py`

```python
# ==== gfe_fill_mutating.py ====
# -*- coding: utf-8 -*-
# 补全 78 个"改模型"函数的签名 —— Route A 续
# 用法: 在 GFE Pre 命令框, 【务必先新建空白/草稿文档】, 然后:
#     exec(open(r"D:\GFE\gfe_fill_mutating.py", encoding="utf-8").read())
# 原理: 用 7 个哨兵参数调用 -> 参数数/类型不匹配任何重载 -> pybind 抛 TypeError
#       回显完整签名, 且【无重载匹配 => 函数体不执行】(高参数计数避免误中零参重载)。
# 残余风险: 极少数接受 *args 或全 object 参数的函数可能被误触发, 故在空白文档跑最稳。

import re, builtins as _b
_getattr, _open, _len, _str, _type = _b.getattr, _b.open, _b.len, _b.str, _b.type

try:
    import GFE
except Exception as e:
    print("无法 import GFE —— 必须在 PrePo 的 python 命令框内运行。", e)
    raise

class _S:   # 不匹配任何 pybind 重载的哨兵类型
    pass

def resolve(path):
    obj = GFE
    for p in path.split(".")[1:]:   # 跳过开头的 'GFE'
        obj = _getattr(obj, p)
    return obj

def probe(fn):
    try:
        fn(*[_S() for _ in range(7)])          # 7 哨兵: 必不匹配 -> TypeError, 不执行
        return "(WARN: 7参调用竟成功, 未取到签名, 可能已执行)"
    except TypeError as e:
        m = _str(e)
        sigs = [l.strip() for l in m.splitlines() if "->" in l]
        return " ; ".join(sigs) if sigs else ("TypeError: " + (m.splitlines()[0] if m else ""))
    except Exception as e:
        return "(异常 %s)" % _type(e).__name__

# 从 spec 里捞出被跳过的 78 个改模型函数路径
paths = []
for line in _open(r"D:\GFE\gfe_api_spec.txt", encoding="utf-8"):
    m = re.match(r"\[func\]\s+(\S+)\s+\(疑似改模型", line)
    if m:
        paths.append(m.group(1))

out = []
for p in paths:
    try:
        out.append("[func]  %s    %s" % (p, probe(resolve(p))))
    except Exception as e:
        out.append("[func]  %s    (无法解析: %s)" % (p, _type(e).__name__))

dst = r"D:\GFE\gfe_mutating_sigs.txt"
with _open(dst, "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("完成: %d 个改模型函数已逼签名 -> %s" % (_len(out), dst))

```


---

## 实时桥 send.py
`03_工具脚本_Bridge\send.py`

```python
# ==== send.py ====
# -*- coding: utf-8 -*-
# 把 D:\GFE\bridge\next.txt 发到 PrePo 的 Python REPL 执行(自动点击聚焦, 无需手点)
# 用法: py D:\GFE\bridge\send.py
import time, pyperclip
from pywinauto import Application, mouse
from pywinauto.keyboard import send_keys

BOX_XY = (2990, 990)     # 命令框内安全点(屏幕坐标), 命中不对就调这里

cmd = open(r"D:\GFE\bridge\next.txt", encoding="utf-8-sig").read().strip()  # utf-8-sig 自动吃掉 BOM
app = Application(backend="uia").connect(title="GFE-PrePo", timeout=8)
win = app.window(title="GFE-PrePo")
pyperclip.copy(cmd)
win.set_focus(); time.sleep(0.4)
mouse.click(button="left", coords=BOX_XY); time.sleep(0.3)   # 自动点命令框聚焦
send_keys("^{END}"); time.sleep(0.15)                        # 光标到 REPL 末尾提示符
send_keys("{ENTER}"); time.sleep(0.3)                        # 冲掉可能卡住的残行
send_keys("^{END}"); time.sleep(0.1)
send_keys("^v"); time.sleep(0.25)
send_keys("{ENTER}")
print("sent %d chars to PrePo REPL" % len(cmd))

```


---

## dump 切分 split_dump.py
`03_工具脚本_Bridge\split_dump.py`

```python
# ==== split_dump.py ====
# -*- coding: utf-8 -*-
# 把 decomp dump 按管理器切分 + 生成索引
# 用法: py split_dump.py <dump.txt> <输出目录>
import sys, re, os

def split_dump(dump_path, outdir):
    os.makedirs(outdir, exist_ok=True)
    lines = open(dump_path, encoding="utf-8").read().splitlines()
    heads = []  # (line_no, mgr_full, count)
    for i, l in enumerate(lines):
        m = re.match(r"### MANAGER (\S+)\(\)\s+->\s+(\d+) objects", l)
        if m:
            heads.append((i, m.group(1), int(m.group(2))))
    rows = []
    for k, (start, mgr, cnt) in enumerate(heads):
        # 块尾 = 下一个 ### MANAGER / ## SCAN / # done
        end = len(lines)
        for j in range(start + 1, len(lines)):
            if re.match(r"^(### MANAGER|## SCAN|# done)", lines[j]):
                end = j; break
        block = lines[start:end]
        short = (mgr.replace("GFE.Pre.", "").replace("GFE.", "")
                 .replace(".", "_").replace("(", "").replace(")", ""))
        names = []
        for b in block:
            mm = re.match(r"\s+OBJ '([^']*)'", b)
            if mm: names.append(mm.group(1))
        if cnt > 0:
            fn = short + ".txt"
            open(os.path.join(outdir, fn), "w", encoding="utf-8").write("\n".join(block))
        else:
            fn = ""
        preview = ", ".join(names[:10]) + (" ..." if len(names) > 10 else "")
        rows.append((mgr, cnt, len(block), fn, preview))
    # 索引
    with open(os.path.join(outdir, "_index.md"), "w", encoding="utf-8") as f:
        f.write("# %s — 按管理器索引\n\n" % os.path.basename(dump_path))
        f.write("| 管理器 | 对象数 | 行数 | 文件 | 对象名预览 |\n|---|---|---|---|---|\n")
        for mgr, cnt, ln, fn, pv in rows:
            if cnt == 0: continue
            f.write("| `%s` | %d | %d | %s | %s |\n" % (mgr, cnt, ln, fn, pv))
        f.write("\n## 空管理器\n")
        empt = [mgr for mgr, cnt, *_ in rows if cnt == 0]
        f.write(", ".join("`%s`" % m for m in empt) + "\n")
    return sum(1 for r in rows if r[1] > 0)

if __name__ == "__main__":
    n = split_dump(sys.argv[1], sys.argv[2])
    print("split %s -> %s (%d non-empty managers)" % (sys.argv[1], sys.argv[2], n))

```
