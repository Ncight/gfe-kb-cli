# YJK 8.0 命令流知识库 — 导航索引

> 用途：本文件是 YJK 8.0 命令流/YJKAPI 在线知识库的总入口，供 GFE-autobuilding skill 先读本索引、再按需取对应分册。
> 目标：AI 用 YJKAPI（Python 命令流）headless 自动建模 YJK 结构/基础，产出 GFE `import_yjk` 所需的三件 ydb，并驱动运行中的 YJK 完成前处理/计算/基础读取。单位制：YJK 内部一律 **mm**（长度/截面/坐标）。
> 来源：各模块 `YJK.CUI` 菜单定义（自省导出，见 `_raw/cmd_*.tsv`）+ YJKAPI 自省 `dir` 输出（`_raw/api_dir.txt`）+ 官方 YJKAPI 案例 + 用户主控实测。命令名/方法名一律与原始数据一致，不杜撰。

---

## 1. 一句话总览

需要把 YJK 结构「画出来 + 算出来 + 导进 GFE」时，整条链路是：用 **YJKAPI** 写 Python headless 建上部/地下结构（→ `dtlmodel.ydb`），再驱动运行中的 YJK 做前处理计算（→ `dtlCalc.ydb`）和基础筏板（→ `Jccad_0.ydb`），三件 ydb 一起交给 GFE `import_yjk`，得到含上部结构 + 筏板的 SSI 模型。本知识库把「调什么命令」「用什么方法」「按什么范式拼」「整条流程怎么走」拆成下面 4 个分册。

---

## 2. 四个分册：查什么 → 读哪个

| 分册文件 | 内容 | 何时查 |
|---|---|---|
| **`YJK-CmdKB-commands.src.md`** | YJK 命令清单（命令流 `RunCmd` / `RunCommand` 的精确查询表）。主程序去重命令按 11 类整理，附地铁/隧道模块增量命令；命令名 + 中文说明逐字对照 CUI。 | 已知要点哪个 CUI 按钮、或要给 `YJKSControl.RunCmd("…")` / `YJKSCommandPy().RunCommand("…")` 填命令名时——按功能标题定位或搜命令名前缀。 |
| **`YJK-CmdKB-api.src.md`** | YJKAPI Python 方法参考（建模与驱动核心类，如 `DataFunc` 上部建模、`JcDataFunc` 基础、`CreateYDB`、`YJKSControl`/`ControlConfig` 驱动等），含方法签名与调用范式。 | 写 YJKAPI 脚本要查某个类有哪些方法、方法怎么调、参数含义时。 |
| **`YJK-CmdKB-patterns.src.md`** | 建模范式库——把上面的命令/方法拼成可跑的端到端片段（三件 ydb 数据流、headless 建结构、JCCAD 布筏板、前处理计算等），每条标 provenance（CUI✓/案例✓/实测✓/未headless验证）。 | 要照着「能跑的骨架」起手、或确认某拼法是否经实测验证时。 |
| **`YJK-CmdKB-workflow.src.md`** | YJK → GFE 完整工作流 + 驱动指南。逐步标「脚本可 headless / 需 YJK 软件开着」，给两套驱动接口（进程外 `YJKSControl`+`yjksipccontrol`／进程内 `YJKSCommandPy`+`YJKSUIPy`）骨架，以及何时提示用户打开 YJK 的话术。 | 要走完整条链路、判断每步能否无人值守、或要驱动一个运行中的 YJK 时。 |

**典型取阅顺序**：先 `workflow`（看全局与每步判据）→ 缺方法签名查 `api` / 缺命令名查 `commands` → 拼脚本时对照 `patterns` 的范式骨架。

---

## 3. 原始数据（`_raw/`）

分册是对下列原始数据的清洗/分类可读版；需要绝对全量（含分册未单列的别名/英文版/港版模块命令）时直接查原始数据：

| 文件 | 内容 |
|---|---|
| `_raw/cmd__MAIN.tsv` | 主程序命令全量（`\YJK.CUI`），**2708 条**，格式 `命令名<TAB>中文说明`。`commands` 分册的主程序部分即源于此。 |
| `_raw/cmd_<模块>.tsv` | 各专业模块命令全量（地铁 `Subway`、隧道渠道 `TunnelAndChannel2D`、英文版 `YJKENG_EN`、港版 `YJKENG_HK` 等），同 `命令名<TAB>说明` 格式。 |
| `_raw/_cui_summary.tsv` | 各模块 CUI 文件路径与命令条数索引（`module<TAB>count<TAB>cui_path`），用于定位某模块命令在哪个 tsv。 |
| `_raw/api_dir.txt` | YJKAPI 全量自省（`dir` 输出，含顶层名 + 各类成员），**410 KB**。`api` / `patterns` 分册的方法名均出自此。注意：该文件部分块为 UTF-16 编码，按需解码。 |

> 全量 grep 入口：命令名搜 `_raw/cmd_*.tsv`，方法名/类名搜 `_raw/api_dir.txt`。

---

## 4. 在线查询（GFE-autobuilding skill 用）

各文件可通过 GitHub raw 直接拉取，URL 前缀：

```
https://raw.githubusercontent.com/Ncight/gfe-kb-cli/main/kb/yjk/<文件名>
```

例：

```
https://raw.githubusercontent.com/Ncight/gfe-kb-cli/main/kb/yjk/YJK-API-index.src.md
https://raw.githubusercontent.com/Ncight/gfe-kb-cli/main/kb/yjk/YJK-CmdKB-commands.src.md
https://raw.githubusercontent.com/Ncight/gfe-kb-cli/main/kb/yjk/YJK-CmdKB-api.src.md
https://raw.githubusercontent.com/Ncight/gfe-kb-cli/main/kb/yjk/YJK-CmdKB-patterns.src.md
https://raw.githubusercontent.com/Ncight/gfe-kb-cli/main/kb/yjk/YJK-CmdKB-workflow.src.md
```

原始数据同理，前缀后接 `_raw/<文件名>`，例：
`https://raw.githubusercontent.com/Ncight/gfe-kb-cli/main/kb/yjk/_raw/cmd__MAIN.tsv`

> 建议：在线场景先拉本索引判断需要哪个分册，再拉对应分册，避免一次性拉全量 tsv（单文件 200-360 KB）。
