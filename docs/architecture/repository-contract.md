# 仓库与工作资料目录契约

版本：1.0。日期：2026-10-28。适用范围：仓库 `D:\Workspace\Sam-PPT-Skills\` 的全部文件，以及仓库外的工作区 `D:\Workspace\Sam-PPT-Lab\`。

1.0 变更：2026-10-28，项目初期为避免"测试会话读到开发记录"，把交接、研究报告、问题台账、测试大纲和工具都放在仓库外的 Lab 里，`CLAUDE.md` 还规定开发会话不主动读取，结果文档散在两处、没有版本、没有入口。实际上隔离靠的是安装方式（见第 5 节），与文档放哪里无关。本版把所有人写的文字资料收进仓库 `docs/`，Lab 只留生成物；新增检查器 `tools/check_docs.py`。迁移明细见 [2026-10-28-migration.json](2026-10-28-migration.json)。

## 1. 两个位置，按"是不是人写的"划分

| 位置 | 放什么 | 不放什么 |
|---|---|---|
| 仓库 `Sam-PPT-Skills\` | 人写、要版本化的东西：Skill、开发工具、所有文档、测试大纲 | 运行输出、渲染图、大的二进制素材 |
| `Sam-PPT-Lab\` | 程序生成或体积大的东西：参考稿和它的预处理库、像素基线、每次运行的输出 | 任何文档、交接、台账、大纲、脚本 |
| `D:\Workspace\Archive\` | 2026-10-26 之前的旧资料，以及 2026-10-28 退役的 Lab 文件（`2026-10-28_Sam-PPT-Lab-retired\`）；只读 | 现行资料 |
| `D:\PPT\Templates\` | 购买的模板原件（R&B.pptx、BLUE.pptx） | 加工后的文件 |

不另建其他工作目录。一次性的临时文件用会话的 scratchpad。

## 2. 仓库顶层

| 条目 | 职责 |
|---|---|
| `CLAUDE.md` | Agent 入口：必须遵守的规则和关键文档位置（Claude Code 自动读取，起 AGENTS.md 的作用，不另建 AGENTS.md） |
| `README.md` | 人类入口：有哪些 Skill、怎么安装和使用 |
| `<Skill 名>\` | 一个 Skill 一个目录，目录名即 Skill 名，例如 `Sam-PPT-Blueprint\` |
| `docs\` | 全部开发文档，见第 3 节 |
| `tools\` | 开发用工具，不随 Skill 安装（如 `metrics.py`、`check_docs.py`） |
| `.gitignore`、`.gitattributes` | Git 配置（需要时再加） |

根目录不放其他文件或目录。新增顶层条目先改本契约和检查器。

## 3. `docs\` 子目录

| 目录 | 放什么 | 文件名 |
|---|---|---|
| `docs\README.md` | 文档索引：每份现行文档一行 | 固定 |
| `architecture\` | 本契约、迁移台账、底层引擎审计（`ppt-master-map\`）、方向决策 | `repository-contract.md`、`YYYY-MM-DD-<主题>-decision.md` |
| `plans\` | 待办清单、交接文档、实施计划、测试记录 | `backlog.md`、`<工作线>-handover.md`、`YYYY-MM-DD-<主题>.md`、`YYYY-MM-DD-<对象>-<大纲>-test.md` |
| `guides\` | 现在就能照做的操作说明 | `<主题>.md` |
| `samples\outlines\` | 测试大纲，一个案例一个文件 | `<编号>-<主题>.md`，如 `s11-fde.md` |
| `archive\` | 已完成的待办、过时的报告和计划 | `backlog-done.md`、保留原日期前缀 |

不按日期、不按生成工具建目录；不保留 `v1`、`-new`、`-final` 这类并存版本，旧版交给 Git 历史。

## 4. Skill 目录

- 只放 Skill 运行时需要的东西：`SKILL.md`、`references\`（规范和子代理说明）、`scripts\`。
- 不放案例内容（大纲、成品、某次测试的结论），不放开发文档（交接、待办、测试记录）。这些都在 `docs\`。
- Skill 的规范文档（`references\*.md`）是产品资源，不是开发文档：现行规则以它们为准，`docs\` 里只写为什么和做到哪了，不复制规则正文。

## 5. 测试隔离靠什么

测试会话看不到开发资料，原因有三条，与文档放在哪里无关：

1. `install.py` 只把 Skill 目录复制到 `~/.claude/skills/`，把参考稿库复制到 `~/.claude/sam-ppt/references/`；仓库的 `docs\`、`tools\`、`CLAUDE.md` 都不会被复制。
2. 测试在一个只放 `outline.md` 的独立文件夹里开新会话（`context: fresh`，不用 fork）。这个文件夹不在仓库里，不继承任何 `CLAUDE.md` 或项目记忆。
3. 测试会话的提示词只有一句话，不提任何开发资料的路径。

所以开发会话可以、也应该读 `docs\`。具体测试步骤见 [测试指南](../guides/testing.md)。

## 6. `Sam-PPT-Lab\` 的结构

```
assets\    参考稿、预处理库、渲染图、像素基线（清单见交接文档"测试资产"一节）
runs\      每次运行一个目录
README.md  只写一句"规则见仓库 docs/architecture/repository-contract.md"
```

运行目录命名：`runs\<yyyymmdd-hhmm>_<对象>_<大纲>\`，对象和大纲只用字母、数字和 `-`，两者之间用一个 `_`，例如 `20261027-2210_blueprint-v7_s11`。目录里放本次用的 `outline.md` 副本、ppt-master 项目目录、导出的 PPTX 和渲染图。运行目录里的 `comparison.md` 之类是当次的原始记录；结论必须写进仓库的测试记录，不能只留在运行目录。

Lab 不是缓存：参考稿库和基线是测试的前提，不整目录清空。要退役的文件先登记，再移到 `D:\Workspace\Archive\<日期>_<说明>\`。

## 7. 新增、修改、删除流程

1. 先判断它是什么：Skill 运行资源、开发工具、文档（哪一类）、测试大纲，还是生成物。生成物进 Lab，其余进仓库对应位置。
2. 已有同类文档就更新它，不新建：待办只进 `backlog.md`，一条工作线只有一份交接文档。
3. 移动或改名时，同一次提交里改掉所有引用（`CLAUDE.md`、README、文档链接、脚本里的路径），不留转发壳。
4. 文档过时：开头加一行状态说明，移入 `archive\`，同步改索引。
5. 改本契约的规则，先改本文和检查器，再动文件。

## 8. 可执行验收

`python tools/check_docs.py`，提交前必须通过；`python tools/check_docs.py --selftest` 用反例确认每条规则还有效。检查项：

1. 仓库根目录只有第 2 节列出的条目（加上 `.git`）。
2. `docs\` 下只有第 3 节列出的子目录，`docs\` 根目录只有 `README.md`。
3. Skill 目录里没有 `docs`、`handover`、`backlog`、`findings`、`outline` 这类开发文档或案例文件名。
4. 路径里没有 `v<数字>` 目录段和 `-new`、`-final`、`-superseded` 文件。
5. 所有 Markdown 里的相对链接都指向存在的文件。
