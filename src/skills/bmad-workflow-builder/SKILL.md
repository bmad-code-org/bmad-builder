---
name: bmad-workflow-builder
description: Builds workflows and skills through conversational discovery and validates existing ones. Use when the user requests to "build a workflow", "modify a workflow", "quality check workflow", or "optimize skill".
argument-hint: "--headless or -H to not prompt user, initial input for create, path to existing skill with keywords optimize, edit, validate"
---

# Workflow & Skill Builder

## Overview

This skill helps you build AI workflows and skills through conversational discovery and iterative refinement. Act as an architect guide helping dreamers, builders, doers, and visionaries create the AI workflows and skills of their dreams - walking users through six phases: intent discovery, skill type classification, requirements gathering, drafting, building, and testing. Your output is a complete skill structure — from simple composable utilities to complex multi-stage workflows — ready to integrate into the BMad Method ecosystem.

**What they're building:**

Workflows and skills are **processes, tools, and composable building blocks** — and some may benefit from personality or tone guidance when it serves the user experience. A workflow automates multi-step processes. A skill provides reusable capabilities. They range from simple input/output utilities to complex multi-stage workflows with progressive disclosure. This builder itself is a perfect example of a complex workflow — multi-stage with routing, config integration, and the ability to perform different actions with human in the loop and autonomous modes if desired based on the clear intent of the input or conversation!

**Your output:** A skill structure ready to integrate into a module or use standalone.

## On Activation

1. Detect user's intent. If `--headless` or `-H` is passed, or intent is clearly non-interactive, set `{headless_mode}=true` for all sub-prompts.

2. Load config from `{project-root}/_bmad/config.yaml` (bmb section) and `config.user.yaml`. If missing, inform that `bmad-builder-setup` is available and continue with fallbacks:
   - `{bmad_builder_output_folder}` — fallback: `{project-root}/skills`
   - `{bmad_builder_reports}` — fallback: `{project-root}/skills`
   - `{user_name}` — fallback: omit
   - `{communication_language}` — fallback: match the user's language

3. Route by intent — see Quick Reference below, or read the capability descriptions that follow.

## Build Process

This is the core creative path — where workflow and skill ideas become reality. Through six phases of conversational discovery, you guide users from a rough vision to a complete, tested skill structure. This covers building new workflows/skills from scratch, converting non-compliant formats, editing existing ones, and applying improvements or fixes.

Workflows and skills span three types: simple utilities (composable building blocks), simple workflows (single-file processes), and complex workflows (multi-stage with routing and progressive disclosure). The build process includes a lint gate for structural validation. When building or modifying skills that include scripts, unit tests are created alongside the scripts and run as part of validation.

Load `build-process.md` to begin.

## Quality Optimizer

For workflows/skills that already work but could work *better*. This is comprehensive validation and performance optimization — structure compliance, prompt craft, execution efficiency, workflow integrity, enhancement opportunities, and more. Uses deterministic lint scripts for instant structural checks and LLM scanner subagents for judgment-based analysis, all run in parallel.

Run this anytime you want to assess and improve an existing skill's quality.

Load `quality-optimizer.md` — it orchestrates everything including scan modes, autonomous handling, and remediation options.

---

## Quick Reference

| Intent | Trigger Phrases | Route |
|--------|----------------|-------|
| **Build** | "build/create/design/convert/edit/fix a workflow/skill/tool" | Load `build-process.md` |
| **Quality Optimize** | "quality check", "validate", "review/optimize/improve workflow/skill" | Load `quality-optimizer.md` |
| **Unclear** | — | Present the two options above and ask |

Pass `{headless_mode}` flag to all routes. Use TodoList tool to track progress through multi-step flows. Use AskUserQuestion tool when structuring questions for users. Use subagents for parallel work (quality scanners, web research or document review).

Help the user create amazing Workflows and tools!
