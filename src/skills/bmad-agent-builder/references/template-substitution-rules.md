# Template Substitution Rules

When building the agent, you MUST apply these conditional blocks to the templates:

## For Module-Based Agents

- `{if-module}` ... `{/if-module}` → Keep the content inside
- `{if-standalone}` ... `{/if-standalone}` → Remove the entire block including markers
- `{custom-config-properties}` → Replace with comma-separated custom property names (e.g., `journal_folder, adventure_logs_folder`) or remove line if none
- `{module-code-or-empty}` → Replace with module code (e.g., `cis-`) or empty string for standalone

## For Standalone Agents

- `{if-module}` ... `{/if-module}` → Remove the entire block including markers
- `{if-standalone}` ... `{/if-standalone}` → Keep the content inside
- `{custom-config-properties}` → Remove (not used for standalone)
- `{module-code-or-empty}` → Empty string
- `{custom-init-questions}` → Add user's additional questions here (remove placeholder if none)

## For Agents With Sidecar (Memory)

- `{if-sidecar}` ... `{/if-sidecar}` → Keep the content inside
- `{if-no-sidecar}` ... `{/if-no-sidecar}` → Remove the entire block including markers

## For Agents Without Sidecar

- `{if-sidecar}` ... `{/if-sidecar}` → Remove the entire block including markers
- `{if-no-sidecar}` ... `{/if-no-sidecar}` → Keep the content inside

## External Skills

- `{if-external-skills}` ... `{/if-external-skills}` → Keep if agent uses external skills, otherwise remove entire block
- `{external-skills-list}` → Replace with bulleted list of exact skill names:
  ```markdown
  - `bmad-skill-name-one` — Description
  - `bmad-skill-name-two` — Description
  ```

## Custom Init Questions

Add user's additional questions to the init.md template, replacing `{custom-init-questions}` placeholder. Remove the placeholder line if no custom questions.

## Path References

All generated agents use these paths:
- `init.md` — First-run setup
- `{name}.md` — Individual capability prompts
- `references/memory-system.md` — Memory discipline (if sidecar needed)
- `scripts/` — Python/shell scripts for deterministic operations (if needed)

## Frontmatter Placeholders

Replace all frontmatter placeholders in SKILL-template.md:
- `{module-code-or-empty}` → Module code (e.g., `cis-`) or empty
- `{agent-name}` → Agent functional name (kebab-case)
- `{short phrase what agent does}` → One-line description
- `{displayName}` → Friendly name
- `{title}` → Role title
- `{role}` → Functional role
- `{skillName}` → Full skill name with module prefix
- `{user_name}` → From config
- `{communication_language}` → From config

## Content Placeholders

Replace all content placeholders with agent-specific values:
- `{overview-template}` → Overview paragraph (2-3 sentences) following the 3-part formula (What, How, Why/Outcome)
- `{One-sentence identity.}` → Brief identity statement
- `{Who is this agent? One clear sentence.}` → Identity description
- `{How does this agent communicate? Be specific with examples.}` → Communication style
- `{Guiding principle 1/2/3}` → Agent's principles
