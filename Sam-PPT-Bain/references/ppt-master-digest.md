# ppt-master 速查（Sam-PPT-Bain 用到的部分）

> 依据 ppt-master **6.7.2** 的 Quick Generate 执行文档整理：`workflows/profiles/quick-generate.md`、`references/shared-standards-core.md`、`executor-base.md`、`executor-structured.md`、`pptx-structure-interface.md`、`semantic-svg.md`、`native-shape-authoring.md`、`executor-chart.md`、`workflows/stages/verify-charts.md`、`scripts/docs/svg-contract.md` §1.1。
> 只收录本 Skill 每次运行实际要遵守的条款；插件本身不改。`sam_bain.py new` 检测到插件版本不是 6.7.2 时会提示：那一次运行改读原文档，并更新本文件。
> 本文件替代"每次通读执行核心"这一步。遇到这里没写到的能力（图片页、原生图表 / 表格、公式、超链接、动画、讲稿）时，仍按原文档的路由表去读对应模块。

## 一、流程（Quick Generate 在本 Skill 里的形态）

1. `new`：已经跑过 attribution_guard、项目初始化、模板安装、导入大纲、字号校准。**不建** `design_spec.md` / `spec_lock.md`，不走确认环节。
2. 写页前在脑子里定好这些，不落成文件：逐页的核心信息、关系（顺序 / 连接 / 从属 / 成员 / 对比 / 交叠）、页型、字号和颜色角色。图标集中一次用 `sam_bain.py icons` 同步；一套 deck 只用一个风格库（默认 `chunk-filled`），文件名要先在 `templates/icons/chunk-filled/` 里查到。
3. 按顺序逐页**手写** SVG。不能交给子代理写，也不能用生成器写正文（`scaffold` 只写模板里的固定页框，正文仍由主 agent 手写）。
4. ≥ 7 页时，写完 P05 跑一次 `check --early`；每次检查之间只做一轮集中修复，不要改一处查一次。
5. 有按数值画的图（柱、点、气泡、折线等），并且被"提升"为核验对象时：带 plot-area 标记，最终检查前用 `svg_position_calculator.py calc …` 核对坐标（见第六节）。
6. `finish`：final 检查 → 导出（`--quick-generate --no-notes`）→ 修复 OPPOSans 中文字体 → PowerPoint 渲染。不跑 `finalize_svg.py`。

## 二、结构化页面（本模板是 Deck 结构）

- 每页根 `<svg>` 都要带四个属性：`data-pptx-master="sam_bain_master"`、`data-pptx-master-name="Sam Bain"`、`data-pptx-layout`、`data-pptx-layout-name`，取值和所用原型一致（`content_frame` / `content_thesis` / ……）。**不写** `data-pptx-page-role`。
- 页框原子（背景、手势标记、标题线、页脚线、论点条底）和 slot 组原样保留在最前面，不改 id、坐标和 `data-pptx-*` 属性。slot 里只替换文字。
- 每个 slot 只能有一个 `data-pptx-carrier="true"` 子元素。不要往 slot 里加别的东西，正文一律写成 slot 之后的 Slide-local 组。
- 根 `<svg>` 上写 `lang="zh-CN"`，并给出公共 `font-family`（`OPPOSans R, Microsoft YaHei, sans-serif`）。
- `scaffold` 输出的就是这个骨架，外加一组常用 defs（见第五节）。

## 三、分组与 bounds（检查器最常报错的地方）

- 正文里每个逻辑单元是一个根层 `<g id="…">`，id 在页内唯一、有描述性，并写 `data-pptx-bounds="x y w h"`。
- **根层组之间重叠不能超过 1 px**（slot 组和 `data-pptx-role="decoration"` 除外）。跨几个组的底色面板写成根层 `<rect id=… data-pptx-role="decoration">`，不包 `<g>`。
- bounds 是模块区，不是字形外框：要包住所有子元素。文字的纵向范围按 `基线 − 0.85×字号` 到 `基线 + 0.35×字号` 估算。文字超出 bounds 5% 以内只是警告，超过 5% 就是错误。
- 主图和贴着它的标注放在同一个组里，不要拆成两个会互相重叠的组。
- 不要用一个大 `<g>` 包住整页；也不要一行文字、一个图标各占一个根层组。
- 嵌套组不需要 bounds。

## 四、文字

- 一个段落写成一个 `<text>`，换行用带 `x`（重复父级 x）和正 `dy` 的 `<tspan>`；同一段落的各行不要写成并列的多个 `<text>`。
- 行内强调用不带位置的 `<tspan>`，可以单独设 `fill` / `font-weight` / `font-size`；`font-family` 写在 `<text>` 或 `<g>` 上，**不写在 `<tspan>` 上**（本 Skill 约定）。
- 字号单位是 px，最多两位小数。行距：密集正文约 1.4–1.5 倍，标题约 1.2–1.3 倍。
- XML 字符：`&` 写成 `&amp;`；`—` `→` `·` `“”` 直接写 Unicode，**不用** `&mdash;` 这类 HTML 实体。
- 宽度用 `new` 输出的校准表估算：中文字数 ÷ 每 100 px 字数 × 100，中英混排两部分相加，留 5% 余量。数字按 DIGITS 列、大写字母按 CAPS 列。

## 五、形状、线条、效果

- **禁用**：`mask`、`<style>`、`class`、`foreignObject`、`textPath`、`@font-face`、动画、脚本。
- 颜色写大写 `#RRGGBB`，或 `none`、`url(#id)`；透明度用 `fill-opacity` / `stroke-opacity`。
- 渐变：双色 `linearGradient` 可以直接用。`filter` 只能挂在单个 `rect` / `circle` / `path` / `text` 上，**不能挂在 `<g>` 上**。阴影要淡，`flood-opacity` 取 0.06–0.20，每页最多 2–3 个浮起物体。
- **箭头标记**：`marker-start` / `marker-end` 只写在 `<line>` / `<path>` 上。marker 里只放一个三顶点 `<polygon>`，`orient="auto"`，**填色必须和这条线的 stroke 一致**，不一致检查器直接报错。所以每种线色配一个 marker：`scaffold` 自带 `arrNavy` #1C4274、`arrRed` #A23424、`arrGray` #8EA9CF、`arrPink` #E3A79C、`arrWhite`；换线色就新增一个 marker。线宽超过 4 px 不挂 marker，改用单独的三角形。
- **预设形状**：除矩形、圆角矩形、圆、椭圆、直线之外的轮廓（箭形色带 `homePlate` / `chevron`、块箭头、梯形、标注气泡、`mathPlus` / `mathEqual` 等运算符），一律用 `preset_shape_svg.py render-batch --input -` 生成（同一页的全部预设一次批量生成），输出原样粘贴，**不手改 path 和 frame**。预设组可以放进带 bounds 的父组里，文字写在预设组外面。改尺寸就重新生成。整体平移、旋转、翻转可以写在外层 `<g transform>` 上。
- 预设只接受纯色填充；要渐变就用普通 SVG 图元。
- 用 `shape_boolean_svg.py` 做合并、相减、交集。手写 `<path>` / `<polygon>` 是最后一级手段，按数值画的折线（`polyline`）不在此列。
- 图标写成 `<use data-icon="chunk-filled/名称" x y width height fill="#HEX"/>`，图标必须已经同步到项目的 `icons/` 里。

## 六、图表（按数值画的几何）

- 柱、点、气泡的位置都按一把明确的比例尺从原值算出来，不靠目测。
- 要核验的图表包成 `<g id="key">` → `<g id="key-chartArea">`，在坐标轴之后、第一个数据标记之前写一行：`<!-- chart-plot-area: object=key | x_min,y_min,x_max,y_max -->`。
- 核验命令：`svg_position_calculator.py calc line --data "x:y,…" --area "x_min,y_min,x_max,y_max" --x-range=0,100 --y-range=0,100`（气泡图、散点图、折线图）；柱图用 `calc bar --value-range=0,max`。比例尺对上了、坐标对不上，才手工改 SVG。
- 小图、迷你走势图属于"附带微图"，可以不提升为核验对象，但仍要按数值精确绘制。

## 七、检查与导出

- 检查命令：`svg_quality_checker.py <project> --quick-generate --canonical-authoring --stage early|final --json`（`sam_bain.py check` 已封装）。
- 必须修的：所有 `[ERROR]`。可以不改的：OPPOSans "non-PPT-safe typeface" 字体提示（导出后由 `fix_cjk_fonts.py` 修复），以及 "Noncanonical compact authoring" 这类样式写法建议。
- 导出要求 final 报告的指纹和当前 `svg_output/` 一致，所以改了 SVG 就要重跑 `finish`，不要只重跑导出。
- 交付前把 `[CARRIERS]` 回执和每页的构造对照一遍：大量"关系"页却没有用到预设箭头或连线，说明构造偏弱。
