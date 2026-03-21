# Universal Scanner Output Schema

All quality scanners — both LLM-based and deterministic lint scripts — MUST produce output conforming to this schema. No exceptions.

## Top-Level Structure

```json
{
  "scanner": "scanner-name",
  "skill_path": "{path}",
  "findings": [],
  "assessments": {},
  "summary": {
    "total_findings": 0,
    "by_severity": {},
    "assessment": "1-2 sentence overall assessment"
  }
}
```

| Key | Type | Required | Description |
|-----|------|----------|-------------|
| `scanner` | string | yes | Scanner identifier (e.g., `"workflow-integrity"`, `"prompt-craft"`) |
| `skill_path` | string | yes | Absolute path to the skill being scanned |
| `findings` | array | yes | ALL items — issues, strengths, suggestions, opportunities. Always an array, never an object |
| `assessments` | object | yes | Scanner-specific structured analysis (cohesion tables, health metrics, user journeys, etc.). Free-form per scanner |
| `summary` | object | yes | Aggregate counts and brief overall assessment |

## Finding Schema (7 fields)

Every item in `findings[]` has exactly these 7 fields:

```json
{
  "file": "SKILL.md",
  "line": 42,
  "severity": "high",
  "category": "frontmatter",
  "title": "Brief headline of the finding",
  "detail": "Full context — rationale, what was observed, why it matters",
  "action": "What to do about it — fix, suggestion, or script to create"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `file` | string | yes | Relative path to the affected file (e.g., `"SKILL.md"`, `"scripts/build.py"`). Empty string if not file-specific |
| `line` | int\|null | no | Line number (1-based). `null` or `0` if not line-specific |
| `severity` | string | yes | One of the severity values below |
| `category` | string | yes | Scanner-specific category (e.g., `"frontmatter"`, `"token-waste"`, `"lint"`) |
| `title` | string | yes | Brief headline (1 sentence). This is the primary display text |
| `detail` | string | yes | Full context — fold rationale, observation, impact, nuance into one narrative. Empty string if title is self-explanatory |
| `action` | string | yes | What to do — fix instruction, suggestion, or script to create. Empty string for strengths/notes |

## Severity Values (complete enum)

```
critical | high | medium | low | high-opportunity | medium-opportunity | low-opportunity | suggestion | strength | note
```

**Routing rules:**
- `critical`, `high` → "Truly Broken" section in report
- `medium`, `low` → category-specific findings sections
- `high-opportunity`, `medium-opportunity`, `low-opportunity` → enhancement/creative sections
- `suggestion` → creative suggestions section
- `strength` → strengths section (positive observations worth preserving)
- `note` → informational observations, also routed to strengths

## Assessment Sub-Structure Contracts

The `assessments` object is free-form per scanner, but the HTML report renderer expects specific shapes for specific keys. These are the canonical formats.

### user_journeys (enhancement-opportunities scanner)

**Always an array of objects. Never an object keyed by persona.**

```json
"user_journeys": [
  {
    "archetype": "first-timer",
    "summary": "Brief narrative of this user's experience",
    "friction_points": ["moment 1", "moment 2"],
    "bright_spots": ["what works well"]
  }
]
```

### autonomous_assessment (enhancement-opportunities scanner)

```json
"autonomous_assessment": {
  "potential": "headless-ready|easily-adaptable|partially-adaptable|fundamentally-interactive",
  "hitl_points": 3,
  "auto_resolvable": 2,
  "needs_input": 1,
  "notes": "Brief assessment"
}
```

### top_insights (enhancement-opportunities scanner)

**Always an array of objects with title/detail/action (same shape as findings but without file/line/severity/category).**

```json
"top_insights": [
  {
    "title": "The key observation",
    "detail": "Why it matters",
    "action": "What to do about it"
  }
]
```

### cohesion_analysis (skill-cohesion / agent-cohesion scanner)

```json
"cohesion_analysis": {
  "dimension_name": { "score": "strong|moderate|weak", "notes": "explanation" }
}
```

Dimension names are scanner-specific (e.g., `stage_flow_coherence`, `persona_alignment`). The report renderer iterates all keys and renders a table row per dimension.

### skill_identity / agent_identity (cohesion scanners)

```json
"skill_identity": {
  "name": "skill-name",
  "purpose_summary": "Brief characterization",
  "primary_outcome": "What this skill produces"
}
```

### skillmd_assessment (prompt-craft scanner)

```json
"skillmd_assessment": {
  "overview_quality": "appropriate|excessive|missing",
  "progressive_disclosure": "good|needs-extraction|monolithic",
  "notes": "brief assessment"
}
```

Agent variant adds `"persona_context": "appropriate|excessive|missing"`.

### prompt_health (prompt-craft scanner)

```json
"prompt_health": {
  "total_prompts": 3,
  "with_config_header": 2,
  "with_progression": 1,
  "self_contained": 3
}
```

### skill_understanding (enhancement-opportunities scanner)

```json
"skill_understanding": {
  "purpose": "what this skill does",
  "primary_user": "who it's for",
  "assumptions": ["assumption 1", "assumption 2"]
}
```

### stage_summary (workflow-integrity scanner)

```json
"stage_summary": {
  "total_stages": 0,
  "missing_stages": [],
  "orphaned_stages": [],
  "stages_without_progression": [],
  "stages_without_config_header": []
}
```

### metadata (structure scanner)

Free-form key-value pairs. Rendered as a metadata block.

### script_summary (scripts lint)

```json
"script_summary": {
  "total_scripts": 5,
  "by_type": {"python": 3, "shell": 2},
  "missing_tests": ["script1.py"]
}
```

### existing_scripts (script-opportunities scanner)

Array of strings (script paths that already exist).

## Complete Example

```json
{
  "scanner": "workflow-integrity",
  "skill_path": "/path/to/skill",
  "findings": [
    {
      "file": "SKILL.md",
      "line": 12,
      "severity": "high",
      "category": "frontmatter",
      "title": "Missing 'description' field in frontmatter",
      "detail": "The SKILL.md frontmatter is missing the description field. Without a description, the skill cannot be triggered reliably by the help system.",
      "action": "Add a description with trigger phrases to the YAML frontmatter block"
    },
    {
      "file": "build-process.md",
      "line": null,
      "severity": "strength",
      "category": "design",
      "title": "Excellent progressive disclosure pattern in build stages",
      "detail": "Each stage provides exactly the context needed without front-loading information. This reduces token waste and improves LLM comprehension.",
      "action": ""
    },
    {
      "file": "SKILL.md",
      "line": 45,
      "severity": "medium-opportunity",
      "category": "experience-gap",
      "title": "No guidance for first-time users unfamiliar with build workflows",
      "detail": "A user encountering this skill for the first time has no onboarding path. The skill assumes familiarity with stage-based workflows, which creates friction for newcomers.",
      "action": "Add a 'Getting Started' section or link to onboarding documentation"
    }
  ],
  "assessments": {
    "stage_summary": {
      "total_stages": 7,
      "missing_stages": [],
      "orphaned_stages": ["cleanup"]
    }
  },
  "summary": {
    "total_findings": 3,
    "by_severity": {"high": 1, "medium-opportunity": 1, "strength": 1},
    "assessment": "Well-structured skill with one critical frontmatter gap. Progressive disclosure is a notable strength."
  }
}
```

## DO NOT

- **DO NOT** rename fields. Use exactly: `file`, `line`, `severity`, `category`, `title`, `detail`, `action`
- **DO NOT** use `issues` instead of `findings` — the array is always called `findings`
- **DO NOT** add fields to findings beyond the 7 defined above. Put scanner-specific structured data in `assessments`
- **DO NOT** use separate arrays for strengths, suggestions, or opportunities — they go in `findings` with appropriate severity values
- **DO NOT** change `user_journeys` from an array to an object keyed by persona name
- **DO NOT** restructure assessment sub-objects — use the shapes defined above
- **DO NOT** put free-form narrative data into `assessments` — that belongs in `detail` fields of findings or in `summary.assessment`

## Self-Check Before Output

Before writing your JSON output, verify:

1. Is your array called `findings` (not `issues`, not `opportunities`)?
2. Does every item in `findings` have all 7 fields: `file`, `line`, `severity`, `category`, `title`, `detail`, `action`?
3. Are strengths in `findings` with `severity: "strength"` (not in a separate `strengths` array)?
4. Are suggestions in `findings` with `severity: "suggestion"` (not in a separate `creative_suggestions` array)?
5. Is `assessments` an object containing structured analysis data (not items that belong in findings)?
6. Is `user_journeys` an array of objects (not an object keyed by persona)?
7. Do `top_insights` items use `title`/`detail`/`action` (not `insight`/`suggestion`/`why_it_matters`)?
