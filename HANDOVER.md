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
| 基准大纲 | `benchmarks/`：只有大纲（考题）。`series1-ecom`（系列一，12 页）、`series2-nev`（系列二，16 页）、`series3-xhs`（系列三，14 页） |
| 评分工具包与私有存档 | **不在仓库里，也不写路径**。参考页截图、评分记录、对比工具、旧引擎导出物都在本机仓库之外的位置，路径记在主会话的本地记忆里（或问用户）。只有评分子代理可以打开 |
| 每次运行 | `Sam-PPT-Bain/runs/run-yyyymmdd-hhmmss-fff/`（gitignore；目前已清空） |

硬约定：每次有意义的修改都 `git commit` + `git push`（无需再问）；只有用户说"可以了"才算确认。

## 3. 系列一闭环结果（2026-10-21）

评分记录与对比图在评分工具包里。盲测得分：P1–P4 19/18/17/20；P5–P8 16/19/19/17；P9–P12 19/19/19/18。用户评价："这三批的质量超过我的预期"。

## 4. 下一步：新会话复现系列一，再测系列二、三

用户计划：先在新会话里按三角色流程重跑 `series1-ecom`，能复现第 3 节的成绩就算"成功了 75%"；之后再跑系列二、三。复现时第 1 轮**不改 Skill**，先看现有 Skill 的真实水平；只有某批不达标才按评分子代理的通用建议改规则重跑。做法见 `benchmarks/README.md` 的"三角色隔离"：

1. **编排会话（你）**：不打开评分工具包。把 `benchmarks/<case>/outline.md` 复制到 `D:\Workspace\tmp\<case>-outline.md`。
2. **生成子代理**：每批 4 页、每轮新开一个。提示要点：用 Skill 工具调用 `Sam-PPT-Bain` 并严格按 SKILL.md 执行；大纲用副本的第 X–Y 页；不得读取 git 历史、`HANDOVER.md`、`Sam-PPT-Bain\runs\` 下别人的目录；不得修改 Skill、不得 commit、不得改大纲；最后回报 RUN_DIR、每页原型与主视觉、省略之处、不满意之处、规则缺口。
3. **评分子代理**：每轮新开一个，把评分工具包路径、RUN_DIR、case、首页页码告诉它，让它按工具包 `README.md` 里的"评分子代理提示模板"执行；它只回报得分和**通用**改进建议。
4. 编排会话把通用建议写进 `references/`，提交推送，再开新的生成子代理重跑；每批最多 3 轮。
5. 全部完成后，请评分子代理把各批对比图汇总，发给用户判断。

## 5. 已踩过的坑

- Python 用 `python` 不用 `python3`；Bash 输出中文加 `PYTHONIOENCODING=utf8`；Python 字符串里写 Windows 路径用原始字符串（`r'D:\...'`），否则 `\t`、`\b` 会被转义。
- PowerPoint 渲染会锁文件；`git mv` 遇到锁会失败，改用复制 + `git rm`。
- 技术约束（已写进 page-patterns 四）：`filter` 只能挂单个图形；`marker-end` 只能挂 line/path；续行 tspan 重复父级 x；根层组不能重叠，跨组底板用根层 `rect` + `data-pptx-role="decoration"`；标题 ≤ 20 汉字。
- 图标名先查插件 `templates/icons/chunk-filled` 再用（没有 `check`、`gear`，要用 `checkmark`、`cog`）。
- 用户说"打包"时只做模板和规则，不要顺手跑整套案例。
