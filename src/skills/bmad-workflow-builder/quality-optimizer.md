---
name: quality-optimizer
description: Comprehensive quality validation for BMad workflows and skills. Runs deterministic lint scripts and spawns parallel subagents for judgment-based scanning. Returns consolidated findings as structured JSON.
menu-code: QO
---

# Quality Optimizer

Communicate with user in `{communication_language}`. Write report content in `{document_output_language}`.

You orchestrate quality scans on a BMad workflow or skill. Deterministic checks run as scripts (fast, zero tokens). Judgment-based analysis runs as LLM subagents. You synthesize all results into a unified report.

## Your Role: Coordination, Not File Reading

**DO NOT read the target skill's files yourself.** Scripts and subagents do all analysis.

You orchestrate quality scans: run deterministic scripts and pre-pass extractors, spawn LLM scanner subagents in parallel, then synthesize all results into a unified report.

## Headless Mode

If `{headless_mode}=true`, skip all user interaction, use safe defaults, note any warnings, and output structured JSON as specified in the Present Findings section.

## Pre-Scan Checks

Check for uncommitted changes. In headless mode, note warnings and proceed. In interactive mode, inform the user and confirm before proceeding. In interactive mode, also confirm the workflow is currently functioning.

## Optimization Principles

**Workflow skills are both art and science.** The optimization report will contain many suggestions — apply judgment:

- Reports may suggest leaner phrasing — but if the current phrasing captures the right guidance, keep it
- Reports may say content is "unnecessary" — but if it adds clarity, it may be worth keeping
- Reports may suggest scripting vs. prompting — consider what works best for the use case

**Over-optimization warning:** Optimizing too aggressively can make workflows lose their effectiveness. Apply human judgment alongside the report's suggestions.

## Quality Scanners

### Lint Scripts (Deterministic — Run First)

These run instantly, cost zero tokens, and produce structured JSON:

| # | Script | Focus | Temp Filename |
|---|--------|-------|---------------|
| S1 | `scripts/scan-path-standards.py` | Path conventions: {project-root} only for _bmad, bare _bmad, double-prefix, absolute paths | `path-standards-temp.json` |
| S2 | `scripts/scan-scripts.py` | Script portability, PEP 723, agentic design, unit tests | `scripts-temp.json` |

### Pre-Pass Scripts (Feed LLM Scanners)

These extract metrics for the LLM scanners so they work from compact data instead of raw files:

| # | Script | Feeds | Temp Filename |
|---|--------|-------|---------------|
| P1 | `scripts/prepass-workflow-integrity.py` | workflow-integrity LLM scanner | `workflow-integrity-prepass.json` |
| P2 | `scripts/prepass-prompt-metrics.py` | prompt-craft LLM scanner | `prompt-metrics-prepass.json` |
| P3 | `scripts/prepass-execution-deps.py` | execution-efficiency LLM scanner | `execution-deps-prepass.json` |

### LLM Scanners (Judgment-Based — Run After Scripts)

| # | Scanner | Focus | Pre-Pass? | Temp Filename |
|---|---------|-------|-----------|---------------|
| L1 | `quality-scan-workflow-integrity.md` | Logical consistency, description quality, progression condition quality, type-appropriate structure | Yes — receives prepass JSON | `workflow-integrity-temp.json` |
| L2 | `quality-scan-prompt-craft.md` | Token efficiency, anti-patterns, outcome balance, Overview quality, progressive disclosure | Yes — receives metrics JSON | `prompt-craft-temp.json` |
| L3 | `quality-scan-execution-efficiency.md` | Parallelization, subagent delegation, read avoidance, context optimization | Yes — receives dep graph JSON | `execution-efficiency-temp.json` |
| L4 | `quality-scan-skill-cohesion.md` | Stage flow coherence, purpose alignment, complexity appropriateness | No | `skill-cohesion-temp.json` |
| L5 | `quality-scan-enhancement-opportunities.md` | Creative edge-case discovery, experience gaps, delight opportunities, assumption auditing | No | `enhancement-opportunities-temp.json` |
| L6 | `quality-scan-script-opportunities.md` | Deterministic operation detection — finds LLM work that should be scripts instead | No | `script-opportunities-temp.json` |

## Execution Instructions

First create output directory: `{bmad_builder_reports}/{skill-name}/quality-scan/{date-time-stamp}/`

### Step 1: Run Lint Scripts (Parallel)

Run all applicable lint scripts in parallel. They output JSON to stdout — capture to temp files in the output directory:

```bash
# Full scan runs all 2 lint scripts + all 3 pre-pass scripts (5 total, all parallel)
python3 scripts/scan-path-standards.py {skill-path} -o {quality-report-dir}/path-standards-temp.json
python3 scripts/scan-scripts.py {skill-path} -o {quality-report-dir}/scripts-temp.json
uv run scripts/prepass-workflow-integrity.py {skill-path} -o {quality-report-dir}/workflow-integrity-prepass.json
python3 scripts/prepass-prompt-metrics.py {skill-path} -o {quality-report-dir}/prompt-metrics-prepass.json
uv run scripts/prepass-execution-deps.py {skill-path} -o {quality-report-dir}/execution-deps-prepass.json
```

### Step 2: Spawn LLM Scanners (Parallel)

After scripts complete, spawn applicable LLM scanners as parallel subagents.

**For scanners WITH pre-pass (L1, L2, L3):** provide the pre-pass JSON file path so the scanner reads compact metrics instead of raw files. The subagent should read the pre-pass JSON first, then only read raw files for judgment calls the pre-pass doesn't cover.

**For scanners WITHOUT pre-pass (L4, L5, L6):** provide just the skill path and output directory as before.

Each subagent receives:
- Scanner file to load (e.g., `quality-scan-skill-cohesion.md`)
- Skill path to scan: `{skill-path}`
- Output directory for results: `{quality-report-dir}`
- Temp filename for output: `{temp-filename}`
- Pre-pass file path (if applicable): `{quality-report-dir}/{prepass-filename}`

The subagent will:
- Load the scanner file and operate as that scanner
- Read pre-pass JSON first if provided, then read raw files only as needed
- Output findings as detailed JSON to: `{quality-report-dir}/{temp-filename}.json`
- Return only the filename when complete

## Synthesis

After all scripts and scanners complete:

**IF only lint scripts ran (no LLM scanners):**
1. Read the script output JSON files
2. Present findings directly — these are definitive pass/fail results

**IF single LLM scanner (with or without scripts):**
1. Read all temp JSON files (script + scanner)
2. Present findings directly in simplified format
3. Skip report creator (not needed for single scanner)

**IF multiple LLM scanners:**
1. Initiate a subagent with `report-quality-scan-creator.md`

**Provide the subagent with:**
- `{skill-path}` — The skill being validated
- `{temp-files-dir}` — Directory containing all `*-temp.json` files (both script and LLM results)
- `{quality-report-dir}` — Where to write the final report

## Generate HTML Report

After the report creator finishes (or after presenting lint-only / single-scanner results), generate the interactive HTML report:

```bash
python3 scripts/generate-html-report.py {quality-report-dir} --open
```

This produces `{quality-report-dir}/quality-report.html` — a self-contained interactive report with severity filters, collapsible sections, per-item copy-prompt buttons, and a batch prompt generator. The `--open` flag opens it in the default browser.

## Present Findings to User

After receiving the JSON summary from the report creator:

**IF `{headless_mode}=true`:**
1. **Output structured JSON:**
```json
{
  "headless_mode": true,
  "scan_completed": true,
  "report_file": "{full-path-to-report}",
  "html_report": "{full-path-to-html}",
  "warnings": ["any warnings from pre-scan checks"],
  "summary": {
    "total_issues": 0,
    "critical": 0,
    "high": 0,
    "medium": 0,
    "low": 0,
    "overall_quality": "{Excellent|Good|Fair|Poor}",
    "truly_broken_found": false
  }
}
```
2. **Exit** — Don't offer next steps, don't ask questions

**IF `{headless_mode}=false` or not set:**
1. **High-level summary** with total issues by severity
2. **Highlight truly broken/missing** — CRITICAL and HIGH issues prominently
3. **Mention reports** — "Full report: {report_file}" and "Interactive HTML report opened in browser (also at: {html_report})"
4. **Offer next steps:**
   - Apply fixes directly
   - Use the HTML report to select specific items and generate prompts
   - Discuss specific findings

## Key Principle

Your role is ORCHESTRATION: run scripts, spawn subagents, synthesize results. Scripts handle deterministic checks (paths, schema, script standards). LLM scanners handle judgment calls (cohesion, craft, efficiency). You coordinate both and present unified findings.
