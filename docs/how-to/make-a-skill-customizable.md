---
title: 'How to Make a Skill Customizable'
description: Opt your skill into end-user customization during the build, name your scalars well, and test an override
---

This guide walks through opting a skill into end-user customization during a build. You'll hit the opt-in moment in the builder, pick names for the scalars you expose, and verify an override actually fires. Read [Customization for Authors](/explanation/customization-for-authors.md) first if you haven't decided whether to opt in.

Keep in mind that your users won't typically hand-write the override files you're enabling. The `bmad-customize` skill in BMad core walks them through authoring overrides conversationally. The names and defaults you pick here are what a user is walked through in that conversation, so pick scalar names that read well out loud.

## When to Use This

- You're building a workflow or stateless agent and want to let teams/org users inject overrides
- You're adding configurability to an existing skill during a rebuild
- You want a swappable template path, output destination, or hook in your skill

## When to Skip This

- Your skill is a single-purpose utility users will invoke and forget (overriding makes no sense)
- You're building a memory or autonomous agent whose behavior lives in the sanctum (the sanctum is already the customization surface)
- You haven't decided yet whether you need customization (read the [author guide](/explanation/customization-for-authors.md) first)

:::note[Prerequisites]

- The Agent Builder or Workflow Builder is available in your project
- You've sketched what your skill does and roughly what stages or capabilities it has
- You've read the [author guide](/explanation/customization-for-authors.md) and know which knobs you want to expose
:::

## Steps

### 1. Answer "Yes" to the Opt-In Question

During the build, both builders ask a version of:

> Should this skill support end-user customization (activation hooks, swappable templates, output paths)? If no, it ships fixed. Users who need changes fork it.

Answer **yes** when you want overrides supported. The builder records this as `{customizable} = yes` and routes to the Configurability Discovery phase.

If you're running headless (`--headless` or `-H`), pass `--customizable` to opt in. The headless default is **no**.

### 2. Walk Through Configurability Discovery

The builder proposes candidates auto-detected from your skill design and asks which should be exposed. Typical candidates:

- **Templates** the skill loads (strongest case)
- **Output destination paths** if the skill writes artifacts
- **`on_<event>` hooks** (prompts or commands executed at lifecycle points)
- **Additional persistent facts** beyond the default `project-context.md` glob

For each candidate you accept, the builder asks for a name and a default value.

### 3. Name Your Scalars Well

Use the suffix conventions below so a user can tell what a scalar does from its name alone.

| Pattern | Use for | Example |
| --- | --- | --- |
| `<purpose>_template` | File paths for templates the skill loads | `brief_template = "resources/brief.md"` |
| `<purpose>_output_path` | Writable destinations | `report_output_path = "{project-root}/docs/reports"` |
| `on_<event>` | Hook scalars | `on_complete = ""` |

Specific names like `brief_template` tell the user exactly what the knob does. Vague names like `style_config` or `format_options` force the user to read your SKILL.md to figure it out.

### 4. Set Good Defaults

Every scalar you expose needs a default that works on first run. Bare paths resolve from the skill root. Use `{project-root}/...` when the default lives somewhere in the user's project.

```toml
[workflow]
brief_template = "resources/brief-template.md"   # ships inside the skill
on_complete = ""                                  # no default post-hook
persistent_facts = [
  "file:{project-root}/**/project-context.md",    # glob into the user's project
]
```

For arrays of tables (menus, capability rosters), give every item a `code` or `id` field so the resolver can merge by key:

```toml
[[agent.menu]]
code = "BR"
description = "Run a brainstorm"
skill = "bmad-brainstorming"
```

Without a `code` or `id` on every item, the array falls back to append-only merging. That's rarely what users actually want.

### 5. Wire `{workflow.X}` or `{agent.X}` References in SKILL.md

The builder does this automatically during emission, but know what's happening: instead of hardcoding `resources/brief-template.md` in your SKILL.md body, the relevant step becomes:

```markdown
Load the brief template from `{workflow.brief_template}`.
```

At runtime, the resolver swaps in whatever the merged scalar is (default, team override, or user override).

### 6. Test an Override

After the skill is built, verify overrides work. In the project where you're testing:

```bash
mkdir -p _bmad/custom
cat > _bmad/custom/{skill-name}.toml <<'EOF'
[workflow]
on_complete = "Print the word CUSTOMIZED to stdout."
EOF
```

Run the resolver directly to confirm your override takes effect:

```bash
python3 _bmad/scripts/resolve_customization.py \
  --skill /path/to/built/skill \
  --key workflow.on_complete
```

Output should be `"Print the word CUSTOMIZED to stdout."`. If you see the default, check that your TOML filename matches the skill directory basename exactly and that the `[workflow]` (or `[agent]`) block header is present.

Then invoke the skill and confirm the customized behavior fires at the expected lifecycle point.

## What You Get

When you opt in, your built skill folder includes:

```text
{skill-name}/
├── SKILL.md            # references {workflow.X} or {agent.X} for customized values
├── customize.toml      # your defaults, the canonical schema
├── references/
├── scripts/
└── assets/
```

Users get:

- A documented override surface via `customize.toml`
- Team-scoped overrides via `_bmad/custom/{skill-name}.toml`
- Personal-scoped overrides via `_bmad/custom/{skill-name}.user.toml`
- Automatic precedence handling from the resolver (user beats team beats defaults)
- A conversational authoring path: the `bmad-customize` core skill scans which skills are customizable, helps the user pick agent vs workflow scope, writes the override file, and verifies the merge. Users who prefer to hand-write TOML still can.

## Tips

- **Ship one good default. Skip the booleans.** A flag like `include_combat_section` usually means you haven't decided what the skill does yet. Pick the default. Users who want a radically different shape can fork.
- **Sentence-shaped variance belongs in `persistent_facts`.** Tone, house rules, and domain constraints are sentences the skill carries through the run. Don't enumerate them as scalars.
- **Read [Customization for Authors](/explanation/customization-for-authors.md) first.** It gives you the three questions to ask for each candidate knob before you start Configurability Discovery.
