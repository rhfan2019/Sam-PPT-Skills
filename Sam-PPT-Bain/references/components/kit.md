# 构件库（用户 2026-10-23 选定的 6 个风格构件）

从用户提供的参考材料里抽出的 6 个构件，只保留形状、比例、配色和效果参数，文字一律是占位词。渲染效果见同目录 `kit-a.png`（构件 1–4、6）和 `kit-b.png`（构件 5）。**动笔前先看这两张图。**

这些构件是本 Skill 风格的"手艺"部分：它们的造型、比例和渐变参数已经调好，**直接复制下面的写法，只改坐标、尺寸和文字**，不要重新发明造型，也不要改配色和效果参数。

## 用法约定：构件可复用，构图要变化

- **每页至少用 2 种构件**（数据页也一样）。图表、表格放进构件 1 或构件 6 划出的大区里，关键数字用构件 2 或构件 5 托出来。
- 同一构件可以在多页、同一页里多次使用；变化的是**整页构图**：构件的组合、位置、大小和数量随本页内容变化。相邻两页不要用同样的构件组合摆同样的位置；连续三页不要用同一种分区方式（全用页签面板或全用侧标签条）。
- 构件只承载大纲里的真实内容。没有对应内容就不放（例如没有阶段关系就不用人字箭头，没有单一主角数字就不用光晕底板）。
- 颜色只用蓝、红两个版本：左 / 用户侧 / 现状用蓝，右 / 策略侧 / 判断用红（rules 二.6）。
- 渐变和阴影的 id（`gNavyV`、`gFadeRedUp`、`gBoardRed`、`tileShadow`、`softShadow` 等）已由 `scaffold` 写进页面 `<defs>`，正文里直接引用。
- 预设形状写成 `<!--P …-->` 标记（SKILL.md 第 5 步）；整组可以用外层 `<g transform="translate(dx,dy)">` 平移。

## 1. 页签 + 浅底面板

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

## 2. 图标指标块

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

## 3. 人字箭头色带 + 阶段卡

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

## 4. 立体标签

**用于**：一列 2–4 个并列类别名（流程每一层的名称、象限或分组的名称），放在一列内容的最左端或节点上，代替平面胶囊。标签上方可写一行说明（20 M，同色）。
**比例**：137×49（可在 110–170 宽之间伸缩，高宽比保持约 1:2.8）；文字 20 B 白色，居中于正面（x 中心 = X + 宽 × 0.45，基线 = Y + 33）。PowerPoint 会自动把顶面画浅、侧面画深。

```xml
<g id="cube-a" data-pptx-bounds="auto">
  <text x="X" y="Y-12" font-family="OPPOSans M, Microsoft YaHei, sans-serif" font-size="20" fill="#1C4274">标签上方说明</text>
  <!--P cube cubeA X Y 137 49 #1C4274 -->                                     <!-- 红版 #A23424 -->
  <text x="X+62" y="Y+33" text-anchor="middle" font-family="OPPOSans B, Microsoft YaHei, sans-serif" font-size="20" fill="#FFFFFF">类别</text>
</g>
```

## 5. 透视光晕底板 + 英雄数字

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

## 6. 竖排侧标签条

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

## 和图表、主视觉怎么配

| 本页内容 | 推荐组合 |
|---|---|
| 一张主图表 + 几条结论 | 构件 6 或大号构件 1 划出图表区；构件 2 或小号构件 5 托出最关键的 1–3 个数字 |
| 多个并列对象的指标对比 | 构件 1 一排并列；或构件 2 一列 + 右侧图表 |
| 推进 / 阶段 / 路径 | 构件 3 做骨架，卡片里放各阶段内容；关键阶段用红 |
| 分层流程（每层有名称） | 构件 4 做每层名称，右侧接流程框和连线 |
| 一个总量或目标数字统领全页 | 构件 5 放在页面上部做焦点，下面接拆解图表或构件 2 |
| 上下两到三块不同性质的内容 | 构件 6 上下堆叠，蓝红区分 |
