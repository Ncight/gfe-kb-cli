# gfe-kb-cli

GFE（广州颖力高性能有限元）命令流知识库 **CLI**。把散在 Obsidian「通用知识库」里的 GFE 经验，做成终端一行就查的工具。

数据源 = OB 知识库的 **双层架构**：
- **raw 精确层**（`kb/raw/`）：787 API 全签名、能力矩阵、案例操作手册、命令流手册原文、对象引用关系、15 章官方命令流 py
- **wiki 关联层**（`kb/wiki/`）：Karpathy 编译的 entity / concept / summary + `[[双链]]`（GFE ↔ 论文 ↔ 概念）

## 安装

```bash
pip install -e .        # 之后全局命令 gfe
# 或免安装直接用:
python -m gfekb <子命令>
```

## 用法

| 命令 | 作用 | 例 |
|---|---|---|
| `gfe api <名>` | 精确查 API 签名（解析 APIref） | `gfe api copy_mesh` |
| `gfe search <词>` | 全文检索 raw+wiki | `gfe search 生死单元 --in raw` |
| `gfe ask <词...>` | 多词相关度排序（轻语义） | `gfe ask 车站 嵌入 土体` |
| `gfe related <主题>` | 双链关联（谁引用谁） | `gfe related GFE对象引用关系` |
| `gfe case <词>` | 案例摘要定位 | `gfe case 基坑` |
| `gfe pitfall [词]` | 避坑（⚠/坑/红线） | `gfe pitfall 网格` |
| `gfe show <路径>` | 看整页内容 | `gfe show raw/GFE-CmdKB-objref.src.md` |

## 双层定位

- **不知道某命令怎么写** → `gfe api <fn>`（精确签名）
- **不知道某词在哪/想全文找** → `gfe search` / `gfe ask`
- **想顺着概念关联探索**（GFE 能力 ↔ 哪篇论文用了） → `gfe related`
- **真向量语义** → 可接本机 qmd（OB 库已 qmd 向量化）；CLI 的 `ask` 是离线轻量版

## 数据来源与授权

数据提炼自 GFE 官方手册/案例，手册原文经授权纳入。`kb/` 内容随上游 OB 知识库（`G:\ObisidianDateLoad\通用知识库`）刷新。
