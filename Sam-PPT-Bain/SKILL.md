---
name: Sam-PPT-Bain
description: 把用户给的 PPT 大纲按 参考模板 模板的贝恩 / 咨询白皮书风格（海军蓝 + 砖红、OPPOSans、论点条 + 区块标签 + 主图两翼 + 证据框 + 框架条）直接生成可编辑 PPTX。用户给出大纲要求做成 PPT、提到 Sam-PPT-Bain、贝恩风格、参考模板 模板、咨询白皮书风格时使用。每次运行输出到独立的 runs/run-yyyymmdd-hhmmss-fff 目录，并用 PowerPoint 渲染自检。不负责写大纲。
---

# Sam-PPT-Bain：大纲 → 咨询风格可编辑 PPTX

本 Skill 把一份现成的大纲排成与 参考模板 模板同一风格的 PPTX。所有元素都是原生对象：文字可改、图表右键"编辑数据"、表格是原生表格、图示是原生形状。

风格不靠记忆复刻，而是写死在代码和规则里：
- `scripts/samppt/tokens.py`：从模板实测的颜色、字号、页面网格（内容左右边界 0.37″ / 12.96″）。
- `scripts/samppt/components.py`：论点条、区块标签、证据框、框架条、标注气泡等组件，组件内部负责对齐。
- `scripts/samppt/layouts/`：20 种版式原型，输入是数据，不手调坐标。
- `assets/kit.pptx`：从模板裁出的母版、页头页脚、图标和图片。
- `references/design-rules.md`：所有设计规则和踩过的坑。**生成前必读。**

`SKILL_DIR` = 本文件所在目录。

## 环境要求

- Windows + Microsoft PowerPoint（渲染自检用；它是唯一能证明文件"真的能打开"的渲染器）。
- Python 3.10+，包：`python-pptx`、`lxml`、`Pillow`。缺包时 `pip install python-pptx lxml pillow`。
- 字体 OPPOSans（H/B/M/R/L）。用户电脑没有时，提醒用户安装，否则 PowerPoint 会替换字体、版面变形。

## 工作流

### 1. 读规则和版式目录
先读 `references/design-rules.md` 和 `references/layouts.md`。

### 2. 规划每一页（写 deck.json 之前，先在回复里列出页面计划）
- 大纲写了"建议呈现"就照做，否则按 `layouts.md` 的"适用场景"选版式。
- **标题写成结论句**；每页再提炼一句**论点条**（`thesis`，只在咨询版式上显示），与标题互补、不重复。
- **不替大纲加词**：可以拆句、换行、提炼标签，但不能添加大纲没有的事实或修饰。
- 推算出来的数字（同比、份额、差值、转化率、均分、倍数）可以用来提高信息密度，但必须由大纲原始数据算出，并在交付时逐条列给用户核实。
- 每种版式都有**容量上限**（见 `layouts.md`）。超出时拆页或精简，不要硬塞。
- 同一版式不要连续出现超过两次；图表页和图示页交替。

### 3. 写 deck.json
放在本次运行目录里（见第 4 步）或任意位置。格式：

```json
{
  "meta": {"title": "报告名（也是文件名）", "org": "机构", "sign": "页脚右下署名", "disclaimer": "页脚左下免责声明"},
  "slides": [ {"layout": "cover", ...}, {"layout": "funnel", "title": "...", "section": "03 消费者洞察", ...} ]
}
```

- 每页通用字段：`layout`、`title`（结论标题）、`section`（右上章节标签）、`speaker_notes`（演讲者备注，可选）。
- 文字里用 `**文字**` 标重点：浅色背景上显示为砖红加粗，深色论点条上显示为浅珊瑚色粗体。每页重点不超过 3 处。
- 完整示例：`examples/nev-report.json`（20 页，覆盖全部版式）、`examples/consulting-samples.json`（3 张咨询版式样张）。

### 4. 生成（每次运行一个独立目录）

```bash
python "$SKILL_DIR/scripts/build.py" deck.json
```

自动创建 `$SKILL_DIR/runs/run-yyyymmdd-hhmmss-fff/`，内含：
- `deck.json`：本次输入的副本
- `<title>.pptx`：生成的文件
- `render/slide-NN.png`：PowerPoint 渲染图
- `contact.png`：全部页面的缩略总览
- `qa.md`：自动检查结果

修改后重建到同一目录：`python build.py deck.json --run <该目录>`。

### 5. 自检（必做，直到干净）
1. 看 `qa.md`：越界、文字溢出、字号过小、图表 XML 缺陷，**必须清零**。
2. 渲染失败（PowerPoint 打不开）= 文件损坏，必须修好再交付；格式校验通过不代表 PowerPoint 能打开。
3. 先看 `contact.png` 整体节奏，再逐页放大看 `render/`，按 `references/qa-checklist.md` 检查。
4. 问题优先改 deck.json（精简文字、拆页、换版式）；只有版式本身有缺陷时才改代码，改完要用 `examples/` 回归。

### 6. 交付
给出 PPTX 路径和运行目录，说明页数、用了哪些版式，并**列出所有推算数字**让用户核实。

## 扩展与维护

- 新增版式：在 `scripts/samppt/layouts/` 的模块里写函数并加入该模块的 `LAYOUTS`，只用 `tokens` 常量和 `components` 组件；坐标以 `EL/ER/CW` 和 `cols()` 推算，不写散落的边距数字。然后在 `references/layouts.md` 补一节，在 `examples/` 加一页，跑一次回归。
- 回归：改动组件或版式后，重跑两个 example，与上一次的渲染图对比（未变动的页面应几乎无像素差）。
- 换模板素材：`python scripts/make_kit.py <参考模板> assets/kit.pptx`（图标、图片清单在脚本顶部）。
