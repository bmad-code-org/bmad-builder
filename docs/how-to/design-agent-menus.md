---
title: "Design Agent Menus"
---

Learn to design effective agent menus that provide intuitive access to your agent's capabilities. Well-designed menus make agents discoverable, efficient, and delightful to use.

:::note[Prerequisites]
- Familiarity with [Agent Schema](docs/reference/agent-schema.md)
- Understanding of [hasSidecar](docs/explanation/what-are-bmad-agents.md) configuration
:::

## Menu Item Schema

```yaml
menu:
  - trigger: XX or fuzzy match on command-name
    [handler]: [value]
    description: '[XX] Display text'
    data: [optional]   # Pass file to workflow
```

| Field | Required | Validation |
|-------|----------|------------|
| `trigger` | Yes | Format: `XX or fuzzy match on command-name` |
| `description` | Yes | Must start with `[XX]` code |
| `handler` | Yes | `action` (Agent) or `exec` (Module) |
| `data` | No | File path for workflow input |

## Handler Types

| Handler | Use Case | Syntax |
|---------|----------|--------|
| `action` | Agent self-contained operations | `action: '#prompt-id'` or `action: 'inline text'` |
| `exec` | Module external workflows | `exec: '{project-root}/path/to/workflow.md'` |

### Action Handler

For agent-internal operations using prompts or inline instructions:

```yaml
# Reference a prompt
- trigger: WC or fuzzy match on write-commit
  action: "#write-commit"
  description: "[WC] Write commit message"

# Inline instruction
- trigger: SM or fuzzy match on save-memory
  action: "Update {project-root}/_bmad/_memory/{sidecar-folder}/memories.md"
  description: "[SM] Save session"
```

### Exec Handler

For module workflows or external scripts:

```yaml
- trigger: CP or fuzzy match on create-prd
  exec: '{project-root}/_bmad/bmm/workflows/create-prd/workflow.md'
  description: '[CP] Create PRD'
```

## Trigger Format

The trigger defines how users can invoke the menu item:

```yaml
trigger: XX or fuzzy match on command-name
```

| Component | Purpose | Example |
|-----------|---------|---------|
| `XX` | Two-letter code for quick reference | `WC` |
| `or` | Separator between exact and fuzzy match | `or` |
| `fuzzy match on` | Indicates fuzzy matching follows | `fuzzy match on` |
| `command-name` | Natural language trigger | `write-commit` |

### Examples

```yaml
# Good: Short code + clear command
- trigger: WC or fuzzy match on write
  description: "[WC] Write commit message"

# Good: Multiple natural triggers
- trigger: WE or fuzzy match on write entry journal
  description: "[WE] Write journal entry"

# Good: Descriptive command name
- trigger: PR or fuzzy match on pattern reflection analyze
  description: "[PR] See patterns in your entries"
```

## Description Format

Descriptions must start with the two-letter code in brackets:

```yaml
description: "[XX] Display text"
```

### Examples

```yaml
# ✅ CORRECT
description: "[WC] Write commit message"
description: "[WE] Write today's journal entry"
description: "[SM] Save what we discussed today"

# ❌ WRONG - Missing code
description: "Write commit message"

# ❌ WRONG - Wrong code
description: "[WR] Write commit message"  # Code doesn't match trigger
```

## Reserved Codes (Never Use)

These codes are auto-injected by the compiler:

| Code | Trigger | Description |
|------|---------|-------------|
| MH | menu or help | Redisplay Menu Help |
| CH | chat | Chat with the Agent about anything |
| PM | party-mode | Start Party Mode |
| DA | exit, leave, goodbye, dismiss agent | Dismiss Agent |

:::tip[Reserved Code Check]
Never use MH, CH, PM, or DA as your trigger codes. They're automatically included in every agent's menu.
:::

## Path Variables

Use these variables in your menu actions:

| Variable | Expands To |
|----------|------------|
| `{project-root}` | Project root directory |
| `{output_folder}` | Document output location |
| `{user_name}` | User's name from config |
| `{communication_language}` | Language preference |

```yaml
# ✅ CORRECT
exec: '{project-root}/_bmad/core/workflows/brainstorming/workflow.md'

# ❌ WRONG
exec: '../../../core/workflows/brainstorming/workflow.md'
```

## Complete Examples

### Without Sidecar (Simple Agent)

```yaml
menu:
  - trigger: WC or fuzzy match on write
    action: "#write-commit"
    description: "[WC] Craft a commit message for your changes"

  - trigger: AC or fuzzy match on analyze
    action: "#analyze-changes"
    description: "[AC] Analyze changes before writing the message"

  - trigger: IM or fuzzy match on improve
    action: "#improve-message"
    description: "[IM] Improve an existing commit message"

  - trigger: BC or fuzzy match on batch
    action: "#batch-commits"
    description: "[BC] Create cohesive messages for multiple commits"

  - trigger: CC or fuzzy match on conventional
    action: "Write a conventional commit (feat/fix/chore/refactor/docs/test/style/perf/build/ci) with proper format: <type>(<scope>): <subject>"
    description: "[CC] Use conventional commit format"
```

### With Sidecar (Expert Agent)

```yaml
menu:
  - trigger: WE or fuzzy match on write
    action: "#guided-entry"
    description: "[WE] Write today's journal entry"

  - trigger: QC or fuzzy match on quick
    action: "Save a quick, unstructured entry to {project-root}/_bmad/_memory/journal-keeper-sidecar/entries/entry-{date}.md"
    description: "[QC] Quick capture without prompts"

  - trigger: MC or fuzzy match on mood
    action: "#mood-check"
    description: "[MC] Track your current emotional state"

  - trigger: PR or fuzzy match on patterns
    action: "#pattern-reflection"
    description: "[PR] See patterns in your recent entries"

  - trigger: SM or fuzzy match on save
    action: "Update {project-root}/_bmad/_memory/journal-keeper-sidecar/memories.md with today's session insights"
    description: "[SM] Save what we discussed today"
```

### Module Agent (External Workflows)

```yaml
menu:
  - trigger: WI or fuzzy match on workflow-init
    exec: '{project-root}/_bmad/bmm/workflows/workflow-status/workflow.md'
    description: '[WI] Initialize workflow'

  - trigger: BS or fuzzy match on brainstorm
    exec: '{project-root}/_bmad/core/workflows/brainstorming/workflow.md'
    description: '[BS] Guided brainstorming'
```

## Menu Design Best Practices

### 1. Logical Grouping

Group related commands together:

```yaml
menu:
  # Creation commands
  - trigger: WC or fuzzy match on write
    action: "#write-commit"
    description: "[WC] Write commit message"

  - trigger: BC or fuzzy match on batch
    action: "#batch-commits"
    description: "[BC] Batch multiple commits"

  # Analysis commands
  - trigger: AC or fuzzy match on analyze
    action: "#analyze-changes"
    description: "[AC] Analyze changes"

  - trigger: PR or fuzzy match on patterns
    action: "#pattern-reflection"
    description: "[PR] Show patterns"

  # Utility commands
  - trigger: SM or fuzzy match on save
    action: "Update memories.md"
    description: "[SM] Save session"
```

### 2. Clear Descriptions

Descriptions should be self-explanatory:

```yaml
# ✅ Good - Clear and specific
description: "[WE] Write today's journal entry"
description: "[QC] Quick capture without prompts"

# ❌ Bad - Vague
description: "[WE] Write"
description: "[QC] Quick"
```

### 3. Consistent Codes

Use memorable two-letter codes:

```yaml
# Write/Creation
WC - Write Commit
WE - Write Entry
WD - Write Doc

# Analysis
AC - Analyze Code
PR - Pattern Reflection
RC - Review Changes

# Utility
SM - Save Memory
QC - Quick Capture
HM - Help Menu
```

### 4. Progressive Disclosure

For complex agents, consider primary vs. secondary commands:

```yaml
menu:
  # Primary - Most common
  - trigger: WE or fuzzy match on write entry
    action: "#guided-entry"
    description: "[WE] Write journal entry"

  - trigger: QC or fuzzy match on quick
    action: "Quick capture"
    description: "[QC] Quick capture"

  # Secondary - Less common
  - trigger: PR or fuzzy match on patterns reflection
    action: "#pattern-reflection"
    description: "[PR] See patterns"

  - trigger: WR or fuzzy match on weekly reflection
    action: "#weekly-reflection"
    description: "[WR] Weekly reflection"
```

## Data Parameter

Attach to ANY handler to pass input files:

```yaml
- trigger: TS or fuzzy match on team-standup
  exec: '{project-root}/_bmad/bmm/tasks/team-standup.md'
  data: '{project-root}/_bmad/_config/agent-manifest.csv'
  description: '[TS] Run team standup'
```

## Validation Rules

1. **Triggers:** `XX or fuzzy match on command-name` format required
2. **Descriptions:** Must start with `[XX]` code matching trigger
3. **Reserved codes:** MH, CH, PM, DA never valid in user menus
4. **Code uniqueness:** Required within each agent
5. **Paths:** Always use `{project-root}`, never relative paths
6. **Handler choice:** `action` for Agents, `exec` for Modules
7. **Sidecar paths:** `{project-root}/_bmad/_memory/{sidecar-folder}/`

## Common Questions

**How many menu items should I have?**

Aim for 5-10 items. Too many becomes overwhelming. Consider if you need multiple agents instead.

**Should I use codes or fuzzy matching?**

Use both! Codes are for power users, fuzzy matching makes it accessible to everyone.

**Can I change codes later?**

Yes, but be aware that users may have memorized them. Document breaking changes.

## See Also

- **[Agent Schema Reference](docs/reference/agent-schema.md)** - Complete menu schema
- **[Critical Actions Reference](docs/reference/critical-actions.md)** - Activation behavior
- **[What Are Agents](docs/explanation/what-are-bmad-agents.md)** - Agent architecture
