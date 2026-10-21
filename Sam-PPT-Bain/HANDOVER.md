# Sam-PPT-Bain 交接文档

> 2026-10-21 重写，同日补充第 5 节（边测边改）。新会话先读本文，再读 `SKILL.md`、`references/rules.md`、`references/page-patterns.md`。

## 1. 现状

- **架构**：薄外壳 + ppt-master。2026-10-21 用户看过 ppt-master 试点（P4/P13/P17）后认可方向（"算是非常不错了，看起来这个方向是对的"），要求清空旧引擎、按薄外壳全力改造。旧的 python-pptx 自研引擎（build.py / samppt / kit.pptx / regress.py）已全部删除，**不要恢复，也不要再写自己的排版引擎**。
- **模板**：`template/` 是 ppt-master 的 Deck（`sam-bain`）+ Style（`sam-bain-consulting`）工作区，6 个原型，通过 ppt-master 模板检查与预览导出。正文两页来自 参考模板；封面、目录、章节、结束页为同一视觉语言的新设计，**2026-10-21 经用户确认为模板基线**（渲染图 `references/approved/template-*.png`）。
- **用户确认过的效果**：
  - 模板 4 个新原型（封面、目录、章节页、结束页）：`references/approved/template-*.png`（2026-10-21 确认）；
  - ppt-master 试点三页：`examples/nev-case/pilot-pages/trend-phases / funnel / hub`（用户的评价是"算是非常不错了"）。这是新能源汽车案例，2026-10-21 按用户要求从 `references/` 移到 `examples/`：只作写法参考，不是品牌/风格资产。
  - 旧引擎的六张新能源样张和汽车素材照片（car3d / sedan / dealer）已于 2026-10-21 按用户要求删除（git 历史里可找回）。
  - 除此之外的任何页面都**不是基线**，不能当作"用户满意"。

## 2. 位置与约定

| 项目 | 位置 |
|---|---|
| 仓库（私有） | https://github.com/rhfan2019/Sam-PPT-Skills ，分支 `main` |
| 本地 | `D:\Workspace\Sam-PPT-Skills\Sam-PPT-Bain`（个人 Skill 目录链接 `C:\Users\fanrh\.claude\skills\Sam-PPT-Bain` 指向这里） |
| ppt-master | 插件 `~/.claude/plugins/cache/ppt-master/ppt-master/<hash>/ppt-master`（只读，不改） |
| 原始模板 | `参考模板` |
| 测试大纲 | `examples/nev-case/outline.md`（新能源汽车案例） |
| 每次运行 | `runs/run-yyyymmdd-hhmmss-fff/`（不提交） |

硬约定：每次有意义的修改都 `git commit` + `git push`（无需再问）；运行输出放 `runs/`；只有用户说"可以了"才算确认。

## 3. 目录

```
Sam-PPT-Bain/
├── SKILL.md                 流程（new → Quick Generate 写 SVG → check → finish → 交付说明）
├── HANDOVER.md              本文
├── template/                ppt-master Deck + Style 工作区（templates/ 6 个原型 + 两份 spec；images/ 页框与封面照片）
├── assets/photos/           通用素材照片（city_tech.png），按需用 `sam_bain.py photos` 复制
├── references/
│   ├── rules.md             用户硬规则 + 咨询感来源 + 自检清单
│   ├── page-patterns.md     坐标体系、构件尺寸、20 种页型做法、ppt-master 约束
│   └── approved/            用户确认的模板原型渲染图（template-*.png）
├── scripts/
│   ├── sam_bain.py          new / photos / icons / check / finish
│   ├── fix_cjk_fonts.py     导出后把中文槽位改回同字重 OPPOSans（ppt-master 不认识 OPPOSans）
│   └── render.ps1           PowerPoint 逐页导出 PNG
└── examples/nev-case/       新能源汽车测试案例：outline.md + pilot-pages/（三张试点页，只借写法）
```

## 4. 已知限制

- ppt-master 把 OPPOSans 当作"非 PPT 安全字体"给出警告（不阻断）；字体不嵌入，交付机器需安装 OPPOSans。
- 图表默认是原生形状（可编辑但不能在 Excel 里改数据）；需要原生图表时按 ppt-master chart 模块写替换标记并 `finish --native-charts`。
- 图标来自 ppt-master 图标库（一套 deck 一个家族，推荐 `chunk-filled`），与 参考模板 的原图标不同。
- 论点条高度沿用 参考模板（61.26 px，26.67 px 字）；超长原句按 rules.md 一.5 处理。

## 5. 下一阶段：边测边改（2026-10-21 起，在新会话进行）

用户要求：**测试必须通过 Sam-PPT-Bain 技能本身进行**，不能绕过技能另做。

### 5.1 每一轮的做法

1. **调用技能**：用户说"用 Sam-PPT-Bain 做……"或输入 `/Sam-PPT-Bain` 时，先用 Skill 工具调用 `Sam-PPT-Bain`，再严格按 SKILL.md 走：`sam_bain.py new` → 按 ppt-master Quick Generate 写 SVG → `check` → `finish`。
2. **小批量**：每轮 3–5 页，以免上下文过长被压缩。用户看过、修好后再扩大页数。
3. **交付**：给出 `contact.png` 和逐页渲染图，按 SKILL.md 第 7 步写交付说明。**不要自己宣布通过。**
4. **改技能，不改成品**：用户指出问题后，改对应的技能文件，不在本次 `runs/` 成品里手工修补。
   - 页型、构件、坐标 → `references/page-patterns.md`
   - 用户硬规则、自检清单 → `references/rules.md`
   - 流程、命令 → `SKILL.md`、`scripts/sam_bain.py`
   - 模板原型 → `template/`
     - 改完必须重跑 `svg_quality_checker.py templates --template-mode --canonical-authoring --format ppt169` 和 `template_preview_pptx.py`。
     - 已确认的 4 个原型，改动前要先问用户。
5. **提交**：改完后 `git commit` + `git push`。
6. **复测**：重新调用技能，跑出新的 `runs/run-*`，与上一轮对比。
7. **记录基线**：用户说"可以了"的案例页，放进 `examples/<案例>/`，并在本文第 1 节登记。

技能目录是指向本仓库的目录链接。正文、规则、模板改动后，**下一次调用就生效**。但 SKILL.md 头部的 `description`（触发描述）是会话启动时加载的，改了它要新开会话才生效。

### 5.2 测试顺序

1. 新能源大纲 `examples/nev-case/outline.md`：先做前 5 页，再逐批做完 20 页，请用户逐页判断。
2. 再用一份**不同行业**的大纲端到端测试，检验 page-patterns 是否通用。确认 `references/`、`assets/` 里没有混进案例内容。

### 5.3 已踩过的坑

- **Python 启动**：用 `python`，不要用 `python3`（WindowsApps 占位程序）。
  - 很长的 Windows 路径（例如会话 scratchpad）会让 Python 起不来，临时文件放 `D:\Workspace\...` 下的短路径。
  - Bash 里输出中文时加 `PYTHONIOENCODING=utf8`。
- **PowerPoint 锁文件**：渲染时 PowerPoint 会占用文件，`runs/` 里个别文件可能删不掉。关掉 PowerPoint 再删，或者不管它（已 gitignore）。
- **结构化模板约束**：
  - 同一 master 下，每个 SVG 的 master 原子必须完全一致，所以 master 只放背景，页框原子放在 layout 层。
  - 每个 layout 内的 placeholder idx 必须唯一。
  - slot 的文字放不下就要扩 bounds 或减字号，checker 会报溢出比例。
- **图标**：`steering` 等名字不在 ppt-master 图标库里，用前先查。
- **范围**：用户说"打包"时只做模板和规则，不要顺手跑整套案例。
- **未使用的运行目录**：`runs/run-20261021-072053-091` 是中途停掉的整套新能源运行，没有用到，可以删。

### 5.4 新会话开场可直接粘贴

> 先读 `D:\Workspace\Sam-PPT-Skills\Sam-PPT-Bain\HANDOVER.md`。然后调用 Sam-PPT-Bain 技能，把 `examples/nev-case/outline.md` 的前 5 页做成 PPT。我会一边看一边提修改意见，你改技能文件后再用技能复测。
