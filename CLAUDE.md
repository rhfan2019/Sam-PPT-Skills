# Sam-PPT-Skills 工作约定

- 仓库：https://github.com/rhfan2019/Sam-PPT-Skills（私有），分支 `main`。
- **每次修改都要自动提交并推送到 GitHub**（用户的长期要求，无需再次确认）：完成一处有意义的改动后 `git add -A && git commit && git push`。
- 每个 Skill 一个子目录（如 `Sam-PPT-Bain/`），目录名即 Skill 名。
- Skill 的每次运行输出放在该 Skill 目录下的 `runs/run-yyyymmdd-hhmmss-fff/`（毫秒三位），`runs/` 已在 `.gitignore` 中，不提交。
- 接手 Sam-PPT-Bain 时先读 `Sam-PPT-Bain/HANDOVER.md`（现状、用户偏好、待办），再读 `SKILL.md`、`references/rules.md`、`references/page-patterns.md`。
- Sam-PPT-Bain 是 ppt-master 的薄外壳：排版、检查、导出都交给 ppt-master（插件只读，不修改），本仓库只放模板工作区、规则、样张和收尾脚本。不要再写自研排版引擎。
- 只有用户说"可以了"的页面才是基线（`Sam-PPT-Bain/references/approved/`；`examples/` 里的案例页只作写法参考）；不要自己宣布通过。
