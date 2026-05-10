---
title: 'Run Evals Against a Skill'
description: Use the bmad-eval-runner skill to evaluate a skill, capture artifacts, and grade the results
---

Use the `bmad-eval-runner` skill to run a skill's evals in a clean workspace and produce a graded report.

## When to Use This

- After editing a skill, to confirm nothing regressed
- Before publishing a module, to validate every skill you ship
- When debugging a description that fires on the wrong queries
- When checking that dependency skills are wired correctly

## When to Skip This

- Quick iteration where you are running the skill manually and reading the output yourself
- Skills with no defined evals (the runner halts on missing evals; it does not invent them)

:::note[Prerequisites]

- The skill you want to evaluate, with `evals.json` and/or `triggers.json` defined
- Either Docker Desktop installed (preferred) or willingness to run in best-effort local isolation. See [Install Docker for Evals](/how-to/install-docker-for-evals.md).
- An Anthropic account authenticated through Claude Code (the runner reuses your existing credential)
:::

:::tip[Quick Path]
Invoke the eval runner with the path to your skill: `bmad-eval-runner ./skills/my-skill`. The runner discovers your evals, picks isolation, runs everything in parallel, and tells you where the report lives.
:::

## Step 1: Confirm Eval Discovery

The runner looks for evals in this order, taking the first match:

1. The path you pass via `--evals`
2. `<skill-path>/evals/`
3. `<skill-path>/../../evals/<skill-name>/`
4. `<project-root>/evals/<skill-name>/`
5. `<project-root>/evals/**/<skill-name>/` (fuzzy)

If discovery fails, the runner halts. It does not invent evals.

## Step 2: Choose Isolation

Pass `--isolation docker|local|auto`. Default is `auto`, which picks Docker when available and local when not.

| Mode   | When to Use                                                              |
| ------ | ------------------------------------------------------------------------ |
| docker | Trigger evals (host skills can leak in local mode); reproducible runs    |
| local  | Quick iteration when you have not installed Docker                       |
| auto   | Default; lets the runner pick the best available option                  |

The first time Docker is selected, the runner builds the `bmad-eval-runner:latest` image. This takes a few minutes once. Subsequent runs reuse the cached image.

## Step 3: Pick Mode

Pass `--mode artifact|trigger|both`. Default is `both` if both eval files are found.

| Mode     | Effect                          |
| -------- | ------------------------------- |
| artifact | Runs `evals.json` only          |
| trigger  | Runs `triggers.json` only       |
| both     | Runs everything in parallel     |

## Step 4: Run the Skill

Invoke the eval runner from your project. A typical invocation:

```bash
bmad-eval-runner ./src/skills/my-skill --isolation docker --workers 8
```

The runner stages each eval's workspace, executes `claude -p` against the prompt, captures the stream-JSON transcript, and rsyncs any files the skill wrote. After all evals complete, it spawns a grader subagent per eval (in parallel) and aggregates the verdicts.

## Step 5: Inspect Results

When the run finishes, the runner emits two paths:

- The run folder, at `~/bmad-evals/<run-id>/` (or your configured `bmad_builder_reports` location)
- An HTML report at `<run-folder>/report.html`

Open the report for the summary view. Drop into the run folder for full transcripts, artifacts, and grading details for any eval you want to examine.

## What You Get

```
~/bmad-evals/20260509-172903-my-skill/
├── run.json                     # Run metadata
├── report.html                  # Aggregate HTML report
├── A1/
│   ├── prompt.txt               # The eval's prompt verbatim
│   ├── transcript.jsonl         # Stream-JSON tool calls and messages
│   ├── artifacts/               # Files the skill wrote
│   ├── grading.json             # Per-expectation verdicts
│   └── metrics.json             # Timing and tool-call counts
├── A2/
│   └── ...
└── triggers-result.json         # Trigger eval rates
```

Run folders are never deleted automatically. Disk management is your call.

## Tips

- Pass `--eval-ids A1,B3` to run only specific evals while iterating
- Pass `--workers 8` to parallelize aggressively (default is 4)
- A specific eval can override the default timeout by setting `"timeout": 900` in its `evals.json` entry
- For trigger evals, prefer Docker. Local mode can let host-installed skills bleed in via cwd-based discovery and bias the fire rate.

## A Worked Example

The `bmad-product-brief` skill in the BMad Method repository (`bmad-code-org/BMAD-METHOD`) ships a complete eval suite at `evals/bmm-skills/bmad-product-brief/`. To run it end-to-end:

```bash
bmad-eval-runner ./src/bmm-skills/1-analysis/bmad-product-brief --isolation docker --workers 8
```

The run produces 17 graded artifact evals (A1-A8 output grading, B1-B8 transcript grading, C1 configuration compliance), 15 trigger eval verdicts, and an aggregated HTML report. Use it as the model when writing evals for your own skills.

## Next Steps

For the complete `evals.json` and `triggers.json` schema, see [Eval Format](/reference/eval-format.md). For concepts and patterns, see [What Are Evals](/explanation/what-are-evals.md).
