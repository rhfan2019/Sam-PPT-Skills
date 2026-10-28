---
name: Sam-PPT-Blueprint
description: 蓝图重绘法：把用户给的 PPT 大纲做成可编辑 PPTX，学参考稿（如 rnb-core.pptx）的"神韵"而不是只换颜色。每页先按逻辑表达规范判断内容是什么关系（循环、流程、层级、对比、漏斗、构成、时间线、战略框架等）、该用什么图示，再按页面分区规范切分区，从参考稿拆好的模块目录里为每个分区挑模块（可来自不同参考页），拼成一页后原地换成大纲内容，保留模块的坐标、渐变、阴影、半透明和装饰，删掉含义不符的部件。主代理规划全稿，独立子代理审查图示含义，再用 fork 子代理分段并行改页。底层引擎是 ppt-master（Quick Generate，自由设计、扁平导出，不装模板、不走 mirror）。用户给出大纲要求做 PPT 并提到 Sam-PPT-Blueprint 或蓝图重绘，或给出大纲和参考稿、要求"照这份模板的感觉做 PPT"时使用；用户没提参考稿时用已安装的默认参考稿库。不负责写大纲，不改大纲内容。
---

# Sam-PPT-Blueprint

**薄外壳**：项目初始化、检查、图表核对、导出全部用 ppt-master 自己的 Quick Generate 流程，不修改 ppt-master 的任何文件。`python scripts/pm.py` 打印它的位置（下文记作 `<PM>`，可用环境变量 `PPT_MASTER_DIR` 覆盖）。

本 Skill 提供：

| 文件 | 作用 |
|---|---|
| `references/logic-diagrams.md` | **逻辑表达规范**：内容结构卡；关系 → 图示 → 必备部件 → 禁用部件；部件含义与删改规则；箭头和颜色；复合页面 |
| `references/page-zoning.md` | **页面分区规范**：页面解剖、栅格、10 个分区模板、挑模块的顺序、组合后的统一检查 |
| `references/module-catalog.md` | 参考稿模块目录 `modules.json` 的拆法和字段 |
| `references/fork-brief.md` | 第 4 步开 fork 用的任务说明 |
| `references/review-brief.md` | 第 2 步末尾开含义审查子代理用的任务说明 |
| `scripts/prepare_reference.py` | 参考稿只预处理一次：导入、渲染、缩略总览、栅格、逐页起页检查、起页后渲染 |
| `scripts/compose_page.py` | 用外壳页加若干模块（可来自不同参考页）拼出一页，可平移和等比缩放 |
| `scripts/start_page.py` | 整页照搬一张参考页作为起点 |
| `scripts/inline_icons.py` | 起页时把参考稿的小矢量图标（页头手形等）转成原生可编辑形状，`start_page` 和 `compose_page` 自动调用 |
| `scripts/edit_page.py` | 按 id 改页：列模块、改字、删、平移、复制、换色、清扫，可一次批量执行 |
| `scripts/check_reuse.py` | 页面还剩多少形状来自参考稿（只作提示） |
| `scripts/check_modules.py` | 核对模块目录（实际搬走多少元素、留下什么、关系编号），用 `--write` 写入质感指标并生成一行一个模块的 `modules-index.txt` |
| `scripts/pick_modules.py` | 按分区的关系编号、单元数、分区尺寸，从目录里按挑选顺序列出候选的完整条目和裁切图；`--batch` 一次做完整稿所有分区 |
| `scripts/check_text.py` | 列出页面上不是来自大纲原文的文字（作者补的读法标签、参考稿残留） |
| `scripts/group_page.py` | 收口时给页面补 ppt-master 要求的根结构：页面角色、页头页脚组、每个模块一个带 bounds 的根组 |
| `scripts/find_library.py` | 找本次用的参考稿和参考稿库：默认用已安装的库，用户给了参考稿就找它的库 |
| `scripts/install.py` | 一次性安装：Skill 装到 `~/.claude/skills/`，参考稿库装到 `~/.claude/sam-ppt/references/` |
| `scripts/style_gap.py` | 参考稿的次色面积、留白、连接件、质感范围（预处理时生成 `style-baseline.json`），以及成品逐页和它的对比 |
| `scripts/review_packet.py` | 把规划、大纲原文、用到的模块的关系部件按页拼成一个审查包，给含义审查员读 |
| `scripts/export.py` | 代替直接调用 `svg_to_pptx.py`，修好中文字体（见"中文字体"） |
| `scripts/render.ps1` | PowerPoint 渲染成 PNG |
| `scripts/dump_blueprint.py` | 列出一页的全部形状和配色（需要细看时用） |

## 输入

- **大纲**：逐字使用。不增删、不合并、不改写任何信息点和数字；版面放不下时调整版面，不砍内容。信息密度归 Sam-PPT-Outline 管。
- **参考稿库**：用 `prepare_reference.py` 预处理过的目录，包括 `import/`、`renders/`、`started-renders/`、`contact/`、`grid.txt`、`start-check.txt`、`style-baseline.json`，以及按 `module-catalog.md` 拆好、经用户审定的模块目录 `modules.json` 和它的一行索引 `modules-index.txt`（`check_modules.py --write` 生成）。
- **运行目录**：用户没指定时，就是当前工作目录；项目、成品、渲染图和运行日志都放在这里，不写到运行目录以外。

用户通常只说一句"用 Sam-PPT-Blueprint 把 X 做成 PPT"，可能带上"参考 Y"。下面这些不问用户，按默认来：
- 大纲：用户点名的文件；没点名时用运行目录里唯一的 `.md` 大纲。
- 参考稿和参考稿库：运行 `python scripts/find_library.py [<用户说的参考稿路径或名称>]`，用它打印的 `library:` 和 `reference:`。
  - 用户没提参考稿时，它取已安装的默认库（`~/.claude/sam-ppt/references/`，由 `install.py` 安装）；
  - 用户给了参考稿文件时，先找文件旁边的库，再找已安装的同一份稿的库；
  - 都找不到时，它会打印预处理命令：运行 `prepare_reference.py`（约 2 分钟），再按 `module-catalog.md` 拆模块目录（可以开子代理分段拆）。没有任何已安装库、用户也没提参考稿时，问用户要参考稿。
  - 库里缺 `style-baseline.json` 时补跑 `python scripts/style_gap.py baseline <参考稿.pptx> <参考稿库>`。
- 运行产物（项目、计划、日志、成品）都放运行目录，不写进参考稿库。

**安装**（每台机器一次，Skill 或参考稿库更新后再跑一次）：`python scripts/install.py <参考稿.pptx> <参考稿库> --name <名称> [--default]`。它把 Skill 装到 `~/.claude/skills/`，把参考稿库连同参考稿装到 `~/.claude/sam-ppt/references/<名称>/`。之后用户在任何放着大纲的文件夹里说一句话即可。
- 模块目录没有用户审定记录时，照用，并在运行日志和最终汇报里注明"模块目录未经审定"。
- 计时、`plan.md`、运行日志、成品 `deck.pptx` 和 `renders/`、最终汇报，都按本文件的规定做，不需要用户提要求。

## 流程

每一步开始和结束都用 `date "+%Y-%m-%d %H:%M:%S"` 记入运行目录的 `timing.txt`。

### 0. 读 ppt-master（只读这些）

`python <PM>/scripts/attribution_guard.py`；`<PM>/SKILL.md`、`workflows/routing.md`、`workflows/profiles/quick-generate.md`、`references/shared-standards-core.md`、`references/executor-base.md`、`references/executor-chart.md`、`references/native-data-interface.md`、`templates/charts/chart-vocabulary.md`。路线固定为 **Generate PPTX → Quick，自由设计（flat）**，不问用户。

### 1. 读规范和参考稿库

读 `references/logic-diagrams.md`、`references/page-zoning.md` 全文，`<参考稿库>/grid.txt`、`start-check.txt`。**不通读** `modules-index.txt` 和 `modules.json`，也不翻整页渲染图：候选模块在第 2 步按分区用 `pick_modules.py` 取。（ppt-master 选图表也是这样：`visualization_recall.py` 从索引按语义召回候选，再由代理判断。）

### 2. 规划全稿（主代理一次做完，写进 `plan.md`）

对大纲的每一页：

1. **填内容结构卡**（`logic-diagrams.md` 第一节）：结论、单元、维度、方向、闭合、权重、数量、好坏、次要信息。
2. **定关系**：按 `logic-diagrams.md` 第二节的判断标准，定出**主关系**（直接证明结论的那个，一页一个）和最多一个**次要关系**，写编号。依赖词、循环词、多维对比是硬信号。
3. **定分区**：按 `page-zoning.md` 第三节选一个分区模板，用 `grid.txt` 算出每个分区的坐标。
4. **挑模块**：先把全稿每页的分区写进 `<运行目录>/work/zones.txt`，一行一个分区（结论条不写，它按 `page-zoning.md` 第六节自己画）：
   ```
   P02 主图 --logic E2 --units 5 --zone 800x440
   P02 侧栏 --logic C4 --units 3 --zone 392x440 --role 文字栏
   ```
   然后**一次**跑完：
   ```
   python scripts/pick_modules.py <参考稿库>/modules.json --batch <运行目录>/work/zones.txt --crops-dir <运行目录>/work > <运行目录>/work/picks.txt
   ```
   它按 `page-zoning.md` 第四节的顺序过门槛、排先后（单元数 → 缩放比 → 质感 → 关系编号是否为模块的第一个），每个分区列前 3 个候选的完整条目（含 `parts`、`not_for`），每页拼一张裁切图 `work/pick-PNN.png`。主代理读 `picks.txt`，每页看一张裁切图，逐条核对第一名的 `parts` 和 `not_for`；不成立就看下一名。写下要删改的关系部件。某个分区"没有过门槛的模块"时，用 ppt-master 的原生图表或表格（`chart/<key>`、`table/<key>`），或用 `executor-structure.md` 的关系原子手写，但整页的外壳和其余分区仍来自参考稿。
   **按数据画的图**按 `page-zoning.md` 第四节分两种：模块本身是立体形状图的，保留形状和渐变，只按数据改尺寸；只有扁平外框的，用 ppt-master 原生图表模板（`chart-vocabulary.md`，按 `native-data-interface.md` 写数据），漏斗用 `funnel_chart`。
5. **定连接和配色**：按 `page-zoning.md` 第六节，写每个分区和相邻分区的关系及连接件（先过第六节第 4 条的清单再写"无"），以及这一页的结构次色单元和唯一的强调处。
6. **定图标**：每个要换的图标写"模块 → 图标 → 理由"，图标意思要和内容对应；参考稿自带、意思不符的语义图标要换掉。

`plan.md` 只写决策，不写理由和描述（ppt-master Quick 的决策本来只留在上下文里；这份文件只为给审查员和 fork 对照）。格式固定：

```
## 全稿约定
外壳页 NN｜页头右侧标签｜页脚写法｜主色 #…、次色 #…（次色用在哪，page-zoning 第六节）｜好色 #…、坏色 #…｜结论条样式｜图标库｜正文/说明字号下限

## P01 <页文件名>
结论：…｜主 D2 / 次 D3｜<分区模板>｜次色：结构 哪些单元；强调 哪一处｜图标：模块 → 图标｜图表：chart/<key> 数据…
| 分区 | 模块 | 来源 bbox → 目标 X,Y,W | 大纲条目 → 位置 | 删改的关系部件 | 和相邻分区 → 连接件 |
|---|---|---|---|---|---|
| 主图 | 49-B | 49:x,y,w,h @X,Y,W | 四步 → 环上 4 节点 | 删第 5 节点；弧箭头重画成 4 段闭环 | 结果 → 侧栏：横向实心箭头 |

## 分工
段 1（主代理）：P01｜段 2：P02｜…

## 推算值
P02 漏斗层宽：…＝…
```

每个分区一行；不写结构卡、不抄 `parts` 原文、不写"保留的部件"（未列出的就是保留）。

**含义审查（必做）**：写完 plan.md 后运行 `python scripts/review_packet.py <运行目录>/plan.md <大纲> <参考稿库>/modules.json -o <运行目录>/work/review-packet.md`，它按页把大纲原文、规划行、所用模块的关系部件拼成一个文件，并在旁边生成所用模块的裁切图。然后开一个**普通子代理**（不用 fork，要它不带主代理的思路），prompt 用 `references/review-brief.md`。它逐页回答"按这个规划，读者从图上会读出什么关系，和大纲是否一致"。主代理按审查意见改 plan.md，并在 plan.md 末尾写"审查与处理"一段（每条一行），然后再进入第 3 步。

### 3. 建项目并拼页（主代理）

按 quick-generate.md：`project_manager.py init <名称> --format ppt169 --dir <运行目录> --quick-generate`，`import-sources <项目> <大纲> --copy`，`text_measure.py calibrate`，`icon_sync.py` 一次同步 plan.md 里用到的全部图标。然后按规划表给每一页拼页：

```
python scripts/compose_page.py <项目>/svg_output/NN_页名.svg <参考稿库>/import/authoring-svg-flat shell=<外壳页> <页>:<x>,<y>,<w>,<h>@<X>,<Y>[,<W>] ...
```

目标宽度 W 按 `page-zoning.md` 第六节第 3 条取（分区高和分区宽都要照顾到），有结论条的页给它留出底部 72。拼完每页跑一次 `edit_page.py sweep`。模块紧贴页边时，参考稿原文可能伸出页面，单页检查会报"exceeds the root viewBox"；换成大纲文字后通常就消失了，拼页时也可以给模块留出 20–40 px 边距。整页恰好合适时，也可以 `python scripts/start_page.py <参考稿库>/import/authoring-svg-flat/slide_NN.svg <项目>/svg_output/NN_页名.svg`。两者都会删掉图片和图片裁剪框、指向被删元素的连接线绑定、自定义几何的源信息、导入插画；把参考稿的小矢量图标转成原生形状；把组上的阴影移到形状上；把描边渐变改成首色；把参考稿字体统一成 OPPOSans；其余全部保留，并在页面里记下来源。

### 4. 分段并行改页（fork）

**分段规则**：按工作量分，不按页数平分。每页工作量 = 1 + 0.5 × 按数据画的图（原生图表或要按数据定尺寸的形状）个数 + 0.5（分区 ≥ 4 时）。总量 ≤ 4：主代理全写，不开子代理。否则：工作量 ≥ 1.5 的页各自单独一段；其余的页两页一段，两页合计不超过 2.5。同时在写的代理最多 5 个（主代理 + 4 个 fork），主代理拿最轻的一段；段多于 5 时，每收到一个 fork 完成通知就开下一段，重段先开。

**开法**：第 3 步做完后，**在同一条消息里**用 Agent 工具为段 2 起的每一段开一个 `subagent_type: "fork"` 的子代理，prompt 用 `references/fork-brief.md`，只替换尖括号里的值。fork 继承主代理到此为止读过的规范、目录、大纲和 plan.md 的思考过程，不用重读、不用重新理解大纲。然后主代理立即写段 1，不等 fork。会话里没有 fork 类型时，按 fork-brief.md 末尾的说明退回普通子代理。（ppt-master `executor-base.md` 要求只由主代理写页，理由是各页共享上游上下文；fork 继承同一份上下文，满足这一本意。用户同意用 fork 并行。）

**每页的改法**（主代理和 fork 相同）：
1. `python scripts/edit_page.py list <页>` 看模块 id 和文字。
2. 用 `edit_page.py batch <页> "命令 ; 命令 ; …"` 一次做完这一页的修改，按这个顺序：
   - **删**：plan.md 里"要删改的部件"；参考稿的模块里大纲用不上的单元；参考稿内容（品牌名、产品名、案例文字、水印文字）整块删除。**装饰（渐变底、阴影、光斑、光条、底板、立体光泽）保留**，删单元时不要连带删掉它下面的底板。
   - **数量**：大纲条目比模块多，`clone` 同类部件并按原间距平移；编号圆、底色等同一行的部件要一起复制或平移。条目少就删掉多余的单元，再平移剩下的单元，把空出来的位置收拢。
   - **文字**：`text <id> 新文字` 在原文本元素里换成大纲原文，保留位置、字体、字号、颜色和对齐；`\n` 换行。放不下时先换行，再微调这个文本框。页面上的每一段文字都必须是大纲原文，或从大纲条目里截取的词组（标题块、维度名、单位）；不补读法说明（阶段名、分组名、"（缺）"、副标题之类）。图示读不懂时改图示，不加字。
   - **颜色**：按全稿约定的颜色角色；箭头方向跟数值，颜色跟好坏（`logic-diagrams.md` 第四节），需要时用 `color` 对调。plan.md 写的次色单元用 `color` 改成次色实填（标题块、编号圆、关键层）。
   - 最后一条命令固定是 `sweep`（删除部件后，清掉没有几何的形状和空组，否则导出会失败）。
3. **图片位**：被删图片留下的位置，用图标库图标、数字或简单形状补上，或让相邻模块占用。**参考稿里用图片做的图表**（起页后整块消失）：在原位置按大纲数据画原生图表。
4. **图表**：模块里的原生图表保留位置和样式，换成大纲数据。参考稿用形状画的数据图（漏斗、圆柱、条形），按 plan.md 换成 ppt-master 原生图表模板，放在原图的位置，外框和装饰保留；不手工重算形状尺寸。按 verify-charts 核对。
5. **版式补齐**（`page-zoning.md` 第六节）：分区铺到主体带底边，并排的顶边、底边对齐；按 plan.md 画分区间连接件；按固定样式画结论条；实心圆、实色标题块、结论条按 `style-baseline.json` 的阴影配方加阴影；分区标题字号不大于页面标题。
6. **部件核对**：逐个读这一页留下的**关系部件**（箭头、环、连线、上下箭头、`+`、连接各块的光束、大小差异、强调色、语义图标），按 `logic-diagrams.md` 第三节的删改规则，含义不成立的就删或改；装饰不动。
7. 单页检查：一段的页**全部写完后**跑一次 `python scripts/check_text.py <大纲> <这几页>`，列出的文字换成大纲原文或删掉；再每页一条 `python <PM>/scripts/svg_quality_checker.py <项目> --quick-generate --canonical-authoring --stage page --page <页文件名>`，有阻断就集中修一轮再跑一次。不要每改一处就检查（ppt-master Quick 的检查节奏：只在检查点和一次集中修改后跑，不为提前验证写法而跑）。
8. **不要新建空白 SVG 自己构图。** 需要新增的小构件（图表、图标、补位形状、连接件、结论条）可以手写，但整页的外壳和各分区必须来自参考稿模块。
9. **新画的形状放进独立的根组**（`<g id="pNN-…" data-pptx-bounds="x y w h">` 直接挂在根 `<svg>` 下；忘了写 bounds 的，第 5 步 `group_page.py` 会补），不要塞进带 `data-pptx-object="shape"` 的导入形状组：导出器只取那种组的几何，组里新加的箭头、图标会丢（v5 第 3 页的环形箭头就是这样丢的）。

**SVG 写法上踩过的坑**：阴影 `filter` 加在具体形状上，不加在 `<g>` 上；角色图元要有 `id`；折线不要用 `marker-end`；图表 JSON 里不能出现裸 `<`；用 OPPOSans B / H 的文字同时写 `font-weight="bold"`；续行 `tspan` 重复父元素的 `x`；模块边界不要互相压线；少数参考页起页后仍有检查错误（见 `start-check.txt`），用到这一页时一并处理。

### 5. 收口检查（主代理，所有段完成后）

逐条核对 plan.md 的全稿约定和 `page-zoning.md` 第五节的统一检查，在 plan.md 写"核对"一段。跑一次 `python scripts/check_reuse.py <项目>/svg_output <参考稿库>/import/authoring-svg-flat`，看每页还剩多少来自参考稿。**这个比例只作提示**：因含义不符删掉部件、为收拢空白移动模块、把形状图换成原生图表而降低，是正确的；低于 50% 的页在运行日志里写一句原因即可，不要为了比例保留错误部件或留白。然后跑 `python scripts/check_text.py <大纲> <项目>/svg_output/*.svg`，必须没有输出；再 `python scripts/group_page.py <参考稿库>/grid.txt <项目>/svg_output/*.svg`，给每页写上页面角色、页头页脚组和每个模块一个带 `data-pptx-bounds` 的根组（ppt-master 扁平页的硬规则，`executor-base.md`、`shared-standards-core.md` §4.3；不要自己另写包组脚本）；然后 `stamp_native_fallbacks.py <项目>/svg_output --write`，`svg_quality_checker.py <项目> --quick-generate --canonical-authoring --stage final --json`，必须 0 阻断。

**禁止**：`--skip-validation`、`--enable-dangerous-nonconforming-svg-export`；不装模板、不用 mirror 模式。

### 6. 导出

```
python scripts/export.py <项目> --quick-generate --no-notes --native-charts-and-tables -o <运行目录>/deck.pptx
```

最后一行必须是 `0 YaHei slot(s) left`，否则退出码为 1。

### 7. 渲染自检（集中修一轮）

```
powershell -ExecutionPolicy Bypass -File scripts/render.ps1 <运行目录>/deck.pptx <运行目录>/renders
```

再跑一次风格对比，结果写进运行日志：

```
python scripts/style_gap.py check <参考稿库> <运行目录>/deck.pptx <运行目录>/renders
```

它逐页给出次色面积、留白、连接件、渐变加阴影，并标出超出参考稿范围的项。然后先看全部页，一次列全这些问题：
- **风格对比标出的项**：次色面积不够的，按全稿约定把次色单元实填；留白多的，按 `page-zoning.md` 第六节铺满；连接件少的，补 plan.md 写了而没画的连接件；质感低的，按它打印的阴影配方给实心圆、实色块补阴影，找回被删的装饰。大纲内容本来就少的页可以低于参考稿密度，但不能苍白、空、互不相连。
- **版面**：溢出、压字、裁切、低对比、参考稿残留、拼贴感、字号层级（分区标题大于页面标题）、结论条不合第六节的样式。
- **含义**：看着渲染图，把每个箭头、环、连线、上下箭头、颜色、大小、强调读一遍，读出的关系必须和大纲一致（`logic-diagrams.md` 第三、四节）。

然后**集中修一轮**，再走第 5、6 步、渲染复查和风格对比。要修的页多于 3 页时，可以按第 4 步的方式开 fork 分页修。页面能不能当基线由用户决定。

## 中文字体

ppt-master 的导出器只认一张固定的中文字体名单，OPPOSans 不在里面，所以中文会被写成微软雅黑。`export.py` 做两层修复，都不改 ppt-master 的文件：

- **A（主）**：在同一个进程里把 OPPOSans 各字重加进导出器的中文字体名单，再调用 ppt-master 自己的导出入口。
- **B（兜底）**：导出后运行 `scripts/fix_cjk_fonts.py`。英文是 OPPOSans 而中文是雅黑或主题引用时，中文改成同一字重的 OPPOSans；英文跟随主题而中文写死雅黑时，中文也改为跟随主题；主题里中文字体跟随同一块的英文字体。其他字体一律不动。A 生效时它改 0 处。也可单独用：`python scripts/fix_cjk_fonts.py deck.pptx [-o out.pptx]`。

## 运行日志

在运行目录写 `run-log.md`：开头是计时表（步骤、开始、结束、用时、工具调用次数，第 4 步拆到每一段和每一页），然后是 plan.md 的规划表、含义审查结果与处理、`check_reuse.py` 结果（低于 50% 的写原因）、检查和导出结果、修改前后两次 `style_gap.py` 的表、`check_text.py` 的结果（应为空）、修改轮次、剩余问题（如实写）。

## 最终汇报

做完后用中文向用户汇报，用户不必另外要求：
- 成品位置（`deck.pptx`、`renders/`）和总用时，各步用时一行一项；
- 每页一行：主关系、分区模板、所用模块及质感档位、哪些分区用了原生图表、次色用在哪；
- 含义审查查出了什么、怎么处理的；
- 修改后的 `style_gap.py` 表，以及仍超出参考稿范围的项和原因；
- 剩余问题（如实写），以及"模块目录未经审定"之类的说明。
