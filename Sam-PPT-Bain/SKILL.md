---
name: Sam-PPT-Bain
description: 把用户给的 PPT 大纲按贝恩 / 咨询白皮书风格（海军蓝 + 砖红、OPPOSans、论点条 + 区块标签 + 主图两翼 + 证据框 + 框架条）生成可编辑 PPTX。底层引擎是 ppt-master（Quick Generate + 本 Skill 自带的 Deck/Style 模板），本 Skill 只固化风格、规则和收尾步骤。用户给出大纲要求做成 PPT、提到 Sam-PPT-Bain、贝恩风格、蓝红咨询模板、咨询白皮书风格时使用。每次运行输出到 Skill 目录之外（系统临时目录下）独立的 run-yyyymmdd-hhmmss-fff 目录，并用 PowerPoint 渲染自检。不负责写大纲。
---

# Sam-PPT-Bain

**薄外壳**：版面生成、检查、导出全部交给 ppt-master；本 Skill 提供三样东西——

1. `template/`：ppt-master 的 Deck + Style 模板工作区（6 个原型：封面、目录、章节页、正文页框、正文 + 论点条、结束页）；
2. `references/`：用户的硬规则、咨询版式做法、经用户确认的样张；
3. `scripts/sam_bain.py`：固定的运行目录（在 Skill 目录之外，见"运行环境"）、模板安装、字号校准、导出后的 OPPOSans 中文字体修复、PowerPoint 渲染。

不要修改 ppt-master 本身；不要再写自己的排版引擎。

## 开工前必读（每次）

1. `references/rules.md` —— 用户的硬规则（不加词、推算值要列出、对齐与边界、只有用户能确认样张）。
2. `references/page-patterns.md` —— 坐标体系、常用构件的精确尺寸、页型做法。
3. 看 `references/approved/template-*.png`（用户确认的封面、目录、章节、结束页原型）。

**独立性**：本 Skill 不带任何案例的内容、数据或成品页。生成时只依据本次大纲、本 Skill 目录里的文件和 ppt-master 插件文档；不读取其他任何文件、目录、历史运行结果或 git 历史。

## 流程

```bash
python scripts/sam_bain.py new <slug> --source <大纲.md>      # 建运行目录 + 装模板 + 字号校准（输出 PROJECT= 路径）
python scripts/sam_bain.py photos <PROJECT> city_tech.png ...  # 需要时复制素材照片（assets/photos/）
python scripts/sam_bain.py icons  <PROJECT> chunk-filled/bolt ...  # 同步图标（一套 deck 只用一个图标库）
python scripts/sam_bain.py check  <PROJECT> --early          # ≥7 页时，写完 P05 后跑一次
python scripts/sam_bain.py finish <PROJECT> --name <文件名>   # 终检 → 导出 → 字体修复 → 渲染 → contact.png
```

1. **新建运行**：`new` 会先跑 ppt-master 的 `attribution_guard.py`（非 0 立即停止），新建运行目录 `<运行根>/run-yyyymmdd-hhmmss-fff/`（运行根见"运行环境"，不在 Skill 目录里）、建项目、安装模板、导入大纲、输出字号校准表（每 100 px 可容纳的中/英文字数）。把输出的 `RUN_DIR=` / `PROJECT=` 和校准表留在上下文里。
2. **按 ppt-master Quick Generate 执行**：读 ppt-master 的 `SKILL.md` → `workflows/profiles/quick-generate.md`，按它的 §2–§4 走（规划能力批次、执行核心 `shared-standards-core.md` / `executor-base.md` / `semantic-svg.md` / `preset-shape-vocabulary.md`、结构化页面的 `pptx-structure-interface.md`、图表页的 chart 模块）。模板已由 `new` 安装，跳过"Template branch"中的安装动作，但要读完已安装的两份 spec 和 6 个原型 SVG。
3. **冻结 Template Application**（固定写法，直接采用）：
   > 参考式使用。每页都用 6 个原型之一的固定层与 slot，不改页框坐标：大纲封面 → `01_cover`；大纲目录 → `02_toc`（条目 Slide-local）；大纲里的章节分隔页 → `03_chapter`；有"结论/发现"可作为 so-what 的正文页 → `04b_content_thesis`，否则 → `04a_content_frame`；只有大纲写了结束页才用 `05_ending`。正文区的几何全部 Slide-local，按 `page-patterns.md` 的页型做法构图。
4. **规划页序**：一页大纲 = 一页幻灯片，顺序不变，不增删页。为每页定：页型（见 page-patterns 第三、三B 节）、论点条文字（"结论 / 发现"原句，没有就不放）、要用到的推算值。页框文字的来源固定如下：

   | 位置 | 取值顺序 |
   |---|---|
   | 右上章节标签 | 该页所属的大纲目录章节名（带编号，如"01 章节名"）→ 大纲没有目录时用大纲头部的"页眉标签" → 都没有就留空 |
   | 左下页脚 | 大纲标了"示例数据"时用"示例数据，不作为真实统计引用"（rules.md 一.4）→ 否则用大纲头部的"说明"原句 → 都没有就留空 |
   | 右下署名 | 大纲头部的"机构" → 没有就留空 |
   | 封面署名 / 日期 | 大纲头部的"机构" / "日期" |
5. **逐页写 SVG**（主 agent 自己写，按顺序）：按 page-patterns 对应页型构图；写完每页对照 rules.md 的自检清单。
6. **收尾**：`finish` 在 RUN_DIR 下生成 `<文件名>.pptx`、`renders/slide-NN.png` 和 `contact.png`，最后打印一个"成品"区块（PPTX 绝对路径、渲染图目录、总览图路径）。**必须逐页看渲染图**（放大看对齐、遮挡、溢出），有问题改 SVG 后重跑 `finish`。
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
   - 推断：<按推断建立的对应关系、示意性的图（大纲没给数值）、因超长缩小字号的标题、完全没用图标的页及原因>

   **仍不满意的地方**
   - <与样张的差异、已知限制、自己觉得还不够好的页面和原因>
   ```

   **不要自己宣布"通过"**，请用户判断。

## 运行环境

- Windows + PowerPoint（渲染）+ OPPOSans 字体；Python 3.12（命令用 `python`，不是 `python3`）。
- ppt-master 插件位置自动查找（`~/.claude/plugins/cache/ppt-master/...`），可用环境变量 `PPT_MASTER_DIR` 指定。
- **运行根**：默认是 `<系统临时目录>\claude\Sam-PPT-Runs\Sam-PPT-Bain\`（`tempfile.gettempdir()` 拼出，Windows 上一般是 `%LOCALAPPDATA%\Temp\claude\Sam-PPT-Runs\Sam-PPT-Bain\`），可用环境变量 `SAM_PPT_RUNS` 覆盖。运行目录一律以 `new` 打印的 `RUN_DIR=` 为准；不要读取运行根下其他运行的目录。
- Bash 里跑 Python 输出中文时加 `PYTHONIOENCODING=utf8`；Windows 长路径会让 Python 起不来，临时文件放短路径。
