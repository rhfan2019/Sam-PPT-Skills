---
name: Sam-PPT-Blueprint
description: 蓝图重绘法：把用户给的 PPT 大纲做成可编辑 PPTX，每页从用户指定参考稿（如 rnb-core.pptx）里选一页作蓝图，把这一页的 SVG 复制过来，在上面删掉参考稿的图片和内容、换成大纲内容，保留它的坐标、主图示、渐变/阴影/半透明和装饰，学到参考稿的"神韵"而不是只换颜色。底层引擎是 ppt-master（Quick Generate，自由设计、扁平导出，不装模板、不走 mirror）；本 Skill 只加蓝图选取与重绘规则、导出时的 OPPOSans 中文字体修复（A 运行时补丁 + B 导出后兜底）和 PowerPoint 渲染自检。用户给出大纲和参考稿要求"照这份模板的感觉做 PPT"、提到 Sam-PPT-Blueprint、蓝图重绘时使用。不负责写大纲，不改大纲内容。
---

# Sam-PPT-Blueprint

**薄外壳**：项目初始化、检查、图表核对、导出全部用 ppt-master 自己的 Quick Generate 流程。本 Skill 只提供：

1. 选蓝图和在蓝图上修改的规则（下面第 2、4 步）；
2. `scripts/start_page.py`：把蓝图页复制成项目页面，作为修改的起点；`scripts/check_reuse.py`：检查页面还剩多少来自蓝图；
3. `scripts/export.py`：代替直接调用 `svg_to_pptx.py`，修好中文字体（见"中文字体"）；
4. `scripts/dump_blueprint.py`：把参考页的几何和配色列成清单；
5. `scripts/render.ps1`：用 PowerPoint 渲染成 PNG 自检。

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

起页用 `<参考工作区>/authoring-svg-flat/slide_NN.svg`，看图用 `renders/slide-NN.png`（保持默认的 1600 px，不要缩小）。已有导入工作区就直接用。

### 2. 每页选一个蓝图

看参考稿渲染图，为每个大纲页挑一页：**它的主图示要能表达这一页的逻辑**（漏斗对应转化、循环对应迭代、金字塔对应分层、对称对应正反、阶梯/柱体对应阶段），而且**模块数量和大纲条目数接近**，这样第 4 步才能原地修改而不是重画。一页一个蓝图，尽量不重复。把对照表写进运行日志：大纲页 → 参考页 → 主图示 → 要增删的模块。`python scripts/dump_blueprint.py <slide_NN.svg>` 可以列出一页的全部形状帮助判断。

### 3. 建项目

按 quick-generate.md：`project_manager.py init <名称> --format ppt169 --dir <运行目录> --quick-generate`，`import-sources <项目> <大纲> --copy`，`text_measure.py calibrate`（OPPOSans 各字重的角色），`icon_sync.py`（只用一个图标库）。

### 4. 从蓝图页起步，原地修改（不要重画）

**每一页都必须从蓝图页的 SVG 文件开始，在它上面删、改、换；禁止新建空白 SVG 自己构图。** "神韵"就在蓝图页的几何、渐变、阴影、半透明和装饰里，重画一定会丢。

1. 起页：`python scripts/start_page.py <参考工作区>/authoring-svg-flat/slide_NN.svg <项目>/svg_output/NN_页名.svg`。它复制蓝图页，只删掉带不过来的东西（图片和图片裁剪框、指向被删图片的连接线绑定、自定义几何的源信息、导入插画），把挂在组上的阴影移到形状上，把描边渐变改成首色，其余全部保留，并在页面里记下蓝图来源。
2. 原地修改，按这个顺序：
   - **文字**：在原有文本元素里把参考稿文字换成大纲内容，保留原来的位置、字体、字号、颜色和对齐；放不下时先精简换行、再微调这个文本框的宽高，不要整块重排。
   - **数量**：大纲条目比蓝图少，删掉多出的整个模块（连同它的底色、编号、连线）；多，就复制一个同类模块，按蓝图里的间距平移。
   - **图片位**：删掉的 logo、照片、产品图位置，用图标库图标、数字或简单形状补上，或者让相邻模块占用；页头的手形图标用图标库的 `pointer` 放在原位置。
   - **图表**：蓝图里的原生图表保留位置和样式，换成大纲数据；蓝图里用形状画的图表，按大纲数据重算尺寸。能做原生图表的做原生图表，按 verify-charts 核对。
   - **颜色**：沿用蓝图配色，只在含义需要时对调（风险用红、对策用蓝等）。
   - 参考稿内容（品牌名、产品名、案例文字）一个都不能留。
3. 改完一页，跑 `python scripts/check_reuse.py <项目>/svg_output <参考工作区>/authoring-svg-flat` 看这一页还剩多少形状来自蓝图（刚起页是 100%，凭空画的页只有 5–10%）。低于 50% 说明已经在重画了：回到蓝图页重新起页；确实需要大改的，在运行日志里写明原因。

**SVG 写法上踩过的坑**：
- 阴影 `filter` 加在具体形状上，不要加在 `<g>` 上，也不要加在会被检查器拒绝的椭圆组合上；
- 角色图元要有 `id`；折线不要用 `marker-end`；图表 JSON 里不能出现裸 `<`；
- 用 OPPOSans B / H 的文字同时写 `font-weight="bold"`；
- 续行 `tspan` 重复父元素的 `x`；模块边界不要互相压线；
- 少数蓝图页起页后仍有检查错误（箭头标记颜色和线条颜色不一致、带文字的组用了复合变换、表格合并单元格不为空），修改这一页时一并处理；参考稿原文超出页面的错误，换成大纲文字后会消失。

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

在运行目录写 `run-log.md`：起止时间、蓝图对照表、每页增删了哪些模块、`check_reuse.py` 的结果、检查和导出的结果、修了几轮、剩余问题（如实写）。
