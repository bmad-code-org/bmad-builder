# Skill Authoring Best Practices

Practical patterns for writing effective BMad agent skills. For field definitions and description format, see `references/standard-fields.md`. For quality dimensions, see `references/quality-dimensions.md`.

## Core Principle: Informed Autonomy

Give the executing agent enough context to make good judgment calls — not just enough to follow steps. The right test for every piece of content is: "Would the agent make *better decisions* with this context?" If yes, keep it. If it's genuinely redundant or mechanical, cut it.

## Freedom Levels

Match specificity to task fragility:

| Freedom | When to Use | Example |
|---------|-------------|---------|
| **High** (text instructions) | Multiple valid approaches, context-dependent | "Analyze the user's vision and suggest capabilities" |
| **Medium** (pseudocode/templates) | Preferred pattern exists, some variation OK | `def generate_config(capabilities, format="json"):` |
| **Low** (exact scripts) | Fragile operations, consistency critical | `python3 scripts/scan-path-standards.py path/to/skill` (do not modify) |

**Analogy**: Narrow bridge with cliffs = low freedom. Open field = high freedom.

## Common Patterns

### Template Pattern

**Strict** (must follow exactly):
````markdown
## Report structure
ALWAYS use this template:
```markdown
# [Title]
## Summary
[One paragraph]
## Findings
- Finding 1 with data
```
````

**Flexible** (adapt as needed):
````markdown
Here's a sensible default, use judgment:
```markdown
# [Title]
## Summary
[Overview]
```
Adapt based on context.
````

### Examples Pattern

Input/output pairs show expected style:
````markdown
## Commit message format
**Example 1:**
Input: "Added user authentication with JWT tokens"
Output: `feat(auth): implement JWT-based authentication`
````

### Conditional Workflow

```markdown
1. Determine modification type:
   **Creating new?** → Creation workflow
   **Editing existing?** → Editing workflow
```

### Soft Gate Elicitation

For guided/interactive workflows, use "anything else?" soft gates at natural transition points instead of hard menus. This pattern draws out information users didn't know they had:

```markdown
## After completing a discovery section:
Present what you've captured so far, then:
"Anything else you'd like to add, or shall we move on?"
```

**Why it works:** Users almost always remember one more thing when given a graceful exit ramp rather than a hard stop. The low-pressure phrasing invites contribution without demanding it. This consistently produces richer, more complete artifacts than rigid section-by-section questioning.

**When to use:** Any guided workflow or agent with collaborative discovery — product briefs, requirements gathering, design reviews, brainstorming synthesis. Use at every natural transition between topics or sections.

**When NOT to use:** Autonomous/headless execution, or steps where additional input would cause scope creep rather than enrich the output.

### Intent-Before-Ingestion

Never scan artifacts, documents, or project context until you understand WHY the user is here. Scanning without purpose produces noise, not signal.

```markdown
## On activation:
1. Greet and understand intent — what is this about?
2. Accept whatever inputs the user offers
3. Ask if they have additional documents or context
4. ONLY THEN scan artifacts, scoped to relevance
```

**Why it works:** Without knowing what the user wants, you can't judge what's relevant in a 100-page research doc vs a brainstorming report. Intent gives you the filter. Without it, scanning is a fool's errand.

**When to use:** Any agent that ingests documents, project context, or external data as part of its process.

### Capture-Don't-Interrupt

When users provide information beyond the current scope (e.g., dropping requirements during a product brief, mentioning platforms during vision discovery), capture it silently for later use rather than redirecting or stopping them.

```markdown
## During discovery:
If user provides out-of-scope but valuable info:
- Capture it (notes, structured aside, addendum bucket)
- Don't interrupt their flow
- Use it later in the appropriate stage or output
```

**Why it works:** Users in creative flow will share their best insights unprompted. Interrupting to say "we'll cover that later" kills momentum and may lose the insight entirely. Capture everything, distill later.

**When to use:** Any collaborative discovery agent where the user is brainstorming, explaining, or brain-dumping.

### Dual-Output: Human Artifact + LLM Distillate

Any artifact-producing agent can output two complementary documents: a polished human-facing artifact AND a token-conscious, structured distillate optimized for downstream LLM consumption.

```markdown
## Output strategy:
1. Primary: Human-facing document (exec summary, report, brief)
2. Optional: LLM distillate — dense, structured, token-efficient
   - Captures overflow that doesn't belong in the human doc
   - Rejected ideas (so downstream doesn't re-propose them)
   - Detail bullets with just enough context to stand alone
   - Designed to be loaded as context for the next workflow
```

**Why it works:** Human docs are concise by design — they can't carry all the detail surfaced during discovery. But that detail has value for downstream LLM workflows (PRD creation, architecture design, etc.). The distillate bridges the gap without bloating the primary artifact.

**When to use:** Any agent producing documents that feed into subsequent LLM workflows. The distillate is always optional — offered to the user, not forced.

### Parallel Review Lenses

Before finalizing any artifact, fan out multiple reviewers with different perspectives to catch blind spots the builder/facilitator missed.

```markdown
## Near completion:
Fan out 2-3 review subagents in parallel:
- Skeptic: "What's missing? What assumptions are untested?"
- Opportunity Spotter: "What adjacent value? What angles?"
- Contextual Reviewer: LLM picks the best third lens
  (e.g., "regulatory risk" for healthtech, "DX critic" for devtools)

Graceful degradation: If subagents unavailable,
main agent does a single critical self-review pass.
```

**Why it works:** A single perspective — even an expert one — has blind spots. Multiple lenses surface issues and opportunities that no single reviewer would catch. The contextually-chosen third lens ensures domain-specific concerns aren't missed.

**When to use:** Any agent producing a significant artifact (briefs, PRDs, designs, architecture docs). The review step is lightweight but high-value.

### Three-Mode Architecture (Guided / Yolo / Autonomous)

For interactive agents, offer three execution modes that match different user contexts:

| Mode | Trigger | Behavior |
|------|---------|----------|
| **Guided** | Default | Section-by-section with soft gates. Drafts from what it knows, questions what it doesn't. |
| **Yolo** | `--yolo` or "just draft it" | Ingests everything, drafts complete artifact upfront, then walks user through refinement. |
| **Autonomous** | `--headless` / `-H` | Headless. Takes inputs, produces artifact, no interaction. |

**Why it works:** Not every user wants the same experience. A first-timer needs guided discovery. A repeat user with clear inputs wants yolo. A pipeline wants autonomous. Same agent, three entry points.

**When to use:** Any facilitative agent that produces an artifact. Not all agents need all three — but considering them during design prevents painting yourself into a single interaction model.

### Graceful Degradation

Every subagent-dependent feature should have a fallback path. If the platform doesn't support parallel subagents (or subagents at all), the workflow must still progress.

```markdown
## Subagent-dependent step:
Try: Fan out subagents in parallel
Fallback: Main agent performs the work sequentially
Never: Block the workflow because a subagent feature is unavailable
```

**Why it works:** Skills run across different platforms, models, and configurations. A skill that hard-fails without subagents is fragile. A skill that gracefully falls back to sequential processing is robust everywhere.

**When to use:** Any agent that uses subagents for research, review, or parallel processing.

### Verifiable Intermediate Outputs

For complex tasks: plan → validate → execute → verify

1. Analyze inputs
2. **Create** `changes.json` with planned updates
3. **Validate** with script before executing
4. Execute changes
5. Verify output

Benefits: catches errors early, machine-verifiable, reversible planning.

## Writing Guidelines

- **Consistent terminology** — choose one term per concept, stick to it
- **Third person** in descriptions — "Processes files" not "I help process files"
- **Descriptive file names** — `form_validation_rules.md` not `doc2.md`
- **Forward slashes** in all paths — cross-platform
- **One level deep** for reference files — SKILL.md → reference.md, never SKILL.md → A.md → B.md
- **TOC for long files** — add table of contents for files >100 lines

## Anti-Patterns

| Anti-Pattern | Fix |
|---|---|
| Too many options upfront | One default with escape hatch for edge cases |
| Deep reference nesting (A→B→C) | Keep references 1 level from SKILL.md |
| Inconsistent terminology | Choose one term per concept |
| Vague file names | Name by content, not sequence |
| Scripts that classify meaning via regex | Intelligence belongs in prompts, not scripts |

## Scripts in Skills

- **Execute vs reference** — "Run `analyze.py` to extract fields" (execute) vs "See `analyze.py` for the algorithm" (read)
- **Document constants** — explain why `TIMEOUT = 30`, not just what
- **PEP 723 for Python** — self-contained scripts with inline dependency declarations
- **MCP tools** — use fully qualified names: `ServerName:tool_name`
