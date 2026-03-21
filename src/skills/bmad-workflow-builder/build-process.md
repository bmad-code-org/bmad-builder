---
name: build-process
description: Six-phase conversational discovery process for building BMad workflows and skills. Covers intent discovery, skill type classification, requirements gathering, drafting, building, and summary.
---

**Language:** Use `{communication_language}` for all output.

# Build Process

Build workflows and skills through six phases of conversational discovery. Act as an architect guide — help users articulate their vision completely, classify the right skill type, and build something that exceeds what they imagined.

## Phase 1: Discover Intent

Understand their vision before diving into specifics. Let them describe what they want to build, encourage them to be as detailed as possible including edge cases, variants, tone and persona of the workflow if needed, tools or other skills.

**Input flexibility:** Accept input in any format:
- Existing BMad workflow/skill path → read, analyze, determine if editing or converting
- Rough idea or description → guide through discovery
- Code, documentation, API specs → extract intent and requirements
- Non-BMad skill/tool → convert to BMad-compliant structure

If editing/converting an existing skill: read it, analyze what exists vs what's missing, ensure BMad standard conformance.

Remember, the best user experience for this process is you conversationally allowing the user to give us info in this stage and you being able to confirm or suggest for them most of what you need for Phase 2 and 3.
For Phase 2 and 3 that follow, adapt to what you already know that the user has given you so far, since they just brain dumped and gave you a lot of information

## Phase 2: Classify Skill Type

Ask upfront:
- Will this be part of a module? If yes:
   - What's the module code? (so we can configure properly)
   - What other skills will it use from the core or specified module, we need the name, inputs, and output so we know how to integrate it? (bmad-init is default unless explicitly opted out, other skills should be either core skills or skills that will be part of the module)
   - What are the variable names it will have access to that it needs to use? (variables can be use for things like choosing various paths in the skill, adjusting output styles, configuring output locations, tool availability, and anything that could be configurable by a user)

Load `references/classification-reference.md` for the full decision tree, classification signals, and module context rules. Use it to classify:

1. Composable building block with clear input/output and generally will use scripts either inline or in the scripts folder? → **Simple Utility**
2. Fits in a single SKILL.md, may have some resources and a prompt, but generally not very complex. Human in the Loop and Autonomous abilities? → **Simple Workflow**
   - **Headless mode?** Should this workflow support `--headless` invocation? (If it produces an artifact, headless mode may be valuable)
3. Needs multiple stages and branches, may be long-running, uses progressive disclosure with prompts and resources, usually Human in the Loop with multiple paths and prompts? → **Complex Workflow**

For Complex Workflows, also ask:
- **Headless mode?** Should this workflow support `--headless` invocation?

Present classification with reasoning. This determines template and structure.

## Phase 3: Gather Requirements

Work through conversationally, adapted per skill type, so you can either glean from the user or suggest based on their narrative.

**All types — Common fields:**
- **Name:** kebab-case. If module: `bmad-{modulecode}-{skillname}`. If standalone: `bmad-{skillname}`
- **Description:** Two parts: [5-8 word summary of what it does]. [Use when user says 'specific phrase' or 'specific phrase'.] — Default to explicit invocation (conservative triggering) unless user specifies organic/reactive activation. See `references/standard-fields.md` for format details and examples.
- **Overview:** 3-part formula (What/How/Why-Outcome). For interactive or complex skills, also include brief domain framing (what concepts does this skill operate on?) and theory of mind (who is the user and what might they not know?). These give the executing agent enough context to make judgment calls when situations don't match the script.
- **Role guidance:** Brief "Act as a [role/expert]" statement to prime the model for the right domain expertise and tone
- **Design rationale:** Any non-obvious choices the executing agent should understand? (e.g., "We interview before building because users rarely know their full requirements upfront")
- **Module context:** Already determined in Phase 2
- **External skills used:** Which skills does this invoke?
- **Script Opportunity Discovery** (active probing — do not skip):
  Walk through each planned step/stage with the user and apply these filters:
  1. "Does this step have clear pass/fail criteria?" → Script candidate
  2. "Could this run without LLM judgment — no interpretation, no creativity, no ambiguity?" → Strong script candidate
  3. "Does it validate, transform, count, parse, format-convert, compare against a schema, or check structure?" → Almost certainly a script

  **Common script-worthy operations:**
  - Schema/format validation (JSON, YAML, frontmatter, file structure)
  - Data extraction and transformation (parsing, restructuring, field mapping)
  - Counting, aggregation, and metric collection (token counts, file counts, summary stats)
  - File/directory structure checks (existence, naming conventions, required files)
  - Pattern matching against known standards (path conventions, naming rules)
  - Comparison operations (diff, version compare, before/after, cross-reference checking)
  - Dependency graphing (parsing imports, references, skill entries)
  - Template artifact detection (orphaned placeholders, unresolved variables)
  - Pre-processing for LLM steps (extract compact metrics from large files so the LLM works from structured data, not raw content)
  - Post-processing validation (verify LLM output conforms to expected schema/structure)

  **Present your script plan**: Before moving to Phase 4, explicitly tell the user which operations you plan to implement as scripts vs. prompts, with one-line reasoning for each. Ask if they agree or want to adjust.
- **Creates output documents?** If yes, will use `{document_output_language}` from config
**Simple Utility additional fields:**
- **Input format:** What does it accept?
- **Output format:** What does it return?
- **Standalone?** Opt out of bmad-init? (Makes it a truly standalone building block)
- **Composability:** How might this be used by other skills/workflows?
- **Script needs:** What scripts does the utility require?

**Simple Workflow additional fields:**
- **Steps:** Numbered steps (inline in SKILL.md)
- **Tools used:** What tools/CLIs/scripts does it use?
- **Output:** What does it produce?
- **Config variables:** What config vars beyond core does it need?

**Complex Workflow additional fields:**
- **Stages:** Named numbered stages with purposes
- **Stage progression conditions:** When does each stage complete?
- **Headless mode:** If yes, what should headless execution do? Default behavior? Named tasks?
- **Config variables:** Core + module-specific vars needed
- **Output artifacts:** What does this create? (output-location)
- **Dependencies:** What must run before this? What does it use? (after/before arrays)

**Module capability metadata (if part of a module):**
For each capability, confirm these with the user — they determine how the module's help system presents and sequences the skill:
- **phase-name:** Which module phase does this belong to? (e.g., "1-analysis", "2-design", "3-build", "anytime")
- **after:** Array of skill names that should ideally run before this one. Ask: "What does this skill use as input? What should have already run?" (e.g., `["brainstorming", "perform-research"]`)
- **before:** Array of skill names this should run before. Ask: "What downstream skills consume this skill's output?" (e.g., `["create-prd"]`)
- **is-required:** If true, skills in the `before` array are blocked until this completes. If false, the ordering is a suggestion (nice-to-have input, not a hard dependency).
- **description (capability):** Keep this VERY short — a single sentence describing what it produces, not how it works. This is what the LLM help system shows users. (e.g., "Produces executive product brief and optional LLM distillate for PRD input.")

**Path conventions (CRITICAL):**
- Skill-internal files use bare relative paths: `references/`, `scripts/`, and prompt files at root
- Only `_bmad` paths get `{project-root}` prefix: `{project-root}/_bmad/...`
- Config variables used directly — they already contain `{project-root}` (no double-prefix)

## Phase 4: Draft & Refine

Once you have a cohesive idea, think one level deeper, clarify with the user any gaps in logic or understanding. Create and present a plan. Point out vague areas. Ask what else is needed. Iterate until they say they're ready.

## Phase 5: Build

**Always load these before building:**
- Load `references/standard-fields.md` — field definitions, description format, path rules
- Load `references/skill-best-practices.md` — authoring patterns (freedom levels, templates, anti-patterns)
- Load `references/quality-dimensions.md` — quick mental checklist for build quality

**Load based on skill type:**
- **If Complex Workflow:** Load `references/complex-workflow-patterns.md` — compaction survival, document-as-cache pattern, config integration, facilitator model, progressive disclosure with prompt files at root. This is essential for building workflows that survive long-running sessions.
- **Always load** `references/script-opportunities-reference.md` — script opportunity spotting guide, catalog, and output standards. Use this to identify additional script opportunities not caught in Phase 3, even if no scripts were initially planned.

When confirmed:

1. Load template substitution rules from `references/template-substitution-rules.md` and apply

2. Load unified template: `assets/SKILL-template.md`
   - Apply skill-type conditionals (`{if-complex-workflow}`, `{if-simple-workflow}`, `{if-simple-utility}`) to keep only relevant sections

3. **Progressive disclosure:** Keep SKILL.md focused on Overview, activation, and routing. Detailed stage instructions go in prompt files at the skill root. Reference data, schemas, and large tables go in `references/`. Multi-branch SKILL.md under ~250 lines is fine as-is; single-purpose up to ~500 lines if genuinely needed.

4. Generate folder structure and include only what is needed for the specific skill:
**Skill Source Tree:**
```
{skill-name}/
├── SKILL.md           # name (same as folder name), description
├── *.md               # Prompt files and subagent definitions at root
├── references/        # Reference data, schemas, guides (read for context)
├── assets/            # Templates, starter files (copied/transformed into output)
├── scripts/           # Deterministic code — validation, transformation, testing
│   └── tests/         # All scripts need unit tests
```

**What goes where:**
| Location | Contains | LLM relationship |
|----------|----------|-----------------|
| **Root `.md` files** | Prompt/instruction files, subagent definitions | LLM **loads and executes** these as instructions — they are extensions of SKILL.md |
| **`references/`** | Reference data, schemas, tables, examples, guides | LLM **reads for context** — informational, not executable |
| **`assets/`** | Templates, starter files, boilerplate | LLM **copies/transforms** these into output — not for reasoning |
| **`scripts/`** | Python, shell scripts with tests | LLM **invokes** these — deterministic operations that don't need judgment |

Only create subfolders that are needed — most skills won't need all four.

5. Output to {`bmad_builder_output_folder`}

6. **Lint gate** — run deterministic validation scripts:
   ```bash
   # Run both in parallel — they are independent
   python3 scripts/scan-path-standards.py {skill-path}
   python3 scripts/scan-scripts.py {skill-path}
   ```
   - If any script returns critical issues: fix them before proceeding
   - If only warnings/medium: note them but proceed
   - These are structural checks — broken paths and script standards issues should be resolved before shipping

## Phase 6: Summary

Present what was built: location, structure, capabilities. Include lint results. Ask if adjustments needed.

If scripts exist, also run unit tests.

**Remind user to commit** working version before optimization.

**Offer quality optimization:**

Ask: *"Build is done. Would you like to run a Quality Scan to optimize further?"*

If yes, load `quality-optimizer.md` with `{scan_mode}=full` and the skill path.
