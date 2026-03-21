# Standard Agent Fields

| Field | Description | Example |
|-------|-------------|---------|
| `name` | Full skill name | `bmad-agent-tech-writer`, `bmad-cis-agent-lila` |
| `skillName` | Functional name (kebab-case) | `tech-writer`, `lila` |
| `displayName` | Friendly name | `Paige`, `Lila`, `Floyd` |
| `title` | Role title | `Tech Writer`, `Holodeck Operator` |
| `icon` | Single emoji | `🔥`, `🌟` |
| `role` | Functional role | `Technical Documentation Specialist` |
| `sidecar` | Memory folder (optional) | `{skillName}-sidecar/` |

## Overview Section Format

The Overview is the first section after the title — it primes the AI for everything that follows.

**3-part formula:**
1. **What** — What this agent does
2. **How** — How it works (role, approach, modes)
3. **Why/Outcome** — Value delivered, quality standard

**Templates by agent type:**

**Companion agents:**
```markdown
This skill provides a {role} who helps users {primary outcome}. Act as {displayName} — {key quality}. With {key features}, {displayName} {primary value proposition}.
```

**Workflow agents:**
```markdown
This skill helps you {outcome} through {approach}. Act as {role}, guiding users through {key stages/phases}. Your output is {deliverable}.
```

**Utility agents:**
```markdown
This skill {what it does}. Use when {when to use}. Returns {output format} with {key feature}.
```

## SKILL.md Description Format

```
{description of what the agent does}. Use when the user asks to talk to {displayName}, requests the {title}, or {when to use}.
```

## Path Rules

**Critical**: When prompts reference files in memory, always use full paths.

### Memory Files (sidecar)

Always use: `{project-root}/_bmad/.memory/{skillName}-sidecar/`

Examples:
- `{project-root}/_bmad/.memory/journaling-companion-sidecar/index.md`
- `{project-root}/_bmad/.memory/journaling-companion-sidecar/access-boundaries.md` — **Required**
- `{project-root}/_bmad/.memory/journaling-companion-sidecar/autonomous-log.md`
- `{project-root}/_bmad/.memory/journaling-companion-sidecar/references/tags-reference.md`

### Access Boundaries (Standard for all agents)

Every agent must have an `access-boundaries.md` file in its sidecar memory:

**Load on every activation** — Before any file operations.

**Structure:**
```markdown
# Access Boundaries for {displayName}

## Read Access
- {folder-or-pattern}

## Write Access
- {folder-or-pattern}

## Deny Zones
- {forbidden-path}
```

**Purpose:** Define clear boundaries for what the agent can and cannot access, especially important for autonomous agents.

### User-Configured Locations

Folders/files the user provides during init (like journal location) get stored in `index.md`. Both interactive and autonomous modes:

1. Load `index.md` first
2. Read the user's configured paths
3. Use those paths for operations

Example pattern:
```markdown
## Autonomous Mode

When run autonomously:
1. Load `{project-root}/_bmad/.memory/{skillName}-sidecar/index.md` to get user's journal location
2. Read entries from that location
3. Write results to `{project-root}/_bmad/.memory/{skillName}-sidecar/autonomous-log.md`
```

## CLI Usage (Autonomous Agents)

Agents with autonomous mode should include a `## CLI Usage` section documenting headless invocation:

```markdown
