---
title: "Critical Actions Reference"
---

Critical actions are numbered steps that execute FIRST on agent activation. They enable autonomous behaviors and are essential for agents with sidecars.

:::note[Prerequisites]
- Understanding of [hasSidecar](docs/explanation/what-are-bmad-agents.md) configuration
- Familiarity with [Agent Schema](docs/reference/agent-schema.md)
:::

## Quick Reference

| hasSidecar | critical_actions |
|------------|------------------|
| `true` | **MANDATORY** - load memories, instructions, restrict file access |
| `false` | **OPTIONAL** - only if activation behavior needed |

## What Critical Actions Do

Critical actions are inserted as activation steps 4, 5, 6... by the compiler:

```xml
<activation critical="MANDATORY">
  <step n="1">Load persona from this current agent file (already in context)</step>
  <step n="2">Load config to get {user_name}, {communication_language}</step>
  <step n="3">Remember: user's name is {user_name}</step>
  <!-- YOUR critical_actions inserted here as steps 4, 5, 6... -->
  <step n="N">ALWAYS communicate in {communication_language}</step>
  <step n="N+1">Show greeting + numbered menu</step>
  <step n="N+2">STOP and WAIT for user input</step>
</activation>
```

## Patterns

### hasSidecar: true (MANDATORY)

Agents with sidecars MUST include these critical actions:

```yaml
critical_actions:
  - 'Load COMPLETE file {project-root}/_bmad/_memory/{sidecar-folder}/memories.md'
  - 'Load COMPLETE file {project-root}/_bmad/_memory/{sidecar-folder}/instructions.md'
  - 'ONLY read/write files in {project-root}/_bmad/_memory/{sidecar-folder}/'
```

**Why these are mandatory:**

1. **Load memories** - The agent needs to remember past sessions
2. **Load instructions** - Additional protocols beyond the persona
3. **Restrict file access** - Security boundary for the agent's operations

### hasSidecar: false (OPTIONAL)

For simple agents, critical actions are optional. Use them for activation-time behaviors:

```yaml
critical_actions:
  - 'Show inspirational quote before menu'
  - 'Fetch latest stock prices before displaying menu'
  - 'Review {project-root}/finances/ for most recent data'
```

### hasSidecar: true + extras

You can add additional actions after the mandatory ones:

```yaml
critical_actions:
  - 'Load COMPLETE file {project-root}/_bmad/_memory/{sidecar-folder}/memories.md'
  - 'Load COMPLETE file {project-root}/_bmad/_memory/{sidecar-folder}/instructions.md'
  - 'ONLY read/write files in {project-root}/_bmad/_memory/{sidecar-folder}/'
  - 'Search web for biotech headlines, display before menu'
```

## Path Patterns

| Use | Pattern |
|-----|---------|
| Sidecar memory | `{project-root}/_bmad/_memory/{sidecar-folder}/file.md` |
| Project data | `{project-root}/path/to/file.csv` |
| Output | `{output_folder}/results/` |

**Key:** `{project-root}` = literal text in YAML, resolved at runtime

### Path Variables

| Variable | Expands To |
|----------|------------|
| `{project-root}` | Project root directory |
| `{output_folder}` | Document output location |
| `{user_name}` | User's name from config |
| `{communication_language}` | Language preference |

```yaml
# ✅ CORRECT
critical_actions:
  - "Load COMPLETE file {project-root}/_bmad/_memory/journal-sidecar/memories.md"
  - "ONLY read/write files in {project-root}/_bmad/_memory/journal-sidecar/"

# ❌ WRONG
critical_actions:
  - "Load ./journal-sidecar/memories.md"
  - "Load /Users/absolute/path/memories.md"
```

## Dos & Don'ts

| ✅ DO | ❌ DON'T |
|-------|---------|
| Use `Load COMPLETE file` | Use `Load file` or `Load ./path/file.md` |
| Restrict file access for sidecars | Duplicate compiler functions (persona, menu, greeting) |
| Use for activation-time behavior | Put philosophical guidance (use `principles`) |
| Use literal `{project-root}` | Use relative paths like `../` |

## Compiler Auto-Adds (Don't Duplicate)

The compiler automatically adds these activation steps. Don't duplicate them in critical_actions:

- Load persona
- Load configuration
- Menu system initialization
- Greeting/handshake

## Complete Examples

### Without Sidecar (No critical_actions)

```yaml
agent:
  metadata:
    id: _bmad/agents/commit-poet/commit-poet.md
    name: "Inkwell Von Comitizen"
    title: "Commit Message Artisan"
    icon: "📜"
    module: stand-alone
    hasSidecar: false

  persona:
    role: "I am a Commit Message Artisan..."
    identity: "I understand commit messages are documentation..."
    communication_style: "Poetic drama with flair..."
    principles:
      - "Every commit tells a story - capture the why"

  prompts:
    - id: write-commit
      content: |
        <instructions>What this does</instructions>

  menu:
    - trigger: WC or fuzzy match on write
      action: "#write-commit"
      description: "[WC] Write commit message"
```

### Without Sidecar (With critical_actions)

```yaml
agent:
  metadata:
    hasSidecar: false

  critical_actions:
    - 'Display inspirational quote before showing menu'
    - 'Check git status for context'

  # ... rest of agent
```

### With Sidecar (Mandatory critical_actions)

```yaml
agent:
  metadata:
    id: _bmad/agents/journal-keeper/journal-keeper.md
    name: "Whisper"
    title: "Personal Journal Companion"
    icon: "📔"
    module: stand-alone
    hasSidecar: true
    sidecar-folder: journal-keeper-sidecar

  critical_actions:
    - "Load COMPLETE file {project-root}/_bmad/_memory/journal-keeper-sidecar/memories.md and remember all past insights"
    - "Load COMPLETE file {project-root}/_bmad/_memory/journal-keeper-sidecar/instructions.md and follow ALL journaling protocols"
    - "ONLY read/write files in {project-root}/_bmad/_memory/journal-keeper-sidecar/ - this is our private space"
    - "Track mood patterns, recurring themes, and breakthrough moments"
    - "Reference past entries naturally to show continuity"

  # ... rest of agent
```

## Domain Restriction Patterns

### Single folder (most common)

```yaml
- 'ONLY read/write files in {project-root}/_bmad/_memory/{sidecar-folder}/'
```

### Read-only knowledge + write memories

```yaml
- 'Load from {project-root}/_bmad/_memory/{sidecar-folder}/knowledge/ but NEVER modify'
- 'Write ONLY to {project-root}/_bmad/_memory/{sidecar-folder}/memories.md'
```

### User folder access

```yaml
- 'ONLY access files in {user-folder}/journals/ - private space'
```

## Validation Rules

### hasSidecar: false

- [ ] No sidecar path references
- [ ] No placeholders (like "TODO: add actions")
- [ ] No compiler-injected steps (persona load, greeting, etc.)

### hasSidecar: true

- [ ] Loads memories from `{project-root}/_bmad/_memory/{sidecar-folder}/memories.md`
- [ ] Loads instructions from `{project-root}/_bmad/_memory/{sidecar-folder}/instructions.md`
- [ ] Restricts file access to sidecar folder
- [ ] ALL paths use `{project-root}/_bmad/_memory/{sidecar-folder}/...` format
- [ ] `{project-root}` is literal (not replaced)

## Common Questions

**What happens if I skip critical_actions for hasSidecar: true?**

The agent won't load memory or instructions, and won't restrict file access. This breaks the sidecar pattern.

**Can I have critical_actions without a sidecar?**

Yes, but they're optional. Use them for activation-time behaviors like showing a quote or fetching data.

**How many critical_actions can I have?**

As many as you need, but keep them focused on activation behavior. Complex logic should go in prompts or workflows.

**Do critical_actions run on every menu command?**

No, they only run once when the agent is first activated.

## See Also

- **[Agent Schema Reference](docs/reference/agent-schema.md)** - Complete agent structure
- **[Design Agent Menus](docs/how-to/design-agent-menus.md)** - Menu system design
- **[What Are Agents](docs/explanation/what-are-bmad-agents.md)** - Agent architecture
- **[Agent Compilation](https://github.com/bmad-code-org/bmad-builder/tree/main/src/workflows/agent/data/agent-compilation.md)** - How YAML becomes compiled agents
