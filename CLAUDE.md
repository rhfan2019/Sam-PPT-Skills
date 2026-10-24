# Sam-PPT-Skills 工作约定

- 仓库：https://github.com/rhfan2019/Sam-PPT-Skills（私有），分支 `main`。
- **每次修改都要自动提交并推送到 GitHub**（用户的长期要求，无需再次确认）：完成一处有意义的改动后 `git add -A && git commit && git push`。
- 每个 Skill 一个子目录（如 `Sam-PPT-Bain/`），目录名即 Skill 名。
- Skill 的每次运行输出统一放在仓库**之外**的 `D:\Workspace\Sam-PPT-Skills-Test\runs\<Skill名>\run-yyyymmdd-hhmmss-fff\`（毫秒三位；用户 2026-10-23 指定），可用环境变量 `SAM_PPT_RUNS` 覆盖。不要把运行目录放回仓库或 Skill 目录。
- 接手 Sam-PPT-Bain 时读 `benchmarks/README.md`、`Sam-PPT-Bain/SKILL.md`、`references/rules.md`、`references/page-patterns.md`。
- 开发记录（交接文档、历次测试的结论）不放在仓库里，**不要主动查找或读取**；只有用户在会话里明确要求并给出路径时才读。针对测试案例的优化由用户另开会话、用明确指令发起；测试会话只用 Skill 和大纲。
- Sam-PPT-Bain 是 ppt-master 的薄外壳：排版、检查、导出都交给 ppt-master（插件只读，不修改），本仓库只放模板工作区、规则、样张和收尾脚本。不要再写自研排版引擎。例外（用户 2026-10-22 同意）：`put` 可以展开胶囊 / 栏头 / 编号圆 / 折行文字四种构件标记，它们不决定位置和版式；主视觉必须手写，不得新增卡片格、多栏之类的版式标记。防模板化约定（用户 2026-10-23 放宽）：构件可复用、构图要变化——`Sam-PPT-Bain/references/components/` 里的构件写法可以逐页复制使用，整页的构件组合和布局要随内容变化。
- 只有用户说"可以了"的页面才是基线（`Sam-PPT-Bain/references/approved/`）；不要自己宣布通过。
- Skill 里不放任何案例内容；测试用的大纲与标准答案放在仓库根的 `benchmarks/`。基准测试的生成只交给没看过参考页的盲测子代理，并按 `benchmarks/README.md` 的防作弊约定限制它的读取范围。
- **视觉风格锁定**（用户 2026-10-24 定，"视觉风格必须严格固化，避免被后续覆盖"）：锁定项见 `Sam-PPT-Bain/references/style-lock.md`。只有用户点名某一项并明确同意时才能改，改后在该文件"变更记录"里登记，再运行 `python Sam-PPT-Bain/scripts/style_guard.py --update`。三道检查会拦住未经同意的改动：`style_guard.py` 在每次 `new` 时运行、仓库 pre-commit 钩子（`git config core.hooksPath .githooks`）、项目 `.claude/settings.json` 里的编辑确认钩子。测试反馈先记进仓库外的 `handover/issues.md`，提炼成 `handover/lessons.md` 的候选规则，经用户确认后才写进 Skill，而且不得削弱锁定项。
- **盲测隔离**（用户 2026-10-24 定）：Skill 运行期间不得读取 `D:\Workspace\Sam-PPT-Skills-Test` 下的任何内容，唯一例外是本次运行的 RUN_DIR。开隔离测试会话前，先用 `python D:\Workspace\tmp\test-guard\seed.py <空文件夹>` 准备会话目录：它会装一个 PreToolUse 钩子，阻断会话读取测试工作区。大纲先复制到 `D:\Workspace\tmp\` 再交给会话。
