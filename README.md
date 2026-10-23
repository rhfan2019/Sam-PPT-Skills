# Sam-PPT-Skills

Sam 的 PPT 生成 Skill 合集。

| Skill | 说明 |
|---|---|
| [Sam-PPT-Bain](Sam-PPT-Bain/) | 以自带的 ppt-master 蓝红模板为底，按贝恩/咨询白皮书风格把大纲生成可编辑 PPTX（ppt-master 薄外壳，PowerPoint 渲染自检） |

每个 Skill 的运行输出放在仓库之外：`D:\Workspace\Sam-PPT-Skills-Test\runs\<Skill名>\run-yyyymmdd-hhmmss-fff\`（该目录不存在时退回 `<系统临时目录>\claude\Sam-PPT-Runs\<Skill名>\`；可用环境变量 `SAM_PPT_RUNS` 覆盖）。

## 安装为 Claude Code Skill

在 Windows 上把 Skill 目录链接到个人 skills 目录（只需一次）：

```powershell
New-Item -ItemType Junction -Path "$env:USERPROFILE\.claude\skills\Sam-PPT-Bain" -Target "D:\Workspace\Sam-PPT-Skills\Sam-PPT-Bain"
```

依赖：Windows + PowerPoint、Python 3.10+（含 Pillow）、OPPOSans 字体、[ppt-master](https://github.com/hugohe3/ppt-master) Claude Code 插件。
