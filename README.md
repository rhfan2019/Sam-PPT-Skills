# Sam-PPT-Skills

把大纲生成为可编辑 PPTX 的 Skill 集合，底层引擎是 ppt-master。
| Skill | 用途 |
|---|---|
| `Sam-PPT-Blueprint` | 蓝图重绘法：按逻辑表达规范定图示、按分区规范切版面，从参考稿拆出的模块（可跨页）拼页再换成大纲内容，学参考稿的神韵；含图示含义审查、参考稿图标转原生形状、OPPOSans 中文字体修复 |

## 安装与使用（Sam-PPT-Blueprint）

前提：已安装 ppt-master 插件和 PowerPoint。每台机器装一次，Skill 或参考稿库更新后再装一次：

```
python Sam-PPT-Blueprint/scripts/install.py <参考稿.pptx> <参考稿库目录> --name <名称> --default
```

Skill 装到 `~/.claude/skills/`，参考稿库连同参考稿装到 `~/.claude/sam-ppt/references/<名称>/`。参考稿库由 `prepare_reference.py` 生成并拆好模块目录（见 `references/module-catalog.md`）。

之后在任何放着大纲的文件夹里开会话，说一句：

```
用 Sam-PPT-Blueprint 把 outline.md 做成 PPT。
```

要换参考稿时加一句"参考 <名称或 .pptx 路径>"。

## 开发

文档入口见 [docs/README.md](docs/README.md)：目录契约、交接文档、待办清单、测试指南和测试记录。`tools/` 是不随 Skill 安装的开发工具，提交前运行 `python tools/check_docs.py`。
