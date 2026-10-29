# Sam-PPT-Skills 工作约定

文件放哪里以 [docs/architecture/repository-contract.md](docs/architecture/repository-contract.md) 为唯一规范；新增、移动、删除文件前先读它。文档入口是 [docs/README.md](docs/README.md)。

## 硬约束

- 仓库：https://github.com/rhfan2019/Sam-PPT-Skills（私有），分支 `main`。**每次修改都要自动提交并推送到 GitHub**（用户的长期要求，无需再次确认）。
- 每个 Skill 一个子目录，目录名即 Skill 名。Skill 目录只放运行时需要的东西，不放案例内容和开发文档。
- 底层引擎是 ppt-master 插件，只读、不修改。提方案前先查它已有的能力（[能力地图](docs/architecture/ppt-master-map/ppt-master能力地图.md)），已有的不自己造、不打补丁。新 Skill 只加"基线实测出来、ppt-master 没有、并经用户同意"的东西。
- 人写的东西（文档、交接、待办、测试记录、测试大纲、开发工具）都进仓库；`D:\Workspace\Sam-PPT-Lab\` 只放参考稿素材和运行输出。不另建工作目录。
- 只有用户说"可以了"的页面才算基线；不要自己宣布通过。
- Skill 不删改大纲内容，信息密度归 Sam-PPT-Outline 管。
- 测试和真实使用完全一样，步骤见 [docs/guides/testing.md](docs/guides/testing.md)：用 `install.py` 全局安装要测的提交，在只放着 `outline.md` 的独立文件夹里开新会话（不用 fork），只说一句"用 Sam-PPT-Blueprint 把 outline.md 做成 PPT。"。不让用户执行任何脚本或准备环境。
- 提交前运行 `python tools/check_docs.py`，失败如实报告，不绕过。

## 文档节奏

- 未完成事项只登记在 [docs/plans/backlog.md](docs/plans/backlog.md)；完成后写提交号，攒批移到 `docs/archive/backlog-done.md`。
- 每条工作线一份交接文档（现为 [docs/plans/blueprint-handover.md](docs/plans/blueprint-handover.md)），持续更新，不新建带日期的快照。
- 每次测试写一份测试记录（`docs/plans/YYYY-MM-DD-<对象>-<大纲>-test.md`），只为共性问题改 Skill，问题登记进待办清单。
- 过时的文档开头标状态后移入 `docs/archive/`，同步改索引；同一事实只写一处，其他地方放链接。
- **结束一个任务前**：更新交接文档的现状和下一步、待办清单（新增或关闭），和改动一起提交。
