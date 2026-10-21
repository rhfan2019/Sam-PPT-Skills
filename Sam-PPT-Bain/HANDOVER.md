# Sam-PPT-Bain 交接文档

> 写于 2026-10-21，供新会话继续"测试 + 持续优化"这个 Skill。新会话请先读完本文，再读 `SKILL.md` 和 `references/design-rules.md`。

## 1. 一句话现状

Sam-PPT-Bain 能把一份结构化的 `deck.json` 按 参考模板 模板风格生成可编辑 PPTX，含 20 种版式、每次运行独立目录、自动检查 + PowerPoint 渲染自检 + 像素级回归。用 20 页新能源汽车测试大纲能完整跑通（自动检查 0 问题，仅说明没有越界/溢出等机械错误）。

**效果上，用户只确认了 3 页**：咨询版的 P4（chart_phases）、P13（funnel）、P17（hub）。**其余 17 页是精修卡片风格，用户明确表示未达预期**，不能当作标准参考，也不要据此推断"用户满意"。

**还没做到的**：17 种版式仍是"精修卡片风格"，只有 3 种是用户确认过的"咨询风格"；从大纲到 deck.json 这一步靠 Claude 手写，没有程序辅助。详见第 7 节待办。

## 2. 位置与约定

| 项目 | 位置 |
|---|---|
| 仓库（私有） | https://github.com/rhfan2019/Sam-PPT-Skills ，分支 `main` |
| 本地 | `D:\Workspace\Sam-PPT-Skills\Sam-PPT-Bain` |
| 已安装为个人 Skill | `C:\Users\fanrh\.claude\skills\Sam-PPT-Bain`（目录链接 → 上面的本地目录，改代码即生效） |
| 原始模板 | `参考模板`（52 MB，只在重建素材包时用） |
| 测试大纲 | `examples/outlines/nev-report-outline.md`（原件 `测试大纲`） |
| 每次运行输出 | `runs/run-yyyymmdd-hhmmss-fff/`（不提交） |
| 旧的临时脚本和成品 | 仓库根目录 `_work/`（不提交，仅供参考，**不要再从这里改代码**） |

**硬约定**（也写在仓库根目录 `CLAUDE.md`）：
- **每次有意义的修改都自动 `git commit` + `git push`**，无需再问用户。提交信息结尾带 Co-Authored-By 行。
- 每次运行输出到 `runs/run-yyyymmdd-hhmmss-fff/`，毫秒三位。
- 改了组件或版式，**必须跑回归**（第 5 节）。

## 3. 目录结构

```
Sam-PPT-Bain/
├── SKILL.md                    工作流（大纲 → 规划 → deck.json → 生成 → 自检 → 交付）
├── HANDOVER.md                 本文
├── assets/kit.pptx             素材包：母版/主题、页头页脚、27 个图标、7 张图片（2 MB，打开可读，有说明页）
├── references/
│   ├── design-rules.md         设计规则 + 14 条踩过的技术坑（最重要）
│   ├── layouts.md              20 种版式的字段与容量上限
│   └── qa-checklist.md         看渲染图的检查清单
├── examples/
│   ├── outlines/nev-report-outline.md   测试大纲（20 页）
│   ├── nev-report.json                  由该大纲写成的 deck.json（覆盖全部 20 种版式）
│   └── consulting-samples.json          用户确认过的 3 张咨询版样张（P4/P13/P17）
├── tests/baseline/             回归渲染图（960×540）；STATUS.json 标明哪些页是用户确认过的（approved），其余只是临时快照（provisional）
└── scripts/
    ├── build.py                入口：deck.json → runs/run-*/（pptx、render/、contact.png、qa.md）
    ├── regress.py              回归：重建 examples、逐像素对比；approved 页变化即失败，provisional 页变化只提示
    ├── render.ps1              用真实 PowerPoint 逐页导出 PNG
    ├── make_kit.py             从 参考模板 重建 assets/kit.pptx
    └── samppt/
        ├── tokens.py           颜色、字号、页面网格（EL=0.37 / ER=12.96 内容边界）
        ├── deck.py             Deck：页框、绘图原语、渐变/阴影/透明、图标着色、图片裁切羽化
        ├── charts.py           原生图表样式（隐藏轴、副轴折线、标签、绘图区定位…）
        ├── components.py       组件：论点条、区块标签、证据框、框架条、标注气泡、卡片、徽章…
        ├── qa.py               自动检查：越界、文字溢出估算、最小字号、图表 XML 缺陷
        └── layouts/            consult（3 咨询版式）、openers、cards、compare、misc
```

## 4. 常用命令

```bash
# 生成（自动建运行目录）
python scripts/build.py examples/nev-report.json
# 改 deck.json 后重建到同一目录
python scripts/build.py deck.json --run runs/run-xxxxxxxx-xxxxxx-xxx
# 回归（改代码后必跑）
python scripts/regress.py
python scripts/regress.py --update                       # 刷新临时快照（provisional）
python scripts/regress.py --approve nev-report:5,6         # 用户确认这些页的效果后，转为 approved
python scripts/regress.py --update-approved nev-report:4   # 用户确认了对已确认页的修改
# 重建素材包
python scripts/make_kit.py "参考模板" assets/kit.pptx
```

Bash 里跑 Python 输出中文时加 `PYTHONIOENCODING=utf8`。

## 5. 测试与回归方法

1. **端到端测试**：拿 `examples/outlines/nev-report-outline.md`（或用户给的新大纲），按 `SKILL.md` 从头走一遍——规划页面、写 deck.json、build、看 qa.md、看 contact.png 和每页渲染图。这能同时测"大纲→deck.json"的指引是否够用。
2. **自动检查**：`qa.md` 必须 0 问题；PowerPoint 渲染失败 = 文件损坏。`qa.py` 已用故意出错的样例验证过能抓住越界、溢出、过宽。
3. **视觉检查**：按 `references/qa-checklist.md`。用户最在意：对齐（同行中线、同列边缘）、不越界、信息密度、不重复、深浅对比。
4. **回归**：`regress.py` 对比 `tests/baseline/`，按 `STATUS.json` 区分两类页面：
   - **approved（已确认）**：目前只有 consulting-samples 的 1–3 页和 nev-report 的第 4、13、17 页。它们一旦变化，回归就失败。必须先把渲染图给用户看，用户确认后才能 `--update-approved <deck>:<页码>`。
   - **provisional（临时快照）**：其余 17 页。只用来发现"意外"变化，效果本身未被认可，升级时本来就该变。变化会列出来供查看，不算失败；确认是有意的改动后用 `--update` 刷新快照。
   - 用户确认了新页面的效果后，用 `--approve <deck>:<页码>` 把它转为 approved，并在 STATUS.json 的说明里写上确认日期。
   - **绝不能自己把页面标成 approved**，只有用户说"可以了"才行。
5. **图标着色自检**：动了 `deck._recolor` 时，把 27 个图标统一着成一种颜色渲染一遍（见 design-rules 第 14 条）。

## 6. 迭代历史与用户的判断标准（很重要）

| 轮次 | 做法 | 用户反馈 |
|---|---|---|
| 1 | 平面咨询卡片（纯色、大字、留白） | "缺少给定模板的精致" |
| 2 | 精修：渐变、阴影、半透明、元素交叠、模板图片、图表批注 | "有所改善，和模板比较接近了" |
| 2.1 | 样张 12 处细节修正 | "样张可以了" → 铺开 20 页 |
| 3 | 用户给出模板第 10 页作标杆："信息密度不够，缺咨询的高级感"，"标题下面缺少分割线" | 重做为咨询构图：论点条 → 区块标签 → 主图两翼 → 证据框 → 框架条 |
| 3.1 | 用户指出"没有对齐、出界"，"标题和页尾的坐标是严格一致的" | 定为硬规则：内容边界 = 标题线/页脚边界（0.37″/12.96″），同行共用中线 |
| 4 | 封装为 Skill；kit.pptx 被指"内容不对" | 改为可读的素材目录；顺带修了 crown/kid 图标着色 bug |

**用户的稳定偏好**：
- 先改 2–3 张代表性样张确认方向，再铺开全套；方向没确认前不要大面积改。
- 以模板（尤其第 10 页）的"咨询感"为标杆：信息密度高、层次多、用线连逻辑而不是堆卡片。
- 对齐和边界零容忍；会放大截图圈出问题。
- **不替大纲加词**；推算出来的数字必须逐条列出请用户核实。
- 用中文沟通；每轮把经验沉淀进 `design-rules.md`。

## 7. 待办与已知问题（建议的下一步顺序）

1. **把其余 17 种版式升级成咨询风格**（最大的一项）。目前只有 `chart_phases`、`funnel`、`hub` 有论点条 + 区块标签 + 框架条；其他版式没有 `thesis` 字段、内容从 1.15″ 开始。建议：先挑 2–3 个（如 `dual_charts`、`matrix`、`versus`）做样张给用户确认，再铺开。每改一个版式都更新 `layouts.md`、`examples/nev-report.json`，跑回归并 `--update`（刷新临时快照）；用户确认样张后再 `--approve` 对应页码。
2. **用一份新的大纲做端到端测试**（不同行业、不同页数），检验 SKILL.md 的规划指引和各版式容量上限是否合理；容量不够或字段不顺手就改版式。
3. **文字溢出检查是估算**（按字宽估行数）。可考虑用 PowerPoint COM 读取实际文本框边界做精确检查。
4. **重叠检查**还没有（比如标注气泡压住数据标签只能靠看图）。
5. **大纲 → deck.json 没有程序辅助**，完全靠 Claude 按 `layouts.md` 手写。可考虑为每个版式提供最小 JSON 模板，或写一个字段校验器（缺字段、超容量时给出清晰报错）。
6. **cover 背景图**目前收在 EL–ER 内；是否允许封面满版出血，可与用户确认。
7. **运行环境**依赖 Windows + PowerPoint + OPPOSans；没有 PowerPoint 时只能 `--no-render`，回归跑不了。

## 8. 环境注意事项（踩过的坑）

- Windows 路径过长会导致原生程序启动失败；仓库路径目前没问题，临时文件放短路径。
- 在 Bash 里用 heredoc 写含中文引号的长 Python 脚本，偶尔会被 shell 截断（"unexpected EOF"）。**长脚本先用 Write 写成文件再运行。**
- 删除命令若作用于无法静态解析的路径会被安全检查拦截；需要清理时用明确的绝对路径。
- `scripts/office/validate.py`（pptx skill 自带）通过 ≠ PowerPoint 能打开；以 `render.ps1` 是否成功为准。
- deck.json 中演讲者备注字段是 `speaker_notes`（`notes` 已被微笑曲线版式占用）。
