---
title: 'Why BMad Eval Runner'
description: Isolation, dependency staging, real trigger detection, and a permanent audit trail for every run
---

The eval runner is built around a simple goal: produce results that reflect the skill itself, not the host that ran it. That goal drives four design choices.

## Isolation

Every eval starts in a clean room. With Docker, the run executes inside a fresh container off `bmad-eval-runner:latest`. Without Docker, the runner falls back to a per-eval temp directory with `HOME` overridden so global memory and global `CLAUDE.md` cannot influence the result. Either way, two developers running the same eval get the same workspace state.

Why this matters: skills are sensitive to context. Your global `~/.claude/CLAUDE.md`, your auto-memory, an ancestor `CLAUDE.md` in the project tree, cached MCP settings. All of these reach a default `claude -p` invocation. The eval should measure the skill, not the bench it was tested on.

## Dependency Staging

Real BMad skills compose. A product brief skill calls a distillator skill, which calls editorial review skills. The runner stages dependencies through a setup overlay system: directories at `evals/setup/` (base, applied to every eval) and `evals/<eval-id>/setup/` (per-eval, applied on top) are rsynced into the workspace before the skill under test is staged.

Drop the dependency skills into `evals/setup/.claude/skills/` and they are available inside the sandbox. Drop a per-eval `_bmad/config.user.yaml` into `evals/C1/setup/` and it overrides the base for that eval only.

## Trigger Detection That Reflects Reality

The runner places the synthetic skill at `<workspace>/.claude/skills/<unique-name>/SKILL.md`, where Claude actually loads skills. The detector watches the stream-JSON transcript for `Skill` tool calls (or `Read` of the synthetic SKILL.md) referencing the unique name. Each query runs three times by default for stability, and the fire rate per query is reported with a configurable threshold.

This matches how skills surface in production. The trigger rate you see is the rate users will see.

## Permanent Artifacts

Every run writes to a dated folder under `~/bmad-evals/<run-id>/`. Each eval gets its own subdirectory containing the prompt, the full stream-JSON transcript, every file the skill wrote, the grading verdict, and timing metrics.

Nothing is rotated or cleaned up. You can read what happened, share the run folder with a collaborator, or diff it against a future run. Disk management is the user's call, not the runner's.

## Independent Grading

After artifact runs complete, the runner spawns a grader subagent per eval (in parallel) using the Agent tool. Each grader reads the eval's transcript and artifacts, scores each expectation independently with cited evidence, and writes `grading.json`. Graders are instructed to flag weak assertions (passing on technicality) so you can spot evals that look strict but would pass for a wrong output.

## Next Steps

For a step-by-step run, see [Run Evals Against a Skill](/how-to/run-evals-against-a-skill.md). For the complete eval file schema, see [Eval Format](/reference/eval-format.md). For why Docker matters, see [Install Docker for Evals](/how-to/install-docker-for-evals.md).
