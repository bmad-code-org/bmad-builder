---
title: 'What Are BMad Agents?'
description: How agents differ from workflows, what makes them stateful personas, and when to build one
---

BMad Agents are self-contained AI skills that combine a **persona**, **capabilities**, and **persistent memory** into a conversational partner you can return to across sessions.

## What Makes an Agent an Agent

Every skill in the BMad ecosystem is ultimately a skill file, but agents carry three traits that set them apart.

| Trait            | What It Means                                                                                                          |
| ---------------- | ---------------------------------------------------------------------------------------------------------------------- |
| **Persona**      | A defined role and voice — architect, therapist, game master, finance advisor — that shapes how the agent communicates |
| **Capabilities** | Actions the agent can perform, either as internal prompt commands or by calling external skills                        |
| **Memory**       | A sidecar directory where the agent stores what it learns about you, your preferences, and past interactions           |

Together these create something that feels less like running a command and more like talking to a specialist who already knows you.

## How Memory Works

When an agent launches for the first time in a project, it can create a sidecar memory directory at `_bmad/memory/<agent-name>/`. On every subsequent launch the agent loads this memory, which is how it remembers your preferences, prior decisions, and anything you told it to retain.

Agents can also include a **first-run onboarding** step — a set of questions the agent asks on initial launch so it can configure itself for your needs before you start working together.

:::tip[Memory Lives Outside the Skill]
Agent memory is stored in your project, not inside the skill folder. This prevents agents from accidentally modifying their own instructions and keeps your data portable. Also the same agent can be used with different projects or shared with others and generate their own memory space!
:::

## Capabilities: Internal and External

Agent capabilities come in two flavors.

| Type                  | Description                                                 | Example                                                                                                     |
| --------------------- | ----------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| **Internal commands** | Prompt-driven actions defined inside the agent's skill file | A Dream Agent's "Dream Capture" command                                                                     |
| **External skills**   | Standalone skills or workflows the agent can invoke         | Calling the `create-prd` workflow via a PM agent - allowing the workflow to retain customization and memory |

You choose the mix when you design the agent. Internal commands keep everything self-contained; external skills let you compose agents from reusable building blocks.

## Headless Mode

Agents support a headless (autonomous) wake mode. When activated — for example through a cron job or an orchestrator like Open Claw — the agent skips waiting for user input and attempts to complete its tasks independently. This makes agents suitable for background automation while still being conversational when a human is present.

## When to Build an Agent vs. a Workflow

| Choose an Agent When                              | Choose a Workflow When                           |
| ------------------------------------------------- | ------------------------------------------------ |
| The user will return to it repeatedly             | The process runs once and produces an output     |
| Remembering context across sessions adds value    | Stateless execution is fine                      |
| A strong persona improves the interaction         | Personality is secondary to getting the job done |
| The skill spans many loosely related capabilities | All steps serve a single, focused goal           |

If you are unsure, start with a workflow. You can always wrap it inside an agent later.

## Building Agents

The **BMad Agent Builder** (`bmad-agent-builder`) walks you through a six-phase conversational discovery process — from intent through capabilities, requirements, drafting, building, and quality optimization. It produces a ready-to-use skill folder you can drop into your tools' skills directory.

See the [Builder Commands Reference](/reference/builder-commands.md) for details on the build process phases and capabilities.
