---
name: Sam-PPT-Blueprint
description: 蓝图重绘法：把用户给的 PPT 大纲做成可编辑 PPTX，每页按版式目录从参考稿（如 rnb-core.pptx）里选一页作蓝图，把这一页的 SVG 复制过来，在上面删掉参考稿的图片和内容、换成大纲内容，保留它的坐标、主图示、渐变/阴影/半透明和装饰，学到参考稿的"神韵"而不是只换颜色。主代理先规划全稿，再用 fork 子代理分段并行改页。底层引擎是 ppt-master（Quick Generate，自由设计、扁平导出，不装模板、不走 mirror）；本 Skill 只加参考稿预处理、按目录选蓝图、起页与改页工具、并行分工、OPPOSans 中文字体修复和 PowerPoint 渲染自检。用户给出大纲和参考稿要求"照这份模板的感觉做 PPT"、提到 Sam-PPT-Blueprint、蓝图重绘时使用。不负责写大纲，不改大纲内容。
---

# Sam-PPT-Blueprint

**薄外壳**：项目初始化、检查、图表核对、导出全部用 ppt-master 自己的 Quick Generate 流程。不修改 ppt-master 的任何文件；`python scripts/pm.py` 打印它的位置（下文记作 `<PM>`，可用环境变量 `PPT_MASTER_DIR` 覆盖）。

本 Skill 提供：

| 文件 | 作用 |
|---|---|
| `scripts/prepare_reference.py` | 参考稿只预处理一次：导入、渲染、缩略总览、逐页起页检查 |
| `scripts/start_page.py` | 把蓝图页复制成项目页面，作为修改的起点 |
| `scripts/edit_page.py` | 按 id 改页：列模块、改字、删、平移、复制、换色、清扫，可一次批量执行 |
| `scripts/check_reuse.py` | 页面还剩多少形状来自蓝图 |
| `scripts/export.py` | 代替直接调用 `svg_to_pptx.py`，修好中文字体（见"中文字体"） |
| `scripts/render.ps1` | PowerPoint 渲染成 PNG |
| `scripts/dump_blueprint.py` | 列出一页的全部形状和配色（需要细看时用） |
| `references/fork-brief.md` | 第 4 步开 fork 用的任务说明 |

## 输入

- **大纲**：逐字使用。不增删、不合并、不改写任何信息点和数字；版面放不下时调整版面，不砍内容。信息密度归 Sam-PPT-Outline 管。
- **参考稿库**：用 `prepare_reference.py` 预处理过的目录，里面有 `import/`、`renders/`、`contact/`、`start-check.txt`，以及用户审定过的版式目录 `catalog.md`。只给了参考稿 PPTX 时，先运行 `python scripts/prepare_reference.py <参考稿.pptx> <参考稿库>`（约 1 分钟）；没有 `catalog.md` 时按下面第 2 步的逻辑表看缩略总览选页，并在运行日志里注明"无版式目录，选页未经审定"。
- **运行目录**：在 Skill 目录之外，由用户指定；项目、成品、渲染图和运行日志都放在这里。

## 流程

每一步开始和结束都用 `date "+%Y-%m-%d %H:%M:%S"` 记入运行目录的 `timing.txt`。

### 0. 读 ppt-master（只读这些）

`python <PM>/scripts/attribution_guard.py`；`<PM>/SKILL.md`、`workflows/routing.md`、`workflows/profiles/quick-generate.md`、`references/shared-standards-core.md`、`references/executor-base.md`、`references/executor-chart.md`、`references/native-data-interface.md`。路线固定为 **Generate PPTX → Quick，自由设计（flat）**，不问用户。

### 1. 读参考稿库

读 `<参考稿库>/catalog.md` 全文和 `start-check.txt`。只在需要时看 `contact/` 缩略总览和 `renders/slide-NN.png`（1600 px，不要缩小）。

### 2. 规划全稿（主代理一次做完，写进 `plan.md`）

**选蓝图**：对大纲每一页：
1. 判断它的主逻辑（一页只取一个）：两方对比、多方 × 多维对比、转化漏斗、循环 / 闭环、线性流程、阶段演进、里程碑 / 时间线、层级依赖、中心辐射、价值分布、三要素构成、数据面板、多项并列。
2. 按 `catalog.md` 第一节这一逻辑的候选页顺序，逐个核对：模块数在可增删范围内、字数在范围内、"含义提醒"不冲突。第一个全部满足的就用；同类都不满足，退到"数据面板"或"多项并列"，并写明原因。**不许选目录"不推荐"里的页，不许为了好看硬套含义冲突的版式。**
3. 一份稿子里同一页最多用一次；相邻两页不用同一种主图示。

`plan.md` 写四部分：
- **规划表**，每页一行：页名 | 主逻辑 | 蓝图页 | 主图示怎么对应内容（一句话） | 模块增删（删哪些 id、复制几份） | 大纲条目 → 模块的对应 | 图表（类型和数据）。
- **全稿约定**：页头右侧标签、页脚来源与机构写法、图标库（只用一个，页头手形图标用 `pointer`）、蓝红含义、正文和说明字号下限。
- **分工**：按第 4 步的分段规则写出每段的页。
- **推算值**：大纲里没有、需要计算才能画的数（如按比例算的条长），写明算式。

### 3. 建项目并起页（主代理）

按 quick-generate.md：`project_manager.py init <名称> --format ppt169 --dir <运行目录> --quick-generate`，`import-sources <项目> <大纲> --copy`，`text_measure.py calibrate`，`icon_sync.py` 一次同步 plan.md 里用到的全部图标。然后给每一页起页：

```
python scripts/start_page.py <参考稿库>/import/authoring-svg-flat/slide_NN.svg <项目>/svg_output/NN_页名.svg
```

起页会删掉图片和图片裁剪框、指向被删图片的连接线绑定、自定义几何的源信息、导入插画，把组上的阴影移到形状上，描边渐变改成首色，参考稿字体统一成 OPPOSans，其余全部保留，并在页面里记下蓝图来源。

### 4. 分段并行改页（fork）

**分段规则**：写页量 W = 页数（数据多或特别密的页算 1.5）。W ≤ 4：主代理全写，不开子代理。否则段数 = min(⌈W ÷ 2⌉, 5)，每段约 2 页，重页分到不同段；同时在写的代理最多 5 个（主代理 + 4 个 fork），段多于 5 时，每收到一个 fork 完成通知就开下一段。

**开法**：第 3 步做完后，**在同一条消息里**用 Agent 工具为段 2 起的每一段开一个 `subagent_type: "fork"` 的子代理，prompt 用 `references/fork-brief.md`，只替换尖括号里的值。fork 继承主代理到此为止读过的文档、目录、大纲和 plan.md 的思考过程，不用重读、不用重新理解大纲。然后主代理立即写段 1，不等 fork。会话里没有 fork 类型时，按 fork-brief.md 末尾的说明退回普通子代理。（ppt-master `executor-base.md` 要求只由主代理写页，理由是各页共享上游上下文；fork 继承同一份上下文，满足这一本意。用户同意用 fork 并行。）

**每页的改法**（主代理和 fork 相同）：
1. `python scripts/edit_page.py list <页>` 看模块 id 和文字。
2. 用 `edit_page.py batch <页> "命令 ; 命令 ; …"` 一次做完这一页的修改，按这个顺序：
   - **删**：参考稿的模块里大纲用不上的、参考稿内容（品牌名、产品名、案例文字、"@职场的IDEAPOINT"等水印）整块删除。
   - **数量**：大纲条目比蓝图多，`clone` 同类模块并按蓝图间距平移；编号圆、底色等同一行的部件要一起复制或平移。
   - **文字**：`text <id> 新文字` 在原文本元素里换成大纲原文，保留位置、字体、字号、颜色和对齐；`\n` 换行。放不下时先换行，再微调这个文本框，不整块重排。
   - **颜色**：沿用蓝图配色，只在含义需要时用 `color` 对调。
   - 最后一条命令固定是 `sweep`（删除部件后，清掉没有几何的形状和空组，否则导出会失败）。
3. **图片位**：被删图片留下的位置，用图标库图标、数字或简单形状补上，或让相邻模块占用；页头手形图标用 `pointer` 放在原位置。**蓝图里用图片做的图表**（起页后整块消失）：在原位置按大纲数据画原生图表。
4. **图表**：蓝图里的原生图表保留位置和样式，换成大纲数据；形状画的图表按数据重算尺寸。按 verify-charts 核对。
5. 单页检查：`python <PM>/scripts/svg_quality_checker.py <项目> --quick-generate --canonical-authoring --stage page --page <页文件名>`，有阻断就集中修一轮；`python scripts/check_reuse.py <项目>/svg_output <参考稿库>/import/authoring-svg-flat` 看这一页还剩多少来自蓝图。低于 50% 说明已经在重画：重新起页；确实需要大改的，写明原因。
6. **不要新建空白 SVG 自己构图。** 需要新增的小构件（图表、图标、补位形状）可以手写，但整页的骨架必须来自蓝图。

**SVG 写法上踩过的坑**：阴影 `filter` 加在具体形状上，不加在 `<g>` 上；角色图元要有 `id`；折线不要用 `marker-end`；图表 JSON 里不能出现裸 `<`；用 OPPOSans B / H 的文字同时写 `font-weight="bold"`；续行 `tspan` 重复父元素的 `x`；模块边界不要互相压线；少数蓝图页起页后仍有检查错误（见 `start-check.txt`），改这一页时一并处理。

### 5. 收口检查（主代理，所有段完成后）

逐条核对 plan.md 的全稿约定，在 plan.md 写"核对"一段。然后 `stamp_native_fallbacks.py <项目>/svg_output --write`，`svg_quality_checker.py <项目> --quick-generate --canonical-authoring --stage final --json`，必须 0 阻断。

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

先看全部页，把溢出、压字、裁切、低对比、参考稿残留一次列全，**集中修一轮**，再走第 5、6 步和渲染复查。要修的页多于 3 页时，可以按第 4 步的方式开 fork 分页修。页面能不能当基线由用户决定。

## 中文字体

ppt-master 的导出器只认一张固定的中文字体名单，OPPOSans 不在里面，所以中文会被写成微软雅黑。`export.py` 做两层修复，都不改 ppt-master 的文件：

- **A（主）**：在同一个进程里把 OPPOSans 各字重加进导出器的中文字体名单，再调用 ppt-master 自己的导出入口。
- **B（兜底）**：导出后运行 `scripts/fix_cjk_fonts.py`。英文是 OPPOSans 而中文是雅黑或主题引用时，中文改成同一字重的 OPPOSans；英文跟随主题而中文写死雅黑时，中文也改为跟随主题；主题里中文字体跟随同一块的英文字体。其他字体一律不动。A 生效时它改 0 处。也可单独用：`python scripts/fix_cjk_fonts.py deck.pptx [-o out.pptx]`。

## 运行日志

在运行目录写 `run-log.md`：开头是计时表（步骤、开始、结束、用时、工具调用次数，第 4 步拆到每一段和每一页），然后是 plan.md 的规划表、`check_reuse.py` 结果、检查和导出结果、修改轮次、剩余问题（如实写）。
