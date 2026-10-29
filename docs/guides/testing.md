# 测试指南

现行操作说明，2026-10-28。测试为什么天然隔离见[目录契约第 5 节](../architecture/repository-contract.md#5-测试隔离靠什么)。

## 两条规矩

- **和真实使用完全一样**：用户只在一个独立文件夹里放 `outline.md`，开会话说一句"用 Sam-PPT-Blueprint 把 outline.md 做成 PPT。"。用户不运行任何脚本、不准备环境；提示词里不写流程、计时、日志、汇报格式，这些都由 Skill 自己规定。多出来的任何一步都是 Skill 的问题，要内置或由安装解决。
- **每次测试都要沉淀**：写一份测试记录，把问题归成共性问题（规则、脚本、可量化门槛）登记进待办清单；只出现在某一页、某个数据上的个例单列，不为它改 Skill。

- **测试会话不改 Skill**：测试会话只产出成品、日志和问题。要改 Skill，回到开发会话在仓库里改，见[目录契约第 5 节第 4 条](../architecture/repository-contract.md#5-测试隔离靠什么)。

## 1. 安装要测的提交（开发会话做）

先确认安装副本没有仓库外的改动（没有输出才继续；有输出先把改动收回仓库）：

```bash
diff -rq --strip-trailing-cr -x __pycache__ ~/.claude/skills/Sam-PPT-Blueprint /d/Workspace/Sam-PPT-Skills/Sam-PPT-Blueprint
```

改了页面脚本（换字、拼页、收口、导入修补）的提交，安装前先过回归阶梯 `Sam-PPT-Blueprint/scripts/ladder.py`（用法见 SKILL.md"改脚本后的回归"）。

从 `git archive` 导出到临时目录再安装，不动仓库工作区：

```bash
T=$(mktemp -d) && git -C /d/Workspace/Sam-PPT-Skills archive <提交号> Sam-PPT-Blueprint | tar -x -C $T && python $T/Sam-PPT-Blueprint/scripts/install.py D:/Workspace/Sam-PPT-Lab/assets/rnb-core.pptx D:/Workspace/Sam-PPT-Lab/assets/rnb-blueprint --name rnb --default
```

Skill 装到 `~/.claude/skills/Sam-PPT-Blueprint`，参考稿库装到 `~/.claude/sam-ppt/references/rnb/` 并设为默认。本机当前装的是哪个提交，记在[交接文档](../plans/blueprint-handover.md)第 1 节。

## 2. 开测试会话

1. 建运行目录 `D:\Workspace\Sam-PPT-Lab\runs\<yyyymmdd-hhmm>_<对象>_<大纲>\`，只放 `outline.md`（从 `docs/samples/outlines/` 或 `docs/samples/testset/` 复制）。用户自己测时文件夹放在哪里都行；测完由开发会话把整个文件夹移进 `runs\`。
2. 开发会话代测时用 `start_session`：`cwd` 设为运行目录，`context: fresh`，`use_worktree: false`；prompt 就是那一句话，background 只说"当前目录里有一份大纲 outline.md"。不要用 `context: fork`，fork 会带上开发会话的全部上下文。

## 3. 评估

1. 规范指标（主要依据），括号里是参考稿 p25–p75 的范围，结果和字段含义见脚本输出：

   ```bash
   python Sam-PPT-Blueprint/scripts/style_gap.py check ~/.claude/sam-ppt/references/rnb <deck.pptx> <运行目录>/renders
   ```

2. 渲染图（Skill 第 7 步已渲染；需要重渲染时）：

   ```bash
   powershell -ExecutionPolicy Bypass -File Sam-PPT-Blueprint/scripts/render.ps1 <deck.pptx> <运行目录>/renders
   ```

3. SVG 密度指标（形状、文字块、字/块、次色、浅底、连接件、图标等 10 项）：成品项目里跑 `Sam-PPT-Blueprint/scripts/page_metrics.py`，用法见脚本说明。它和 `style_gap` 的结论目前可能互相矛盾（F33），两者都记下。
4. 像素指标（辅助）：coverage、solid、dark_solid、colour 四项占整页的比例，低于基线 P5 标 `-`，高于 P95 标 `+`：

   ```bash
   python tools/metrics.py <运行目录>/renders --baseline D:/Workspace/Sam-PPT-Lab/assets/rnb-baseline.csv
   ```

5. 拼一张总览图，逐页看渲染图，对照大纲看图示含义。新旧版本对比由用户盲测：A、B 随机左右，答案另存，只按"像不像参考稿"选。
6. 读运行日志里的用时、阶段和会话自报的问题；会话自述不可信，以成品和指标为准。

指标只辅助判断。页面能不能当基线由用户说了算，只有用户说"可以了"的页面才算基线。

## 4. 记录

1. 在 `docs/plans/` 写测试记录 `YYYY-MM-DD-<对象>-<大纲>-test.md`：环境（提交号、模型、参考稿库）、用时、指标对比、逐页问题、问题分析。问题编号用 `F<序号>`，接着[待办清单](../plans/backlog.md)里最大的编号往下排（2026-10-28 时到 F45）。
2. 每个共性问题在[待办清单](../plans/backlog.md)登记一行，测试记录只写分析、不维护状态。已改待验证的条目在本次测试里有了结果的，在待办清单里改状态。
3. 更新[交接文档](../plans/blueprint-handover.md)的现状和下一步。
