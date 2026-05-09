# Eval Formats

The runner accepts two file shapes, both compatible with Anthropic's skill-creator conventions.

## Artifact evals — `evals.json`

```json
{
  "skill_name": "bmad-product-brief",
  "evals": [
    {
      "id": 1,
      "prompt": "I want to create a brief for ...",
      "expected_output": "A run folder with brief.md and decision-log.md ...",
      "files": [
        "evals/.../files/some-fixture.md"
      ],
      "expectations": [
        "brief.md exists in the run folder",
        "decision-log.md exists",
        "brief.md word count is between 250 and 1500"
      ]
    }
  ]
}
```

Field semantics:

- **id**: stable identifier; used as the eval's directory name in the run folder.
- **prompt**: the literal user message Claude will receive. Sent verbatim to `claude -p`.
- **expected_output**: human-readable description, used for context only — the grader reads it but does not score against it directly.
- **files**: optional fixture paths. Resolved relative to the project root (or the evals folder). Each file is staged into the eval's workspace before execution. Path semantics:
  - A bare filename is staged at the workspace root.
  - A nested path (`some-brief/brief.md`) preserves the directory structure inside the workspace.
- **expectations**: list of pass/fail assertions evaluated by the grader subagent. Each is graded independently. The grader is instructed to flag weak assertions — assertions a wrong output would also trivially pass.

The grader writes `grading.json` next to each eval's artifacts; the runner aggregates.

## Trigger evals — `triggers.json`

```json
[
  { "query": "Help me write a product brief for ...", "should_trigger": true },
  { "query": "Help me brainstorm ideas for ...",      "should_trigger": false }
]
```

The runner creates a synthetic command file in the sandbox's `.claude/commands/<skill-name>.md` containing the skill's description, then runs each query against `claude -p` with stream-JSON output and detects whether the skill (or a Read of its SKILL.md) appears as a tool call. Each query is run `--runs-per-query` times (default 3); `trigger_rate` is the fraction of runs that fired.

A query passes when:
- `should_trigger=true` and `trigger_rate >= --trigger-threshold` (default 0.5)
- `should_trigger=false` and `trigger_rate < --trigger-threshold`

Trigger evals do not produce artifacts beyond the result JSON. They are cheap and parallelize aggressively.

## Where evals can live

The runner discovers evals in this order:

1. `--evals <path>` — explicit. May point to a folder or a specific `*.json`.
2. `<skill-path>/evals/` — colocated with the skill.
3. `<skill-path>/../../evals/<skill-name>/` — sibling-of-parent. Common pattern when evals are intentionally excluded from skill distribution.
4. `<project-root>/evals/<skill-name>/`.
5. `<project-root>/evals/**/<skill-name>/` — fuzzy search under the project's evals tree.

If both `evals.json` and `triggers.json` are found, both run unless `--mode` narrows it.

## Writing good expectations

The grader's job is easier when expectations are *discriminating* — they are hard to pass without actually doing the work. Weak patterns to avoid:

- **Filename-only checks** — "brief.md exists" can pass for an empty file. Pair with a content check.
- **Wholly subjective phrasing** — "the brief is high quality" cannot be evaluated. State the property concretely.
- **Tautologies** — anything that follows from the prompt being understood is not a useful expectation.

Strong patterns:

- Specific facts that should appear in the output ("incorporates at least 2 specific findings from section X")
- Structural claims that a wrong output would fail ("brief.md word count is between 250 and 1500")
- Negative assertions ("does not introduce content from unrelated sections")
- Decision-log entries that capture process choices ("decision-log indicates the report was filtered to the helmet category rather than ingested whole")
