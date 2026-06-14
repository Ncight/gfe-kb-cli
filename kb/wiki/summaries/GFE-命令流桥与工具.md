---
title: "GFE-命令流桥与工具 — 反编译 / 参数化建模 / 无人值守实时桥"
type: manual
software: GFE
tags: [gfe, manual, 命令流, automation, bridge]
sources: ["[[GFE-CmdKB-tools.src]]", "[[GFE-CmdKB-INDEX.src]]"]
created: 2026-06-04
updated: 2026-06-04
---

> 让 Claude 用命令流实际操作 [[PrePo]] 的工具链：模型反编译、参数化建模、API 自省，以及把命令送进 PrePo REPL 的「实时桥」。脚本全文见 raw [[GFE-CmdKB-tools.src]]。

## 实时桥（Claude 无人值守驱动 PrePo）
原理：PrePo 须运行（窗口 `GFE-PrePo`）；`send.py` 用 pywinauto 自动点命令框 + pyperclip 粘贴 + 回车，无需人手点。
1. 多行代码写 `D:\GFE\bridge\cmd.py`
2. `D:\GFE\bridge\next.txt` 放单行 `exec(open(r"D:\GFE\bridge\cmd.py",encoding="utf-8").read())`
3. 跑 `py D:\GFE\bridge\send.py` → 在 PrePo 主线程执行；命令自写结果到文件 → Claude 读回自审
- **坑**：next.txt 须无 BOM（PS `Out-File utf8` 会加 BOM 致 SyntaxError）；send.py 读用 utf-8-sig；多行必须走 cmd.py，勿直接粘多行进 REPL；send.py 命令框聚焦靠硬编码屏幕坐标 BOX_XY=(2990,990)（行 8）鼠标点击，换分辨率/挪窗口/改布局即点空失效，需先调 send.py 行 8——无人值守场景的首要故障点。
- live 副本在 `D:\GFE\bridge\`（实际运行处）；KB 内为参考副本。

## 工具脚本
| 脚本 | 作用 |
|---|---|
| **gfe_decompile.py** | 模型反编译器：读当前 PrePo 模型全状态 → dump 到 `D:\GFE\decomp\<名>.txt`（[[GFE对象引用关系]] / 真实工程解析的数据来源） |
| **build_model.py** | 参数化建模：改 PARAMS 区重跑。土材料 + [[一维土层]] + 三维土（Block1-2，已验证 [OK]）；Block3-12（几何~工况）为注释 TODO 待逐块实跑；存盘仍须手动 GUI File→Save |
| gfe_introspect.py | API 自省 → 产 [[GFE-CmdKB-APIspec.src]] |
| gfe_probe_assembly.py | 装配点探针（构造器 / [[连接器]] / [[列车荷载]] type / case 回读） |
| gfe_fill_mutating.py | 改模型函数「7 哨兵逼签名」 |
| split_dump.py | 把整 dump 按管理器切分（纯文本，不碰 PrePo） |

## 限制
- 命令流**无 save API**：.pre 存盘只能 GUI File→Save
- 裸 python 不能 `import GFE`：必须在 PrePo 宿主进程内（经桥）执行
- 几何只能**名级感知**（按名字操作，不能像 GUI 那样点选）
- 「工程—」菜单功能的命令流可达性分三档：①[[快速建土]] = GFE.soil.box_builder/data_builder，命令流已验证可用（build_model.py Block2 [OK]）；②土体材料转 [[Davidenkov]] / [[YJK]] 材料与配筋转换：v3.3.0+ 手册有命令流 API（geotool.convert_to_davidenkov / convert_material / convert_reinforce，§3.4.18-21），但装机自省 spec 未见这些符号，升级版本后实测确认；③gmat 导入 / [[反应位移法]] 助手疑似 GUI 专有

相关：[[GFE-CmdKB]] · [[GFE-命令流API规格]] · [[GFE-命令流SSI骨架]] · [[GFE-Cmd]] · [[PrePo]]
