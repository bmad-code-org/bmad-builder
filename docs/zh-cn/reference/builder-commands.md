---
title: '构建器命令参考'
description: Agent Builder、Workflow Builder 和 Module Builder 所有能力、模式和路径的完整参考
---

三个核心 BMad Builder 技能的参考：Agent Builder（`bmad-agent-builder`）、Workflow Builder（`bmad-workflow-builder`）和 Module Builder（`bmad-module-builder`）。

## 能力概览

| 能力 | 菜单代码 | Agent Builder | Workflow Builder |
| ---- | -------- | ------------- | ---------------- |
| **Build Process** | BP | 构建、编辑、转换或修复智能体 | 构建、编辑、转换或修复工作流和工具 |
| **Quality Optimize** | QO | 验证和优化已有智能体 | 验证和优化已有工作流和工具 |
| **Convert** | CW | - | 将任何技能转换为 BMad 兼容的、成果驱动的等效版本，附带比较报告 |

两项能力均支持通过 `--headless` / `-H` 标志的自主/无头模式。

## 技能命名

| 上下文 | 智能体模式 | 工作流模式 |
| ------ | ---------- | ---------- |
| **独立** | `agent-{name}` | `{name}` |
| **模块内** | `{modulecode}-agent-{name}` | `{modulecode}-{name}` |

名称必须是 kebab-case 并与文件夹名匹配。智能体名称应包含 `agent`。模块内技能的模块代码前缀由用户在构建时选择。

:::caution[保留前缀]
`bmad-` 前缀保留给官方 BMad 作品。用户构建的技能不应包含它。如果转换已有 `bmad-` 前缀的技能，保留该前缀除非用户要求重命名。
:::

## Build Process（BP）

核心创建路径。六个阶段的对话式发现带你从粗糙想法到完整、测试过的技能文件夹。

### 输入类型

两个构建器都接受以下任何一种作为起点。

| 输入 | 发生什么 |
| ---- | -------- |
| 粗糙想法或描述 | 从零开始引导发现 |
| 已有 BMad 技能路径 | 编辑模式。分析现有内容，确定要改什么 |
| 非 BMad 技能、工具或代码 | 转换为 BMad 兼容结构 |
| 文档、API 规范或代码 | 自动提取意图和需求 |

### 交互模式

| 模式 | 行为 | 最适合 |
| ---- | ---- | ------ |
| **引导** | 构建器引导逐步决策、澄清模糊点、确保完整性 | 生产级技能、首次构建者 |
| **YOLO** | 一股脑倒出想法；构建器用最少提问猜测生成成品 | 快速原型、有经验的构建者 |
| **自主** | 完全无头；无交互提示，使用安全默认值 | CI/CD、批处理、编排构建 |

### 构建阶段

| 阶段 | Agent Builder | Workflow Builder |
| ---- | ------------- | ---------------- |
| 1 | **发现意图**：理解愿景；通过自然提问检测智能体类型（无状态、记忆型或自主型） | **发现意图**：理解愿景；接受任何输入格式 |
| 2 | **能力策略**：内部命令、外部技能、脚本；可演进能力决策 | **分类技能类型**：简单工具、简单工作流或复杂工作流；模块归属 |
| 3 | **收集需求**：身份、角色记忆种子、初醒领域、PULSE 行为、文件夹管辖 | **收集需求**：名称、描述、阶段、配置变量、输出制品、依赖 |
| 4 | **起草与细化**：展示大纲，迭代直到就绪 | **起草与细化**：展示计划，澄清缺口，迭代直到就绪 |
| 5 | **构建**：按智能体类型生成技能结构，lint 门 | **构建**：生成技能结构，lint 门 |
| 6 | **总结**：展示结果，提供 Quality Optimize | **总结**：展示结果，如有脚本运行单元测试，提供 Quality Optimize |

### Agent Builder：Phase 1 智能体类型检测

构建器通过自然提问确定智能体类型，而非菜单：

| 问题（自然提出） | 如果否 | 如果是 |
| ---------------- | ------ | ------ |
| 此智能体需要跨会话记忆吗？ | 无状态 | 记忆型或自主型 |
| 用户应能教它新技能吗？ | 固定能力 | 可演进能力 |
| 它在会话之间自主运行吗？ | 记忆型 | 自主型 |

对于记忆型和自主型智能体，构建器还确定**关系深度**：深度（校准式初醒，开放式发现）或聚焦（配置式初醒，引导式提问）。

### Agent Builder：Phase 2 能力策略

确定内部和外部能力的组合，以及脚本机会。

| 能力类型 | 描述 |
| -------- | ---- |
| **内部命令** | 提示词驱动的动作，各自在 `references/` 中有文件 |
| **外部技能** | 智能体按注册名调用的独立技能 |
| **脚本** | 从 LLM 卸载的确定性操作（验证、数据处理、文件操作） |
| **可演进能力** | 如启用：用户可通过编写参考随时间教智能体新能力 |

### Agent Builder：Phase 3 需求

需求因智能体类型而异。无状态智能体需要身份和能力。记忆型和自主型智能体需要以下全部。

**所有智能体类型：**

| 需求 | 描述 |
| ---- | ---- |
| **身份** | 此智能体是谁？沟通风格、决策哲学 |
| **能力** | 内部命令、外部技能、脚本 |
| **文件夹管辖** | 读边界、写边界、显式拒绝区域 |

**记忆型和自主型智能体额外需要：**

| 需求 | 描述 |
| ---- | ---- |
| **身份种子** | 2-3 句性格 DNA，写入 PERSONA.md |
| **物种级使命** | 领域特定的目标陈述，写入 CREED.md |
| **核心价值观** | 指导行为的 3-5 个价值观 |
| **常备指令** | 惊喜与取悦 + 自我改进，适配领域并附带示例 |
| **CREED 种子** | 哲学、边界、反模式（行为 + 操作） |
| **BOND 领域** | 关于主人需了解的领域特定方面 |
| **初醒领域** | 通用集之外的发现问题 |

**自主型智能体额外需要：**

| 需求 | 描述 |
| ---- | ---- |
| **PULSE 行为** | 默认唤醒行为、领域特定自主任务 |
| **命名任务路由** | 通过 `--headless {task-name}` 或 `-H {task-name}` 调用的任务 |
| **频率与安静时段** | 多久唤醒一次，何时不唤醒 |

### Workflow Builder：Phase 2-3 详情

**技能类型分类**决定模板和结构。

| 类型 | 信号 | 结构 |
| ---- | ---- | ---- |
| **简单工具** | 可组合构建模块，清晰输入/输出，通常由脚本驱动 | 单 SKILL.md，scripts 文件夹 |
| **简单工作流** | 放在一个 SKILL.md 中，几个顺序步骤，可选自主 | SKILL.md 内联步骤，可选 prompts 和 resources |
| **复杂工作流** | 多阶段、分支提示词流、渐进式展开、长时运行 | SKILL.md 路由 + `prompts/` 阶段 + `resources/` |

**Phase 3 收集的工作流特定需求：**

| 需求 | 简单工具 | 简单工作流 | 复杂工作流 |
| ---- | -------- | ---------- | ---------- |
| **输入/输出格式** | 是 | - | - |
| **可组合性** | 是 | - | - |
| **步骤** | - | 编号步骤 | 命名阶段+推进条件 |
| **无头模式** | - | 可选 | 可选 |
| **配置变量** | - | 核心 + 自定义 | 核心 + 模块特定 |
| **模块排序** | 可选 | 可选 | 推荐 |

### 构建输出

输出结构取决于智能体类型。

**无状态智能体：**

```
{skill-name}/
├── SKILL.md              # 完整身份 + 角色 + 能力
├── references/           # 能力提示词
├── agents/               # 子智能体定义（如需要）
├── scripts/              # 确定性脚本
│   └── tests/            # 脚本单元测试
└── assets/               # 模板（如需要）
```

**记忆型和自主型智能体：**

```
{skill-name}/
├── SKILL.md              # 精简引导器（约 30 行内容）
├── references/
│   ├── first-breath.md   # 初醒对话指南
│   ├── memory-guidance.md          # 会话关闭和策展实践
│   ├── capability-authoring.md     # 如启用可演进能力
│   └── {capability}.md             # 面向成果的能力提示词
├── assets/               # 圣殿种子模板
│   ├── INDEX-template.md
│   ├── PERSONA-template.md
│   ├── CREED-template.md
│   ├── BOND-template.md
│   ├── MEMORY-template.md
│   ├── CAPABILITIES-template.md
│   └── PULSE-template.md          # 仅自主型智能体
├── agents/               # 子智能体定义（如需要）
└── scripts/
    ├── init-sanctum.py   # 创建圣殿文件夹、复制模板、生成 CAPABILITIES.md
    └── tests/
```

种子模板包含发现阶段的真实内容，而非占位符。初始化脚本以技能名、文件列表和可演进标志为参数。

**Workflow Builder** 输出无论智能体类型均保持不变：

```
{skill-name}/
├── SKILL.md              # 技能指令
├── prompts/              # 复杂工作流的阶段提示词
├── resources/            # 参考数据
├── agents/               # 并行处理的子智能体定义
├── scripts/              # 确定性脚本
│   └── tests/            # 脚本单元测试
└── templates/            # 生成输出的构建模块
```

### Lint 门

完成构建前，两个构建器都运行确定性验证。

| 脚本 | 检查内容 |
| ---- | -------- |
| `scan-path-standards.py` | 路径约定：无 `{skill-root}`，项目范围用 `{project-root}`，技能内部用 `./`，无双前缀 |
| `scan-scripts.py` | 脚本可移植性、PEP 723 元数据、智能体设计、单元测试存在性 |

关键问题阻止完成。警告记录但不阻止。

## Quality Optimize（QO）

已有技能的验证和优化。并行运行确定性 lint 脚本进行即时结构检查和 LLM 扫描子智能体进行基于判断的分析。

### 预扫检查

在交互模式中，优化器：

1. 检查未提交更改并建议先提交
2. 询问技能当前是否按预期工作

在自主模式中，两项检查都跳过并在报告中记为警告。

### 扫描流水线

优化器运行三层分析。

**第 1 层：Lint 脚本**（确定性，零 token，即时）：

| 脚本 | 焦点 |
| ---- | ---- |
| `scan-path-standards.py` | 路径约定违规 |
| `scan-scripts.py` | 脚本可移植性和标准 |

**第 2 层：预扫脚本**（为 LLM 扫描器提取指标）：

| 脚本 | Agent Builder | Workflow Builder |
| ---- | ------------- | ---------------- |
| 结构/完整性预扫 | `prepass-structure-capabilities.py` | `prepass-workflow-integrity.py` |
| 提示词指标预扫 | `prepass-prompt-metrics.py` | `prepass-prompt-metrics.py` |
| 执行依赖预扫 | `prepass-execution-deps.py` | `prepass-execution-deps.py` |

**第 3 层：LLM 扫描器**（基于判断，作为并行子智能体运行）：

| 扫描器 | Agent Builder 焦点 | Workflow Builder 焦点 |
| ------ | ------------------- | --------------------- |
| **结构/完整性** | 结构、能力、身份、记忆设置、一致性 | 逻辑一致性、描述质量、推进条件、类型适配结构 |
| **提示词技巧** | Token 效率、反模式、角色声音、概述质量 | Token 效率、反模式、概述质量、渐进式展开 |
| **执行效率** | 并行化、子智能体委派、记忆加载、上下文优化 | 并行化、子智能体委派、读取回避、上下文优化 |
| **内聚性** | 角色-能力对齐、缺口、冗余 | 阶段流连贯性、目标对齐、复杂度适当性 |
| **增强机会** | 脚本自动化、自主潜力、边缘情况、惊喜 | 创意边缘情况发现、体验缺口、假设审计 |

### 报告综合

所有扫描器完成后，优化器将结果综合为统一报告，保存到 `{bmad_builder_reports}/{skill-name}/quality-scan/{timestamp}/`。

在交互模式中，展示严重级别计数的摘要并提供下一步选项：

- 直接应用修复
- 导出检查清单供手动修复
- 讨论具体发现

在自主模式中，输出含严重级别计数和报告文件路径的结构化 JSON。

### 优化指导

并非每个建议都应采纳。优化器传达这些决策规则：

- **保留措辞**，如果它捕捉了意图的声音。精简并不总是对角色驱动技能更好
- **保留内容**，如果它为 AI 增加清晰度，即使人类觉得显而易见
- **优先脚本化**确定性操作；**优先提示词**创意或判断任务
- **拒绝更改**，如果它们扁平化个性，除非明确要求中性语调

## Convert（CW）

一条命令将任何现有技能转换为 BMad 兼容的、成果驱动的等效版本。接受不合规技能（臃肿、结构差或不遵循 BMad 实践）并产出干净版本。与 Build Process 的编辑/重建模式不同，`--convert` 始终无头运行并产出可视化比较报告。

### 用法

```
--convert <path-or-url> [-H]
```

`--convert` 标志隐含无头模式。接受本地技能路径或 URL。

### 流程

| 步骤 | 发生什么 |
| ---- | -------- |
| **1. 捕获** | 获取或读取原始技能，保存副本用于比较 |
| **2. 重建** | 从意图完全无头重建：提取技能的成就，应用 BMad 成果驱动最佳实践 |
| **3. 报告** | 测量两个版本，分类变更内容和原因，生成交互式 HTML 比较报告 |

### 比较报告

HTML 报告包含：

| 区域 | 内容 |
| ---- | ---- |
| **横幅** | 整体 token 减少百分比 |
| **指标表** | 行数、词数、字符数、节数、文件数、估算 token，带可视化条形图 |
| **变更内容** | 分类差异（臃肿移除、结构重组、最佳实践对齐）附严重级别和示例 |
| **保留内容** | 证明其价值的内容：LLM 不被明确告知就无法正确遵循的指令 |
| **评语** | 转换的一句话总结 |

报告保存到 `{bmad_builder_reports}/convert-{skill-name}/`。

### 何时使用 Convert vs Build Process

| 场景 | 使用 |
| ---- | ---- |
| 你有任何非 BMad 兼容技能并想快速转换 | `--convert` |
| 你有臃肿技能并想要精简替换附比较报告 | `--convert` |
| 你想交互式讨论要改什么 | Build Process（编辑模式） |
| 你想从零重新思考技能，带完整发现 | Build Process（重建模式） |
| 你想要详细质量分析而不重建 | Quality Optimize |

## Module Builder

Module Builder（`bmad-module-builder`）处理模块级规划、脚手架和验证。它在比 Agent Builder 和 Workflow Builder 更高的层级运行；它将这些构建器产出的内容编排为连贯、可安装的模块。

### 能力概览

| 能力 | 菜单代码 | 作用 |
| ---- | -------- | ---- |
| **Ideate Module** | IM | 通过创意引导进行头脑风暴和规划模块 |
| **Create Module** | CM | 将技能打包为可安装模块：多技能用 setup 技能，独立用自注册 |
| **Validate Module** | VM | 检查多技能和独立模块的结构完整性与条目质量 |

### Ideate Module（IM）

帮助你从零规划模块的头脑风暴会话。构建器作为创意协作者，引出想法、探索可能性，并引导你找到正确的架构。

| 方面 | 详情 |
| ---- | ---- |
| **交互** | 仅交互式；无无头模式 |
| **输入** | 一个想法或粗糙描述 |
| **输出** | 计划文档保存到 `{bmad_builder_reports}` |

**覆盖内容：**

- 问题空间探索和创意头脑风暴
- 架构决策：单智能体+能力 vs 多技能 vs 混合
- 独立模块或现有模块的扩展
- 外部依赖（CLI 工具、MCP 服务器）
- UI 和可视化机会
- Setup 技能在配置之外的扩展
- 每技能能力定义及帮助 CSV 元数据
- 配置变量和合理默认值

计划文档使用带 YAML frontmatter 的可恢复模板，使长时头脑风暴会话能在上下文压缩后存活。

**构思之后：** 使用 Agent Builder（BA）或 Workflow Builder（BW）构建每个计划的技能，然后返回 Create Module（CM）搭建模块脚手架。

### Create Module（CM）

将构建好的技能打包为可安装 BMad 模块。自动检测单技能 vs 多技能输入并推荐适当方式。支持 `--headless` / `-H`。

| 方面 | 详情 |
| ---- | ---- |
| **交互** | 引导式或无头 |
| **输入** | 技能文件夹或单技能路径（或 SKILL.md 文件），可选计划文档 |
| **输出** | 多技能模块的 setup 技能，或独立模块的自注册文件 |

**执行内容：**

1. 读取 SKILL.md 文件以理解每个技能
2. 检测单技能 vs 多技能并与用户确认打包方式
3. 收集模块身份（名称、代码、描述、版本、问候语）
4. 定义帮助 CSV 条目：能力、菜单代码、排序、关系
5. 捕获配置变量和外部依赖
6. 搭建模块基础设施

**多技能输出：** 专用 `{code}-setup/` 文件夹，含合并脚本、清理脚本和通用 SKILL.md。

**独立输出：** 技能中嵌入 `assets/module-setup.md`、`assets/module.yaml` 和 `assets/module-help.csv`，加上 `scripts/` 中的合并脚本和分发用的 `.claude-plugin/marketplace.json`。技能的 SKILL.md 被更新以在激活时检查注册状态。

### Validate Module（VM）

验证模块结构完整且准确。自动检测带 setup 技能的多技能模块和带自注册的独立模块。结合确定性验证脚本和基于 LLM 的质量评估。

| 方面 | 详情 |
| ---- | ---- |
| **交互** | 交互式 |
| **输入** | 模块技能文件夹或单技能路径 |
| **输出** | 验证报告 |

**结构检查**（脚本驱动）：

| 检查 | 捕获什么 |
| ---- | -------- |
| 模块结构 | 缺失 setup 技能或独立文件（`module-setup.md`、合并脚本） |
| 覆盖率 | 没有 CSV 条目的技能、指向不存在技能的孤立条目 |
| 菜单代码 | 模块内重复代码 |
| 引用 | before/after 字段指向不存在的能力 |
| 必填字段 | CSV 行中缺失技能名、显示名、菜单代码或描述 |
| module.yaml | 缺失 code、name 或 description |

**质量评估**（LLM 驱动）：

- 描述准确性：每个条目是否匹配技能实际功能？
- 描述质量：简洁、面向行动、具体、不过于冗长
- 完整性：所有不同能力是否注册为独立行？
- 排序：before/after 关系是否合理？
- 菜单代码：是否直觉且易记？

## 触发短语

| 意图 | 短语 | 构建器 | 路由 |
| ---- | ---- | ------ | ---- |
| 新建 | "create/build/design an agent" | Agent | `prompts/build-process.md` |
| 新建 | "create/build/design a workflow/skill/tool" | Workflow | `prompts/build-process.md` |
| 编辑 | "edit/modify/update an agent" | Agent | `prompts/build-process.md` |
| 编辑 | "edit/modify/update a workflow/skill" | Workflow | `prompts/build-process.md` |
| 转换 | "convert this to a BMad agent" | Agent | `prompts/build-process.md` |
| 转换 | "convert this to a BMad skill" | Workflow | `prompts/build-process.md` |
| 转换 | `--convert <path-or-url>` | Workflow | `./references/convert-process.md` |
| 优化 | "quality check/validate/optimize/review agent" | Agent | `prompts/quality-optimizer.md` |
| 优化 | "quality check/validate/optimize/review workflow/skill" | Workflow | `prompts/quality-optimizer.md` |
| 构思 | "ideate module/plan a module/brainstorm a module" | Module | `./references/ideate-module.md` |
| 创建 | "create module/build a module/scaffold a module" | Module | `./references/create-module.md` |
| 验证 | "validate module/check module" | Module | `./references/validate-module.md` |
