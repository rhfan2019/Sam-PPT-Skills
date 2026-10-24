---
name: Sam-PPT-Bain
description: 把用户给的 PPT 大纲按贝恩 / 咨询白皮书风格（海军蓝 + 砖红、OPPOSans、结论标题 + 论点条 + 一个有体积感的主视觉与围绕它的配角）生成可编辑 PPTX。底层引擎是 ppt-master（Quick Generate + 本 Skill 自带的 Deck/Style 模板），本 Skill 只固化风格、规则和收尾步骤。用户给出大纲要求做成 PPT、提到 Sam-PPT-Bain、贝恩风格、蓝红咨询模板、咨询白皮书风格时使用。每次运行输出到 Skill 目录之外独立的 run-yyyymmdd-hhmmss-fff 目录，并用 PowerPoint 渲染自检。不负责写大纲。
---

# Sam-PPT-Bain

**薄外壳**：版面生成、检查、导出全部交给 ppt-master；本 Skill 提供三样东西——

1. `template/`：ppt-master 的 Deck + Style 模板工作区（6 个原型：封面、目录、章节页、正文页框、正文 + 论点条、结束页）；
2. `references/`：用户的硬规则、咨询版式做法、经用户确认的样张；
3. `scripts/sam_bain.py` + `scripts/components.py`：固定的运行目录（在 Skill 目录之外，见"运行环境"）、模板安装、字号校准、构件标记展开与正文检查、导出后的 OPPOSans 中文字体修复、PowerPoint 渲染。

不要修改 ppt-master 本身；不要再写自己的排版引擎（构件标记只展开小构件，不决定位置和版式，见第 5 步）。

## 开工前必读（每次）

开工第一条命令是 `python scripts/sam_bain.py start`（把读文档、规划的时间也记进耗时），然后读：

1. `references/rules.md` —— 用户的硬规则（不加词、推算值要列出、对齐与边界、只有用户能确认样张）。全文读。
2. `references/quick-card.md` —— page-patterns 的压缩速查（坐标、字号、构件尺寸、关系 → 构造一行表、版面纪律）。**替代通读 `references/page-patterns.md`**：本次第一次用到某个构造、或速查卡写得不够时，按卡上的 §号去读 page-patterns 原文那一节。
3. `references/ppt-master-digest.md` —— ppt-master 执行规则速查（分组与 bounds、箭头颜色、预设形状、结构化 slot、图表核验），替代通读插件执行核心；`new` 提示插件版本不符时改读原文档。
4. 看 `references/approved/template-*.png`（用户确认的封面、目录、章节、结束页原型），再读 `references/approved/samples.md`，并看其中和本次大纲页型相关的正文页样张 `sample-*.png`（用户 2026-10-23 选定的风格样张，学质感和层次，不照抄构图）。
5. `references/components/kit.md` —— 核心构件库 K01–K19（栏头面板、指标块、证据框、人字箭头、时间轴、准星节点、括号、压线框、光柱……），并看 `references/components/kit-a.png` 到 `kit-e.png` 五张效果图。**每页至少用其中 2 种**，按文末“按内容选构件”表挑，写法直接复制、只改坐标尺寸和文字。备用库 `references/components/archive/index.md` 不必读，核心库没有对得上的写法时再查。

**独立性**：本 Skill 不带任何案例的内容、数据或成品页。生成时只依据本次大纲、本 Skill 目录里的文件和 ppt-master 插件文档；不读取其他任何文件、目录、历史运行结果或 git 历史。

## 流程

```bash
python scripts/sam_bain.py start                              # 开工即跑：记下起点，读文档时间也进 timing.log
python scripts/sam_bain.py new <slug> --source <大纲.md>      # 建运行目录 + 装模板 + 字号校准（输出 PROJECT= 路径）
python scripts/sam_bain.py photos <PROJECT> city_tech.png ...  # 需要时复制素材照片（assets/photos/）
python scripts/sam_bain.py icons  <PROJECT> chunk-filled/bolt ...  # 同步图标（一套 deck 只用一个图标库；拼错的名字给近似名，不影响其余）
python scripts/sam_bain.py scaffold <PROJECT> 03_xxx --title "…" [--thesis "…"] [--sample-data] [--source-note "…"]  # 写好一页的固定页框，正文留空
python scripts/sam_bain.py measure "文字" ... --role body [--max-width 300]  # 先量后定框：宽度 / 超宽提示 / 按宽度断行
python scripts/sam_bain.py put <PROJECT> 03_xxx [正文.svg]     # 把手写正文（默认 <PROJECT>/body/03_xxx.svg）贴进页框，展开 C/T/P 标记、实测 auto bounds、正文检查，接着 preview
python scripts/sam_bain.py preview <PROJECT> 03_xxx ...       # 浏览器快速截图（含图标）→ <PROJECT>/preview/*.png，并做单页检查
python scripts/sam_bain.py check  <PROJECT> --early          # ≥7 页时，写完 P05 后跑一次
python scripts/sam_bain.py finish <PROJECT> --name <文件名>   # 终检 → 导出 → 字体修复 → 渲染 → contact.png
```

1. **新建运行**：`new` 会先跑 ppt-master 的 `attribution_guard.py`（非 0 立即停止），新建运行目录 `<运行根>/run-yyyymmdd-hhmmss-fff/`（运行根见"运行环境"，不在 Skill 目录里）、建项目、安装模板、导入大纲、输出字号校准表（每 100 px 可容纳的中/英文字数）。把输出的 `RUN_DIR=` / `PROJECT=` 和校准表留在上下文里。
2. **按 ppt-master Quick Generate 执行**：插件版本与 `references/ppt-master-digest.md` 一致时，按速查执行，不再通读执行核心；版本不一致（`new` 会提示）或用到速查没写的能力（图片页、原生图表 / 表格、公式、超链接、动画、讲稿）时，读 ppt-master 的 `SKILL.md` → `workflows/profiles/quick-generate.md` 及对应模块。模板已由 `new` 安装，跳过"Template branch"中的安装动作，但要读完已安装的两份 spec 和 6 个原型 SVG。
3. **冻结 Template Application**（固定写法，直接采用）：
   > 参考式使用。每页都用 6 个原型之一的固定层与 slot，不改页框坐标：大纲封面 → `01_cover`；大纲目录 → `02_toc`（条目 Slide-local）；大纲里的章节分隔页 → `03_chapter`；有"结论/发现"可作为 so-what 的正文页 → `04b_content_thesis`，否则 → `04a_content_frame`；只有大纲写了结束页才用 `05_ending`。正文区的几何全部 Slide-local，按 `page-patterns.md` 的页型做法构图。
4. **规划页序**：一页大纲 = 一页幻灯片，顺序不变，不增删页。为每页定：页型（见 page-patterns 第三、三B 节）、论点条文字（"结论 / 发现"原句，没有就不放）、要用到的推算值。页框文字的来源固定如下：

   | 位置 | 取值顺序 |
   |---|---|
   | 右上章节标签 | 该页所属的大纲目录章节名（带编号，如"01 章节名"）→ 大纲没有目录时用大纲头部的"页眉标签" → 都没有就留空 |
   | 左下页脚 | 大纲标了"示例数据"时用"示例数据，不作为真实统计引用"（rules.md 一.4）→ 否则用大纲头部的"说明"原句 → 都没有就留空。大纲给了"来源 / 脚注"（全局或每页）时，接在上面那句后面一起放进页脚 |
   | 右下署名 | 大纲头部的"机构" → 没有就留空 |
   | 封面署名 / 日期 | 大纲头部的"机构" / "日期" |
5. **逐页写 SVG**（主 agent 自己写，按顺序）：先用 `scaffold` 写好页框（标题、章节标签、页脚、署名按上表从大纲头部取值，`--sample-data` / `--source-note` / `--section` 覆盖；有论点条时传 `--thesis` 用 `04b`），再把正文组手写在 `<PROJECT>/body/<页名>.svg`，用 `put` 贴进页框（重复 `put` 会替换上一版正文）；按 page-patterns 对应页型构图。
   - 预设形状（箭形色带、块箭头、梯形、气泡、运算符）在正文里写成一行标记 `<!--P chevron st1 360 204 165.67 52 #16365F -->`（预设名、id、x y w h、填色；可选 `stroke=#HEX sw=1 op=0.5`，其余 `名=公式` 是调整值，如 `adj=val 15000`），`put` 会一次批量调用 `preset_shape_svg.py render-batch` 原样替换。翻转、旋转写在标记外层的 `<g transform>` 上。
   - **构件标记**（只省重复书写，位置和尺寸仍由你逐个决定）：
     - `<!--C pill x y w h "文字" [fill= stroke= color= size=12 font=R rx=] -->` 胶囊 / 小标签框（`rx=0` 为直角）；
     - `<!--C head x y w h "栏头" [fill=#1C4274 size=20 sub="（括注）"] -->` 栏头条（高 28–42）；
     - `<!--C num cx cy r "1" [fill=] -->` 编号圆（字号自动取已有档位）；
     - `<!--T x y w 字号 "长句" [font=R fill=#404040 lh=1.45 anchor=] -->` 按宽度折行的说明文字（用检查器同一套字宽，`\n` 强制换行，12 px 超 3 行直接报错）。
     文字超出自己的框、栏头高度越界时 `put` 直接报错，不悄悄缩字。行内要换色、加粗的句子仍手写。
   - **防模板化（硬性）**：
     - 每页正文第一行写 `<!--MAIN 主视觉组id-->`（精炼页写 `<!--MAIN id lean-->`）。
     - 主视觉（核心圆、漏斗、色带、曲线、矩阵、交叠圆……）必须用 `<!--P-->` 预设和手写图元构造；`put` 发现主视觉组一半以上是 C 标记、或整页六成以上图形来自 C 标记、或主视觉不到正文区 35% 时会报 `LINT … [WARN]`，见到就按 rules 五"返工时先换构造"重做，不要只调标记。
     - 不新增"卡片格 / 多栏 / 整块版式"类标记；标记只限上面四种原子。
     - **构件可复用、构图要变化**：`components/kit.md` 的构件是手写 SVG 片段，可以逐页、同页多次复制使用；变化的是整页构图——构件的组合、位置、大小、数量随内容走，相邻两页不要同样的组合摆同样的位置。
     - `finish` 会比对各页根层组的骨架，3 页以上雷同时报警：换构造，不同页用不同的 §三B 关系构造。
   - 根层组的 `data-pptx-bounds` 可以写 `auto`，`put` 按内容实测后写回（+1 px）；手写 bounds 照常可用。`put` 还会报出"带箭头的 path 含多个 M"（PowerPoint 会在每段都画箭头头）和挂在 `<g>` 上的 marker。
   - 定框前先用 `measure` 量字：给角色（`--role body` 等，同校准表）或 `--font --size`；加 `--max-width` 时标出超宽的串，只给一串时按宽度断行。
   - `put` / `preview` 截图后会跑单页检查，只打印需要处理的项（`CHECK 页名: OK / WARN / ERROR`），OPPOSans 字体提示等预期内的项已过滤。它能抓出越过模块 bounds 或画布、缺图标、结构错误；**抓不出文字溢出自己的小框或胶囊**，这类问题仍要看截图。
   - 每写完一页看截图，对照 rules.md 的自检清单，当场修。`preview` 只是浏览器预览，字体度量与 PowerPoint 略有差异，最终以 `finish` 的渲染图为准。
6. **收尾**：`finish` 在 RUN_DIR 下生成 `<文件名>.pptx`、`renders/slide-NN.png` 和 `contact.png`，最后打印一个"成品"区块（PPTX 绝对路径、渲染图目录、总览图路径）。**必须逐页看渲染图**（放大看对齐、遮挡、溢出），有问题改 SVG 后重跑 `finish`。
   - 每条命令都会往 `RUN_DIR\timing.log` 追加一行起止时间；`finish` 结束时据此打印"耗时"区块（建项目、逐页编写、每页耗时、preview/check/finish 次数、返修时长）。用户问耗时就引用这个区块。开工时跑过 `start` 的话，"读文档 + 规划"也单独列出、并计入总计；没跑就不含。
   - 成品 PPTX 正被 PowerPoint 打开时，`finish` 会自动另存为 `<文件名>-v2.pptx`、`-v3`……，以成品区块打印的路径为准。
   - 用户对某页返工时（"空""简陋"之类），按 rules.md 五"返工时先换构造，不打补丁"处理。
   - 检查器和导出报的 OPPOSans 字体安全提示（"Font stack exports non-PPT-safe typeface(s) … OPPOSans"、`unsafe_exported_faces` / portability advisory 之类）是**预期内的**：本 Skill 指定用 OPPOSans，导出后由 `fix_cjk_fonts.py` 修复。这类提示可以忽略，但只忽略这一类，其余警告照常处理。
7. **最终回复**（必须用中文，按下面的固定模板、按顺序写，不要省略任何一节；某节没有内容就写"无"）：

   ```
   **成品 PPTX**：<finish 打印的 PPTX 绝对路径>
   成品位于系统临时目录，可能被系统清理；需要保留请另存到其他位置。

   **渲染图**：<renders 目录绝对路径>；总览图：<contact.png 绝对路径>

   **每页原型与主视觉**
   - P01 <原型，如 04b_content_thesis>：<主视觉一句话>
   - …

   **对大纲的省略、拆分、推断**
   - 推算值：<数值> = <算式>（请核实）
   - 对原文的改动：<拆句 / 缩写 / 省略的原句与位置>
   - 推断：<按推断建立的对应关系、示意性的图（大纲没给数值）、因超长缩小字号或挪走前缀的标题、按精炼页处理的页、完全没用图标的页及原因>

   **仍不满意的地方**
   - <与样张的差异、已知限制、自己觉得还不够好的页面和原因>
   ```

   **不要自己宣布"通过"**，请用户判断。

## 运行环境

- Windows + PowerPoint（渲染）+ OPPOSans 字体；Python 3.12（命令用 `python`，不是 `python3`）。
- ppt-master 插件位置自动查找（`~/.claude/plugins/cache/ppt-master/...`），可用环境变量 `PPT_MASTER_DIR` 指定。
- **运行根**：默认是 `D:\Workspace\Sam-PPT-Skills-Test\runs\Sam-PPT-Bain\`；本机没有 `D:\Workspace\Sam-PPT-Skills-Test\runs` 时退回 `<系统临时目录>\claude\Sam-PPT-Runs\Sam-PPT-Bain\`；可用环境变量 `SAM_PPT_RUNS` 覆盖。运行目录一律以 `new` 打印的 `RUN_DIR=` 为准；不要读取运行根下其他运行的目录。
- Bash 里跑 Python 输出中文时加 `PYTHONIOENCODING=utf8`；Windows 长路径会让 Python 起不来，临时文件放短路径。
