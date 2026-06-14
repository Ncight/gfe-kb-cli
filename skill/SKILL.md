---
name: gfe-kb
description: 在线查 GFE/PrePo(广州颖力岩土有限元)命令流知识库——787 API 全签名、能力矩阵(1331项×自动化三层)、149 条避坑、15 章案例建模路径、wiki 双链关联(GFE↔论文↔概念)。当用户问 GFE/PrePo 某命令流 API 怎么写(如 copy_mesh/box_builder/property_shell/as_elastic 签名)、GFE 建模流程或案例(基坑开挖/地铁站/施工生死单元/SSI/列车振动)、GFE 避坑(网格/材料/工况/生死单元/边界/单位制)、或顺概念关联探索(某 GFE 能力↔哪篇论文/概念)时使用。即使没点名"GFE",只要在 GFE 命令流建模上下文里查 API/经验/案例,也用此 skill。数据在线托管于 github.com/Ncight/gfe-kb-cli,无需本地安装,Claude 用 WebFetch/gh 在线取。
---

# GFE 命令流知识库（纯在线）

数据托管在 **github.com/Ncight/gfe-kb-cli**。**用在线方式取，无需 clone、无需装 Python/CLI。**
**优先在线取准再答 GFE 命令流问题——API 签名/枚举/字段极易记错，别凭记忆。**

## 怎么取内容（按 repo 可见性二选一）

- **repo 公开** → 用内置 WebFetch（任何人零依赖）：
  `WebFetch https://raw.githubusercontent.com/Ncight/gfe-kb-cli/main/<路径>`
- **repo 私有** → 用 gh（需 `gh auth login` 且对该 repo 有访问权）：
  `gh api repos/Ncight/gfe-kb-cli/contents/<路径> -H "Accept: application/vnd.github.raw"`

## 关键文件路径（<路径> 处填）

| 内容 | 路径 |
|---|---|
| **API 全签名** | `kb/raw/GFE-CmdKB-APIref.src.md` |
| **避坑清单**(红线/高危/提示, 12域) | `kb/raw/GFE-CmdKB-pitfalls.src.md` |
| **能力矩阵**(1331项×①命令流/②半自动/③纯GUI) | `kb/raw/GFE-CmdKB-capability.src.md` |
| **对象引用关系**(截面/BC/Tie/Embed/Case 引用规则) | `kb/raw/GFE-CmdKB-objref.src.md` |
| **案例建模路径**(15章命令流步骤链) | `kb/raw/GFE-CmdKB-paths.src.md` |
| **总索引** | `kb/raw/GFE-CmdKB-INDEX.src.md` |
| **API 自省原始符号** | `kb/raw/GFE-CmdKB-APIspec.src.md` |
| **真实工程解析**(400gal SSI 弹塑性) | `kb/raw/GFE-CmdKB-400galVC.src.md` |
| **wiki 实体/概念/摘要**(双链) | `kb/wiki/entities/*.md` `kb/wiki/concepts/*.md` `kb/wiki/summaries/*.md` |

## 查法

| 你要 | 做法 |
|---|---|
| 某 API 签名 | 取 `APIref`，搜函数名行（格式 `` - `fn` 签名 ``）；找不到再 `search` |
| 避坑 | 取 `pitfalls`，按域（网格/材料/工况/生死单元/边界/SPH/列车）定位 |
| 某能力能否命令流自动化 | 取 `capability`，看该行 ①/②/③ 标记 |
| 模块间怎么引用(BC用啥集/Tie用啥) | 取 `objref` |
| 复现某案例流程 | 取 `paths`，定位 `路径_ch<N>` 段读步骤链 |
| 全文/模糊搜 | `gh search code "<词>" --repo Ncight/gfe-kb-cli --limit 20`（私有/公开皆可，需 gh） |
| 概念关联(GFE能力↔论文/概念) | 取对应 `wiki` 页，读 `[[双链]]` |

## 纪律

- 大文件（APIref/capability ~百KB）：能 `gh search code` 先定位行号/文件，再精取，省上下文；WebFetch 取回后在内容里找目标段即可。
- 答 GFE API 签名前先取 `APIref` 核对；答建模坑前先取 `pitfalls` 核对。
- 单位制随模型（m-t-kPa 或 mm-t-MPa），命令流无 save API（.pre 存盘走 GUI），β=0（显式动力）——这些高频铁律在 `pitfalls`/`INDEX` 有。

## 本地加速（可选）

装了本地副本的人可 `pip install -e <clone路径>` 后用 `py -m gfekb api/search/ask/related/case/pitfall/show`（更快、可离线）；未装则纯在线如上。
