---
name: Sam-PPT-Blueprint
description: 蓝图重绘法：把用户给的 PPT 大纲做成可编辑 PPTX，每页以用户指定参考稿（如 rnb-core.pptx）里的一页为蓝图，沿用它的坐标、主图示、渐变/阴影/半透明和装饰手法，按大纲内容重新手写 SVG，学到参考稿的"神韵"而不是只换颜色。底层引擎是 ppt-master（Quick Generate，自由设计、扁平导出，不装模板、不走 mirror）；本 Skill 只加蓝图选取与重绘规则、导出时的 OPPOSans 中文字体修复（A 运行时补丁 + B 导出后兜底）和 PowerPoint 渲染自检。用户给出大纲和参考稿要求"照这份模板的感觉做 PPT"、提到 Sam-PPT-Blueprint、蓝图重绘时使用。不负责写大纲，不改大纲内容。
---

# Sam-PPT-Blueprint

**薄外壳**：项目初始化、检查、图表核对、导出全部用 ppt-master 自己的 Quick Generate 流程。本 Skill 只提供：

1. 选蓝图和重绘页面的规则（下面第 2、4 步）；
2. `scripts/export.py`：代替直接调用 `svg_to_pptx.py`，修好中文字体（见"中文字体"）；
3. `scripts/dump_blueprint.py`：把参考页的几何和配色列成清单；
4. `scripts/render.ps1`：用 PowerPoint 渲染成 PNG 自检。

不修改 ppt-master 的任何文件；`python scripts/pm.py` 打印它的位置（下文记作 `<PM>`，可用环境变量 `PPT_MASTER_DIR` 覆盖）。

## 输入

- **大纲**：逐字使用。不增删、不合并、不改写任何信息点和数字；版面放不下时调整版面，不砍内容。信息密度归 Sam-PPT-Outline 管。
- **参考稿**：用户指定的 PPTX。
- **运行目录**：在 Skill 目录之外，由用户指定；项目、成品、渲染图和运行日志都放在这里。

## 流程

### 0. 读 ppt-master

先运行 `python <PM>/scripts/attribution_guard.py`。再读 `<PM>/SKILL.md`、`workflows/routing.md`、`workflows/profiles/quick-generate.md` 以及它要求的参考文档（shared-standards-core、executor-base、semantic-svg、canvas-formats、executor-chart、native-data-interface、preset-shape-vocabulary；按需看 native-shape-authoring）。路线固定为 **Generate PPTX → Quick，自由设计（flat）**，不需要问用户。

### 1. 准备参考稿（每份参考稿只做一次）

```
python <PM>/scripts/pptx_template_import.py <参考稿.pptx> -o <参考工作区> --inheritance-mode both
powershell -ExecutionPolicy Bypass -File scripts/render.ps1 <参考稿.pptx> <参考工作区>/renders
```

用 `<参考工作区>/svg-flat/slide_NN.svg`（每页自带全部几何）和 `renders/slide-NN.png`。已有导入工作区就直接用。

### 2. 每页选一个蓝图

看参考稿渲染图，为每个大纲页挑一页：**它的主图示要能表达这一页的逻辑**（漏斗对应转化、循环对应迭代、金字塔对应分层、对称对应正反、阶梯/柱体对应阶段）。一页一个蓝图，尽量不重复。把对照表写进运行日志：大纲页 → 参考页 → 主图示。

### 3. 建项目

按 quick-generate.md：`project_manager.py init <名称> --format ppt169 --dir <运行目录> --quick-generate`，`import-sources <项目> <大纲> --copy`，`text_measure.py calibrate`（OPPOSans 各字重的角色），`icon_sync.py`（只用一个图标库）。

### 4. 逐页重绘 SVG

`python scripts/dump_blueprint.py <参考工作区>/svg-flat/slide_NN.svg` 列出蓝图，对照渲染图手写新 SVG 到 `svg_output/`。

**沿用**（这就是"神韵"）：
- 页头页脚骨架、主图示的位置和比例、模块分区坐标；
- 参考页的渐变、柔和/硬阴影、半透明叠色（用参考页的 alpha 值）、虚线框和虚线分隔、编号圆点、箭头、竖排侧栏文字、水印大字；
- 配色和字体角色（OPPOSans H/B/M/R）、字号层级。

**去掉或换掉**：
- 参考稿的 logo、照片、产品图、截图、插画全部删除，不复制；需要视觉锚点时用图标库图标或简单矢量图形代替；参考页里的矢量小图标可以把路径内联进 SVG，**不要用 `<image>` 引用参考稿的图片文件**；
- 参考页的文字只用来判断位置和字号，内容全部来自大纲；文本框按内容重新排；
- 参考页的图表按大纲数据重画：能做原生图表的做原生图表并按 verify-charts 核对；漏斗宽度、对比条长度等用形状表示数据时，尺寸要按数据算准；
- 节点、栏目数量按大纲改（参考页 5 个节点、大纲 4 步，就画 4 个）；颜色要和含义一致（风险用红、对策用蓝等）。

**SVG 写法上踩过的坑**：
- 阴影 `filter` 加在具体形状上，不要加在 `<g>` 上，也不要加在会被检查器拒绝的椭圆组合上；
- 角色图元要有 `id`；折线不要用 `marker-end`；图表 JSON 里不能出现裸 `<`；
- 用 OPPOSans B / H 的文字同时写 `font-weight="bold"`；
- 续行 `tspan` 重复父元素的 `x`；模块边界不要互相压线。

### 5. 检查

按 quick-generate.md：`stamp_native_fallbacks.py --write`，`svg_quality_checker.py <项目> --quick-generate --canonical-authoring --stage early|final --json`（页数够就过早期关卡），原生图表用 `svg_position_calculator.py calc …` 核对。必须 0 阻断再导出。

**禁止**：`--skip-validation`、`--enable-dangerous-nonconforming-svg-export`；不装模板、不用 mirror 模式（已知在 Windows 上导不出）。

### 6. 导出（代替 svg_to_pptx.py）

```
python scripts/export.py <项目> --quick-generate --no-notes --native-charts-and-tables -o <运行目录>/deck.pptx
```

最后一行必须是 `0 YaHei slot(s) left`，否则退出码为 1，去查是哪个字体名没被识别。

### 7. 渲染自检

```
powershell -ExecutionPolicy Bypass -File scripts/render.ps1 <运行目录>/deck.pptx <运行目录>/renders
```

逐页看 PNG：溢出、压字、裁切、浅底白字等低对比、参考稿残留。改 SVG → 第 5 步 → 第 6 步 → 再渲染，直到干净。页面能不能当基线由用户决定。

## 中文字体

ppt-master 的导出器只认一张固定的中文字体名单，OPPOSans 不在里面，所以中文会被写成微软雅黑。`export.py` 做两层修复，都不改 ppt-master 的文件：

- **A（主）**：在同一个进程里把 OPPOSans 各字重加进导出器的中文字体名单，再调用 ppt-master 自己的导出入口。导出器只在渲染兜底 PNG 时开子进程，那部分不涉及字体。
- **B（兜底）**：导出后运行 `scripts/fix_cjk_fonts.py`。只在同一组字体设置里英文是 OPPOSans、中文是雅黑或主题引用时，把中文改成同一字重的 OPPOSans；主题里中文字体跟随同一块的英文字体。其他字体一律不动。A 生效时它改 0 处；ppt-master 升级导致 A 失效时由它补上。也可单独用：`python scripts/fix_cjk_fonts.py deck.pptx [-o out.pptx]`。

## 运行日志

在运行目录写 `run-log.md`：起止时间、蓝图对照表、每页沿用和去掉了什么、检查和导出的结果、修了几轮、剩余问题（如实写）。
