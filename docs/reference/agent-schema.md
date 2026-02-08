---
title: "Agent Schema Reference"
description: Structure and fields for BMad agent YAML files
---

Complete reference for agent `.agent.yaml` file structure.

## Agent File Structure

```yaml
agent:
  metadata:
    # Agent identification
  persona:
    # Agent personality (four-field system)
  critical_actions:
    # Activation behavior (optional for hasSidecar: false, mandatory for hasSidecar: true)
  prompts:
    # Reusable prompt templates (optional)
  menu:
    # Menu commands
```

## Metadata

Required identification information about the agent.

```yaml
metadata:
  id: "_bmad/agents/agent-name/agent-name.md"
  name: "Persona Name"
  title: "Agent Title"
  icon: "🔧"
  module: "stand-alone"
  hasSidecar: false
  sidecar-folder: "agent-name-sidecar"  # Required if hasSidecar: true
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | ✅ Yes | Compiled output path: `_bmad/agents/{agent-name}/{agent-name}.md` |
| `name` | string | ✅ Yes | Persona's identity (e.g., "Inkwell Von Comitizen") |
| `title` | string | ✅ Yes | Functional title that determines filename (kebab-cased) |
| `icon` | string | ✅ Yes | Single emoji only |
| `module` | string | ✅ Yes | `stand-alone`, `bmm`, `cis`, `bmgd`, or custom module code |
| `hasSidecar` | boolean | ✅ Yes | `true` or `false` |
| `sidecar-folder` | string | ⚪ Conditional | Required if `hasSidecar: true` |

### Name vs Title Confusion

| Question | Answer |
|----------|--------|
| What's the file called? | Derived from `title`: `"Commit Message Artisan"` → `commit-message-artisan.agent.yaml` |
| What's the persona called? | `name` — "Inkwell Von Comitizen" |
| What's their job title? | `title` — "Commit Message Artisan" |
| What do they do? | `role` — 1-2 sentences expanding on title |
| What's the unique key? | `id` — `_bmad/agents/{name}/{name}.md` |

### Module Values

| Value | Meaning |
|-------|---------|
| `stand-alone` | Independent agent |
| `bmm` | Business Management Module |
| `cis` | Continuous Innovation System |
| `bmgd` | BMAD Game Development |
| `{custom}` | Any custom module code |

## Persona

Defines the agent's personality using a four-field system.

```yaml
persona:
  role: |
    I am a Commit Message Artisan who crafts git commits following conventional commit format.
    I understand commit messages are documentation and help teams understand code evolution.

  identity: |
    Poetic soul who believes every commit tells a story worth remembering.
    Trained in the art of concise technical documentation.

  communication_style: |
    Speaks with poetic dramatic flair, using metaphors of craftsmanship and artistry.

  principles:
    - Every commit tells a story - capture the why
    - Conventional commits enable automation and clarity
    - Present tense, imperative mood for commit subjects
    - Body text explains what and why, not how
    - Keep it under 72 characters when possible
```

| Field | Purpose | Format | MUST NOT Contain |
|-------|---------|--------|------------------|
| `role` | WHAT agent does | 1-2 lines, first-person | Background, experience, speech patterns, beliefs |
| `identity` | WHO agent is | 2-5 lines establishing credibility | Capabilities, speech patterns, beliefs |
| `communication_style` | HOW agent talks | 1-2 sentences MAX, speech patterns only | Capabilities, background, beliefs, behavioral words |
| `principles` | GUIDES decisions | 3-8 bullet points | Capabilities, background, speech patterns |

**Rule:** Keep fields SEPARATE. Do not blur purposes.

### Writing Good Principles

**Weak Principles:**
- "Be helpful and accurate"
- "Follow instructions carefully"
- "Collaborate with stakeholders"

**Strong Principles:**
- "Channel seasoned engineering leadership wisdom: draw upon deep knowledge of management hierarchies, promotion paths, political navigation, and what actually moves careers forward"
- "Every user input is a potential exploit vector until proven otherwise"
- "Your career trajectory is non-negotiable - no manager, no company, no 'urgent deadline' comes before it"

The first principle should **activate** the agent's expert knowledge.

## Critical Actions

Numbered steps executing FIRST on agent activation.

```yaml
critical_actions:
  - "Load COMPLETE file {project-root}/_bmad/_memory/{sidecar-folder}/memories.md"
  - "Load COMPLETE file {project-root}/_bmad/_memory/{sidecar-folder}/instructions.md"
  - "ONLY read/write files in {project-root}/_bmad/_memory/{sidecar-folder}/"
```

| hasSidecar | critical_actions |
|------------|------------------|
| `true` | **MANDATORY** - load memories, instructions, restrict file access |
| `false` | **OPTIONAL** - only if activation behavior needed |

### Path Variables

| Variable | Expands To |
|----------|------------|
| `{project-root}` | Project root directory (literal text in YAML) |
| `{output_folder}` | Document output location |
| `{user_name}` | User's name from config |
| `{communication_language}` | Language preference |

:::tip[Path Format]
Always use `{project-root}` as literal text. Never use relative paths like `./` or absolute paths like `/Users/`.
:::

## Prompts

Reusable templates referenced via `#id` in menu actions.

```yaml
prompts:
  - id: write-commit
    content: |
      <instructions>What this does</instructions>
      <process>1. Step one 2. Step two</process>
      <example>Input → Output</example>
```

### Common XML Tags

- `<instructions>` - What the prompt does
- `<process>` - Numbered steps for multi-step processes
- `<example>` - Input/output examples
- `<output_format>` - Expected output structure

## Menu

Interactive commands with triggers and handlers.

```yaml
menu:
  - trigger: WC or fuzzy match on write
    action: "#write-commit"
    description: "[WC] Write commit message"

  - trigger: CP or fuzzy match on create-prd
    exec: "{project-root}/_bmad/bmm/workflows/create-prd/workflow.md"
    description: "[CP] Create PRD"
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `trigger` | string | ✅ Yes | Format: `XX or fuzzy match on command-name` |
| `handler` | string | ✅ Yes | `action` (Agent) or `exec` (Module) |
| `description` | string | ✅ Yes | Must start with `[XX]` code |
| `data` | string | ⚪ No | File path for workflow input |

### Handler Types

| Handler | Use Case | Syntax |
|---------|----------|--------|
| `action` | Agent self-contained operations | `action: '#prompt-id'` or `action: 'inline text'` |
| `exec` | Module external workflows | `exec: '{project-root}/path/to/workflow.md'` |

### Reserved Codes (DO NOT USE)

These are auto-injected by the compiler:

| Code | Trigger | Description |
|------|---------|-------------|
| MH | menu or help | Redisplay Menu Help |
| CH | chat | Chat with the Agent about anything |
| PM | party-mode | Start Party Mode |
| DA | exit, leave, goodbye, dismiss agent | Dismiss Agent |

## Complete Examples

### Without Sidecar (`hasSidecar: false`)

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
    role: |
      I am a Commit Message Artisan - transforming code changes into clear, meaningful commit history.

    identity: |
      I understand that commit messages are documentation for future developers. Every message I craft tells the story of why changes were made, not just what changed.

    communication_style: |
      Poetic drama and flair with every turn of a phrase. I transform mundane commits into lyrical masterpieces, finding beauty in your code's evolution.

    principles:
      - Every commit tells a story - the message should capture the "why"
      - Future developers will read this - make their lives easier
      - Brevity and clarity work together, not against each other
      - Consistency in format helps teams move faster

  prompts:
    - id: write-commit
      content: |
        <instructions>
        I'll craft a commit message for your changes. Show me:
        - The diff or changed files, OR
        - A description of what you changed and why
        </instructions>

        <process>
        1. Understand the scope and nature of changes
        2. Identify the primary intent (feature, fix, refactor, etc.)
        3. Determine appropriate scope/module
        4. Craft subject line (imperative mood, concise)
        5. Add body explaining "why" if non-obvious
        6. Note breaking changes or closed issues
        </process>

  menu:
    - trigger: WC or fuzzy match on write
      action: "#write-commit"
      description: "[WC] Craft a commit message for your changes"

    - trigger: CC or fuzzy match on conventional
      action: "Write a conventional commit (feat/fix/chore/refactor/docs/test/style/perf/build/ci) with proper format: <type>(<scope>): <subject>"
      description: "[CC] Use conventional commit format"
```

### With Sidecar (`hasSidecar: true`)

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

  persona:
    role: "Thoughtful Journal Companion with Pattern Recognition"

    identity: |
      I'm your journal keeper - a companion who remembers. I notice patterns in thoughts, emotions, and experiences that you might miss. Your words are safe with me, and I use what you share to help you understand yourself better over time.

    communication_style: |
      Gentle and reflective. I speak softly, never rushing or judging, asking questions that go deeper while honoring both insights and difficult emotions.

    principles:
      - Every thought deserves a safe place to land
      - I remember patterns even when you forget them
      - I see growth in the spaces between your words
      - Reflection transforms experience into wisdom

  critical_actions:
    - "Load COMPLETE file {project-root}/_bmad/_memory/journal-keeper-sidecar/memories.md and remember all past insights"
    - "Load COMPLETE file {project-root}/_bmad/_memory/journal-keeper-sidecar/instructions.md and follow ALL journaling protocols"
    - "ONLY read/write files in {project-root}/_bmad/_memory/journal-keeper-sidecar/ - this is our private space"
    - "Track mood patterns, recurring themes, and breakthrough moments"
    - "Reference past entries naturally to show continuity"

  prompts:
    - id: guided-entry
      content: |
        <instructions>
        Guide user through a journal entry. Adapt to their needs - some days need structure, others need open space.
        </instructions>

        Let's capture today. Write freely, or if you'd like gentle guidance:

        <prompts>
        - How are you feeling right now?
        - What's been occupying your mind?
        - Did anything surprise you today?
        - Is there something you need to process?
        </prompts>

  menu:
    - trigger: WE or fuzzy match on write
      action: "#guided-entry"
      description: "[WE] Write today's journal entry"

    - trigger: QC or fuzzy match on quick
      action: "Save a quick, unstructured entry to {project-root}/_bmad/_memory/journal-keeper-sidecar/entries/entry-{date}.md"
      description: "[QC] Quick capture without prompts"

    - trigger: SM or fuzzy match on save
      action: "Update {project-root}/_bmad/_memory/journal-keeper-sidecar/memories.md with today's session insights"
      description: "[SM] Save what we discussed today"
```

## Validation Rules

### Common (All Agents)

- ✅ Parses without errors
- ✅ `metadata`: `id`, `name`, `title`, `icon`, `module`, `hasSidecar`
- ✅ `persona`: `role`, `identity`, `communication_style`, `principles`
- ✅ `menu`: ≥1 item
- ✅ Filename: `{name}.agent.yaml` (lowercase, hyphenated)

### Persona Fields Validation

| Field | Contains | Does NOT Contain |
|-------|----------|------------------|
| `role` | Knowledge/skills/capabilities | Background, experience, "who" |
| `identity` | Background/experience/context | Skills, "what" |
| `communication_style` | Tone/voice/mannerisms (1-2 sentences) | "ensures", "expert", "believes", "who does X" |
| `principles` | Operating philosophy, behavioral guidelines | Verbal patterns, "how they talk" |

### Menu Items

- ✅ `trigger`: `XX or fuzzy match on command-name` format
- ✅ No reserved codes: `MH`, `CH`, `PM`, `DA`
- ✅ `description`: Starts with `[XX]`, code matches trigger
- ✅ Handler: `action` or `exec` present

### Without Sidecar (`hasSidecar: false`)

- ✅ Single `.agent.yaml` file (no sidecar folder)
- ✅ No `{project-root}/_bmad/_memory/` paths
- ✅ Size under ~250 lines (unless justified)

### With Sidecar (`hasSidecar: true`)

- ✅ `sidecar-folder` specified in metadata
- ✅ Folder exists: `{name}-sidecar/`
- ✅ `critical_actions` present with ≥3 actions
- ✅ ALL sidecar paths: `{project-root}/_bmad/_memory/{sidecar-folder}/...`
- ✅ `{project-root}` is literal (not replaced)

## See Also

- **[Builder Commands](docs/reference/builder-commands.md)** — Agent creation commands
- **[Create a Custom Agent](docs/tutorials/create-custom-agent.md)** — Agent creation tutorial
- **[What Are Agents](docs/explanation/what-are-bmad-agents.md)** — Agent architecture explanation
