---
title: '分发你的模块'
description: 配置 Git 仓库分享你的 BMad 模块，让任何人都能一条命令安装
---

本指南介绍如何将 BMad 模块发布到 Git 仓库，并通过 `.claude-plugin/marketplace.json` 清单让任何人都能一条命令安装。

## 何时使用

- 你有一个准备公开或在组织内分享的模块
- 他人应能通过 BMad 安装器安装它
- 仓库可托管一个或多个模块

## 何时跳过

- 模块仅供个人在单一项目中使用。保留技能在项目中即可。
- 模块尚不稳定。稳定后再分发。

:::note[前置条件]

- 一个已完成并验证的 BMad 模块（参见 **[构建你的第一个模块](../../tutorials/build-your-first-module.md)**）
- 任何 Git 托管平台上的仓库（GitHub、GitLab、Bitbucket 或自托管）
- 本地已安装 Git
:::

:::tip[快速路径]
从 [BMad Module Template](https://github.com/bmad-code-org/bmad-module-template) 开始。在 GitHub 上点击 **Use this template**，将技能添加到 `skills/` 目录，更新 `marketplace.json`，然后推送。如果你已有包含技能的仓库，使用 Create Module（CM）直接搭建清单和注册文件。
:::

## 步骤 1：配置插件清单

模块通过仓库根目录的 `.claude-plugin/marketplace.json` 清单被发现。Create Module 为你生成此文件。发布前请验证并完善。

:::tip[安装器支持]
BMad Method 安装器（`npx bmad-method install`）支持从任何 Git 托管平台或本地路径安装自定义模块。用户可交互式安装或通过 `--custom-source <url-or-path>` 安装。详见 [BMad Method 安装指南](https://docs.bmad-method.org/zh-cn/how-to/install-custom-modules/)。
:::

此格式适用于任何支持技能的平台，不仅限于 Claude。我们使用 claude 文件作为约定以支持任何基于技能的平台。

单模块的最小清单：

```json
{
  "name": "my-module",
  "owner": { "name": "Your Name" },
  "license": "MIT",
  "homepage": "https://github.com/your-github/my-module",
  "repository": "https://github.com/your-github/my-module",
  "keywords": ["bmad", "your-domain"],
  "plugins": [
    {
      "name": "my-module",
      "source": "./",
      "description": "What your module does in one sentence.",
      "version": "1.0.0",
      "author": { "name": "Your Name" },
      "skills": [
        "./skills/my-agent",
        "./skills/my-workflow"
      ]
    }
  ]
}
```

| 字段 | 用途 |
| ---- | ---- |
| **name** | 包标识符，小写加连字符 |
| **plugins[].source** | 从仓库根到模块技能文件夹父目录的路径 |
| **plugins[].skills** | 每个技能目录的相对路径数组 |
| **plugins[].version** | 语义版本；每次发布时递增 |

对于发布多个模块的仓库，在 `plugins` 数组中为每个模块添加条目，指向各自的技能目录。

## 步骤 2：组织仓库结构

组织仓库使技能可相对于 `marketplace.json` 被定位。

### 单模块仓库

```
my-module/
├── .claude-plugin/
│   └── marketplace.json
├── skills/
│   ├── my-agent/
│   │   ├── SKILL.md
│   │   ├── prompts/
│   │   └── scripts/
│   ├── my-workflow/
│   │   ├── SKILL.md
│   │   └── prompts/
│   └── mymod-setup/             # 由 Create Module（CM）生成
│       ├── SKILL.md
│       ├── assets/
│       │   ├── module.yaml
│       │   └── module-help.csv
│       └── scripts/
│           ├── merge-config.py
│           ├── merge-help-csv.py
│           └── cleanup-legacy.py
├── README.md
└── LICENSE
```

### 独立单技能模块

```
my-skill/
├── .claude-plugin/
│   └── marketplace.json
├── skills/
│   └── my-skill/
│       ├── SKILL.md
│       ├── assets/
│       │   ├── module-setup.md
│       │   ├── module.yaml
│       │   └── module-help.csv
│       ├── references/
│       └── scripts/
│           ├── merge-config.py
│           └── merge-help-csv.py
├── README.md
└── LICENSE
```

### 多模块市场仓库

```
my-marketplace/
├── .claude-plugin/
│   └── marketplace.json          # plugins[] 中包含多个条目
├── skills/
│   ├── module-a/
│   │   ├── skill-one/
│   │   ├── skill-two/
│   │   └── moda-setup/
│   └── module-b/
│       └── standalone-skill/
├── README.md
└── LICENSE
```

:::caution[技能路径必须匹配]
`marketplace.json` 中的 `skills` 数组必须与相对于仓库根的实际目录路径匹配。如果你重组了文件夹，请更新清单。
:::

## 步骤 3：验证清单

发布前确认清单准确。

### 检查技能路径

`skills` 数组中的每个路径必须指向包含 `SKILL.md` 文件的目录。

### 检查模块注册文件

多技能模块需要 setup 技能中的 `assets/module.yaml` 和 `assets/module-help.csv`。独立模块将这些文件保存在技能自身的 `assets/` 文件夹中。

### 运行 Validate Module

```
"Validate my module at ./skills"
```

Validate Module（VM）检查缺失文件、孤立条目和其他结构问题。修复标记的问题后再发布。

## 步骤 4：发布

将仓库推送到 Git 托管平台（GitHub、GitLab、Bitbucket 或自托管）。仓库可访问后，任何有权限的人都能安装。

### 安装你的模块

用户通过 BMad 安装器安装自定义模块：

```bash
# 交互式：安装器提示输入自定义源 URL 或路径
npx bmad-method install

# 非交互式：直接指定源
npx bmad-method install --custom-source https://github.com/your-org/my-module --tools claude-code --yes
```

安装器接受 HTTPS URL、SSH URL、带深层路径的 URL（如 `/tree/main/subdir`）和本地文件路径。

### 私有或组织模块

对于私有仓库，用户需要 Git 访问权限来克隆。安装器使用机器上配置的任何 Git 认证。

### 版本管理

用语义版本标记发布。安装默认从默认分支拉取，除非用户指定标签或分支。

## 你将获得

发布后，用户可以：

- 通过 BMad 安装器从任何 Git URL 或本地路径安装
- 运行 setup 技能注册到 `bmad-help`
- 通过帮助系统浏览模块能力
- 获取 `module.yaml` 中定义的配置提示

## 步骤 5：在市场上架（可选）

将模块提交到 [BMad Plugins Marketplace](https://github.com/bmad-code-org/bmad-plugins-marketplace)，与官方模块一起获得曝光。上架不是安装的必要条件，但能增加可发现性和审查后的信任层级徽章。

参见市场 [CONTRIBUTING.md](https://github.com/bmad-code-org/bmad-plugins-marketplace/blob/main/CONTRIBUTING.md) 了解提交流程。

## 建议

- 包含一个 `README.md`，说明模块功能、安装方式和外部依赖
- 添加 `LICENSE` 文件。MIT 是开源 BMad 模块的常见选择
- 保持 `marketplace.json` 版本与发布标签同步
- 外部依赖（CLI 工具、MCP 服务器）应在 README 中记录，并由 setup 技能检测
- 每次发布前运行 `Validate Module（VM）` 以捕获回归问题
