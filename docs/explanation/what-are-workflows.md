---
title: "What Are BMad Workflows?"
description: How workflows guide users through structured processes, how they differ from agents and simple skills, and when to build one
---

BMad Workflows are skills that guide users through a **structured process** to produce a specific output. They are the workhorses of the BMad ecosystem — focused, composable, and generally stateless.

## What Makes a Workflow a Workflow

Like agents, workflows are ultimately skill files. The difference is in emphasis: workflows prioritize **getting to an outcome** over maintaining a persistent identity.

| Trait | Workflow | Agent |
| ----- | -------- | ----- |
| **Goal** | Complete a defined process and produce an artifact | Be an ongoing conversational partner |
| **Persona** | Minimal — enough to facilitate a good conversation | Central to the experience |
| **Memory** | Generally stateless between sessions | Persistent sidecar memory |
| **Scope** | All steps serve one cohesive purpose | Can span loosely related capabilities |

## Workflow Types

The BMad Builder classifies workflows into three tiers based on complexity.

| Type | Description | Example |
| ---- | ----------- | ------- |
| **Simple Utility** | A single-purpose tool that does one thing well | Validate a schema, convert a file format |
| **Simple Workflow** | A short guided process with a few sequential steps | Create a quick tech spec |
| **Complex Workflow** | A multi-stage process with branching paths, progressive disclosure, and potentially multiple outputs | Create and manage PRDs — covering create, edit, validate, convert, and polish |

:::tip[Start Simple]
Most ideas start as a Simple Utility or Simple Workflow. Graduate to Complex only when you genuinely need branching paths or multiple related operations in one skill.
:::

## Progressive Disclosure

Complex workflows use **progressive disclosure** to handle multiple operations within a single skill. Rather than building five separate skills for create, edit, validate, convert, and polish, you build one workflow that detects the user's intent — from how they talk to it or what arguments they pass — and routes internally to the right path.

This is the same pattern that powers BMad's own multi-capability agents and workflows. It keeps the user's experience simple while the skill handles routing behind the scenes.

## YOLO Mode and Guided Mode

Both the Agent Builder and the Workflow Builder support two interaction styles when creating skills.

| Mode | How It Works | Best For |
| ---- | ------------ | -------- |
| **YOLO** | You brain-dump your idea; the builder guesses its way to a finished skill, asking only when truly stuck | Quick prototypes, experienced builders |
| **Guided** | The builder walks you through decisions, clarifies ambiguities, and ensures nothing is overlooked | Production workflows, first-time builders |

Guided mode is no longer the slow multi-step process of earlier BMad versions. It is conversational and adaptive, but produces significantly better results than YOLO for complex workflows.

## Headless (Autonomous) Mode

Like agents, workflows can support a **Headless Mode**. When invoked headless — through a scheduler, orchestrator, or another skill — the workflow skips interactive prompts and completes its process end-to-end without waiting for user input.

## When to Build a Workflow vs. an Agent

| Choose a Workflow When | Choose an Agent When |
| ---------------------- | -------------------- |
| The process has a clear start and end | The user will return to it across sessions |
| No need to remember past interactions | Remembering context adds value |
| All steps serve one cohesive goal | Capabilities are loosely related |
| You want a composable building block | You want a persistent conversational partner |

Workflows are also excellent as the **internal capabilities** of an agent. Build the workflow first, then wrap it in an agent if you need persona and memory on top.

## Building Workflows

The **BMad Workflow Builder** (`bmad-workflow-builder`) uses the same six-phase conversational discovery as the Agent Builder — intent, classification, requirements, drafting, building, and quality optimization. It produces a ready-to-use skill folder.

See the [Builder Commands Reference](/reference/builder-commands.md) for details on the build process phases and capabilities.
