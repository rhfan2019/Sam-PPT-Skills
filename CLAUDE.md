# Sam-PPT-Skills 工作约定

- 仓库：https://github.com/rhfan2019/Sam-PPT-Skills（私有），分支 `main`。
- **每次修改都要自动提交并推送到 GitHub**（用户的长期要求，无需再次确认）。
- 每个 Skill 一个子目录，目录名即 Skill 名。Skill 里不放任何案例内容。
- 底层引擎是 ppt-master 插件，只读、不修改。提方案前先查它已有的能力，已有的不自己造、不打补丁。新 Skill 只加"基线实测出来、ppt-master 没有、并经用户同意"的东西。
- 仓库之外的工作资料只放在 `D:\Workspace\Sam-PPT-Lab\`，结构和 runs 命名见它的 `README.md`。不要另建工作目录。
- 开发记录在 `Sam-PPT-Lab\handover\`，不进仓库，**不要主动读取**；只有用户在会话里明确要求并给出路径时才读。
- 只有用户说"可以了"的页面才算基线；不要自己宣布通过。
- Skill 不删改大纲内容，信息密度归 Sam-PPT-Outline 管。测试大纲放在 `Sam-PPT-Lab\outlines\`。
- 测试和真实使用完全一样：Skill 和参考稿库用 `install.py` 全局安装（测哪个提交就先装哪个），在一个只放着 `outline.md` 的独立文件夹里开新会话，只说一句"用 Sam-PPT-Blueprint 把 outline.md 做成 PPT。"。不让用户执行任何脚本或准备环境；测试会话里不写流程、计时、汇报等要求，这些都内置在 Skill 里。每次测试的共性问题记进 `Sam-PPT-Lab\findings.md`。
