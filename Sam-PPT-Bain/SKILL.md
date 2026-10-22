---
name: Sam-PPT-Bain
description: 把用户给的 PPT 大纲按贝恩 / 咨询白皮书风格（海军蓝 + 砖红、OPPOSans、论点条 + 区块标签 + 主图两翼 + 证据框 + 框架条）生成可编辑 PPTX。底层引擎是 ppt-master（Quick Generate + 本 Skill 自带的 Deck/Style 模板），本 Skill 只固化风格、规则和收尾步骤。用户给出大纲要求做成 PPT、提到 Sam-PPT-Bain、贝恩风格、蓝红咨询模板、咨询白皮书风格时使用。每次运行输出到独立的 runs/run-yyyymmdd-hhmmss-fff 目录，并用 PowerPoint 渲染自检。不负责写大纲。
---

# Sam-PPT-Bain

**薄外壳**：版面生成、检查、导出全部交给 ppt-master；本 Skill 提供三样东西——

1. `template/`：ppt-master 的 Deck + Style 模板工作区（6 个原型：封面、目录、章节页、正文页框、正文 + 论点条、结束页）；
2. `references/`：用户的硬规则、咨询版式做法、经用户确认的样张；
3. `scripts/sam_bain.py`：固定的运行目录、模板安装、字号校准、导出后的 OPPOSans 中文字体修复、PowerPoint 渲染。

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

1. **新建运行**：`new` 会先跑 ppt-master 的 `attribution_guard.py`（非 0 立即停止），在 `runs/run-*/` 下建项目、安装模板、导入大纲、输出字号校准表（每 100 px 可容纳的中/英文字数）。把校准表留在上下文里。
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
6. **收尾**：`finish` 生成 `runs/run-*/<文件名>.pptx`、`renders/slide-NN.png` 和 `contact.png`。**必须逐页看渲染图**（放大看对齐、遮挡、溢出），有问题改 SVG 后重跑 `finish`。
7. **交付说明**（中文）：成品路径、contact.png；逐条列出推算值（算式）；列出所有对大纲原文的改动（拆句、缩写、省略）；列出示意性的图（大纲没给数值的曲线、小图）、按推断建立的对应关系、因超长而缩小字号的标题、完全没用图标的页及原因；列出与样张的差异和已知限制。**不要自己宣布"通过"**，请用户判断。

## 运行环境

- Windows + PowerPoint（渲染）+ OPPOSans 字体；Python 3.12（命令用 `python`，不是 `python3`）。
- ppt-master 插件位置自动查找（`~/.claude/plugins/cache/ppt-master/...`），可用环境变量 `PPT_MASTER_DIR` 指定。
- Bash 里跑 Python 输出中文时加 `PYTHONIOENCODING=utf8`；Windows 长路径会让 Python 起不来，临时文件放短路径。
