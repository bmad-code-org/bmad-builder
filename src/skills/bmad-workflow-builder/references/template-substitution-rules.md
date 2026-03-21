# Template Substitution Rules

When building the workflow/skill, you MUST apply these conditional blocks to the templates:

## Skill Type Conditionals

### Complex Workflow
- `{if-complex-workflow}` ... `{/if-complex-workflow}` → Keep the content inside
- `{if-simple-workflow}` ... `{/if-simple-workflow}` → Remove the entire block including markers
- `{if-simple-utility}` ... `{/if-simple-utility}` → Remove the entire block including markers

### Simple Workflow
- `{if-complex-workflow}` ... `{/if-complex-workflow}` → Remove the entire block including markers
- `{if-simple-workflow}` ... `{/if-simple-workflow}` → Keep the content inside
- `{if-simple-utility}` ... `{/if-simple-utility}` → Remove the entire block including markers

### Simple Utility
- `{if-complex-workflow}` ... `{/if-complex-workflow}` → Remove the entire block including markers
- `{if-simple-workflow}` ... `{/if-simple-workflow}` → Remove the entire block including markers
- `{if-simple-utility}` ... `{/if-simple-utility}` → Keep the content inside

## Module Conditionals

### For Module-Based Skills
- `{if-module}` ... `{/if-module}` → Keep the content inside
- `{if-standalone}` ... `{/if-standalone}` → Remove the entire block including markers
- `{module-code-or-empty}` → Replace with module code (e.g., `bmb-`)

### For Standalone Skills
- `{if-module}` ... `{/if-module}` → Remove the entire block including markers
- `{if-standalone}` ... `{/if-standalone}` → Keep the content inside
- `{module-code-or-empty}` → Empty string

## bmad-init Conditional

### Uses bmad-init (default)
- `{if-bmad-init}` ... `{/if-bmad-init}` → Keep the content inside

### Opted out of bmad-init (standalone utilities only)
- `{if-bmad-init}` ... `{/if-bmad-init}` → Remove the entire block including markers

## Feature Conditionals

### Headless Mode
- `{if-headless}` ... `{/if-headless}` → Keep if supports headless/autonomous mode, otherwise remove

### Creates Documents
- `{if-creates-docs}` ... `{/if-creates-docs}` → Keep if creates output documents, otherwise remove

### Has Stages (Complex Workflow)
- `{if-stages}` ... `{/if-stages}` → Keep if has numbered stage prompts, otherwise remove

### Has Scripts
- `{if-scripts}` ... `{/if-scripts}` → Keep if has scripts/ directory, otherwise remove

## External Skills
- `{if-external-skills}` ... `{/if-external-skills}` → Keep if skill uses external skills, otherwise remove
- `{external-skills-list}` → Replace with bulleted list of exact skill names:
  ```markdown
  - `bmad-skill-name` — Description
  ```

## Frontmatter Placeholders

Replace all frontmatter placeholders:
- `{module-code-or-empty}` → Module code prefix (e.g., `bmb-`) or empty
- `{skill-name}` → Skill functional name (kebab-case)
- `{skill-description}` → Full description with trigger phrases
- `{role-guidance}` → Brief role/expertise statement

## Content Placeholders

Replace all content placeholders with skill-specific values:
- `{overview-template}` → Overview paragraph following 3-part formula (What, How, Why/Outcome)
- `{stage-N-name}` → Name of numbered stage
- `{stage-N-purpose}` → Purpose description of numbered stage
- `{progression-condition}` → When this stage completes

## Path References

All generated skills use these paths:
- `references/{reference}.md` — Reference documents loaded on demand
- `01-{stage}.md` — Numbered stage prompts at skill root (complex workflows)
- `scripts/` — Python/shell scripts for deterministic operations (if needed)
