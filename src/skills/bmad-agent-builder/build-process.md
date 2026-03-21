---
name: build-process
description: Six-phase conversational discovery process for building BMad agents. Covers intent discovery, capabilities strategy, requirements gathering, drafting, building, and summary.
---

**Language:** Use `{communication_language}` for all output.

# Build Process

Build AI agents through six phases of conversational discovery. Act as an architect guide — probe deeper than what users articulate, suggest what they haven't considered, and build something that exceeds what they imagined.

## Phase 1: Discover Intent

Understand their vision before diving into specifics. Ask what they want to build and encourage detail.

If editing/converting an existing agent: read it, analyze what exists vs what's missing, understand what needs changing and specifically ensure it conforms to our standard with building new agents upon completion.

## Phase 2: Capabilities Strategy

Early check: internal capabilities only, external skills, both, or unclear?

**If external skills involved:** Suggest `bmad-module-builder` to bundle agents + skills into a cohesive module. Modules are the heart of the BMad ecosystem — shareable packages for any domain.

**Script Opportunity Discovery** (active probing — do not skip):
Walk through each planned capability with the user and apply these filters:
1. "Does this operation have clear pass/fail criteria?" → Script candidate
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
- Memory structure validation (required sections, path correctness)
- Access boundary extraction and verification
- Dependency graphing (parsing imports, references, skill entries)
- Pre-processing for LLM capabilities (extract compact metrics from large files so the LLM works from structured data, not raw content)
- Post-processing validation (verify LLM output conforms to expected schema/structure)

**Present your script plan**: Before moving to Phase 3, explicitly tell the user which operations you plan to implement as scripts vs. prompts, with one-line reasoning for each. Ask if they agree or want to adjust.

If scripts are planned, the `scripts/` folder will be created. Scripts are invoked from prompts when needed, not run automatically.

## Phase 3: Gather Requirements

Work through these conversationally:

- **Name:** Functional (kebab-case), display name, title, icon
- **Overview:** Draft a 2-3 sentence overview following the 3-part formula:
  - **What** — What this agent does
  - **How** — Role, approach, or key capabilities
  - **Why/Outcome** — Value delivered or quality standard
  - *Example:* "This skill provides a {role} who helps users {outcome}. Act as {name} — {key quality}."
- **Identity:** Who is this agent? How do they communicate? What guides their decisions?
- **Module context:** Standalone (`bmad-agent-{name}`) or part of a module (`bmad-{modulecode}-agent-{name}`)
- **Activation modes:**
  - **Interactive only** — User invokes the agent directly
  - **Interactive + Autonomous** — Also runs on schedule/cron for background tasks
- **Memory & Persistence:**
  - **Sidecar needed?** — What persists across sessions?
  - **Critical data** (must persist immediately): What data is essential to capture the moment it's created?
  - **Checkpoint data** (save periodically): What can be batched and saved occasionally?
  - **Save triggers:** After which interactions should memory be updated?
- **Capabilities:**
  - **Internal prompts:** Capabilities the agent knows itself (each will get its own prompt file)
  - **External skills:** Skills the agent invokes (ask for **exact registered skill names** — e.g., `skill-creator`)
    - Note: Skills may exist now or be created later
- **First-run:** What should it ask on first activation? (standalone only; module-based gets config from module's config.yaml)

**If autonomous mode is enabled, ask additional questions:**
- **Autonomous tasks:** What should the agent do when waking on a schedule?
  - Examples: Review/organize memory, process queue, maintenance tasks, implement tickets
- **Default wake behavior:** What happens with `--headless` | `-H` (no specific task)?
- **Named tasks:** What specific tasks can be invoked with `--headless:{task-name}` or `-H:{task-name}`?

- **Folder Dominion / Access Boundaries:**
  - **What folders can this agent read from?** (e.g., `journals/`, `financials/`, specific file patterns)
  - **What folders can this agent write to?** (e.g., output folders, log locations)
  - **Are there any explicit deny zones?** (folders the agent must never touch)
  - Store these boundaries in memory as the standard `access-boundaries` section (see memory-system template)

**Key distinction:** Folder dominion (where things live) ≠ agent memory (what persists across sessions)

- **Path Conventions** (CRITICAL for reliable agent behavior):
  - **Memory location:** `{project-root}/_bmad/memory/{skillName}-sidecar/`
  - **Project artifacts:** `{project-root}/_bmad/...` when referencing project-level files
  - **Skill-internal files:** Use relative paths (`references/`, `scripts/`)
  - **Config variables:** Use directly — they already contain full paths (NO `{project-root}` prefix)
    - Correct: `{output_folder}/file.md`
    - Wrong: `{project-root}/{output_folder}/file.md` (double-prefix breaks resolution)
  - **No absolute paths** (`/Users/...`) or relative prefixes (`./`, `../`)

## Phase 4: Draft & Refine

Once you have a cohesive idea, think one level deeper. Once you have done this, present a draft outline. Point out vague areas. Ask what else is needed. Iterate until they say they're ready.

## Phase 5: Build

**Always load these before building:**
- Load `references/standard-fields.md` — field definitions, description format, path rules
- Load `references/skill-best-practices.md` — authoring patterns (freedom levels, templates, anti-patterns)
- Load `references/quality-dimensions.md` — quick mental checklist for build quality

**Load based on context:**
- **Always load** `references/script-opportunities-reference.md` — script opportunity spotting guide, catalog, and output standards. Use this to identify additional script opportunities not caught in Phase 2, even if no scripts were initially planned.

When confirmed:

1. Load template substitution rules from `references/template-substitution-rules.md` and apply

2. Create skill structure using templates from `assets/` folder:
   - **SKILL-template.md** — skill wrapper with full persona content embedded
   - **init-template.md** — first-run setup (if sidecar)
   - **memory-system.md** — memory (if sidecar, saved at root level)
   - **autonomous-wake.md** — autonomous activation behavior (if activation_modes includes "autonomous")
   - **save-memory.md** — explicit memory save capability (if sidecar enabled)

3. **Folder structure:**
```
{skill-name}/
├── SKILL.md               # Contains full persona content (agent.md embedded)
├── init.md                # First-run setup (if sidecar)
├── autonomous-wake.md     # Autonomous activation (if autonomous mode)
├── save-memory.md         # Explicit memory save (if sidecar)
├── {name}.md              # Each internal capability prompt
├── references/            # Reference data, schemas, guides (read for context)
│   └── memory-system.md   # (if sidecar needed)
├── assets/                # Templates, starter files (copied/transformed into output)
└── scripts/               # Deterministic code — validation, transformation, testing
    └── run-tests.sh       # uvx-powered test runner (if python tests exist)
```

**What goes where:**
| Location | Contains | LLM relationship |
|----------|----------|-----------------|
| **Root `.md` files** | Prompt/instruction files, subagent definitions | LLM **loads and executes** these as instructions — they are extensions of SKILL.md |
| **`references/`** | Reference data, schemas, tables, examples, guides | LLM **reads for context** — informational, not executable |
| **`assets/`** | Templates, starter files, boilerplate | LLM **copies/transforms** these into output — not for reasoning |
| **`scripts/`** | Python, shell scripts with tests | LLM **invokes** these — deterministic operations that don't need judgment |

Only create subfolders that are needed — most skills won't need all four.

4. Output to `bmad_builder_output_folder` from config, or `{project-root}/bmad-builder-creations/`

5. **Lint gate** — run deterministic validation scripts:
   ```bash
   python3 scripts/scan-path-standards.py {skill-path}
   python3 scripts/scan-scripts.py {skill-path}
   ```
   - If any script returns critical issues: fix them before proceeding
   - If only warnings/medium: note them but proceed

## Phase 6: Summary

Present what was built: location, structure, first-run behavior, capabilities. Ask if adjustments needed.

**After the build completes, offer quality optimization:**

Ask: *"Build is done. Would you like to run a Quality Scan to optimize the agent further?"*

If yes, load `quality-optimizer.md` with `{scan_mode}=full` and the agent path.

Remind them: BMad module system compliant. Use the module-init skill to install and configure into a project.
