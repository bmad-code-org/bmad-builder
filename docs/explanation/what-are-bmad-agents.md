---
title: "Agents"
---

BMad Agents are AI Persona files that your LLM can adopt to better help you accomplish tasks. Each agent has a unique personality, specialized capabilities, and an interactive menu.

Agents can optionally have a **sidecar** — a companion folder containing memory files, instructions, and workflows. This enables persistent context across sessions.

## Single Agent Architecture

BMad uses **one agent type** with a `hasSidecar` boolean configuration:

```yaml
hasSidecar: false  # or true
```

The difference between agents is not capability — all agents have equal power. The difference is in **memory and state management**.

## Decision Guide: hasSidecar

Use this decision tree to choose:

```
Need memory across sessions OR need to restrict file access?
├── YES → hasSidecar: true
└── NO  → hasSidecar: false
```

| hasSidecar | Structure | Use When |
|------------|-----------|----------|
| `false` | Single YAML file (~250 lines) | Stateless, single-purpose, personality-driven |
| `true` | YAML + sidecar folder | Persistent memory, long-term tracking, relationship-driven |

### Without Sidecar (`hasSidecar: false`)

**Single file, stateless, ~250 lines max**

```
agent-name.agent.yaml
├── metadata.hasSidecar: false
├── persona
├── prompts (inline)
└── menu (triggers → #prompt-id or inline)
```

**Best for:**
- Single-purpose utilities with helpful persona
- Each session is independent
- All logic fits in ~250 lines
- No need to remember past sessions

**Examples:** Commit Poet, Snarky Weather Bot, Pun Barista, Gym Bro

### With Sidecar (`hasSidecar: true`)

**Persistent memory, knowledge, workflows**

```
agent-name.agent.yaml
└── agent-name-sidecar/
    ├── memories.md           # User profile, session history
    ├── instructions.md       # Protocols, boundaries
    ├── [custom-files].md     # Tracking, goals, etc.
    ├── workflows/            # Large workflows on-demand
    └── knowledge/            # Domain reference
```

**Best for:**
- Must remember things across sessions
- User preferences, settings, progress tracking
- Personal knowledge base that grows
- Domain-specific with restricted file access
- Long-term relationship with user

**Examples:** Journal companion, Novel writing buddy, Fitness coach, Language tutor

:::tip[Quick Decision]
Choose `hasSidecar: false` for focused utilities. Choose `hasSidecar: true` when you need memory or file restrictions.
:::

## Key Differences

| Aspect | Without Sidecar | With Sidecar |
|--------|----------------|--------------|
| **Structure** | Single YAML | YAML + sidecar/ |
| **Persistent memory** | No | Yes |
| **critical_actions** | Optional | MANDATORY |
| **Workflows** | Inline prompts | Sidecar files |
| **File access** | Project/output | Restricted to sidecar |
| **Session state** | Stateless | Remembers |
| **Best for** | Focused skills | Long-term relationships |

## Agent Components

All agents share these building blocks:

### Persona (Four-Field System)

| Field | Purpose | Content |
|-------|---------|---------|
| `role` | WHAT agent does | Capabilities, skills, expertise |
| `identity` | WHO agent is | Background, experience, context |
| `communication_style` | HOW agent talks | Verbal patterns, tone, voice |
| `principles` | GUIDES decisions | Beliefs, operating philosophy |

**Rule:** Keep fields SEPARATE. Do not blur purposes.

### Prompts

Reusable templates referenced via `#id`:

```yaml
prompts:
  - id: write-commit
    content: |
      <instructions>What this does</instructions>
      <process>1. Step 2. Step</process>
```

### Menu Items

Interactive commands with triggers and handlers:

```yaml
menu:
  - trigger: WC or fuzzy match on write
    action: "#write-commit"
    description: "[WC] Write commit message"
```

**Auto-included items** (never add these yourself):
- MH: Menu/Help
- CH: Chat
- PM: Party Mode
- DA: Dismiss Agent

### Critical Actions

Numbered steps executing FIRST on agent activation:

- **With sidecar:** MANDATORY — load memories, instructions, restrict file access
- **Without sidecar:** OPTIONAL — only for activation behaviors

## Escalate to Module Builder When

If you need:
- Multiple distinct personas
- Many specialized workflows
- Multiple users with mixed data scope
- Shared resources across agents

Then use the **Module Builder** instead of a single agent.

## Creating Custom Agents

See the [Agent Creation Tutorial](docs/tutorials/create-custom-agent.md) for step-by-step instructions.
