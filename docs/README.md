# 文档索引

只列现行文档。规则入口是仓库根目录的 `CLAUDE.md`。

- [目录契约](architecture/repository-contract.md)：仓库和 `Sam-PPT-Lab` 各放什么、测试为什么天然隔离、新增和移动文件的流程。动文件前先读。
- [Sam-PPT-Blueprint 交接文档](plans/blueprint-handover.md)：这条工作线的新会话入口（现行，持续更新）。
- [待办与问题清单](plans/backlog.md)：所有未完成事项的唯一入口。
- [测试指南](guides/testing.md)：安装要测的提交、开测试会话、评估、记录。
- [S/4 + 测试集测试记录](plans/2026-10-28-blueprint-s4-testset-test.md)：27 页完整运行、两轮 Skill 修改、四套测试集，F19–F45 的问题分析。
- [s11 测试记录（v3–v7）](plans/2026-10-27-s11-blueprint-tests.md)：5 轮隔离测试的结果和 F1–F18 的问题分析。
- [ppt-master 6.7.2 能力地图](architecture/ppt-master-map/ppt-master能力地图.md)：底层引擎有什么，提方案前先查；同目录有 5 份分册和独立复核。
- 测试大纲：`samples/outlines/` 一个案例一个文件（[s11-fde](samples/outlines/s11-fde.md)、[s4-migration](samples/outlines/s4-migration.md)）；`samples/testset/` 是回归用的四套节选（[S03](samples/testset/S03-xhs.md)、[S04](samples/testset/S04-s4-migration.md)、[S10](samples/testset/S10-retail.md)、[S11](samples/testset/S11-fde.md)）。

目录：`architecture/` 契约、迁移台账、引擎审计、方向决策；`plans/` 待办、交接、计划、测试记录（计划和测试记录不代表当前完成状态，现状看待办清单）；`guides/` 现行操作说明；`samples/` 测试大纲；`archive/` 历史资料和已完成清单，不作为现行依据。
