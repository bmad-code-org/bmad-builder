---
title: 'Build Your First Module'
description: Create a complete BMad module from idea to installable package using the Module Builder
---

Walk through the complete module lifecycle — from brainstorming an idea to scaffolding an installable BMad module with help registration and configuration.

## What You'll Learn

- How to plan a module using the Ideate Module (IM) capability
- When to use a single agent vs. multiple workflows
- How to build individual skills with the Agent and Workflow Builders
- How to scaffold a setup skill with Create Module (CM)
- How to validate your module with Validate Module (VM)

:::note[Prerequisites]

- BMad Builder module installed in your project (`bmad-builder-setup`)
- Familiarity with what agents and workflows are — see **[What Are Agents](/explanation/what-are-bmad-agents.md)** and **[What Are Workflows](/explanation/what-are-workflows.md)**
  :::

:::tip[Quick Path]
Already have your skills built? Skip to **Step 3: Scaffold the Module** to package them. Just need to validate an existing module? Jump to **Step 4: Validate**.
:::

## Understanding Modules

A BMad module is a folder of skills (agents and/or workflows) plus a setup skill that handles installation. The setup skill collects configuration, registers capabilities with the help system, and makes the module discoverable.

| Component           | What It Does                                                    |
| ------------------- | --------------------------------------------------------------- |
| **Your skills**     | Agents and workflows that deliver the module's value            |
| **Setup skill**     | Generated infrastructure — config collection, help registration |
| **module.yaml**     | Module identity and configurable variables                      |
| **module-help.csv** | Capability entries for the help system                          |

See **[What Are Modules](/explanation/what-are-modules.md)** for architecture decisions and design patterns.

## Step 1: Plan Your Module

Start with the Ideate Module capability to brainstorm and plan.

:::note[Example]
**You:** "I want to ideate a module"

**Builder:** Starts a creative brainstorming session — exploring what the module could do, who it's for, and how capabilities should be organized.
:::

The ideation session covers:

| Topic             | What You'll Decide                                                        |
| ----------------- | ------------------------------------------------------------------------- |
| **Vision**        | Problem space, target users, core value                                   |
| **Architecture**  | Single agent, multiple workflows, or hybrid                               |
| **Memory**        | For multi-agent modules: personal sidecars, shared module memory, or both |
| **Module type**   | Standalone or expansion of another module                                 |
| **Skills**        | Each planned skill's purpose, capabilities, and relationships             |
| **Configuration** | Custom install questions and variables                                    |
| **Dependencies**  | External CLI tools, MCP servers, web services                             |

The output is a **plan document** saved to your reports folder. This document captures everything you discussed and serves as a blueprint for building each skill.

## Step 2: Build Your Skills

With your plan in hand, build each skill individually.

| Skill Type          | Builder          | Menu Code |
| ------------------- | ---------------- | --------- |
| Agent               | Agent Builder    | BA        |
| Workflow or utility | Workflow Builder | BW        |

Share the plan document as context when building each skill — it helps the builder understand the bigger picture and how the skill fits into the module.

:::caution[Build Before Packaging]
Build and test each skill before scaffolding the module. The Create Module step reads your finished skills to generate accurate help entries.
:::

## Step 3: Scaffold the Module

Once all skills are built, run Create Module (CM) to scaffold the setup skill.

:::note[Example]
**You:** "I want to create a module" or provide the path to your skills folder.

**Builder:** Reads every skill, asks about module identity and capability ordering, then scaffolds the setup skill.
:::

The builder generates:

```
your-skills-folder/
├── bmad-{code}-setup/           # Generated setup skill
│   ├── SKILL.md                 # Setup instructions
│   ├── scripts/                 # Config merge and cleanup scripts
│   │   ├── merge-config.py
│   │   ├── merge-help-csv.py
│   │   └── cleanup-legacy.py
│   └── assets/
│       ├── module.yaml          # Your module's identity and config vars
│       └── module-help.csv      # Your module's capability entries
├── your-agent-skill/
├── your-workflow-skill/
└── ...
```

## Step 4: Validate

Run Validate Module (VM) to check that everything is wired correctly.

:::note[Example]
**You:** "Validate my module at ./my-skills-folder"

**Builder:** Runs structural checks and quality assessment, then reports findings.
:::

| Check Type     | What It Catches                                                        |
| -------------- | ---------------------------------------------------------------------- |
| **Structural** | Missing files, orphan entries, duplicate menu codes, broken references |
| **Quality**    | Inaccurate descriptions, missing capabilities, poor entry quality      |

Fix any findings and re-validate until clean.

## What You've Accomplished

```
your-module/
├── bmad-{code}-setup/           # Installable setup skill
│   ├── SKILL.md
│   ├── scripts/
│   └── assets/
│       ├── module.yaml          # Module identity
│       └── module-help.csv      # Capability registry
├── skill-one/                   # Your built skills
├── skill-two/
└── ...
```

Your module is now a complete, distributable BMad module. To install it in any project, users run the setup skill.

## Quick Reference

| Capability       | Menu Code | When to Use                                        |
| ---------------- | --------- | -------------------------------------------------- |
| Ideate Module    | IM        | Planning a new module from scratch                 |
| Build an Agent   | BA        | Building an agent skill for the module             |
| Build a Workflow | BW        | Building a workflow skill for the module           |
| Create Module    | CM        | Scaffolding the setup skill after skills are built |
| Validate Module  | VM        | Checking the module is complete and accurate       |

## Common Questions

### Do I need to ideate before creating?

No. If you already know what your module should contain and have built the skills, skip straight to Create Module (CM). Ideation is for when you're starting from an idea and want help planning.

### Can I add skills to a module later?

Yes. Build the new skill, then re-run Create Module (CM) on the folder. The scaffolding uses an anti-zombie pattern — it replaces the existing setup skill cleanly.

### What if my module only has one skill?

A single agent or workflow can still be a module. The setup skill provides configuration and help registration. For very simple cases, a standalone skill with self-registration may be a better fit — see the agent or workflow builder for that pattern.

### Can my module extend another module?

Yes. During ideation or creation, specify that your module is an expansion. Your help CSV entries can reference the parent module's capabilities in their before/after ordering fields.

## Getting Help

- **[What Are Modules](/explanation/what-are-modules.md)** — Concepts and architecture decisions
- **[Module Configuration](/explanation/module-configuration.md)** — Setup skill internals and config patterns
- **[Builder Commands Reference](/reference/builder-commands.md)** — Full capability documentation
- **[Discord](https://discord.gg/gk8jAdXWmj)** — Community support

:::tip[Key Takeaways]
Plan first with Ideate Module (IM), build individual skills with the Agent and Workflow Builders, scaffold with Create Module (CM), and verify with Validate Module (VM). The setup skill handles the rest — config collection, help registration, and making your module installable.
:::
