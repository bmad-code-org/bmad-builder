---
title: "Edit Agents and Workflows"
description: Modify existing agents and workflows while maintaining BMad compliance
---

Modify existing agents and workflows using the builder's edit workflows, which help you make changes while maintaining compliance with best practices.

## Before You Begin

- Have an existing agent or workflow you want to modify
- Understand what changes you want to make
- Completed the relevant creation tutorial (agent or workflow)

:::tip[Direct Editing vs Builder Workflows]
You can edit agent and workflow files directly. The edit workflows (`[EA]`, `[EW]`, `[EM]`) provide guided assistance and validation, but aren't required for simple changes.
:::

## Editing Agents

### Using the Edit Agent Workflow

Bond's edit workflow helps you modify agents while maintaining compliance:

```
[EA] or "edit-agent"
```

Bond will guide you through:

| Step | What Happens |
|------|--------------|
| **Load** | Select the agent file to edit |
| **Discover** | Describe what changes you want |
| **Select** | Choose which elements to modify (persona, commands, etc.) |
| **Apply** | Make the changes with validation |
| **Celebrate** | Review and confirm |

### What You Can Edit

| Element | Description |
|---------|-------------|
| **Persona** | Role, identity, communication style, principles |
| **Menu Commands** | Add, remove, or modify commands |
| **Critical Actions** | Autonomous behaviors |
| **Metadata** | Name, description, version |
| **Sidecar** | Expert agent memory files |

### Direct Editing

For simple changes, you can edit the agent YAML file directly:

```yaml
agent:
  metadata:
    name: "My Agent"
    # Edit metadata here

  persona:
    role: "What they do"
    # Edit persona fields here

  menu:
    - trigger: "my-command"
      # Edit commands here
```

After editing, rebuild the agent:

```bash
npx bmad-method build <agent-name>
```

## Editing Workflows

### Using the Edit Workflow Workflow

Wendy's edit workflow helps you modify workflows:

```
[EW] or "edit-workflow"
```

Wendy will guide you through:

| Step | What Happens |
|------|--------------|
| **Assess** | Load and review the existing workflow |
| **Discover** | Describe what changes you want |
| **Select** | Choose which parts to modify (steps, menus, frontmatter) |
| **Apply** | Make the changes |
| **Validate** | Check for compliance issues |

### What You Can Edit

| Element | Description |
|---------|-------------|
| **Frontmatter** | Name, description, goal, startup method |
| **Steps** | Add, remove, or modify step files |
| **Menus** | Change menu options and handlers |
| **Templates** | Update output templates |
| **Data** | Modify reference materials |

### Direct Editing

Workflows are markdown files. You can edit directly:

```markdown
---
name: my-workflow
description: My workflow description
# Edit frontmatter here
---

# Workflow content here
```

After editing, validate your workflow:

```
[VW] or "validate-workflow"
```

## Editing Modules

For module-level changes (configuration, install questions), use Morgan's edit workflow:

```
[EM] or "edit-module"
```

This guides you through:
- Modifying `module.yaml`
- Updating install questions
- Changing configuration values

## Validation After Editing

Always validate after making changes:

| Content Type | Validation Command |
|--------------|-------------------|
| Agents | `[VA]` or `validate-agent` |
| Workflows | `[VW]` or `validate-workflow` |
| Modules | `[VM]` or `validate-module` |

Validation checks for:
- Proper YAML formatting
- Required fields are present
- Compliance with BMad standards
- Menu and command structure

## Common Edit Scenarios

### Adding a Menu Command to an Agent

1. Run `[EA]` or open the agent YAML file
2. Add to the `menu` section:

```yaml
menu:
  - trigger: "new-command"
    exec: "path/to/workflow.md"
    description: "What this command does"
```

3. Rebuild or validate

### Adding a Step to a Workflow

1. Run `[EW]` or open the workflow
2. Create new step file: `step-XX-new-step.md`
3. Update the previous step to load the new step
4. Validate the workflow

### Updating Agent Principles

1. Run `[EA]` or open the agent YAML
2. Modify the `principles` field in persona
3. Rebuild and test the agent

## Tips for Effective Editing

| Tip | Why |
|-----|-----|
| **Validate often** | Catch issues early |
| **Test changes** | Verify behavior matches expectations |
| **Backup first** | Keep a copy before major edits |
| **Iterate** | Make small changes and test |
| **Document** | Note why you made changes |

## Getting Help

- **[Discord Community](https://discord.gg/gk8jAdXWmj)** — Ask in #bmad-method-help
- **[GitHub Issues](https://github.com/bmad-code-org/bmad-builder/issues)** — Report bugs

## Related Guides

- **[Validate Agents and Workflows](docs/how-to/validate-agents-and-workflows.md)** — Quality assurance
- **[Create a Custom Agent](docs/tutorials/create-custom-agent.md)** — Creating agents
- **[Create Your First Workflow](docs/tutorials/create-your-first-workflow.md)** — Creating workflows
