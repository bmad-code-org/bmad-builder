---
title: 'What Are BMad Modules?'
description: How agents and workflows combine into installable, configurable modules within the BMad ecosystem
---

BMad modules package related agents and workflows into a cohesive, installable unit with shared configuration and help system registration.

## What a Module Contains

A module is a folder of skills — agents and/or workflows — plus a **setup skill** that handles installation and configuration.

| Component           | Purpose                                                                               |
| ------------------- | ------------------------------------------------------------------------------------- |
| **Skills**          | The agents and workflows that deliver the module's capabilities                       |
| **Setup skill**     | Collects user preferences, writes config, registers capabilities with the help system |
| **module.yaml**     | Declares module identity and configurable variables                                   |
| **module-help.csv** | Lists every capability users can discover and invoke                                  |

The setup skill is the only required infrastructure. Everything else is just well-built skills that happen to work together.

## Agent vs. Workflow vs. Both

The first architecture decision when planning a module is whether to use a single agent, multiple workflows, or a combination.

| Architecture                       | When It Fits                                                                 | Trade-offs                                                                                                    |
| ---------------------------------- | ---------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| **Single agent with capabilities** | All capabilities serve the same user journey and benefit from shared context | Simpler to maintain, better memory continuity, seamless UX. Can feel monolithic if capabilities are unrelated |
| **Multiple workflows**             | Capabilities serve different user journeys or require different tools        | Each workflow is focused and composable. Users switch between skills explicitly                               |
| **Hybrid**                         | Some capabilities need persistent persona/memory while others are procedural | Best of both worlds but more skills to build and maintain                                                     |

:::tip[Agent-First Thinking]
Many users default to building multiple single-purpose agents. Consider whether one agent with rich internal capabilities and routing would serve users better. A single agent accumulates context, maintains memory across interactions, and provides a more seamless experience.
:::

## Multi-Agent Modules and Memory

Modules with multiple agents introduce a memory architecture decision. Every BMad agent has its own **sidecar memory** — a personal folder where it stores user preferences, learned patterns, session history, and domain-specific data. In a multi-agent module, you also need to decide whether agents should share memory.

| Pattern                              | When It Fits                                                                            |
| ------------------------------------ | --------------------------------------------------------------------------------------- |
| **Personal sidecars only**           | Agents have distinct domains with minimal overlap                                       |
| **Personal + shared module sidecar** | Agents have their own context but also learn shared things about the user or project    |
| **Shared sidecar only**              | All agents serve the same domain — consider whether a single agent is the better design |

**Example:** A social creative module with a podcast expert, a viral video expert, and a blog expert. Each agent remembers the specifics of what it has done with the user — episode topics, video formats, blog themes. But they all also learn about the user's communication style, favorite catchphrases, content preferences, and brand voice. This shared knowledge lives in a module-level sidecar that every agent reads from and contributes to.

Each agent should still be self-contained with its own capabilities, even if this means duplicating some common functionality. A podcast expert that can independently handle a full session without needing the blog expert is better than one that depends on shared state to function.

See **[What Are BMad Agents](/explanation/what-are-bmad-agents.md)** for details on how agent memory and sidecars work.

## Standalone vs. Expansion Modules

| Type           | Description                                                                                                               |
| -------------- | ------------------------------------------------------------------------------------------------------------------------- |
| **Standalone** | Provides complete, independent value. Does not depend on another module being installed                                   |
| **Expansion**  | Extends an existing module with new capabilities. Should still provide utility even if the parent module is not installed |

Expansion modules can reference the parent module's capabilities in their help CSV ordering (before/after fields). This lets a new capability slot into the parent module's natural workflow sequence.

Even expansion modules should be designed to work independently — the parent module being absent should degrade gracefully, not break the expansion.

## Configuration and Registration

Modules register with a project through three files in `{project-root}/_bmad/`:

| File               | Purpose                                                                |
| ------------------ | ---------------------------------------------------------------------- |
| `config.yaml`      | Shared settings committed to git — module section keyed by module code |
| `config.user.yaml` | Personal settings (gitignored) — user name, language preferences       |
| `module-help.csv`  | Capability registry — one row per action users can discover            |

Not every module needs configuration. If skills work with sensible defaults, the setup skill can focus purely on help registration. See **[Module Configuration](/explanation/module-configuration.md)** for details on when configuration adds value.

## External Dependencies

Some modules depend on tools outside the BMad ecosystem.

| Dependency Type  | Examples                                             |
| ---------------- | ---------------------------------------------------- |
| **CLI tools**    | `docker`, `terraform`, `ffmpeg`                      |
| **MCP servers**  | Custom or third-party Model Context Protocol servers |
| **Web services** | APIs that require credentials or configuration       |

When a module has external dependencies, the setup skill should check for their presence and guide users through installation or configuration.

## UI and Visualization

Modules can include user interfaces — dashboards, progress views, interactive visualizations, or even full web applications. A UI skill might show shared progress across the module's capabilities, provide a visual map of how skills relate, or offer an interactive way to navigate the module's features.

Not every module needs a UI. But for complex modules with many capabilities, a visual layer can make the experience significantly more accessible.

## Building a Module

The Module Builder (`bmad-module-builder`) provides three capabilities for the module lifecycle:

1. **Ideate Module (IM)** — Brainstorm and plan through creative facilitation
2. **Create Module (CM)** — Scaffold the setup skill into your skills folder
3. **Validate Module (VM)** — Verify structural integrity and entry quality

See the **[Builder Commands Reference](/reference/builder-commands.md)** for detailed documentation on each capability.
