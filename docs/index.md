---
title: Welcome
description: BMad Builder - Build More, Architect Dreams
---

# BMad Builder - A BMad Method EcoSystem Module

:::caution[Replaced by Toolsmith in BMad Method v7]
BMad Builder is no longer developed. These docs cover its last release, `v2.2.2`, which the BMad v6 installer still installs. To build skills, agents, and modules, upgrade to BMad Method v7 and use Toolsmith: read the [Toolsmith docs](https://docs.bmad-method.org/toolsmith/toolsmith/), [install BMad](https://docs.bmad-method.org/start/install-bmad/), and convert a module you built here with [Migrate an Old Module](https://docs.bmad-method.org/toolsmith/migrate-an-old-module/).
:::

**Build More, Architect Dreams.**

## The Dream

What if your AI remembered everything? A fitness coach that tracks every PR. A writing partner that knows your characters better than you do. A research assistant that already knows how you work.

BMad Builder lets you create:

- **Personal AI Companions**: Agents with memory that evolve with you over time
- **Domain Experts**: Specialists for any field: legal, medical, creative, technical
- **Workflow Automations**: Structured processes that guide you through complex tasks
- **Custom Modules**: Bundle agents and workflows into shareable packages

## What Makes It Different

| Feature               | Why It Matters                                              |
| --------------------- | ----------------------------------------------------------- |
| **Persistent Memory** | Agents remember across sessions and keep improving          |
| **Composable**        | Your creations work alongside the entire BMad ecosystem     |
| **Skill-Compliant**   | Built on open standards that work with any AI tool          |
| **Shareable**         | Package and distribute your modules to the BMad community   |

## Quick Start

### 1. Register the Module

On first use, run `bmad-bmb-setup` to register BMad Builder in your project. This collects your preferences (name, language, output paths) and registers the builder's capabilities with the help system so `bmad-help` can guide you.

:::tip[Single-Skill Modules]
If you install a module that contains only one skill, that skill handles its own registration on first run. No separate setup step needed.
:::

### 2. Build Something

Invoke the **Agent Builder** or **Workflow Builder** and describe what you want to create. Both walk you through a series of questions and produce a ready-to-use skill folder.

| Goal                      | Builder          | Menu Code |
| ------------------------- | ---------------- | --------- |
| AI companion with memory  | Agent Builder    | BA        |
| Structured process / tool | Workflow Builder | BW        |
| Package skills as module  | Module Builder   | CM        |

### 3. Use Your Skill

The builders produce a complete skill folder. Copy it into your AI tool's skills directory (`.claude/skills/`, `.codex/skills/`, `.agents/skills/`, or wherever your tool looks) and it's immediately usable.

:::tip[Custom Module Installation]
The BMad Method installer supports installing custom modules from any Git host (GitHub, GitLab, Bitbucket, self-hosted) or local paths. See the [BMad Method install guide](https://docs.bmad-method.org/how-to/install-custom-modules/) for details.
:::

:::tip[No Module Required]
If you're building something for personal use, you don't need to package it as a module. Copy the skill folder and use it directly. Module packaging (with `bmad-help` registration and configuration) is for sharing or richer discoverability.
:::

### 4. Learn More

See the [Builder Commands Reference](/reference/builder-commands.md) for all capabilities, modes, and phases.

## What You Can Build

| Domain           | Example                                                                                    |
| ---------------- | ------------------------------------------------------------------------------------------ |
| **Personal**     | Journal companion, habit coach, learning tutor, friendly personal companions that remember |
| **Professional** | Code reviewer, documentation specialist, workflow automator                                |
| **Creative**     | Story architect, character developer, campaign designer                                    |
| **Any Domain**   | Anything you can describe as a repeatable process                                          |

## Design Patterns

Build better skills with these guides, drawn from real-world BMad development.

| Guide                                                                                | What You'll Learn                                                    |
| ------------------------------------------------------------------------------------ | -------------------------------------------------------------------- |
| **[Progressive Disclosure](/explanation/progressive-disclosure.md)**                 | Structure skills so they load only the context needed at each moment |
| **[Subagent Patterns](/explanation/subagent-patterns.md)**                           | Six orchestration patterns for parallel and hierarchical work        |
| **[Skill Authoring Best Practices](/explanation/skill-authoring-best-practices.md)** | Core principles, quality dimensions, and anti-patterns               |

## Documentation

| Section                                                                          | Purpose                                                                  |
| -------------------------------------------------------------------------------- | ------------------------------------------------------------------------ |
| **[Build Your First Module](/tutorials/build-your-first-module.md)**             | Plan, build, scaffold, and validate a complete module                    |
| **[Distribute Your Module](/how-to/distribute-your-module.md)**                  | Share your module via any Git host for anyone to install                  |
| **[Concepts](/explanation/)**                                                    | Agent types, memory architecture, workflows, skills, and how they relate |
| **[Design Patterns](/explanation/#design-patterns)**                             | Progressive disclosure, subagent orchestration, authoring best practices |
| **[Reference](/reference/)**                                                     | Builder commands, workflow patterns                                      |

## Community

- **[Discord](https://discord.gg/gk8jAdXWmj)**: Get unstuck, share what you built
- **[GitHub](https://github.com/bmad-code-org/bmad-builder)**: Source code
- **[BMad Method](https://docs.bmad-method.org)**: Core framework
