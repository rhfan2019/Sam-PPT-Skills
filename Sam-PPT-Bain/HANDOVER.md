# Sam-PPT-Bain 交接文档

> 2026-10-21 重写。新会话先读本文，再读 `SKILL.md`、`references/rules.md`、`references/page-patterns.md`。

## 1. 现状

- **架构**：薄外壳 + ppt-master。2026-10-21 用户看过 ppt-master 试点（P4/P13/P17）后认可方向（"算是非常不错了，看起来这个方向是对的"），要求清空旧引擎、按薄外壳全力改造。旧的 python-pptx 自研引擎（build.py / samppt / kit.pptx / regress.py）已全部删除，**不要恢复，也不要再写自己的排版引擎**。
- **模板**：`template/` 是 ppt-master 的 Deck（`sam-bain`）+ Style（`sam-bain-consulting`）工作区，6 个原型，通过 ppt-master 模板检查与预览导出。正文两页来自 参考模板；封面、目录、章节、结束页为同一视觉语言的新设计，**尚未经用户确认**。
- **用户确认过的效果**：
  - 旧引擎的六张咨询版样张：`references/approved/nev-p04/05/07/10/13/17.png`；
  - ppt-master 试点三页：`references/exemplars/trend-phases / funnel / hub`（用户的评价是"算是非常不错了"）。
  - 除此之外的任何页面都**不是基线**，不能当作"用户满意"。

## 2. 位置与约定

| 项目 | 位置 |
|---|---|
| 仓库（私有） | https://github.com/rhfan2019/Sam-PPT-Skills ，分支 `main` |
| 本地 | `D:\Workspace\Sam-PPT-Skills\Sam-PPT-Bain`（个人 Skill 目录链接 `C:\Users\fanrh\.claude\skills\Sam-PPT-Bain` 指向这里） |
| ppt-master | 插件 `~/.claude/plugins/cache/ppt-master/ppt-master/<hash>/ppt-master`（只读，不改） |
| 原始模板 | `参考模板` |
| 测试大纲 | `examples/outlines/nev-report-outline.md` |
| 每次运行 | `runs/run-yyyymmdd-hhmmss-fff/`（不提交） |

硬约定：每次有意义的修改都 `git commit` + `git push`（无需再问）；运行输出放 `runs/`；只有用户说"可以了"才算确认。

## 3. 目录

```
Sam-PPT-Bain/
├── SKILL.md                 流程（new → Quick Generate 写 SVG → check → finish → 交付说明）
├── HANDOVER.md              本文
├── template/                ppt-master Deck + Style 工作区（templates/ 6 个原型 + 两份 spec；images/ 页框与封面照片）
├── assets/photos/           内容素材照片（来自 参考模板），按需用 `sam_bain.py photos` 复制
├── references/
│   ├── rules.md             用户硬规则 + 咨询感来源 + 自检清单
│   ├── page-patterns.md     坐标体系、构件尺寸、20 种页型做法、ppt-master 约束
│   ├── exemplars/           已验收的 ppt-master 试点页（SVG + PNG），写新页的起点
│   └── approved/            旧引擎时期用户确认的六张样张（视觉目标）
├── scripts/
│   ├── sam_bain.py          new / photos / icons / check / finish
│   ├── fix_cjk_fonts.py     导出后把中文槽位改回同字重 OPPOSans（ppt-master 不认识 OPPOSans）
│   └── render.ps1           PowerPoint 逐页导出 PNG
└── examples/outlines/       测试大纲
```

## 4. 已知限制

- ppt-master 把 OPPOSans 当作"非 PPT 安全字体"给出警告（不阻断）；字体不嵌入，交付机器需安装 OPPOSans。
- 图表默认是原生形状（可编辑但不能在 Excel 里改数据）；需要原生图表时按 ppt-master chart 模块写替换标记并 `finish --native-charts`。
- 图标来自 ppt-master 图标库（一套 deck 一个家族，推荐 `chunk-filled`），与 参考模板 的原图标不同。
- 论点条高度沿用 参考模板（61.26 px，26.67 px 字）；超长原句按 rules.md 一.5 处理。

## 5. 待办

1. 用 20 页新能源大纲完整跑一遍（第二阶段），请用户逐页判断；把用户确认的页面加入 `references/exemplars/`。
2. 再用一份**不同行业**的大纲做端到端测试，检验 page-patterns 的通用性。
3. 封面 / 目录 / 章节 / 结束页的设计请用户确认。
