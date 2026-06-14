# YJKAPI 方法参考（建模与驱动核心类）

> 用途：供 AI 用 YJKAPI Python 命令流自动建模 YJK 8.0 结构/基础模型，并驱动运行中的 YJK。
> 来源：方法名自省自 `_raw/api_dir.txt`（392 顶层名 + 各类 dir 输出）；调用范式逐句提取自官方案例
> `案例1_框架结构\kj.py`、`案例11_基础建模\jc_model.py`、`案例10_远程控制\control.py`、`依赖YJK案例\post.py`。
> 单位制：YJK 内部全部 **mm**（长度/截面/坐标）；层高、节点坐标、截面尺寸均按 mm 填写。
> 准则：方法名/参数与原始数据一致，宁缺毋错。本表只展开**建模与驱动相关**核心类；
> 数据结构 `Mdl_*` / 后处理 `Post*` / 枚举 / 截面库类不逐一展开，见末尾"其余类"一节。

入口固定为：

```python
from YJKAPI import *
import os
```

---

## 1. DataFunc — 上部结构建模

自省共 147 个成员（见 `_raw/api_dir.txt` CLASS DataFunc）。建模主类：定义截面/荷载 → 生成节点网格 → 布置构件 → 组装楼层 → 提交。

### 1.1 标准层与楼层组装

| 方法 | 作用 | 范式 |
|---|---|---|
| `StdFlr_Generate(层高)` | 新建标准层，返回带 `.ID` 的标准层对象 | `StdFlr = dataFunc.StdFlr_Generate(3900)` |
| `SpcFlr_Generate(...)` | 新建特殊（错层等）标准层 | 见 api_dir |
| `Floor_Assemb(...)` | 组装单个自然层 | — |
| `Floors_Assemb(起始层号, 标准层, 复制层数, 层高)` | 批量组装/复制自然层 | `dataFunc.Floors_Assemb(0, StdFlr, 6, 3600)` |

### 1.2 截面定义（返回带 `.ID` 的定义对象）

截面定义文法：`XxxSect_Def(材料, 截面类型, "尺寸串")`。
- 第 1 参 = 材料号：`6` = 混凝土（案例统一用 6）；`5` = 钢（见 BraceSect_Def 案例）。
- 第 2 参 = 截面类型号：`1` = 矩形。
- 第 3 参 = 尺寸串：矩形为 `"b,h"`（mm，宽,高）；墙厚为单值。

| 方法 | 作用 | 范式 |
|---|---|---|
| `ColSect_Def(材料, 类型, "b,h")` | 柱截面定义；`6,1` = 混凝土矩形 | `defcol = dataFunc.ColSect_Def(6, 1, "400,400")` |
| `BeamSect_Def(材料, 类型, "b,h")` | 梁截面定义 | `defbeam1 = dataFunc.BeamSect_Def(6, 1, "250,600")` |
| `WallSect_Def(材料, 类型, 墙厚)` | 墙截面定义（第 3 参为单值厚度，非 "b,h" 串） | `defwall = dataFunc.WallSect_Def(6, 1, 1001)` |
| `BraceSect_Def(材料, 类型, "尺寸")` | 支撑截面定义；案例用钢 `5,3` | `defbrace = dataFunc.BraceSect_Def(5, 3, "501")` |
| `WallHoleDef(洞宽, 洞高)` | 墙洞（门窗洞）定义 | `defwallhole = dataFunc.WallHoleDef(300, 2501)` |
| `ColCapSect_Def(ColCapSectCreateInfo)` | 柱帽截面定义（入参为 info 对象，见 §4.2） | `colCapSect = dataFunc.ColCapSect_Def(colCapDefInfo)` |
| `Load_Def(荷载类型号, "荷载值串")` | 荷载定义；`12` = 梁线荷载类型 | `beamload1 = dataFunc.Load_Def(12, "1.00,9.60")` |

其余截面定义（同文法，见 api_dir）：`BeamJGSect_Def` / `BeamJYSect_Def` / `ColJGSect_Def` / `SteelJGSect_Def` / `SlabJYSect_Def` / `SkinLoadSect_Def` / `CantiSlab_Def` / `Stair_Def` / `FillWall_Def` / `XNQ_Def` / `GKLoad_Def` / `SlabHoleDef`。

### 1.3 节点 / 轴线 / 网格

| 方法 | 作用 | 范式 |
|---|---|---|
| `Joint_Generate(标准层ID, x, y)` | 在标准层平面生成节点，返回带 `.ID` 的节点 | `node = dataFunc.Joint_Generate(StdFlr.ID, xpos[i], ypos[j])` |
| `Axis_Generate(标准层ID, 起点节点ID, 终点节点ID)` | 由两节点生成轴线，返回带 `.ID` | `axis = dataFunc.Axis_Generate(StdFlr.ID, n1.ID, n2.ID)` |
| `Grid_Generate(标准层ID, 起点节点ID, 终点节点ID, 轴线ID)` | 由两节点 + 轴线生成网格线，返回带 `.ID` | `grid = dataFunc.Grid_Generate(StdFlr.ID, n1.ID, n2.ID, axis.ID)` |

（同义小写别名 `node_generate` / `grid_generate` 也存在，案例统一用大写形式。）

### 1.4 构件布置（arrange）

| 方法 | 作用 | 范式 |
|---|---|---|
| `column_arrange(节点二维列表, 柱截面def)` | 在节点阵列上批量布柱，返回柱列表 | `col_list = dataFunc.column_arrange(nodelist, defcol)` |
| `beam_arrange(网格列表, 梁截面def)` | 在网格上批量布梁，返回梁列表 | `beam_list = dataFunc.beam_arrange(gridlist, defbeam1)` |
| `wall_arrange(...)` | 布墙 | 见 api_dir（参数同梁式：网格 + 墙def） |
| `colCap_arrange(柱对象, 柱帽截面)` | 在单根柱上布柱帽 | `dataFunc.colCap_arrange(col_list[0], colCapSect)` |
| `slab_arrange(SlabCreateInfo)` | 按 info 布板，返回板对象（见 §4.1） | `slab = dataFunc.slab_arrange(slabInfo)` |
| `load_arrange(构件列表, 荷载def)` | 在构件（如梁）上批量加荷载 | `dataFunc.load_arrange(beam_list, beamload1)` |
| `wallhole_arrange(...)` | 布墙洞 | 见 api_dir |

其余布置（同 arrange 族，见 api_dir）：`brace_arrange` / `midslab_arrange` / `slabHole_arrange` / `stair_arrange` / `subbeam_arrange` / `skin_arrange` / `skinLoad_arrange` / `XNQ_arrange` / `FillWall_arrange` / `property_arrange` / `beamjg_arrange` / `columnjg_arrange` / `beamjy_arrange` / `slabjy_arrange` / `steeljg_arrange` / `simple_truss`。

### 1.5 提交 / 取数 / 内存复用

| 方法 | 作用 | 范式 |
|---|---|---|
| `DbModel_Assign()` | 提交当前建模数据到内存模型（布置后必调） | `dataFunc.DbModel_Assign()` |
| `GetDbModelData()` | 取出可交给 `Hi_AddToAndReadYjk` 的模型对象 | `model = dataFunc.GetDbModelData()` |
| `GetUpdateInfo()` | 取增量更新信息（改截面后回灌 YJK 用，配 `ReflecToYJK`） | `updateInfo = dataFunc.GetUpdateInfo()` |
| `SetModel(model)` | 把已读出的 YJK 模型装回 DataFunc（在已有工程上改） | `dataFunc.SetModel(model)` |
| `SetID(maxID)` | 设置 ID 起始基准（避免与已有构件 ID 冲突） | `dataFunc.SetID(maxID)` |
| `GetGroupObjList(组)` | 取某 group 内构件列表（含 collist/beamlist/walllist/bracelist/windowlist） | `group = dataFunc.GetGroupObjList(model.m_Group[0])` |

取数 getter（`GetXxxList` / `GetXxxNo`）共数十个，见 api_dir，按需取已有截面/节点/网格清单。

### 1.6 两种典型流程

**A. headless 从零建模产 ydb（`案例1_框架结构\kj.py`）**

```python
dataFunc = DataFunc()
StdFlr = dataFunc.StdFlr_Generate(3900)
defcol  = dataFunc.ColSect_Def(6, 1, "400,400")
defbeam = dataFunc.BeamSect_Def(6, 1, "250,600")
# ...生成 nodelist / gridlist（双重循环 Joint_Generate + Axis_Generate + Grid_Generate）...
col_list  = dataFunc.column_arrange(nodelist, defcol)
beam_list = dataFunc.beam_arrange(gridlist, defbeam)
slabInfo = SlabCreateInfo()
slabInfo.SetCentroid(1950, 9350).SetThick(300).SetStdFlr(StdFlr).SetCc(0).SetDeadLive(9, 9)
dataFunc.slab_arrange(slabInfo)
dataFunc.Floors_Assemb(0, StdFlr, 6, 3600)
dataFunc.DbModel_Assign()
model = dataFunc.GetDbModelData()
my = Hi_AddToAndReadYjk(model)
isok = my.CreateYDB(os.getcwd(), "kj.ydb")
```

**B. 在运行中 YJK 上改截面并回灌（`依赖YJK案例\post.py::test_group_update`）**

```python
yjkscmd = YJKSCommandPy(); yjkscmd.RunCommand("yjk_save")
my = Hi_AddToAndReadYjk()
model = my.ReadFromYJK()
maxID = my.GetUnionID()
dataFunc = DataFunc(); dataFunc.SetModel(model); dataFunc.SetID(maxID)
defcol = dataFunc.ColSect_Def(6, 1, "501,501")
group = dataFunc.GetGroupObjList(model.m_Group[0])
for col in group.collist: col.SectID = defcol.ID
dataFunc.DbModel_Assign()
my.ReflecToYJK(dataFunc.GetUpdateInfo())
```

---

## 2. JcDataFunc — 基础（Jccad）建模

自省共 101 个成员（见 `_raw/api_dir.txt` CLASS JcDataFunc）。基础建模主类：读 `Jccad_0.ydb` →
取上部节点/网格 → 定义+布置基础构件 → 产出新的 `Jccad_0.ydb`。

> ⚠ 前置：`Jccad_0.ydb` 由 YJK 进入基础模块后点"重新读取"生成于工程路径，依赖上部建模数据。
> 实测"重新读取上部数据"命令 = `jccad_read`（详见 cmd KB / 案例注释）。
> 循环读写时需先删旧 `Jccad_0.ydb` 再生成，避免累加效应。

### 2.1 读取与取数

| 方法 | 作用 | 范式 |
|---|---|---|
| `ReadJcYdb(目录, 文件名)` | 读入基础 ydb | `jcdataFunc.ReadJcYdb(current_directory, "\\Jccad_0.ydb")` |
| `GetJcModelDBdata()` | 取基础模型数据（`.ToPyList()` 转 Python 对象，内含 `m_jcNode` / `m_jcIwag` / `m_jcAppColumn` 等） | `m = jcdataFunc.GetJcModelDBdata().ToPyList()` |

取上部节点/墙网格：`nodelist = m.m_jcNode`、`iwaglist = m.m_jcIwag`、`ColumnList = m.m_jcAppColumn`。
其余 getter（`GetJcAxisList` / `GetJcAppPileList` / `GetJcRaftSlabList` / `GetJcDEFRaftYList` …）数十个见 api_dir。

### 2.2 定义（Def，返回带 `.lID` / `.DaisFlag` / `.kind` 的定义对象）

| 方法 | 作用 | 范式 |
|---|---|---|
| `JcDj_Def(0, "尺寸串")` | 独立基础定义 | `jcdataFunc.JcDj_Def(0, "0,0,0,2,3300,3300,300,600,600,3000,0,0,0")` |
| `JcPile_Def(类型, "尺寸串")` | 桩定义 | `PileDef = jcdataFunc.JcPile_Def(2, "800,200,300,500,25.0,1")` |
| `JcDais_Def(p1, 形状, ...)` | 桩基承台定义（形状 2=方形, 0=圆形） | `DaisDef = jcdataFunc.JcDais_Def(10, 2, 1, 4, 100, 100)` |
| `JcFbeam_Def(...)` | 地基梁定义 | `FbeamDef = jcdataFunc.JcFbeam_Def(401, 1001, 1501, 501, 301, 0)` |
| `JcLL_Def(宽, 高)` | 拉梁定义 | `LLDef = jcdataFunc.JcLL_Def(400, 600)` |
| `JcTJ_Def(0, "尺寸串")` | 条形基础定义 | `TJDef = jcdataFunc.JcTJ_Def(0, "2000,200,133,100,250,100,100,60,60")` |
| `JcRaftSlab_Def(-1, "参数串")` | 筏板定义 | `SlabDef = jcdataFunc.JcRaftSlab_Def(-1, "200,10,2,3,0,-0.5,1,10,10,10")` |
| `JcZD_Def(类型, 长, 宽, 高, 角)` | 柱墩定义 | `ZDDef = jcdataFunc.JcZD_Def(1, 5000, 4000, 1000, 45)` |
| `JcCol_Def(...)` / `JcWall_Def(...)` | 基础柱/墙定义 | 见 api_dir |

承台轮廓辅助（配 `JcDais_Def` 用）：
- `JcDais_Cir(承台Flag, ...)` — 加承台边/桩位（方形多坐标重载 / 圆形半径重载）：
  `jcdataFunc.JcDais_Cir(DaisDef.DaisFlag, 0, 1500, 1500)`；`jcdataFunc.JcDais_Cir(DaisDef1.DaisFlag, 3001)`
- `JcDais_StepH(Flag, p, h)` — 承台台阶高：`jcdataFunc.JcDais_StepH(0, 0, 301)`

### 2.3 布置（App，参数多为：定义ID/Flag + 节点或网格 + 偏移/标高/塔号）

| 方法 | 作用 | 范式 |
|---|---|---|
| `JcDJ_App(节点ID, ...)` | 布独基 | `jcdataFunc.JcDJ_App(nodelist[0].ID, 1, 500, 500, 60, -1.5, 1)` |
| `JcDais_App(节点ID, 承台lID, ...)` | 布承台 | `jcdataFunc.JcDais_App(nodelist[0].ID, DaisDef.lID, 100, 100, 60, 10, -1.5, 1)` |
| `JcPile_App(桩lID, 节点或坐标, ...)` | 布桩（按节点 / 按相对坐标+承台Flag 两种重载） | `jcdataFunc.JcPile_App(PileDef.lID, 750, 750, 0, DaisDef.DaisFlag, 0.0, 10, -1.5, 1)` |
| `JcFbeam_App(地基梁lID, 网格, ...)` | 布地基梁 | `jcdataFunc.JcFbeam_App(FbeamDef.lID, iwaglist[0], 500, -1.5, 1)` |
| `JcLL_App(拉梁lID, 网格, ...)` | 布拉梁 | `jcdataFunc.JcLL_App(LLDef.lID, iwaglist[1], 100, 10, 10, -1.5, 1)` |
| `JcTJ_App(条基lID, 网格, ...)` | 布条基 | `jcdataFunc.JcTJ_App(TJDef.lID, iwaglist[3], 100, -1.5, 1)` |
| `JcRaftSlab_App(筏板lID, x, y)` | 布筏板（给角点坐标，逐点调用围成板） | `jcdataFunc.JcRaftSlab_App(SlabDef.lID, 16200, 12600)` |

柱墩按属性赋值（非 App 函数）：`ColumnList[12].lZDKind = ZDDef.kind`。
节点网格生成（基础内自建）：`JcNode_Generate` / `JcAxis_Generate` / `JcGrid_Generate` / `JcVer_Generate`。

### 2.4 产出 ydb

| 方法 | 作用 | 范式 |
|---|---|---|
| `CreateYDB(目录, "Jccad_0.ydb")` | 产出基础 ydb | `jcdataFunc.CreateYDB(r"...\yjk", "Jccad_0.ydb")` |

> 产出前先删工程路径下旧 `Jccad_0*` 与 `*_F.*`（见案例 `delete_files`），随后在 YJK 命令行
> 执行 `jccad_read`（重新读取上部数据，**勿点导入 ydb 按钮**，会累加）。
> 注：案例 jc_model.py 注释里写的是 `jccad_read_by_ydb`，但主控实测正确命令为 `jccad_read`。

---

## 3. Hi_AddToAndReadYjk — 模型与 YJK 的桥（产 ydb / 读写运行中 YJK）

自省共 26 个成员（见 `_raw/api_dir.txt` CLASS Hi_AddToAndReadYjk）。

| 方法 | 作用 | 范式 |
|---|---|---|
| `Hi_AddToAndReadYjk(model)` | 用 DataFunc 产出的模型构造（产 ydb 路径） | `my = Hi_AddToAndReadYjk(model)` |
| `Hi_AddToAndReadYjk()` | 无参构造（连运行中 YJK 路径） | `my = Hi_AddToAndReadYjk()` |
| `CreateYDB(目录, 文件名)` | 把内存模型写成 ydb（headless 产 `dtlmodel.ydb` 主路径） | `isok = my.CreateYDB(os.getcwd(), "kj.ydb")` |
| `ReadYdb(...)` | 读 ydb 进内存 | 见 api_dir |
| `ReadFromYJK()` | 从运行中 YJK 读出当前模型 | `model = my.ReadFromYJK()` |
| `RefreshToYJK()` | 不经 ydb，直接把内存新模型刷进运行中 YJK（整模型重生成） | `isok = my.RefreshToYJK()` |
| `ReflecToYJK(updateInfo)` | 把增量更新（改截面等）回灌运行中 YJK | `my.ReflecToYJK(updateInfo)` |
| `ReflectAndCreateYDB(...)` | 反射并产 ydb | 见 api_dir |
| `GetUnionID()` | 取全模型最大 ID（配 DataFunc.SetID 用） | `maxID = my.GetUnionID()` |
| `GetMaxID()` / `GetDbmodel()` / `SetDbmodel()` | 取最大 ID / 取设模型对象 | 见 api_dir |
| `ReadIdByNO(GjKind, 全楼NO, 层号)` | 全楼编号 → 建模模块 ID | `ID = my.ReadIdByNO(GjKind.IDK_BEAM, No, flrNo)` |

> headless 三件套与 GFE 挂接：`dtlmodel.ydb` 由本类 `CreateYDB` 产；`dtlCalc.ydb` 需 YJK 前处理计算
> （软件开着，见 §6 驱动）；`Jccad_0.ydb` 由 `JcDataFunc.CreateYDB` 产。GFE `import_yjk` 三件齐全方有筏板（Raft 来自 Jccad_0）。

---

## 4. CreateInfo 辅助类（链式 setter 构造布置/定义入参）

### 4.1 SlabCreateInfo（板）

自省成员（见 CLASS SlabCreateInfo）：`SetCentroid` / `SetThick` / `SetStdFlr` / `SetCc` / `SetDeadLive` / `GetSlab`。链式调用后交给 `DataFunc.slab_arrange`。

| 方法 | 作用 |
|---|---|
| `SetCentroid(x, y)` | 板形心坐标（mm），程序据此定位所属闭合网格区域 |
| `SetThick(t)` | 板厚（mm） |
| `SetStdFlr(标准层对象)` | 所属标准层 |
| `SetCc(值)` | 板面标高调整 |
| `SetDeadLive(恒载, 活载)` | 恒/活面荷载 |

```python
slabInfo = SlabCreateInfo()
slabInfo.SetCentroid(1950, 9350).SetThick(300).SetStdFlr(StdFlr).SetCc(0).SetDeadLive(9, 9)
slab = dataFunc.slab_arrange(slabInfo)
```

### 4.2 ColCapSectCreateInfo（柱帽截面）

自省成员（见 CLASS ColCapSectCreateInfo）：`SetKind` / `SetSectPara` / `SetName` / `GetColCapSect`。链式后交给 `DataFunc.ColCapSect_Def`。

```python
colCapDefInfo = ColCapSectCreateInfo()
colCapDefInfo.SetKind(1).SetSectPara(1000, 1000, 1000, 2000, 1000, 2000).SetName("柱帽截面01")
colCapSect = dataFunc.ColCapSect_Def(colCapDefInfo)
```

> 同族 CreateInfo（加固/叠合/填充墙/悬挑板/墙洞等，文法一致：链式 setter + 对应 `Xxx_Def`/`Xxx_arrange`）见 api_dir：
> `BeamJGCreateInfo*` / `ColJGCreateInfo*` / `FillWallSectCreateInfo` / `FillWallSegCreateInfo` /
> `CantiSlabDefCreateInfo` / `CantiSlabSegCreateInfo` / `SlabHoleDefCreateInfo` / `GKLoadDefCreateInfo`。

---

## 5. 远程驱动运行中 YJK（进程外）

### 5.1 ControlConfig

自省字段（见 CLASS ControlConfig）：`Version` / `Invisible` / `Pid`（各带 get_/set_）。

| 字段 | 含义 |
|---|---|
| `Version` | YJK 版本，如 `"8.0.0"` |
| `Invisible` | 是否静默运行（True 静默；静默时须调 `exit` 命令，否则 yjks 进程残留） |
| `Pid` | 目标 YJK 进程 PID；`-1` = 不指定（会弹窗让用户选进程） |

### 5.2 YJKSControl（静态/类方法）

自省成员（见 CLASS YJKSControl）：`initConfig` / `RunYJK` / `RunCmd` / `SelectYjkProcess` / `init` / `exit` / `startprocess` / `IPC_Pipe` / `IPC_ShareMem`。

| 方法 | 作用 | 范式 |
|---|---|---|
| `initConfig(ControlConfig)` | 用配置初始化控制（连接/启动前必调） | `YJKSControl.initConfig(config)` |
| `RunYJK(yjks.exe 路径)` | 启动一个 YJK 实例 | `YJKSControl.RunYJK(r"E:\...\yjks.exe")` |
| `RunCmd(命令名, 参数字符串)` | 向运行中 YJK 发命令（命令名见 cmd KB） | `YJKSControl.RunCmd("UIOpen", r"E:\...\1.yjk")` |

**两种连接方式：**

```python
# A. 由 API 启动 YJK
config = ControlConfig(); config.Version = "8.0.0"; config.Invisible = False
YJKSControl.initConfig(config)
YJKSControl.RunYJK(r"E:\专业软件\YJK8.0\...\yjks.exe")
YJKSControl.RunCmd("UIOpen", r"E:\...\1.yjk")
YJKSControl.RunCmd("yjk_save", "")

# B. 接管已开的 YJK：先在 YJK 命令行输 yjksipccontrol，再：
config = ControlConfig(); config.Version = "8.0.0"; config.Invisible = False
config.Pid = -1            # -1 弹窗选进程；多 yjks 时手动匹配
YJKSControl.initConfig(config)
YJKSControl.RunCmd("yjk_save", "")
```

进程外建模→前处理→设计计算的完整命令序列（`control.py::test01`）：
`UIOpen` → `yjk_repair` → `yjk_save` → `yjk_formnode "2"` → `yjk_formslab_alllayer` →
`yjk_setlayersupport` → `yjkspre_genmodrel` → `yjktransload_tlplan` → `yjktransload_tlvert` →
`SetCurrentLabel "IDSPRE_ROOT"` → `yjkdesign_dsncalculating_all` → `SetCurrentLabel "IDDSN_DSP"`。
（`SetCurrentLabel <Ribbon标签ID>` 用于切换功能模块标签栏。）

---

## 6. 进程内脚本驱动（嵌入 YJK 的 Python，入口 `def pyyjks`）

> 来源：`依赖YJK案例\post.py`。这些类**未出现在 `_raw/api_dir.txt` 的 392 顶层名中**
> （自省在进程外环境采集，进程内类未注册），但在官方进程内案例中实证可用，
> 经 `yjks_pyload` 加载、以 `def pyyjks():` 为入口执行。

| 类 / 方法 | 作用 | 范式 |
|---|---|---|
| `YJKSCommandPy().RunCommand(命令名)` | 进程内发命令（无参直传命令名，命令见 cmd KB） | `YJKSCommandPy().RunCommand("yjk_save")` |
| `YJKSUIPy().QSetRunScript(1)` | 进入脚本模式（不弹窗执行） | `YJKSUIPy().QSetRunScript(1)` |
| `YJKSUIPy().QSetCurrentRibbonLabel(标签ID)` | 切换功能区标签栏 | `ui.QSetCurrentRibbonLabel("IDSPRE_ROOT")` |

脚本模式不弹窗完成设计计算（`post.py::test_DsnCal`）：

```python
def pyyjks():
    ui  = YJKSUIPy()
    cmd = YJKSCommandPy()
    ui.QSetCurrentRibbonLabel("IDModule_Axis")
    ui.QSetRunScript(1)
    cmd.RunCommand("yjk_repairex"); cmd.RunCommand("yjk_save")
    cmd.RunCommand("yjk_setlayersupport")
    cmd.RunCommand("yjkspre_genmodrel")
    cmd.RunCommand("yjktransload_tlplan")
    cmd.RunCommand("yjktransload_tlvert")
    ui.QSetCurrentRibbonLabel("IDSPRE_ROOT")
    cmd.RunCommand("yjkdesign_dsncalculating_all")   # 产 dtlCalc 所需的前处理计算
    ui.QSetCurrentRibbonLabel("IDDSN_DSP")
```

进程内还可用（同源 post.py，参数化前处理/楼层/温度/超限读取，按需查 api_dir）：
`YJKSPrePy`（NZRC/NBeam/FlrBeams/NColumn/FlrColumns/NJD…全楼编号取数）、
`YJKSPrePy_Tower`（多塔/楼层信息 GetTower/AddTower/AutoGen/Save）、
`YJKSPrePy_JSCS`（前处理计算参数 SetSParInt/SetSParFloat/SetSParIntArray/SetSParFloatArray/SParaSave）、
`YJKSPrePy_Temperature`（UniTemp/Save）、`YJKSDsnDataPy`（设计结果 dsnInitData/dsnGetFlrStiff…）。
这些为读取/计算驱动类，非建模主链，不在本表展开。

---

## 7. 其余类（数据结构 / 枚举 / 截面库，自省全表见 `_raw/api_dir.txt`）

下列类不参与建模主链调用，仅作数据载体或常量，按需查 api_dir，**不在本参考逐一展开**：

- **数据结构 `Mdl_*`（207 个顶层名）**：构件/截面/楼层等只读数据对象（`Mdl_Joint` / `Mdl_Beam*` / `Mdl_Col*` /
  `Mdl_Wall*` / `Mdl_Slab*` / `Mdl_Grid` / `Mdl_Axis` / `Mdl_Floor` / `Mdl_Group` /
  `Mdl_JcModelDBData(_Py)` / `Mdl_JcResultData(_Py)` …），多由 `GetXxxList` / `GetDbModelData` 返回。
- **`Hi_DbModelData` / `Hi_DbModelData_Py`**：模型容器，字段 `m_Joint` / `m_BeamSect` / `m_Slab` /
  `m_Group` / `m_StdFlr` … 及 `unionID`（即 DataFunc 模型的内部字段表）。
- **`Hi_DesignData`（385 成员）/ `JcResultDataFunc` / `Mdl_JcResultData*`**：设计/基础**结果**读取类，非建模。
- **后处理 `Post*`（42 个顶层名）**：设计结果后处理对象/枚举（如 `PostGjKind` / `PostBeamKind` / `PostLimitKind` …）。
- **枚举 / 常量类**：`GjKind`（构件种类，如 `IDK_BEAM`）、`GJType`、`ENUM_DBMDL`、
  `DataFuncState` / `DataFuncFSM`、`DdeErrorState`、`PostGjKind`、`EnumHelper`、`Compare`、`JYDef`、`Link2YJK` 等。
- **GBK 截面库类**：api_dir 中以乱码命名的类（如 `=== CLASS ���ȱ߽Ṉֶ̀߱������ (92) ===`）
  为 GBK 编码的型钢/标准截面库类，名称在 UTF-8 视图下不可读，**按需直接查 `_raw/api_dir.txt`**。

> 完整 392 顶层名与每个类的全部成员，权威来源始终是 `E:\gfe-kb-cli\kb\yjk\_raw\api_dir.txt`。
> 命令名（`RunCmd` / `RunCommand` 的第一参）权威来源是 `_raw\cmd__MAIN.tsv`（2708 条）。
