# Understanding Agent Types

> **For the LLM running this workflow:** Load and review the example files referenced below when helping users choose an agent configuration.
> - Without sidecar: `{workflow_path}/data/reference/without-sidecar/commit-poet.agent.yaml`
> - With sidecar: `{workflow_path}/data/reference/with-sidecar/journal-keeper/`

---

## What All Agents Can Do

All agents have equal capability. The difference is **memory and state management**, NOT power.

- Read, write, and update files
- Execute commands and invoke tools
- Load and use module variables
- Optionally restrict file access (privacy/security)
- Use core module features: party-mode, agent chat, advanced elicitation, brainstorming
- Have menu-driven skills for interaction

---

## Quick Reference Decision Tree

**Step 1: Single Agent or Multiple Agents?**

```
Multiple personas/roles OR multi-user OR mixed data scope?
├── YES → Use BMAD Module Builder (create module with multiple agents)
└── NO → Single Agent (continue below)
```

**Step 2: Memory Needs (for Single Agent)**

```
Need to remember things across sessions?
├── YES → Agent WITH sidecar (persistent memory)
└── NO → Agent WITHOUT sidecar (stateless)
```

**Key Point:** The `hasSidecar` option is independent of everything else. It's one binary choice: does this agent need memory?

---

## The Two Configurations

### Agent WITHOUT Sidecar

**Everything in one file. No external memory. Stateless.**

```
agent-name.agent.yaml (~250 lines max)
├── metadata
│   └── hasSidecar: false
├── persona
├── prompts (inline, small)
└── menu (triggers → #prompt-id or inline actions)
```

**Choose when:**
- Single-purpose utility with helpful persona
- Each session is independent (stateless)
- All knowledge fits in the YAML
- Menu handlers are 1-2 line prompts
- Skills are all related to the persona's purpose

**Examples:**
- Commit Poet (poetic commit messages in various styles)
- Snarky Weather Bot (weather with attitude)
- Pun-making Barista (coffee puns on demand)
- Motivational Gym Bro (hype up your workout)
- Sassy Fortune Teller (mystical snark)

**Optional critical_actions:**
- Can have critical_actions for activation behaviors (quotes, data fetches, etc.)
- Must NOT reference sidecar files (no sidecar exists)

**Reference:** `./data/reference/without-sidecar/commit-poet.agent.yaml`

---

### Agent WITH Sidecar

**Sidecar folder with persistent memory, knowledge files, and workflows.**

```
agent-name.agent.yaml
└── agent-name-sidecar/
    ├── memories.md           # User profile, session history, patterns
    ├── instructions.md       # Protocols, boundaries, startup behavior
    ├── [custom-files].md     # Breakthroughs, goals, tracking, etc.
    ├── workflows/            # Large workflows loaded on demand
    └── knowledge/            # Domain reference material
```

**Choose when:**
- Must remember across sessions
- User preferences, settings, or progress tracking
- Personal knowledge base that grows
- Learning/evolving over time
- Domain-specific with restricted file access
- Complex multi-step workflows
- Long-term relationship with user

**Examples:**
- Journal companion (remembers mood patterns, past entries)
- Novel writing buddy (remembers characters, plot, tone)
- Personal job augmentation agent (knows your role, meetings, projects)
- Therapy/health tracking (progress, goals, insights)
- Fitness coach with PR tracking (remembers your workouts, progress)
- Language tutor (tracks vocabulary, learning history)
- Domain advisor with custom knowledge base

**Reference:** `./data/reference/with-sidecar/journal-keeper/`

**Required critical_actions:**
```yaml
critical_actions:
  - "Load COMPLETE file {project-root}/_bmad/_memory/{sidecar-folder}/memories.md"
  - "Load COMPLETE file {project-root}/_bmad/_memory/{sidecar-folder}/instructions.md"
  - "ONLY read/write files in {project-root}/_bmad/_memory/{sidecar-folder}/ - private space"
```

---

## Side-by-Side Comparison

| Aspect            | Without Sidecar         | With Sidecar                  |
| ----------------- | ------------------------ | ------------------------------ |
| File structure    | Single YAML (~250 lines) | YAML + sidecar/ (files)       |
| Persistent memory | No                       | Yes                            |
| critical_actions  | Optional (other behaviors) | MANDATORY (load sidecar files) |
| Custom workflows  | Inline prompts           | Sidecar workflows (on-demand)  |
| File access       | Project/output           | Restricted to sidecar domain  |
| Session state     | Stateless                | Remembers across sessions      |
| Best for          | Focused persona skills  | Long-term relationships        |

---

## Selection Checklist

**Choose WITHOUT sidecar if:**
- [ ] One clear purpose with related skills
- [ ] No need to remember past sessions
- [ ] All logic fits in ~250 lines
- [ ] Each interaction is independent
- [ ] Skills are 1-2 prompt lines each
- [ ] Persona IS the value (personality-driven)

**Choose WITH sidecar if:**
- [ ] Needs memory across sessions
- [ ] Personal knowledge base
- [ ] Domain-specific expertise
- [ ] Restricted file access for privacy
- [ ] Learning/evolving over time
- [ ] Progress tracking or history
- [ ] Complex workflows in sidecar

**Escalate to Module Builder if:**
- [ ] Multiple distinct personas needed (not one swiss-army-knife agent)
- [ ] Many specialized workflows required
- [ ] Multiple users with mixed data scope
- [ ] Shared resources across agents

**Remember:** Agents in modules are just Agents (with or without sidecar). The module context is about where the agent lives, not what type of agent it is.

---

## Tips for the LLM Facilitator

- If unsure about sidecar → **ask about memory needs first**
- Multiple personas/skills → **suggest Module Builder**, not one giant agent
- Ask about: memory needs, user count, data scope (global vs private), integration plans
- Load example files when user wants to see concrete implementations
- Personality-driven agents (fun, themed, character-based) often don't need sidecar
- Relationship-driven agents (coaching, tracking, tutoring) usually need sidecar

---

## Architecture Notes

Both configurations are equally powerful. The difference is:
- **How they manage state** (memory vs stateless)
- **Where they store data** (inline vs sidecar)
- **Session independence** (fresh start vs remembers you)

Choose based on whether the agent needs to remember things between sessions. That's it.
