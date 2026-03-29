---
title: 'Builder Commands Reference'
description: Complete reference for all capabilities, modes, and paths available in the Agent Builder, Workflow Builder, and Module Builder
---

Reference for the three core BMad Builder skills — the Agent Builder (`bmad-agent-builder`), the Workflow Builder (`bmad-workflow-builder`), and the Module Builder (`bmad-module-builder`).

## Capabilities Overview

| Capability           | Menu Code | Agent Builder                         | Workflow Builder                                       |
| -------------------- | --------- | ------------------------------------- | ------------------------------------------------------ |
| **Build Process**    | BP        | Build, edit, convert, or fix agents   | Build, edit, convert, or fix workflows and utilities   |
| **Quality Optimize** | QO        | Validate and optimize existing agents | Validate and optimize existing workflows and utilities |

Both capabilities support autonomous/headless mode via `--headless` / `-H` flags.

## Build Process (BP)

The core creative path. Six phases of conversational discovery take you from a rough idea to a complete, tested skill folder.

### Input Types

Both builders accept any of these as a starting point.

| Input                             | What Happens                                              |
| --------------------------------- | --------------------------------------------------------- |
| A rough idea or description       | Guided discovery from scratch                             |
| An existing BMad skill path       | Edit mode — analyze what exists, determine what to change |
| A non-BMad skill, tool, or code   | Convert to BMad-compliant structure                       |
| Documentation, API specs, or code | Extract intent and requirements automatically             |

### Interaction Modes

| Mode           | Behavior                                                                                     | Best For                                     |
| -------------- | -------------------------------------------------------------------------------------------- | -------------------------------------------- |
| **Guided**     | The builder walks through decisions, clarifies ambiguities, ensures completeness             | Production skills, first-time builders       |
| **YOLO**       | Brain-dump your idea; the builder guesses its way to a finished skill with minimal questions | Quick prototypes, experienced builders       |
| **Autonomous** | Fully headless — no interactive prompts, proceeds with safe defaults                         | CI/CD, batch processing, orchestrated builds |

### Build Phases

| Phase | Agent Builder                                                                                    | Workflow Builder                                                                                      |
| ----- | ------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------- |
| 1     | **Discover Intent** — understand the vision                                                      | **Discover Intent** — understand the vision; accepts any input format                                 |
| 2     | **Capabilities Strategy** — internal commands, external skills, or both; script opportunities    | **Classify Skill Type** — Simple Utility, Simple Workflow, or Complex Workflow; module membership     |
| 3     | **Gather Requirements** — name, persona, memory, capabilities, autonomous modes, folder dominion | **Gather Requirements** — name, description, stages, config variables, output artifacts, dependencies |
| 4     | **Draft & Refine** — present outline, iterate until ready                                        | **Draft & Refine** — present plan, clarify gaps, iterate until ready                                  |
| 5     | **Build** — generate skill structure, lint gate                                                  | **Build** — generate skill structure, lint gate                                                       |
| 6     | **Summary** — present results, offer Quality Optimize                                            | **Summary** — present results, run unit tests if scripts exist, offer Quality Optimize                |

### Agent Builder: Phase 2-3 Details

**Capabilities strategy** determines the mix of internal and external capabilities.

| Capability Type       | Description                                                                             |
| --------------------- | --------------------------------------------------------------------------------------- |
| **Internal commands** | Prompt-driven actions defined inside the agent, each gets a file in `prompts/`          |
| **External skills**   | Standalone skills the agent invokes by registered name                                  |
| **Scripts**           | Deterministic operations offloaded from the LLM (validation, data processing, file ops) |

**Agent-specific requirements** gathered in Phase 3:

| Requirement              | Description                                                                         |
| ------------------------ | ----------------------------------------------------------------------------------- |
| **Identity**             | Who is this agent? Communication style, decision-making philosophy                  |
| **Memory & persistence** | Sidecar needed? Critical data vs checkpoint data, save triggers                     |
| **Activation modes**     | Interactive only, or interactive + autonomous (schedule/cron)                       |
| **First-run onboarding** | What to ask on first activation to configure itself                                 |
| **Folder dominion**      | Read boundaries, write boundaries, explicit deny zones                              |
| **Autonomous tasks**     | Default wake behavior, named tasks via `--headless {task-name}` or `-H {task-name}` |

### Workflow Builder: Phase 2-3 Details

**Skill type classification** determines template and structure.

| Type                 | Signals                                                                       | Structure                                                                           |
| -------------------- | ----------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| **Simple Utility**   | Composable building block, clear input/output, usually mostly script-driven   | Single SKILL.md, scripts folder                                                     |
| **Simple Workflow**  | Fits in one SKILL.md, a few sequential steps, optional autonomous             | SKILL.md with inline steps, optional prompts and resources                          |
| **Complex Workflow** | Multiple stages, branching prompt flows, progressive disclosure, long-running | SKILL.md for routing, `prompts/` for stage details, `resources/` for reference data |

**Workflow-specific requirements** gathered in Phase 3:

| Requirement             | Simple Utility | Simple Workflow | Complex Workflow                         |
| ----------------------- | -------------- | --------------- | ---------------------------------------- |
| **Input/output format** | Yes            | —               | —                                        |
| **Composability**       | Yes            | —               | —                                        |
| **Steps**               | —              | Numbered steps  | Named stages with progression conditions |
| **Headless mode**       | —              | Optional        | Optional                                 |
| **Config variables**    | —              | Core + custom   | Core + module-specific                   |
| **Module sequencing**   | Optional       | Optional        | Recommended                              |

### Build Output

Both builders produce the same folder structure, with components included only as needed.

```
{skill-name}/
├── SKILL.md              # Skill instructions (persona embedded for agents)
├── prompts/              # Internal capability prompts, init, autonomous-wake
├── resources/            # Reference data, memory-system definition (agents)
├── agents/               # Subagent definitions for parallel processing
├── scripts/              # Deterministic scripts - bash, python or typescript generally
│   └── tests/            # Unit tests for scripts
└── templates/            # Building blocks for generated output
```

### Lint Gate

Before completing the build, both builders run deterministic validation.

| Script                   | What It Checks                                                                            |
| ------------------------ | ----------------------------------------------------------------------------------------- |
| `scan-path-standards.py` | Path conventions — no `{skill-root}`, `{project-root}` only for `_bmad`, no double-prefix |
| `scan-scripts.py`        | Script portability, PEP 723 metadata, agentic design, unit test presence                  |

Critical issues block completion. Warnings are noted but don't block.

## Quality Optimize (QO)

Comprehensive validation and optimization for existing skills. Runs deterministic lint scripts for instant structural checks and LLM scanner subagents for judgment-based analysis, all in parallel.

### Pre-Scan Checks

In interactive mode, the optimizer:

1. Checks for uncommitted changes and recommends committing first
2. Asks if the skill is currently working as expected

In autonomous mode, both checks are skipped and noted as warnings in the report.

### Scan Pipeline

The optimizer runs three tiers of analysis.

**Tier 1 — Lint scripts** (deterministic, zero tokens, instant):

| Script                   | Focus                            |
| ------------------------ | -------------------------------- |
| `scan-path-standards.py` | Path convention violations       |
| `scan-scripts.py`        | Script portability and standards |

**Tier 2 — Pre-pass scripts** (extract metrics for LLM scanners):

| Script                        | Agent Builder                       | Workflow Builder                |
| ----------------------------- | ----------------------------------- | ------------------------------- |
| Structure/integrity pre-pass  | `prepass-structure-capabilities.py` | `prepass-workflow-integrity.py` |
| Prompt metrics pre-pass       | `prepass-prompt-metrics.py`         | `prepass-prompt-metrics.py`     |
| Execution dependency pre-pass | `prepass-execution-deps.py`         | `prepass-execution-deps.py`     |

**Tier 3 — LLM scanners** (judgment-based, run as parallel subagents):

| Scanner                       | Agent Builder Focus                                                        | Workflow Builder Focus                                                                       |
| ----------------------------- | -------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| **Structure / Integrity**     | Structure, capabilities, identity, memory setup, consistency               | Logical consistency, description quality, progression conditions, type-appropriate structure |
| **Prompt Craft**              | Token efficiency, anti-patterns, persona voice, overview quality           | Token efficiency, anti-patterns, overview quality, progressive disclosure                    |
| **Execution Efficiency**      | Parallelization, subagent delegation, memory loading, context optimization | Parallelization, subagent delegation, read avoidance, context optimization                   |
| **Cohesion**                  | Persona-capability alignment, gaps, redundancies                           | Stage flow coherence, purpose alignment, complexity appropriateness                          |
| **Enhancement Opportunities** | Script automation, autonomous potential, edge cases, delight               | Creative edge-case discovery, experience gaps, assumption auditing                           |

### Report Synthesis

After all scanners complete, the optimizer synthesizes results into a unified report saved to `{bmad_builder_reports}/{skill-name}/quality-scan/{timestamp}/`.

In interactive mode, it presents a summary with severity counts and offers next steps:

- Apply fixes directly
- Export checklist for manual fixes
- Discuss specific findings

In autonomous mode, it outputs structured JSON with severity counts and the report file path.

### Optimization Guidance

Not every suggestion should be applied. The optimizer communicates these decision rules:

- **Keep phrasing** that captures the intended voice — leaner is not always better for persona-driven skills
- **Keep content** that adds clarity for the AI even if a human finds it obvious
- **Prefer scripting** for deterministic operations; **prefer prompting** for creative or judgment-based tasks
- **Reject changes** that flatten personality unless a neutral tone is explicitly wanted

## Module Builder

The Module Builder (`bmad-module-builder`) handles module-level planning, scaffolding, and validation. It operates at a higher level than the Agent and Workflow Builders — it orchestrates what those builders produce into a cohesive, installable module.

### Capabilities Overview

| Capability          | Menu Code | What It Does                                                           |
| ------------------- | --------- | ---------------------------------------------------------------------- |
| **Ideate Module**   | IM        | Brainstorm and plan a module through creative facilitation             |
| **Create Module**   | CM        | Scaffold a setup skill into an existing folder of built skills         |
| **Validate Module** | VM        | Check structural integrity and entry quality of a module's setup skill |

### Ideate Module (IM)

A facilitative brainstorming session that helps you envision your module from scratch. The builder acts as a creative collaborator — drawing out ideas, exploring possibilities, and guiding you toward the right architecture.

| Aspect          | Detail                                          |
| --------------- | ----------------------------------------------- |
| **Interaction** | Interactive only — no headless mode             |
| **Input**       | An idea or rough description                    |
| **Output**      | Plan document saved to `{bmad_builder_reports}` |

**What it covers:**

- Problem space exploration and creative brainstorming
- Architecture decision — single agent with capabilities vs. multiple skills vs. hybrid
- Standalone module or expansion of an existing module
- External dependencies (CLI tools, MCP servers)
- UI and visualization opportunities
- Setup skill extensions beyond configuration
- Per-skill capability definitions with help CSV metadata
- Configuration variables and sensible defaults

The plan document uses a resumable template with YAML frontmatter, so long brainstorming sessions survive context compaction.

**After ideation:** Build each planned skill using the Agent Builder (BA) or Workflow Builder (BW), then return to Create Module (CM) to scaffold the module.

### Create Module (CM)

Takes an existing folder of built skills and scaffolds a setup skill that makes it an installable BMad module. Supports `--headless` / `-H`.

| Aspect          | Detail                                                        |
| --------------- | ------------------------------------------------------------- |
| **Interaction** | Guided or headless                                            |
| **Input**       | Path to a skills folder, optional plan document               |
| **Output**      | Setup skill (`bmad-{code}-setup/`) added to the skills folder |

**What it does:**

1. Reads every SKILL.md in the folder to understand each skill
2. Collects module identity (name, code, description, version, greeting)
3. Defines help CSV entries — capabilities, menu codes, ordering, relationships
4. Captures configuration variables and external dependencies
5. Scaffolds the setup skill with generated `module.yaml` and `module-help.csv`

The scaffolded setup skill includes merge scripts, cleanup scripts, and a generic SKILL.md — only the asset files are customized per module.

### Validate Module (VM)

Verifies that a module's setup skill is complete and accurate. Combines a deterministic validation script with LLM-based quality assessment.

| Aspect          | Detail                             |
| --------------- | ---------------------------------- |
| **Interaction** | Interactive                        |
| **Input**       | Path to the module's skills folder |
| **Output**      | Validation report                  |

**Structural checks** (script-driven):

| Check                 | What It Catches                                                         |
| --------------------- | ----------------------------------------------------------------------- |
| Setup skill structure | Missing SKILL.md, module.yaml, or module-help.csv                       |
| Coverage              | Skills without CSV entries, orphan entries for nonexistent skills       |
| Menu codes            | Duplicate codes across the module                                       |
| References            | Before/after fields pointing to nonexistent capabilities                |
| Required fields       | Missing skill name, display name, menu code, or description in CSV rows |
| module.yaml           | Missing code, name, or description                                      |

**Quality assessment** (LLM-driven):

- Description accuracy — does each entry match what the skill actually does?
- Description quality — concise, action-oriented, specific, not overly verbose
- Completeness — are all distinct capabilities registered as separate rows?
- Ordering — do before/after relationships make sense?
- Menu codes — are they intuitive and memorable?

## Trigger Phrases

| Intent    | Phrases                                                 | Builder  | Route                             |
| --------- | ------------------------------------------------------- | -------- | --------------------------------- |
| Build new | "create/build/design an agent"                          | Agent    | `prompts/build-process.md`        |
| Build new | "create/build/design a workflow/skill/tool"             | Workflow | `prompts/build-process.md`        |
| Edit      | "edit/modify/update an agent"                           | Agent    | `prompts/build-process.md`        |
| Edit      | "edit/modify/update a workflow/skill"                   | Workflow | `prompts/build-process.md`        |
| Convert   | "convert this to a BMad agent"                          | Agent    | `prompts/build-process.md`        |
| Convert   | "convert this to a BMad skill"                          | Workflow | `prompts/build-process.md`        |
| Optimize  | "quality check/validate/optimize/review agent"          | Agent    | `prompts/quality-optimizer.md`    |
| Optimize  | "quality check/validate/optimize/review workflow/skill" | Workflow | `prompts/quality-optimizer.md`    |
| Ideate    | "ideate module/plan a module/brainstorm a module"       | Module   | `./references/ideate-module.md`   |
| Create    | "create module/build a module/scaffold a module"        | Module   | `./references/create-module.md`   |
| Validate  | "validate module/check module"                          | Module   | `./references/validate-module.md` |
