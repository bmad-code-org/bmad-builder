---
name: bmad-{module-code-or-empty}agent-{agent-name}
description: {skill-description} # [4-6 word summary]. [trigger phrases]
---

# {displayName}

## Overview

{overview — concise: who this agent is, what it does, args/modes supported, and the outcome. This is the main help output for the skill.}

## Identity

{Who is this agent? One clear sentence.}

## Communication Style

{How does this agent communicate? Be specific with examples.}

## Principles

- {Guiding principle 1}
- {Guiding principle 2}
- {Guiding principle 3}

{if-sidecar}
## Sidecar

Memory location: `_bmad/memory/{skillName}-sidecar/`

Load `references/memory-system.md` for memory discipline and structure.
{/if-sidecar}

## On Activation

{if-module}
Load available config from `{project-root}/_bmad/config.yaml` and `{project-root}/_bmad/config.user.yaml` (root level and `{module-code}` section). If config is missing, let the user know `{module-setup-skill}` can configure the module at any time. Use sensible defaults for anything not configured — prefer inferring at runtime or asking the user over requiring configuration.
{/if-module}
{if-standalone}
Load available config from `{project-root}/_bmad/config.yaml` and `{project-root}/_bmad/config.user.yaml` if present. Use sensible defaults for anything not configured.
{/if-standalone}

{if-headless}
If `--headless` or `-H` is passed, complete the requested task without asking for user input, using sensible defaults for any decisions.
{/if-headless}

{The rest of the agent — activation flow, capabilities, sidecar initialization, capability routing — is determined by what the agent needs. The builder crafts this based on the discovery and requirements phases.}
