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

Identify deterministic operations that should be scripts. Load `./references/script-opportunities-reference.md` for the full catalog. Confirm the script-vs-prompt plan with the user before proceeding.

If scripts are planned, the `./scripts/` folder will be created. Scripts are invoked from prompts when needed, not run automatically.

## Phase 3: Gather Requirements

Gather requirements through conversation: identity, capabilities (internal prompts + external skills), activation modes, memory needs, and access boundaries. Refer to `./references/standard-fields.md` for conventions.

Key structural context:

- **Naming:** Standalone agents use `bmad-agent-{name}`, module agents use `bmad-{modulecode}-agent-{name}`
- **Activation modes:** Interactive only, or Interactive + Headless (also runs on schedule/cron for background tasks)
- **Memory architecture:** See `./references/memory-system.md` template. Sidecar at `{project-root}/_bmad/memory/{skillName}-sidecar/`
- **Access boundaries:** Read/write/deny zones stored in memory as the standard `access-boundaries` section

**If headless mode is enabled, also gather:**
- Default wake behavior (`--headless` | `-H` with no specific task)
- Named tasks (`--headless:{task-name}` or `-H:{task-name}`)

- **Path Conventions** (CRITICAL for reliable agent behavior):
  - **Memory location:** `{project-root}/_bmad/memory/{skillName}-sidecar/`
  - **Project artifacts:** `{project-root}/_bmad/...` when referencing project-level files
  - **Skill-internal files:** Always use `./` prefix (`./references/`, `./scripts/`) — this distinguishes them from `{project-root}` paths
  - **Config variables:** Use directly — they already contain full paths (NO `{project-root}` prefix)
    - Correct: `{output_folder}/file.md`
    - Wrong: `{project-root}/{output_folder}/file.md` (double-prefix breaks resolution)
  - **No absolute paths** (`/Users/...`)

## Phase 4: Draft & Refine

Once you have a cohesive idea, think one level deeper. Once you have done this, present a draft outline. Point out vague areas. Ask what else is needed. Iterate until they say they're ready.

## Phase 5: Build

**Always load these before building:**
- Load `./references/standard-fields.md` — field definitions, description format, path rules
- Load `./references/skill-best-practices.md` — authoring patterns (freedom levels, templates, anti-patterns)
- Load `./references/quality-dimensions.md` — quick mental checklist for build quality

**Load based on context:**
- **Always load** `./references/script-opportunities-reference.md` — script opportunity spotting guide, catalog, and output standards. Use this to identify additional script opportunities not caught in Phase 2, even if no scripts were initially planned.

Build the agent skill structure using templates from `./assets/` and rules from `./references/template-substitution-rules.md`. Output to `{bmad_builder_output_folder}`.

**Lint gate** — after building, run validation and auto-fix failures:

If subagents are available, delegate the lint-fix loop to a subagent. Otherwise run inline.

1. Run both lint scripts in parallel:
   ```bash
   python3 ./scripts/scan-path-standards.py {skill-path}
   python3 ./scripts/scan-scripts.py {skill-path}
   ```
2. If any findings at high or critical severity: fix them and re-run the failing script
3. Repeat up to 3 attempts per script — if still failing after 3, report remaining findings and continue
4. If scripts exist in the built skill, also run unit tests (`./scripts/run-tests.sh` or equivalent)

**Folder structure:**
```
{skill-name}/
├── SKILL.md               # Frontmatter (name + description only), persona, activation, capability routing
├── references/            # ALL progressive disclosure content lives here
│   ├── {capability}.md    # Each internal capability prompt
│   ├── memory-system.md   # Memory discipline and structure (if sidecar)
│   ├── init.md            # First-run onboarding (if sidecar)
│   ├── autonomous-wake.md # Headless activation (if headless mode)
│   └── save-memory.md     # Explicit memory save (if sidecar)
├── assets/                # Templates, starter files (copied/transformed into output)
└── scripts/               # Deterministic code — validation, transformation, testing
    └── run-tests.sh       # uvx-powered test runner (if python tests exist)
```

**What goes where:**
| Location | Contains | LLM relationship |
|----------|----------|-----------------|
| **SKILL.md** | Persona, activation, capability routing table | LLM **identity and router** — the only root `.md` file |
| **`./references/`** | Capability prompts, reference data, schemas, guides | LLM **loads on demand** — progressive disclosure via routing table |
| **`./assets/`** | Templates, starter files, boilerplate | LLM **copies/transforms** these into output — not for reasoning |
| **`./scripts/`** | Python, shell scripts with tests | LLM **invokes** these — deterministic operations that don't need judgment |

Only create subfolders that are needed — most agents won't need all three.

**Activation guidance for built agents:**

Activation is a single flow regardless of mode (interactive or headless). It should:
- Load config and resolve values (with defaults — see SKILL.md step 2)
- Load sidecar `index.md` if the agent has memory — this is the single entry point that tells the agent what else to load
- If headless, route to `./references/autonomous-wake.md` and complete without interaction
- If interactive, greet the user and either continue naturally from memory context or offer to show available capabilities

## Phase 6: Summary

Present what was built: location, structure, first-run behavior, capabilities. Ask if adjustments needed.

**After the build completes, offer quality optimization:**

Ask: *"Build is done. Would you like to run a Quality Scan to optimize the agent further?"*

If yes, load `quality-optimizer.md` with `{scan_mode}=full` and the agent path.

Remind them: BMad module system compliant. Use the module-init skill to install and configure into a project.
