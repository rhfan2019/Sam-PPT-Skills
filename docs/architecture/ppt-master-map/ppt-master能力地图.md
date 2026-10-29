# ppt-master 6.7.2 能力地图（含与 Sam-PPT-MBB 的对照）

> 状态：现行参考，适用于 ppt-master 6.7.2（2026-10-26 通读）。插件升级后先重读文档集并更新本目录。独立复核见[同目录复核版](ppt-master能力地图-独立复核.md)。文中"Sam-PPT-MBB"是已退役的上一版 Skill。

2026-10-26。通读范围：`SKILL.md`、`workflows/` 全部 24 个文件、`references/` 全部 110 个文件、`templates/` 全部说明文档、`scripts/README.md` 和 `scripts/docs/` 全部 22 篇，以及约 60 个脚本的命令行定义。说明文档合计约 2.5 万行。每条能力的出处（文件:行号）见同目录 5 份分册：A-workflows、B-core-references、C-styles-images、D-templates、E-scripts。下文的路径都相对于插件根目录。

---

## 0. 结论先行

1. **ppt-master 有三条路线，其中一条正好对应我们最初的目标，但我们从没用过。** 路线 3「Edit Native PPTX」的定位是：把一份现成的 PPTX 模板当作页面库，按每段内容的论证形态挑出原稿页，填入新内容，同时保留原稿的原生设计（`workflows/edit-native-pptx.md:11-16, 58`）。用户买的 R&B.pptx 正适合走这条路。
2. **我们用的是 Quick 模式，它恰好拿掉了 ppt-master 的设计规划层。** 这一层包括：策划角色、三套方案比较、design_spec 和 spec_lock、每页的 Relationships、Composition、Audience move、page_rhythm 字段、五页一次的锁定值重读，以及按模板做规划的 strategist-template。Quick 拿掉这些之后，我们又自己写规则、检查和标记去补（`quick-generate.md:17-27`）。
3. **ppt-master 明文反对"素"。** 终检之后有一道必做的"载体回执"复核：全稿没用预设形状、没有行内强调、没有渐变、没有图标，或者用到预设形状的页比有顺序 / 包含关系的页还少，都要写出理由。它还写明"风格、速度、克制都不算理由"（`references/executor-base.md:286-305`）。而我们的 Style 和检查，一直在把页面往"克制"那头推。
4. **我们自己写的不少东西，ppt-master 已经有现成的。** 有的与 ppt-master 的工具重复，有的与它的规则冲突（见第 9 节）。
5. **ppt-master 自带咨询风格的素材，我们没看过。** 包括：Style `mbb-consulting` 和 `consulting-decision`，论证方式 `pyramid`，阅读方式 `text`，视觉风格 `editorial`、`swiss-minimal`、`data-journalism`，以及 bain、mckinsey、bcg 等品牌配色。

---

## 1. 路线全景

| 路线 / 配置档 | 做什么 | 何时用 | 关键产物 |
|---|---|---|---|
| **Generate · Default** | 从素材生成新 deck；先由策划做设计规划，经两轮确认，再逐页绘制 | 默认 | design_spec.md、spec_lock.md、svg_output、PPTX |
| Generate · Quick | 同上，但没有策划、确认和锁定文件，一次跑完 | 用户明说要快、跳过确认 | svg_output、PPTX |
| Generate · Beautify | 原 PPTX 逐页重新设计，文字和页数不变 | 美化已有 PPTX | PPTX |
| Generate · Image to PPTX | 把图片页还原成可编辑 PPTX | 只能在 Codex 上用 | PPTX |
| **Create Template** | 从参考材料生成可复用的 Brand、Style、Layout 或 Deck 工作区 | 做模板 | templates/ 工作区 |
| **Edit Native PPTX** | 把原 PPTX 转成可往返编辑的工作区；未改动的页逐字节还原，改动的页只重建改了的部分；可删页、重排、重复使用某页、填新内容 | 填一份现成模板并保留其设计 | page_plan.json、PPTX，以及原样保留、局部修改、重建三类页的回执 |

额外的步骤按需挂上：资料调研、设计规划审阅（refine-spec）、图表数值核验（verify-charts）、视觉自审（visual-review）、实时预览（live-preview）、自定义动画、配音和视频、网图评审。

---

## 2. Default 生成流程（我们漏掉的那一层）

| 步 | 内容 | Quick 有没有 |
|---|---|---|
| 1 | 素材转 Markdown（`source_to_md.py`，支持 PDF、Word、Excel、PPTX、网页等） | 有 |
| 2 | 建项目、导入素材，生成 PPTX 原稿的特征包 | 有 |
| 3 | 列出可选模板 | 无，只能直接指定模板 |
| 4 | **策划**：第一轮确认受众、目的、核心信息和模板；第二轮给出**三套明显不同的方案**（论证方式、视觉风格、配色、字体、图标、图片、页数、阅读方式）供挑选；然后写 design_spec（第 I–X 节）和 spec_lock，过两道一致性检查 | **无** |
| 4a | design_spec 第 IX 节逐页写明：Audience move（这页要让读者怎么想）、**Relationships**（内容单元之间是顺序、因果、上下级、并列、对照还是交叠）、Composition（构图参考）、数据来源编号、是否导出为原生图表；任何字段加 `(binding)` 后，绘制时必须照办 | **无** |
| 4b | spec_lock 锁定配色、字体档位、图标库、**每页节奏**（anchor 重点页 / dense 密页 / breathing 留白页）、页面结构 | **无** |
| 5 | 图片：AI 生成、网图检索、切图、图片处理 | 有 |
| 6 | **绘制**：动笔前做字宽校准，自动开实时预览；每页走 9 步决策：拓扑判定 → 节奏 → 载体组合 → 模块行 → 构图 → **几何签名**（和前几页比，构造不得无故雷同）→ 坐标；第 5 页后跑一次早检，最后终检，再做**载体回执复核** | 绘制步骤有；但没有每页规划和锁定可依，五页重读也没有 |
| 7 | 拆分讲稿 → finalize → 导出原生 PPTX（附出货报告） | 不做 finalize |

**一句话**：Default 先逐页决定"这页的逻辑关系是什么、用什么图形承载、和前后页怎么区分"，再动笔。Quick 只能边画边想。我们用了 Quick，又写了 page-patterns、quick-card、规划表、`<!--MAIN-->` 标记和雷同检查，等于自己重造了一个简化版的策划层。

---

## 3. 模板体系（四种，各管一段）

| 种类 | 管什么 | 不管什么 | 装进项目后的效果 |
|---|---|---|---|
| Brand | 身份：配色、字体、标志、语气、图标风格 | 页面结构 | 页面不带母版 |
| Style | 方法和视觉默认：论证方式、页面角色、证据纪律、构图、密度、装饰、配色行为、审阅要点 | 身份（它的配色只是候选，会被 Brand / Deck 覆盖）、页面结构 | 只装 Style 时页面不带母版 |
| Layout | 与品牌无关的结构：画布、母版与版式、页面类型、占位框 | 配色、字体 | 带母版和版式 |
| Deck | 某类反复出现的演示：应用场景 + 身份 + 结构 | — | 带母版和版式 |

- 优先级：身份 Brand > Deck；结构 Layout > Deck；Style 只管方法（`workflows/stages/apply-template-workspace.md:87-100`）。
- 模板的复用范围：`mirror` 照搬原型页、只换文字；`layout` 沿用母版和版式、内容自由；`style` 只取方向。贴合程度分 strict 和 adaptive 两档（`strategist-template.md:25-31`）。
- **制作方式**（Create Template）：`standard` 自由设计；`fidelity` 忠实还原；`mirror` 把原 PPTX 页面逐页镜像过来，保留原生对象（`create-template.md:62-68`）。
- **模板里的字号不会被继承**，字号一律取锁定的字体档位（`executor-structured.md:25`）。

**自带资产里和咨询相关的：**
- Style `mbb-consulting`：结论先行、文档级密度；带编号的图表（A、B、C 编号徽标、单位行）、关键信息栏、浅灰"含义"面板、编号脚注加来源行；每页 5–7 个模块；不用卡片、不用阴影；字号：标题 24、正文 14、脚注 10；后备配色是麦肯锡系的海军蓝。
- Style `consulting-decision`：同一套方法，视觉更松（1–3 个主区）。
- Layout `report_core`：两套母版，真实的页码、页脚、日期占位符，页眉和页脚细线，"先用细线、再用容器"。
- Brand bain、mckinsey、bcg、accenture、deloitte、pwc：只有配色、字体和语气，没有页面 SVG。
- 论证方式 `pyramid`：结论式标题、SCQA、要点句、MECE、驱动树、2×2，每个数据页都标来源。
- 阅读方式 `text`：读稿型白皮书，正文起始 20 px（这一点我们的 Style 定的是 14–16）。
- 视觉风格 `editorial`（细线和分栏取代卡片）、`swiss-minimal`（官方注明适合"高端咨询"；单一粗细的线、少数几个大面、颜色只作分区）、`data-journalism`（高密度证据、细线、每页来源行）；可用 `custom` 组合多个。

---

## 4. 绘制工具箱（executor 可以动用的手段）

- **文字手段**：引导语、行内强调、引语、眉题、英雄数字、要点句。
- **18 种常用版面元件**：渐变带、卡片、图标加标签、编号圆、KPI 卡、要点框、分隔线和 2 px 强调条、满版图加遮罩、引语块、时间线 / 步骤条、流程图、标注、强调立体对象等（`executor-base.md:51-72`）。
- **7 种关系对应的结构**：单一论点、对等比较、主证据加结论（3:7 或 2:8）、并列序列、核心加周边、宽图加说明、整页大图形组织（page field）。
- **187 种 Office 预设形状**和布尔合并：箭形、括号、大括号、梯形、弧、环、标注气泡等。预设形状由 `preset_shape_svg.py render-batch` 生成，布尔合并用 `shape_boolean_svg.py`。
- **拓扑组装**：按 Relationships 组装箭形阶段、分合流、泳道、梯形金字塔、交叠圆、阈值不居中的 2×2、放射结构等；不得因为"节点数量相等"就做成对称（`executor-structure.md:32`）。
- **构图视角**：page field（一个大图形组织全页）、outline carrier（不填色的框、弧、括号、带）、嵌套、跨页连续、景深与对比。这些正是"线条感"的正规做法（`native-shape-authoring.md:79-88`）。
- **效果**：渐变、透明度、阴影 / 发光（分四档高度）、半调网点、刻面、纸雕、墨迹等构造风格，虚线预设，文字效果，径向 / 仪表 / 旭日图（`svg-effects.md`，610 行）。
- **图表**：33 种参考图，其中 23 种可导出为原生可编辑图表；**表格**：6 种，"只用横线，不画满格"；还有数值核验工具。
- **原生公式、超链接、讲稿、动画**（48 种切换、203 种对象动画、Morph）、**配音和视频**。

---

## 5. 质量关口

| 关口 | 必做还是可选 | 管什么 |
|---|---|---|
| 策划一致性检查 1、2 和 `project_manager.py validate` | Default 必做 | 设计规划和确认一致；锁定文件语法正确 |
| `svg_quality_checker.py` 早检（第 5 页后）和终检 | 必做；导出时没有终检报告就拒绝导出 | 禁用元素、越界、文字溢出超过 5%、根组重叠、字号档位漂移（第三次出现未声明的字号即报错）、与 spec_lock 的配色和字体对齐、图片授权等。**没有可调的阈值或开关** |
| **载体回执复核** | 必做 | 预设形状、行内强调、渐变、图标的使用量与页面任务是否相符；没用的要写理由，"克制"不算理由 |
| 几何签名、全稿节奏检查 | 必做（在上下文中进行） | 防止页面模板化、雷同 |
| verify-charts | 有数据图表时必做 | 图表数值和几何位置 |
| visual-review | **只有用户明说才做** | 硬项 H1–H9（越界、溢出、遮挡、对比度等）、软项 S1–S10（节奏、对齐、强调错位、留白页里塞卡片等），以及 Style 的审阅要点 |
| `pptx_delivery_check.py` | 可选 | 成品 PPTX 的完整性、字体可移植性、媒体体积 |

---

## 6. 工具清单（按用途）

- **素材**：`source_to_md.py`、`pptx_intake.py`、`analyze_images.py`
- **项目**：`project_manager.py`（init、import-sources、validate、page-context）、`workflow_log.py`
- **模板**：`pptx_template_import.py`、`mirror_template_materialize.py`、`svg_authoring_view.py`、`extract_svg_assets.py`、`extract_svg_pictures.py`、`template_preview_pptx.py`、`apply_template.py`、`register_template.py`
- **确认与审阅**：`confirm_ui/server.py`（两轮确认页面）、`spec_review/server.py`（在浏览器里审改 design_spec）、`svg_editor/server.py --live`（实时预览，可直接拖改、加批注）、`check_annotations.py`
- **绘制辅助**：`text_measure.py`（measure、wrap、box、calibrate）、`preset_shape_svg.py`、`shape_boolean_svg.py`、`svg_position_calculator.py`、`visualization_recall.py`、`icon_sync.py`（5 个图标库共 1.2 万个图标）
- **检查与审阅**：`svg_quality_checker.py`（`--stage early|page|final`、`--slot-capacity-report`）、`visual_review.py`
- **收尾与导出**：`compact_svg_styles.py`、`compact_svg_coordinates.py`、`stamp_native_fallbacks.py`、`update_spec.py`（全稿换色换字体，**需要 spec_lock**）、`total_md_split.py`、`finalize_svg.py`、`svg_to_pptx.py`（母版结构、原生图表 / 表格、讲稿、动画、配音）、`pptx_delivery_check.py`
- **往返编辑**：`pptx_to_svg.py --roundtrip`、`svg_to_pptx.py --roundtrip`
- **图片**：`image_gen.py`（15 个后端，或用宿主自带的生图工具）、`image_search.py`、`slice_images.py`、`image_treat.py`
- **配音和视频**：`notes_to_audio.py` → `narration_sync.py` → `powerpoint_video.py` → `video_sound_mix.py` / `video_subtitles.py`

---

## 7. 默认关闭、容易漏掉的

1. Default 的策划层：Quick 里整层都没有。
2. strategist-template（按已装模板做规划）：只在 Default 且装了模板时才加载。
3. refine-spec：动笔前在浏览器里审改逐页规划，相当于咨询公司的"故事线评审"。默认关闭。
4. visual-review：只有用户明说才做；Style 的审阅要点也只在这时生效。
5. 原生可编辑图表 / 表格：要同时满足第 IX 节标了 `Native-ready` 和导出加 `--native-charts-and-tables`。
6. `(binding)`：加在逐页规划的任何字段后面，绘制时必须照办。
7. spec_lock 的 `forbidden`：只收用户原话，并标 `(user)`。
8. 实时预览加批注回改。
9. split 模式：规划和绘制分开在两个会话里做，适合大稿。
10. Edit Native PPTX：直接填原模板。
11. Create Template 的 mirror 方式：把原稿页面原样做成可复用的原型。
12. `visual_style: custom`：组合多个视觉风格。

---

## 8. 每个角色的硬规则（容易和我们的做法冲突）

- **页面 SVG 由主代理亲手写**，不交给子代理，也不交给生成器，为的是跨页连贯（`executor-base.md:278`）。我们的 fork 并行写页违反这一条，当时是用户同意的例外。
- **不为装下内容删减文字**：先扩大区域、重新排版、换表达方式（`executor-base.md:275`）。
- **列表只用于真正并列的项**："只是好排版"不构成理由（`executor-base.md:231`）。
- **强调色只用在关键数字或关键词上**，用 60-30-10 的配色比例（`executor-base.md:118-119`）。
- **分隔方式从轻到重依次是**：空白 → 线 / 括号 → 浅底 → 描边 → 面板 → 浮起（`shared-standards-core.md:253`）。这也是 ppt-master 的默认取向：结构先靠线。

---

## 9. 逐项对照 Sam-PPT-MBB

| Sam-PPT-MBB 的东西 | 对应的 ppt-master 能力 | 判断 |
|---|---|---|
| 按 Quick 模式执行 | Default 模式的策划层 | **用错了路线**：拿掉了最关键的一层 |
| `plan.md` 规划短表（构图编号、主图、分栏、焦点） | design_spec 第 IX 节（Relationships、Composition、Audience move）和 spec_lock 的 page_rhythm | 重复，而且更弱 |
| `rules.md` 第二部分、`page-patterns.md`、`quick-card.md` | executor-base 的元件、结构和配方，native-shape 的构图视角，plan-core 的节奏 | 大部分重复；"深色只一处"之类的条款与载体回执冲突 |
| `components.py` 版面检查（深色栏头、浅底面积、红色数量、英雄数字的上限） | 终检、载体回执、几何签名、visual-review 的 S5 / S7 / S8 / S10 | **冲突**：只设上限、不设下限，方向和 ppt-master 相反 |
| `<!--MAIN-->` 标记、雷同骨架比对 | 几何签名、全稿节奏检查 | 重复 |
| `put` 的 P 标记批量展开 | `preset_shape_svg.py render-batch` | 包了一层外壳，可以保留，也可以直接用原工具 |
| `put` 的 C / T 标记（胶囊、窄标签、编号圆、折行文字） | `text_measure.py wrap/box` | 部分重复 |
| `measure`、字号校准表 | `text_measure.py measure/calibrate` | 重复 |
| `preview` 截图和单页检查 | `svg_editor --live`、`visual_review.py`、`svg_quality_checker --stage page --page` | 重复 |
| `recolor.py`（纯蓝换色） | `update_spec.py` | Quick 下没有 spec_lock、用不了，所以我们只好自己写；**改用 Default 后可以直接用** |
| `compositions/` 57 个构图加 `comp` 命令 | Create Template 的 mirror Deck（原型页带母版和版式），或 Edit Native 直接用原稿页 | 自己造的简化版，而且拆不开、套不进页框，正是因为没走正规路线 |
| `kit.md` 线条构件 L01–L12 | 元件菜单、outline carrier、括号 / 大括号预设 | 重复 |
| `style_guard.py`、锁定哈希、pre-commit 钩子 | spec_lock（单次运行内）；跨运行保护模板文件不在 ppt-master 的职责内 | **ppt-master 没有，保留**；但只保护模板和 Style 文件，不应再锁页面写法 |
| 运行目录、计时、`finish` 里的 PowerPoint 渲染、contact 总览图 | 导出报告、`pptx_delivery_check` | 运行目录和 PowerPoint 实渲染是 ppt-master 没有的，保留 |
| `fix_cjk_fonts.py`（OPPOSans 中文字体修复） | 不处理，OPPOSans 会被提示为不可移植字体 | ppt-master 没有，保留 |
| 子代理并行写页 | 主代理亲手写全部页 | 和 ppt-master 的硬规则冲突（用户批准过的例外） |
| Deck `sam-mbb`（7 个页框）和 Style `rnb-line-whitepaper` | Create Template 的产物 | 本身是正规路线；问题在于 Deck 只有页框、没有正文原型页 |

---

## 10. 由此可选的三条路线（只做分析，不做修改）

**路线 A：Generate Default，沿用现有 Deck 和 Style。**
- 改动最小：Skill 只负责装模板、调用 Default、换色（用 `update_spec.py`）、修字体、渲染。
- 每次运行要过两轮确认；如果想全自动，需要用户事先授权"由代理代为确认"（ppt-master 支持这种授权，`generate-pptx.md:130`）。
- 风险：Style 里"深色至多一处成块"这句话还在，可能仍然偏素。

**路线 B：重做 Deck，用 mirror 方式把 R&B 的正文页也做进去，再走 Default。**
- 用 Create Template 的 mirror 方式，把 R&B 里代表性的正文页（p60–103 的若干种论证形态）做成带母版的原型页。
- 策划规划时选 `template_reuse_scope: layout`，按页挑原型；绘制时沿用母版和版式、重写内容。
- 这样就取代了我们手造的构图库。

**路线 C：Edit Native PPTX，直接拿 R&B.pptx 当页面库。**
- 按每页内容的论证形态（主论点、先导语后细节、比较、递进、指标行、密集说明）挑原稿页，填入新内容。未改的对象原生还原，所以 R&B 的视觉 100% 保真。
- 这是 ppt-master 官方给"填一份现成模板、保留其设计"指定的路线。
- 限制：页面结构受原稿限制，内容要削足适履时得换页，或者删内容（它的规则是"宁可删内容或换页，也不硬塞"）；不走 Generate 的策划和检查流程。

**建议的验证方式**：用同一份 S11 大纲（适度删减的副本），在隔离会话里先跑路线 C 和路线 A 各一次，和上一版、R&B 原稿对比；路线 B 工作量最大，放在 A、C 的结果出来之后再定。

---

## 11. 这份地图的覆盖边界

- 说明文档全部通读过。脚本只读了文档字符串和命令行参数，没有逐行读实现，也没有运行。
- 45 张对比用的 WebP 图只看过 5 张；声音素材表只读了前 60 行，其余是编号清单。
- 以上结论都来自文档；ppt-master 实际跑出来的效果，要靠第 10 节的实验验证。
