# BMad Module Workflows

Advanced patterns for BMad module workflows — long-running, multi-stage processes with progressive disclosure, config integration, and compaction survival.

---

## Workflow Persona: Facilitator Model

BMad workflows treat the human operator as the expert. The agent's role is **facilitator**, not replacement.

**Principles:**
- Ask clarifying questions when requirements are ambiguous
- Present options with trade-offs, don't assume preferences
- Validate decisions before executing irreversible actions
- The operator knows their domain; the workflow knows the process

**Example voice:**
```markdown
## Discovery
I found 3 API endpoints that could handle this. Which approach fits your use case?

**Option A**: POST /bulk-import — Faster, but no validation until complete
**Option B**: POST /validate + POST /import — Slower, but catches errors early
**Option C**: Streaming import — Best of both, requires backend support

Which would you prefer?
```

---

## Config Reading and Integration

Workflows read config values from `{project-root}/_bmad/config.yaml` and `config.user.yaml`. The loading behavior differs based on whether the skill is part of a module or standalone.

### Config Loading Pattern

**Module-based skills** — load config with fallback and setup skill awareness:
```
Load config from {project-root}/_bmad/config.yaml ({module-code} section) and config.user.yaml.
If config is missing:
  - Inform the user that the module setup skill ({module-setup-skill}) is available for initial setup
  - Continue with sensible fallback values for each variable
```

**Standalone skills** — load config best-effort:
```
Load config from {project-root}/_bmad/config.yaml and config.user.yaml if available.
If config is missing:
  - Continue with fallback values — no mention of a setup skill
```

Store config values in memory as `{var_name}` for use in prompts.

### Required Core Variables

Load core config variables (user preferences, language, output locations) with sensible defaults. If the workflow creates documents, include document output language.

**Example for BMB workflow (creates documents, has output var):**
```
vars: user_name:BMad,communication_language:English,document_output_language:English,output_folder:{project-root}/_bmad-output,bmad_builder_output_folder:{project-root}/bmad-builder-creations/
```

**Example for analysis workflow (no documents, has output var):**
```
vars: user_name:BMad,communication_language:English,output_folder:{project-root}/_bmad-output,analysis_output_folder:{project-root}/_bmad-output/analysis/
```

**Example for processing workflow (no documents, no output var):**
```
vars: user_name:BMad,communication_language:English,output_folder:{project-root}/_bmad-output
```

### Using Config Values in Prompts

Each prompt file should establish communication language and relevant output settings at the top.

**Use throughout prompts:**
```markdown
"Creating documentation in {document_output_language}..."  ← ONLY if creates documents
"Writing output to {bmad_builder_output_folder}/report.md" ← ONLY if has output var
"Connecting to API at {my_module_api_url}..."
```

---

## {project_root} Pattern for Portable Paths

Artifacts MUST use `{project_root}` for paths so the skill works regardless of install location (user directory or project).

### Path Pattern

```
{project_root}/docs/foo.md         → Correct (portable)
./docs/foo.md                      → Wrong (breaks if skill in user dir)
~/my-project/docs/foo.md           → Wrong (not portable)
/bizarre/absolute/path/foo.md      → Wrong (not portable)
```

### Writing Artifacts

```markdown
1. Create the artifact at {project_root}/docs/architecture.md
2. Update {project_root}/CHANGELOG.md with entry
3. Copy template to {project_root}/.bmad-cache/template.md
```

### {project_root} Resolution

`{project_root}` is automatically resolved to the directory where the workflow was launched. This ensures:
- Skills work whether installed globally or per-project
- Multiple projects can use the same skill without conflict
- Artifact paths are always relative to the active project

---

## Long-Running Workflows: Compaction Survival

Workflows that run long (many steps, large context) may trigger context compaction. Critical state MUST be preserved in output files.

### The Document-Itself Pattern

**The output document is the cache.** Write directly to the file you're creating, updating it progressively as the workflow advances.

The document stores both content and context:
- **YAML front matter** — paths to input files used (for recovery after compaction)
- **Draft sections** — progressive content as it's built
- **Status marker** — which stage is complete (for resumption)

This avoids:
- File collisions when working on multiple PRDs/research projects simultaneously
- Extra `_bmad-cache` folder overhead
- State synchronization complexity

### Draft Document Structure

```markdown
---
title: "Analysis: Research Topic"
status: "analysis"  # discovery | planning | analysis | synthesis | polish
inputs:
  - "{project_root}/docs/brief.md"
  - "{project_root}/data/sources.json"
created: "2025-03-02T10:00:00Z"
updated: "2025-03-02T11:30:00Z"
---

# Analysis: Research Topic

## Discovery
[content from stage 1...]

## Analysis
[content from stage 2...]

---

*Last updated: Stage 2 complete*
```

### Input Tracking Pattern

**Stage 1: Initialize document with inputs**
```markdown
## Stage 1: Discovery
1. Gather sources and identify input files
2. Create output document with YAML front matter:
```yaml
---
title: "{document_title}"
status: "discovery"
inputs:
  - "{relative_path_to_input_1}"
  - "{relative_path_to_input_2}"
created: "{timestamp}"
updated: "{timestamp}"
---
```
3. Write discovery content to document
4. Present summary to user
```

**Stage 2+: Reload context if compacted**

Each stage after the first should begin by reading the output document to recover context. If compacted, re-read input files listed in the YAML front matter.

```markdown
## Stage 1: Research
1. Gather sources
2. **Write findings to {project_root}/docs/research-topic.md**
3. Present summary to user

## Stage 2: Analysis
1. **Read {project_root}/docs/research-topic.md** (survives compaction)
2. Analyze patterns
3. **Append/insert analysis into the same file**

## Stage 3: Synthesis
1. Read the growing document
2. Synthesize into final structure
3. **Update the same file in place**

## Stage 4: Final Polish
1. Spawn a subagent to polish the completed document:
   - Cohesion check
   - Redundancy removal
   - Contradiction detection and fixes
   - Add TOC if long document
2. Write final version to {project_root}/docs/research-topic.md
```

### When to Use This Pattern

**Guided flows with long documents:** Always write updates to the document itself at each stage.

**Yolo flows with multiple turns:** If the workflow takes multiple conversational turns, write to the output file progressively.

**Single-pass yolo:** Can wait to write final output if the entire response fits in one turn.

### Progressive Document Structure

Each stage appends to or restructures the document:

```markdown
## Initial Stage
# Document Title

## Section 1: Initial Research
[content...]

---

## Second Stage (reads file, appends)
# Document Title

## Section 1: Initial Research
[existing content...]

## Section 2: Analysis
[new content...]

---

## Third Stage (reads file, restructures)
# Document Title

## Executive Summary
[ synthesized from sections ]

## Background
[ section 1 content ]

## Analysis
[ section 2 content ]
```

### Final Polish Subagent

At workflow completion, spawn a subagent for final quality pass:

```markdown
## Final Polish

Launch a general-purpose agent with:
```
Task: Polish {output_file_path}

Actions:
1. Check cohesion - do sections flow logically?
2. Find and remove redundancy
3. Detect contradictions and fix them
4. If document is >5 sections, add a TOC at the top
5. Ensure consistent formatting and tone

Write the polished version back to the same file.
```

### Compaction Recovery Pattern

Each stage after the first should begin by reading the output document to recover context. If compacted, re-read input files listed in the YAML front matter.

### When NOT to Use This Pattern

- **Short, single-turn outputs:** Just write once at the end
- **Purely conversational workflows:** No persistent document needed
- **Multiple independent artifacts:** Each gets its own file; write each directly

---

## Sequential Progressive Disclosure

Place numbered prompt files at the skill root when:
- Multi-phase workflow with ordered questions
- Input of one phase affects the next
- User requires specific sequence
- Workflow is long-running and stages shouldn't be visible upfront

### Prompt File Structure

```
my-workflow/
├── SKILL.md
├── 01-discovery.md           # Stage 1: Gather requirements, start output doc
├── 02-planning.md            # Stage 2: Create plan (uses discovery output)
├── 03-execution.md           # Stage 3: Execute (uses plan, updates output)
├── 04-review.md              # Stage 4: Review and polish final output
└── references/
    └── stage-templates.md
```

### Progression Conditions

Each prompt file specifies when to proceed:

```markdown
# 02-planning.md

## Prerequisites
- Discovery complete (output doc exists and has discovery section)
- User approved scope (user confirmed: proceed)

## On Activation
1. Read the output doc to get discovery context
2. Generate plan based on discovered requirements
3. **Append/insert plan section into the output doc**
4. Present plan summary to user

## Progression Condition
Proceed to execution stage when user confirms: "Proceed with plan" OR user provides modifications

## On User Approval
Route to 03-execution.md
```

### SKILL.md Routes to Prompt Files

Main SKILL.md is minimal — just routing logic:

```markdown
## Workflow Entry

1. Load config from {project-root}/_bmad/bmb/config.yaml

2. Check if workflow in progress:
   - If output doc exists (user specifies path or we prompt):
     - Read doc to determine current stage
     - Resume from last completed section
   - Else: Start at 01-discovery.md

3. Route to appropriate prompt file based on stage
```

### When NOT to Use Separate Prompt Files

Keep inline in SKILL.md when:
- Simple skill (session-long context fits)
- Well-known domain tool usage
- Single-purpose utility
- All stages are independent or can be visible upfront

---

## Module Metadata Reference

BMad module workflows require extended frontmatter metadata. See `references/metadata-reference.md` for the metadata template, field explanations, and comparisons between standalone skills and module workflows.

---

## Workflow Architecture Checklist

Before finalizing a BMad module workflow, verify:

- [ ] **Facilitator persona**: Does the workflow treat the operator as expert?
- [ ] **Config integration**: Are language, output locations, and module props read and used?
- [ ] **Portable paths**: All artifact paths use `{project_root}`?
- [ ] **Continuous output**: Does each stage write to the output document directly (survives compaction)?
- [ ] **Document-as-cache**: Output doc has YAML front matter with `status` and `inputs` for recovery?
- [ ] **Input tracking**: Does front matter list relative paths to all input files used?
- [ ] **Final polish**: Does workflow include a subagent polish step at the end?
- [ ] **Progressive disclosure**: Are stages in `./references/` with clear progression conditions?
- [ ] **Metadata complete**: All bmad-* fields present and accurate?
- [ ] **Recovery pattern**: Can the workflow resume by reading the output doc front matter?

---

## Example: Complete BMad Workflow Skeleton

```
my-module-workflow/
├── SKILL.md                              # Routing + entry logic
├── 01-discovery.md                       # Gather requirements
├── 02-planning.md                        # Create plan
├── 03-execution.md                       # Execute
├── 04-review.md                          # Review results
├── references/
│   └── templates.md                      # Stage templates
└── scripts/
    └── validator.sh                      # Output validation
```

**SKILL.md** (minimal routing):
```yaml
---
name: bmad-mymodule-workflow
description: Complex multi-stage workflow for my module. Use when user requests to 'run my module workflow' or 'create analysis report'.
---

## Workflow Entry

1. Load config from `{project-root}/_bmad/config.yaml` (`mymod` section) and `config.user.yaml`. If config is missing, inform that `bmad-mymodule-setup` is available for initial setup, then continue with fallbacks:
   - `user_name` — fallback: omit
   - `communication_language` — fallback: match the user's language
   - `document_output_language` — fallback: match the user's language
   - `my_output_folder` — fallback: `{project-root}/_bmad-output/mymodule`

2. Ask user for output document path (or suggest {my_output_folder}/analysis-{timestamp}.md)

3. Check if doc exists:
   - If yes: read to determine current stage, resume
   - If no: start at 01-discovery.md

4. Route to appropriate prompt file based on stage
```

**01-discovery.md**:
```markdown
Language: {communication_language}
Output Language: {document_output_language}
Output Location: {my_output_folder}

## Discovery

1. What are we building?
2. What are the constraints?
3. What input files should we reference?

**Create**: {output_doc_path} with:
```markdown
---
title: "Analysis: {topic}"
status: "discovery"
inputs:
  - "{relative_path_to_input_1}"
  - "{relative_path_to_input_2}"
created: "{timestamp}"
updated: "{timestamp}"
---

# Analysis: {topic}

## Discovery
[findings...]

---

*Status: Stage 1 complete*
```

## Progression
When complete → 02-planning.md
```

**02-planning.md**:
```markdown
Language: {communication_language}
Output Language: {document_output_language}

## Planning Start

1. Read {output_doc_path}
2. Parse YAML front matter — reload all `inputs` to restore context
3. Verify status is "discovery"

## Planning
1. Generate plan based on discovery
2. Update {output_doc_path}:
   - Update status to "planning"
   - Append planning section

## Progression
When complete → 03-execution.md
```

**04-review.md**:
```markdown
Language: {communication_language}
Output Language: {document_output_language}

## Final Polish

1. Read the complete output doc
2. Launch a general-purpose agent:
```
Task: Polish {output_doc_path}

Actions:
1. Check cohesion - do sections flow logically?
2. Find and remove redundancy
3. Detect contradictions and fix them
4. If document is >5 sections, add a TOC at the top
5. Ensure consistent formatting and tone
6. Update YAML status to "complete" and remove draft markers

Write the polished version back to the same file.
```

## Progression
When complete → present final result to user
```
