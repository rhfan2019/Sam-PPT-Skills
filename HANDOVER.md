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
| 每次运行 | 仓库之外：`%LOCALAPPDATA%\Temp\claude\Sam-PPT-Runs\Sam-PPT-Bain\run-yyyymmdd-hhmmss-fff\`（`sam_bain.py` 用 `tempfile.gettempdir()` 拼出，环境变量 `SAM_PPT_RUNS` 可覆盖）。Skill 目录下不再有 `runs\`；2026-10-21 已把旧运行目录全部移到这里。临时目录可能被系统清理，要保留的成品另存 |

硬约定：每次有意义的修改都 `git commit` + `git push`（无需再问）；只有用户说"可以了"才算确认。

## 3. 系列一闭环结果（2026-10-21）

评分记录与对比图在评分工具包里。盲测得分：P1–P4 19/18/17/20；P5–P8 16/19/19/17；P9–P12 19/19/19/18。用户评价："这三批的质量超过我的预期"。

### 复现测试（2026-10-21，新会话，三角色隔离，Skill 未改动）

三批都是第 1 轮达标：P1–P4 20/18/19/20；P5–P8 19/19/19/19；P9–P12 20/19/19/19（合计 230/240，上一轮 220/240）。是否算复现成功由用户判断。剩余扣分主要在"连接与流向"和"文字容器化"。

### 复现建议并入 Skill（2026-10-21，来源 `benchmarks/series1-ecom/rerun1-suggestions.md`）

已并入（都写成通用规则，Skill 里不引用建议文件）：
- **A1 连接与流向（1–6）**：page-patterns 新增"三C、模块之间的连接与对位"；硬性部分写成 rules 二.11"关系要画出来"。改动：建议里的"支撑：××"小标签会往页面上加大纲没有的词，改成"写着对应节点原词的小标签"。
- **A2 文字容器化（7–9）**：page-patterns 新增"三D、文字装进容器"；旅程曲线、U 形轨道两行构造同步改为"标签 + 小字 / 要点"。
- **A3 填满（10–12）**：并入 page-patterns 三B 的"卡片与格子要'满'"；"格子底部空白 ≤ 1/3"写进 rules 二.10。
- **A4 内容与精度**：13 矩阵按列归属 → rules 一.8 + 三B"阶段 × 维度"行；14 区块标题保留 → rules 一.7；15 运算符位置 → page-patterns 二"运算符"构件；16 图表关键点直接标数 → page-patterns 三"图内数据标签"。
- **B 技术类（1–5）**：粗线箭头改用单独三角形、水平镜像写法、主图与贴身标注同组 + U 形轨道标准拆组、英雄数字宽度（`sam_bain.py` 校准表新增 `hero` 56 px B 角色；数字旁标签放上下）、卫星圆间距 → page-patterns 一、二、三B、四。
- **B 规则空白类**：6 无结论页不自造论点条 → page-patterns 四末段；7 英雄数字退路 → rules 二.9 + page-patterns 二；8 字号种类怎么数 → page-patterns 一；9 高密度页下限（5 块 ≥ 40%，6–8 块 ≥ 35%，不删内容和区块标题）→ page-patterns 三B；10 一一对应先按语义再按顺序 → 三B；11 对齐暗示对应 → rules 二.11 + 三C 第 7 条，并把 rules 二.3 限定为"同一栏、同一组"；12 同结构 A→B 画出差异 → 三B；13 标题超长降到 34.67 / 32 px → page-patterns 四；14 页眉 / 页脚 / 署名字段来源 → SKILL.md 第 4 步表格；15 示意图注明"示意"、何时省刻度 → rules 一.2 + page-patterns 三 + SKILL.md 第 7 步；16 何时用图标、没用要说明 → page-patterns 二 + SKILL.md 第 7 步；17 结构词算不算加词 → rules 一.1 补充正反例。
- 顺带整理：`sam_bain.py` 校准表补 `thesis_xs`（21.33 px，论点条第三档）；page-patterns 删除两处带案例色彩的示例、修正标题"约 35 字"与 20 字上限的矛盾、把错位在表格外的一行并回三B 表、合并第四节里重复的 marker 规则。

未采纳：无。全部建议都已并入，"支撑"标签一条改写后采纳。高密度页的面积下限（40% / 35%）和标题降级字号（34.67 / 32 px）是建议没给数、由我定的值，需要在后续测试里验证。

### 系列二考试（2026-10-21）

考试模式（Skill 未改动，每批只跑 1 轮）：

| 批次 | 页 | 总分 | 达标 |
|---|---|---|---|
| 1 | P1 / P2 / P3 / P4 | 19 / 18 / 20 / 19 | 是 |
| 2 | P5 / P6 / P7 / P8 | 20 / 19 / 19 / 19 | 是 |
| 3 | P9 / P10 / P11 / P12 | 19 / 19 / 19 / 19 | 是 |
| 4 | P13 / P14 / P15 / P16 | 19 / 20 / 20 / 19 | 是 |
| 合计 | | 307 / 320 | |

RUN_DIR：
- 批次 1：`%LOCALAPPDATA%\Temp\claude\Sam-PPT-Runs\Sam-PPT-Bain\run-20261021-190524-436`
- 批次 2：`%LOCALAPPDATA%\Temp\claude\Sam-PPT-Runs\Sam-PPT-Bain\run-20261021-192522-795`
- 批次 3：`%LOCALAPPDATA%\Temp\claude\Sam-PPT-Runs\Sam-PPT-Bain\run-20261021-194319-069`
- 批次 4：`%LOCALAPPDATA%\Temp\claude\Sam-PPT-Runs\Sam-PPT-Bain\run-20261021-200434-800`

### 系列二考试后的修改（2026-10-21）

来源：`benchmarks/series2-nev/exam1-suggestions.md`（由一个只读 `series2-nev/scores.md` 的子代理摘出 20 条通用建议，舍弃 0 条；主会话没有打开评分工具包）。系列二考试扣分分布：连接 6 页、主视觉 2、精度 2、填满 / 容器化 / 内容各 1。

**运行目录与交付**
- 运行目录移出 Skill 目录：`sam_bain.py` 用 `tempfile.gettempdir()` 拼出 `<临时目录>\claude\Sam-PPT-Runs\Sam-PPT-Bain\`，`SAM_PPT_RUNS` 可覆盖；旧的 8 个运行目录已移过去，`.gitignore` 去掉 `**/runs/`；SKILL.md、CLAUDE.md、README、benchmarks/README、本文第 2 节同步。
- `finish` 末尾打印"成品"区块（PPTX、renders、contact.png 绝对路径 + 临时目录另存提示）；SKILL.md 第 7 步改成固定的中文最终回复模板（成品路径放第一行）。
- SKILL.md 第 6 步说明 OPPOSans 的字体安全提示属预期、可忽略（只这一类）。

**规则（全部写成通用规则）**
- 连接与对位 → page-patterns 三C 新增第 8–12 条（该不该连：同名原词 / 从属 / 组织轴，只是相邻不连；数量对不上：语义优先、括号多对一、并排编号圆一对多、配不上的不硬连；步骤带→下方区、左主图→右说明区、并列卡片组）；rules 二.11 指过去。建议 1–7 全采纳。
- 主视觉 → 三B 阶段行补"强调阶段要放大，不只换色"，新增"贯穿链路 + 并列路径""组织轴"两行（建议 8、9 + 1）。高密度页补 6 步腾空间顺序，并规定面积怎么量。
- 焦点 → rules 二.9：至少一个、同级不超过两个；第三个以上数字降到 28–32 px；结构相同的等权组（三项主角组、一排统一字号的并列数字）整体算一个焦点。
- 填满 → rules 二.10 + 三B"卡片与格子要满"：先补本块真实内容 → 再调尺寸（含建议 10、11）→ 再让邻块扩过来；禁止淡色大图标 / 大号淡色编号 / 水印字补位（同时删掉了原来"大号淡色编号卡片"的说法）。
- 小字 → page-patterns 一：10.67 / 12 px 的用途与上限，分类标签 ≥ 卡片标题 80% 或上实色块（建议 12）。
- 图标 → page-patterns 二"图标语义"：渲染后逐个确认，列出 11 类易误读图标与替代名（都在插件 `chunk-filled` 里核对过存在）。
- 论点条 → rules 一.5：先逐档降字号保持单行，21.33 px 仍超宽才断两行，两行仍放不下才改 `04a` 深色横条。
- 折线图 → page-patterns 三：五类必标点、≤ 8 点时全标，图注从对应区段引线（建议 2），小图表占满子区。
- 其他：容器化（建议 13）→ 三D.3；编号圆 / 胶囊 / 引线端点间距、列表等距（建议 14–18）→ 二"编号与间距"；双色栏头分界（建议 19）→ 二"栏头条"；不补括注、不改类别（建议 20）→ rules 一.1。

未采纳：无。

**由我自定、尚未验证的数值**：12 px 段落 ≤ 3 行、12 px 说明 ≤ 全页说明行数一半；10.67 px 每段 ≤ 10 字；第三个以上数字降到 28–32 px；两行论点条 21.33 px、基线 120.4 / 146.4（模板论点条高 61.26 能容纳，但还没在真实页面上渲染过）；侧栏最窄 25%（约 300 px）；次要块标题降到 14.67–16 px；栏间白缝 30→20 px、面板内边距 16→12 px；编号圆 r 10–14；胶囊间距 ≥ 高度 1/3、端点间隙 ≥ 1/4；折线 ≤ 8 点全标、标签上下间距 ≥ 14 px。高密度页下限 40% / 35% 维持不变：系列二主视觉扣分的 2 页都是"强调不够大"，不是面积不够，目前没有证据说明下限要改。

冒烟测试（自拟 2 页大纲，不算基准）：`new` → `finish` 通过，运行目录落在 `C:\Users\fanrh\AppData\Local\Temp\claude\Sam-PPT-Runs\Sam-PPT-Bain\run-20261021-205920-351`，Skill 目录与 `D:\Workspace` 下没有新增运行目录，成品区块正常打印。

## 4. 下一步：新会话复现系列一，再测系列二、三

用户计划：先在新会话里按三角色流程重跑 `series1-ecom`，能复现第 3 节的成绩就算"成功了 75%"；之后再跑系列二、三。复现时第 1 轮**不改 Skill**，先看现有 Skill 的真实水平；只有某批不达标才按评分子代理的通用建议改规则重跑。做法见 `benchmarks/README.md` 的"三角色隔离"：

1. **编排会话（你）**：不打开评分工具包。把 `benchmarks/<case>/outline.md` 复制到 `D:\Workspace\tmp\<case>-outline.md`。
2. **生成子代理**：每批 4 页、每轮新开一个。提示要点：用 Skill 工具调用 `Sam-PPT-Bain` 并严格按 SKILL.md 执行；大纲用副本的第 X–Y 页；不得读取 git 历史、`HANDOVER.md`、运行根下别人的运行目录；不得修改 Skill、不得 commit、不得改大纲；最后回报 RUN_DIR、每页原型与主视觉、省略之处、不满意之处、规则缺口。
3. **评分子代理**：每轮新开一个，把评分工具包路径、RUN_DIR、case、首页页码告诉它，让它按工具包 `README.md` 里的"评分子代理提示模板"执行；它只回报得分和**通用**改进建议。
4. 编排会话把通用建议写进 `references/`，提交推送，再开新的生成子代理重跑；每批最多 3 轮。
5. 全部完成后，请评分子代理把各批对比图汇总，发给用户判断。

## 5. 已踩过的坑

- Python 用 `python` 不用 `python3`；Bash 输出中文加 `PYTHONIOENCODING=utf8`；Python 字符串里写 Windows 路径用原始字符串（`r'D:\...'`），否则 `\t`、`\b` 会被转义。
- PowerPoint 渲染会锁文件；`git mv` 遇到锁会失败，改用复制 + `git rm`。
- 技术约束（已写进 page-patterns 四）：`filter` 只能挂单个图形；`marker-end` 只能挂 line/path；续行 tspan 重复父级 x；根层组不能重叠，跨组底板用根层 `rect` + `data-pptx-role="decoration"`；标题 ≤ 20 汉字。
- 图标名先查插件 `templates/icons/chunk-filled` 再用（没有 `check`、`gear`，要用 `checkmark`、`cog`）。
- 用户说"打包"时只做模板和规则，不要顺手跑整套案例。
