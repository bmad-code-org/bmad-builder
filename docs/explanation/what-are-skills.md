---
title: 'What Are Skills?'
description: The universal building block underneath agents, workflows, and utilities in the BMad ecosystem
---

Skills are the universal packaging format for everything the BMad Builder produces. Agents are skills. Workflows are skills. Simple utilities are skills. The format follows the [Agent Skills open standard](https://agentskills.io/home).

## Skills in BMad

The BMad Builder produces skills that conform to the open standard and adds a few BMad-specific conventions on top.

| Component      | Purpose                                                              |
| -------------- | -------------------------------------------------------------------- |
| **SKILL.md**   | The skill's instructions — persona, capabilities, and behavior rules |
| **resources/** | Reference data, templates, and guidance documents                    |
| **scripts/**   | Deterministic validation and analysis scripts                        |
| **templates/** | Building blocks for generated output                                 |

Not every skill needs all of these. A simple utility might be a single `SKILL.md`. A complex workflow or agent may use the full structure.

## Ready to Use on Build

The builders output a complete skill folder. Place it in your tool's skills directory — `.claude/skills`, `.codex/skills`, `.agent/skills`, or wherever your tool looks — and it is immediately usable.

See [What Are Agents](/explanation/what-are-bmad-agents.md) and [What Are Workflows](/explanation/what-are-workflows.md) for how agents and workflows each use this foundation differently.
