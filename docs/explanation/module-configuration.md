---
title: "Module Configuration and the Setup Skill"
description: How BMad modules handle user configuration through a setup skill, when to use configuration vs. alternatives, and how to register with the help system
---

Every BMad module can include a **setup skill** that collects user preferences and registers the module's capabilities with the help system. The BMad Builder module's own setup skill (`bmad-builder-setup`) is the reference implementation.

## When You Need Configuration

Most modules should not need configuration at all. Before adding configurable values, consider whether a simpler alternative exists.

| Approach | When to Use |
| -------- | ----------- |
| **Sensible defaults** | The variable has one clearly correct answer for most users that could be overridden or updated by the specific skill that needs it the first time it runs |
| **Agent memory** | Your module follows the agent pattern and the agent can learn preferences through conversation |
| **Configuration** | The value genuinely varies across projects and cannot be inferred at runtime |

:::tip[Standalone Skills and Agents]
If you are building a standalone agent or skill — not a multi-capability module — the setup skill overhead is not worth it. A concise overview section at the top of your SKILL.md body, clear comments in script headers, and `--help` flags on any CLI tools give users everything they need to discover and use the skill.
:::

## What the Setup Skill Does

A setup skill serves two purposes:

| Purpose | What Happens |
| ------- | ------------ |
| **Configuration** | Collects user preferences and writes them to shared config files |
| **Help registration** | Adds the module's capabilities to the project-wide help system so users can discover them |

## Configuration Files

Setup skills write to three files in `{project-root}/_bmad/`:

| File | Scope | Contains |
| ---- | ----- | -------- |
| `config.yaml` | Shared, committed to git | Core settings at root level, plus a section per module with metadata and module-specific values |
| `config.user.yaml` | Personal, gitignored | User-only settings like `user_name` and `communication_language` |
| `module-help.csv` | Shared, committed to git | One row per capability the module exposes |

Core settings (like `output_folder` and `document_output_language`) live at the root of `config.yaml` and are shared across all modules. Each module also gets its own section keyed by its module code.

## The module.yaml File

Each module declares its identity and configurable variables in an `assets/module.yaml` inside the setup skill. This file drives both the prompts shown to the user and the values written to config.

```yaml
code: mymod
name: "My Module"
description: "What this module does"
module_version: 1.0.0
default_selected: false
module_greeting: >
  Welcome message shown after setup completes.

my_output_folder:
  prompt: "Where should output be saved?"
  default: "{project-root}/_bmad-output/my-module"
  result: "{project-root}/{value}"
```

Variables with a `prompt` field are presented to the user during setup. The `default` value is used when the user accepts defaults. Adding `user_setting: true` to a variable routes it to `config.user.yaml` instead of the shared config.

:::caution[Literal Token]
`{project-root}` is a literal token in config values. Never substitute it with an actual path. It signals to the consuming tool that the value is relative to the project root.
:::

## Help Registration Without Configuration

You may not need any configurable values but still want to register your module with the help system. This is worth doing when:

- The skill description in SKILL.md frontmatter cannot fully convey what the module offers while staying concise
- You want to express capability sequencing, phase constraints, or other metadata the CSV supports
- An agent has many internal capabilities that users should be able to discover
- Your module has more than about three distinct things it can do

For simpler cases, these alternatives are often sufficient:

| Alternative | What It Provides |
| ----------- | ---------------- |
| **SKILL.md overview section** | A concise summary at the top of the skill body — the `--help` system scans this section to present user-facing help, so keep it succinct |
| **Script header comments** | Describe purpose, usage, and flags at the top of each script |

If these cover your discoverability needs, you can skip the setup skill entirely.

## The module-help.csv File

The CSV asset registers the module's capabilities with the help system. Each row describes one capability that users can discover and invoke.

```csv
module,agent-name,skill-name,display-name,menu-code,capability,args,description,...
mymod,,my-skill,My Skill,MS,build-process,,"Does something useful.",...
```

When the setup skill runs, it merges these rows into the project-wide `_bmad/module-help.csv`, replacing any existing rows for this module. This is how users find your module's commands through the help system.

## Anti-Zombie Pattern

Both merge scripts use an anti-zombie pattern: before writing new values for a module, they remove all existing entries for that module's code. This prevents stale configuration or help entries from persisting across module updates. Running setup a second time is always safe.

## Design Guidance

Configuration is for **basic, project-level settings** — output folders, language preferences, feature toggles. Keep the number of configurable values small.

| Pattern | Configuration Role |
| ------- | ------------------ |
| **Agent pattern** | Prefer agent memory for per-user preferences. Use config only for values that must be shared across the project |
| **Workflow pattern** | Use config for output locations and behavior switches that vary across projects |
| **Skill-only pattern** | Use config sparingly. If the skill works with sensible defaults, skip config entirely |

Extensive workflow customization — step overrides, conditional branching, template selection — is a separate concern and will be covered in a dedicated document.

## Upcoming Tooling

A module scaffolding tool is planned that will generate the setup skill as part of module creation, along with the marketplace manifest format. Until then, use the BMad Builder module's setup skill as a reference implementation.

Once available, you will be able to generate a setup skill from your existing collection of agents, workflows, and skills with a prompt like:

:::note[Example]
"Create a setup skill for my module in `./my-module-skills/` that mirrors `bmad-builder-setup` — with its own module name and code (my cool module, mcm), config variables for output folder locations, and help entries inferred from the existing skills in the folder."
:::

A decent LLM will clone the entire `bmad-builder-setup` skill components amd structure — SKILL.md, scripts, tests — updating only the skill name, description, and the two asset files (`module.yaml` and `module-help.csv`) to reflect your module.
Take the time to ensure the description that triggers it is correct, along with the module.yaml and module-help.csv
