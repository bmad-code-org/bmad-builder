---
name: bmad-{module-code-or-empty}{skill-name}
description: {skill-description} # Format: [5-8 word summary]. [trigger phrase, e.g. Use when user says "create xyz"]
---

# {skill-name}

## Overview

{overview-template}

{if-simple-utility}
## Input

{input-format-description}

## Process

{processing-steps}

## Output

{output-format-description}
{/if-simple-utility}

{if-simple-workflow}
Act as {role-guidance}.

## On Activation

1. **Load config** from `{project-root}/_bmad/config.yaml` — Store all returned vars for use:
   - Use `{user_name}` from config for greeting
   - Use `{communication_language}` for all communications
   {if-creates-docs}- Use `{document_output_language}` for output documents{/if-creates-docs}

2. **Greet user** as `{user_name}`, speaking in `{communication_language}`

3. **Proceed to workflow steps below**

## Workflow Steps

### Step 1: {step-1-name}
{step-1-instructions}

### Step 2: {step-2-name}
{step-2-instructions}

### Step 3: {step-3-name}
{step-3-instructions}
{/if-simple-workflow}

{if-complex-workflow}
Act as {role-guidance}.

{if-headless}
## Activation Mode Detection

**Check activation context immediately:**

1. **Headless mode**: If the user passes `--headless` or `-H` flags, or if their intent clearly indicates non-interactive execution:
   - Skip questions, proceed with safe defaults, output structured results
   - If `--headless:{task-name}` → run that specific task headless mode
   - If just `--headless` → run default headless behavior

2. **Interactive mode** (default): Proceed to `## On Activation` section below
{/if-headless}

## On Activation

1. **Load config** from `{project-root}/_bmad/config.yaml` — Store all returned vars for use:
   - Use `{user_name}` from config for greeting
   - Use `{communication_language}` for all communications
   {if-creates-docs}- Use `{document_output_language}` for output documents{/if-creates-docs}
   - Store any other config variables as `{var-name}` and use appropriately

2. **Greet user** as `{user_name}`, speaking in `{communication_language}`

3. **Check if workflow in progress:**
   - If output doc exists (user specifies path or we prompt):
     - Read doc to determine current stage
     - Resume from last completed stage
   - Else: Start at `01-{stage-1-name}.md`

4. **Route to appropriate stage** based on progress

{if-headless}
**Headless mode routing:**
- Default: Run all stages sequentially with safe defaults
- Named task: Execute specific stage or task
- Output structured JSON results when complete
{/if-headless}

## Stages

| # | Stage | Purpose | Prompt |
|---|-------|---------|--------|
| 1 | {stage-1-name} | {stage-1-purpose} | `01-{stage-1-name}.md` |
| 2 | {stage-2-name} | {stage-2-purpose} | `02-{stage-2-name}.md` |
{/if-complex-workflow}

{if-external-skills}
## External Skills

This workflow uses:
{external-skills-list}
{/if-external-skills}

{if-scripts}
## Scripts

Available scripts in `scripts/`:
- `{script-name}` — {script-description}
{/if-scripts}
