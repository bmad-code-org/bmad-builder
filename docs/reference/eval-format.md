---
title: 'Eval Format'
description: Complete schema for evals.json and triggers.json including fixtures, setup overlays, per-eval timeouts, and grading expectations
---

The runner accepts two file shapes. Both are JSON. Both live in an evals directory the runner can discover.

## File Layout

A typical evals directory:

```
evals/<skill-name>/
├── evals.json            # Artifact evals
├── triggers.json         # Trigger evals
├── setup/                # Base overlay applied to every eval
│   └── .claude/
│       └── skills/
│           └── bmad-distillator/
├── A1/
│   └── setup/            # Per-eval overlay applied on top of base
├── files/                # Fixture files staged via the eval's `files` field
│   └── some-fixture.md
```

## Artifact Evals (evals.json)

```json
{
  "skill_name": "bmad-product-brief",
  "evals": [
    {
      "id": "A1",
      "prompt": "Run headless. Create a product brief for ...",
      "expected_output": "A run folder with brief.md and decision-log.md ...",
      "files": ["evals/.../files/q2-brainstorm.md"],
      "expectations": [
        "brief.md exists in the run folder",
        "decision-log.md captures the pricing decision with rationale",
        "Final assistant message contains JSON with intent='create'"
      ],
      "timeout": 900
    }
  ]
}
```

### Field Reference

| Field             | Type     | Required | Description                                                                                  |
| ----------------- | -------- | -------- | -------------------------------------------------------------------------------------------- |
| `id`              | string   | yes      | Stable identifier; used as the eval's directory name in the run folder                       |
| `prompt`          | string   | yes      | Literal user message sent to `claude -p`                                                     |
| `expected_output` | string   | no       | Human-readable description; the grader reads it for context but does not score against it    |
| `files`           | string[] | no       | Fixture paths to stage into the workspace before execution                                   |
| `expectations`    | string[] | yes      | Pass/fail assertions evaluated by the grader subagent                                        |
| `timeout`         | int      | no       | Per-eval timeout in seconds; overrides the runner's default                                  |

### Top-Level Optional Fields

| Field           | Type   | Purpose                                                                          |
| --------------- | ------ | -------------------------------------------------------------------------------- |
| `skill_name`    | string | Documentation only; the runner derives the skill name from the SKILL.md path     |
| `_design_notes` | string | Free-form notes for human readers; ignored by the runner                         |

### Fixture Files

Each entry in `files` is staged into the eval's workspace before execution.

- A nested path (`evals/skill-x/files/some-brief/brief.md`) preserves directory structure inside the workspace
- The eval prompt then references the staged path explicitly so the skill can find it
- Fixtures are read-only inputs. The skill may read them; assertions may check that the skill did not modify them.

### Per-Eval Timeout

When omitted, the runner's default applies (currently 600 seconds, overridable via `--timeout`). Set per-eval timeouts when an eval invokes a slow dependency. Example for an eval that triggers a distillator subagent:

```json
{
  "id": "B8",
  "timeout": 900,
  "prompt": "Run headless. Create a product brief ... and generate a distillate."
}
```

### Expectations

Expectations are assertions the grader scores independently. Each is graded PASS or FAIL with cited evidence from the transcript or artifacts. The grader is instructed to flag weak assertions, so a passing eval that only proves the skill did not crash is surfaced as a problem, not a victory.

See [What Are Evals](/explanation/what-are-evals.md) for the two patterns (artifact correctness and process discipline) and the kinds of assertions that work well for each.

## Trigger Evals (triggers.json)

```json
[
  { "query": "Help me write a product brief for ...", "should_trigger": true },
  { "query": "Help me brainstorm ideas for ...",      "should_trigger": false }
]
```

### Field Reference

| Field            | Type    | Required | Description                                                |
| ---------------- | ------- | -------- | ---------------------------------------------------------- |
| `query`          | string  | yes      | The user message sent to a clean Claude session            |
| `should_trigger` | boolean | yes      | Whether the skill's description should fire on this query  |

### How Trigger Detection Works

The runner places a synthetic copy of the skill at `<workspace>/.claude/skills/<unique-name>/SKILL.md`. It then runs `claude -p` against each query and watches the stream-JSON output for a `Skill` tool call (or a `Read` of the synthetic SKILL.md) referencing the unique name. Each query runs three times by default for stability. The fire rate is the fraction of runs that fired.

A query passes when:

- `should_trigger=true` and `trigger_rate >= --trigger-threshold` (default 0.5)
- `should_trigger=false` and `trigger_rate < --trigger-threshold`

:::caution[Trigger Evals Need Docker]
Local-mode trigger evals can be biased by host-installed skills that are discoverable via cwd-based skill discovery. The detector may see a real skill fire instead of the synthetic. Use Docker isolation for trigger evals whenever it is available.
:::

## Setup Overlays

The runner supports a two-tier overlay system that rsyncs files into the workspace before the skill under test is staged. Use overlays to ship dependency skills, project configuration (`_bmad/`), or fixture state with the evals.

### Base Overlay

Files at `evals/<skill-name>/setup/` are applied to every eval. Use this for dependency skills the skill under test calls.

```
evals/bmad-product-brief/setup/
└── .claude/
    └── skills/
        ├── bmad-distillator/
        ├── bmad-editorial-review-prose/
        └── bmad-editorial-review-structure/
```

### Per-Eval Overlay

Files at `evals/<skill-name>/<eval-id>/setup/` are applied after the base overlay, only for that eval. Use this for eval-specific configuration: a custom `_bmad/config.user.yaml`, additional skills, or a different output path.

```
evals/bmad-product-brief/C1/setup/
└── _bmad/
    └── bmm/
        └── config.user.yaml
```

The base overlay and per-eval overlay are applied with `rsync -a`, so files at the same path in the per-eval overlay win.

### Order of Operations

Inside the workspace, before the eval runs:

1. Project root is rsynced from the host
2. Base setup overlay is rsynced on top
3. Per-eval setup overlay is rsynced on top
4. The skill under test is symlinked or copied into `.claude/skills/`
5. Fixtures from the `files` array are staged at their declared paths

The skill under test always wins. Overlays cannot replace the skill being evaluated.

## Eval Discovery

The runner discovers evals in this order, taking the first match:

| Order | Path                                                                |
| ----- | ------------------------------------------------------------------- |
| 1     | `--evals <path>` argument (folder or specific JSON file)            |
| 2     | `<skill-path>/evals/`                                               |
| 3     | `<skill-path>/../../evals/<skill-name>/`                            |
| 4     | `<project-root>/evals/<skill-name>/`                                |
| 5     | `<project-root>/evals/**/<skill-name>/` (fuzzy)                     |

If both `evals.json` and `triggers.json` are found in the discovered directory, both run unless `--mode` narrows it.

## Headless Prompts

Multi-step workflow skills need a signal to suppress clarifying questions and emit a structured JSON status block at the end. Once that signal is present, the skill executes its full internal flow (subagent calls, polish passes, finalize sequence) inside a single `claude -p` invocation, and the runner captures everything.

Common conventions for the signal:

- The literal phrase `Run headless.` at the start of the prompt
- Skill-specific keywords documented in the skill's `## Headless Mode` section
- A complete prompt with no genuine ambiguity for the skill to ask about

When designing evals for a multi-step skill, pack the prompt with everything the skill's discovery phase would have surfaced. The skill then has no reason to ask, runs end-to-end, and the artifacts are ready for grading.

## Example Suite

The `bmad-product-brief` skill in the BMad Method repository ships a complete eval suite that exercises every option in this reference. Read it as a worked example.

| Group | What It Covers                                                                                       |
| ----- | ---------------------------------------------------------------------------------------------------- |
| A1-A8 | Output grading: brief content, frontmatter, source-filtering, right-sizing across 8 product scenarios |
| B1-B8 | Transcript grading: decision-log fidelity, polish phase ordering, read-only Validate, distillate flow |
| C1    | Configuration compliance: custom output paths, document language, communication style                 |
| Triggers | 15 queries (positive + negative) covering create, update, validate intents and adjacent skills      |

What it shows in practice:

- Setup overlays for dependency skills (`bmad-distillator`, editorial review skills) under `evals/setup/.claude/skills/`
- Per-eval setup overlay at `evals/bmad-product-brief/C1/setup/_bmad/` for custom configuration
- Per-eval `timeout` override on B8 (the distillator-invoking eval)
- Read-only fixture staging for Validate-mode evals (A4, B5, B6, B7) using the `files` field
- Mixed expectations in the same eval: some assertions check files, others scan the transcript for tool-call ordering

See `evals/bmm-skills/bmad-product-brief/` in the BMad Method repository (`bmad-code-org/BMAD-METHOD`).
