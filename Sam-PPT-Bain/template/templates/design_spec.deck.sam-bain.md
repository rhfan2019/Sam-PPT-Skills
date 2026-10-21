---
deck_id: sam-bain
kind: deck
category: general
summary: 中文咨询白皮书 / 行业研究报告的结论先行内容页，海军蓝 + 砖红，帮助管理层快速读懂判断与证据并形成决策。
keywords: [咨询, 白皮书, 行业研究, 蓝红, 结论先行]
primary_color: "#1C4274"
canvas_format: ppt169
canvas_width: 1280
canvas_height: 720
canvas_viewbox: "0 0 1280 720"
source_canvas_width: 1280
source_canvas_height: 720
source_viewbox: "0 0 1280 720"
replication_mode: standard
native_structure_mode: structured
page_count: 6
page_types: [cover, toc, chapter, content, ending]
placeholders:
  01_cover: ["{{COVER_TAG}}", "{{TITLE}}", "{{SUBTITLE}}", "{{AUTHOR}}", "{{DATE}}"]
  02_toc: ["{{PAGE_TITLE}}", "{{SECTION_NAME}}", "{{SOURCE}}", "{{AUTHOR}}", "{{TOC_ITEM_1_TITLE}}", "{{TOC_ITEM_1_DESC}}", "{{TOC_ITEM_2_TITLE}}", "{{TOC_ITEM_2_DESC}}", "{{TOC_ITEM_3_TITLE}}", "{{TOC_ITEM_3_DESC}}"]
  03_chapter: ["{{CHAPTER_NUM}}", "{{CHAPTER_TITLE}}", "{{CHAPTER_DESC}}"]
  04a_content_frame: ["{{PAGE_TITLE}}", "{{SECTION_NAME}}", "{{SOURCE}}", "{{AUTHOR}}"]
  04b_content_thesis: ["{{PAGE_TITLE}}", "{{SECTION_NAME}}", "{{KEY_MESSAGE}}", "{{SOURCE}}", "{{AUTHOR}}"]
  05_ending: ["{{THANK_YOU}}", "{{CONTACT_INFO}}", "{{AUTHOR}}"]
---

# Sam 蓝红咨询白皮书 — Design Specification

## I. Template Overview

| Application context | Definition |
| --- | --- |
| Recurring presentation family | 中文行业研究报告、咨询白皮书、经营分析与方案汇报的正文页 |
| Intended audiences and outcomes | 面向管理层与业务决策者；让读者在一页内读到结论、看到支撑证据并据此决策 |
| Delivery and reading assumptions | 现场讲解与会后精读并重；页面信息密度高，需能脱离讲解独立阅读 |
| Representative narrative/page roles | 封面、目录、章节页、结束页，以及数据趋势与阶段诊断、转化漏斗、中心辐射生态、左右对比、矩阵、看板等正文页 |

- 白底，海军蓝为主、砖红只用于强调与"另一侧"的语义；每页顶部是"手势标记 + 结论标题 + 右上章节标签 + 贯通深蓝标题线"，底部是灰色页脚线 + 左下免责声明 + 右下署名。
- 来源 参考模板 的 80 页全部是正文页，母版与版式为空、页框逐页手绘；本模板把页框重建为真实的 Master/Layout。正文两种原型来自 参考模板；封面、章节页、结束页为同一视觉语言新设计的"深色三明治"两端：海军蓝满版 + 右侧建筑照片向左渐隐 + 砖红短横线，目录页沿用正文页框并在左侧放一幅渐隐城市照片（2026-10-21 用户确认按 ppt-master 方向全面改造后补齐，同日经用户确认为模板基线 [decision]）。

## II. Color Scheme

| Role | Color | Application |
| --- | --- | --- |
| Navy (primary) | #1C4274 | 标题、论点条、主图主色、左侧/用户侧语义 |
| Navy rule | #1D4274 | 标题下贯通分割线（来源原值） |
| Brick red (accent) | #A23424 | 强调数字、最大断点、右侧/策略侧语义、重点标签 |
| Dark navy | #0E213A | 右上章节标签、深色文字 |
| Zone blue | #C4D7F1 | 左侧区块标签底色、浅蓝标签框 |
| Zone pink | #F4D1CC | 右侧区块标签底色、浅粉标签框、证据框底色（低透明度） |
| Body text | #404040 | 正文、说明文字 |
| Muted text | #595959 | 次级标签、署名、图表标注 |
| Footer rule | #999999 | 页脚分割线 |

渐变仅在同一色相内由深到浅：海军蓝 #16365F → #2E5A94，砖红 #8E2B1D → #C0503E。红色面积不超过全页约 20%。

## III. Typography

| Role | Font stack | Application |
| --- | --- | --- |
| Page title | `OPPOSans H, Microsoft YaHei, sans-serif` | 页面结论标题，37.33 px（28 pt） |
| Labels / thesis / emphasis | `OPPOSans M, Microsoft YaHei, sans-serif` | 论点条 26.67 px、区块标签、章节标签 14.67 px、条目标题 |
| Body | `OPPOSans R, Microsoft YaHei, sans-serif` | 正文与说明，约 12.7–14 px（9.5–10.5 pt） |
| Bold numbers | `OPPOSans B, Microsoft YaHei, sans-serif` | 指标数字、百分比 |
| Fine print | `OPPOSans L, Microsoft YaHei, sans-serif` | 页脚免责声明 8 px |

OPPOSans 系列为非系统预装字体，用户已确认在交付机器上安装（[decision]）；PowerPoint 不嵌入字体，未安装时回退微软雅黑。

## IV. Signature Design Elements

- **页框（白底版式共用，每页一致）**：手势标记 (28.07, 22.37, 49.37 方)；标题线 x 35.93→1244.07、y 82.51、3 px #1D4274；页脚线 y 687.01 通栏 1.33 px #999999。Master 只放白色背景，页框作为 Layout 原子写在目录与两种正文版式里，深色的封面/章节/结束页因此不带页框。
- **深色两端（封面 / 章节 / 结束）**：满版 #1C4274，照片放在右侧（封面、结束页 x 560–1280）或满版（章节页），用同色相渐变向左压暗到不透明；文字统一左对齐于 x 80，砖红短横线 72×6 作为唯一强调。
- **内容左右边界 = 标题线两端 35.93 / 1244.07 px**。任何内容元素不得越过这两条边；全宽元素（论点条、底部框架条、贯通分隔线）两端贴齐它们。
- **论点条（Layout `content_thesis`）**：标题线下 y 95.26、高 61.26 的全宽海军蓝条，白色 OPPOSans M 26.67 px 居中，写这一页的 so-what，与标题互补不重复。
- **咨询构图语法（Slide-local，由内容决定）**：区块标签（207.74×55.14，左蓝 #C4D7F1 / 右粉 #F4D1CC，24 px 文字）→ 中央主图 + 左右两翼条目 → 远端证据框（砖红虚线框 + 大数字 + 微型标签 + 升降箭头）→ 底部"A ⇄ B"框架条（两组虚线浅色框 + 双向箭头）。去卡片化：条目浮在版面上，用圆点虚线、弧形箭头、右箭头连成逻辑。
- **对齐**：同一行的标题、箭头、标签框、说明文字共用一条中线；上下相邻的列左右边缘对齐。
- **信息密度**：一条信息 = 图标圆 + 粗体标题 + 说明 + 标签框；证据框允许 10.7 px（8 pt）的单位与注释。
- **主图立体感**：漏斗/金字塔等每层左右两半深浅不同，同色相渐变。

## V. Page Roster

| File | Layout key / picker name | Role and visual character | Slots (bounds x y w h) and typography |
| --- | --- | --- | --- |
| `01_cover.svg` | `cover` / 封面 | 海军蓝满版，右侧玻璃幕墙照片向左渐隐；左侧标签 → 砖红短横线 → 大标题 → 副标题，底部细线下署名与日期 | `body` idx1 标签 80 196 640 36（OPPOSans M 18.67 #F4D1CC）；`title` 80 268 780 136（OPPOSans H 48 白，最多两行）；`subtitle` 80 424 780 40（R 21.33 #C4D7F1）；`body` idx3 署名 80 614 480 28（M 16 白）；`date` 80 646 480 26（R 14.67 #C4D7F1） |
| `02_toc.svg` | `toc` / 目录 | 正文页框 + 左侧 380 宽渐隐城市照片；右侧逐行"砖红大编号 + 章节名 + 说明 + 虚线分隔"，条目为 Slide-local，按章节数增减（3–6 行，行距随数量均分） | 与 `04a` 相同的四个 slot；条目区 463.93–1244.07 × 112–672 |
| `03_chapter.svg` | `chapter` / 章节页 | 满版城市照片 + 自左向右的海军蓝渐变压暗；超大浅蓝编号 → 砖红短横线 → 章节名 → 说明 | `body` idx1 编号 80 216 480 172（OPPOSans B 112 #C4D7F1）；`title` 80 404 1000 68（H 44 白）；`body` idx2 说明 80 486 1000 40（R 21.33 #C4D7F1） |
| `04a_content_frame.svg` | `content_frame` / 标题与自由内容 | 只有页框的正文页；标题线以下 y≈95 至页脚线 y≈680 之间、x 35.93–1244.07 的区域完全自由 | `title` 80.7 26 880 56（OPPOSans H 37.33 #1C4274，单行）；`body` idx1 章节标签 980 44 264.07 30（右对齐 OPPOSans M 14.67 #0E213A）；`footer` idx4 免责声明 35.93 690 420 15（OPPOSans L 8）；`body` idx2 署名 944.07 690 300 15（右对齐 OPPOSans M 9.33 #595959） |
| `04b_content_thesis.svg` | `content_thesis` / 标题、论点条与自由内容 | 页框 + 全宽海军蓝论点条；论点条下 y≈165 至 680 的区域自由，适合咨询构图（区块标签、主图两翼、证据框、底部框架条） | 同上四个 slot，另加 `body` idx3 论点 55.93 95.26 1168.14 61.26（白色 OPPOSans M 26.67 居中，单行约 43 个汉字；更长的原句在本页把字号降到 22.67，约 51 字） |
| `05_ending.svg` | `ending` / 结束页 | 与封面同构的深色收尾；只在大纲本身写了结束页时使用 | `title` 80 304 780 80（H 53.33 白）；`body` idx1 80 398 780 40（R 21.33 #C4D7F1）；`body` idx2 署名 80 614 480 28 |

## VI. Assets

| File | Use | Reason |
| --- | --- | --- |
| `images/hold-gesture.svg` | 白底版式左上手势标记 | 模板身份元素 |
| `images/cover-tower.jpg` | 封面、结束页右侧照片 | 来自 参考模板；行业中性的蓝色玻璃幕墙，压暗后与海军蓝融合 |
| `images/chapter-city.jpg` | 章节页满版照片 | 来自 参考模板 的城市黄昏 |
| `images/toc-city.jpg` | 目录页左侧照片 | 来自 参考模板 的城市天际线 |

未采用为模板资产：来源中的汽车、城市科技插画、门店照片与 27 个图标 —— 属于示例内容素材，放在 Skill 的 `assets/photos/` 随具体项目按需复制；图标使用 ppt-master 图标库（一页一个图标家族）。
