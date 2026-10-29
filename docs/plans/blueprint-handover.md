# Sam-PPT-Blueprint 交接文档

> 状态：现行，持续更新。最后更新：2026-10-28（文档结构整理；Skill 内容停在 4834378）。

用于开启新会话。读完 `CLAUDE.md`、[目录契约](../architecture/repository-contract.md)和本文即可接手。测试和评估方法见[测试指南](../guides/testing.md)；未完成事项以[待办清单](backlog.md)为准，本文只列编号。

## 1. 现状一句话

Skill 把大纲做成可编辑 PPTX，学参考稿 `rnb-core.pptx` 的神韵；底层是 ppt-master 6.7.2（Quick Generate、自由设计、扁平导出）。s11 大纲（8 页）跑了 5 轮隔离测试（v3–v7，见[测试记录](2026-10-27-s11-blueprint-tests.md)），之后修了 F13–F17（4834378）并加了全局安装（018b41f），**这两个提交还没测过**。本机当前安装的是 018b41f。

## 2. 下一步

- 待处理：TEST-001（用户的 30 页案例，验证 F13–F18）。
- 待决定：DOC-001（模块目录审定）。
- 暂缓：FEAT-001、FEAT-002。

## 3. 已知问题

待验证：F13–F18。待处理：TEST-002。低优先级：TECH-001～003。

## 4. 架构速览

| 文件 | 作用 |
|---|---|
| `SKILL.md` | 第 0–7 步流程、输入默认值、运行日志和最终汇报的格式 |
| `references/logic-diagrams.md` | 逻辑表达规范：关系编号、对应图示、关系部件的含义和删改规则、箭头与颜色 |
| `references/page-zoning.md` | 页面分区规范：栅格、10 个分区模板、挑模块的顺序；第六节是参考稿的版式习惯（次色、结论条、铺满、分区间连接、阴影、字号层级） |
| `references/module-catalog.md` | 模块目录 `modules.json` 的拆法和字段 |
| `references/review-brief.md` / `fork-brief.md` | 含义审查子代理、fork 改页子代理的任务说明 |
| `scripts/prepare_reference.py` | 参考稿预处理一次：导入、渲染、栅格、起页检查，生成 `style-baseline.json` |
| `scripts/pick_modules.py` | 按分区召回候选模块；排序是单元数 → 缩放比 → 质感 → 关系编号；`--batch` 一次做完整稿 |
| `scripts/review_packet.py` | 生成给含义审查员读的审查包 |
| `scripts/compose_page.py` / `start_page.py` | 用参考稿模块拼一页 / 整页照搬一张参考页 |
| `scripts/edit_page.py` | 按 id 改页，`batch` 一次执行多条命令 |
| `scripts/check_text.py` | 页面文字必须来自大纲（第 4、5 步） |
| `scripts/group_page.py` | 收口时补页面角色、页头页脚组、带 bounds 的根组（第 5 步） |
| `scripts/find_library.py` / `install.py` | 找本次用的参考稿库 / 把 Skill 和参考稿库装到 `~/.claude/` |
| `scripts/style_gap.py` | `baseline` 生成参考稿指标范围和阴影配方；`check` 逐页对比成品（第 7 步） |
| `scripts/export.py` / `fix_cjk_fonts.py` | 导出，并把中文字体修成 OPPOSans |
| `scripts/check_reuse.py` / `check_modules.py` / `inline_icons.py` / `dump_blueprint.py` / `render.ps1` / `pm.py` | 辅助工具 |

流程：第 0 步读 ppt-master → 第 1 步读规范 → 第 2 步主代理规划全稿写 `plan.md`（批量挑模块、次色、连接件），再开普通子代理做含义审查 → 第 3 步建项目、拼页 → 第 4 步按工作量分段，开 fork 并行改页 → 第 5 步收口（`check_text`、`group_page`、`stamp`、final 检查）→ 第 6 步导出 → 第 7 步渲染、跑 `style_gap`、集中修一轮。

ppt-master 的位置用 `python Sam-PPT-Blueprint/scripts/pm.py` 查。它的完整能力地图在 [ppt-master-map](../architecture/ppt-master-map/ppt-master能力地图.md)（6.7.2 版；插件升级后要重读文档集再用）。为什么从"整页照搬"改成"按关系选图、跨页拼模块"，见 [10-27 研究报告](../archive/2026-10-27-logic-and-zoning-research.md)（历史，现行规则以 Skill 的 references 为准）。

## 5. 测试资产

`D:\Workspace\Sam-PPT-Lab\assets\`：

| 文件 | 内容 |
|---|---|
| `rnb-core.pptx` | R&B.pptx 的精选版（PowerPoint 删页并删去随之变空的 2 个节，页面内容未改）：原稿 P1 封面、P2 目录、P3 章节 + P06–P67，共 65 页 |
| `blue-core.pptx` | BLUE.pptx 的同一精选版，页序与 rnb-core 一一对应 |
| `rnb-import\` | rnb-core.pptx 的 `pptx_template_import` 导入工作区（`--inheritance-mode both`，65 页） |
| `rnb-renders\` | rnb-core.pptx 65 页的 PowerPoint 渲染图 p01–p65.png（1600×900）；p04–p65 对应原稿 P06–P67 |
| `rnb-blueprint\` | 参考稿库：`prepare_reference.py` 生成的 `import\ renders\ started-renders\ contact\ grid.txt start-check.txt style-baseline.json`（含阴影配方），加上模块目录 `modules.json`（247 个模块，未审定，DOC-001）和一行索引 `modules-index.txt` |
| `rnb-baseline.csv` | p04–p65（原稿 P06–P67，62 页）的像素指标，供 `tools/metrics.py --baseline` 对比 |

测试大纲在 [docs/samples/outlines/](../samples/outlines/s11-fde.md)：`s11-fde.md`，8 页，FDE 主题，每页一句"结论"。历次运行在 `Sam-PPT-Lab\runs\`，v7 是最近一次（`20261027-2210_blueprint-v7_s11`）。

## 6. 本工作线的注意事项

- **Bash 工具和中文**：控制台打印中文会乱码，设 `PYTHONIOENCODING=utf-8`，或把输出写进 UTF-8 文件再读；python 里路径写 `D:/...`，不要写 `/d/...`；heredoc 里的 python 字符串 `"\\n"` 会变成真换行，含 `\n` 的修改用 Edit 工具。
- 用户能看出逻辑表达问题，但没有 PPT 审美训练：视觉判断要给排好序的诊断、用指标说话；基线只由用户说"可以了"决定。

## 7. 新会话开场提示（可直接复制）

> 请先阅读 CLAUDE.md、docs/architecture/repository-contract.md 和 docs/plans/blueprint-handover.md。我们在 main 上继续 Sam-PPT-Blueprint。先用 `python Sam-PPT-Blueprint/scripts/pm.py` 找到 ppt-master，确认插件版本仍是 6.7.2（变了就先重读它的文档集），再看待办清单，然后等我的具体指令。
