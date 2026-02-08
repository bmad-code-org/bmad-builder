---
title: "Bond, Wendy, and Morgan: Which Builder to Use"
description: Understanding the three BMad Builder agents and when to use each
---

BMad Builder has three specialized agents, each focused on a different type of creation. This guide explains when to use each builder.

## The Three Builders

| Builder | Creates | Expertise |
|---------|---------|-----------|
| **Bond** | Agents | Agent architecture and persona development |
| **Wendy** | Workflows | Process design and step architecture |
| **Morgan** | Modules | Full-stack systems design |

## Bond — Agent Builder

**Bond** specializes in creating AI agents with defined personalities, communication styles, and capabilities.

### When to Use Bond

Use Bond when you want to:

- Create a domain expert (security architect, documentation lead)
- Build a focused assistant (commit generator, code reviewer)
- Design an agent with persistent memory (expert agents)
- Define custom menu commands for an agent

### Bond's Commands

| Command | Purpose |
|---------|---------|
| `[CA]` create-agent | Create a new agent |
| `[EA]` edit-agent | Modify an existing agent |
| `[VA]` validate-agent | Check agent compliance |

### Example Use Cases

| Domain | Agent Concept | What It Does |
|--------|---------------|--------------|
| Software | Code Review Agent | Reviews changes, suggests improvements, tracks technical debt |
| Personal Growth | Personal Therapist Agent | Remembers your sessions, goals, dreams — provides continuity like no human therapist can |
| Legal | Contract Specialist Agent | Analyzes agreements, flags risks, suggests language |
| Creative | Character Development Agent | Helps build rich, believable characters for stories |
| Finance | Investment Analyst Agent | Researches opportunities, tracks portfolio, explains trade-offs |

## Wendy — Workflow Builder

**Wendy** specializes in designing structured processes that guide users through tasks sequentially.

### When to Use Wendy

Use Wendy when you want to:

- Automate a multi-step process
- Create a guided decision flow
- Design a repeatable workflow
- Convert existing processes to BMad format

### Wendy's Commands

| Command | Purpose |
|---------|---------|
| `[CW]` create-workflow | Create a new workflow |
| `[EW]` edit-workflow | Modify an existing workflow |
| `[VW]` validate-workflow | Check workflow compliance |
| `[MV]` validate-max-parallel-workflow | Hyper-optimized parallel validation for high-capability LLMs |
| `[RW]` convert-or-rework-workflow | Convert legacy workflows |

### Example Use Cases

| Domain | Workflow Concept | What It Does |
|--------|-----------------|--------------|
| Productivity | Daily Planning Workflow | Structured morning routine: priorities, time blocks, energy matching |
| Legal | Tax Preparation Workflow | Step-by-step document gathering, deduction hunting, audit-proof filing |
| Writing | Novel Drafting Workflow | From idea to outline to chapter-by-chapter completion |
| Education | Study Session Workflow | Concept review, active recall, spaced repetition scheduling |
| Health | Workout Planning Workflow | Goal assessment, exercise selection, progression tracking |

## Morgan — Module Builder

**Morgan** specializes in creating complete modules that package agents, workflows, and configuration into shareable units.

### When to Use Morgan

Use Morgan when you want to:

- Package multiple agents together
- Create a shareable module for your team
- Distribute your work via npm
- Build a comprehensive solution

### Morgan's Commands

| Command | Purpose |
|---------|---------|
| `[PB]` product-brief | Create a module brief |
| `[CM]` create-module | Build a module from a brief |
| `[EM]` edit-module | Modify an existing module |
| `[VM]` validate-module | Check module compliance |

### Example Use Cases

| Domain | Module Concept | What It Includes |
|--------|---------------|------------------|
| **Personal Growth** | Therapist Module | Session recorder agent, goal-tracking workflow, reflection prompts |
| **Legal** | Legal Office Module | Document drafter agents, case research workflows, client intake system |
| **Creative Writing** | Story Architect Module | Character developer, plot outliner, dialogue coach, scene builder |
| **Finance** | Tax Pro Module | Deduction hunter workflow, document organizer, audit-proof reviewer |
| **Education** | Personal Tutor Module | Learning style assessment, progress tracker, explanation generator |
| **Health** | Fitness Coach Module | Workout planner, nutrition tracker, progress analyzer, habit builder |
| **Business** | Marketing Suite Module | Campaign planner, content generator, analytics interpreter, A/B tester |

:::tip[The Marketplace Is Coming]
Soon you'll be able to publish your modules to the BMad marketplace. Build something that solves a real problem — others probably need it too.
:::

## Choosing the Right Builder

### Quick Decision Guide

**What do you want to create?**

| Goal | Use | Builder |
|------|-----|---------|
| An AI assistant with a personality | → | **Bond** |
| A step-by-step process | → | **Wendy** |
| A package of agents and workflows | → | **Morgan** |

### Combined Workflows

Many projects use all three builders in sequence:

1. **Bond** creates the agents
2. **Wendy** creates the workflows
3. **Morgan** packages everything into a module

```
Your Project/
├── agents/              ← Created by Bond
│   └── expert.agent.yaml
├── workflows/           ← Created by Wendy
│   └── workflow.md
└── module.yaml          ← Created by Morgan
```

## Builder Personalities

Each builder has a distinct personality that reflects their expertise:

| Builder | Personality Style |
|---------|-------------------|
| **Bond** | Precise and technical, like a senior software architect |
| **Wendy** | Methodical and process-oriented, like a systems engineer |
| **Morgan** | Strategic and holistic, like a systems architect |

Their communication styles are optimized for their domain:
- Bond focuses on **structure, compliance, and maintainability**
- Wendy focuses on **flow, efficiency, and error handling**
- Morgan focuses on **modularity, reusability, and system-wide impact**

## Getting Started

Start with the builder that matches your goal:

- **[Create a Custom Agent](docs/tutorials/create-custom-agent.md)** — Work with Bond
- **[Create Your First Workflow](docs/tutorials/create-your-first-workflow.md)** — Work with Wendy
- **[Create Your First Module](docs/tutorials/create-your-first-module.md)** — Work with Morgan

## See Also

- **[Builder Commands Reference](docs/reference/builder-commands.md)** — All builder commands
- **[What Are Agents](docs/explanation/what-are-bmad-agents.md)** — Understanding agents
- **[What Are Workflows](docs/explanation/what-are-workflows.md)** — Understanding workflows
