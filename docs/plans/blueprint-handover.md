# Sam-PPT-Blueprint 交接（2026-10-27）

给新会话用。先读本文件，再按需读文中列出的文件。

## 1. 目标与现状

- **目标**：Sam-PPT-Blueprint Skill 把用户的 PPT 大纲做成可编辑 PPTX，学参考稿 `rnb-core.pptx` 的神韵，而不是只换颜色。底层引擎是 ppt-master 6.7.2（只读，Quick Generate、扁平导出）。
- **仓库**：`D:\Workspace\Sam-PPT-Skills`（GitHub `rhfan2019/Sam-PPT-Skills`，私有，`main`）。最新提交是 **018b41f**（Skill 内容到 4834378，018b41f 加了全局安装）。
- **现状**：s11 大纲（8 页，FDE 主题）一共跑了 7 次隔离测试，v7 是最后一次。之后在 v7 的基础上又修了 5 条共性问题（4834378），**这一版还没有经过测试**。
- **下一步**：用户要做一个 30 页的案例。用户对那个案例非常熟悉，能看出逻辑表达问题。用它来验证 4834378，并补全问题台账里"待测"的指标。

## 2. 必须遵守的约定

这些规则来自仓库的 `CLAUDE.md` 和用户的记忆。

- 和用户交流一律用中文。用户会写代码，但没有 PPT 审美眼光：要给出排好序的诊断、用指标说话、需要时提出反对意见。
- 每次修改仓库都自动提交并推送。一个 Skill 一个子目录，Skill 里不放任何案例内容。
- **ppt-master 只读**：不改、不打补丁。提方案前先查它有没有这个能力，有就用它的。新加的 Skill 内容要同时满足三条：基线测试里实测出来、ppt-master 没有、用户同意。较大的改动先给方案，等用户确认再做。
- 仓库以外的资料只放 `D:\Workspace\Sam-PPT-Lab\`，结构和运行目录的命名规则见它的 `README.md`。`handover\` 不要主动读，用户给出路径时才读。
- 用户说"可以了"的页面才算基线，不要自己宣布通过。Skill 不删改大纲内容，信息密度归 Sam-PPT-Outline 管。
- "房型图"指战略屋。
- **测试**（2026-10-27 用户新定的规矩）：
  - 和真实使用完全一样：用户只放大纲、说一句话，不运行任何脚本、不准备环境；流程、计时、日志、汇报格式都内置在 Skill 里；
  - 每次测试都要沉淀：结论记进 `Sam-PPT-Lab\findings.md`，只为共性问题改 Skill，个例单列、不改 Skill。

## 3. Skill 结构（`Sam-PPT-Blueprint/`）

| 文件 | 作用 |
|---|---|
| `SKILL.md` | 第 0–7 步流程、输入默认值、运行日志和最终汇报的格式 |
| `references/logic-diagrams.md` | 逻辑表达规范：关系编号、对应图示、关系部件的含义和删改规则、箭头与颜色 |
| `references/page-zoning.md` | 页面分区规范：栅格、10 个分区模板、挑模块的顺序，**第六节是参考稿的版式习惯**（次色、结论条、铺满、分区间连接、阴影、字号层级） |
| `references/module-catalog.md` | 模块目录 `modules.json` 的拆法和字段 |
| `references/review-brief.md` / `fork-brief.md` | 含义审查子代理、fork 改页子代理的任务说明 |
| `scripts/prepare_reference.py` | 参考稿预处理一次：导入、渲染、栅格、起页检查，并生成 `style-baseline.json` |
| `scripts/pick_modules.py` | 按分区召回候选模块。排序是单元数 → 缩放比 → 质感 → 关系编号；`--batch zones.txt` 一次做完整稿 |
| `scripts/review_packet.py` | 生成给含义审查员读的审查包 |
| `scripts/compose_page.py` / `start_page.py` | 用参考稿模块拼一页 / 整页照搬一张参考页 |
| `scripts/edit_page.py` | 按 id 改页，`batch` 可以一次执行多条命令 |
| `scripts/check_text.py` | 页面文字必须来自大纲，按短语逐段比对（第 4、5 步） |
| `scripts/group_page.py` | 收口时补齐页面角色、页头页脚组、每个模块一个带 bounds 的根组（第 5 步） |
| `scripts/find_library.py` / `install.py` | 找本次用的参考稿库（默认用已安装的库）/ 一次性把 Skill 和参考稿库装到 `~/.claude/` |
| `scripts/style_gap.py` | `baseline` 生成参考稿的指标范围和阴影配方；`check` 逐页对比成品（第 7 步） |
| `scripts/export.py` / `fix_cjk_fonts.py` | 导出，并把中文字体修成 OPPOSans |
| `scripts/check_reuse.py` / `check_modules.py` / `inline_icons.py` / `dump_blueprint.py` / `render.ps1` / `pm.py` | 辅助工具 |

**流程**：
- 第 0 步读 ppt-master；第 1 步读规范；
- 第 2 步主代理规划全稿，写 `plan.md`（批量挑模块、次色、连接件），再开普通子代理做含义审查；
- 第 3 步建项目、拼页；
- 第 4 步按工作量分段，开 fork 并行改页；
- 第 5 步收口：`check_text`、`group_page`、`stamp`、final 检查；
- 第 6 步导出；
- 第 7 步渲染，跑 `style_gap`，集中修一轮。

ppt-master 的位置用 `python scripts/pm.py` 查，目前在 `C:\Users\fanrh\.claude\plugins\cache\ppt-master\ppt-master\cc8b722a24e9-32c1cf49\ppt-master`。

## 4. Lab 里的资料

- `assets\rnb-core.pptx`：参考稿，65 页。
- `assets\rnb-blueprint\`：参考稿库，有 `import\`、`renders\`、`started-renders\`、`contact\`、`grid.txt`、`start-check.txt`、`style-baseline.json`（含阴影配方），以及 `modules.json`（247 个模块，**未经用户审定**）和 `modules-index.txt`。
  - `catalog-v1-superseded.md` 是旧目录；建测试目录时要从副本里删掉。
- `outlines\s11-fde.md`：8 页测试大纲，每页都有一句"结论"。
- `findings.md`：问题台账，目前 17 条共性问题加个例。
- `runs\`：每次运行一个目录，v3–v7 的目录里有 `comparison.md`、`sheet.png` 和 `run-log.md`；v6 另有 `reference-gap.md`，是和参考稿的差异量化。

## 5. 怎么测试（和真实使用完全一样）

用户只做一件事：在一个独立文件夹里放 `outline.md`，开会话说"用 Sam-PPT-Blueprint 把 outline.md 做成 PPT。"。**不让用户运行任何脚本**，`seed.py` 和测试钩子已经停用。

开发会话负责的准备：用要测的提交全局安装（Skill → `~/.claude/skills/`，库 → `~/.claude/sam-ppt/references/rnb/`，设为默认）。

```bash
T=$(mktemp -d) && git -C /d/Workspace/Sam-PPT-Skills archive <提交号> Sam-PPT-Blueprint | tar -x -C $T && python $T/Sam-PPT-Blueprint/scripts/install.py D:/Workspace/Sam-PPT-Lab/assets/rnb-core.pptx D:/Workspace/Sam-PPT-Lab/assets/rnb-blueprint --name rnb --default
```

本机当前装的是 018b41f。新文件夹不会继承任何 CLAUDE.md 或项目记忆（已核对 D 盘根目录、D:/Workspace、D:/PPT、~/.claude 下都没有 CLAUDE.md），所以天然隔离。

由开发会话代测时，在 `Sam-PPT-Lab/runs/<yyyymmdd-hhmm>_<对象>_<大纲>/` 里只放 `outline.md`，再用 `start_session` 开会话：
- `cwd` 设为该目录，`context: fresh`，`use_worktree: false`，`wake_when_done: true`；
- prompt 就是那一句话；
- background 只说"当前目录里有一份大纲 outline.md"。

**评估**：
- `python Sam-PPT-Blueprint/scripts/style_gap.py check ~/.claude/sam-ppt/references/rnb <deck.pptx> <renders>`；
- 拼一张总览图，看渲染图；
- 写 `comparison.md`；
- 更新 `findings.md`。

## 6. 历次测试结果（s11，8 页）

| 版本 | 提交 | 总用时（分钟） | 要点 |
|---|---|---:|---|
| v3 | 4ba35ac | 17.1 | 整页起页，质感最好，但图示含义常和内容不符 |
| v4 | 5a95cd8 | 24.3 | 有了逻辑和分区规范、含义审查，含义 8/8 正确，但质感退步 |
| v5 | 21199a7 | 23.8 | 质感优先、装饰保留，质感回升 |
| v6 | 9c7bbbe | 19.3 | 召回、审查包、原生图表，前期时间降下来了，但蓝多红少、结论条单薄、留白多 |
| v7 | 5ddb38a | 20.1 | 一句话提示词走完全程；留白回到参考稿范围；结论条、立体漏斗变好；次色和连接件仍不足 |

v7 的 `style_gap` 每页平均值，括号里是参考稿 p25–p75，对应字段名 `secondary_ratio`、`empty_pct`、`connectors`、`texture`、`shapes`：

| 指标 | v7 | 参考稿范围 |
|---|---:|---|
| 次色 / 主色面积比 | 0.23 | 0.39–0.96 |
| 留白 % | 11.6 | 7.2–13.1 |
| 连接件 | 2.1 | 5–13.5 |
| 渐变 + 阴影 | 2.9 | 4–16.8 |
| 形状数 | 75 | 100–137 |

## 7. 4834378 修了什么（还没测）

- **13 根组 bounds**：根因是 ppt-master 扁平页要求根节点写 `data-pptx-page-role`，写了以后每个根组都必须带 `data-pptx-bounds`。新增 `group_page.py`。用 v7 改页后、会话补边界之前的 8 页验证，final 检查从 8 页报错变成 0 阻断。
- **14 结构次色与强调分开**：交替的标题块、对比的一方、数据系列、结论标签属于结构次色，不受"强调只在一处"的限制。
- **15 分区间关系清单**：8 种关系、大纲里的信号词和对应连接件；有两个及以上分区的页至少一处连接件。
- **16 `check_text.py`**：页面文字必须来自大纲。拿 v7 成品试跑，查出 6 处补加的文字。
- **17 阴影配方**：参考稿的质感主要靠阴影，不是渐变。阴影配方是 `dx=2.8 dy=2.8 stdDeviation=2.7`，黑色，不透明度 0.4 或 0.22，加在实心圆和实色矩形上。

## 8. 30 页案例要注意的

- 用时：s11 的 8 页约 20 分钟；30 页时第 4 步最多 5 个代理同时写，重段先开。第 2 步规划全稿是主代理一个人做，会明显变长，要盯住。
- 用户能看出逻辑表达问题。重点观察：主关系判断、分区间连接件是否画对、含义审查有没有漏掉错配。
- 模块目录 `modules.json` 一直没有经过用户审定，每次运行都要在日志里注明。
- 30 页里会有参考稿没有的关系，比如路线图、组织结构、问题树。按 `page-zoning.md` 第四节，这类页改用原生图表、表格或关系原子，观察效果。

## 9. 踩过的坑

- **Bash 工具和中文**：
  - 控制台打印中文会乱码，要设 `PYTHONIOENCODING=utf-8`，或者把输出写进 UTF-8 文件再读；
  - python 里写路径用 `D:/...`，不要用 `/d/...`；
  - 在 heredoc 里写 python 字符串 `"\\n"` 会被转成真的换行，含 `\n` 的修改改用 Edit 工具。
- **`edit_page.py batch` 的 `\n` 被吃掉**：posix shlex 会把 `\n` 变成字母 n，4834378 之前的提交已经修好。
