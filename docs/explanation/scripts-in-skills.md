---
title: "Scripts in Skills"
description: Why deterministic scripts make skills faster, cheaper, and more reliable — and the technical choices behind portable script design
---

Scripts are the reliability backbone of a well-built skill. They handle work that has clear right-and-wrong answers — validation, transformation, extraction, counting — so the LLM can focus on what it does best: judgment, synthesis, and creative reasoning.

## The Problem: LLMs Do Too Much

Without scripts, every operation in a skill runs through the LLM. That means:

- **Non-deterministic results.** Ask an LLM to count tokens in a file three times and you may get three different numbers. Ask a script and you get the same answer every time.
- **Wasted tokens and time.** Parsing a JSON file, checking if a directory exists, or comparing two strings are mechanical operations. Running them through the LLM burns context window and adds latency for no gain.
- **Harder to test.** You can write unit tests for a script. You cannot write unit tests for an LLM prompt.

The pattern shows up everywhere: skills that try to LLM their way through structural validation are slower, less reliable, and more expensive than skills that offload those checks to scripts.

## The Determinism Boundary

The core design principle is **intelligence placement** — put each operation where it belongs.

| Scripts Handle | LLM Handles |
| -------------- | ----------- |
| Validate structure, format, schema | Interpret meaning, evaluate quality |
| Count, parse, extract, transform | Classify ambiguous input, make judgment calls |
| Compare, diff, check consistency | Synthesize insights, generate creative output |
| Pre-process data into compact form | Analyze pre-processed data with domain reasoning |

**The test:** Given identical input, will this operation always produce identical output? If yes, it belongs in a script. Could you write a unit test with expected output? Definitely a script. Requires interpreting meaning, tone, or context? Keep it as an LLM prompt.

:::tip[The Pre-Processing Pattern]
One of the highest-value script uses is pre-processing. A script extracts compact metrics from large files into a small JSON summary. The LLM then reasons over the summary instead of reading raw files — dramatically reducing token usage while improving analysis quality because the data is clean and structured.
:::

## Why Python, Not Bash

Skills must work across macOS, Linux, and Windows. Bash is not portable.

| Factor | Bash | Python |
| ------ | ---- | ------ |
| **macOS / Linux** | Works | Works |
| **Windows (native)** | Fails or behaves inconsistently | Works identically |
| **Windows (WSL)** | Works, but can conflict with Git Bash on PATH | Works identically |
| **Error handling** | Limited, fragile | Rich exception handling |
| **Testing** | Difficult | Standard unittest/pytest |
| **Complex logic** | Quickly becomes unreadable | Clean, maintainable |

Even basic commands like `sed -i` behave differently on macOS vs Linux. Piping, `jq`, `grep`, `awk` — all of these have cross-platform pitfalls that Python's standard library avoids entirely.

**Safe bash commands** that work everywhere and remain fine to use directly:

| Command | Purpose |
| ------- | ------- |
| `git`, `gh` | Version control and GitHub CLI |
| `uv run` | Python script execution |
| `npm`, `npx`, `pnpm` | Node.js ecosystem |
| `mkdir -p` | Directory creation |

Everything beyond that list should be a Python script.

## Standard Library First

Python's standard library covers most script needs without any external dependencies. Stdlib-only scripts run with plain `python3`, need no special tooling, and have zero supply-chain risk.

| Need | Standard Library |
| ---- | ---------------- |
| JSON parsing | `json` |
| Path handling | `pathlib` |
| Pattern matching | `re` |
| CLI interface | `argparse` |
| Text comparison | `difflib` |
| Counting, grouping | `collections` |
| Source analysis | `ast` |
| Data formats | `csv`, `xml.etree` |

Only reach for external dependencies when the stdlib genuinely cannot do the job — `tiktoken` for accurate token counting, `pyyaml` for YAML parsing, `jsonschema` for schema validation. Each external dependency adds install-time cost, requires `uv` to be available, and expands the supply-chain surface. The BMad builders require explicit user approval for any external dependency during the build process.

## Zero-Friction Dependencies with PEP 723

Python scripts in skills use [PEP 723](https://peps.python.org/pep-0723/) inline metadata to declare their dependencies directly in the file. Combined with `uv run`, this gives you `npx`-like behavior — dependencies are silently cached in an isolated environment, no global installs, no user prompts.

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml>=6.0"]
# ///

import yaml
# script logic here
```

When a skill invokes this script with `uv run scripts/analyze.py`, the dependency (`pyyaml` in this example) is automatically resolved. The user never sees an install prompt, never needs to manage a virtual environment, and never pollutes their global Python installation.

**Why this matters for skill authoring:** Without PEP 723, skills that needed libraries like `pyyaml` or `tiktoken` would force users to run `pip install` — a jarring, trust-breaking experience that makes users hesitate to adopt the skill.

## Graceful Degradation

Skills run in multiple environments: CLI terminals, desktop apps, IDE extensions, and web interfaces like claude.ai. Not all environments can execute Python scripts.

The principle: **scripts are the fast, reliable path — but the skill must still deliver its outcome when execution is unavailable.**

When a script cannot run, the LLM performs the equivalent work directly. This is slower and less deterministic, but the user still gets a result. The script's `--help` output documents what it checks, making the fallback natural — the LLM reads the help to understand the script's purpose and replicates the logic.

Frame script steps as outcomes in the SKILL.md, not just commands:

| Approach | Example |
| -------- | ------- |
| **Good** | "Validate path conventions (run `scripts/scan-paths.py --help` for details)" |
| **Fragile** | "Execute `python3 scripts/scan-paths.py`" with no context |

The good version tells the LLM both what to accomplish and where to find the details — enabling graceful degradation without additional instructions.

## When to Reach for a Script

Look for these signal verbs in a skill's requirements — they indicate script opportunities:

| Signal | Script Type |
| ------ | ----------- |
| "validate", "check", "verify" | Validation |
| "count", "tally", "aggregate" | Metrics |
| "extract", "parse", "pull from" | Data extraction |
| "convert", "transform", "format" | Transformation |
| "compare", "diff", "match against" | Comparison |
| "scan for", "find all", "list all" | Pattern scanning |

The builders guide you through script opportunity discovery during the build process. The key insight: if you find yourself writing detailed validation logic in a prompt, it almost certainly belongs in a script instead.
