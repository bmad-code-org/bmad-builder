---
title: 'Customization for Authors'
description: How to decide whether your skill should support end-user customization, and what to expose when it does
---

Shipping a `customize.toml` is opt-in per skill. This is the author-side counterpart to [How to Customize BMad](https://docs.bmad-method.org/how-to/customize-bmad/), which covers the end-user view. Read that first if you haven't; it shows what users experience when they override a skill. This guide is about deciding whether to give them that surface at all.

Downstream users typically don't hand-write TOML. BMad ships a core skill called `bmad-customize` that walks them through authoring overrides conversationally — it scans which skills are customizable, picks agent vs workflow scope, writes the override file, and verifies the merge. Users who prefer to edit TOML directly still can, but the conversational flow is the default path. That affects the names and defaults you pick: a user being walked through `"set prd_template to your template path"` handles that fine; `tmpl_override` or `opt_2` makes the conversation awkward. Pick field names that read well out loud.

## The Problem

Every customization knob you ship is a promise. Users pin values to it, teams commit overrides to git, and future releases have to respect the shape you locked in. Over-exposing makes the skill harder to evolve and invites drift; under-exposing forces forks for changes that should have been a three-line TOML file.

Aim to expose what varies naturally across your users, and nothing else.

## How Authoring Customization Fits

BMad has a three-layer override model from the user's side:

```text
Priority 1 (wins): _bmad/custom/{skill-name}.user.toml  (personal, gitignored)
Priority 2:        _bmad/custom/{skill-name}.toml        (team/org, committed)
Priority 3 (last): skill's own customize.toml            (your defaults)
```

As an author you own Priority 3. You ship `customize.toml` next to `SKILL.md`. Every field you put there is a commitment to your users: this is what I support overriding. The resolver merges layers structurally (scalars win, arrays of tables keyed by `code` or `id` replace-by-key, other arrays append), so you don't write merge logic. You write defaults and trust the shape.

## The Three Questions

For each candidate knob, ask:

1. **Does it vary naturally across the actual user population?** If every user wants roughly the same value, don't make it configurable. Pick the right default and move on.
2. **Is it the skill's identity, or something the skill consumes?** Identity stays baked. Consumed context (templates, facts, output paths, tone) is the right surface.
3. **Would hiding it force a fork, or just a sentence?** If the alternative is forking the whole skill, expose it. If the alternative is a one-line sentence the user can drop into `persistent_facts`, hide it.

Candidates that pass all three earn a place in `customize.toml`. Everything else stays baked, or gets folded into `persistent_facts` where sentence-shaped variance belongs.

## Agent vs Workflow Defaults

Agents and workflows enter the customize.toml question from different starting points.

| Surface | Metadata block | Override surface | Notes |
| --- | --- | --- | --- |
| Agent | Always required | Opt-in | Metadata feeds `module.yaml:agents[]` and the central agent roster. |
| Workflow | Not required | Fully opt-in | No roster. If you don't opt in, no `customize.toml` is emitted at all. |

For agents, you always ship `customize.toml` (the roster depends on it). The real question is whether it carries an override surface beyond metadata. For workflows, the choice is binary: ship one or don't.

## Memory and Autonomous Agents

Default to **no** on the override-surface opt-in for memory and autonomous agents. Their sanctum (PERSONA, CREED, BOND, CAPABILITIES) is already the customization surface. It's calibrated at First Breath, evolved by the owner over time, and shared across teams as sanctum files when the whole team wants the same voice. A parallel TOML surface competes with that; you end up with two places to shape the agent and neither fully owns the job.

Opt in only when you have a specific org-level need the sanctum can't express. Pre-sanctum compliance loads qualify (a legal banner acknowledgment gate before rebirth, for example). Persona tweaks don't.

## A Worked Example: `bmad-session-prep`

A weekly session-prep workflow for tabletop RPG game masters. It reads the last session's log, reviews open campaign threads, drafts the scene spine, stats NPCs and encounters, and produces a GM notes document to run from.

Here's how to think about its customization surface, field by field.

### `persistent_facts` (default globs the campaign bible)

```toml
persistent_facts = [
  "file:{project-root}/campaigns/**/campaign-bible.md",
  "file:{project-root}/campaigns/**/house-rules.md",
]
```

Every GM runs a different world. Without their campaign bible in context, the workflow is a generic fantasy prep tool that knows nothing about the party's rivals, the kingdom's politics, or last month's cliffhanger. The default glob is shaped so a GM can drop a `campaign-bible.md` in their project and the workflow picks it up. Forcing them to paste world context at the start of every session would burn trust. That's what persistent facts are for.

### `system_rules_template` (scalar, default to D&D 5e)

```toml
system_rules_template = "resources/dnd-5e-quick-reference.md"
```

D&D 5e, Pathfinder 2e, and Call of Cthulhu reason about encounters in very different ways. A PF2e GM who overrides this with their own rules reference gets correctly-calibrated encounter math without the workflow pretending to know a system it doesn't. The skill isn't trying to catalog every RPG; it ships one default that covers most users and lets everyone else swap in their own reference. The `*_template` suffix signals what changes if the user touches it.

### `session_notes_template` (scalar)

```toml
session_notes_template = "resources/session-notes-minimalist.md"
```

GM prep style is personal. Some GMs want theater-of-mind bullets; others want scene blocks with initiative trackers pre-filled and read-aloud boxes for boxed text. No single shipping default wins against that variance. The structural fact that "prep produces notes" is universal, though, so the override changes the shape of the notes file, not the stage sequence.

### `on_complete` (scalar, default empty)

```toml
on_complete = ""
```

The core skill ends when notes are drafted. Some GMs want the workflow to draft a Discord teaser for the group chat, others want encounter stat blocks pushed to Roll20, others want a pre-game meditation prompt. These are real patterns, but they're downstream of the skill's job, not part of it. An empty default means the skill doesn't presume. Override example:

```toml
on_complete = "Draft a 2-sentence Discord teaser ending on a cliffhanger. Save to {project-root}/teasers/next-session.md"
```

### `activation_steps_prepend` (pre-flight context load)

Before the workflow asks the GM anything, some tables want the most recent session log already loaded and summarized:

```toml
activation_steps_prepend = [
  "Scan {project-root}/session-logs/ and load the most recent log. Extract unresolved threads before asking the GM anything."
]
```

Not every GM keeps session logs. The ones who do want the pre-load; the ones who don't would get a broken activation if it were baked in. Opt-in via the prepend hook lets both tables use the same skill.

### What Not to Expose

The stage sequence (recap, threads, spine, NPCs, notes) is the skill's identity. A GM who wants a very different flow (solo journaling, West Marches gossip round) should fork. Every stage made optional erodes what the skill is.

Mechanical encounter math toggles like `auto_balance_cr` or `verbose_stat_blocks` stay out. The LLM handles those naturally once it has the system reference. Toggles here would amount to telling the executor how to do its job.

Per-stage question order stays out too. Too fiddly. If it matters enough to customize, you're describing a different skill.

## Naming and Shape Conventions

When you do expose a scalar, name it like a contract.

| Pattern | Use for | Example |
| --- | --- | --- |
| `<purpose>_template` | File paths for templates the skill loads | `brief_template = "resources/brief.md"` |
| `<purpose>_output_path` | Writable destinations | `report_output_path = "{project-root}/docs/reports"` |
| `on_<event>` | Hook scalars (prompts or commands) | `on_complete = ""` |

A scalar named `brief_template` tells the user what changes if they override it. A scalar named `style_config` or `format_options_file` doesn't.

For arrays of tables (menus, capability rosters), give every item a `code` or `id` field. The resolver uses that key to merge by code: matching entries replace in place, new entries append. Mixing `code` on some items and `id` on others falls back to append-only, which is rarely what authors want and almost never what users expect.

There's no removal mechanism. If you need users to suppress a default menu item, have them override it by `code` with a no-op description or prompt. If the natural override flow requires deleting defaults, your surface is probably wrong, and you should reconsider what belongs in the skill body.

## Where This Shows Up in Your Build

Both the Agent Builder and the Workflow Builder ask the opt-in question during requirements gathering. If you say yes, a follow-up phase called Configurability Discovery walks you through candidate knobs (templates, output paths, hooks) and emits them into your skill's `customize.toml`. If you say no, workflows get no `customize.toml` at all, and agents get a metadata-only block.

The builders default the opt-in to **no** in headless mode unless you pass `--customizable`. Customization should be a deliberate decision, not an automatic one.

## When to Graduate to a Fork

If your override surface grows to the point where shipping multiple related overrides is the common user path, the skill probably wants splitting. Two signals: users routinely ship four or more overrides together to make the skill work for them, or the overrides imply structural changes that `persistent_facts` and scalar swaps can't actually express. When you see either, a second skill variant is the honest answer, not a bigger TOML.

:::tip[Rule of Thumb]
Ship one good default over a permutation forest of toggles. A scalar called `include_combat_section = true/false` is almost always a sign the author couldn't decide what the skill should do. Pick the default. Fork if you need different.
:::
