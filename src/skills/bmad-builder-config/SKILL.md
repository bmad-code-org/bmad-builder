---
name: bmad-builder-config
description: Installs BMad Builder module into a project. Use when the user requests to 'install bmb module', 'configure bmad builder', or 'setup bmad builder'.
---

# BMad Builder Config

## Overview

Installs and configures the BMad Builder (bmb) module into a project. Collects user preferences, writes them to a shared `{project-root}/_bmad/config.yaml`, and registers module capabilities in `{project-root}/_bmad/module-help.csv`. Both scripts use an anti-zombie pattern — existing entries for this module are removed before writing fresh ones, so stale values never persist.

## On Activation

1. Confirm `{project-root}` with the user — display the detected project root and verify before proceeding
2. Read `assets/module.yaml` for module metadata and variable definitions
3. Check if `{project-root}/_bmad/config.yaml` exists — if a `bmb` section is already present, inform the user this is an update

## Collect Configuration

Ask the user for values. Show defaults in brackets; accept blank for default. Pre-fill from existing config values when updating.

**Core config** (only if no `core` section exists yet): `user_name` (required, no default), `communication_language`, `document_output_language`, `output_folder`. These are shared across all modules.

**Module config**: Read each variable in `assets/module.yaml` that has a `prompt` field. Ask using that prompt with its `default` value.

## Write Files

Write a temp JSON file with the collected answers structured as `{"core": {...}, "module": {...}}` (omit `core` if it already exists). Then run both scripts — they can run in parallel since they write to different files:

```bash
python3 scripts/merge-config.py --config-path "{project-root}/_bmad/config.yaml" --module-yaml assets/module.yaml --answers {temp-file}
python3 scripts/merge-help-csv.py --target "{project-root}/_bmad/module-help.csv" --source assets/module-help.csv
```

Both scripts output JSON to stdout with results. If either exits non-zero, surface the error and stop.

Run `scripts/merge-config.py --help` or `scripts/merge-help-csv.py --help` for full usage.

## Confirm

Use the script JSON output to display what was written — config values set, help entries added, fresh install vs update.
