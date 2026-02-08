---
title: "Create a Custom Agent"
---

Build your own AI agent with a unique personality, specialized commands, and optional persistent memory using the BMad Builder workflow.

:::note[BMB Module]
This tutorial uses the **BMad Builder (BMB)** module. Make sure you have BMad installed with the BMB module enabled.
:::

## What You'll Learn

- How to run the `create-agent` workflow
- Choose between `hasSidecar: true` or `false`
- Define your agent's persona (role, identity, communication style, principles)
- Design effective menu commands
- Package and install your custom agent

:::note[Prerequisites]
- BMad installed with the BMB module
- An idea for what you want your agent to do
- About 15-30 minutes for your first agent
:::

:::tip[Quick Path]
Run `create-agent` workflow → Follow the guided steps → Install your agent module → Test and iterate.
:::

## Understanding hasSidecar

BMad uses **one agent type** with a `hasSidecar` boolean configuration:

```yaml
hasSidecar: false  # or true
```

The difference is not capability — all agents have equal power. The difference is in **memory and state management**.

### Decision Guide

```
Need memory across sessions OR need to restrict file access?
├── YES → hasSidecar: true
└── NO  → hasSidecar: false
```

| hasSidecar | Structure | Best For |
|------------|-----------|----------|
| `false` | Single YAML (~250 lines) | Single-purpose utilities, personality-driven agents |
| `true` | YAML + sidecar folder | Persistent memory, long-term tracking, domain specialists |

**Without Sidecar Examples:** Commit Poet, Snarky Weather Bot, Pun Barista, Gym Bro

**With Sidecar Examples:** Journal companion, Novel writing buddy, Fitness coach, Language tutor

## Step 1: Start the Workflow

In your IDE (Claude Code, Cursor, etc.), invoke the create-agent workflow with the agent-builder agent.

The workflow guides you through eight steps:

| Step | What You'll Do |
|------|----------------|
| **Brainstorm** *(optional)* | Explore ideas with creative techniques |
| **Discovery** | Define the agent's purpose and goals |
| **Type & Metadata** | Choose hasSidecar, name your agent |
| **Persona** | Craft the agent's personality and principles |
| **Commands** | Define what the agent can do |
| **Activation** | Set up critical_actions *(optional/mandatory)* |
| **Build** | Generate the agent file |
| **Validation** | Review and verify everything works |

:::tip[Workflow Options]
At each step, the workflow provides options:
- **[A] Advanced** - Get deeper insights and reasoning
- **[P] Party** - Get multiple agent perspectives
- **[C] Continue** - Move to the next step
:::

## Step 2: Define the Persona

Your agent's personality is defined by four fields:

| Field | Purpose | Example |
|-------|---------|---------|
| **Role** | What they do | "Senior code reviewer who catches bugs and suggests improvements" |
| **Identity** | Who they are | "Friendly but exacting, believes clean code is a craft" |
| **Communication Style** | How they speak | "Direct, constructive, explains the 'why' behind suggestions" |
| **Principles** | Why they act | "Security first, clarity over cleverness, test what you fix" |

### Field Separation Rule

Keep each field focused on its purpose:

| Field | Contains | Does NOT Contain |
|-------|----------|------------------|
| `role` | Knowledge/skills/capabilities | Background, experience, speech patterns, beliefs |
| `identity` | Background/experience/context | Skills, speech patterns, beliefs |
| `communication_style` | Tone/voice/mannerisms (1-2 sentences) | Behavioral words, capabilities, beliefs |
| `principles` | Operating philosophy | Verbal patterns, capabilities |

:::note[Writing Great Principles]
The first principle should "activate" the agent's expertise:

**Weak:**
- "Be helpful and accurate"
- "Follow instructions carefully"

**Strong:**
- "Channel seasoned engineering leadership wisdom: draw upon deep knowledge of management hierarchies, promotion paths, and what actually moves careers forward"
- "Think like an attacker first: leverage OWASP Top 10, common vulnerability patterns, and the mindset that finds what others miss"
:::

## Step 3: Design Menu Commands

Define what your agent can do through menu items:

```yaml
menu:
  - trigger: WC or fuzzy match on write
    action: "#write-commit"
    description: "[WC] Write commit message"
```

### Menu Format Rules

| Component | Format | Example |
|-----------|--------|---------|
| `trigger` | `XX or fuzzy match on command-name` | `WC or fuzzy match on write` |
| `description` | `[XX] Display text` | `[WC] Write commit message` |
| `action` | `#prompt-id` or inline text | `#write-commit` |

### Handler Types

| Handler | Use Case | Syntax |
|---------|----------|--------|
| `action` | Agent self-contained operations | `action: '#prompt-id'` or `action: 'inline text'` |
| `exec` | Module external workflows | `exec: '{project-root}/path/to/workflow.md'` |

### Reserved Codes (Never Use)

These are auto-injected:
- **MH**: Menu/Help
- **CH**: Chat
- **PM**: Party Mode
- **DA**: Dismiss Agent

## Step 4: Configure Critical Actions

Instructions that execute before the agent starts.

### Without Sidecar (OPTIONAL)

```yaml
critical_actions:
  - "Show inspirational quote before menu"
  - "Fetch latest stock prices before displaying menu"
```

### With Sidecar (MANDATORY)

```yaml
critical_actions:
  - "Load COMPLETE file {project-root}/_bmad/_memory/{sidecar-folder}/memories.md"
  - "Load COMPLETE file {project-root}/_bmad/_memory/{sidecar-folder}/instructions.md"
  - "ONLY read/write files in {project-root}/_bmad/_memory/{sidecar-folder}/"
```

:::tip[Path Format]
Always use `{project-root}` as literal text. Never use relative paths like `./` or absolute paths like `/Users/`.
:::

## Step 5: Install Your Agent

Once created, package your agent for installation:

```
my-custom-stuff/
├── module.yaml          # Contains: unitary: true
├── agents/
│   └── {agent-name}/
│       ├── {agent-name}.agent.yaml
│       └── {agent-name}-sidecar/    # hasSidecar: true only
│           ├── memories.md
│           ├── instructions.md
│           └── [custom-files].md
└── workflows/           # Optional: custom workflows
```

Install using the BMad installer, then invoke your new agent in your IDE.

## What You've Accomplished

You've created a custom AI agent with:

- A defined purpose and role in your workflow
- A unique persona with communication style and principles
- Custom menu commands for your specific tasks
- Optional persistent memory for ongoing context

Your project now includes:

```
_bmad/
├── _config/
│   └── agents/
│       └── {your-agent}/        # Your agent customizations
└── {module}/
    └── agents/
        └── {your-agent}/
            └── {your-agent}.agent.yaml
```

## Quick Reference

| Action | How |
|--------|-----|
| Start workflow | `"Run the BMad Builder create-agent workflow"` |
| Edit agent directly | Modify `{agent-name}.agent.yaml` |
| Edit customization | Modify `_bmad/_config/agents/{agent-name}` |
| Rebuild agent | `npx bmad-method build <agent-name>` |
| Study examples | Check `src/workflows/agent/data/reference/` |

## Common Questions

**Should I use hasSidecar true or false?**
Use `false` for focused, one-off tasks. Use `true` when you need memory across sessions or restricted file access.

**How do I add more commands later?**
Edit the agent YAML directly or use the customization file in `_bmad/_config/agents/`. Then rebuild.

**Can I share my agent with others?**
Yes. Package your agent as a standalone module and share it with your team or the community.

**Where can I see example agents?**
Study the reference agents in `src/workflows/agent/data/reference/`:
- [commit-poet.agent.yaml](https://github.com/bmad-code-org/bmad-builder/tree/main/src/workflows/agent/data/reference/without-sidecar/commit-poet.agent.yaml) (hasSidecar: false)
- [journal-keeper](https://github.com/bmad-code-org/bmad-builder/tree/main/src/workflows/agent/data/reference/with-sidecar/journal-keeper/) (hasSidecar: true)

## Getting Help

- **[Discord Community](https://discord.gg/gk8jAdXWmj)** - Ask in #bmad-method-help or #report-bugs-and-issues
- **[GitHub Issues](https://github.com/bmad-code-org/bmad-builder/issues)** - Report bugs or request features

## Further Reading

- **[What Are Agents](docs/explanation/what-are-bmad-agents.md)** - Deep technical details on agent architecture
- **[Agent Schema Reference](docs/reference/agent-schema.md)** - Complete field reference
- **[Custom Content Installation](docs/how-to/install-custom-modules.md)** - Package and distribute your agents
- **[Persona Development Guide](docs/how-to/develop-agent-persona.md)** - Advanced persona crafting
- **[Principles Crafting Guide](docs/explanation/crafting-agent-principles.md)** - Write effective principles

:::tip[Key Takeaways]
- **Start small** - Your first agent should solve one problem well
- **Persona matters** - Strong principles activate the agent's expertise
- **Iterate often** - Test your agent and refine based on behavior
- **Learn from examples** - Study reference agents before building your own
:::
