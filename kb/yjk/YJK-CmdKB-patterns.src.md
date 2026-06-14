# YJK 8.0 建模范式库 (YJK-CmdKB-patterns)

> **用途**: 供 AI(GFE-autobuilding skill) 在线查询后, 用 YJKAPI / YJK 命令流自动建结构模型并产出 GFE import_yjk 所需的三件 ydb。
> **来源**: 官方 YJKAPI 案例 (`D:\GFE\cases\small-building-ssi\yjkapi\案例\二次开发\` 下 案例1/3/10/11/15 + 依赖YJK案例\post.py) + 已验证脚本 (`F:\Autobuilding\case_tod_hub\build_struct_yjk.py / build_raft_jc.py / yjk_auto_prep.py`)。命令名/方法名一律与原始数据一致, 不杜撰。
> **单位**: YJK 内部一律 **mm**(长度)。`cx`/`cy` 等坐标须为 **int**。材料编号 **6 = 混凝土**。
>
> **provenance 约定** (每个命令/方法标注出处, 宁缺毋错):
> - `[CUI✓]` — 命令名在 `_raw\cmd__MAIN.tsv` 的 CUI dump 中实测命中。
> - `[案例✓]` — 方法/命令出现在官方 YJKAPI 案例脚本里(可跑)。
> - `[实测✓]` — 主控已实测确认(见任务背景事实)。
> - `[未headless验证]` — 仅据案例整理, 依赖 GUI 前置或坐标待核, 用前须实测。

---

## 0. 三件 ydb 与数据流总览

GFE `import_yjk` 需要同一项目目录下的 **三件 ydb**, 缺一不可(已实测):

| ydb | 产出方式 | 携带数据 | 范式 |
|---|---|---|---|
| `dtlmodel.ydb` | YJKAPI `CreateYDB` **可 headless** 产 | 上部+地下结构(梁柱墙板, 自动带配筋) | 范式 1 |
| `dtlCalc.ydb` | **需 YJK 前处理计算**(软件开着) | 前处理网格/荷载导算/计算结果 | 范式 3 |
| `Jccad_0.ydb` | 基础模块「重新读取」上部数据 + JCCAD 脚本布筏板 | 基础(筏板 Raft / 桩 / 承台 / 独基 …) | 范式 2 |

**关键事实**: 筏板(Raft)来自 `Jccad_0.ydb` — 去掉它 GFE 里 Raft=0(已实测)。

典型全链:
```
范式1(headless) → dtlmodel.ydb
   ↓ (YJK 开工程)
范式3(a/b) 前处理计算 → dtlCalc.ydb
   ↓ (基础模块重新读取 jccad_read → 初始 Jccad_0.ydb)
范式2(JCCAD 脚本布筏板) → 重写 Jccad_0.ydb
   ↓
GFE import_yjk(dtlmodel + dtlCalc + Jccad_0) → 完整地下+地上+筏板模型
```

---

## 1. 上部/地下结构 headless 建模 → `dtlmodel.ydb`

**目标**: 纯 YJKAPI(不开 YJK GUI)生成上部结构数据并落盘 `dtlmodel.ydb`。
**骨架命名空间**: `from YJKAPI import *`。
**核心流水线**:
```
DataFunc() → StdFlr_Generate(层高) → 截面 *Sect_Def / Load_Def
  → Joint_Generate → Axis_Generate → Grid_Generate
  → column/beam/wall/slab_arrange + load_arrange
  → Floor_Assemb / Floors_Assemb (楼层组装)
  → DbModel_Assign() → GetDbModelData()
  → Hi_AddToAndReadYjk(model).CreateYDB(dir, "dtlmodel.ydb")
```

### 1A. 框架结构 最小骨架 (源: 案例1 kj.py [案例✓])
```python
from YJKAPI import *
import os
df = DataFunc()
sf = df.StdFlr_Generate(3900)                 # 标准层, 层高 mm
# 截面 (材料6=混凝土, 第2参=类型, 串为尺寸 mm)
defcol  = df.ColSect_Def(6, 1, "400,400")     # 矩形柱 400x400
defbeam = df.BeamSect_Def(6, 1, "250,600")    # 矩形梁 250x600
beamload = df.Load_Def(12, "1.00,9.60")       # 荷载定义(类型12=梁线荷载, 恒,活)

# 节点二维阵列 (xpos/ypos 为 int 坐标 mm)
xpos = [0, 3900, 7800, 11700, 15600, 19500, 23400]
ypos = [0, 6700, 12000]
nodelist = []
for x in xpos:
    col = [df.Joint_Generate(sf.ID, x, y) for y in ypos]
    nodelist.append(col)

# 网格: 竖向(同一X相邻Y) + 横向(相邻X同Y); 每条边先 Axis_Generate 再 Grid_Generate
gridlist = []
for col in nodelist:                                   # 竖向
    for i in range(len(col)-1):
        ax = df.Axis_Generate(sf.ID, col[i].ID, col[i+1].ID)
        gridlist.append(df.Grid_Generate(sf.ID, col[i].ID, col[i+1].ID, ax.ID))
for i in range(len(nodelist)-1):                        # 横向
    for j in range(len(nodelist[i])):
        ax = df.Axis_Generate(sf.ID, nodelist[i][j].ID, nodelist[i+1][j].ID)
        gridlist.append(df.Grid_Generate(sf.ID, nodelist[i][j].ID, nodelist[i+1][j].ID, ax.ID))

col_list  = df.column_arrange(nodelist, defcol)         # 批量布柱(吃二维节点表)
beam_list = df.beam_arrange(gridlist, defbeam)          # 批量布梁(吃网格表)

# 板: SlabCreateInfo 链式 setter (形心/厚度/标准层/Cc/恒活)
info = SlabCreateInfo()
info.SetCentroid(1950, 9350).SetThick(300).SetStdFlr(sf).SetCc(0).SetDeadLive(9, 9)
df.slab_arrange(info)

df.load_arrange(beam_list, beamload)                    # 梁上荷载
df.Floors_Assemb(0, sf, 6, 3600)                        # 标准层复制: (底标高, 标准层, 层数, 层高)
df.DbModel_Assign()                                     # 提交建模数据
model = df.GetDbModelData()
my = Hi_AddToAndReadYjk(model)
my.CreateYDB(os.getcwd(), "dtlmodel.ydb")               # 落盘 (案例原名 kj.ydb, 入GFE须改 dtlmodel.ydb)
```
**坑**:
- `column_arrange` 既可吃**二维节点表**(案例1, 一次布全部柱), 也可吃**单节点**(案例15 reflec). `beam_arrange`/`wall_arrange` 吃**网格(列表或单条)**。
- 每条边必须 `Axis_Generate` 在前、`Grid_Generate` 在后(Grid 第4参=Axis.ID)。
- 节点/网格/截面对象都用 `.ID` 引用, 不要传对象本身给需要 ID 的位置。
- 案例 `CreateYDB` 落地名是 `kj.ydb` — **入 GFE 必须命名为 `dtlmodel.ydb`**。

### 1B. 剪力墙结构 最小骨架 (源: 案例3 jlq.py [案例✓])
剪力墙用便捷批量法 `node_generate` / `grid_generate`(注意是小写, 与案例1的逐节点法不同), 墙+墙洞成对布置。
```python
from YJKAPI import *
df = DataFunc()
sf = df.StdFlr_Generate(3000, 12, 3)          # 层高;(可带额外形参, 见案例3)
defwall     = df.WallSect_Def(6, 1, 200)      # 墙: 材料6, 类型1, 厚 200 (注意是单值不是串)
defwallhole = df.WallHoleDef(900, 2500)        # 墙洞: 宽 900 高 2500

for ox, oy in [(0,0), (7000,8000), (10500,-8000)]:
    xspans = [ox, 3500, 3500]                  # 首元=起点坐标, 其后=各跨跨度(增量)
    yspans = [oy, 3000, 5000]
    nodelist = df.node_generate(xspans, yspans, sf)   # 便捷批量造节点阵
    gridlist = df.grid_generate(nodelist, 1, 1)        # (nodelist, X向?, Y向?) 1=生成
    df.wall_arrange(gridlist, defwall)
    df.wallhole_arrange(gridlist, defwallhole)

df.Floors_Assemb(0, sf, 18, 3000)
df.DbModel_Assign()
model = df.GetDbModelData()
Hi_AddToAndReadYjk(model).CreateYDB(os.getcwd(), "jlq.ydb")
```
**坑**:
- `node_generate(xspans, yspans, sf)` 的 spans 首元是**绝对起点坐标**, 其余是**跨度增量**(不是绝对坐标)。这与案例1 `xpos` 直接给绝对坐标的写法相反。
- `grid_generate(nodelist, x?, y?)` 第2/3参 1/0 控制是否生成 X/Y 向网格(案例15 用 `grid_generate(nodelist,0,1)` 只生成 Y 向)。
- 墙厚 `WallSect_Def(6,1,200)` 第3参是**整数厚度**, 不是 `"宽,高"` 串(与梁柱不同)。

### 1C. 箱型地铁车站(地下) + 上盖塔楼 一体 (源: build_struct_yjk.py [案例✓ headless 已跑])
要点: 把**底板层/站台层/站厅层**各做成一个标准层, 用 `Floor_Assemb(标准层, 底标高mm, 层高mm)` **逐层指定底标高**叠放(地下层底标高为负), 再 `Floors_Assemb` 把塔楼复制到顶。
```python
from YJKAPI import *
df = DataFunc()
colS  = df.ColSect_Def(6, 1, "800,1000")   # 车站中柱
beamS = df.BeamSect_Def(6, 1, "1000,1400") # 车站梁
wallS = df.WallSect_Def(6, 1, 700)         # 车站侧墙/端墙 厚700
colT  = df.ColSect_Def(6, 1, "600,600")    # 塔楼柱
beamT = df.BeamSect_Def(6, 1, "300,600")   # 塔楼梁
loadT = df.Load_Def(12, "1.00,5.00")

# 复用工具: 一次造平面节点表 + 纵/横网格字典
def plan(sf, X, Y):
    node = [[df.Joint_Generate(sf.ID, x, y) for y in Y] for x in X]
    def mk(a, b):
        ax = df.Axis_Generate(sf.ID, a.ID, b.ID)
        return df.Grid_Generate(sf.ID, a.ID, b.ID, ax.ID)
    longg = {j: [mk(node[i][j], node[i+1][j]) for i in range(len(X)-1)] for j in range(len(Y))}
    trang = {i: [mk(node[i][j], node[i][j+1]) for j in range(len(Y)-1)] for i in range(len(X))}
    return node, longg, trang

def slabs(sf, X, Y, t, d, l):              # 逐网格格子布板
    for i in range(len(X)-1):
        for j in range(len(Y)-1):
            info = SlabCreateInfo()
            info.SetCentroid((X[i]+X[i+1])//2, (Y[j]+Y[j+1])//2)  # 形心用 //2 保 int
            info.SetThick(t).SetStdFlr(sf).SetCc(0).SetDeadLive(d, l)
            df.slab_arrange(info)

xs = [0,9000,18000,27000,36000,45000,54000]; ys = [0,9000,18000]; H = 4500
# 车站箱身标准层: 两侧纵墙(lb[0],lb[2]) + 两端横墙(tb[首],tb[尾]) + 中纵梁 + 内部横梁 + 中柱 + 板
box = df.StdFlr_Generate(H)
nb, lb, tb = plan(box, xs, ys)
df.wall_arrange(lb[0] + lb[2] + tb[0] + tb[len(xs)-1], wallS)
df.beam_arrange(lb[1], beamS)
inn = []
for i in range(1, len(xs)-1): inn += tb[i]
df.beam_arrange(inn, beamS)
for i in range(len(xs)): df.column_arrange(nb[i][1], colS)   # 中柱沿中线 y=ys[1]
slabs(box, xs, ys, 700, 20, 4)

base = df.StdFlr_Generate(500)             # 底板层: 仅梁格+800厚板, 无柱无墙
nB, lB, tB = plan(base, xs, ys)
allg = []
for j in range(3): allg += lB[j]
for i in tB: allg += tB[i]
df.beam_arrange(allg, beamS)
slabs(base, xs, ys, 800, 20, 4)

txs = [9000,18000,27000,36000,45000]; tys = [0,9000,18000]   # 塔楼平面退台
tower = df.StdFlr_Generate(3600)
nt, lt, tt = plan(tower, txs, tys)
df.column_arrange([[nt[i][j] for j in range(len(tys))] for i in range(len(txs))], colT)
grids = []
for j in range(len(tys)): grids += lt[j]
for i in tt: grids += tt[i]
beamsT = df.beam_arrange(grids, beamT)
slabs(tower, txs, tys, 120, 5, 2)
df.load_arrange(beamsT, loadT)

# ★楼层组装: Floor_Assemb 逐层放(底标高可负), Floors_Assemb 批量复制
df.Floor_Assemb(base, -500, 500)           # 底板层  z=-0.5..0
df.Floor_Assemb(box,   0,    H)            # 站台层  z=0..4.5
df.Floor_Assemb(box,   H,    H)            # 站厅层  z=4.5..9 (同一标准层可复用两次)
df.Floors_Assemb(9000, tower, 4, 3600)     # 上盖塔楼 z=9..23.4

df.DbModel_Assign()
model = df.GetDbModelData()
my = Hi_AddToAndReadYjk(model)
my.CreateYDB(r"...\yjk_station", "dtlmodel.ydb")
```
**坑**:
- `Floor_Assemb(标准层对象, 底标高mm, 层高mm)` 与 `Floors_Assemb(底标高mm, 标准层, 层数, 层高mm)` **形参顺序不同**: 前者标准层在首, 后者底标高在首。地下层底标高填**负值**。
- 同一标准层对象可被 `Floor_Assemb` 复用多次叠放(站台/站厅共用 box)。
- 板形心坐标用整除 `//2` 保证 int(YJK 坐标须 int)。
- 此脚本即对应 GFE 教程 ch11「高层带地下室」, import_yjk 一次导入完整地下+地上(自动带配筋)。

---

## 2. 基础筏板 (JCCAD) → 重写 `Jccad_0.ydb`

**目标**: 在初始 `Jccad_0.ydb`(由基础模块「重新读取」生成)上, 用 `JcDataFunc` 布筏板/桩/承台, 重写 `Jccad_0.ydb` 供 GFE 读成 Raft。
**命名空间**: `from YJKAPI import *`。

### 2A. 前置(脚本不可替代, 基础设计依赖上部计算结果)
1. 范式1 已产 `dtlmodel.ydb`。
2. YJK 前处理及计算 → `dtlCalc.ydb`(范式3)。
3. 进基础(JCCAD)模块 → 点「重新读取」/命令 `jccad_read` [CUI✓] → 生成初始 `Jccad_0.ydb`(把上部节点/网格/荷载导进基础模块)。
   - **注意**: 实测「重新读取上部数据」命令是 **`jccad_read`** [实测✓], **不是** `jccad_read_by_ydb`(后者在 CUI dump 中查无, 仅见于旧案例注释)。

### 2B. JCCAD 脚本布筏板 最小骨架 (源: 案例11 jc_model.py [案例✓] + build_raft_jc.py [未headless验证])
```python
import os, glob
from YJKAPI import *

PROJ = r"...\yjk_station"                      # 须含 dtlmodel/dtlCalc/Jccad_0.ydb 三件
jc = JcDataFunc()
jc.ReadJcYdb(PROJ, "\\Jccad_0.ydb")           # 读初始 Jccad_0.ydb (第2参带前导反斜杠)
m = jc.GetJcModelDBdata().ToPyList()          # 注意链式: GetJcModelDBdata() 再 .ToPyList()
nodes = m.m_jcNode                            # 基础节点
iwags = m.m_jcIwag                            # 基础网格(地基梁/拉梁布置用)
print("jcNode count =", len(nodes))           # ★先打印, 据真实节点核对筏板角点坐标

# 定义筏板: JcRaftSlab_Def(-1, "板厚mm,...其余材料/配筋/标高等参数串...")
raft = jc.JcRaftSlab_Def(-1, "1400,10,2,3,0,-0.5,1,10,10,10")  # 首段=板厚(此处1400)
# 布筏板: JcRaftSlab_App(lID, x, y) 每个角点一次, 围成矩形
for x, y in [(-1000,-1000), (55000,-1000), (55000,19000), (-1000,19000)]:
    jc.JcRaftSlab_App(raft.lID, x, y)

# 删旧盘文件 + 重写(内存已 ReadJcYdb, 删盘不影响内存)
for f in glob.glob(os.path.join(PROJ, "Jccad_0*")):
    os.remove(f)
ok = jc.CreateYDB(PROJ, "Jccad_0.ydb")
# 之后回 YJK 命令行再执行一次重新读取(范式2A第3步), 再 GFE import_yjk 即得 Raft
```
**可选构件**(同源案例11, 桩基 SSI 常用):
```python
# 桩: JcPile_Def(类型, "桩径,...") → JcPile_App(lID, node, ...)
PileDef = jc.JcPile_Def(2, "800,200,300,500,25.0,1")
jc.JcPile_App(PileDef.lID, nodes[0], -1, 0.0, 10)
# 承台: JcDais_Def(...) → JcDais_Cir(角点) → JcDais_StepH(...) → JcDais_App(node, lID, ...)
DaisDef = jc.JcDais_Def(10, 2, 1, 4, 100, 100)
jc.JcDais_Cir(DaisDef.DaisFlag, 0, 1500, 1500)
jc.JcDais_App(nodes[0].ID, DaisDef.lID, 100, 100, 60, 10, -1.5, 1)
jc.JcPile_App(PileDef.lID, 750, 750, 0, DaisDef.DaisFlag, 0.0, 10, -1.5, 1)
# 独基/地基梁/拉梁/条基/柱墩: JcDj_Def/JcDJ_App, JcFbeam_Def/_App, JcLL_Def/_App, JcTJ_Def/_App, JcZD_Def
```
**坑**(案例11 文件头注释明示, 重要):
- 完成布置后须**先删 YJK 项目目录下 `Jccad_0.ydb`, 再 CreateYDB 生成**(避免累加)。
- 之后在 YJK 命令行执行重新读取命令(`jccad_read`)**, 不要点导入 ydb 按钮**——按钮会**累加**(旧版 bug)。
- 循环读写 ydb 时, 当前读取的须是**上一循环生成的** ydb。
- 基础数据**依赖上部建模数据**: 最开始须调一次重新读取; 上部结构变化时, 须先删 `Jccad_0.ydb` 再重新读取。
- `JcRaftSlab_App(lID, x, y)` 角点坐标**必须与 ReadJcYdb 实际节点对齐**——用打印的 `nodes` 坐标核对后再填(build_raft_jc.py 里的坐标是推定值, 未核对)。
- 筏板参数串首段=板厚 mm; 其余材料/配筋/标高(如 `-0.5`)等沿用案例默认, 按需细化。

---

## 3. 驱动「运行中的 YJK」做前处理计算 → `dtlCalc.ydb`

`dtlCalc.ydb` 须**软件开着**做前处理计算才产生。两套互斥的驱动方式:

### 3a. 进程外驱动 (源: 案例10 control.py + yjk_auto_prep.py [案例✓ / 未headless验证])
外部 Python 进程通过 IPC 控制运行中的 YJK。**前提**: 先在 YJK 命令行手输一次 `yjksipccontrol` 建立 IPC。
```python
from YJKAPI import *
config = ControlConfig()
config.Version = "8.0.0"
config.Invisible = False        # True=静默计算, 但须最后调 exit, 否则 yjks 进程残留
config.Pid = -1                 # -1: 多YJK进程时弹窗让选; 也可填具体 Pid 精确连接
print(YJKSControl.initConfig(config))
# (从零起也可: YJKSControl.RunYJK(r"...\yjks.exe") 启动新进程, 再 RunCmd("UIOpen", 工程路径))

def R(cmd, arg=""):
    YJKSControl.RunCmd(cmd, arg)

# ===== 前处理 + 计算 → dtlCalc.ydb (命令序列源: post.py test_DsnCal / control.py test01) =====
R("yjk_repairex")                            # 工程修复 [案例✓(post.py)][CUI✓] (control.py test01 用的是 yjk_repair, 仅案例不在CUI)
R("yjk_save")                                # [案例✓]
R("yjk_setlayersupport")                     # 建模→前处理过渡 [案例✓][CUI✓]
R("yjkspre_genmodrel")                       # 生成模型关系 [案例✓]
R("yjktransload_tlplan")                      # 平面荷载导算 [案例✓]
R("yjktransload_tlvert")                      # 竖向荷载导算 [案例✓]
R("SetCurrentLabel", "IDSPRE_ROOT")          # 切前处理标签 [案例✓]
R("yjkdesign_dsncalculating_all")            # 设计计算(生成数据) → dtlCalc [案例✓]
R("yjk_save")
# ===== 基础模块重新读取 → 初始 Jccad_0.ydb =====
R("jccad_read")                              # 重新读取上部数据 [CUI✓][实测✓]
R("yjk_save")
```
**坑**:
- 这些前处理命令多数(`yjk_save` / `yjkspre_genmodrel` / `yjktransload_tlplan` / `yjktransload_tlvert` / `yjkdesign_dsncalculating_all` / `SetCurrentLabel`)**不在 CUI dump** 里, 出处是**官方案例脚本**(control.py / post.py)——`[案例✓]` 而非 `[CUI✓]`。少数例外**同时也在 CUI dump**: `jccad_read`[CUI✓][实测✓]、`yjk_repairex`[CUI✓]、`yjk_setlayersupport`[CUI✓]。
- 进程外(control.py test01)实际用 `yjk_repair`(CUI 中查无); `yjk_repairex` 是 post.py(进程内)用的形式, 且在 CUI dump 中命中。两者都是修复命令, 按你的驱动方式择一。
- `Invisible=True` 静默计算后必须 `exit`, 否则 yjks.exe 残留。
- 多个 YJK 进程时 `Pid=-1` 会弹窗; 无人值守须填具体 Pid。
- 进程外只有 `YJKSControl.RunCmd`; 不要在进程外用 `YJKSCommandPy`(那是进程内)。

### 3b. 进程内脚本 (源: 案例10 control.py test02/test03 + post.py [案例✓])
脚本在 YJK 进程内执行(经 `yjks_pyload` 加载, 入口函数固定名 `def pyyjks()`)。用 `YJKSCommandPy().RunCommand` + `YJKSUIPy()` 切标签/进脚本模式。
```python
from YJKAPI import *

def test_DsnCal():                           # 源: post.py test_DsnCal [案例✓]
    ui  = YJKSUIPy()
    cmd = YJKSCommandPy()
    ui.QSetCurrentRibbonLabel("IDModule_Axis")   # 先切到轴线网格标签
    ui.QSetRunScript(1)                           # ★进脚本模式(不弹窗)
    cmd.RunCommand("yjk_repairex")
    cmd.RunCommand("yjk_save")
    cmd.RunCommand("yjk_setlayersupport")         # 建模→前处理过渡
    cmd.RunCommand("yjkspre_genmodrel")
    cmd.RunCommand("yjktransload_tlplan")
    cmd.RunCommand("yjktransload_tlvert")
    ui.QSetCurrentRibbonLabel("IDSPRE_ROOT")      # 切前处理标签
    cmd.RunCommand("yjkdesign_dsncalculating_all")# 设计计算 → dtlCalc
    ui.QSetCurrentRibbonLabel("IDDSN_DSP")        # 切设计结果标签

def pyyjks():                                # ★固定入口名, yjks_pyload 调用它
    test_DsnCal()
```
**坑**:
- 进程内入口函数**必须叫 `pyyjks`**(yjks_pyload 找它)。
- `RunCommand` 是进程内(YJKSCommandPy), `RunCmd` 是进程外(YJKSControl), 别混。
- 切前处理/设计结果须配 `QSetCurrentRibbonLabel`(常用标签: `IDModule_Axis` 轴网 / `IDSPRE_ROOT` 前处理 / `IDDSN_DSP` 设计结果 / `IDDTL_DETAIL_BEAM|COLUMN|WALL|SLAB` 施工图各模块)。
- `QSetRunScript(1)` 必调, 否则命令会弹窗卡住。
- 前处理参数(风/温差/多塔等)有专用类: `YJKSPrePy_JSCS`(计算参数)/`YJKSPrePy_Tower`(楼层多塔)/`YJKSPrePy_Temperature`(温差)/`YJKSPrePy`(查构件全楼ID)/`YJKSDsnDataPy`(读设计结果)。见 post.py 各 test_* 函数。

---

## 4. 注入「运行中模型」(不落 ydb, 内存联动)

把内存里 `DataFunc` 造/改的模型直接灌进运行中的 YJK, 免落盘往返。三条注入路径:

### 4A. `RefreshToYJK()` — 整模型重灌 (源: post.py test_refresh [案例✓])
内存中重新生成整模型后, 一次刷进 YJK(不经 ydb)。
```python
df = DataFunc()
# ...(同范式1: StdFlr_Generate / 截面 / 节点网格 / arrange / Floors_Assemb)...
df.DbModel_Assign()
model = df.GetDbModelData()
my = Hi_AddToAndReadYjk(model)
my.RefreshToYJK()                            # 整模型刷新进运行中的 YJK
```

### 4B. `ReflecToYJK(updateInfo)` — 增量改 (源: post.py test_group_update [案例✓])
读现有 YJK 模型 → 改 group 内构件截面 → 只把改动(updateInfo)反射回去。
```python
cmd = YJKSCommandPy(); cmd.RunCommand("yjk_save")
my = Hi_AddToAndReadYjk()
model = my.ReadFromYJK()                      # 从运行中的 YJK 读模型
maxID = my.GetUnionID()
df = DataFunc(); df.SetModel(model); df.SetID(maxID)
defcol = df.ColSect_Def(6, 1, "501,501")      # 新增截面
group = df.GetGroupObjList(model.m_Group[0])  # 取第一个 group 内构件
for col in group.collist: col.SectID = defcol.ID
df.DbModel_Assign()
updateInfo = df.GetUpdateInfo()
my.ReflecToYJK(updateInfo)                    # 只反射增量改动
```

### 4C. `transUpdateInfo` / `transModel`(联动 link, 源: 案例15 link.py [案例✓])
联动模式: 主进程 `DataFunc.InitForLink(unionID)` 造增量, 经 `Link2YJK.Instance` 包装, 用 `yjks_pyload` 调 YJK 内 helper 反射。需配套一个 `MyHelper.py`(YJK 进程内, 含 `test_ipcreflect`/`test_ipcrefresh`/`test_readModel`/`test_updateUnionID` 等接收函数)。
```python
# 取 YJK 端当前 unionID
def getUnionID():
    YJKSControl.RunCmd("yjks_pyload", r"...\MyHelper.py", "test_updateUnionID")
    return Link2YJK.Instance.GetIPCUnionID()

# 增量改动注入
def transUpdateInfo(updateInfo):
    link = Link2YJK.Instance
    link.LinkPrepareWrapper(updateInfo, Hi_UpdateInfo)
    YJKSControl.RunCmd("yjks_pyload", r"...\MyHelper.py", "test_ipcreflect")

# 用法: 增删构件 → DbModel_Assign → GetUpdateInfo → transUpdateInfo
df = DataFunc()
unionID = getUnionID()
df.InitForLink(unionID)                       # ★联动必须先 InitForLink
# ...增删梁柱墙(Joint_Generate/column_arrange/.../updateInfo.DeleteObj/ModifyObj)...
df.DbModel_Assign()
transUpdateInfo(df.GetUpdateInfo())
```
**坑**:
- 三条路径对象不同: `RefreshToYJK`/`ReflecToYJK` 是 `Hi_AddToAndReadYjk` 的方法; `transUpdateInfo`/`transModel` 是联动自定义函数(经 `Link2YJK.Instance` + `yjks_pyload`)。
- 联动必须先 `df.InitForLink(unionID)`, unionID 须从 YJK 端实时取(`getUnionID`), 否则 ID 冲突。
- `updateInfo` 增量: `ModifyObj(改后对象)` / `DeleteObj(对象)`; 每轮 `updateInfo.Clear()` 复用。
- 联动依赖 YJK 进程内 `MyHelper.py` 接收端(案例15 配套), 不是单边能跑。

---

## 通用避坑速查

| 坑 | 说明 |
|---|---|
| 三件 ydb 必需 | GFE import_yjk 缺 dtlmodel/dtlCalc/Jccad_0 任一都不完整; 筏板靠 Jccad_0 |
| 坐标须 int | `cx`/`cy`/`Joint_Generate` 坐标、板形心都用整数(用 `//` 保 int) |
| 单位 mm | YJK 内部一律 mm(长度), 层高/截面/坐标全是 mm |
| 材料 6=混凝土 | `*Sect_Def(6, ...)` 首参 6 即混凝土 |
| 墙厚是单值 | `WallSect_Def(6,1,200)` 第3参整数厚度, 非 `"宽,高"` 串 |
| spans 语义 | `node_generate` 的 xspans/yspans 首元=绝对起点, 余项=跨度增量 |
| Axis 先于 Grid | `Grid_Generate(...,Axis.ID)` 第4参需 Axis.ID, 顺序不能反 |
| .ID 引用 | 需要 ID 的参数传 `obj.ID`/`obj.lID`, 不传对象本身 |
| 落盘改名 | 案例落地名(kj/jlq)入 GFE 必改 `dtlmodel.ydb` |
| dtlCalc/Jccad 需开软件 | 这两件靠运行中的 YJK 计算/读取产生, headless 不出 |
| jccad_read 非 _by_ydb | 重新读取上部数据命令是 `jccad_read`[CUI✓][实测✓] |
| 勿点导入按钮 | 重写 Jccad_0 后用命令重读, 点导入按钮会累加(旧版bug) |
| RunCmd vs RunCommand | 进程外 `YJKSControl.RunCmd`; 进程内 `YJKSCommandPy().RunCommand` |
| 进程内入口名 | yjks_pyload 找 `def pyyjks()`, 函数名固定 |
| QSetRunScript(1) | 进程内脚本不弹窗的开关, 不调会卡窗 |
