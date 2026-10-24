# 构件库（核心库：K01–K19）

从用户提供的参考材料里抽出的 19 个构件，只保留形状、比例、配色和效果参数，文字一律是占位词。K01–K06 是 2026-10-23 首批手量的构件；K07–K19 是同日按参考材料里的出现频率挖出、经用户同意取舍后手工整理的构件，参数（阴影、描边透明度、虚线、比例）照原件。渲染效果（PowerPoint 导出后渲染）：

| 图 | 构件 |
|---|---|
| `kit-a.png` | K01–K04、K06 |
| `kit-b.png` | K05 |
| `kit-c.png` | K07–K10 |
| `kit-d.png` | K11–K15 |
| `kit-e.png` | K16–K19 |

**动笔前先看这五张图。** 核心库没有合适的写法时，再查备用库 `archive/index.md`（不必每次读）。

这些构件是本 Skill 风格的"手艺"部分：它们的造型、比例和渐变参数已经调好，**直接复制下面的写法，只改坐标、尺寸和文字**，不要重新发明造型，也不要改配色和效果参数。

## 用法约定：构件可复用，构图要变化

- **每页至少用 2 种构件**（数据页也一样）。图表、表格放进 K01、K06、K07 或 K08 划出的大区里，关键数字用 K02、K05、K09 或 K16 托出来。
- **按内容挑，不为凑数用**：先按本页内容的关系查文末的选择表，只用表里对得上的构件；同一页不要把准星节点、括号、光柱、指向块之类的点缀构件都摆一遍。
- 同一构件可以在多页、同一页里多次使用；变化的是**整页构图**：构件的组合、位置、大小和数量随本页内容变化。相邻两页不要用同样的构件组合摆同样的位置；连续三页不要用同一种分区方式（全用页签面板或全用侧标签条）。
- 构件只承载大纲里的真实内容。没有对应内容就不放（例如没有阶段关系就不用人字箭头，没有单一主角数字就不用光晕底板）。
- 颜色只用蓝、红两个版本：左 / 用户侧 / 现状用蓝，右 / 策略侧 / 判断用红（rules 二.6）。
- 渐变和阴影的 id（`gNavyV`、`gFadeRedUp`、`gBoardRed`、`tileShadow`、`softShadow`、`nodeShadow`、`glowRed`、`glowNavy`、`gColumnTop`、`gColumnBody`、`gBeamUp` 等）已由 `scaffold` 写进页面 `<defs>`，正文里直接引用。`nodeShadow`（右下 45°、模糊 5.3、黑 40%）是参考材料里最常用的阴影，只给小圆节点、编号圆这类小物件用；大面积的浮起卡片仍用 `softShadow` / `tileShadow`。
- K07–K19 的写法用的是 `kit-c/d/e.png` 里的示例坐标：复制后用外层 `<g transform="translate(dx,dy)">` 整组平移，或按比例改坐标；`<!--P-->` 标记里的 id 每次改成本页唯一的名字。
- 预设形状写成 `<!--P …-->` 标记（SKILL.md 第 5 步）；整组可以用外层 `<g transform="translate(dx,dy)">` 平移。

## K01 · 页签 + 浅底面板

**用于**：并列的 2–6 个对象各占一栏（对象名做页签，指标和结论放面板里）；也可以放大成一个大区，给图表或表格做外框（页签写区块名）。
**比例**：页签高 47（下沿是波浪），面板与页签同宽；栏宽 120–260；栏间距 12。面板底部可放一个白底结论小框（76×70 起，带极淡阴影）。

```xml
<g id="tab-a" data-pptx-bounds="auto">
  <rect x="X" y="Y" width="160" height="216" fill="#F2F6FC"/>                 <!-- 红版 #FDF5F4 -->
  <!--P flowChartDocument tabA X Y 160 47 #1C4274 -->                         <!-- 红版 #A23424 -->
  <text x="X+80" y="Y+29" text-anchor="middle" font-family="OPPOSans M, Microsoft YaHei, sans-serif" font-size="18.67" fill="#FFFFFF">页签标题</text>
  <g font-family="OPPOSans R, Microsoft YaHei, sans-serif" text-anchor="middle">
    <text x="X+80" y="Y+76" font-size="13.33" fill="#404040">指标甲 <tspan fill="#A23424">38%</tspan></text>
    <text x="X+80" y="Y+100" font-size="12" fill="#595959">指标乙 22%</text>
  </g>
  <rect x="X+42" y="Y+132" width="76" height="70" fill="#FFFFFF" stroke="#C4D7F1" stroke-width="0.5" filter="url(#tileShadow)"/>  <!-- 红版描边 #F4D1CC -->
  <text x="X+80" y="Y+162" text-anchor="middle" font-family="OPPOSans M, Microsoft YaHei, sans-serif" font-size="17.33" fill="#1C4274">关键<tspan x="X+80" dy="22">词语</tspan></text>
</g>
```

## K02 · 图标指标块

**用于**：3–6 个并列指标（倍数、份额、规模），每条一行；数值的相对大小用短进度条表达。整组外面套一个海军蓝虚线框。
**比例**：每行 388×76（可按栏宽伸缩，行高不小于 64），行距 12；图标圆 r 31 距左 40；标签 18.67 M；数值 24 R 在进度条正上方；进度条高 19、白底轨道 + 实色填充，填充宽 = 轨道宽 × 数值 / 本组最大值。

```xml
<g id="kpi-a" data-pptx-bounds="auto">
  <rect x="X-16" y="Y-12" width="420" height="190" fill="none" stroke="#1C4274" stroke-width="1.33" stroke-dasharray="6,4"/>
  <rect x="X" y="Y" width="388" height="76" fill="#DAE6F6" stroke="#FFFFFF" stroke-width="1"/>   <!-- 红版 #F8E2DF -->
  <circle cx="X+40" cy="Y+38" r="31" fill="url(#gNavyV)"/>                                        <!-- 红版 url(#gRedV) -->
  <use data-icon="chunk-filled/users" x="X+24" y="Y+22" width="32" height="32" fill="#FFFFFF"/>
  <text x="X+84" y="Y+45" font-family="OPPOSans M, Microsoft YaHei, sans-serif" font-size="18.67" fill="#1C4274">指标名称</text>
  <text x="X+188" y="Y+30" font-family="OPPOSans R, Microsoft YaHei, sans-serif" font-size="24" fill="#1C4274">1.50X</text>
  <rect x="X+188" y="Y+42" width="188" height="19" fill="#FFFFFF"/>
  <rect x="X+188" y="Y+42" width="94" height="19" fill="#1C4274"/>
  <!-- 下一行 Y+88，同样写法 -->
</g>
```

## K03 · 人字箭头色带 + 阶段卡

**用于**：3–6 个依次推进的阶段（时间段、步骤、S→C→Q→A 这类推进链）。色带写阶段名，下面每段挂一张同宽的浅色卡片放该阶段内容；色带上方可加一条细箭头线和一句"由 A 转向 B"。
**比例**：人字箭头高 39，宽 = 卡片宽 + 20，步距 = 卡片宽 + 9（相邻箭头相互咬合）；颜色蓝红交替或只把重点阶段做红；卡片描边用 0.67 px、51% 不透明度的同色。

```xml
<g id="chev-a" data-pptx-bounds="auto">
  <line x1="X" y1="Y-10" x2="X+786" y2="Y-10" stroke="#1C4274" stroke-width="1" marker-end="url(#arrNavy)"/>
  <text x="X+393" y="Y-17" text-anchor="middle" font-family="OPPOSans R, Microsoft YaHei, sans-serif" font-size="13.33" fill="#404040">由 A 转向 B</text>
  <!--P chevron chv1 X Y 275 39 #1C4274 -->
  <!--P chevron chv2 X+264.2 Y 275 39 #A23424 -->
  <!--P chevron chv3 X+528.4 Y 275 39 #1C4274 -->
  <g font-family="OPPOSans R, Microsoft YaHei, sans-serif" font-size="20" fill="#FFFFFF" text-anchor="middle">
    <text x="X+132" y="Y+26">第一阶段</text><text x="X+401" y="Y+26">第二阶段</text><text x="X+665" y="Y+26">第三阶段</text>
  </g>
  <rect x="X" y="Y+45" width="255" height="150" fill="#F7F9FD" stroke="#1C4274" stroke-opacity="0.51" stroke-width="0.67"/>
  <rect x="X+264.2" y="Y+45" width="255" height="150" fill="#FDF9F8" stroke="#A23424" stroke-opacity="0.51" stroke-width="0.67"/>
  <rect x="X+528.4" y="Y+45" width="255" height="150" fill="#F7F9FD" stroke="#1C4274" stroke-opacity="0.51" stroke-width="0.67"/>
</g>
```

## K04 · 立体标签

**用于**：一列 2–4 个并列类别名（流程每一层的名称、象限或分组的名称），放在一列内容的最左端或节点上，代替平面胶囊。标签上方可写一行说明（20 M，同色）。
**比例**：137×49（可在 110–170 宽之间伸缩，高宽比保持约 1:2.8）；文字 20 B 白色，居中于正面（x 中心 = X + 宽 × 0.45，基线 = Y + 33）。PowerPoint 会自动把顶面画浅、侧面画深。

```xml
<g id="cube-a" data-pptx-bounds="auto">
  <text x="X" y="Y-12" font-family="OPPOSans M, Microsoft YaHei, sans-serif" font-size="20" fill="#1C4274">标签上方说明</text>
  <!--P cube cubeA X Y 137 49 #1C4274 -->                                     <!-- 红版 #A23424 -->
  <text x="X+62" y="Y+33" text-anchor="middle" font-family="OPPOSans B, Microsoft YaHei, sans-serif" font-size="20" fill="#FFFFFF">类别</text>
</g>
```

## K05 · 透视光晕底板 + 英雄数字

**用于**：一页只有一个最重要的数字（规模、目标、占比）时，用它托起这个数字，作为全页焦点。每页最多一个。
**构成**：上方一块倒梯形看板（白 → 浅色渐变、带阴影），下方一块向上渐隐的浅色梯形地台和一圈细线外框，两侧可放半透明上箭头。看板下沿与地台上沿相距 8–15。
**比例**（看板宽 W，可在 340–800 之间）：看板高 ≈ W × 0.13–0.30，下沿两侧各内收 W × 0.08；地台宽 ≈ W × 1.2，高 ≈ 46，上沿两侧各内收地台宽 × 0.24；外框比地台宽 ≈ 25%。

```xml
<g id="plat-a" data-pptx-bounds="auto">
  <!-- 外框细线（红版；蓝版 stroke #1C4274） -->
  <path d="M 49 366 L 317 303 L 963 303 L 1231 366" fill="none" stroke="#A23424" stroke-opacity="0.55" stroke-width="1"/>
  <!-- 地台：向上渐隐（蓝版 url(#gFadeNavyUp)） -->
  <polygon points="161,350 387,304 893,304 1119,350" fill="url(#gFadeRedUp)"/>
  <!-- 看板：倒梯形圆角（蓝版 fill url(#gBoardNavy) stroke #C4D7F1） -->
  <path d="M 252 150 L 1029 150 Q 1036 150 1032 157 L 970 280 Q 966 288 954 288 L 327 288 Q 315 288 311 280 L 249 157 Q 245 150 252 150 Z" fill="url(#gBoardRed)" stroke="#F4D1CC" stroke-width="0.75" filter="url(#softShadow)"/>
  <!--P upArrow upL 120 245 60 90 #F4D1CC op=0.6 -->
  <!--P upArrow upR 1100 245 60 90 #F4D1CC op=0.6 -->
  <text x="640" y="190" text-anchor="middle" font-family="OPPOSans R, Microsoft YaHei, sans-serif" font-size="18.67" fill="#404040">指标说明文字</text>
  <text x="640" y="250" text-anchor="middle" font-family="OPPOSans B, Microsoft YaHei, sans-serif" font-size="48" fill="#1C4274">3,000<tspan font-size="24">亿</tspan></text>
</g>
```

小号版（看板宽 340，见 `kit-b.png` 下方）适合放在图表旁边或一栏顶部，托起本栏的结论数字。

## K06 · 竖排侧标签条

**用于**：把页面切成 2–3 个横向大区（上下排列），每个大区左侧一条贯穿全高的色条，竖排写区块名，右侧接同色系浅底面板，面板里放图表、流程或条目。代替横向栏头，让大区有"重量"。
**比例**：色条宽 42；竖排字 20 M 白色，每字一行（行距 24），整列在色条内垂直居中；面板浅底 `#F2F6FC`（红版 `#FDF5F4`）紧贴色条右侧，大区之间留 10–14。

```xml
<g id="side-a" data-pptx-bounds="auto">
  <rect x="X" y="Y" width="42" height="H" fill="#1C4274"/>                    <!-- 红版 #A23424 -->
  <text x="X+21" y="竖排起点" text-anchor="middle" font-family="OPPOSans M, Microsoft YaHei, sans-serif" font-size="20" fill="#FFFFFF">区<tspan x="X+21" dy="24">块</tspan><tspan x="X+21" dy="24">名</tspan><tspan x="X+21" dy="24">称</tspan></text>
  <rect x="X+42" y="Y" width="W-42" height="H" fill="#F2F6FC"/>              <!-- 红版 #FDF5F4 -->
  <!-- 面板内容写在这里或另起根层组 -->
</g>
```

竖排起点 = Y + H / 2 − (字数 − 1) × 12 + 7。

## K07 · 编号栏头 + 浅粉面板 + 证据框（红）

**用于**：一个重点大区：编号 + 区块名做栏头，面板里放要点，底部一排证据框托出本区的数字。参考材料里出现最多的构件（15 页）。蓝版见 K08。
**比例**：栏头宽约为面板的 40–45%、高 36，左缘与面板对齐、上沿高出面板 22；编号圆 r 16（白描边 2.67 + `nodeShadow`）圆心压在栏头左缘；面板 `#F4D1CC` 14% 填充 + 砖红 0.67 px 51% 描边；面板内用 0.67 px 砖红虚线（`3,2.25`）分出证据区；证据框白底、砖红 0.75 px 虚线，大数字 32 B + 单位 18.67，指标名 14.67，右侧 `upArrow`（约 30×52）。

```xml
<g id="k07" data-pptx-bounds="auto">
  <rect x="60" y="150" width="440" height="300" fill="#F4D1CC" fill-opacity="0.14" stroke="#A23424" stroke-width="0.67" stroke-opacity="0.51"/>
  <rect x="60" y="128" width="190" height="36" fill="#A23424"/>
  <text x="163" y="152" text-anchor="middle" font-family="OPPOSans M, Microsoft YaHei, sans-serif" font-size="18.67" fill="#FFFFFF">栏头标题</text>
  <circle cx="60" cy="146" r="16" fill="#A23424" stroke="#FFFFFF" stroke-width="2.67" filter="url(#nodeShadow)"/>
  <text x="60" y="151.5" text-anchor="middle" font-family="OPPOSans B, Microsoft YaHei, sans-serif" font-size="16" fill="#FFFFFF">1</text>
  <g font-family="OPPOSans R, Microsoft YaHei, sans-serif" font-size="14.67" fill="#262626">
    <text x="84" y="198">• 要点一占位文字，说明本栏的第一条内容</text>
    <text x="84" y="224">• 要点二占位文字</text>
    <text x="84" y="250">• 要点三占位文字，说明第三条</text>
    <text x="84" y="276">• 要点四占位文字</text>
  </g>
  <line x1="60" y1="318" x2="500" y2="318" stroke="#A23424" stroke-width="0.67" stroke-dasharray="3,2.25"/>
  <rect x="84" y="336" width="190" height="96" fill="#FFFFFF" stroke="#A23424" stroke-width="0.75" stroke-dasharray="3,2.25"/>
  <text x="104" y="384" font-family="OPPOSans B, Microsoft YaHei, sans-serif" font-size="32" fill="#A23424">38<tspan font-size="18.67">%</tspan></text>
  <text x="104" y="414" font-family="OPPOSans R, Microsoft YaHei, sans-serif" font-size="14.67" fill="#404040">指标名称</text>
  <!--P upArrow k07u1 226 358 30 52 #A23424 -->
  <rect x="290" y="336" width="190" height="96" fill="#FFFFFF" stroke="#A23424" stroke-width="0.75" stroke-dasharray="3,2.25"/>
  <text x="310" y="384" font-family="OPPOSans B, Microsoft YaHei, sans-serif" font-size="32" fill="#A23424">2.4<tspan font-size="18.67">倍</tspan></text>
  <text x="310" y="414" font-family="OPPOSans R, Microsoft YaHei, sans-serif" font-size="14.67" fill="#404040">指标名称</text>
  <!--P upArrow k07u2 432 358 30 52 #A23424 -->
</g>
```

## K08 · 深色栏头 + 浅蓝面板（蓝）

**用于**：并列的 2–4 个大区各占一栏，或一个大区里分几组小标题 + 要点。K07 的蓝色同族写法，栏头是平直矩形（K01 是波浪页签）。
**比例**：栏头高 36，与面板同宽，**和面板之间留 3 px 白缝**；面板 `#C4D7F1` 31% 填充 + `#0E213A` 0.67 px 51% 描边；面板内小标题 16 M 海军蓝 + 13.33 要点，组间距约 90。

```xml
<g id="k08" data-pptx-bounds="auto">
  <rect x="540" y="128" width="260" height="36" fill="#1C4274"/>
  <text x="670" y="152" text-anchor="middle" font-family="OPPOSans M, Microsoft YaHei, sans-serif" font-size="18.67" fill="#FFFFFF">栏头标题</text>
  <rect x="540" y="167" width="260" height="283" fill="#C4D7F1" fill-opacity="0.31" stroke="#0E213A" stroke-width="0.67" stroke-opacity="0.51"/>
  <g font-family="OPPOSans M, Microsoft YaHei, sans-serif" font-size="16" fill="#1C4274">
    <text x="560" y="202">小标题甲</text><text x="560" y="292">小标题乙</text><text x="560" y="382">小标题丙</text>
  </g>
  <g font-family="OPPOSans R, Microsoft YaHei, sans-serif" font-size="13.33" fill="#262626">
    <text x="560" y="226">• 要点占位文字，一行一条</text><text x="560" y="248">• 要点占位文字</text>
    <text x="560" y="316">• 要点占位文字，一行一条</text><text x="560" y="338">• 要点占位文字</text>
    <text x="560" y="406">• 要点占位文字，一行一条</text><text x="560" y="428">• 要点占位文字</text>
  </g>
</g>
```

## K09 · 虚线证据框

**用于**：1–3 个支撑结论的数字（增长、倍数、份额），放在图表旁或栏底。横版放 2 个数字 + 一支大箭头，竖版上面写说明、下面放数字。
**比例**：白底，0.75 px 虚线（`3,2.25`），蓝版海军蓝、红版砖红；大数字 32 B + 单位 18.67，指标名 14.67–16 R #404040；箭头用 `upArrow` 预设（横版约 36×64，竖版约 30×56），上升用 `upArrow`，下降用 `downArrow`。

```xml
<g id="k09a" data-pptx-bounds="auto">
  <rect x="840" y="128" width="400" height="100" fill="#FFFFFF" stroke="#1C4274" stroke-width="0.75" stroke-dasharray="3,2.25"/>
  <text x="860" y="178" font-family="OPPOSans B, Microsoft YaHei, sans-serif" font-size="32" fill="#1C4274">88.8<tspan font-size="18.67">倍</tspan></text>
  <text x="860" y="210" font-family="OPPOSans R, Microsoft YaHei, sans-serif" font-size="16" fill="#404040">指标名称</text>
  <text x="1010" y="178" font-family="OPPOSans B, Microsoft YaHei, sans-serif" font-size="32" fill="#1C4274">1,280<tspan font-size="18.67">万</tspan></text>
  <text x="1010" y="210" font-family="OPPOSans R, Microsoft YaHei, sans-serif" font-size="16" fill="#404040">指标名称</text>
  <!--P upArrow k09u1 1184 146 36 64 #1C4274 -->
</g>
<g id="k09b" data-pptx-bounds="auto">
  <rect x="840" y="250" width="180" height="200" fill="#FFFFFF" stroke="#A23424" stroke-width="0.75" stroke-dasharray="3,2.25"/>
  <g font-family="OPPOSans R, Microsoft YaHei, sans-serif" font-size="14.67" fill="#404040">
    <text x="858" y="282">说明占位文字</text><text x="858" y="304">第二行说明</text>
  </g>
  <text x="858" y="404" font-family="OPPOSans B, Microsoft YaHei, sans-serif" font-size="32" fill="#A23424">38<tspan font-size="18.67">%</tspan></text>
  <text x="858" y="434" font-family="OPPOSans R, Microsoft YaHei, sans-serif" font-size="14.67" fill="#404040">指标名称</text>
  <!--P upArrow k09u2 972 376 30 56 #A23424 -->
</g>
```

## K10 · 准星节点

**用于**：图上需要被点名的关键节点（关键阶段、关键对象、核心问题），一页 1–3 个。红版写两字关键词，蓝版放图标。
**比例**：白底圆 r 30–42，0.75 px 描边，挂 `glowRed` / `glowNavy`（同色柔光）；十字短线 1.33 px，从圆内约 4–7 px 伸到圆外约 16–21 px；红版只画左右两根，蓝版画四根。圆内字 14.67 M 两行，或 28×28 图标。

```xml
<g id="k10a" data-pptx-bounds="auto">
  <circle cx="1130" cy="300" r="30" fill="#FFFFFF" stroke="#A23424" stroke-width="0.75" filter="url(#glowRed)"/>
  <line x1="1084" y1="300" x2="1104" y2="300" stroke="#A23424" stroke-width="1.33"/>
  <line x1="1156" y1="300" x2="1176" y2="300" stroke="#A23424" stroke-width="1.33"/>
  <g font-family="OPPOSans M, Microsoft YaHei, sans-serif" font-size="14.67" fill="#262626" text-anchor="middle">
    <text x="1130" y="297">关键</text><text x="1130" y="315">节点</text>
  </g>
</g>
<g id="k10b" data-pptx-bounds="auto">
  <circle cx="1130" cy="400" r="36" fill="#FFFFFF" stroke="#1C4274" stroke-width="0.75" filter="url(#glowNavy)"/>
  <line x1="1073" y1="400" x2="1101" y2="400" stroke="#1C4274" stroke-width="1.33"/>
  <line x1="1159" y1="400" x2="1187" y2="400" stroke="#1C4274" stroke-width="1.33"/>
  <line x1="1130" y1="343" x2="1130" y2="371" stroke="#1C4274" stroke-width="1.33"/>
  <line x1="1130" y1="429" x2="1130" y2="457" stroke="#1C4274" stroke-width="1.33"/>
  <use data-icon="chunk-filled/target" x="1116" y="386" width="28" height="28" fill="#1C4274"/>
</g>
```

## K11 · 时间轴

**用于**：3–6 个时间点或阶段的通栏时间轴；页面底部收束，或做图表上方的时间刻度。
**比例**：2 px 海军蓝主线 + `arrNavy` 箭头，贴左右边界；节点白底小圆 r 6.2、0.75 px 描边 + `nodeShadow`，强调的节点描边改砖红；节点上方 16 M 年份，下方 13.33 说明。

```xml
<g id="k11" data-pptx-bounds="auto">
  <line x1="36" y1="150" x2="1240" y2="150" stroke="#1C4274" stroke-width="2" marker-end="url(#arrNavy)"/>
  <circle cx="200" cy="150" r="6.2" fill="#FFFFFF" stroke="#1C4274" stroke-width="0.75" filter="url(#nodeShadow)"/>
  <circle cx="520" cy="150" r="6.2" fill="#FFFFFF" stroke="#1C4274" stroke-width="0.75" filter="url(#nodeShadow)"/>
  <circle cx="840" cy="150" r="6.2" fill="#FFFFFF" stroke="#1C4274" stroke-width="0.75" filter="url(#nodeShadow)"/>
  <circle cx="1100" cy="150" r="6.2" fill="#FFFFFF" stroke="#A23424" stroke-width="0.75" filter="url(#nodeShadow)"/>
  <g font-family="OPPOSans M, Microsoft YaHei, sans-serif" font-size="16" fill="#1C4274" text-anchor="middle">
    <text x="200" y="132">2022</text><text x="520" y="132">2023</text><text x="840" y="132">2024</text>
    <text x="1100" y="132" fill="#A23424">2025</text>
  </g>
  <g font-family="OPPOSans R, Microsoft YaHei, sans-serif" font-size="13.33" fill="#404040" text-anchor="middle">
    <text x="200" y="180">阶段说明占位</text><text x="520" y="180">阶段说明占位</text>
    <text x="840" y="180">阶段说明占位</text><text x="1100" y="180">阶段说明占位</text>
  </g>
</g>
```

## K12 · 徽章箭头条

**用于**：3–4 个依次推进的步骤，只需步骤名、不需要每步的卡片（要卡片用 K03）。
**比例**：一条 `homePlate` 预设做底（高 32），步骤之间放白色小 `chevron`（12×16）；编号徽章 r 11 海军蓝、白描边 2.67 + `nodeShadow`，压在条上；步骤名 14.67 M 白字。

```xml
<g id="k12" data-pptx-bounds="auto">
  <!--P homePlate k12bar 60 230 700 32 #1C4274 -->
  <!--P chevron k12c1 276 238 12 16 #FFFFFF -->
  <!--P chevron k12c2 506 238 12 16 #FFFFFF -->
  <circle cx="84" cy="246" r="11" fill="#1C4274" stroke="#FFFFFF" stroke-width="2.67" filter="url(#nodeShadow)"/>
  <circle cx="314" cy="246" r="11" fill="#1C4274" stroke="#FFFFFF" stroke-width="2.67" filter="url(#nodeShadow)"/>
  <circle cx="544" cy="246" r="11" fill="#1C4274" stroke="#FFFFFF" stroke-width="2.67" filter="url(#nodeShadow)"/>
  <g font-family="OPPOSans B, Microsoft YaHei, sans-serif" font-size="12" fill="#FFFFFF" text-anchor="middle">
    <text x="84" y="250.2">1</text><text x="314" y="250.2">2</text><text x="544" y="250.2">3</text>
  </g>
  <g font-family="OPPOSans M, Microsoft YaHei, sans-serif" font-size="14.67" fill="#FFFFFF">
    <text x="104" y="251">阶段名称占位</text><text x="334" y="251">阶段名称占位</text><text x="564" y="251">阶段名称占位</text>
  </g>
</g>
```

## K13 · 括号分组

**用于**：一个总概念分出 2–4 个分项（一总包分几类）。
**比例**：图标 24 + 关键词 21.33 M 海军蓝；`leftBrace` 预设（宽约 12、高 = 分项行数 × 27，1.33 px 描边，无填充）；分项 16 R，行距 27。

```xml
<g id="k13" data-pptx-bounds="auto">
  <use data-icon="chunk-filled/target" x="60" y="323" width="24" height="24" fill="#1C4274"/>
  <text x="92" y="343" font-family="OPPOSans M, Microsoft YaHei, sans-serif" font-size="21.33" fill="#1C4274">核心概念</text>
  <!--P leftBrace k13b 196 300 12 70 none stroke=#1C4274 sw=1.33 -->
  <g font-family="OPPOSans R, Microsoft YaHei, sans-serif" font-size="16" fill="#404040">
    <text x="216" y="314">分项一占位</text><text x="216" y="341">分项二占位</text><text x="216" y="368">分项三占位文字</text>
  </g>
</g>
```

## K14 · 压线标题框

**用于**：一段需要单独框起来的说明或结论（样张 07 的“标题压在框线上”）。蓝版放说明，红版左边放关键词、右边放要点。
**比例**：0.75 px 细框（蓝版 `#C4D7F1` 6% 填充，红版白底）；标题放在一块白底小圆角块（rx 4、高 28）上，压住框的上沿、左缩进 16；标题 21.33 M；框内文字 14.67–16；红版中间用 0.75 px `#E3A79C` 竖线隔开关键词和要点。

```xml
<g id="k14a" data-pptx-bounds="auto">
  <rect x="420" y="316" width="330" height="120" fill="#C4D7F1" fill-opacity="0.06" stroke="#1C4274" stroke-width="0.75"/>
  <rect x="436" y="302" width="112" height="28" rx="4" fill="#FFFFFF"/>
  <text x="444" y="323" font-family="OPPOSans M, Microsoft YaHei, sans-serif" font-size="21.33" fill="#1C4274">框标题</text>
  <g font-family="OPPOSans R, Microsoft YaHei, sans-serif" font-size="16" fill="#262626">
    <text x="440" y="362" fill="#A23424">重点句占位文字，</text><text x="440" y="388">说明文字占位内容</text><text x="440" y="414">说明文字占位</text>
  </g>
</g>
<g id="k14b" data-pptx-bounds="auto">
  <rect x="790" y="316" width="450" height="120" fill="#FFFFFF" stroke="#A23424" stroke-width="0.75"/>
  <rect x="806" y="302" width="112" height="28" rx="4" fill="#FFFFFF"/>
  <text x="814" y="323" font-family="OPPOSans M, Microsoft YaHei, sans-serif" font-size="21.33" fill="#A23424">框标题</text>
  <text x="810" y="388" font-family="OPPOSans M, Microsoft YaHei, sans-serif" font-size="26.67" fill="#262626">关键词</text>
  <line x1="940" y1="346" x2="940" y2="416" stroke="#E3A79C" stroke-width="0.75"/>
  <g font-family="OPPOSans R, Microsoft YaHei, sans-serif" font-size="14.67" fill="#404040">
    <text x="958" y="358">• 要点占位文字，一行一条</text><text x="958" y="384">• 要点占位文字</text><text x="958" y="410">• 要点占位文字，一行一条</text>
  </g>
</g>
```

## K15 · 环绕弧形箭头

**用于**：围绕一个核心对象的“提升 / 循环 / 推动”关系；只在内容里确有这层动作时用。
**比例**：浅蓝底圆 r 70（`#C4D7F1` 24%）；弧箭头是 3 条错开 3–4 px 的细 `blockArc`（外框直径约为圆直径的 1.42 倍，旋转 270°）+ 三角箭头头，叠出有速度感的粗弧；一条横线穿过圆心，圆内用白色横带断开。**bounds 要手写**：`put` 的 auto 会把弧形预设的外框量大，与邻近模块误判重叠。

```xml
<g id="k15" data-pptx-bounds="500 450 282 216">
  <circle cx="640" cy="560" r="70" fill="#C4D7F1" fill-opacity="0.24" stroke="#C4D7F1" stroke-width="0.67"/>
  <g transform="rotate(270 640 560)"><!--P blockArc k15a1 540.5 460.5 199 199 #1C4274 adj1=val 16392552 adj2=val 20996104 adj3=val 1434 --></g>
  <g transform="rotate(75 628.55 462.55)"><!--P triangle k15t1 621 456 15.1 13.1 #1C4274 --></g>
  <g transform="translate(2.8 3.9)">
    <g transform="rotate(270 640 560)"><!--P blockArc k15a2 540.5 460.5 199 199 #1C4274 adj1=val 16392552 adj2=val 20996104 adj3=val 1434 --></g>
    <g transform="rotate(75 628.55 462.55)"><!--P triangle k15t2 621 456 15.1 13.1 #1C4274 --></g>
  </g>
  <g transform="translate(-4.2 2.9)">
    <g transform="rotate(270 640 560)"><!--P blockArc k15a3 540.5 460.5 199 199 #1C4274 adj1=val 16392552 adj2=val 20996104 adj3=val 1434 --></g>
    <g transform="rotate(75 628.55 462.55)"><!--P triangle k15t3 621 456 15.1 13.1 #1C4274 --></g>
  </g>
  <rect x="500" y="556" width="280" height="8" fill="#FFFFFF"/>
  <line x1="510" y1="560" x2="590" y2="560" stroke="#1C4274" stroke-width="1.33"/>
  <line x1="690" y1="560" x2="770" y2="560" stroke="#1C4274" stroke-width="1.33"/>
  <g font-family="OPPOSans M, Microsoft YaHei, sans-serif" font-size="16" fill="#1C4274" text-anchor="middle">
    <text x="640" y="544">核心主题</text><text x="640" y="588" fill="#A23424">重点占位</text>
  </g>
</g>
```

## K16 · 发光光柱 / 舞台光带

**用于**：光柱：托起一个数字或对象，让它“站”在一束浅蓝光里（参考材料 11 页用到渐隐光带）。光带：一排对象下面的舞台，把它们托成一组。
**比例**：光柱 = 一块 `gColumnTop` 渐隐矩形 + 一块 `gColumnBody` 圆底柱体（宽为矩形的 80%，底边下鼓约 12）；光带 = 上窄下宽的弧肩梯形，填 `gBeamUp`（下淡上实）。只用浅蓝，不用红。

```xml
<g id="k16" data-pptx-bounds="auto">
  <rect x="60" y="140" width="234" height="186" fill="url(#gColumnTop)"/>
  <path d="M 83.5 157.5 L 270.3 157.5 L 270.3 326.6 C 270.3 333.1 228.5 338.4 176.9 338.4 C 125.3 338.4 83.5 333.1 83.5 326.6 Z" fill="url(#gColumnBody)"/>
  <text x="176.9" y="214" text-anchor="middle" font-family="OPPOSans R, Microsoft YaHei, sans-serif" font-size="16" fill="#404040">指标说明</text>
  <text x="176.9" y="276" text-anchor="middle" font-family="OPPOSans B, Microsoft YaHei, sans-serif" font-size="48" fill="#1C4274">3.2<tspan font-size="24">倍</tspan></text>
</g>
<g id="k16b" data-pptx-bounds="auto">
  <path d="M 330 656.5 C 408.86 637 453.81 619.28 439.47 590 L 743.58 590 C 744.77 615.72 786.88 628.11 865.74 656.5 Z" fill="url(#gBeamUp)"/>
  <circle cx="530" cy="606" r="14" fill="#1C4274" stroke="#FFFFFF" stroke-width="2.67" filter="url(#nodeShadow)"/>
  <circle cx="598" cy="606" r="14" fill="#A23424" stroke="#FFFFFF" stroke-width="2.67" filter="url(#nodeShadow)"/>
  <circle cx="666" cy="606" r="14" fill="#1C4274" stroke="#FFFFFF" stroke-width="2.67" filter="url(#nodeShadow)"/>
</g>
```

## K17 · 指向块

**用于**：把一句结论标签指到它下面的具体内容（图表某段、某一项）。
**比例**：实色块约 192×71（砖红或海军蓝），底边一个宽 30、高 16 的下尖角，位置对准被指向的内容；块内 18.67 M 白字。

```xml
<g id="k17" data-pptx-bounds="auto">
  <path d="M 330 140 L 522 140 L 522 211 L 392 211 L 377 227 L 362 211 L 330 211 Z" fill="#A23424"/>
  <text x="426" y="182" text-anchor="middle" font-family="OPPOSans M, Microsoft YaHei, sans-serif" font-size="18.67" fill="#FFFFFF">结论标签</text>
  <text x="330" y="256" font-family="OPPOSans R, Microsoft YaHei, sans-serif" font-size="14.67" fill="#404040">被指向的内容占位</text>
  <path d="M 560 140 L 752 140 L 752 211 L 622 211 L 607 227 L 592 211 L 560 211 Z" fill="#1C4274"/>
  <text x="656" y="182" text-anchor="middle" font-family="OPPOSans M, Microsoft YaHei, sans-serif" font-size="18.67" fill="#FFFFFF">结论标签</text>
  <text x="560" y="256" font-family="OPPOSans R, Microsoft YaHei, sans-serif" font-size="14.67" fill="#404040">被指向的内容占位</text>
</g>
```

## K18 · 三圆交叠

**用于**：三个等权、可并列的对象（page-patterns 三B“三圆交叠”的写法）；有递进或因果的三项不要用。
**比例**：三圆等大（r 60），品字形交叠：粉 `#E8A399` 在后、海军蓝居中、砖红在前；字写在各圆没被压住的部分，18.67 M 白字。

```xml
<g id="k18" data-pptx-bounds="auto">
  <circle cx="941" cy="199" r="60" fill="#E8A399"/>
  <circle cx="940" cy="281" r="60" fill="#1C4274"/>
  <circle cx="860" cy="250" r="60" fill="#A23424"/>
  <g font-family="OPPOSans M, Microsoft YaHei, sans-serif" font-size="18.67" fill="#FFFFFF" text-anchor="middle">
    <text x="846" y="256">对象甲</text><text x="966" y="188">对象乙</text><text x="966" y="300">对象丙</text>
  </g>
</g>
```

## K19 · 箭头卡片列

**用于**：3–4 步自上而下的推进，每步有名称和两三行说明（窄栏里的竖向流程）。
**比例**：卡片 `#F4D1CC` 31% 填充 + 砖红 0.67 px 51% 描边，宽约 190；卡片之间一支 `downArrow`（36×29）居中；卡片高度按内容收紧，不留空洞。

```xml
<g id="k19" data-pptx-bounds="auto">
  <!--P downArrow k19d1 1124.5 140 36 29 #A23424 -->
  <rect x="1046" y="172" width="193" height="100" fill="#F4D1CC" fill-opacity="0.31" stroke="#A23424" stroke-width="0.67" stroke-opacity="0.51"/>
  <!--P downArrow k19d2 1124.5 278 36 29 #A23424 -->
  <rect x="1046" y="310" width="193" height="120" fill="#F4D1CC" fill-opacity="0.31" stroke="#A23424" stroke-width="0.67" stroke-opacity="0.51"/>
  <!--P downArrow k19d3 1124.5 436 36 29 #A23424 -->
  <rect x="1046" y="468" width="193" height="120" fill="#F4D1CC" fill-opacity="0.31" stroke="#A23424" stroke-width="0.67" stroke-opacity="0.51"/>
  <g font-family="OPPOSans M, Microsoft YaHei, sans-serif" font-size="16" fill="#A23424">
    <text x="1062" y="198">步骤名称一</text><text x="1062" y="336">步骤名称二</text><text x="1062" y="494">步骤名称三</text>
  </g>
  <g font-family="OPPOSans R, Microsoft YaHei, sans-serif" font-size="13.33" fill="#404040">
    <text x="1062" y="222">说明占位文字</text><text x="1062" y="242">说明占位文字</text>
    <text x="1062" y="360">说明占位文字</text><text x="1062" y="380">说明占位文字</text><text x="1062" y="400">说明占位文字</text>
    <text x="1062" y="518">说明占位文字</text><text x="1062" y="538">说明占位文字</text><text x="1062" y="558">说明占位文字</text>
  </g>
</g>
```

## 按内容选构件

| 本页内容 | 构件 |
|---|---|
| 一张主图表 + 几条结论 | K06、大号 K01 或 K08 划出图表区；K02、小号 K05、K09 托出最关键的 1–3 个数字 |
| 一个重点大区（编号 + 要点 + 数字） | K07（红）/ K08（蓝） |
| 多个并列对象的指标对比 | K01 一排并列；或 K02 一列 + 右侧图表 |
| 推进 / 阶段 / 路径 | 有每阶段内容：K03；只有步骤名：K12；窄栏竖向：K19；按时间：K11 |
| 分层流程（每层有名称） | K04 做每层名称，右侧接流程框和连线 |
| 一个总量或目标数字统领全页 | K05 放在上部做焦点；或 K16 光柱托起 |
| 上下两到三块不同性质的内容 | K06 上下堆叠，蓝红区分 |
| 一总包分几类 | K13 |
| 需要点名的关键节点 | K10（一页 1–3 个） |
| 单独框出的一段说明 / 结论 | K14 |
| 结论指向具体内容 | K17 |
| 三个等权并列的对象 | K18 |
| 围绕核心的提升 / 循环 | K15 |
