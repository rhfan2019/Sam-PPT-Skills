# Sam-PPT-Skills 工作约定

- 仓库：https://github.com/rhfan2019/Sam-PPT-Skills（私有），分支 `main`。
- **每次修改都要自动提交并推送到 GitHub**（用户的长期要求，无需再次确认）：完成一处有意义的改动后 `git add -A && git commit && git push`。
- 每个 Skill 一个子目录（如 `Sam-PPT-Bain/`），目录名即 Skill 名。
- Skill 的每次运行输出放在该 Skill 目录下的 `runs/run-yyyymmdd-hhmmss-fff/`（毫秒三位），`runs/` 已在 `.gitignore` 中，不提交。
- 接手 Sam-PPT-Bain 时先读 `Sam-PPT-Bain/HANDOVER.md`（现状、用户偏好、待办），再读 `SKILL.md` 和 `references/design-rules.md`。
- 改了组件或版式后必须跑 `python Sam-PPT-Bain/scripts/regress.py`；变化确认是有意的再 `--update`，基线和代码一起提交。
