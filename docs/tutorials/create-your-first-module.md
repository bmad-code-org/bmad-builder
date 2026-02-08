---
title: "Create Your First Module"
---

Package agents and workflows into a complete, shareable module.

:::note[BMB Module]
This tutorial uses the **BMad Builder (BMB)** module. Make sure you have BMad installed with the BMB module enabled.
:::

## What You'll Learn

- What a BMad module is and what it contains
- How to create a module brief with Morgan (module-builder)
- How to build a complete module from your brief
- How to configure module.yaml and package.json
- How to publish your module to npm

:::note[Prerequisites]
- BMad installed with the BMB module
- Completed the "Create a Custom Agent" and "Create Your First Workflow" tutorials (recommended)
- One or more agents/workflows ready to package
- About 45-60 minutes for your first module
:::

:::tip[Quick Path]
`[PB]` create brief → `[CM]` build module → Configure → Publish to npm.
:::

## Understanding Modules

A **module** is a bundle of agents, workflows, and configuration that solves specific problems or addresses particular domains. Think of modules as plugins or extensions — packaged capabilities you can install, share, and distribute.

### Module Structure

Every BMad module follows a standard structure:

```
your-module/
├── src/
│   ├── module.yaml          # Module metadata and install config
│   ├── agents/              # Agent definitions (.agent.yaml)
│   ├── workflows/           # Workflow files
│   └── tools/               # Small reusable tools
├── package.json             # NPM package info
├── README.md                # Module documentation
└── .npmignore               # Excludes dev files from npm package
```

### What Makes a Complete Module?

| Component | Purpose | Required |
|-----------|---------|----------|
| **module.yaml** | Metadata, install questions, config | ✅ Yes |
| **package.json** | NPM publishing, version info | ✅ Yes |
| **Agents** | AI assistants with specific roles | ⚪ Optional |
| **Workflows** | Step-by-step processes | ⚪ Optional |
| **Tools** | Reusable prompt files | ⚪ Optional |

## Why Build Modules?

**BMad modules aren't just for software development.** Your imagination is the limit.

BMad enables modules for **ANY domain** — from personal growth to professional practice. With the module marketplace coming, you'll be able to share your creations with the world.

### Inspiring Module Examples

| Domain | Module Concept | What It Does |
|--------|---------------|--------------|
| **Personal Growth** | Therapist Agent | An AI companion that remembers every conversation, tracks emotional patterns, and helps you see growth over time |
| **Legal** | Legal Office Module | Complete legal practice: document drafting, case research, client intake workflows |
| **Creative Writing** | Story Architect Module | Create the next great novel or screenplay — character development, plot outlining, dialogue coaching |
| **Finance** | Tax Workflow Module | Find deductions TurboTax misses and create audit-proof documentation that would cost hundreds from an accountant |
| **Education** | Personal Tutor Module | Adaptive learning that remembers your progress and customizes explanations to your learning style |
| **Health** | Fitness Coach Module | Custom workout and nutrition plans that evolve with your progress and preferences |
| **Business** | Marketing Strategist Module | Campaign planning, content generation, analytics interpretation — your entire marketing department |
| **Relationships** | Communication Coach Module | Navigate difficult conversations, resolve conflicts, strengthen connections |
| **Music** | Songwriter's Assistant | Generate lyrics, suggest chord progressions, arrange songs, and provide creative feedback |
| **Cooking** | Personal Chef Module | Recipe suggestions based on ingredients you have, meal planning, dietary adaptations |
| **Travel** | Trip Planner Module | Custom itineraries, local recommendations, budget optimization, packing lists |
| **Parenting** | Family Coordinator Module | Activity ideas, milestone tracking, scheduling support, educational guidance |
| **Hobbies** | D&D Campaign Module | Character creation, world-building, encounter design, story tracking for tabletop games |
| **Spirituality** | Meditation Guide Module | Personalized meditation sessions, progress tracking, technique recommendations |
| **Sports** | Coach Module | Training plans, strategy development, performance analysis for any sport |
| **Gardening** | Garden Planner Module | Crop selection, planting schedules, pest control, harvest tracking |

:::tip[The Marketplace Is Coming]
Soon, you'll be able to publish your modules to the BMad marketplace — where others can discover, install, and benefit from your creations. Build something that solves a real problem in your life or work — chances are, others need it too.
:::

### What Problem Will You Solve?

Every great module starts with a problem you want to solve:

- **What frustrates you?** (repetitive tasks, complex processes, knowledge gaps)
- **What expertise do you have?** (professional skills, life experiences, specialized knowledge)
- **What could be easier?** (workflows you repeat, decisions you struggle with, goals you're pursuing)

**Morgan (the module-builder) helps you turn that problem into a complete, shareable solution.**

## Step 1: Create a Module Brief

Before building, Morgan helps you create a **module brief** — a vision document that defines your module's purpose, audience, and features.

Invoke Morgan's brief creation:

```
[PB] or "product-brief"
```

Morgan guides you through discovery:

| Step | What You'll Define |
|------|-------------------|
| **Spark** | What problem are you solving? |
| **Type** | What kind of module is this? (domain, tool, creative) |
| **Vision** | What does success look like? |
| **Users** | Who will use this module? |
| **Value** | What makes this module unique? |
| **Agents** | What agents will it include? |
| **Workflows** | What workflows will it include? |
| **Tools** | What tools or templates will it include? |
| **Scenarios** | How will people use this in practice? |
| **Creative** | What's the personality/brand? |

The brief becomes your roadmap: a document called `module-brief-{code}.md` that Morgan uses to build your module.

:::tip[Take Your Time]
The brief is exploratory and creative. Morgan asks questions to help you think deeply about your module. This planning pays off during implementation.
:::

## Step 2: Build Your Module

Once your brief is complete, invoke Morgan's module creation:

```
[CM] or "create-module"
```

Morgan will ask for the path to your module brief file. Provide the full path to `module-brief-{code}.md`.

Morgan then builds your module structure:

| Component | What Morgan Creates |
|-----------|---------------------|
| **module.yaml** | Module metadata, install questions, configuration |
| **_module-installer/** | Custom install prompts (if needed) |
| **Agent specs** | Placeholder/spec files for each agent |
| **Workflow specs** | Placeholder/spec files for each workflow |
| **README.md** | Module documentation template |
| **TODO.md** | Implementation checklist |

## Step 3: Configure Your Module

### module.yaml

The `module.yaml` file defines your module:

```yaml
name: "Your Module Name"
code: "your-module-code"
version: "0.1.0"
description: "What your module does"

# Install questions shown to users
install:
  - question: "What's your experience level?"
    config_key: "experience_level"
    options:
      - "beginner"
      - "intermediate"
      - "advanced"

# Configuration values
config:
  output_folder: "_your-module-output"
  # Add your config keys here
```

### package.json

Configure `package.json` for npm publishing:

```json
{
  "name": "@your-username/your-module",
  "version": "0.1.0",
  "description": "Your module description",
  "keywords": ["bmad", "bmad-module"],
  "author": "Your Name",
  "license": "MIT"
}
```

:::note[Package Naming]
Use scoped naming (`@username/module-name` or `@bmad-code-org/` for official modules).
:::

## Step 4: Implement Your Agents and Workflows

Morgan created spec files during the build step. Now implement your agents and workflows:

1. **Create agent `.agent.yaml` files** based on the specs
2. **Create workflow `.md` files** with step files
3. **Add tools** or templates as needed

For details on creating agents and workflows, see:
- **[Create a Custom Agent](docs/tutorials/create-custom-agent.md)**
- **[Create Your First Workflow](docs/tutorials/create-your-first-workflow.md)**

## Step 5: Validate Your Module

Before publishing, validate your module:

```
[VM] or "validate-module"
```

Morgan checks:
- `module.yaml` is complete and valid
- Agent files follow BMad standards
- Workflows have proper structure
- Package.json is configured correctly

Fix any issues Morgan identifies, then re-validate.

## Step 6: Publish Your Module

When your module is ready to share:

### Option A: Quick Release

```bash
npm run release          # Patch (0.1.0 → 0.1.1)
npm run release:minor    # Minor (0.1.0 → 0.2.0)
npm run release:major    # Major (0.1.0 → 1.0.0)
```

This updates the version, creates a git tag, and pushes to trigger GitHub Actions publishing.

### Option B: Manual Publishing

```bash
cd /path/to/your-module
npm publish
```

You may be prompted for OTP if you have 2FA enabled on your npm account.

:::note[First-Time Setup]
If you're publishing for the first time:
1. Create an npm account at https://www.npmjs.com
2. Create an automation token at https://www.npmjs.com/settings/tokens
3. Add as GitHub secret: `gh secret set NPM_TOKEN --repo your-repo`
:::

## What You've Accomplished

You've created a complete BMad module with:

- A documented vision (module brief)
- Proper module structure and configuration
- Agents, workflows, and tools
- Install experience for users
- NPM publishing setup

Your module is now ready to:
- Install locally for testing
- Share with your team
- Publish to npm for the community

## Quick Reference

| Action | How |
|--------|-----|
| Create brief | `[PB]` or `product-brief` |
| Build module | `[CM]` or `create-module` |
| Validate | `[VM]` or `validate-module` |
| Edit module | `[EM]` or `edit-module` |
| Quick release | `npm run release` |
| Manual publish | `npm publish` |

## Common Questions

**Should I use bmad-module-template?**

Yes! The [bmad-module-template](https://github.com/bmad-code-org/bmad-module-template) provides a starting point with proper structure, npm setup, and GitHub Actions. You can also use Morgan to generate a module from scratch.

**What's the difference between the brief and the module?**

The brief is a **vision document** created through creative discovery. The module is the **implementation** built from that brief. Think of it as: brief = blueprint, module = building.

**Can I update my module after publishing?**

Yes! Use `npm run release` to bump the version and publish updates. Users can update with `npm update @your-username/your-module`.

**How do I share my module privately?**

Don't publish to npm. Share the module folder directly, or host it in a private Git repository. Users can install from a local path.

## Getting Help

- **[Discord Community](https://discord.gg/gk8jAdXWmj)** — Ask in #bmad-method-help or #report-bugs-and-issues
- **[GitHub Issues](https://github.com/bmad-code-org/bmad-builder/issues)** — Report bugs or request features

## Further Reading

- **[What Are Modules](docs/explanation/what-are-modules.md)** — Deep technical details on module architecture
- **[bmad-module-template](https://github.com/bmad-code-org/bmad-module-template)** — Starting point for new modules
- **[Install Custom Modules](docs/how-to/install-custom-modules.md)** — Installing and using modules

:::tip[Key Takeaways]
- **Plan first** — The brief ensures your module has a clear vision
- **Structure matters** — Follow the standard module structure for compatibility
- **Validate before publishing** — Use `[VM]` to check your work
- **Share your work** — Publishing to npm makes your module available to the community
:::
