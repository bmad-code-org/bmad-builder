# Quality Dimensions — Quick Reference

Six dimensions to keep in mind when building skills. The quality scanners check these automatically during optimization — this is a mental checklist for the build phase.

## 1. Informed Autonomy

The executing agent needs enough context to make judgment calls when situations don't match the script. The Overview section establishes this: domain framing, theory of mind, design rationale.

- Simple utilities need minimal context — input/output is self-explanatory
- Interactive/complex workflows need domain understanding, user perspective, and rationale for non-obvious choices
- When in doubt, explain *why* — an agent that understands the mission improvises better than one following blind steps

## 2. Intelligence Placement

Scripts handle plumbing (fetch, transform, validate). Prompts handle judgment (interpret, classify, decide).

**Test:** If a script contains an `if` that decides what content *means*, intelligence has leaked.

**Reverse test:** If a prompt validates structure, counts items, parses known formats, compares against schemas, or checks file existence — determinism has leaked into the LLM. That work belongs in a script. Scripts have access to full bash, Python with standard library plus PEP 723 dependencies, and system tools — think broadly about what can be offloaded.

## 3. Progressive Disclosure

SKILL.md stays focused. Detail goes where it belongs.

- Stage instructions → `./references/`
- Reference data, schemas, large tables → `./references/`
- Templates, config files → `./assets/`
- Multi-branch SKILL.md under ~250 lines: fine as-is
- Single-purpose up to ~500 lines: acceptable if focused

## 4. Description Format

Two parts: `[5-8 word summary]. [Use when user says 'X' or 'Y'.]`

Default to conservative triggering. See `./references/standard-fields.md` for full format and examples.

## 5. Path Construction

Only use `{project-root}` for `_bmad` paths. Config variables used directly — they already contain `{project-root}`.

See `./references/standard-fields.md` for correct/incorrect patterns.

## 6. Token Efficiency

Remove genuine waste (repetition, defensive padding, meta-explanation). Preserve context that enables judgment (domain framing, theory of mind, design rationale). These are different things — the prompt-craft scanner distinguishes between them.
