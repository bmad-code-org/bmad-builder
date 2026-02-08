---
title: "Workflow Schema Reference"
description: Structure and fields for BMad workflow files
---

Complete reference for workflow file structure.

## Workflow File Structure

```
my-workflow/
├── workflow.md              # Entry point and configuration
├── steps/                   # Step files (loaded one at a time)
│   ├── step-01-init.md
│   ├── step-02-process.md
│   └── step-N-complete.md
├── data/                    # Reference materials
└── templates/               # Output templates
```

## Workflow Frontmatter

The `workflow.md` file contains workflow configuration in YAML frontmatter.

```yaml
---
name: my-workflow
description: A brief description of what this workflow does
goal: What the workflow achieves
startup: single-session
output_format: standard
---
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | ✅ Yes | Workflow identifier (kebab-case) |
| `description` | string | ✅ Yes | Short description |
| `goal` | string | ✅ Yes | What the workflow achieves |
| `startup` | string | ⚪ No | `single-session` or `continuable` |
| `output_format` | string | ⚪ No | Output format type |

## Startup Modes

| Mode | Description | When to Use |
|------|-------------|-------------|
| `single-session` | Completes in one sitting | Quick tasks, < 8 steps |
| `continuable` | Can stop and resume | Complex tasks, multiple sessions |

## Output Formats

| Format | Description |
|--------|-------------|
| `standard` | Regular markdown output |
| `minimal` | Minimal output format |
| `custom` | Custom output definition |

## Step Files

Each step is a separate markdown file loaded only when needed.

### Step Frontmatter

```yaml
---
name: step-01-init
description: Initialize the workflow
nextStepFile: './step-02-process.md'
---
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | ✅ Yes | Step identifier |
| `description` | string | ✅ Yes | What this step does |
| `nextStepFile` | string | ⚪ No | Path to next step |

### Step Content

Steps contain:
- **Goal** — What the step accomplishes
- **Instructions** — What the AI should do
- **Output** — What gets produced
- **Menu** — User options (if applicable)

### Step Naming Convention

Use sequential numbering:
- `step-01-init.md`
- `step-02-process.md`
- `step-03-validate.md`
- `step-N-complete.md`

## State Tracking (Continuable Workflows)

Continuable workflows track progress in output file frontmatter:

```yaml
---
stepsCompleted: ['step-01-init', 'step-02-process']
status: IN_PROGRESS
created: 2024-01-15
---
```

| Field | Type | Description |
|-------|------|-------------|
| `stepsCompleted` | array | List of completed step names |
| `status` | string | `IN_PROGRESS` or `COMPLETE` |
| `created` | date | Workflow start date |

## Menu Handling

Workflows can include menus for user interaction:

```markdown
#### Menu Options

**[C] Continue** — Proceed to next step
**[A] Advanced** — Get deeper insights
**[P] Party** — Get multiple perspectives
```

### Menu Rules

- Halt and wait for user input
- Only proceed when user selects continue
- Document the menu options clearly
- Use consistent option letters

## Data Files

Reference materials for workflow context.

```
data/
├── examples.md          # Example workflows
├── standards.md         # Workflow standards
└── reference.md         # Reference information
```

Data files are loaded as needed using variables in step files:

```yaml
---
workflowExamples: '../data/workflow-examples.md'
---
```

## Templates

Output document templates for consistent formatting.

```
templates/
├── output-template.md
└── report-template.md
```

Templates use placeholders for dynamic content:

```markdown
# {title}

Created: {date}

## Summary
{summary}

## Details
{details}
```

## Workflow Variables

Variables reference workflow resources:

| Variable | Resolves To |
|----------|-------------|
| `{project-root}` | Project root directory |
| `{output_folder}` | Configured output folder |
| `{workflow_name}` | Current workflow name |
| `{step_name}` | Current step name |

## Complete Example

### Simple Workflow (workflow.md)

```yaml
---
name: daily-planning
description: Create a daily plan with priorities and time blocks
goal: Create an organized daily plan
startup: single-session
output_format: standard
---

# Daily Planning Workflow

A structured workflow to create your daily plan with priorities and time blocks.
```

### Step File (steps/step-01-init.md)

```yaml
---
name: step-01-init
description: Gather information and set context
nextStepFile: './step-02-priorities.md'
---

# Step 1: Initialize

## Goal
Understand what needs to be planned for today.

## Instructions
Ask the user about:
- Their main objectives for today
- Any fixed commitments (meetings, deadlines)
- Energy levels throughout the day

## Output
Create the daily plan document with gathered information.

#### Menu Options
**[C] Continue** — Proceed to set priorities
```

## Validation Rules

When validating workflows, Wendy checks:

- ✅ Frontmatter contains required fields
- ✅ `name` is valid kebab-case
- ✅ Step files exist and are numbered sequentially
- ✅ `nextStepFile` references are valid
- ✅ Menus are properly formatted
- ✅ Continuable workflows have state tracking

## Best Practices

| Practice | Why |
|----------|-----|
| **One goal per step** | Keeps steps focused and manageable |
| **Number sequentially** | Clear execution order |
| **Load data files as needed** | Just-in-time loading |
| **Update state after each step** | Progress tracking for continuable workflows |
| **Use menus for user choice** | Interactive workflows need user input |

## See Also

- **[Builder Commands](docs/reference/builder-commands.md)** — Workflow commands
- **[Create Your First Workflow](docs/tutorials/create-your-first-workflow.md)** — Workflow creation tutorial
- **[What Are Workflows](docs/explanation/what-are-workflows.md)** — Workflow concepts
