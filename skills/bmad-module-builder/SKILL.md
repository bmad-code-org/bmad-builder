---
name: bmad-module-builder
description: Plans, creates, and validates BMad modules. Use when the user requests to 'ideate module', 'plan a module', 'create module', 'build a module', or 'validate module'.
---

# BMad Module Builder

## Overview

This skill helps you bring BMad modules to life — from the first spark of an idea to a fully scaffolded, installable module. It offers three paths:

- **Ideate Module (IM)** — A creative brainstorming session that helps you imagine what your module could be, decide on the right architecture (agent vs. workflow vs. both), and produce a detailed plan document. The plan then guides you through building each piece with the Agent Builder and Workflow Builder.
- **Create Module (CM)** — Takes an existing folder of built skills and scaffolds the setup infrastructure (module.yaml, module-help.csv, setup skill) that makes it a proper installable BMad module. Supports `--headless` / `-H`.
- **Validate Module (VM)** — Checks that a module's setup skill is complete and correct — every skill has its capabilities registered, entries are accurate and well-crafted, and structural integrity is sound.

**Args:** Accepts `--headless` / `-H` for CM path only, an initial description for IM, or a path to a skills folder for CM/VM.

## On Activation

Load available config from `{project-root}/_bmad/config.yaml` and `{project-root}/_bmad/config.user.yaml` (root level and `bmb` section). If config is missing, let the user know `bmad-builder-setup` can configure the module at any time. Use sensible defaults for anything not configured.

Detect user's intent:

- **Ideate / Plan** keywords or no path argument → Load `./references/ideate-module.md`
- **Create / Scaffold** keywords or a folder path → Load `./references/create-module.md`
- **Validate / Check** keywords → Load `./references/validate-module.md`
- **Unclear** → Present options:
  - **Ideate Module (IM)** — "I have an idea for a module and want to brainstorm and plan it"
  - **Create Module (CM)** — "I've already built my skills and want to package them as a module"
  - **Validate Module (VM)** — "I want to check that my module's setup skill is complete and correct"

If `--headless` or `-H` is passed, route to CM with headless mode.
