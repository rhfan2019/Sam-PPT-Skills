# 版式目录

每个版式的完整字段写法见 `examples/nev-report.json` 中同名 `layout` 的那一页。下面给出适用场景、关键字段和**容量上限**（超出就拆页或精简）。

所有页通用：`layout`、`title`、`section`、`speaker_notes`。文字中 `**x**` 为重点。字号已固定，不要靠缩小字号塞内容。

## 一、咨询版式（模板第 10 页结构：论点条 → 区块标签 → 主图两翼 → 证据 → 框架条）

> **状态：已经用户确认（approved）。** 第一批 chart_phases / funnel / hub，第二批 dual_charts / versus / matrix（2026-10-21），这 6 种是目前达到预期效果的版式。

信息密度最高、最有"咨询感"，**优先使用**。共有字段：
- `thesis`：全宽深蓝论点条，一句话说清这页的 so-what（≤ 40 字）
- `zones`：两个区块标签 `[左, 右]`（各 ≤ 8 字）
- `strip`：底部框架条 `{left, left_boxes[[a,b],[a,b]], right, right_boxes, mid[上,下], left_icon, right_icon}`，每格两行、每行 ≤ 6 字

### chart_phases — 时间序列分阶段
柱（销量）+ 线（渗透率等百分比，浮在柱上方）+ 阶段底色带；右侧阶段诊断链 + 3 个指标框。
- `categories` ≤ 8；`bars{name, values}`；`line{name, values, ref?, ref_label?, format?}`
- `phases` 2–3 段：`{from, to, name, years, tag, tone, icon, points[≤2 条，每条 ≤ 22 字]}`
- `callout{at, text}`：指向某个数据点；`growth: "auto"` 自动算同比胶囊（≥50% 标红，`growth_hot` 可改）
- `kpis` ≤ 3：`{value, unit, label(≤ 10 字), up}` —— 放本页没出现过的推算数字

### funnel — 转化漏斗
立体切面漏斗 + 左翼阶段定义 + 右翼转化诊断（转化率、流失自动算，最弱一环自动标红）+ 指标框 + 剩余人数小图。
- `stages` 4–5：`{name, value(占起点 %), desc(≤ 16 字), icon, short?}`
- `transition_notes`：与转化环节一一对应（≤ 14 字）
- `kpis` ≤ 3，`mini_chart{title, label}`，`axis_label`，`start_note[2 行]`

### hub — 中心辐射
中心节点 + 2–6 个卫星（左右各半）；卫星说明做成无卡片条目，用圆点虚线连到节点；两翼下方各一个证据模块。
- `center[主, 副]`，`background`（图片键，可选），`hero_photo`（默认 car3d）
- `nodes` 2–6：`{name(≤ 8 字), metric(≤ 5 字), group(标签 ≤ 4 字), desc(≤ 14 字), icon, tone}`
- `evidence_left / evidence_right`：`{type: split_bar|bars|kpis, title, ...}`

### dual_charts — 三栏：年度结构 | 月度走势 | 增长拆解（咨询构图，**已确认**）
栏宽按内容自动分配（每个类目所需宽度 + 末端标注列；证据栏固定 2.9″，可用 `widths[3]` 覆盖），栏间 0.4″ 留白 + 细竖线，区块标签与栏同宽。左：堆积柱 + 段间虚线 + 最新年份浅红底带 + 末端直接标注 + 份额胶囊行；中：堆积面积（白色接缝）+ 末月虚线 + 末端标注与增幅胶囊；右：3 个指标框 + 增量拆分条。三栏底部各有一行微型说明，共用同一条基线。
- `zones[左, 中, 右]`；`left / right`：`{title, type: stacked_column|stacked_area, categories(左 ≤ 6，右 ≤ 9), series{名: 值[]}(≤ 3 个系列), callout{at, text(≤ 10 字)}, caption(≤ 24 字)}`
- `left.pill_row{label(≤ 4 字), values, suffix, hot}`；`right.end_tags[每个系列一个 ≤ 5 字]`
- `evidence{kpi_title, kpis ≤ 3 {value, unit, label(≤ 14 字), tone}, split{title, parts[2]{label, value(%), note}, caption}, caption}`

### versus — 三栏行对齐：左翼 | 指标对决 | 右翼（咨询构图，**已确认**）
VS 徽章压在区块标签行；表头：图标圆 + 路线名 + "N 项占优"胶囊，下接各自颜色的粗线；三栏之间用细竖线分隔（与 dual_charts 一致），行间用浅灰虚线，不加底色；每行左右两翼的优势/劣势条目与中间的指标对齐（条目 `ref` = 指标行号，无 `ref` 的条目放进空行）；占优一方实色渐变 + 粗体数值；底部框架条。
- `zones[左, 右]`（默认取 `claim`），`sides` 2：`{name(≤ 14 字符), tone, icon, pros[≤ 2], cons[≤ 2]}`；条目为字符串或 `{text(≤ 14 字), ref}`
- `metrics{title, left, right, rows ≤ 5 {label(≤ 10 字), a, b, better: low|high}}`（占优项数自动算）
- `strip`：同咨询版式；格子第二行留空 `["有家充", ""]` 时显示为单行大字

### matrix — 开放式 2×2 矩阵 + 证据翼（咨询构图，**已确认**）
矩阵去卡片：浅色象限 + 编号图标圆 + 标题 + 标签 + 说明；`band` 行用红色虚线框圈出并挂胶囊；右翼：大数字 + 拆分条（圆点虚线连到 band）+ 两个证据小条形图；出处写在各模块下方的微型说明里。
- `zones[左, 右]`，`axes{x, y, ends?[低, 高]}`（轴名不要带箭头，两端自动标"低 / 高"）
- `quads[4]{title(≤ 6 字), label(≤ 9 字), desc(≤ 14 字), tone, icon}`（顺序：左上、右上、左下、右下）
- `band{row, label(≤ 6 字)}`，`hero{value, unit, icon, title, sub}`，`split{title?, parts[2]{label, value, tone, show_value, note}, caption}`
- `evidence` ≤ 2：`{title, tone, label_w?, unit?, caption, rows ≤ 3 {label, value, tone: navy|red|mid}}`（可放跨页引用，caption 注明出处）

## 二、卡片与图表版式

> **状态：未达预期（provisional）。** 以下 14 种是精修卡片风格，能用但用户反馈效果不够，待逐个升级为咨询构图（见 HANDOVER.md 第 7 节）。不要把它们当作风格标准参考。

### cover — 封面
`label, title_lines[2 行，每行 ≤ 10 字], subtitle, chips[≤3]{text, icon, tone}, byline, note, hero{main[值,说明], red[值,单位,说明], white[值,说明]}, photo, background`

### contents — 目录
`panel{kicker, claim[2 行], text}`，`chapters` ≤ 6：`{title, sub, pages, kpi, kpi_label}`

### kpi_rings — 3–4 个环形 KPI
`rings[{label(≤ 12 字), value(%), tone, icon, note(≤ 14 字), compare[[标签,值],[标签,值]]}]`，`summary`（≤ 70 字，可用 `**`）

### dashboard — 看板
`kpis` 4：`{label, value, unit, growth, tone, icon, share(0–1), caption}`；`panels` 3：`{type: donut|bar|area, title, categories, values, center?, highlight?, callout?, note}`

### spec_table — 参数表 + 焦点列
`columns`（≤ 4 列），`rows`（≤ 7 行，单元格 ≤ 16 字），`row_icons`，`focus_col`，`focus_label`，`highlight_cells[[行,列]]`，`hero{icon, kicker, title, sub}`，`mini_bars{title, names, groups[2]{label, values[3]}}`，`finding{title, metric, points[2]}`

### radar — 雷达评分
`dims`（5–8），`series{名: 分值[]}`（2–4 个），`max`（默认 10），`chart_title`，`findings[3]{title, tone?, points[2]}`。各维度领先者、均分、"最均衡"自动算。

### butterfly — 两组人群对称条形
`left / right{name, icon, values[]}`，`factors`（≤ 8），`chart_title`，`diff_hot`（差值标红阈值，默认 15），`findings[3]`

### persona — 人物画像
`name, tagline, tags[4], quote(≤ 26 字), photo, avatar_icon, attrs[4]{icon, label, value}, needs[4]{icon, text(≤ 14 字), tag}, index{title, categories(≤6), values, baseline, note}`

### bubble — 气泡分布
`axes{x, y, xmax, ymax, xstep?, ystep?}`，`zones[{from, to, label, tone}]`，`series{名: [{label, x, y, size, pos: right|left|above|below}]}`（≤ 12 点），`callout{series, point, text}`，`findings[3]`

### smile_curve — 价值链曲线
`links`（5–8），`values`，`notes`（每条 ≤ 9 字），`icons`，`highlight[索引]`，`zones[{from, to, label, tone}]`，`callout{at, text}`，`axis_note`

### pyramid — 金字塔
`layers` 3–6（自上而下）：`{name(≤ 6 字), desc(≤ 20 字), icon}`；`axis`（左侧箭头文字），`crown`

### timeline — 时间轴
`eras[{label, sub, until}]`（≤ 2 段，`until` = 第一段结束于第几个事件），`events` ≤ 7：`{year, text[≤3 行，每行 ≤ 10 字], icon, mark: focus|forecast}`，`summary`，`photo`

### company_cards — 主体卡片
`companies` ≤ 6：`{name, route, value, unit, value_note, icon, points[≤3]}`，`bench_name, bench_text`，`summary`

### strategy_house — 战略屋
`roof{kicker, title, kpis[[值, 说明], [值, 说明]]}`，`pillars` 3–5：`{name, points[≤3], icon, tag}`，`foundation`，`photo`

## 素材键

- 图标（可任意着色）：battery, home, growth, coin, ai, city, globe, storm, family, man, target, check, box, cycle, trend, improve, cart, warn, cube, crown, star, chat, computer, tag, group, women, kid
- 图片：car3d（白色 3D 小车，透明底）、sedan（轿车抠图，透明底）、dealer（门店洽谈）、city_sun、city_dusk、city_tech（科技城市，透明底）、tower
