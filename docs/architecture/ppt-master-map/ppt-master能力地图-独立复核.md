# ppt-master 6.7.2 能力地图（独立复核版）与差异评判

复核时间：2026-10-26
复核对象：`C:\Users\fanrh\.claude\plugins\cache\ppt-master\ppt-master\cc8b722a24e9-32c1cf49\ppt-master\`（v6.7.2，commit `cc8b722a24e9fb540e67c2d58a9ea3da534cd682`）
对照对象：`ppt-master能力地图.md`（2026-10-26，作者同目录 A–E 五份分册）

---

## 0. 复核方法与口径

| 项 | 说明 |
|---|---|
| 已通读 | `SKILL.md`；`workflows/` 全部 23 篇（含 routing、index、3 路线、3 profile、10 个 stage、4 个 create-template 子流程、governance）；`references/` 核心 25 篇（executor-base、shared-standards-core、executor-structured、executor-structure、native-shape-authoring、visual-review、canvas-formats、modes/_index、visual-styles/_index、animations、preset-shape-vocabulary 等）；`templates/` 索引与 3 份关键 design_spec（mbb-consulting、report_core、styles/README）；`scripts/README.md`、`scripts/docs/` 目录、`attribution_guard.py`、`image_gen.py`、`docs/native-data.md` |
| 全部计数 | 用 `find`/`ls`/`json` 实测，不取文档自述 |
| 未做 | 未运行任何脚本；未逐行读 303 个 `.py`；45 张 WebP 未看；未读 `references/ai-image-comparison` 的画面内容 |
| 判定口径 | 「✓ 属实」＝原文有直接依据；「≈ 口径偏差」＝方向对但数字/条件不准；「✗ 无据」＝原文查不到；「＋ 遗漏」＝原文未覆盖 |

---

## 1. 能力地图（七层）

### L0 定位与入口纪律

- 形态：Claude Code 插件（marketplace 安装），非普通 skill 目录；版本 6.7.2，MIT，仓库 `hugohe3/ppt-master`。
- **入口硬门（原地图完全未提）**：`SKILL.md` 第 2 步强制运行 `scripts/attribution_guard.py`，非 0 立即停止，且明文禁止"检查、修复或绕过"。守卫校验四项：① `SKILL.md` frontmatter 里 `copyright` / `license` / `official_repository` 必须逐字匹配、`sponsors` 字段必须存在、gate 标记行必须恰好出现 1 次；② `LICENSE` 的 sha256 必须等于固定摘要；③ `LICENSE`、`SPONSORS.md`、`SPONSORS_CN.md` 必须存在；④ 9 个 gate 脚本（`project_manager.py`、`svg_quality_checker.py`、`svg_to_pptx.py`、`svg_to_pptx/pptx_package/cli.py`、`register_template.py`、`template_preview_pptx.py` 等）与 `console_encoding.py` 必须保持 AST 级的 `require_skill_integrity()` 调用。
- 路径纪律：`${SKILL_DIR}` 为绝对锚点，禁止 `cd`、禁 CWD、禁猜测路径。
- 加载纪律：只读"被路由选中的那一份运行时权威"，不预读其他路线；支持文档永远不构成第四条路线。
- 全局执行纪律 7 条：串行、`⛔ BLOCKING` 即停、不跨阶段打包、入口先验收、不投机执行、确定性路由（不额外问"走哪条路"）、**在拥有该缺陷的最浅层修复**。

### L1 路线矩阵（3 条顶层路线 / 4 个 profile）

| 路线或档案 | 步骤 | 产物 | 关键约束 |
|---|---|---|---|
| **Generate · Default** | 7 步：素材→建项目→模板候选→策划+两轮确认→图片→绘制→收尾导出 | `design_spec.md`(I–X)、`spec_lock.md`、`svg_output/`、`exports/*.pptx` | 两轮 BLOCKING；支持显式委托代确认；支持 `split` 跨会话 |
| Generate · Quick | §1–§4，一次跑完 | 无 spec/lock/确认；`svg_output/`、PPTX | 只减交互与可追溯性，不减能力；生图耗尽走 no-AI replan |
| Generate · Beautify | 1:1 重设计 | PPTX | 保文字/页数/顺序；Quick 仅在明确"要快"时挂 |
| Generate · Image to PPTX | Quick 子集 | 分层可编辑 PPTX | **仅 Codex**；flat 输出；永不装模板 |
| **Create Template** | 8 步（含确认门 + 原型复核 + review PPTX + 注册） | 工作区（Brand/Style/Layout/Deck 四选一） | 3 策略 `standard`/`fidelity`/`mirror`；scope `library`/`project` |
| **Edit Native PPTX** | 8 节 | round-trip 工作区、`page_plan.json`、新 PPTX | 未改页 byte-for-byte；四类回执 passthrough/cloned_passthrough/patched/rebuilt |

### L2 策划层（Default 独有，本包最重的一层）

- 规划核心批次：`strategist.md`、`plan-core.md`、`canvas-formats.md`，按条件追加 `strategist-template.md`（装了模板）、`video-design.md`（录播/自运行/视频）。
- 能力地图批次（只做"能力可见"，不做清单）：`strategist-image.md`、`modes/_index`、`visual-styles/_index`、`image-renderings/_index`、icons README、`chart-vocabulary`、`table-vocabulary`。
- Stage 1 确认"沟通契约 + 免费设计/模板"二选一；Stage 2 确认"完整方案 + 制作机制"；`refine_spec` 可插第三门；`confirm_ui/server.py` 提供浏览器确认页，聊天分支等价。
- `design_spec.md` 十节：I 项目信息（含 Template Application / 生产三开关）/ II 画布 / III 视觉主题 / IV 字体系统 / V 布局原则 / VI 图标 / VII 可视化清单 / VIII 图片资源清单 / IX 内容大纲（逐页 Core message、Audience move、**Relationships**、Composition、Native-ready、Motion suggestion）/ X 讲稿要求。
- `spec_lock.md`：配色/字体/图标/间距锚点、`page_rhythm`（anchor/dense/breathing）、`pptx_structure`（masters/layouts/page_layouts）、`page_visualizations`、`forbidden`、`typography` 角色。
- 三套 Stage-2 方案 → 全稿节奏检查、封面/结尾冲击检查；`(binding)` 标记把任意字段升级为硬约束。

### L3 绘制层

- **每页 9 步决策链**（executor-base §2.2）：沟通轨迹→阅读模式→拓扑判定→节奏→载体组合→模块行→构图→几何移动→坐标。
- 阅读模式 3 档：`text` / `balanced` / `presentation`；注册画布 **8 种**：`ppt169` `ppt43` `xiaohongshu` `moments` `story` `wechat` `banner` `a4`，每种带字号起点表（`ppt169` + `text` 起始 20 px，`balanced` 24，`presentation` 32）。
- 叙事模式 5 种：`pyramid` / `narrative` / `instructional` / `showcase` / `briefing` + `custom`。
- 视觉风格 **18 种**：blueprint、brutalist、chalkboard、dark-tech、data-journalism、editorial、glassmorphism、ink-notes、ink-wash、memphis、paper-cut、photo-editorial、pixel-art、sketch-notes、soft-rounded、swiss-minimal、vintage-poster、zine + `custom`。
- 表达语汇：6 类文字特征元素；**18 个日常元件**；7 类关系结构（含 3:7 / 2:8）；**187 个 Office 预设形状** + `shape_boolean_svg.py` 布尔合并；freeform 仅末位；6 个构图透镜（page field / outline carrier / nested fields / continuity / depth / deck language）；跨页母题。
- 技术契约：一段一 `<text>`；每个逻辑单元 `data-pptx-bounds`；`data-pptx-page-role`（cover/toc/section/content/ending）；**shape-first**（导出幻灯片的所有可见内容必须存在于页面 SVG）；`pptx_structure.mode` = `flat`（全 Slide-local）或 `structured`（声明 Master/Layout/slot）；**模板字号永不继承**，一律取 lock 的字体角色。

### L4 质检门（按执行顺序）

| 门 | 性质 | 内容 |
|---|---|---|
| `attribution_guard.py` | 每次入口必过 | 见 L0 |
| 策划一致性 + `project_manager.py validate` | Default 必做 | final 态→spec→lock 三段一致 |
| `svg_quality_checker.py --stage early` | P05 后；**roster ≤6 页跳过**；Quick 为 ≤6 页跳过、≥7 页才跑 | 越界、溢出（≤5% 警告、>5% 报错）、根组重叠（>1px 报错）、禁用元素、字号档位漂移、图片授权 |
| `svg_quality_checker.py --stage final` | 必做；导出靠指纹绑定，缺失/过期拒绝导出 | 同上 + 结构化模板警告 |
| **载体回执复核** | 必做 | 预设形状/行内强调/渐变/图标为零或与关系页数量不符时，**必须逐条写理由**；"风格、速度、克制、够用了"明确不算理由 |
| 几何签名 + 全稿节奏 | 必做（上下文内，无产物） | 逐页保留 `页面任务→构图动作→轮廓/边缘语言` 与上一页比对 |
| `verify-charts` | 有数据图表必做 | 坐标与编码 |
| `visual-review` | **仅用户明说** | 硬项 H1–H4、H6–H9（**H5 已废弃划掉**，标注由 checker 接管）+ 软项 S1–S10 |
| `pptx_delivery_check.py` | 可选 | 字体可移植性、媒体体积 |

### L5 资产库（实测条目数）

| 类 | 数量 | 说明 |
|---|---|---|
| `templates/brands/` | **21** 个 | accenture、alibaba、anthropic、aws、bain、bcg、deloitte、google、huawei、ibm、jpmorgan、mckinsey、microsoft、nvidia、pwc、tencent、xiaomi、zcare-rescue、中国电信、中国电建、中汽研 |
| `templates/styles/` | **14** 个 | 含 mbb-consulting、consulting-decision、operating-review、investor-pitch、academic-research、technical-deepdive、incident-postmortem、duty-manual、workshop-teaching、science-explainer、solution-proposal、product-launch、creative-pitch、narrative-keynote |
| `templates/layouts/` | **7** 个 | report_core（2 Master / 13 Layout）、presentation_core、presentation_core_43、editorial_bleed、story_vertical、moments_square、xiaohongshu_post |
| `templates/decks/` | **2** 个 | 中国电信、中汽研 |
| `templates/charts/` | **33** 个 SVG | 另有 6 个 `templates/tables/` 表模板 |
| `templates/icons/` | **5 库 / 12,027 SVG** | chunk-filled、phosphor-duotone、simple-icons、tabler-filled、tabler-outline |
| `templates/sounds/` | 3 库 + 词表 252 行 | kenney-interface、kenney-ui、bigsoundbank |
| `templates/schemas/` | 2 个 JSON Schema | design_spec、spec_lock |

优先级（`apply-template-workspace` §5.1）：身份 Brand > Deck；结构 Layout > Deck；方法 Style 永不拥有身份、结构或配色真值。复用范围 `mirror` / `layout` / `style`，贴合度 `strict` / `adaptive`。

### L6 图像与音视频

- 生图：**15 个后端**（gemini、openai、minimax、stability、bfl、ideogram、qwen、zhipu、volcengine、tencent、modelscope、siliconflow、fal、replicate、openrouter）+ `host-native` 路径；三路径模型 `api` / `host-native` / `manual`。
- 图像语汇：21 个 renderings、12 个 type-templates、14 个 palettes（文档注明 palettes 为 legacy 兼容）、45 张 WebP 对比图。
- 网图：`image_search.py` + `web-image-review` 阶段（有视觉上下文才开候选评审）+ 版权/署名落 `image_sources.json`。
- 切图：chroma-key 网格切图，`--strict-alpha` 失败即回退准备阶段；`image_treat.py` 做模糊/去色/双色调/缩放。
- 配音：4 家带时间戳（Edge / ElevenLabs / MiniMax / CosyVoice），Qwen 仅音频；`notes_to_audio.py` → `narration_sync.py` → `powerpoint_video.py` → `video_sound_mix.py` / `video_subtitles.py`。
- 动画：**48 个切换键** + **203 个对象动画预设** + Morph 强制配对 + 音效（选在动效定稿之后）。

### L7 导出、往返与工具面

- 导出：`svg_to_pptx.py`（flat/structured、`--native-charts-and-tables`、讲稿、`animations.json`、`--quick-generate`、`--roundtrip`）；`finalize_svg.py`（Quick 禁用）；postflight 回执。
- 往返：`pptx_to_svg.py --roundtrip` 生成 `authoring-svg-flat/` + `native-payloads/`；source proxy 为原子对象（SmartArt/复杂效果/媒体帧）；`--adopt-object` 合并页；四类页回执。
- 规模：顶层可执行脚本 **81 个**，`scripts/` 下共 **303 个 `.py`**，`scripts/docs/` **22 篇**；3 个本地 GUI 服务（confirm_ui、spec_review、svg_editor --live）。

### L8 治理与可维护

`failure-recovery.md`（失败恢复指针与 stop/continue 策略）、`artifact-ownership.md`（事实通道与产物边界）、`prompt_audit.py` + `prompt_audit_manifest.json`（维护者提示预算审计）、`workflows/index.md`（维护者注册表，运行时不加载）、`tests/`。

---

## 2. 与原地图的逐项评判

### 2.1 总体结论

原地图**结构与判断基本正确，准确度高于一般"通读笔记"**：三条路线的识别、Default/Quick 的差异本质（"整层策划被拿掉"）、载体回执"反对素"这一条、模板四类的职责切分、Edit Native 作为"填现成模板"的正规路线——这些判断我都独立验证成立，且引用的行号绝大多数对得上。

问题集中在四类，按严重度排序：

1. **三个能力块整块缺位**（影响后续决策，最严重）：完整性守卫 `attribution_guard`、`pptx_structure` 语义结构契约、图像生成矩阵。
2. **个别数字无据**：最典型是"33 种参考图，其中 23 种可导出为原生可编辑图表"。
3. **数量口径偏差**：`references 110` / `workflows 24` / `约 60 个脚本`。
4. **过度概括导致的条件丢失**：早检的页数门槛、Quick 仍有强制 anchors。

### 2.2 事实核验表（我逐条验的 24 项）

| # | 原地图说法 | 实测 | 判定 |
|---|---|---|---|
| 1 | 三条顶层路线，Edit Native 是"填现成模板"的正规路线 | routing.md §2 + edit-native-pptx §1 均为该定位 | ✓ |
| 2 | Quick 拿掉了策划层（无 spec/lock/确认） | quick-generate §1 明文：无 root design_spec/spec_lock、无 Confirm UI | ✓ |
| 3 | Default 两轮确认，可事先授权代确认 | generate-pptx.md:128–130 | ✓ |
| 4 | design_spec 第 I–X 节，IX 逐页含 Relationships/Composition/Audience move | design_spec_reference 结构 | ✓ |
| 5 | spec_lock 锁配色、字体档位、图标库、page_rhythm、页面结构 | spec_lock_reference §2–3 | ✓ |
| 6 | 每页 9 步决策、几何签名、五页重读 lock | executor-base §2.2；generate-pptx Step 6 | ✓ |
| 7 | 载体回执"克制/风格/速度不算理由" | executor-base.md:296–305 逐字 | ✓ |
| 8 | 第 5 页后跑一次早检 | 实际有门槛：Default roster ≤6 页跳过；Quick 需 ≥7 页 | ≈ 条件丢失 |
| 9 | 187 个 Office 预设形状 | preset-shape-vocabulary.md 开头自述 187 | ✓ |
| 10 | 18 种常用版面元件 / 7 种关系结构 | executor-base 表格 18 行 / 7 行 | ✓ |
| 11 | 33 种图表参考、6 种表格 | charts 33 SVG / tables 6 SVG | ✓ |
| 12 | **其中 23 种可导出为原生可编辑图表** | 全局搜不到 "23"；`native-data.md:41` 的支持清单是 **22 个类型名**，且明文 `heatmap` / `bullet` / `gantt` / `map` 不支持 | ✗ 无据 |
| 13 | 48 种切换、203 种对象动画 | animations.md:160、:217 逐字 | ✓ |
| 14 | 15 个生图后端 | image_gen.py docstring 列 15 个 | ✓ |
| 15 | 5 个图标库共 1.2 万图标 | 实测 5 库 / 12,027 个 SVG | ✓ |
| 16 | 阅读方式 text 正文起始 20 px | canvas-formats.md §Typography Scale Start：`ppt169`+`text` 起始 20（区间 18–21） | ✓ |
| 17 | 模板字号不被继承 | executor-structured.md:24–25 "font size is skin, not geometry" | ✓ |
| 18 | 身份 Brand>Deck、结构 Layout>Deck、Style 只管方法 | apply-template-workspace.md §5.1 | ✓ |
| 19 | mirror/layout/style + strict/adaptive | strategist-template.md:25–31 | ✓ |
| 20 | 页面 SVG 必须主代理亲手写 | executor-base.md:278 | ✓ |
| 21 | 强调色只用于关键数字，60-30-10 | executor-base.md:118–119 | ✓ |
| 22 | 分隔从轻到重：空白→线/括号→浅底→描边→面板→浮起 | shared-standards-core "Boundary strength" 行 | ✓ |
| 23 | 溢出超过 5% 报错、无阈值可调 | checker.py `_BOUNDS_OVERFLOW_ERROR_RATIO = 0.05`；≤5% 警告、>5% 报错；无用户可调阈值 | ✓ |
| 24 | visual-review 硬项 H1–H9 | H5 已划掉（"covered by svg_quality_checker"），实际生效 8 项；S1–S10 齐 | ≈ 细节 |

### 2.3 数量口径偏差

| 项 | 原地图 | 实测 | 偏差性质 |
|---|---|---|---|
| `references/` 文件数 | 110 | **117** 个 `.md`（其中 106 个非 `_` 开头） | 对不上任何一种口径 |
| `workflows/` 文件数 | 24 | **23** 个 `.md` | 多算 1 |
| `scripts/docs/` | 22 | 22 | 一致 |
| 脚本命令行定义 | 约 60 | 顶层 **81** 个可执行脚本，全部 **303** 个 `.py` | 明显少算 |
| 45 张 WebP | 45 | 45 | 一致 |

### 2.4 遗漏清单（按对我们项目的实际影响排序）

| # | 遗漏 | 实际内容 | 影响 |
|---|---|---|---|
| 1 | **`attribution_guard.py` 完整性守卫** | 每次进入技能即校验 SKILL.md metadata、LICENSE 摘要、gate 标记唯一性、9 个 gate 脚本的 AST 调用；失败即停、禁止绕过 | 直接影响"改造/魔改"方案：改 `SKILL.md` 的版权头部、`LICENSE`、或重写 `project_manager.py`/`svg_quality_checker.py`/`svg_to_pptx.py`/`register_template.py`/`template_preview_pptx.py`/`console_encoding.py` 会让整个技能在入口直接失败，且不是"警告"而是"拒绝启动"。改 `templates/`、`references/`、自有 Deck/Style 不受影响 |
| 2 | **`pptx_structure` 语义结构契约** | `flat` vs `structured`；`data-pptx-layer` / `data-pptx-placeholder` / `data-pptx-page-role` / `data-pptx-bounds` / `data-pptx-morph-staging` 的语义与边界；`semantic-svg.md`、`pptx-structure-interface.md`、`executor-structured.md` | 这正是"Deck 只有页框、没有正文原型页"问题的技术落点：结构不是靠"画得像"，而是靠显式声明 |
| 3 | **图像生成矩阵** | 21 renderings × 12 type-templates × 15 后端；3 路径；chroma-key 切图；45 张对比图 | 原地图 §4 一句"图片：AI 生成、网图检索、切图、图片处理"把这一大块压掉了 |
| 4 | **8 个注册画布 + 每画布字号起点表** | `ppt169/ppt43/xiaohongshu/moments/story/wechat/banner/a4`，各自 body 起始与区间 | 原地图 §3 提出"我们的 Style 定 14–16、官方 text 起始 20"的冲突，根因就在这张表，但没引到 |
| 5 | **5 个 mode 全谱、18 个视觉风格全谱** | 只提了 `pyramid` 一个 mode、3 个 style | 会低估"briefing / narrative / instructional / showcase"这几种骨架的可用性 |
| 6 | **资产库真实规模** | 21 brands（含中国电信、中国电建、中汽研、阿里、华为、腾讯、小米、IBM）、14 styles、7 layouts、2 decks | 只报了 6 brands / 2 styles / 1 layout / 0 decks |
| 7 | **Edit Native 的边界细节** | source proxy 原子性、`--adopt-object` 合并页、四类回执、`--roundtrip` 不支持改幻灯片尺寸/加结构 | 路线 C 的可行性边界全在这里，原地图只给了一句"页面结构受原稿限制" |
| 8 | **Quick 的 no-AI replan** | 生图/切图耗尽后不问路径、移除 AI 作业、用原生文字/SVG 顶上继续 | 直接影响"全自动流水线"能不能不中断 |
| 9 | **治理层** | `failure-recovery`、`artifact-ownership`、`prompt_audit`、`workflows/index.md`、`tests` | 影响二次开发的成本判断 |
| 10 | **音视频链的供应商差异** | 4 家带时间戳、Qwen 无时间戳；SRT；`powerpoint_video.py` 需 Windows PowerPoint 2016+；MP4 混音需 ffmpeg+numpy | 原地图只写"配音和视频" |

### 2.5 表述可商榷处

| 位置 | 原文 | 问题 |
|---|---|---|
| §2 末 | "Quick 只能边画边想" | 过头。Quick 仍强制 §2 的 transient anchors：冻结 roster、逐页核心信息、Relationships、按角色字号校准、全稿节奏检查——只是不落盘、不确认。准确说法是"Quick 保留规划判断，但取消规划产物与交互" |
| §2 第 6 行 | "第 5 页后跑一次早检" | 丢了门槛：≤6 页的 roster 不跑早检 |
| §5 | "没有可调的阈值或开关" | 判定阈值确实不可调，但 checker 有 `--stage early/page/final`、`--slot-capacity-report`、`--template-mode`、`--roundtrip` 等模式开关。"没有任何开关"会被误读成"无法分级检查" |
| §4 | "23 种可导出为原生可编辑图表" | 无据（见 2.2 #12）。准确说法：原生图表支持 22 个类型名（含变体），`heatmap/bullet/gantt/map` 明确不支持；且"选了模板 ≠ 能用原生"，还要 §IX 标 `Native-ready` + 导出加 `--native-charts-and-tables` |
| §9 | 逐项对照 Sam-PPT-MBB | 依赖我们项目内部事实（`components.py`、`plan.md`、`kit.md` 等），我无法独立复核。个别方向性判断我认可：`components.py` "只设上限不设下限" 与载体回执"缺省须写理由"确实反向 |

### 2.6 一处应当强调、原地图只轻描的机制

**导出与质检报告是哈希指纹绑定**：`svg_to_pptx.py` 必须读到与当前 `svg_output/` 匹配的 `final` 报告，缺失/过期/非 final/blocking 一律拒绝导出。这意味着"先导出、后补检查"这条路在 ppt-master 里根本不存在——对流程设计（尤其自动化流水线）是关键约束，原地图 §5 只写了"没有终检报告就拒绝导出"，没有点明"指纹绑定、过期也拒"。

---

## 3. 结论

| 维度 | 评分（主观，供参考） | 理由 |
|---|---|---|
| 结构完整性 | 高 | 路线、模板体系、绘制工具箱、质检门、工具清单、默认关闭项六个切面都切对了 |
| 事实准确率 | 中高 | 24 项抽验中 21 项完全属实、2 项条件或细节有偏差（早检门槛、H5 已废弃）、1 项无据（原生图表 23 种） |
| 数字可靠性 | 中 | 5 个计数里 2 个对、3 个错（含 1 个无据） |
| 决策可用性 | 高 | §9 对照与 §10 三条路线的判断，方向正确、可直接落地 |
| 覆盖盲区 | 中 | 缺 attribution_guard 与结构契约两块，都是"会踩坑"级别 |

**一句话**：这份地图可以直接作为工作文档用，但三处必须补：① 入口有完整性守卫，改代码前先确认不会踩；② 原生图表不是 23 种，条件也不止"选模板"；③ 计数口径按实测修正（117 / 23 / 81）。其余判断我未发现方向性错误。

### 若要修订原文件，建议只动 6 处

1. §0/§1 增加一段"入口完整性守卫"，并说明可改/不可改的文件范围。
2. §2 第 6 行补早检门槛（≤6 页跳过）。
3. §2 末句改为"Quick 保留规划判断，取消规划产物与交互"。
4. §4 把"23 种原生"改为"22 个类型名，heatmap/bullet/gantt/map 不支持"，并强调双条件。
5. §5 补"导出与 final 报告哈希指纹绑定"。
6. §6 的计数改为 117 / 23 / 81（顶层）/ 303（全部）。
