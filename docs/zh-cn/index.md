---
title: 欢迎
description: BMad Builder —— 筑梦架构
---

# BMad Builder —— BMad 方法生态模块

**筑梦架构（Build More, Architect Dreams）。**

## 梦想

如果你的 AI 能记住一切呢？一个记录你每次 PR 的健身教练。一个比你更了解你笔下角色的写作搭档。一个已经熟悉你工作习惯的研究助手。

BMad Builder 让你创建：

- **私人 AI 伙伴**：具备记忆、随时间成长的智能体
- **领域专家**：覆盖法律、医疗、创意、技术等任何领域的专业智能体
- **工作流自动化**：引导你完成复杂任务的结构化流程
- **自定义模块**：将智能体和工作流打包成可分享的模块

## 差异化优势

| 特性 | 为什么重要 |
| ---- | ---------- |
| **持久记忆** | 智能体跨会话记忆，持续改进 |
| **可组合** | 你的作品与整个 BMad 生态无缝协作 |
| **技能标准兼容** | 基于开放标准，适配任何 AI 工具 |
| **可分享** | 打包并分发你的模块给 BMad 社区 |

## 快速开始

### 1. 注册模块

首次使用时，运行 `bmad-bmb-setup` 在项目中注册 BMad Builder。它会收集你的偏好（姓名、语言、输出路径），并将构建器的能力注册到帮助系统，让 `bmad-help` 能够引导你。

:::tip[单技能模块]
如果你安装的模块只包含一个技能，该技能会在首次运行时自行注册，无需额外配置步骤。
:::

### 2. 开始构建

调用 **Agent Builder** 或 **Workflow Builder**，描述你想创建的内容。两者都会引导你回答一系列问题，最终生成一个可直接使用的技能文件夹。

| 目标 | 构建器 | 菜单代码 |
| ---- | ------ | -------- |
| 带记忆的 AI 伙伴 | Agent Builder | BA |
| 结构化流程/工具 | Workflow Builder | BW |
| 将技能打包为模块 | Module Builder | CM |

### 3. 使用你的技能

构建器会生成一个完整的技能文件夹。将它复制到你 AI 工具的 skills 目录（`.claude/skills/`、`.codex/skills/`、`.agents/skills/` 或工具指定的位置）即可立即使用。

:::tip[自定义模块安装]
BMad Method 安装器支持从任何 Git 托管平台（GitHub、GitLab、Bitbucket、自托管）或本地路径安装自定义模块。详见 [BMad Method 安装指南](https://docs.bmad-method.org/zh-cn/how-to/install-custom-modules/)。
:::

:::tip[不需要打包成模块]
如果你只是为个人使用而构建，不需要打包成模块。直接复制技能文件夹即可。模块打包（包含 `bmad-help` 注册和配置）是为了分享或更丰富的可发现性。
:::

### 4. 了解更多

参见 [构建器命令参考](./reference/builder-commands.md) 了解所有能力、模式和阶段。

## 你能构建什么

| 领域 | 示例 |
| ---- | ---- |
| **个人** | 日记伙伴、习惯教练、学习导师、能记住你的友好个人伙伴 |
| **职业** | 代码审查员、文档专家、工作流自动化 |
| **创意** | 故事架构师、角色开发者、战役设计师 |
| **任意领域** | 任何你能描述为可重复流程的事物 |

## 设计模式

用以下指南构建更好的技能，均来自真实的 BMad 开发经验。

| 指南 | 你将学到 |
| ---- | -------- |
| **[渐进式展开](./explanation/progressive-disclosure.md)** | 如何结构化技能，让它在每个时刻只加载所需上下文 |
| **[子智能体模式](./explanation/subagent-patterns.md)** | 六种并行与层级编排模式 |
| **[技能编写最佳实践](./explanation/skill-authoring-best-practices.md)** | 核心原则、质量维度与反模式 |

## 文档

| 章节 | 用途 |
| ---- | ---- |
| **[构建你的第一个模块](./tutorials/build-your-first-module.md)** | 从规划、构建、脚手架到验证，完成一个完整模块 |
| **[分发你的模块](./how-to/distribute-your-module.md)** | 通过任何 Git 托管平台分享你的模块，让任何人都能安装 |
| **[概念](./explanation/)** | 智能体类型、记忆架构、工作流、技能及其关联 |
| **[设计模式](./explanation/#design-patterns)** | 渐进式展开、子智能体编排、编写最佳实践 |
| **[参考](./reference/)** | 构建器命令、工作流模式 |

## 社区

- **[Discord](https://discord.gg/gk8jAdXWmj)**：获取帮助、分享你的成果
- **[GitHub](https://github.com/bmad-code-org/bmad-builder)**：源代码
- **[BMad 方法](https://docs.bmad-method.org/zh-cn/)**：核心框架
