---
title: "Validate Agents and Workflows"
description: Check existing agents and workflows for BMad compliance and best practices
---

Validate your agents and workflows to ensure they follow best practices and comply with standards.

## Why Validate

Validation catches issues before they cause problems:

| Benefit | Example |
|---------|---------|
| **Catch errors** | Missing required fields, invalid YAML |
| **Best practices** | Menu structure, persona quality |
| **Compliance** | BMad Core standards |
| **Performance** | Optimized structure |

:::note[When to Validate]
Validate after creating, editing, or updating any agent or workflow. Also validate before publishing modules.
:::

## Validating Agents

Use Bond's validation workflow:

```
[VA] or "validate-agent"
```

### What Bond Checks

| Category | Checks |
|----------|--------|
| **Metadata** | Name, description, module, path correctness |
| **Persona** | Role, identity, communication style, principles present |
| **Menu** | Triggers formatted correctly, commands valid |
| **Structure** | YAML valid, required fields present |
| **Compliance** | BMad Core standards followed |

### Validation Output

Bond provides a detailed report:

```
✅ PASSED: Agent structure is valid
✅ PASSED: Persona is complete
⚠️ WARNING: Principles could be more specific
❌ FAILED: Menu trigger has invalid characters
```

### Fixing Issues

After validation, Bond offers to fix issues:

- **[A] Apply fixes** — Automatically correct what Bond can
- **[M] Manual review** — See what needs manual fixing
- **[R] Revalidate** — Run validation again after fixes

## Validating Workflows

Use Wendy's validation workflow:

```
[VW] or "validate-workflow"
```

### What Wendy Checks

| Category | Checks |
|----------|--------|
| **Frontmatter** | Name, description, goal, startup complete |
| **Structure** | Workflow.md, step files, templates present |
| **Menus** | Menu handling, options, triggers valid |
| **Steps** | Sequential ordering, nextStep references correct |
| **Output format** | Output configuration valid |
| **Cohesiveness** | Steps connect logically |

### Validation Output

Wendy provides a comprehensive report:

```
✅ PASSED: Frontmatter is complete
✅ PASSED: Step sequence is valid
⚠️ WARNING: step-03 has no nextStep defined
❌ FAILED: step-02 references non-existent step
```

### Max-Parallel Validation

For high-capability LLMs (like Claude) that support extensive parallel processing:

```
[MV] or "validate-max-parallel-workflow"
```

This hyper-optimized validation uses task agents to validate multiple workflow aspects simultaneously in sub-processes for dramatically faster results.

## Validating Modules

Use Morgan's validation workflow:

```
[VM] or "validate-module"
```

### What Morgan Checks

| Category | Checks |
|----------|--------|
| **module.yaml** | Metadata, install questions, config valid |
| **Structure** | Agents, workflows, tools folders present |
| **Agents** | All agent files valid |
| **Workflows** | All workflow files valid |
| **Package** | package.json configured correctly |

## Common Validation Issues

### Agent Issues

| Issue | Fix |
|-------|-----|
| **Missing persona fields** | Add role, identity, communication style, principles |
| **Invalid menu triggers** | Use kebab-case, no spaces, no special chars |
| **Empty principles** | Add at least 2-3 meaningful principles |
| **Missing metadata** | Add name, description, module |

### Workflow Issues

| Issue | Fix |
|-------|-----|
| **Incomplete frontmatter** | Add all required fields (name, description, goal) |
| **Broken step references** | Ensure nextStep files exist |
| **Missing menus** | Add menu where workflow requires user choice |
| **Invalid output format** | Specify correct output format in frontmatter |

### Module Issues

| Issue | Fix |
|-------|-----|
| **Invalid module.yaml** | Check YAML syntax, required fields |
| **Missing install questions** | Add at least one install question or mark optional |
| **Package.json errors** | Add name, version, description |
| **Folder structure** | Ensure src/ folder with proper structure |

## Validation Workflow

Recommended validation process:

1. **Create** your agent/workflow/module
2. **Validate** immediately after creation
3. **Fix** any issues found
4. **Revalidate** to confirm fixes
5. **Test** by actually using the agent/workflow
6. **Validate again** before publishing

## Tips for Passing Validation

| Tip | How |
|-----|-----|
| **Follow templates** | Use existing agents/workflows as examples |
| **Use the builders** | Bond, Wendy, Morgan create compliant content |
| **Read error messages** | Validation tells you exactly what's wrong |
| **Fix incrementally** | Address one issue at a time, revalidate |
| **Test thoroughly** | Validation checks structure, not behavior |

## Getting Help

If validation fails and you're not sure why:

- **[Discord Community](https://discord.gg/gk8jAdXWmj)** — Ask in #bmad-method-help
- **[GitHub Issues](https://github.com/bmad-code-org/bmad-builder/issues)** — Report suspected bugs
- **[Reference Examples](https://github.com/bmad-code-org/BMAD-METHOD)** — Study valid examples

## Related Guides

- **[Edit Agents and Workflows](docs/how-to/edit-agents-and-workflows.md)** — Fixing validation issues
- **[Create a Custom Agent](docs/tutorials/create-custom-agent.md)** — Agent creation
- **[Create Your First Workflow](docs/tutorials/create-your-first-workflow.md)** — Workflow creation
