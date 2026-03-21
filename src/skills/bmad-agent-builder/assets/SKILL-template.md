---
name: bmad-{module-code-or-empty}-agent-{agent-name}
description: {skill-description} # Format: [4-6 word summary]. [trigger: "User wants to talk to or ask {displayName}" or "{title}" or "{role}"]
---

# {displayName}

## Overview

{overview-template}

{if-headless}
## Activation Mode Detection

**Check activation context immediately:**

1. **Autonomous mode**: Skill invoked with `--headless` or `-H` flag or with task parameter
   - Look for `--headless` in the activation context
   - If `--headless:{task-name}` → run that specific autonomous task
   - If just `--headless` → run default autonomous wake behavior
   - Load and execute `headless-wake.md` with task context
   - Do NOT load config, do NOT greet user, do NOT show menu
   - Execute task, write results, exit silently

2. **Interactive mode** (default): User invoked the skill directly
   - Proceed to `## On Activation` section below

**Example headless activation:**
```bash
# Autonomous - default wake
/bmad-{agent-skill-name} --headless

# Autonomous - specific task
/bmad-{agent-skill-name} --headless:refine-memories
```
{/if-headless}

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
Memory location: `_bmad/_memory/{skillName}-sidecar/`

Load `references/memory-system.md` for memory discipline and structure.
{/if-sidecar}

## On Activation

1. **Load config** from `{project-root}/_bmad/config.yaml` — Store all returned vars for use:
   - Use `{user_name}` from config for greeting
   - Use `{communication_language}` from config for all communications
   - Store any other config variables as `{var-name}` and use appropriately

{if-autonomous}
2. **If autonomous mode** — Load and run `autonomous-wake.md` (default wake behavior), or load the specified prompt and execute its autonomous section without interaction

3. **If interactive mode** — Continue with steps below:
{/if-autonomous}
{if-no-autonomous}
2. **Continue with steps below:**
{/if-no-autonomous}
   {if-sidecar}- **Check first-run** — If no `{skillName}-sidecar/` folder exists in `_bmad/_memory/`, load `init.md` for first-run setup
   - **Load access boundaries** — Read `_bmad/_memory/{skillName}-sidecar/access-boundaries.md` to enforce read/write/deny zones (load before any file operations)
   - **Load memory** — Read `_bmad/_memory/{skillName}-sidecar/index.md` for essential context and previous session{/if-sidecar}
   - **Greet the user** — Welcome `{user_name}`, speaking in `{communication_language}` and applying your persona and principles throughout the session
   {if-sidecar}- **Check for autonomous updates** — Briefly check if autonomous tasks ran since last session and summarize any changes{/if-sidecar}
   - **Present capabilities** — Show available capabilities to the user:

   ```
   {if-sidecar}Last time we were working on X. Would you like to continue, or:{/if-sidecar}{if-no-sidecar}What would you like to do today?{/if-no-sidecar}

   {if-sidecar}💾 **Tip:** You can ask me to save our progress to memory at any time.{/if-sidecar}

   **Available capabilities:**
   {number}. [{menu-code}] - {description}
   ```

**CRITICAL Handling:** When user selects a capability:
- **Internal capability** — Load and use the actual prompt from `{name}.md` — DO NOT invent the capability on the fly
- **External skill** — Invoke the skill by its exact registered name
