# Sam-PPT-Bain 交接文档

> 2026-10-21 更新。新会话先读本文和 `benchmarks/README.md`，再读 `Sam-PPT-Bain/SKILL.md`、`references/rules.md`、`references/page-patterns.md`。
> 本文放在仓库根而不是 Skill 目录里，是为了让盲测子代理调用 Skill 时接触不到任何基准信息。**不要把本文给盲测子代理看。**

## 1. 现状

- **架构**：薄外壳 + ppt-master。排版、检查、导出交给 ppt-master（插件只读）；Skill 目录只放模板工作区、规则、收尾脚本。旧的自研引擎已删除，**不要恢复，也不要再写排版引擎**。
- **模板**：`Sam-PPT-Bain/template/` 是 Deck（`sam-bain`）+ Style（`sam-bain-consulting`）工作区，6 个原型。封面、目录、章节、结束页 2026-10-21 经用户确认为基线（`references/approved/template-*.png`）。
- **独立性（用户硬要求）**：Skill 里不放任何案例的内容、数据、成品页；规则只能是通用构图 / 版面 / 技术规则。案例材料都在仓库根 `benchmarks/`。
- **规则来源**：`references/rules.md`（用户硬规则）与 `references/page-patterns.md`（坐标、构件、数据页型、三B 定性框架页、技术要点）。三B 的构造是用系列一（电商）做闭环对比时总结出的通用构图。

## 2. 位置与约定

| 项目 | 位置 |
|---|---|
| 仓库（私有） | https://github.com/rhfan2019/Sam-PPT-Skills ，分支 `main` |
| 本地 | `D:\Workspace\Sam-PPT-Skills`（个人 Skill 目录链接 `C:\Users\fanrh\.claude\skills\Sam-PPT-Bain` 指向 `Sam-PPT-Bain/`） |
| ppt-master | 插件 `~/.claude/plugins/cache/ppt-master/ppt-master/<hash>/ppt-master`（只读） |
| 参考 PPT 原件 | `参考模板`（80 页；`参考模板副本` 是同一文件） |
| 对照基准 | `benchmarks/`：`ecom-case`（系列一，已完成）、`series2-nev`（系列二，16 页，待测）、`series3-xhs`（系列三，14 页，待测）、`nev-case`（早期自编，暂停）、`tools/compare.py` |
| 私有存档（不在仓库） | `私有存档`：`_work`（旧引擎与 参考模板 全量 SVG 导入，含全部 80 页源码）、`bain_cmp`（80 页渲染图）、`runs`（2026-10-21 之前的全部运行）。**这是作弊高风险区，盲测子代理禁止访问** |
| 每次运行 | `Sam-PPT-Bain/runs/run-yyyymmdd-hhmmss-fff/`（gitignore；目前已清空） |

硬约定：每次有意义的修改都 `git commit` + `git push`（无需再问）；只有用户说"可以了"才算确认。

## 3. 系列一闭环结果（2026-10-21）

详见 `benchmarks/ecom-case/scores.md` 与 `results/`。盲测得分：P1–P4 19/18/17/20；P5–P8 16/19/19/17；P9–P12 19/19/19/18。用户评价："这三批的质量超过我的预期"。

## 4. 下一步：系列二、三迁移测试（在新会话进行）

用户要求：先在新会话里测试系列二、三，检验 Skill 换主题后是否仍"神似"。

1. 读 `benchmarks/README.md` 的"防作弊约定"和"闭环测试流程"，严格照做。
2. 把 `benchmarks/series2-nev/outline.md` 复制到 `D:\Workspace\tmp\series2-outline.md`（系列三同理），盲测子代理只读这份副本。
3. 每批 4 页由**新的**盲测子代理生成（提示模板见下），主会话用 `tools/compare.py` 对比、按评分表打分、写 `scores.md`、把通用差距写进 Skill、提交推送，每批最多 3 轮。
4. 全部完成后，把各批对比图汇总给用户判断。

盲测子代理提示要点（每次照抄并替换页码）：
- 用 Skill 工具调用 `Sam-PPT-Bain`，严格按 SKILL.md 执行；大纲用 `D:\Workspace\tmp\<case>-outline.md` 的第 X–Y 页。
- 禁止打开或搜索：`D:\Workspace\Sam-PPT-Skills\benchmarks\`、`D:\Workspace\Sam-PPT-Skills\HANDOVER.md`、`模板目录` 下的任何 PPTX、`私有存档`、git 历史（`git log -p` / `git show`）、`Sam-PPT-Bain\runs\` 下除自己新建以外的目录。
- 不得修改 Skill 文件、不得 commit、不得改大纲文字。
- 最后回复：RUN_DIR、每页原型与主视觉、对大纲的省略、仍不满意之处、Skill 规则里缺了什么。

## 5. 已踩过的坑

- Python 用 `python` 不用 `python3`；Bash 输出中文加 `PYTHONIOENCODING=utf8`；Python 字符串里写 Windows 路径用原始字符串（`r'D:\...'`），否则 `\t`、`\b` 会被转义。
- PowerPoint 渲染会锁文件；`git mv` 遇到锁会失败，改用复制 + `git rm`。
- 技术约束（已写进 page-patterns 四）：`filter` 只能挂单个图形；`marker-end` 只能挂 line/path；续行 tspan 重复父级 x；根层组不能重叠，跨组底板用根层 `rect` + `data-pptx-role="decoration"`；标题 ≤ 20 汉字。
- 图标名先查插件 `templates/icons/chunk-filled` 再用（没有 `check`、`gear`，要用 `checkmark`、`cog`）。
- 用户说"打包"时只做模板和规则，不要顺手跑整套案例。
