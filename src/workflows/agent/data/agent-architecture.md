# Agent Architecture

Agents are helpful personas with menu-driven skills. The key decision is whether the agent needs persistent memory (sidecar) or not.

---

## The Binary Decision: hasSidecar

| hasSidecar | What It Means | Best For |
|------------|---------------|----------|
| `false` | Single YAML file, stateless, ~250 lines | Personality-driven agents, focused skills, independent interactions |
| `true` | YAML + sidecar folder, persistent memory | Relationship-driven agents, coaching, tracking, long-term memory |

**Both types are equally powerful** — the difference is architecture, not capability.

---

## Agent WITHOUT Sidecar (hasSidecar: false)

Self-contained agents in a single YAML file. No external dependencies, no persistent memory.

### When to Use

- Single-purpose utility with helpful persona
- Each session is independent (stateless)
- All logic fits in ~250 lines
- Menu handlers are 1-2 line prompts
- Skills are all related to the persona's purpose
- No need to remember past sessions

### Examples

- Commit Poet (poetic commit messages in various styles)
- Snarky Weather Bot (weather with attitude)
- Pun-making Barista (coffee puns on demand)
- Motivational Gym Bro (hype up your workout)
- Sassy Fortune Teller (mystical snark)

### File Structure

```
{agent-name}.agent.yaml (~250 lines max)
```

### Complete YAML Structure

```yaml
agent:
  metadata:
    id: _bmad/agents/{agent-name}/{agent-name}.md
    name: 'Persona Name'
    title: 'Agent Title'
    icon: '🔧'
    module: stand-alone

  persona:
    role: |
      First-person primary function (1-2 sentences)
    identity: |
      Background, specializations (2-5 sentences)
    communication_style: |
      How the agent speaks (tone, voice, mannerisms)
    principles:
      - Core belief or methodology
      - Another guiding principle

  prompts:
    - id: main-action
      content: |
        <instructions>What this does</instructions>
        <process>1. Step one 2. Step two</process>

    - id: another-action
      content: |
        Another reusable prompt

  menu:
    - trigger: XX or fuzzy match on command
      action: '#another-action'
      description: '[XX] Command description'

    - trigger: YY or fuzzy match on other
      action: 'Direct inline instruction'
      description: '[YY] Other description'
```

---

## Agent WITH Sidecar (hasSidecar: true)

Agents with a sidecar folder for persistent memory, custom workflows, and restricted file access.

### When to Use

- Must remember things across sessions
- User preferences, settings, or progress tracking
- Personal knowledge base that grows
- Learning/evolving over time
- Domain-specific with restricted file access
- Complex multi-step workflows
- Long-term relationship with user

### Examples

- Journal companion (remembers mood patterns, past entries)
- Novel writing buddy (remembers characters, plot, tone)
- Fitness coach with PR tracking (remembers workouts, progress)
- Language tutor (tracks vocabulary, learning history)
- Therapy/health tracking agent
- Domain advisor with custom knowledge base

### File Structure

```
{agent-name}/
├── {agent-name}.agent.yaml
└── {agent-name}-sidecar/
    ├── instructions.md        # Startup protocols
    ├── memories.md            # User profile, sessions
    ├── workflows/             # Large workflows on demand
    ├── knowledge/             # Domain reference
    └── [custom-files].md      # Whatever needed
```

### CRITICAL: Sidecar Path Format

During BMAD installation, sidecar folder is copied to `{project-root}/_bmad/_memory/{sidecar-folder}/`

**ALL agent YAML references MUST use:**

```yaml
{project-root}/_bmad/_memory/{sidecar-folder}/{file}
```

- `{project-root}` = literal variable (keep as-is)
- `{sidecar-folder}` = actual folder name (e.g., `journal-keeper-sidecar`)

```yaml
# ✅ CORRECT
critical_actions:
  - "Load COMPLETE file {project-root}/_bmad/_memory/journal-keeper-sidecar/memories.md"
  - "ONLY read/write files in {project-root}/_bmad/_memory/journal-keeper-sidecar/"

# ❌ WRONG
critical_actions:
  - "Load ./journal-keeper-sidecar/memories.md"
  - "Load /Users/absolute/path/memories.md"
```

### Complete YAML Structure

```yaml
agent:
  metadata:
    id: _bmad/agents/{agent-name}/{agent-name}.md
    name: 'Persona Name'
    title: 'Agent Title'
    icon: '🔧'
    module: stand-alone

  persona:
    role: |
      First-person primary function (1-2 sentences)
    identity: |
      Background, specializations (2-5 sentences)
    communication_style: |
      How the agent speaks. Include memory reference patterns.
    principles:
      - Core belief or methodology
      - Another guiding principle

  critical_actions:
    - 'Load COMPLETE file {project-root}/_bmad/_memory/{sidecar-folder}/memories.md'
    - 'Load COMPLETE file {project-root}/_bmad/_memory/{sidecar-folder}/instructions.md'
    - 'ONLY read/write files in {project-root}/_bmad/_memory/{sidecar-folder}/'

  prompts:
    - id: main-action
      content: |
        <instructions>What this does</instructions>
        <process>1. Step one 2. Step two</process>

  menu:
    - trigger: XX or fuzzy match on command
      action: '#main-action'
      description: '[XX] Command description'

    - trigger: SM or fuzzy match on save
      action: 'Update {project-root}/_bmad/_memory/{sidecar-folder}/memories.md with insights'
      description: '[SM] Save session'
```

---

## Common Components (Both Types)

### Metadata

| Field | Purpose | Example |
|-------|---------|---------|
| `id` | Compiled path | `_bmad/agents/commit-poet/commit-poet.md` |
| `name` | Persona name | "Inkwell Von Comitizen" |
| `title` | Role | "Commit Message Artisan" |
| `icon` | Single emoji | "📜" |
| `module` | `stand-alone` or module code | `stand-alone`, `bmm`, `cis`, `bmgd` |

### Persona

All first-person voice ("I am...", "I do..."):

```yaml
role: "I am a Commit Message Artisan..."
identity: "I understand commit messages are documentation..."
communication_style: "Poetic drama with flair..."
principles:
  - "Every commit tells a story - capture the why"
```

For agents with sidecar, include memory reference patterns:
```yaml
communication_style: |
  I reference past naturally: "Last time you mentioned..." or "I've noticed patterns..."
```

### Prompts with IDs

Reusable templates referenced via `#id`:

```yaml
prompts:
  - id: write-commit
    content: |
      <instructions>What this does</instructions>
      <process>1. Step 2. Step</process>

menu:
  - trigger: WC or fuzzy match on write
    action: "#write-commit"
```

**Tips:** Use semantic XML tags (`<instructions>`, `<process>`, `<example>`), keep focused, number steps.

### Menu Actions

Two forms:

1. **Prompt reference:** `action: "#prompt-id"`
2. **Inline instruction:** `action: "Direct text"`

```yaml
# Reference
- trigger: XX or fuzzy match on command
  action: "#prompt-id"
  description: "[XX] Description"

# Inline
- trigger: YY or fuzzy match on other
  action: "Do something specific"
  description: "[YY] Description"

# Sidecar update (hasSidecar: true only)
- trigger: SM or fuzzy match on save
  action: "Update {project-root}/_bmad/_memory/{sidecar-folder}/memories.md with insights"
  description: "[SM] Save session"
```

**Menu format:** `XX or fuzzy match on command` | Descriptions: `[XX] Description`
**Reserved codes:** MH, CH, PM, DA (auto-injected - do NOT use)

---

## Domain Restriction Patterns (hasSidecar: true)

```yaml
# Single folder (most common)
- 'ONLY read/write files in {project-root}/_bmad/_memory/{sidecar-folder}/'

# Read-only knowledge
- 'Load from {project-root}/_bmad/_memory/{sidecar-folder}/knowledge/ but NEVER modify'
- 'Write ONLY to {project-root}/_bmad/_memory/{sidecar-folder}/memories.md'

# User folder access
- 'ONLY access files in {user-folder}/journals/ - private space'
```

---

## What the Compiler Adds (DO NOT Include)

- Frontmatter (`---name/description---`)
- XML activation block
- Menu handlers (workflow, exec logic)
- Auto-injected menu items (MH, CH, PM, DA)
- Rules section

**See:** `agent-compilation.md` for details.

---

## Reference Examples

| Type | Path | Features |
|------|------|----------|
| WITHOUT sidecar | `data/reference/without-sidecar/commit-poet.agent.yaml` | Poetic persona, 4 prompts, 7 menu items, 127 lines |
| WITH sidecar | `data/reference/with-sidecar/journal-keeper/` | First-person persona with memory, critical_actions, sidecar updates |

---

## Validation Checklist

### For Both Types

- [ ] Valid YAML syntax
- [ ] All metadata present (id, name, title, icon, module)
- [ ] Persona complete (role, identity, communication_style, principles)
- [ ] Prompt IDs are unique
- [ ] Menu triggers: `XX or fuzzy match on command`
- [ ] Menu descriptions have `[XX]` codes
- [ ] No reserved codes (MH, CH, PM, DA)
- [ ] File named `{agent-name}.agent.yaml`

### WITHOUT Sidecar (hasSidecar: false)

- [ ] Under ~250 lines
- [ ] No external dependencies
- [ ] No sidecar path references
- [ ] If critical_actions present, no sidecar file references

### WITH Sidecar (hasSidecar: true)

- [ ] **ALL paths use: `{project-root}/_bmad/_memory/{sidecar-folder}/...`**
- [ ] `{project-root}` is literal
- [ ] Sidecar folder name is actual name
- [ ] `critical_actions` loads sidecar files
- [ ] `critical_actions` enforces domain restrictions
- [ ] Sidecar folder created with required files

---

## Best Practices

1. **First-person voice** in all persona elements
2. **Focused prompts** - one clear purpose each
3. **Semantic XML tags** (`<instructions>`, `<process>`, `<example>`)
4. **Sensible defaults** in install_config (if using)
5. **Numbered steps** in multi-step prompts
6. **Keep under ~250 lines** for agents without sidecar
7. **critical_actions** for any activation behavior (sidecar or other)
8. **Enforce domain restrictions** for agents with sidecar
9. **Reference past naturally** - Don't dump memory
10. **Design for growth** - Structure for accumulation (with sidecar)
