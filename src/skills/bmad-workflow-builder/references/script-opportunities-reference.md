# Script Opportunities Reference — Workflow Builder

## Core Principle

Scripts handle deterministic operations (validate, transform, count). Prompts handle judgment (interpret, classify, decide). If a check has clear pass/fail criteria, it belongs in a script.

---

## Section 1: How to Spot Script Opportunities

### The Determinism Test

Ask two questions about any operation:

1. **Given identical input, will it always produce identical output?** If yes, it's a script candidate.
2. **Could you write a unit test with expected output?** If yes, it's definitely a script.

**Script territory:** The operation has no ambiguity — same input, same result, every time.
**Prompt territory:** The operation requires interpreting meaning, tone, or context — reasonable people could disagree on the output.

### The Judgment Boundary

| Scripts Handle | Prompts Handle |
|----------------|----------------|
| Fetch | Interpret |
| Transform | Classify (with ambiguity) |
| Validate | Create |
| Count | Decide (with incomplete info) |
| Parse | Evaluate quality |
| Compare | Synthesize meaning |
| Extract | Assess tone/style |
| Format | Generate recommendations |
| Check structure | Weigh tradeoffs |

### Pattern Recognition Checklist

When you see these verbs or patterns in a workflow's requirements, think scripts first:

| Signal Verb / Pattern | Script Type | Example |
|----------------------|-------------|---------|
| validate | Validation script | "Validate frontmatter fields exist" |
| count | Metric script | "Count tokens per file" |
| extract | Data extraction | "Extract all config variable references" |
| convert / transform | Transformation script | "Convert stage definitions to graph" |
| compare | Comparison script | "Compare prompt frontmatter vs SKILL.md references" |
| scan for | Pattern scanning | "Scan for orphaned template artifacts" |
| check structure | File structure checker | "Check skill directory has required files" |
| against schema | Schema validation | "Validate output against JSON schema" |
| graph / map dependencies | Dependency analysis | "Map skill-to-skill dependencies" |
| list all | Enumeration script | "List all resource files loaded by prompts" |
| detect pattern | Pattern detector | "Detect subagent delegation patterns" |
| diff / changes between | Diff analysis | "Show what changed between versions" |

### The Outside-the-Box Test

Scripts are not limited to validation. Push your thinking:

- **Data gathering as script:** Could a script collect structured data (file sizes, dependency lists, config values) and return JSON for the LLM to interpret? The LLM gets pre-digested facts instead of reading raw files.
- **Pre-processing:** Could a script reduce what the LLM needs to read? Extract only the relevant sections, strip boilerplate, summarize structure.
- **Post-processing validation:** Could a script validate LLM output after generation? Check that generated YAML parses, that referenced files exist, that naming conventions are followed.
- **Metric collection:** Could scripts count, measure, and tabulate so the LLM makes decisions based on numbers it didn't have to compute? Token counts, file counts, complexity scores — feed these to LLM judgment without making the LLM count.
- **Workflow stage analysis:** Could a script parse stage definitions and progression conditions, giving the LLM a structural map without it needing to parse markdown?

### Your Toolbox

Scripts have access to the full capabilities of the execution environment. Think broadly — if you can express the logic as deterministic code, it's a script candidate.

**Bash:** Full shell power — `jq`, `grep`, `awk`, `sed`, `find`, `diff`, `wc`, `sort`, `uniq`, `curl`, plus piping and composition. Great for file discovery, text processing, and orchestrating other scripts.

**Python:** The entire standard library — `json`, `yaml`, `pathlib`, `re`, `argparse`, `collections`, `difflib`, `ast`, `csv`, `xml.etree`, `textwrap`, `dataclasses`, and more. Plus PEP 723 inline-declared dependencies for anything else: `tiktoken` for accurate token counting, `jsonschema` for schema validation, `pyyaml` for YAML parsing, etc.

**System tools:** `git` commands for history, diff, blame, and log analysis. Filesystem operations for directory scanning and structure validation. Process execution for orchestrating multi-script pipelines.

### The --help Pattern

All scripts use PEP 723 metadata and implement `--help`. This creates a powerful integration pattern for prompts:

Instead of inlining a script's interface details into a prompt, the prompt can simply say:

> Run `scripts/foo.py --help` to understand its inputs and outputs, then invoke appropriately.

This saves tokens in the prompt and keeps a single source of truth for the script's API. When a script's interface changes, the prompt doesn't need updating — `--help` always reflects the current contract.

---

## Section 2: Script Opportunity Catalog

Each entry follows the format: What it does, Why it matters for workflows, What it checks, What it outputs, and Implementation notes.

---

### 1. Frontmatter Validator

**What:** Validate SKILL.md frontmatter structure and content.

**Why:** Frontmatter drives skill triggering and routing. Malformed frontmatter means the skill never activates or activates incorrectly.

**Checks:**
- `name` exists and is kebab-case
- `description` exists and follows "Use when..." pattern
- No forbidden fields or reserved prefixes
- Optional fields have valid values if present

**Output:** JSON with pass/fail per field, line numbers for errors.

**Implementation:** Python with argparse, no external deps needed. Parse YAML frontmatter between `---` delimiters.

---

### 2. Template Artifact Scanner

**What:** Scan all skill files for orphaned template substitution artifacts.

**Why:** The build process may leave behind `{if-autonomous}`, `{displayName}`, `{skill-name}`, or other placeholders that should have been replaced. These cause runtime confusion.

**Checks:**
- Scan all `.md` files for `{placeholder}` patterns
- Distinguish real config variables (loaded at runtime) from build-time artifacts
- Flag any that don't match known runtime variables

**Output:** JSON with file path, line number, artifact text, and whether it looks intentional.

**Implementation:** Bash script with `grep` and `jq` for JSON output, or Python with regex.

---

### 3. Prompt Frontmatter Comparator

**What:** Compare prompt file frontmatter against SKILL.md stage references.

**Why:** Misalignment between prompts and SKILL.md causes routing failures — the skill references a stage it can't deliver, or has a prompt that's never reachable.

**Checks:**
- Every prompt file at root has frontmatter with `name`, `description`, `menu-code`
- Every stage referenced in SKILL.md has a corresponding prompt file
- Flag orphaned prompts not referenced in SKILL.md

**Output:** JSON with mismatches, missing files, orphaned prompts.

**Implementation:** Python, reads SKILL.md and all prompt `.md` files at skill root.

---

### 4. Token Counter

**What:** Count approximate token counts for each file in a skill.

**Why:** Identify verbose files that need optimization. Catch skills that exceed context window budgets. Understand where token budget is spent across prompts, resources, and the SKILL.md.

**Checks:**
- Total tokens per `.md` file (approximate: chars / 4, or accurate via tiktoken)
- Code block tokens vs prose tokens
- Cumulative token cost of full skill activation (SKILL.md + loaded resources + initial prompt)

**Output:** JSON with file path, token count, percentage of total, and a sorted ranking.

**Implementation:** Python. Use `tiktoken` (PEP 723 dependency) for accuracy, or fall back to character approximation.

---

### 5. Dependency Graph Generator

**What:** Map dependencies between the current skill and external skills it invokes.

**Why:** Understand the skill's dependency surface. Catch references to skills that don't exist or have been renamed.

**Checks:**
- Parse SKILL.md and prompts for skill invocation patterns (`invoke`, `load`, skill name references)
- Build a dependency list with direction (this skill depends on X, Y depends on this skill)

**Output:** JSON adjacency list or DOT format (GraphViz). Include whether each dependency is required or optional.

**Implementation:** Python with regex for invocation pattern detection.

---

### 6. Stage Flow Analyzer

**What:** Parse multi-stage workflow definitions to extract stage ordering, progression conditions, and routing logic.

**Why:** Complex workflows define stages with specific progression conditions. Misaligned stage ordering, missing progression gates, or unreachable stages cause workflow failures that are hard to debug at runtime.

**Checks:**
- Extract all defined stages from SKILL.md and prompt files
- Verify each stage has a clear entry condition and exit/progression condition
- Detect unreachable stages (no path leads to them)
- Detect dead-end stages (no progression and not marked as terminal)
- Validate stage ordering matches the documented flow
- Check for circular stage references

**Output:** JSON with stage list, progression map, and structural warnings.

**Implementation:** Python with regex for stage/condition extraction from markdown.

---

### 7. Config Variable Tracker

**What:** Find all `{var}` references across skill files and verify they are loaded or defined.

**Why:** Unresolved config variables cause runtime errors or produce literal `{var_name}` text in outputs. This is especially common after refactoring or renaming variables.

**Checks:**
- Scan all `.md` files for `{variable_name}` patterns
- Cross-reference against variables defined in `{project-root}/_bmad/config.yaml`
- Distinguish template variables from literal text in code blocks
- Flag undefined variables and unused loaded variables

**Output:** JSON with variable name, locations where used, and whether it's defined/loaded.

**Implementation:** Python with regex scanning and config file parsing.

---

### 8. Resource Loading Analyzer

**What:** Map which resources are loaded at which point during skill execution.

**Why:** Resources loaded too early waste context. Resources never loaded are dead weight in the skill directory. Understanding the loading sequence helps optimize token budget.

**Checks:**
- Parse SKILL.md and prompts for `Load resource` / `Read` / file reference patterns
- Map each resource to the stage/prompt where it's first loaded
- Identify resources in `references/` that are never referenced
- Identify resources referenced but missing from `references/`
- Calculate cumulative token cost at each loading point

**Output:** JSON with resource file, loading trigger (which prompt/stage), and orphan/missing flags.

**Implementation:** Python with regex for load-pattern detection and directory scanning.

---

### 9. Subagent Pattern Detector

**What:** Detect whether a skill that processes multiple sources uses the BMad Advanced Context Pattern (subagent delegation).

**Why:** Skills processing 5+ sources without subagent delegation risk context overflow and degraded output quality. This pattern is required for high-source-count workflows.

**Checks:**
- Count distinct source/input references in the skill
- Look for subagent delegation patterns: "DO NOT read sources yourself", "delegate to sub-agents", `/tmp/analysis-` temp file patterns
- Check for sub-agent output templates (50-100 token summaries)
- Flag skills with 5+ sources that lack the pattern

**Output:** JSON with source count, pattern found/missing, and recommendations.

**Implementation:** Python with keyword search and context extraction.

---

### 10. Prompt Chain Validator

**What:** Trace the chain of prompt loads through a workflow and verify every path is valid.

**Why:** Workflows route between prompts based on user intent and stage progression. A broken link in the chain — a `Load foo.md` where `foo.md` doesn't exist — halts the workflow.

**Checks:**
- Extract all `Load *.md` prompt references from SKILL.md and every prompt file
- Verify each referenced prompt file exists
- Build a reachability map from SKILL.md entry points
- Flag prompts that exist but are unreachable from any entry point

**Output:** JSON with prompt chain map, broken links, and unreachable prompts.

**Implementation:** Python with regex extraction and file existence checks.

---

### 11. Skill Health Check (Composite)

**What:** Run all available validation scripts and aggregate results into a single report.

**Why:** One command to assess overall skill quality. Useful as a build gate or pre-commit check.

**Composition:** Runs scripts 1-10 in sequence, collects JSON outputs, aggregates findings by severity.

**Output:** Unified JSON health report with per-script results and overall status.

**Implementation:** Bash script orchestrating Python scripts, `jq` for JSON aggregation. Or a Python orchestrator using `subprocess`.

---

### 12. Skill Comparison Validator

**What:** Compare two versions of a skill (or two skills) for structural differences.

**Why:** Validate that changes during iteration didn't break structure. Useful for reviewing edits, comparing before/after optimization, or diffing a skill against a template.

**Checks:**
- Frontmatter changes
- New or removed prompt files
- Token count changes per file
- Stage flow changes (for workflows)
- Resource additions/removals

**Output:** JSON with categorized changes and severity assessment.

**Implementation:** Bash with `git diff` or file comparison, Python for structural analysis.

---

## Section 3: Script Output Standard and Implementation Checklist

### Script Output Standard

All scripts MUST output structured JSON for agent consumption:

```json
{
  "script": "script-name",
  "version": "1.0.0",
  "skill_path": "/path/to/skill",
  "timestamp": "2025-03-08T10:30:00Z",
  "status": "pass|fail|warning",
  "findings": [
    {
      "severity": "critical|high|medium|low|info",
      "category": "structure|security|performance|consistency",
      "location": {"file": "SKILL.md", "line": 42},
      "issue": "Clear description",
      "fix": "Specific action to resolve"
    }
  ],
  "summary": {
    "total": 0,
    "critical": 0,
    "high": 0,
    "medium": 0,
    "low": 0
  }
}
```

### Implementation Checklist

When creating new validation scripts:

- [ ] Uses `--help` for documentation (PEP 723 metadata)
- [ ] Accepts skill path as argument
- [ ] `-o` flag for output file (defaults to stdout)
- [ ] Writes diagnostics to stderr
- [ ] Returns meaningful exit codes: 0=pass, 1=fail, 2=error
- [ ] Includes `--verbose` flag for debugging
- [ ] Self-contained (PEP 723 for Python dependencies)
- [ ] No interactive prompts
- [ ] No network dependencies
- [ ] Outputs valid JSON to stdout
- [ ] Has tests in `scripts/tests/` subfolder
