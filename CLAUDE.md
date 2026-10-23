# Sam-PPT-Skills 工作约定

- 仓库：https://github.com/rhfan2019/Sam-PPT-Skills（私有），分支 `main`。
- **每次修改都要自动提交并推送到 GitHub**（用户的长期要求，无需再次确认）：完成一处有意义的改动后 `git add -A && git commit && git push`。
- 每个 Skill 一个子目录（如 `Sam-PPT-Bain/`），目录名即 Skill 名。
- Skill 的每次运行输出放在仓库和 Skill 目录**之外**：`<系统临时目录>\claude\Sam-PPT-Runs\<Skill名>\run-yyyymmdd-hhmmss-fff\`（毫秒三位；本机即 `C:\Users\fanrh\AppData\Local\Temp\claude\Sam-PPT-Runs\Sam-PPT-Bain\`），可用环境变量 `SAM_PPT_RUNS` 覆盖。不要把运行目录放回 Skill 目录或 `D:\Workspace` 下。
- 接手 Sam-PPT-Bain 时先读仓库根的 `HANDOVER.md`（现状、用户偏好、待办）和 `benchmarks/README.md`，再读 `Sam-PPT-Bain/SKILL.md`、`references/rules.md`、`references/page-patterns.md`。
- Sam-PPT-Bain 是 ppt-master 的薄外壳：排版、检查、导出都交给 ppt-master（插件只读，不修改），本仓库只放模板工作区、规则、样张和收尾脚本。不要再写自研排版引擎。例外（用户 2026-10-22 同意）：`put` 可以展开胶囊 / 栏头 / 编号圆 / 折行文字四种构件标记，它们不决定位置和版式；主视觉必须手写，不得新增卡片格、多栏之类的版式标记（防模板化）。
- 只有用户说"可以了"的页面才是基线（`Sam-PPT-Bain/references/approved/`）；不要自己宣布通过。
- Skill 里不放任何案例内容；测试用的大纲与标准答案放在仓库根的 `benchmarks/`。基准测试的生成只交给没看过参考页的盲测子代理，并按 `benchmarks/README.md` 的防作弊约定限制它的读取范围。
