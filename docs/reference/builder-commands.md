---
title: "Builder Commands Reference"
description: Commands for the BMad Builder agents (Bond, Wendy, Morgan)
---

Quick reference for all builder commands.

## Builder Agents

| Agent | Name | Purpose |
|-------|------|---------|
| **agent-builder** | Bond | Create, edit, and validate agents |
| **workflow-builder** | Wendy | Create, edit, and validate workflows |
| **module-builder** | Morgan | Create, edit, and validate modules |

## Bond Commands (agent-builder)

| Command | Trigger | Description |
|---------|---------|-------------|
| **Create Agent** | `[CA]` or `create-agent` | Create a new BMad agent with guided assistance |
| **Edit Agent** | `[EA]` or `edit-agent` | Edit an existing agent while maintaining compliance |
| **Validate Agent** | `[VA]` or `validate-agent` | Check an agent for BMad compliance and best practices |

### Create Agent (`[CA]`)

Creates a new agent through a guided workflow.

**Workflow Steps:**
1. Brainstorm (optional) — Explore ideas
2. Discovery — Define agent's purpose
3. Type & Metadata — Choose Simple/Expert/Module, name agent
4. Persona — Craft personality and principles
5. Commands — Define menu commands
6. Activation — Set up autonomous behaviors (optional)
7. Build — Generate agent file
8. Validation — Review and verify

**Outputs:**
- Agent `.agent.yaml` file
- Optional `_memory/` folder for Expert agents

### Edit Agent (`[EA]`)

Edits an existing agent.

**Workflow Steps:**
1. Load existing agent
2. Discover changes needed
3. Select elements to modify
4. Apply changes
5. Celebrate completion

**What You Can Edit:**
- Persona (role, identity, communication style, principles)
- Menu commands
- Critical actions
- Metadata
- Sidecar files

### Validate Agent (`[VA]`)

Validates an agent against BMad standards.

**Checks:**
- Metadata completeness
- Persona structure
- Menu formatting
- YAML validity
- BMad Core compliance

## Wendy Commands (workflow-builder)

| Command | Trigger | Description |
|---------|---------|-------------|
| **Create Workflow** | `[CW]` or `create-workflow` | Create a new workflow with proper structure |
| **Edit Workflow** | `[EW]` or `edit-workflow` | Edit an existing workflow |
| **Validate Workflow** | `[VW]` or `validate-workflow` | Validate workflow structure and compliance |
| **Validate Max-Parallel** | `[MV]` or `validate-max-parallel-workflow` | Validate for parallel sub-process execution |
| **Rework Workflow** | `[RW]` or `convert-or-rework-workflow` | Convert or rework to V6 compliant format |

### Create Workflow (`[CW]`)

Creates a new workflow.

**Options:**
- **From Scratch** — Start with guided discovery
- **Convert Existing** — Convert existing workflow to BMad format

**Workflow Steps:**
1. Discovery — Understand your idea
2. Classification — Type, structure, output
3. Requirements — Inputs, tools, validation
4. Design — Step sequence
5. Foundation — Create workflow.md
6. Build Steps — Create step files
7. Completion — Final review

### Edit Workflow (`[EW]`)

Edits an existing workflow.

**Workflow Steps:**
1. Assess workflow
2. Discover edits needed
3. Select mode (direct/placeholder)
4. Apply edits
5. Validate after changes
6. Complete

### Validate Workflow (`[VW]`)

Validates a workflow.

**Checks:**
- Frontmatter completeness
- Step structure
- Menu handling
- Output format
- Cohesiveness

### Validate Max-Parallel (`[MV]`)

Hyper-optimized workflow validation for LLMs with high parallel processing capability (like Claude). Uses task agents to validate multiple workflow aspects simultaneously in sub-processes for dramatically faster results.

**Additional Checks:**
- Parallel compatibility
- Sub-process optimization
- Task agent orchestration
- LLM parallel capability utilization

### Rework Workflow (`[RW]`)

Converts or reworks workflows to V6 format.

**Use For:**
- Updating legacy workflows
- Fixing compliance issues
- Converting from other formats

## Morgan Commands (module-builder)

| Command | Trigger | Description |
|---------|---------|-------------|
| **Product Brief** | `[PB]` or `product-brief` | Create a module brief through creative discovery |
| **Create Module** | `[CM]` or `create-module` | Create a complete module from a brief |
| **Edit Module** | `[EM]` or `edit-module` | Edit an existing module |
| **Validate Module** | `[VM]` or `validate-module` | Validate module structure and compliance |

### Product Brief (`[PB]`)

Creates a module brief.

**Workflow Steps:**
1. Welcome and spark ideas
2. Define module type
3. Clarify vision
4. Identify users
5. Define value proposition
6. Plan agents
7. Plan workflows
8. Plan tools
9. Explore scenarios
10. Review and finalize

**Output:** `module-brief-{code}.md` file

### Create Module (`[CM]`)

Creates a module from a brief.

**Input:** Path to module brief file

**Creates:**
- Module directory structure
- `module.yaml` with configuration
- `_module-installer/` folder (if needed)
- Agent and workflow spec files
- README.md and TODO.md

### Edit Module (`[EM]`)

Edits an existing module.

**Can Edit:**
- `module.yaml` configuration
- Install questions
- Module metadata
- Configuration values

### Validate Module (`[VM]`)

Validates a module.

**Checks:**
- `module.yaml` validity
- Folder structure
- Agent file compliance
- Workflow file compliance
- `package.json` configuration

## Command Quick Reference

| Task | Agent | Command |
|------|-------|---------|
| Create agent | Bond | `[CA]` |
| Create workflow | Wendy | `[CW]` |
| Create module brief | Morgan | `[PB]` |
| Create module | Morgan | `[CM]` |
| Edit agent | Bond | `[EA]` |
| Edit workflow | Wendy | `[EW]` |
| Edit module | Morgan | `[EM]` |
| Validate agent | Bond | `[VA]` |
| Validate workflow | Wendy | `[VW]` |
| Validate module | Morgan | `[VM]` |
| Rework workflow | Wendy | `[RW]` |

## See Also

- **[Agent Reference](docs/reference/agent-schema.md)** — Agent YAML structure
- **[Workflow Reference](docs/reference/workflow-schema.md)** — Workflow frontmatter and structure
- **[Module Reference](docs/reference/module-yaml.md)** — Module configuration
