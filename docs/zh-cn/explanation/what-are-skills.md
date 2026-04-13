---
title: '什么是技能？'
description: BMad 生态中智能体、工作流和工具底层的通用构建单元
---

技能（Skill）是 BMad Builder 所有产出物的通用打包格式。智能体是技能，工作流是技能，简单工具也是技能。该格式遵循 [Agent Skills 开放标准](https://agentskills.io/home)。

## BMad 中的技能

BMad Builder 生产的技能符合开放标准，并在此基础上增加了一些 BMad 特有约定。

| 组件 | 用途 |
| ---- | ---- |
| **SKILL.md** | 技能的指令：角色、能力与行为规则 |
| **resources/** | 参考数据、模板与指导文档 |
| **scripts/** | 确定性验证与分析脚本 |
| **templates/** | 用于生成输出的构建模块 |

并非每个技能都需要以上所有组件。一个简单工具可能只有一个 `SKILL.md`。复杂工作流或智能体可能使用完整结构。

## 构建即可用

构建器输出一个完整的技能文件夹。将它放到你 AI 工具的 skills 目录（`.claude/skills`、`.codex/skills`、`.agent/skills` 或工具指定的位置）即可立即使用。

参见 [什么是智能体](../what-are-bmad-agents.md) 和 [什么是工作流](../what-are-workflows.md) 了解智能体和工作流各自如何使用这个基础。
