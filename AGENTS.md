# AGENTS.md

## Project Overview

**BMad Builder (BMB)** is a meta-module for the BMad Code Platform that helps users create custom AI agents, workflows, and domain-specific modules. It's a documentation-driven project with YAML-based agent/workflow definitions and some minimal Node.js tooling.

## Key Commands

### Development

```bash
npm run docs:dev          # Start Astro dev server (http://localhost:4321)
npm run docs:build        # Build documentation site
npm run docs:preview      # Preview built site
```

### Testing & Validation

```bash
npm test                  # Run full test suite (schemas, refs, lint, format, md)
npm run test:schemas      # Validate agent YAML schemas
npm run test:refs         # Validate internal file references
npm run validate:schemas  # Validate actual agent files against schema
npm run validate:refs     # Check file references (alias for above)
```

### Code Quality

```bash
npm run lint              # ESLint check
npm run lint:fix          # ESLint auto-fix
npm run lint:md           # Markdown lint
npm run format:check      # Prettier check
npm run format:fix        # Prettier format
```

### Release

```bash
npm run release           # Bump patch version and push tag
npm run release:minor     # Bump minor version
npm run release:major     # Bump major version
```

## Architecture

### Source Structure (`src/`)

- **`agents/`** — Agent definitions (`*.agent.yaml`) with persona, menu, and metadata
- **`workflows/`** — Multi-step guided processes organized by type (agent, workflow, module)
  - Each workflow has `steps-c/` (create), `steps-e/` (edit), `steps-v/` (validate)
  - Step-file architecture: JIT loading, sequential execution, state tracking
  - `data/` contains CSV knowledge bases for agents

### Module Structure

```
your-module/
├── src/
│   ├── module.yaml      # Module metadata, install config, variables
│   ├── agents/          # *.agent.yaml files
│   ├── workflows/       # Workflow files with step subdirectories
│   └── tools/           # Optional reusable tools
└── package.json
```

### Build Tools (`tools/`)

- **`build-docs.mjs`** — Consolidates docs, generates LLM-friendly files (`llms.txt`), builds Astro site
- **`validate-file-refs.mjs`** — Validates cross-file references in agents/workflows

### Documentation (`docs/`)

- Diataxis structure: tutorials, how-to, explanation, reference
- Starlight-based site in `website/`
- `_STYLE_GUIDE.md` — Project-specific writing conventions (Google style + Diataxis)

### Skills (`.claude/skills/`)

- BMad OS (Open Source) skills for maintainer workflows
- `bmad-os-add-doc` — Diataxis documentation authoring
- `bmad-os-release-module` — Module release process
- `bmad-os-gh-triage` — GitHub issue triage

## Important Concepts

### Agent YAML Structure

- `agent.metadata` — id, name, title, icon, module
- `agent.persona` — role, identity, communication_style, principles
- `agent.menu` — trigger commands that execute workflows
- `conversational_knowledge` — CSV files loaded at runtime

### Workflow Step Architecture

- Micro-file design: each step is self-contained
- Just-in-time loading: only current step in memory
- Sequential enforcement with state tracking
- Menus halt execution waiting for user input
- Frontmatter defines: name, description, web_bundle, createWorkflow

### Path Variables

- `{project-root}/_bmad/bmb/` — Installation path (in repo, maps to `src/`)
- `{bmad_builder_output_folder}` — User's custom content output
- Runtime variables: `{output_folder}`, `{project-root}` from Core config

## Development Notes

- **Node.js 22+ required** (see `.nvmrc`)
- Module is `default_selected: false` — not auto-installed
- File references in src/ become `_bmad/bmb/` after installation
- All YAML uses double quotes with `avoidEscape: true`
- Website builds to `build/site/` for deployment
- LLM docs have 600k char limit (~150k tokens)

## Publishing

BMad modules are published as npm packages. The module code (`src/`) is what gets installed into user projects via `npx bmad-method install`. The astro website is deployed separately (GitHub Pages via CNAME).
