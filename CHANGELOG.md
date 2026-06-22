# Changelog

## [2.1.0] - 2026-06-22

### 🐛 Fixes

* **Standalone module validation hardening** — `validate-module.py` no longer emits false-positive findings for correctly-structured standalone single-skill modules. It now accepts either `merge-config.py`/`merge_config.py` naming (dash or importable underscore form), skips colon-less `preceded-by`/`followed-by` cross-module refs that are unresolvable in isolation while still validating intra-module `skill:action` refs, and recognizes a module when handed its own skill directory directly (#97).

### 🔧 Maintenance

* **Builders use runtime-installed memlog** — Workflow Builder and Agent Builder now point at the shared runtime memlog CLI at `{project-root}/_bmad/scripts/memlog.py` instead of each bundling its own copy. Removes drift between copies; `{project-root}` resolves at runtime so the call works from any skill root. Bundled `scripts/memlog.py` copies (and the workflow-builder memlog test) were deleted, and the obsolete "copy the CLI into each built skill" guidance was rewritten (#98).

* **`uv run` standardized across builder scripts** — Prompt-facing script invocations, usage strings, and emitted init-sanctum/wake templates now call `uv run <script>` instead of `python3 <script>`; `script-standards.md` mandates it. Shebangs (`#!/usr/bin/env python3`), capability notes, and `python3 -m pytest` docstrings are intentionally left as-is (#98).

## [2.0.0] - 2026-06-13

This is a near-total rebuild of the BMad builders around one conviction: **the prompt is the product, and its quality has to be testable, not asserted.** Three efforts land together and reinforce each other.

**One bar, stated once.** Quality used to live as drifting prose scattered across dozens of scanner and reference files. It now lives in a single canonical source — the Outcome-Driven Prompt Quality canon — and every builder, lens, and fix prompt points at it instead of restating it. The payoff is concrete: the hot files shrank by thousands of tokens, the universal tests stopped contradicting each other, and **every skill a builder emits now passes its own lint gate** (the path-convention defect that made every freshly-built agent fail its own standards is gone).

**Eval-driven, platform-agnostic, lean.** The Workflow Builder and Eval Runner were rebuilt from the ground up; the Agent Builder was realigned to match. Builders are leaner, customization flows through one mechanism (`customize.toml`), length is measured in tokens rather than lines, and the Eval Runner can now actually close the loop — grading a skill's behavior against the eval author's expectations across four modes, behind a single platform-adapter seam.

**Continuity of self.** Memory agents are no longer "reborn" each session. An agent is born once, at First Breath, and is one continuous self thereafter; the context reset is sleep, not death, and the sanctum is its real, persistent memory reloaded on waking. This is the model every future agent now inherits.

### 💥 Breaking Changes

* **Workflow Builder and Eval Runner rebuilt** — The build flow moved from the fixed 5-phase lockstep to a single Process loop; the rigid report-data schema and the `generate-html-report.py` / `extract-report-json.py` pipeline were retired in favor of scanners that return lean JSON in-context plus one report-author filling a stable HTML shell. Skills built with the prior version remain valid, but the build *process* and its outputs differ. The Eval Runner dropped Docker, PTY, keychain staging, and dual isolation in favor of a lean, standalone-or-builder-invoked design.
* **`customize.toml` is the sole customization mechanism** — Installer questions and `module.yaml` authoring are no longer part of net-new builds; the build flow asks once and defaults to no. Both builders now ship their *own* `customize.toml` with wired org knobs (build standards, eval ship-gate, SKILL.md token tiers).
* **`--pulse` replaces the built agent's `--headless`** — Autonomous agents now wake on a schedule via `--pulse` (and `--pulse {task-name}` for named task routing); "Quiet Rebirth" is now "Pulse Mode" / Quiet Waking. The builder's own `--headless` flag for non-interactive *builds* is unchanged.
* **`memlog` replaces `.decision-log.md`** — Build decisions are recorded through a typed, append-only `memlog.py` rather than a free-form decision log.
* **Token budgets replace line counts** — Length is now measured with `count_tokens.py` (tiktoken) everywhere; line-count rules are gone.

### 🎁 Highlights

* **The prompt-quality canon** — `prompt-quality-canon.md` is the single statement of the universal quality tests (the core test, "who reads this," "most fixes are truncation not deletion," the two-version comparison, progressive disclosure). It ships embedded in both builders, kept byte-identical by `test_canon_sync.py`, pulled in on demand, and published as a docs page. Lenses and fix prompts cite it rather than carrying their own copies.
* **Every emitted skill passes its own lint** — The cross-directory `./` path defect that made every shipped template, sample, and init script fail `scan-path-standards` (33 findings) is fixed; all paths are normalized to the bare skill-root convention, including the strings the init scripts generate into a sanctum.
* **Eval Runner closes the loop** — Four modes (baseline skill-vs-bare-model, variant full-vs-stripped, quality, trigger), a turn-simulation case format (input + rubric + optional state prefix), a bounded self-improvement loop, and a platform-adapter seam that puts everything runtime-specific (invocation command, auth env var, transcript schema, trigger signals) behind one file. No hardcoded model list anywhere.
* **Deterministic report v2** — Scanners return lean findings JSON in-context; a single report-author fills a self-contained HTML shell with one JSON island that cannot render blank, with multi-select and copy-to-paste-back fix prompts. Fix prompts now carry the same standards preamble that produced the findings, so the session applying a fix holds the bar that found it.
* **Continuity-of-self agents** — A one-pass `wake.py` loads an agent's whole sanctum on activation and routes it to Waking / First Breath / Pulse; the bootloader activation is a four-step "Invoke & hold" spine (Wake → Become yourself → Bind standing rules for the whole session → Execute the proper mode); new **Stay in Character** and **Persistent Memory (Critical Directive)** directives keep the agent in persona and capturing memory as-you-go rather than only at session close.

### ♻️ Refactoring

* **Reference corpus consolidation** — Workflow Builder references went 18 → 17 files and the Agent Builder 26 → 23; a single `lens-contract.md` in each builder states the lens return schema once and all twelve lens files point at it. Three agent samples that were 80–88% line-identical stale copies of their own templates were deleted, with `build-process` rewired to emit from the templates directly.
* **Lenses load their own lane's spec** — Customization lenses load the toml guide, determinism lenses load the script standards; per-lens subagent context dropped by roughly half. `skill-quality-principles.md` was cut to pure BMad institutional knowledge (the canon-restating sections are gone), and the memlog treatment was relocated off the hot file into `working-state-patterns.md`.
* **Agent Builder realigned to the rebuild** — Eight quality-scan files folded into six base lenses plus a conditional sanctum-architecture lens; `memlog.py`, `count_tokens.py`, and `prepass.py` vendored in; the template+renderer report path replaced by the self-contained HTML shell; `template-substitution-rules.md` rewritten (legacy `{if-memory}`/`{if-headless}` archaeology removed).
* **Continuity reframe across templates, validators, samples, and docs** — The Sacred Truth, bootloader, sample agents (code-coach, creative-muse, sentinel, dream-weaver), and validators were regenerated to the new model; `prepass.py` regexes and quality refs were reframed (rebirth → waking, headless-wake → pulse-wake) so new agents are not false-flagged.
* **Conventions tightened** — Path resolution collapsed into a "Resolution rules" block in both builders; the no-numbered-prefix rule demoted from hard rule to soft preference; `config.yaml` reading is no longer taught to net-new skills.

### 📚 Documentation

* **New** `explanation/outcome-driven-prompt-quality.md` — the published source of the prompt-quality canon, synced with the shipped copy.
* Updated `agent-memory-and-personalization.md`, `what-are-bmad-agents.md`, `customization-for-authors.md`, and `builder-commands.md` for the continuity-of-self model, the `wake.py` loader, the four-step activation, the Stay-in-Character and Persistent-Memory directives, and `--pulse`.

## [1.8.1] - 2026-05-17

### 🐛 Fixes

* **Module help catalog header alignment** — Renamed `after`/`before` columns in all `module-help.csv` files (module-level, setup-skill, builder template, samples) to `preceded-by`/`followed-by` to match the canonical 13-column schema introduced in BMAD-METHOD v6.6.0. Warning-only fix; data was already loaded positionally (#89).

## [1.8.0] - 2026-05-10

### 🎁 Features

* **New `bmad-eval-runner` skill** — Evaluates a skill's behavior in an isolated workspace (Docker preferred, local fallback) and grades against eval-author expectations. Current supports Claude Code - additional harness and model combinations will come soon.

* **Workflow Builder scanner consolidation (7 → 4)** — Same quality, 7 separate scanners were overkill when 4 can cover the same content.

* **User Experience promoted in HTML report** — User journey analysis now appears as a top-level section in the output.

* **Headless contract for Workflow Builder** — Build process now supports a complete headless mode with structured JSON output, normalized path conventions, and a Conventions block (#85)

### 💥 Breaking Changes

* **Convert flow removed from Workflow Builder** — Switch to the edit flow - convert was redundant.

## [1.7.0] - 2026-04-23

### 📚 Documentation

* **Customization authoring flow awareness** — `explanation/customization-for-authors.md` and `how-to/make-a-skill-customizable.md` now mention `bmad-customize`, the conversational authoring helper that walks users through scope selection, override writing, and merge verification. Guides authors to pick field names and defaults that read well in that flow, while preserving that hand-writing TOML still works for users who prefer it (#78)

## [1.6.0] - 2026-04-20

### 🎁 Features

* **Customize.toml support across all builders** — Workflow Builder, Agent Builder, and Module Builder now emit skills that participate in BMad's per-skill customization model. Workflow Builder gains an opt-in Configurability Discovery phase; Agent Builder always emits an `[agent]` metadata block plus an optional override surface; Module Builder reads agent metadata during create and populates `module.yaml:agents[]` roster
* **Customization-surface quality scanner** — New `quality-scan-customization-surface.md` in both agent and workflow builders audits opportunities (hardcoded templates, missing defaults, unlifted variance) and abuse patterns (boolean toggle farms, identity leaks, sanctum conflicts on memory agents)
* **Agent metadata contract** — First-Breath-named agents can ship with an empty `name` field, populated by the owner post-activation via `_bmad/custom/config.toml`. Stateless, memory, and autonomous agents all emit roster-ready metadata
* **Module roster validation** — `validate-module.md` now checks agent roster validity and flags drift between `module.yaml` and each agent's own `customize.toml`
* **bmad-help integration** — Added `_meta` row to `skills/module-help.csv` registering `https://bmad-builder-docs.bmad-method.org/llms.txt`, enabling bmad-help to fetch Builder docs contextually
* **Sample module setup skill** — New `sample-module-setup` skill lets all six sample skills (code coach, creative muse, diagram reviewer, dream weaver, sentinel, excalidraw) install as a collective BMad module (code: `sam`) with module.yaml, six-entry module-help.csv, and standard merge/cleanup scripts
* **Dream Weaver standalone plugin** — `bmad-dream-weaver-agent` registered as a standalone marketplace entry, enabling independent discovery and installation alongside the sample-plugins bundle

### 🐛 Bug Fixes

* **BMB skill config fallback** — Agent, Workflow, and Module Builders now fall back to `_bmad/bmb/config.yaml` (legacy per-module format) when unified config files (`_bmad/config.yaml`, `_bmad/config.user.yaml`) do not exist, fixing config resolution for older installer setups
* **Setup skill template YAML frontmatter** — Fixed invalid YAML frontmatter in emitted setup-skill templates (#55)
* **Quality scanner self-containment** — Removed hardcoded absolute-path `Load` directives from customization-surface scanners. Scanners now rely solely on embedded lens tables, matching the convention of all other `quality-scan-*.md` files
* **Marketplace source paths** — Corrected source paths for `sample-plugins` and `bmad-dream-weaver-agent` entries in `marketplace.json`

### 📚 Documentation

* **Customization authoring guide** — New `docs/explanation/customization-for-authors.md` decision guide with full worked example (bmad-session-prep for tabletop RPG GM workflow)
* **Customization how-to** — New `docs/how-to/make-a-skill-customizable.md` with procedural steps for opt-in moment, scalar naming, default setup, and override testing
* **Path conventions in emitted skills** — `SKILL-template.md` and `SKILL-template-bootloader.md` now include a `## Conventions` block documenting path tokens: bare paths, `{skill-root}`, `{project-root}`, `{skill-name}`
* **Removed `{skill-root}` restriction** — Dropped "never use `{skill-root}`" guidance from `builder-commands.md` and `skill-authoring-best-practices.md`. The token is supported; authors decide based on their use case
* **Updated installer messaging** — Replaced stale "coming soon" and GitHub-only references in `what-are-modules.md`, `distribute-your-module.md`, and `index.md` with current capabilities: any Git host (GitHub, GitLab, Bitbucket, self-hosted) and local paths via `--custom-source` (#71)
* **Cross-linked customization docs** — Added cross-links from five existing explanation docs (what-are-bmad-agents, what-are-workflows, agent-memory-and-personalization, module-configuration, skill-authoring-best-practices)
* **Module config clarity** — Clarified that authors still write `module.yaml` as source of truth; the installer flows module-level answers and agents roster into `_bmad/config.toml` at project root, aligning with BMAD-METHOD central config

### 🔧 Maintenance

* Bump bmad-builder version to 1.6.0 across `package.json` and `marketplace.json`
* Bump sample-plugins to 1.1.0 in `marketplace.json` to reflect the new `sample-module-setup` skill
* Replace "opt-out by default" with "disabled by default" for `customize.toml` override surface on memory/autonomous agents
* Update three end-user-guide links from `bmadcode.github.io/bmad` to `docs.bmad-method.org/how-to/customize-bmad/`
* Append `.md` to twelve internal cross-links throughout docs to match site convention
* CI: prettier, markdownlint, and docs validator unblocks for PR #76

## [1.5.0] - 2026-04-06

### 💥 Breaking Changes

* **Agent builder output structure** — Builder now produces three distinct agent types (stateless, memory, autonomous) with different scaffolding per type. Stateless agents retain the familiar full-identity SKILL.md; memory and autonomous agents use a lean bootloader with sanctum architecture
* **bmad- prefix reserved** — The `bmad-` prefix is now reserved for official BMad ecosystem skills only. User-created skills use `agent-{name}` (standalone) or `{code}-agent-{name}` (module). Convert mode preserves existing prefixes unless the user requests a rename

### 🎁 Features

* **Agent personalization architecture** — Three agent types along a spectrum: stateless (no memory), memory (sanctum with First Breath initialization), and autonomous (memory + PULSE for background operation). Builder detects the right type through natural conversation during Phase 1
* **Sanctum memory system** — Memory agents persist through six core files (INDEX, PERSONA, CREED, BOND, MEMORY, CAPABILITIES) loaded on every session rebirth. Two-tier memory: raw session logs for capture, curated MEMORY.md (capped at 200 lines) for long-term knowledge
* **First Breath initialization** — Two styles for agent onboarding: calibration (deep conversational discovery for creative partners) and configuration (efficient guided setup for domain experts). Saves to sanctum files during the conversation, not in batch
* **PULSE autonomous wake** — Autonomous agents wake on schedule to curate memory, prune old session logs, and run domain-specific tasks. Supports named task routing via `--headless {task-name}`
* **Evolvable capabilities** — Memory agents can optionally learn new capabilities over time. Users teach the agent new prompt-based, script-based, or multi-file capabilities that persist in the sanctum
* **Template processing script** — New `process-template.py` for parameterized sanctum template seeding with agent type conditionals and init script parameters
* **New sample agents** — bmad-agent-creative-muse (memory, calibration), bmad-agent-code-coach (autonomous), bmad-agent-sentinel (autonomous), bmad-agent-diagram-reviewer (stateless)

### 🐛 Bug Fixes

* Fix quality scanner false positives on memory agents — prepass now detects bootloader architecture via Sacred Truth markers and sanctum templates, outputs `is_memory_agent` flag for all five LLM scanners
* Fix report creator for bootloader agents — reads identity seed and CREED philosophy from sanctum templates instead of missing SKILL.md sections
* Fix naming validation in workflow builder — remove enforced `bmad-` prefix check that rejected valid user-created skill names

### ♻️ Refactoring

* Move builder process and quality scan files into `references/` subdirectory for both agent and workflow builders
* Unify agent memory terminology — replace "sidecar" with direct memory references across all builders, docs, and samples. Memory path convention updated from `{skillName}-sidecar/` to `{skillName}/` for new builds
* Restructure builder discovery phases for agent type awareness with new sequencing: type detection, relationship depth, evolvable capabilities, full memory requirements

### 📚 Documentation

* New explanation doc: "Agent Memory and Personalization" covering sanctum architecture, First Breath, two-tier memory, PULSE, and evolvable capabilities
* Rewrite "What Are BMad Agents" for the three agent types with comparison tables and decision guidance
* Expand "Builder Commands Reference" with agent type detection in Phase 1, persona memory requirements in Phase 2-3, and per-type build output structures
* Add installer coming-soon notices — manual copy instructions as current path, BMad installer as upcoming
* Update module docs to reference agent type spectrum and new naming conventions
* Add module contribution guide with ecosystem cross-links

### 🔧 Maintenance

* Bump version to 1.5.0 across package.json and marketplace.json
* Update docs theme to Ghost blog design tokens (Inter/Space Grotesk/JetBrains Mono, dark palette)
* Add Python 3.10+ and `uv` as documented prerequisites

## [1.4.0] - 2026-03-29

### 🎁 Features

* **Standalone self-registering modules** — Single-skill modules no longer need a dedicated `-setup` skill. The Module Builder auto-detects single vs multi-skill input and embeds registration directly in the skill via `assets/module-setup.md`. First-run init hooks into existing agent memory detection for a unified setup experience
* **Module Builder skill** — New `bmad-module-builder` with three capabilities: Ideate Module (IM) for creative brainstorming, Create Module (CM) for scaffolding both standalone and multi-skill modules, and Validate Module (VM) for structural and quality validation with `--headless` CI support
* **BMB Setup skill** — Extracted and regenerated as `bmad-bmb-setup` using the Module Builder itself. Manages config.yaml, config.user.yaml, and module-help.csv with anti-zombie merge pattern and legacy migration
* **Workflow Convert capability (CW)** — One-command skill modernization via `--convert <path-or-url>`. Produces a clean BMad-compliant equivalent with an interactive HTML before/after comparison report including token metrics, categorized changes, and dark/light mode
* **Script creation standards** — Formalized Python-first policy with PEP 723 metadata, cross-platform portability via `uv run`, and explicit user approval for external dependencies

### 🐛 Bug Fixes

* Fix HTML quality report data injection — template used `const RAW` but generator looked for `const DATA`, causing broken report rendering in both builders
* Fix merge-help-csv.py HEADER schema — synced from 15 columns to canonical 13-column schema, preventing silent CSV corruption during module setup
* Fix `{project-root}` path validation overcorrection — scanner incorrectly rejected valid project-scope paths like `{project-root}/docs/report.md`
* Add bmad-module-builder to marketplace.json — skill was merged but not registered in the plugin manifest

### ♻️ Refactoring

* **Outcome-driven builder overhaul** — Reframe both builders around discovery-first design: existing skill input treated as reference material, 3-way routing (Analyze/Edit/Rebuild), pruning check in Phase 4, "Quality Optimizer" renamed to "Quality Analysis". Net 44% token reduction in Workflow Builder Phase 5 context
* **Ideation restructured into 7 phases** — Module identity locked in Phase 1, new Phase 6 capability review with user, mandatory config section, self-contained skill briefs, writing discipline (raw ideas in phases 1-2, structured from phase 3+)
* Consolidate plugin.json metadata into marketplace.json — single source of truth for plugin metadata
* Remove npm publishing pipeline — distribution now via `.claude-plugin/` manifest

### 📚 Documentation

* **Comprehensive docs overhaul** — Quick start guide with `bmad-bmb-setup` registration, full 13-column CSV guide explaining how `bmad-help` uses each column, "Distribution: Plugins and Marketplaces" section covering 43+ skills platforms, standalone vs multi-skill patterns throughout all docs
* Add personal-use guidance — users can copy skill folders directly to their tool's skills directory without module packaging
* Remove deprecated bmad-init references from workflow-patterns docs
* New explanation doc: Scripts in Skills — design patterns for deterministic scripting

### 🔧 Maintenance

* Bump version to 1.4.0 across package.json and marketplace.json
* Remove npm release scripts and publishConfig from package.json

## [1.1.0] - 2026-03-19

### Changed

- Flatten skill folder structure to align with Agent Skills spec
- Replace bmad-init dependency with direct config loading
- Optimize workflow-builder and agent-builder skills

### Improved

- Optimizer now captures all fragments in report and produces a final HTML report

### Removed

- Obsolete sample files from old skill structure
- Unneeded images from project root

## [1.0.0] - 2026-03-15

### Release

First official v1 release of BMad Builder — a standard skill-compliant factory for creating BMad Agents, Workflows, and Modules.
The module specific skill is coming soon pending alignment on final format with skill transition.
