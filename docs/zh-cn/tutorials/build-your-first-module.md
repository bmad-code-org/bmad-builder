---
title: '构建你的第一个模块'
description: 使用 Module Builder 从想法到可安装包，创建一个完整的 BMad 模块
---

本教程带你从最初的想法到一个可用的、可安装的 BMad 模块，包含帮助注册和配置。

## 你将学到

- 使用 Ideate Module（IM）能力规划模块
- 在单智能体和多工作流之间选择
- 使用 Agent Builder 和 Workflow Builder 构建单个技能
- 使用 Create Module（CM）搭建 setup 技能脚手架
- 使用 Validate Module（VM）验证模块

:::note[前置条件]

- 项目中已注册 BMad Builder 模块（首次使用请运行 `bmad-bmb-setup`）
- 对智能体和工作流有基本了解（参见 **[什么是智能体](../../explanation/what-are-bmad-agents.md)** 和 **[什么是工作流](../../explanation/what-are-workflows.md)**）
:::

:::tip[快速路径]
已经构建好技能？跳到 **步骤 3：搭建模块脚手架** 进行打包。只需验证已有模块？跳到 **步骤 4：验证**。
:::

## 理解模块

BMad 模块将技能打包在一起，使其可被发现和配置。Module Builder 根据你构建的内容提供两种方式：

| 方式 | 何时使用 | 生成什么 |
| ---- | -------- | -------- |
| **Setup 技能** | 2+ 个技能的文件夹 | 专用 `{code}-setup` 技能，含配置和帮助资源 |
| **自注册** | 单个独立技能 | 注册嵌入技能自身的 `assets/` 文件夹 |

两者产出相同的注册制品：`module.yaml`（身份和配置变量）和 `module-help.csv`（能力条目），注册到 `bmad-help`。

参见 **[什么是模块](../../explanation/what-are-modules.md)** 了解这些选择背后的架构。

## 步骤 1：规划模块

从 Ideate Module 能力开始。

:::note[示例]
**你：** "I want to ideate a module"

**构建器：** 开始头脑风暴会话，探索模块的目的、受众和能力结构。
:::

构思会话覆盖：

| 主题 | 你将决定什么 |
| ---- | ------------ |
| **愿景** | 问题空间、目标用户、核心价值 |
| **架构** | 单智能体、多工作流或混合 |
| **智能体类型** | 每个智能体：无状态、记忆型或自主型（参见 [什么是智能体](../../explanation/what-are-bmad-agents.md)） |
| **记忆** | 多智能体模块：个人记忆、共享模块记忆或两者 |
| **模块类型** | 独立或现有模块的扩展 |
| **技能** | 每个计划技能的目的、能力和关系 |
| **配置** | 自定义安装问题和变量 |
| **依赖** | 外部 CLI 工具、MCP 服务器、Web 服务 |

输出是保存到报告文件夹的**计划文档**。构建每个技能时将引用它。

## 步骤 2：构建技能

逐个构建每个技能。

| 技能类型 | 构建器 | 菜单代码 |
| -------- | ------ | -------- |
| 智能体 | Agent Builder | BA |
| 工作流或工具 | Workflow Builder | BW |

构建每个技能时分享计划文档作为上下文，让构建器知道它在模块中的位置。对于智能体，构建器通过对话式发现检测正确的类型（无状态、记忆型或自主型）并相应调整构建过程。

:::caution[先构建再打包]
在搭建模块脚手架之前，先构建并测试每个技能。Create Module 步骤读取你完成的技能以生成准确的帮助条目。
:::

## 步骤 3：搭建模块脚手架

运行 Create Module（CM）打包你完成的技能。

:::note[示例]
**你：** "I want to create a module" 或提供你的技能文件夹路径（或单个技能）。

**构建器：** 读取你的技能，检测是多技能还是单技能模块，确认方式，并搭建输出脚手架。
:::

### 多技能模块

构建器生成专用 setup 技能：

```
your-skills-folder/
├── {code}-setup/                # 生成的 setup 技能
│   ├── SKILL.md                 # 配置指令
│   ├── scripts/                 # 配置合并和清理脚本
│   │   ├── merge-config.py
│   │   ├── merge-help-csv.py
│   │   └── cleanup-legacy.py
│   └── assets/
│       ├── module.yaml          # 模块身份和配置变量
│       └── module-help.csv      # 能力条目
├── your-agent-skill/
├── your-workflow-skill/
└── ...
```

### 独立模块

构建器将注册嵌入技能本身：

```
your-skill/
├── SKILL.md                     # 已更新，含注册检查
├── assets/
│   ├── module-setup.md          # 自注册参考
│   ├── module.yaml              # 模块身份和配置变量
│   └── module-help.csv          # 能力条目
├── scripts/
│   ├── merge-config.py          # 配置合并脚本
│   └── merge-help-csv.py        # 帮助 CSV 合并脚本
└── ...
```

父级目录还会生成一个 `.claude-plugin/marketplace.json` 用于分发。

## 步骤 4：验证

运行 Validate Module（VM）检查结构和质量问题。

:::note[示例]
**你：** "Validate my module at ./my-skills-folder"

**构建器：** 运行结构和质量检查，然后报告发现。
:::

| 检查类型 | 捕获什么 |
| -------- | -------- |
| **结构** | 缺失文件、孤立条目、重复菜单代码、损坏引用 |
| **质量** | 不准确的描述、缺失能力、低质量条目 |

修复发现的问题并重新验证，直到通过。

## 你构建了什么

你的模块已准备好分发。多技能模块通过 setup 技能安装；独立模块在首次运行时自注册。无论哪种方式，能力都会出现在 `bmad-help` 中，配置自动持久化。

## 快速参考

| 能力 | 菜单代码 | 何时使用 |
| ---- | -------- | -------- |
| Ideate Module | IM | 从零规划新模块 |
| Build an Agent | BA | 创建智能体技能 |
| Build a Workflow | BW | 创建工作流或工具技能 |
| Create Module | CM | 将技能打包为可安装模块 |
| Validate Module | VM | 检查完整性和准确性 |

## 常见问题

### 创建前必须先构思吗？

不必。如果你已经知道模块应包含什么，直接跳到 Create Module（CM）。构思在你仍在塑造概念时有帮助。

### 可以后续添加技能吗？

可以。构建新技能并在文件夹上重新运行 Create Module（CM）。反僵尸模式确保现有 setup 技能被干净替换。

### 如果模块只有一个技能呢？

Module Builder 自动处理。给它一个单技能，它会推荐**独立自注册**方式，注册直接嵌入技能并在首次运行或用户传入 `setup`/`configure` 时触发。

### 模块可以扩展另一个模块吗？

可以。在构思或创建时告诉构建器你的模块是扩展。你的帮助 CSV 条目可在 before/after 排序字段中引用父模块的能力。

## 获取帮助

- **[什么是模块](../../explanation/what-are-modules.md)**：概念和架构
- **[模块配置](../../explanation/module-configuration.md)**：Setup 技能内部和配置模式
- **[构建器命令参考](../../reference/builder-commands.md)**：所有构建器能力
- **[Discord](https://discord.gg/gk8jAdXWmj)**：社区支持

:::tip[关键要点]
工作流是 IM，然后每个技能用 BA/BW，然后 CM 打包，然后 VM 验证。单技能模块不需要额外的 setup 基础设施。
:::
