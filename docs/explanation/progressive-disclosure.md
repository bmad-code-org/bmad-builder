---
title: 'Progressive Disclosure in Skills'
description: How to structure skills so they load only the context needed at each moment — from frontmatter through dynamic routing to step files
---

Progressive disclosure is the technique that separates basic skills from powerful ones. The core idea: never load more context than the agent needs _right now_. This keeps token usage low, prevents context pollution, and makes skills survive long conversations.

## The Four Layers

Skills can use any combination of these layers. Most production skills use Layers 1-3. Layer 4 is reserved for strict sequential processes.

| Layer                      | What It Does                                                              | Token Cost                         |
| -------------------------- | ------------------------------------------------------------------------- | ---------------------------------- |
| **1. Frontmatter vs Body** | Frontmatter is always in context; body loads only when triggered          | ~100 tokens always, body on demand |
| **2. On-Demand Resources** | SKILL.md points to resources and scripts loaded only when relevant        | Zero until needed                  |
| **3. Dynamic Routing**     | SKILL.md acts as a router, dispatching to entirely different prompt flows | Only the chosen path loads         |
| **4. Step Files**          | Agent reads one step at a time, never sees ahead                          | One step's worth at a time         |

## Layer 1: Frontmatter vs Body

Frontmatter (name + description) is **always in context** — it is how the LLM decides whether to load the skill. The body only loads when the skill triggers.

This means frontmatter must be precise and include trigger phrases. The body stays under 500 lines and pushes detail into Layers 2-3.

```markdown
---
name: bmad-my-skill
description: Validates API contracts against OpenAPI specs. Use when user says 'validate API' or 'check contract'.
---

# Body loads only when triggered

...
```

## Layer 2: On-Demand Resources

SKILL.md points to resources loaded only when relevant. This includes both **reference files** (context for the LLM) and **scripts** (offload work from the LLM entirely).

```markdown
## Which Guide to Read

- Python project → Read `resources/python.md`
- TypeScript project → Read `resources/typescript.md`
- Need validation → Run `scripts/validate.py` (don't read the script, just run it)
```

Scripts are particularly powerful here: the LLM does not process the logic, it just calls the script and receives structured output. This offloads deterministic work and saves tokens.

## Layer 3: Dynamic Routing

The skill body acts as a **router** that dispatches to entirely different prompt flows, scripts, or external skills based on what the user is asking for.

```markdown
## What Are You Trying To Do?

### "Build a new workflow"

→ Read `prompts/create-flow.md` and follow its instructions

### "Review an existing workflow"

→ Read `prompts/review-flow.md` and follow its instructions

### "Run analysis"

→ Run `scripts/analyze.py --target <path>` and present results
```

The key difference from Layer 2: Layer 2 loads supplementary resources alongside the skill body. Layer 3 **branches the entire execution path** — different prompts, different scripts, different skills. The skill body becomes a dispatcher, not an instruction set.

## Layer 4: Step Files

The most restrictive pattern. The agent reads **one step file at a time**, does not know what is next, and waits for user confirmation before proceeding.

```
prompts/
├── step-01.md  ← agent reads ONLY current step
├── step-02.md  ← loaded after user confirms step 1
├── step-03a.md ← branching path A
└── step-03b.md ← branching path B
```

**When to use:** Only when you need exact sequential progression with no skipping, compaction-resistance (each step is self-contained), or the agent deliberately constrained from looking ahead.

**Trade-off:** Very rigid. Limits the agent's ability to adapt, combine steps, or be creative. Do not use for exploratory or creative tasks. Do not use when Layer 3 routing would suffice. Try to follow level 1-3 first! The lowest level needed is best.

:::tip[Start at Layer 2]
Most skills only need Layers 1-2. Add Layer 3 when the skill genuinely handles multiple distinct operations. Add Layer 4 only for strict compliance or audit workflows where the agent must not skip ahead.
:::

## Compaction Survival

Long-running workflows risk losing context when the conversation compresses. The **document-as-cache pattern** solves this: the output document itself stores the workflow's state.

| Component             | Purpose                                                |
| --------------------- | ------------------------------------------------------ |
| **YAML front matter** | Paths to input files, current stage status, timestamps |
| **Draft sections**    | Progressive content built across stages                |
| **Status marker**     | Which stage is complete, for resumption                |

Each stage reads the output document to restore context, does its work, and writes results back to the same document. If context compacts mid-workflow, the next stage recovers by reading the document and reloading the input files listed in front matter.

```markdown
---
title: 'Analysis: Research Topic'
status: 'analysis'
inputs:
  - '{project_root}/docs/brief.md'
  - '{project_root}/data/sources.json'
---
```

This avoids separate cache files, file collisions when running multiple workflows, and state synchronization complexity.

## Choosing the Right Layer

| Situation                                      | Recommended Layer             |
| ---------------------------------------------- | ----------------------------- |
| Single-purpose utility with one path           | Layer 1-2                     |
| Skill with conditional reference data          | Layer 2                       |
| Skill that does multiple distinct things       | Layer 3                       |
| Skill with stages that depend on each other    | Layer 3 + compaction survival |
| Strict sequential process, no skipping allowed | Layer 4                       |
| Long-running workflow producing a document     | Layer 3 + document-as-cache   |
