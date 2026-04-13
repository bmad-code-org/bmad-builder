---
title: '模块配置与 Setup 技能'
description: BMad 模块如何通过 setup 技能处理用户配置，何时使用配置与替代方案，以及如何注册到帮助系统
---

BMad 模块将其能力注册到帮助系统，并可选地收集用户偏好。多技能模块使用专用 **setup 技能**完成此任务。单技能独立模块在首次运行时自行注册。

创建自己的模块时，你可以添加配置技能，或在每个技能中嵌入该功能（独立模式）。对于超过 1-2 个技能的模块，setup 技能是更好的选择。

## 何时需要配置

大多数模块根本不需要配置。添加可配置值之前，考虑是否有更简单的替代方案。

| 方式 | 何时使用 |
| ---- | -------- |
| **合理默认值** | 变量对大多数用户有一个明显正确的答案，可在具体技能首次运行时覆盖或更新 |
| **智能体记忆** | 模块使用智能体模式，智能体可通过对话学习偏好 |
| **配置** | 值确实因项目而异，且无法在运行时推断 |

:::tip[独立技能]
如果你构建的是单个独立智能体或工作流，不需要单独的 setup 技能。Module Builder 可将其打包为**独立自注册模块**，注册逻辑通过 `assets/module-setup.md` 参考文件直接嵌入技能，在首次激活或用户传入 `setup`/`configure` 时运行。
:::

## 模块注册的作用

模块注册服务于两个目的：

| 目的 | 发生什么 |
| ---- | -------- |
| **配置** | 收集用户偏好并写入共享配置文件 |
| **帮助注册** | 将模块能力添加到项目级帮助系统，让用户能发现它们 |

### 为什么要注册到帮助系统？

`bmad-help` 技能读取 `module-help.csv` 来了解可用能力、检测已完成的能力（通过检查输出位置中的制品），并根据依赖图推荐下一步。没有注册，`bmad-help` 无法发现或推荐你模块的能力，只能依赖技能头部的基本信息。帮助系统提供更丰富的细节：参数、与其他技能的关系、输入输出及其他编写的元数据。如果技能有多个能力，每个能力都有自己的帮助条目。

### 两条注册路径

| 路径 | 何时使用 | 工作方式 |
| ---- | -------- | -------- |
| **Setup 技能** | 多技能模块（2+ 技能） | 专用 `{code}-setup` 技能为所有技能处理注册 |
| **自注册** | 单技能独立模块 | 技能自身在首次运行或用户传入 `setup`/`configure` 时注册 |

Module Builder 根据输入检测使用哪条路径：一组技能触发 setup 技能方式，单个技能触发独立方式。

## 配置文件

Setup 技能写入 `{project-root}/_bmad/` 中的三个文件：

| 文件 | 范围 | 内容 |
| ---- | ---- | ---- |
| `config.yaml` | 共享，提交到 git | 根级核心设置，加上每个模块的区域（含元数据和模块特定值） |
| `config.user.yaml` | 个人，gitignored | 仅用户设置如 `user_name` 和 `communication_language` |
| `module-help.csv` | 共享，提交到 git | 模块暴露的每项能力一行 |

核心设置（如 `output_folder` 和 `document_output_language`）位于 `config.yaml` 的根级，所有模块共享。每个模块还有自己的区域，按模块代码索引。

## module.yaml 文件

每个模块在 `assets/module.yaml` 文件中声明身份和可配置变量。多技能模块中，该文件在 setup 技能内。独立模块中，在技能自身的 `assets/` 文件夹内。此文件驱动向用户展示的提示和写入配置的值。

```yaml
code: mymod
name: 'My Module'
description: 'What this module does'
module_version: 1.0.0
default_selected: false
module_greeting: >
  Welcome message shown after setup completes.

my_output_folder:
  prompt: 'Where should output be saved?'
  default: '{project-root}/_bmad-output/my-module'
  result: '{project-root}/{value}'
```

带有 `prompt` 字段的变量会在配置时向用户展示。`default` 值在用户接受默认值时使用。给变量添加 `user_setting: true` 会将其路由到 `config.user.yaml` 而非共享配置。

:::caution[字面 Token]
`{project-root}` 是配置值中的字面 token。永远不要用实际路径替代它。它向消费工具发出信号：该值相对于项目根目录。
:::

## 无需配置的帮助注册

你可能不需要任何可配置值，但仍想将模块注册到帮助系统。以下情况注册仍有价值：

- SKILL.md frontmatter 中的技能描述无法在保持简洁的同时完整传达模块功能
- 你想表达能力排序、阶段约束或 CSV 支持的其他元数据
- 智能体有许多用户应能发现的内部能力
- 模块能做的不同事情超过三件

对于更简单的场景，以下替代方案通常足够：

| 替代方案 | 提供什么 |
| -------- | -------- |
| **SKILL.md 概述区域** | 技能正文顶部的简洁摘要；`--help` 系统扫描此区域以展示用户帮助，保持简洁 |
| **脚本头部注释** | 在每个脚本顶部描述用途、用法和标志 |

如果这些能覆盖你的可发现性需求，完全可以跳过 setup 技能。

## module-help.csv 文件

CSV 将模块能力注册到帮助系统。每行描述用户可发现和调用的一项能力。文件有 13 列：

```csv
module,skill,display-name,menu-code,description,action,args,phase,after,before,required,output-location,outputs
```

### 列指南

| 列 | 用途 |
| -- | ---- |
| **module** | 模块显示名称。在帮助输出中分组条目 |
| **skill** | 技能文件夹名称（如 `bmad-agent-builder`）；必须匹配实际目录名 |
| **display-name** | 帮助菜单中显示的用户可见标签（如"Build an Agent"） |
| **menu-code** | 1-3 字母短代码，在帮助中显示为 `[CODE]`，模块内唯一，直觉助记 |
| **description** | 此能力做什么。简洁、面向行动、足够具体以让 `bmad-help` 正确路由 |
| **action** | 技能内的动作名称。当一个技能暴露多个能力时区分它们 |
| **args** | 能力接受的参数（如 `[-H] [path]`），在帮助中显示 |
| **phase** | 能力何时可用：`anytime` 或工作流阶段如 `1-analysis`、`2-planning` |
| **after** | 应在此能力之前完成的能力：格式 `skill-name:action`，多个用逗号分隔 |
| **before** | 应在此能力之后运行的能力，格式同 `after` |
| **required** | `true` 表示这是阶段推进的阻塞门，否则 `false` |
| **output-location** | 配置变量名（如 `output_folder`）；`bmad-help` 从配置解析以扫描完成制品 |
| **outputs** | `bmad-help` 在输出位置查找的文件模式以检测完成（如"quality report"） |

### bmad-help 如何使用这些条目

`after`/`before` 列创建一个**依赖图**，`bmad-help` 遍历它来推荐下一步。`required=true` 条目是阻塞门；`bmad-help` 不会建议后续阶段能力，直到必需门通过。`output-location` 和 `outputs` 列启用**完成检测**：`bmad-help` 扫描这些路径以查找匹配制品来确定已完成的工作。

### 示例条目

```csv
module,skill,display-name,menu-code,description,action,args,phase,after,before,required,output-location,outputs
BMad Builder,bmad-agent-builder,Build an Agent,BA,"Create, edit, convert, or fix an agent skill.",build-process,"[-H] [description | path]",anytime,,bmad-agent-builder:quality-optimizer,false,output_folder,agent skill
```

注册时，这些行会合并到项目级的 `_bmad/module-help.csv`，替换该模块的所有现有行（反僵尸模式）。

## 反僵尸模式

两个合并脚本都使用反僵尸模式：写入模块新值之前，先移除该模块代码的所有现有条目。这防止过时的配置或帮助条目在模块更新后残留。重复运行 setup 始终安全。

## 遗留目录清理

配置数据迁移且单独文件被合并脚本清理后，一个独立的清理步骤从 `_bmad/` 移除安装器的按模块目录树。这些目录包含已安装到工具 skills 目录的技能文件，配置合并后就是冗余的。

移除任何目录前，清理脚本会验证其包含的每个技能都存在于安装位置。没有技能的目录（如 `_config/`）直接移除。脚本是幂等的；清理后再次运行 setup 是安全的。

## 设计指导

配置用于**基本的项目级设置**：输出文件夹、语言偏好、功能开关。保持可配置值数量少。

| 模式 | 配置角色 |
| ---- | -------- |
| **智能体模式** | 优先使用智能体记忆处理每用户偏好。仅对必须跨项目共享的值使用配置 |
| **工作流模式** | 对因项目而异的输出位置和行为开关使用配置 |
| **纯技能模式** | 谨慎使用配置。如果技能使用合理默认值即可工作，跳过配置 |

大量工作流定制（步骤覆盖、条件分支、模板选择）是独立议题，将在专门文档中介绍。

## 使用 Module Builder 创建模块

**Module Builder**（`bmad-module-builder`）自动化模块创建。它提供三项能力：

| 能力 | 菜单代码 | 作用 |
| ---- | -------- | ---- |
| **Ideate Module** | IM | 通过引导式发现进行头脑风暴和规划；产出计划文档 |
| **Create Module** | CM | 将技能打包为可安装 BMad 模块（setup 技能或独立自注册） |
| **Validate Module** | VM | 检查模块结构是否完整、准确且正确注册 |

**多技能模块流程：**

1. 运行 **Ideate Module（IM）** 进行头脑风暴和规划
2. 使用 **Agent Builder（BA）** 或 **Workflow Builder（BW）** 构建每个技能
3. 运行 **Create Module（CM）**。它生成专用的 `-setup` 技能，包含 `module.yaml`、`module-help.csv` 和合并脚本
4. 运行 **Validate Module（VM）** 验证一切连接正确

**单技能模块流程：**

1. 使用 **Agent Builder（BA）** 或 **Workflow Builder（BW）** 构建技能
2. 用技能路径运行 **Create Module（CM）**。它直接在技能中嵌入自注册（`assets/module-setup.md`、`assets/module.yaml`、`assets/module-help.csv`），并生成分发用的 `marketplace.json`
3. 运行 **Validate Module（VM）** 验证

Module Builder 自动检测单技能 vs 多技能输入，推荐适当方式。

参见 **[什么是模块](../what-are-modules.md)** 了解概念和架构决策，或 **[构建器命令参考](../../reference/builder-commands.md)** 了解详细能力文档。
