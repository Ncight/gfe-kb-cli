# YJK → GFE 完整工作流 + 驱动指南

> 用途：供 AI（GFE-autobuilding skill）端到端把 YJK 8.0 自动建模产出的三件 ydb 交给 GFE `import_yjk`，建出含上部结构（SuperStru）+ 筏板（Raft）的 SSI 模型。本文给出每步「脚本可 headless / 需 YJK 软件开着」判据、两套驱动接口骨架、以及「何时提示用户打开 YJK」的话术。
> 来源：用户主控实测（命令序列 / jccad_read / 两套驱动 / 筏板来自 Jccad_0）+ 自省数据 `_raw/api_dir.txt`（YJKSControl/ControlConfig/JcDataFunc/CreateYDB 类与方法）+ 主程序命令清单 `_raw/cmd__MAIN.tsv`（jccad_read / yjk_repairex / yjk_setlayersupport 等）+ GFE 命令流知识库（`../raw/GFE-Cmd.src.md` §6.4.1 import_yjk / §3.4.20-21 convert_material/convert_reinforce）。
> 单位制：YJK 内部 mm。命令名 / 方法名均与原始数据一致，未在原始数据中出现的（如 yjk_save / yjkspre_genmodrel / yjktransload_* / yjkdesign_dsncalculating_all / yjksipccontrol / IDSPRE_ROOT / 进程内 YJKSCommandPy/YJKSUIPy）来源为用户主控实测，按实测原样记录。

---

## 1. 总览

AI 用 YJK 建模，产出三件 ydb，再交给 GFE 一次性导入：

```
①上部结构建模 ──► dtlmodel.ydb ─┐
②前处理+计算  ──► dtlCalc.ydb  ─┼─► GFE import_yjk ──► SuperStru(上部结构) + Raft(筏板)
③④基础+筏板   ──► Jccad_0.ydb  ─┘
```

三件 ydb 缺一不可（GFE `import_yjk` 同时读这三个文件）：

| ydb | 含义 | 谁产 | 备注 |
|---|---|---|---|
| `dtlmodel.ydb` | 上部结构几何+构件+配筋定义 | YJKAPI `CreateYDB`（headless 脚本） | 纯几何模型，不含计算结果 |
| `dtlCalc.ydb`  | 前处理后的计算模型 | YJK 前处理及计算（软件运行中） | 含支座/导荷/工况，需软件算 |
| `Jccad_0.ydb`  | 基础模型（筏板的唯一来源） | 基础模块「重新读取上部数据」初始化 + 布筏板覆写 | **去掉它 GFE 端 Raft=0（实测）** |

> 关键实测：GFE 端**筏板（Raft）只来自 `Jccad_0.ydb`**。若只给 dtlmodel+dtlCalc 而无 Jccad_0，导入后筏板为空。

---

## 2. 步骤表

> 标注：`[脚本可headless]` = 纯 Python/YJKAPI，不需 YJK 主程序界面；`[需YJK软件开着]` = 必须 YJK 主程序运行中（前处理/基础/计算依赖软件态）。

| 步 | 操作 | 产物 | 执行方式 | 命令 / API |
|---|---|---|---|---|
| ① | 上部结构建模 | `dtlmodel.ydb` | `[脚本可headless]` | YJKAPI `CreateYDB`（见 §2.1） |
| ② | 前处理及计算 | `dtlCalc.ydb` | `[需YJK软件开着]` | 命令序列（见 §2.2） |
| ③ | 基础模块「重新读取上部数据」 | 初始 `Jccad_0.ydb` | `[需YJK软件开着]` | `jccad_read`（见 §2.3） |
| ④ | 布筏板 | 覆写 `Jccad_0.ydb` | `[脚本可headless]` | `JcDataFunc`（见 §2.4） |
| ⑤ | GFE `import_yjk` 读三件 ydb | SuperStru + Raft | GFE 端 PrePo | `io.get_current().import_yjk(...)`（见 §5） |

### 2.1 步① 上部结构建模 → dtlmodel.ydb `[脚本可headless]`

用 YJKAPI 自省可见的 `DataFunc` / `CreateYDB` 建上部结构后落盘。`CreateYDB` 是 headless 产 `dtlmodel.ydb` 的入口（`api_dir.txt` 同时出现 `CreateYDB` 与 `ReflectAndCreateYDB`，以及 `JcDataFunc.CreateYDB`）。具体构件 API（轴网/梁/柱/墙/楼板/荷载）见同目录 patterns 文档，本文只锚定产物：本步结束应得到 `dtlmodel.ydb`。

> 实测口径：`CreateYDB` 只产 `dtlmodel.ydb`（上部几何），不产 `dtlCalc.ydb`；后者必须经步②软件计算。

### 2.2 步② 前处理及计算 → dtlCalc.ydb `[需YJK软件开着]`

在运行中的 YJK 里按序发命令（用 §3 任一套驱动 RunCmd/RunCommand 逐条执行）。命令序列（用户主控实测）：

```
yjk_repairex                       # 工程修复（cmd__MAIN.tsv 实证：工程修复）
yjk_save                           # 保存工程
yjk_setlayersupport                # 设置支座（cmd__MAIN.tsv 实证：设置支座）
yjkspre_genmodrel                  # 生成模型关系（前处理建模关系）
yjktransload_tlplan                # 导荷-平面荷载传导
yjktransload_tlvert                # 导荷-竖向荷载传导
SetCurrentLabel IDSPRE_ROOT        # 切到前处理 ribbon 根标签（驱动用，见 §3 QSetCurrentRibbonLabel 等价）
yjkdesign_dsncalculating_all       # 设计-全部计算
```

> 命令名说明：`yjk_repairex` / `yjk_setlayersupport` 已在 `cmd__MAIN.tsv` 核到（工程修复 / 设置支座）；`yjk_save` / `yjkspre_genmodrel` / `yjktransload_tlplan` / `yjktransload_tlvert` / `yjkdesign_dsncalculating_all` / `SetCurrentLabel IDSPRE_ROOT` 为用户主控实测序列，按实测原样记录，TSV 导出中未单列。
> 本步**必须 YJK 软件运行中**：前处理建模关系、导荷、设计计算都依赖软件内核与当前工程态。算完得到 `dtlCalc.ydb`。

### 2.3 步③ 基础模块「重新读取上部数据」→ 初始 Jccad_0.ydb `[需YJK软件开着]`

进基础（Jccad）模块，执行：

```
jccad_read                         # 重新读取上部数据（cmd__MAIN.tsv 实证：HelpString=重新读取上部数据）
```

> 实测关键：「重新读取上部数据」对应命令是 **`jccad_read`**，**不是** `jccad_read_by_ydb`（后者在 api/命令清单中不存在，易误用）。
> 本步**必须 YJK 软件运行中**：基础模块要从已算的上部数据派生基础初始模型，生成初始 `Jccad_0.ydb`。

### 2.4 步④ 布筏板 → 覆写 Jccad_0.ydb `[脚本可headless]`

用 `JcDataFunc`（基础数据函数类）脚本布筏板并写回 `Jccad_0.ydb`。`api_dir.txt` 中 `JcDataFunc(101)` 已确认含筏板相关方法：

| 方法 | 作用 |
|---|---|
| `ReadJcYdb` | 读入 Jccad_0.ydb（基础模型） |
| `JcRaftSlab_Def` | 定义筏板（截面/类型） |
| `JcRaftSlab_App` | 布置/排布筏板 |
| `GetJcRaftSlabList` | 取筏板列表（校验） |
| `GetJcRaftYInfoList` / `GetJcRaftCornerPointList` | 取筏板信息/角点 |
| `CreateYDB` | 写回 ydb |

典型流（详见同目录 foundation patterns 文档）：`ReadJcYdb(Jccad_0.ydb)` → `JcRaftSlab_Def(...)` 定义筏板 → `JcRaftSlab_App(...)` 布置 → `CreateYDB(...)` 覆写 `Jccad_0.ydb`。

> 本步纯脚本（`JcDataFunc` 操作 ydb 数据），不强依赖软件界面；但 `Jccad_0.ydb` 的**初始版必须先由步③在软件里产出**，步④只是覆写其筏板部分。

### 2.5 三件齐活后

`<工程文件夹>` 下应同时存在 `dtlmodel.ydb` + `dtlCalc.ydb` + `Jccad_0.ydb`，可进入步⑤ GFE 导入（§5）。

---

## 3. 两套驱动接口（驱动运行中的 YJK）

步②③需要把命令发给运行中的 YJK。有两套接口，二选一。

### 3.1 进程外驱动：YJKSControl + yjksipccontrol

**适用**：AI 进程与 YJK 是两个进程，靠 IPC（Pipe/共享内存）通信。
**前置**：用户须先在 **YJK 命令行输入 `yjksipccontrol`** 打开 YJK 端的 IPC 控制监听（否则连不上）。

`api_dir.txt` 确认 `YJKSControl(17)` 含方法：`init` / `initConfig` / `startprocess` / `SelectYjkProcess` / `RunYJK` / `RunCmd` / `exit` / `IPC_Pipe` / `IPC_ShareMem`；配置类 `ControlConfig(17)` 含 `Pid` / `Invisible` / `Version`（及对应 get_/set_）。

骨架：

```python
# 进程外：通过 IPC 把命令发给已运行的 YJK
# 前置：用户已在 YJK 命令行输入  yjksipccontrol  打开 IPC 监听
from YJKSControl import YJKSControl, ControlConfig   # 命名空间以本机自省为准

cfg = ControlConfig()
cfg.Version = "8.0"          # 目标 YJK 版本
cfg.Invisible = False        # 是否隐藏界面（前处理/计算建议 False 便于排错）
# cfg.Pid = <已运行YJK进程的Pid>   # 若要附着到指定进程

ctl = YJKSControl()
ctl.initConfig(cfg)          # 用 ControlConfig 初始化
ctl.init()                   # 建立 IPC（Pipe/共享内存）
ctl.SelectYjkProcess()       # 选定要驱动的 YJK 进程（多开时）

# 逐条发步②③命令
for cmd in [
    "yjk_repairex", "yjk_save", "yjk_setlayersupport",
    "yjkspre_genmodrel", "yjktransload_tlplan", "yjktransload_tlvert",
    "SetCurrentLabel IDSPRE_ROOT", "yjkdesign_dsncalculating_all",
]:
    ctl.RunCmd(cmd)

# 进基础模块重新读取上部数据
ctl.RunCmd("jccad_read")

ctl.exit()
```

> 说明：`RunCmd` 是进程外发单条命令的入口；`RunYJK` / `startprocess` 用于由控制端拉起 YJK 进程。**`yjksipccontrol` 是 YJK 端命令**（用户在 YJK 命令行输入以开监听），不是 Python 方法——这是「进程外」能连上的开关。

### 3.2 进程内驱动：yjks_pyload + pyyjks（YJKSCommandPy / YJKSUIPy）

**适用**：脚本被 YJK 自身的 Python 宿主加载并在 YJK 进程内执行（同进程，无需 IPC）。
**机制（用户主控实测）**：脚本经 **`yjks_pyload`** 加载，入口约定为 `def pyyjks(...)`；进程内用 `YJKSCommandPy().RunCommand(...)` 发命令、用 `YJKSUIPy().QSetRunScript(1)` 进脚本模式、`QSetCurrentRibbonLabel(...)` 切 ribbon 标签。

骨架：

```python
# 进程内：被 YJK 通过 yjks_pyload 加载后调用，入口函数名固定 pyyjks
def pyyjks():
    cmd = YJKSCommandPy()      # 进程内命令执行器（实测）
    ui  = YJKSUIPy()           # 进程内 UI/ribbon 控制（实测）

    ui.QSetRunScript(1)                       # 进入脚本运行模式
    ui.QSetCurrentRibbonLabel("IDSPRE_ROOT")  # 切到前处理 ribbon 根标签

    # 步②前处理+计算
    for cmd_name in [
        "yjk_repairex", "yjk_save", "yjk_setlayersupport",
        "yjkspre_genmodrel", "yjktransload_tlplan", "yjktransload_tlvert",
        "yjkdesign_dsncalculating_all",
    ]:
        cmd.RunCommand(cmd_name)

    # 步③基础模块重新读取上部数据
    cmd.RunCommand("jccad_read")
```

> 说明：`YJKSCommandPy` / `YJKSUIPy` / `yjks_pyload` / `pyyjks` / `QSetRunScript` / `QSetCurrentRibbonLabel` 均为用户主控实测，本机 `api_dir.txt`（DataFunc/Jc* 命名空间 dump）未覆盖这些运行期类，按实测原样记录。`QSetCurrentRibbonLabel("IDSPRE_ROOT")` 与进程外的 `SetCurrentLabel IDSPRE_ROOT` 等价（切前处理标签）。

### 3.3 两套怎么选

| | 进程外 YJKSControl | 进程内 yjks_pyload |
|---|---|---|
| 进程关系 | AI 与 YJK 分进程，IPC | 脚本在 YJK 进程内 |
| YJK 端前置 | 须输 `yjksipccontrol` 开监听 | 由 YJK 加载脚本（`yjks_pyload`） |
| 发命令 | `YJKSControl().RunCmd(...)` | `YJKSCommandPy().RunCommand(...)` |
| 切 ribbon | `RunCmd("SetCurrentLabel IDSPRE_ROOT")` | `YJKSUIPy().QSetCurrentRibbonLabel("IDSPRE_ROOT")` |
| AI 自动化便利 | 高（外部全程脚本控制） | 中（须借 YJK 宿主加载入口） |

无论哪套，步②③都要求 **YJK 主程序正在运行且已打开目标工程**。

---

## 4. ★「提示用户打开 YJK」的话术与判据

AI 要清楚区分：哪些步纯脚本就能跑（不打扰用户），哪些步**必须 YJK 软件运行中**（执行前必须先提示用户）。

### 4.1 判据表

| 步 | 是否需 YJK 软件运行 | 原因 |
|---|---|---|
| ① 上部结构建模（CreateYDB） | 否 `[脚本可headless]` | YJKAPI 直接产 dtlmodel.ydb |
| ② 前处理及计算 | **是 `[需YJK软件开着]`** | 前处理建模关系/导荷/设计计算依赖软件内核 |
| ③ 基础「重新读取上部数据」(jccad_read) | **是 `[需YJK软件开着]`** | 基础模块从上部数据派生，需软件态 |
| ④ 布筏板（JcDataFunc 覆写） | 否 `[脚本可headless]` | 纯 ydb 数据操作（但需步③已产初始 Jccad_0.ydb） |
| 后处理（如读计算结果） | **是 `[需YJK软件开着]`** | 同前处理/计算，依赖软件 |
| ⑤ GFE import_yjk | 否（在 GFE/PrePo 侧） | 读已落盘的三件 ydb |

**总结判据**：凡涉及**前处理 / 基础模块 / 计算 / 后处理**（步②③及任何读算结果）→ 必须 YJK 软件运行中；凡**纯建模 / 布筏板**（步①④，YJKAPI/JcDataFunc 操作 ydb）→ 纯脚本即可。

### 4.2 提示话术（AI 执行到步②或③前先说）

> 「接下来要做 YJK 前处理与计算（步②）/ 基础模块重新读取上部数据（步③），这一步必须在 YJK 软件里运行。请您：
> 1. 打开 YJK 8.0，加载本工程（含上一步产出的 `dtlmodel.ydb` 的工程文件夹）；
> 2.（若用进程外驱动）在 YJK 命令行输入 `yjksipccontrol` 并回车，打开 IPC 控制监听；
> 完成后告诉我，我再发命令序列驱动它计算。」

进入步③（基础）前若工程未在基础模块，提示用户切到基础（Jccad）模块再执行 `jccad_read`。

### 4.3 流程编排建议

AI 应把 headless 步（①④）和需软件步（②③）**分段**：先脚本跑完步①产 dtlmodel.ydb → 提示用户开 YJK 跑步②③（一次性提示，连续发命令）→ 步③产初始 Jccad_0.ydb 后，AI 再脚本跑步④布筏板覆写 → 三件齐活转步⑤。避免在每条命令前反复打扰用户，**只在「从 headless 切到需软件」的边界提示一次**。

---

## 5. 与 GFE 衔接（步⑤及导 INP）

### 5.1 import_yjk 调用

在 GFE/PrePo 端，对**含三件 ydb 的工程文件夹**调用 `import_yjk`（GFE 命令流知识库 §6.4.1 实证）：

```python
from GFE import io
io_instance = io.get_current()

# yjk_para：43 元整数列表（场景相关，不可跨场景照抄）
# 下值为 ch10 地铁站【主控 probe 实测可用】(import_yjk 返回 OK，产 SuperStru+439集+380截面)；ch11 同此值；ch15 不同([10]=400/[12]=800/[13]=28000)
yjk_para = [1, 1, 0, 1, 1, 0, 1, 0,
            300, 5, 40, 0, 510, 2800, 200, 610,
            150, 3, 1, 0, 5, 250, 0, 40000,
            1, 10, 10, 300, 140, 260, 80, 160,
            400, 179, 310, 50, 1, 260, 0, 100,
            0, 0, 0]
yjk_para2 = ['', '']

result = io_instance.import_yjk('<YDB文件夹>', yjk_para, yjk_para2, True, '', False)
# 参数：(YDB文件夹路径, yjk_para 43元, ['',''], True, '', False)
if result:
    print("YJK 模型导入成功")   # 得到 SuperStru(上部结构) + Raft(筏板)
```

> 参数口径：第 1 参数是**工程文件夹路径**（GFE 内部找该文件夹下的 dtlmodel/dtlCalc/Jccad_0）；`yjk_para` 是 **43 元整数列表**；`yjk_para2 = ['', '']`；尾三参 `True, '', False`。
> 筏板来自 Jccad_0（实测）：导入后若 Raft=0，多半是工程文件夹缺 `Jccad_0.ydb` 或其内无筏板（回查步③④）。

### 5.2 导 INP 前的材料/配筋转换

导入 YJK 模型后、导出 INP（给求解器）前，按需把 YJK 线性材料/配筋转成 GFE 非线性（GFE 命令流知识库 §3.4.20-21 实证）：

```python
GFE.geometry.geotool.convert_material(1)    # 1: 线性→非线性（YJK 材料）
GFE.geometry.geotool.convert_reinforce(1)   # 1: 转为 YJK 配筋（0 移除 / 2 默认配筋）
```

> `convert_material(type)`：0 非线性→线性，1 线性→非线性；返回 bool（重复转换返回 False）。
> `convert_reinforce(type)`：0 移除所有配筋，1 转为 YJK 配筋，2 转为默认配筋。
> 顺序：先 `convert_material(1)` 再 `convert_reinforce(1)`，再走 GFE 的土体/网格/边界/分析步→导 INP 流程（见 `../raw/GFE-CmdKB-cases.src.md` 动力 SSI 链）。

---

## 6. 一句话流程卡（AI 速查）

```
①CreateYDB → dtlmodel.ydb        [脚本]
   ↓ 提示用户：打开 YJK + 加载工程 (+输 yjksipccontrol 若进程外)
②YJK里发命令序列 → dtlCalc.ydb    [需YJK开]  yjk_repairex/yjk_save/yjk_setlayersupport/
                                            yjkspre_genmodrel/yjktransload_tlplan/
                                            yjktransload_tlvert/SetCurrentLabel IDSPRE_ROOT/
                                            yjkdesign_dsncalculating_all
③jccad_read → 初始 Jccad_0.ydb    [需YJK开]
④JcDataFunc 布筏板 → 覆写 Jccad_0  [脚本]   JcRaftSlab_Def/JcRaftSlab_App/CreateYDB
⑤GFE import_yjk(文件夹, 43元, ['',''], True,'',False) → SuperStru+Raft
   导INP前: convert_material(1) + convert_reinforce(1)
```
