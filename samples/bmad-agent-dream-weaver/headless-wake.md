---
name: autonomous-wake
description: Default autonomous wake behavior — reviews journal, surfaces patterns, generates coaching nudges.
---

<!-- Internal — autonomous invocation only. Not a user-selectable capability. -->

# Autonomous Wake

You're running autonomously. No one is here. Execute wake behavior and exit.

## Context

- Memory location: `{project-root}/_bmad/memory/dream-weaver-sidecar/`
- Activation time: `{current-time}`

## Instructions

- Don't ask questions
- Don't wait for input
- Don't greet anyone
- Execute your wake behavior
- Write results to memory
- Exit

## Task Routing

Check if a specific task was requested:

- `--headless:morning` → **Morning Recall Prompt**: Write a personalized morning recall prompt to `{project-root}/_bmad/memory/dream-weaver-sidecar/daily-prompt.md`. Reference recent symbols, active techniques, and coaching goals. Keep it warm and brief — something the user sees first thing.

- `--headless:evening` → **Evening Seeding Exercise**: Write a pre-sleep intention-setting exercise to `{project-root}/_bmad/memory/dream-weaver-sidecar/daily-prompt.md`. Pull from seed log to suggest themes, use active coaching techniques. Calm, meditative tone.

- `--headless:weekly` → **Weekly Progress Report**: Generate a weekly summary covering:
  - Dreams logged this week (count, vividness average)
  - Recall trend (improving/stable/declining)
  - New symbols and recurring ones
  - Coaching progress (technique adherence, milestone proximity)
  - Seed success rate
  - One insight or pattern Oneira noticed
  - Write to `{project-root}/_bmad/memory/dream-weaver-sidecar/weekly-report.md`

- No specific task → **Default Wake Behavior** (below)

## Default Wake Behavior

1. **Batch-read in parallel:** `index.md`, `symbol-registry.yaml`, `coaching-profile.yaml`
2. Scan recent journal entries (last 7 days)
3. **Run in parallel:** `scripts/symbol_stats.py` against journal folder AND `scripts/recall_metrics.py` to update recall trends
   - **Script fallback:** If either script is unavailable (missing Python runtime, permission error), manually estimate from journal entries — count symbols by scanning frontmatter, calculate recall rate from entry dates.
5. Look for:
   - New recurring symbols (appeared 3+ times recently)
   - Emotion pattern shifts
   - Recall rate changes
   - Coaching milestone proximity
6. Write findings to `{project-root}/_bmad/memory/dream-weaver-sidecar/autonomous-insights.md`
7. Update `index.md` with latest stats

## Logging

Append to `{project-root}/_bmad/memory/dream-weaver-sidecar/autonomous-log.md`:

```markdown
## {YYYY-MM-DD HH:MM} - Autonomous Wake

- Task: {task-name or "default"}
- Status: {completed|actions taken}
- {relevant-details}
```
