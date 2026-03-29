---
title: 'Workflow & Skill Patterns'
description: Reference for the three skill types, their structure patterns, decision criteria, and execution models
---

Reference for how the BMad Builder classifies and structures skills. Every skill falls into one of three types, each with a distinct structure and set of signals.

## Skill Type Taxonomy

| Type                 | Description                                                                                                                   | Structure                                             |
| -------------------- | ----------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------- |
| **Simple Utility**   | Input/output building block. Headless, composable, often script-driven. May opt out of config loading for true standalone use | SKILL.md + `scripts/`                                 |
| **Simple Workflow**  | Multi-step process contained in a single SKILL.md. Loads config directly from module config.yaml. Minimal or no `prompts/`    | SKILL.md + optional `resources/`                      |
| **Complex Workflow** | Multi-stage with progressive disclosure, stage prompts in `prompts/`, config integration. May support headless mode           | SKILL.md (routing) + `prompts/` stages + `resources/` |

## Decision Tree

```
1. Is it a composable building block with clear input/output?
   └─ YES → Simple Utility
   └─ NO ↓

2. Can it fit in a single SKILL.md without progressive disclosure?
   └─ YES → Simple Workflow
   └─ NO ↓

3. Does it need multiple stages, long-running process, or progressive disclosure?
   └─ YES → Complex Workflow
```

## Classification Signals

### Simple Utility

- Clear input → processing → output pattern
- No user interaction needed during execution
- Other skills and workflows call it
- Deterministic or near-deterministic behavior
- Could be a script but needs LLM judgment
- Examples: JSON validator, format converter, file structure checker

### Simple Workflow

- 3-8 numbered steps
- User interaction at specific points
- Uses standard tools (gh, git, npm, etc.)
- Produces a single output artifact
- No need to track state across compactions
- Examples: PR creator, deployment checklist, code review

### Complex Workflow

- Multiple distinct phases or stages
- Long-running (likely to hit context compaction)
- Progressive disclosure needed (too much for one file)
- Routing logic in SKILL.md dispatches to stage prompts
- Produces multiple artifacts across stages
- May support headless/autonomous mode
- Examples: agent builder, module builder, project scaffolder

## Structure Patterns

### Simple Utility

```
bmad-my-utility/
├── SKILL.md              # Complete instructions, input/output spec
└── scripts/              # Core logic
    ├── process.py
    └── tests/
```

### Simple Workflow

```
bmad-my-workflow/
├── SKILL.md              # Steps inline, config loading, output spec
└── resources/            # Optional reference data
```

### Complex Workflow

```
bmad-my-complex-workflow/
├── SKILL.md              # Routing logic — dispatches to prompts/
├── prompts/              # Stage instructions
│   ├── 01-discovery.md
│   ├── 02-planning.md
│   ├── 03-execution.md
│   └── 04-review.md
├── resources/            # Reference data, templates, schemas
├── agents/               # Subagent definitions for parallel work
└── scripts/              # Deterministic operations
    └── tests/
```

## Execution Models

| Model                     | Applicable Types                  | Description                                                      |
| ------------------------- | --------------------------------- | ---------------------------------------------------------------- |
| **Interactive**           | All                               | User invokes skill and interacts conversationally                |
| **Headless / Autonomous** | Simple Utility, Complex Workflow  | Runs without user interaction — takes inputs, produces outputs   |
| **YOLO**                  | Simple Workflow, Complex Workflow | User brain-dumps; builder drafts the full artifact, then refines |
| **Guided**                | Simple Workflow, Complex Workflow | Section-by-section discovery with soft gates at transitions      |

## Module Context

Module membership is orthogonal to skill type — any type can be standalone or part of a module.

| Context          | Naming                          | Init                                                               |
| ---------------- | ------------------------------- | ------------------------------------------------------------------ |
| **Module-based** | `bmad-{modulecode}-{skillname}` | Loads config from module config.yaml                               |
| **Standalone**   | `bmad-{skillname}`              | Loads config from module config.yaml; simple utilities may opt out |
