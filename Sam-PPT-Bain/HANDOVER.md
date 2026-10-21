# Sam-PPT-Bain 交接文档

> 2026-10-21 更新（基准闭环测试完成第一遍）。新会话先读本文，再读 `SKILL.md`、`references/rules.md`、`references/page-patterns.md`，最后读仓库根的 `benchmarks/README.md` 与 `benchmarks/ecom-case/scores.md`。

## 1. 现状

- **架构**：薄外壳 + ppt-master。排版、检查、导出交给 ppt-master（插件只读）；本目录只放模板工作区、规则、收尾脚本。旧的自研引擎已删除，**不要恢复，也不要再写排版引擎**。
- **模板**：`template/` 是 Deck（`sam-bain`）+ Style（`sam-bain-consulting`）工作区，6 个原型。封面、目录、章节、结束页 2026-10-21 经用户确认为基线（`references/approved/template-*.png`）。
- **独立性（用户硬要求）**：Skill 里不放任何案例的内容、数据、成品页；生成时不得读取 `benchmarks/`。案例材料都在仓库根 `benchmarks/`。
- **规则来源**：`references/rules.md`（用户硬规则）与 `references/page-patterns.md`（坐标、构件、数据页型、三B 定性框架页、技术要点）。三B 的构造是 2026-10-21 用参考 PPT（参考模板 第一个系列，12 页）做闭环对比时总结出的**通用构图**，不含文字和数据。
- **用户确认过的效果**：只有模板 4 个原型。其他页面都不是基线；不要自己宣布通过。

## 2. 位置与约定

| 项目 | 位置 |
|---|---|
| 仓库（私有） | https://github.com/rhfan2019/Sam-PPT-Skills ，分支 `main` |
| 本地 | `D:\Workspace\Sam-PPT-Skills\Sam-PPT-Bain`（个人 Skill 目录链接 `C:\Users\fanrh\.claude\skills\Sam-PPT-Bain` 指向这里） |
| ppt-master | 插件 `~/.claude/plugins/cache/ppt-master/ppt-master/<hash>/ppt-master`（只读） |
| 参考 PPT | 仓库根 `参考模板`（80 页，未纳入 git，52 MB） |
| 对照基准 | 仓库根 `benchmarks/`：`ecom-case/`（电商 12 页大纲 + 参考图 + 评分记录 + 对比图）、`nev-case/`（新能源，暂停） |
| 每次运行 | `runs/run-yyyymmdd-hhmmss-fff/`（不提交） |

硬约定：每次有意义的修改都 `git commit` + `git push`（无需再问）；只有用户说"可以了"才算确认。

## 3. 基准闭环测试（2026-10-21）

做法见 `benchmarks/README.md`：按大纲分批（每批 4 页）生成 → 与参考页并排 → 10 项评分（满分 20，≥16 且无 0 分达标）→ 把差距写成通用规则 → 重跑，每批最多 3 轮。

- **盲测**：从第 1 批 R2 起，生成一律交给**没看过参考页的子代理**（只给 Skill + 大纲副本 `D:\Workspace\tmp\ecom-outline.md`，明确禁止读 `benchmarks/`、`参考模板`、其他 runs），主会话只负责对比、评分、改规则。主会话看过参考页，自己生成不算数。
- **结果**（详见 `benchmarks/ecom-case/scores.md`，对比图在 `benchmarks/ecom-case/results/`）：
  - 第 1 批 P1–P4：R1 主会话 19/19/19/20（不算），R2 盲测 19/18/17/20 达标；
  - 第 2 批 P5–P8：R1 盲测 16/19/19/17 达标；
  - 第 3 批 P9–P12：R1 盲测 19/19/19/18 达标。
- **用户评价（2026-10-21）**：看过三张对比图后说"这三批的质量超过我的预期"。这是对 Skill 当前水平的认可；成品页属于案例内容，按独立性要求不放进 Skill 的 `references/approved/`，对照记录留在 `benchmarks/ecom-case/`。

## 4. 下一步

1. 迁移性验证：用一份**不同主题**的大纲（可恢复 `benchmarks/nev-case/`）盲测，确认三B 的通用构造不只适用于电商这 12 页。
2. 仍待改进的共性问题：高密度页主视觉被挤到 30% 左右；分层图与策略之间的连接箭头偏少。

## 5. 已踩过的坑

- Python 用 `python` 不用 `python3`；Bash 输出中文加 `PYTHONIOENCODING=utf8`；长路径会让 Python 起不来，临时文件放 `D:\Workspace\tmp`。
- PowerPoint 渲染会锁文件；`git mv` 遇到锁会失败，改用复制 + `git rm`。
- 技术约束（已写进 page-patterns 四）：`filter` 只能挂单个图形；`marker-end` 只能挂 line/path；续行 tspan 重复父级 x；根层组不能重叠，跨组底板用根层 `rect` + `data-pptx-role="decoration"`；标题 ≤ 20 汉字；结构化模板 master 只放背景。
- 图标名先查插件 `templates/icons/chunk-filled` 再用（如没有 `check`、`gear`，要用 `checkmark`、`cog`）。
- 用户说"打包"时只做模板和规则，不要顺手跑整套案例。
