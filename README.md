# Sam-PPT-Skills

Sam 的 PPT 生成 Skill 合集。

| Skill | 说明 |
|---|---|
| [Sam-PPT-Bain](Sam-PPT-Bain/) | 以 参考模板 模板为底，按贝恩/咨询白皮书风格把大纲直出为可编辑 PPTX（20 种版式，PowerPoint 渲染自检） |

每个 Skill 的运行输出放在各自目录下的 `runs/run-yyyymmdd-hhmmss-fff/`，不提交到仓库。

## 安装为 Claude Code Skill

在 Windows 上把 Skill 目录链接到个人 skills 目录（只需一次）：

```powershell
New-Item -ItemType Junction -Path "$env:USERPROFILE\.claude\skills\Sam-PPT-Bain" -Target "D:\Workspace\Sam-PPT-Skills\Sam-PPT-Bain"
```

依赖：Windows + PowerPoint、Python 3.10+（`pip install python-pptx lxml pillow`）、OPPOSans 字体。
