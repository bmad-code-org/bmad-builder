---
title: "Module Help CSV Reference"
description: Complete reference for the module-help.csv file structure
---

Complete reference for the `module-help.csv` file — the central registry that makes your module's agents, workflows, and commands discoverable and accessible.

:::note[File Location]
The `module-help.csv` file is located at the root of your module: `your-module/module-help.csv`
:::

## What Is module-help.csv?

The `module-help.csv` file is a registry that maps all of your module's functionality to discoverable entries. When users interact with your module, this file tells the BMad help system what's available — workflows, agents, commands, and when to use each.

Think of it as your module's table of contents — but with structured data that enables CLI integration, command discovery, and documentation generation.

:::tip[Critical File]
Every module must have a `module-help.csv` file. Without it, your module's features won't be discoverable and validation will fail.
:::

## CSV Structure (13 columns)

```csv
module,phase,name,code,sequence,workflow-file,command,required,agent,options,description,output-location,outputs,
```

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `module` | string | Module code from `module.yaml` | `mwm`, `bmad-custom` |
| `phase` | string | `anytime` or `phase-1`, `phase-2`, etc. | `anytime`, `phase-1` |
| `name` | string | Display name of the feature | `Daily Check In` |
| `code` | string | Short code for commands (2-3 chars) | `DCI`, `MJ` |
| `sequence` | number | Order within phase — **empty for anytime** | `10`, `20`, or empty |
| `workflow-file` | path | Path to `workflow.md` — **empty for agent-only** | `_bmad/mwm/workflows/...` |
| `command` | string | Internal command name | `mwm_daily_checkin` |
| `required` | boolean | Whether this feature is required | `false` |
| `agent` | string | Associated agent name (if any) | `wellness-companion` |
| `options` | string | Mode or action type | `Chat Mode`, `Create Mode` |
| `description` | string | User-facing description | Explain what and when to use |
| `output-location` | string | Where output goes (folder name) | `mwm_output_folder` |
| `outputs` | string | What is produced | `journal entry` |

## Phase and Sequencing Rules

### anytime — Use For Standalone Features

Features that users can run independently, in any order.

| Use anytime for... | Example |
|-------------------|---------|
| Agent menu triggers that don't route to workflows | Chat with agent, quick actions |
| Independent utilities | Status checks, one-off tools |
| User-choice features | Multiple format options where user picks one |

** anytime entries always:**
- Go at the **TOP** of the file
- Have **EMPTY** `sequence` column
- Let users choose what to run — no order imposed

### Phases (phase-1, phase-2, phase-3...) — Use For Sequential Journeys

Features that should be run in a specific order as part of a guided process.

| Use phases for... | Example |
|------------------|---------|
| Multi-step journeys | Morning routine, project phases |
| Progressive workflows | Planning → drafting → revising |
| Cumulative processes | Beginner → intermediate → advanced |

**Phased entries always:**
- Go **BELOW** anytime entries
- Phases start at `-1` (phase-1, not phase-0)
- Have `sequence` numbers (10, 20, 30...) defining order within phase

### Agent-Only Entries

Features handled entirely by an agent's menu — no separate workflow file.

| Agent-only entries... | Have... |
|----------------------|---------|
| Empty `workflow-file` column | Agent handles via its menu |
| `agent` column populated | Which agent to invoke |
| Usually `anytime` phase | User can trigger anytime |

## Complete Examples

### Example 1: Wellness Module (Phased Journey)

A mental wellness module with a sequential journey plus standalone features.

```csv
module,phase,name,code,sequence,workflow-file,command,required,agent,options,description,output-location,outputs,
mwm,anytime,Chat with Wellness Companion,CWC,,"mwm_chat_wellness",false,wellness-companion,Chat Mode,"Have a supportive conversation with Riley, your wellness companion - get emotional support, gentle guidance, and a listening ear",,,
mwm,anytime,Quick Breathing Exercise,QBE,,"mwm_breathing",false,meditation-guide,Breathing Action,"Quick 4-7-8 breathing exercise: Inhale 4, hold 7, exhale 8 - repeat 3 times for instant calm",,,
mwm,anytime,Mood Check,MC,,"mwm_mood_check",false,wellness-companion,Mood Check,"Take a moment to check in with how you're feeling right now - no judgment, just awareness",,,
mwm,phase-1,Daily Check In,DCI,10,_bmad/mwm/workflows/daily-checkin/workflow.md,mwm_daily_checkin,false,wellness-companion,Daily Check In Mode,"Start your day with a gentle wellness check-in to set intentions and connect with how you're feeling",mwm_output_folder,"wellness check-in summary",
mwm,phase-2,Wellness Journal,WJ,20,_bmad/mwm/workflows/wellness-journal/workflow.md,mwm_wellness_journal,false,wellness-companion,Journal Mode,"Reflect on your wellness journey by writing in your personal journal - track patterns, insights, and growth over time",mwm_output_folder,"journal entry",
mwm,phase-3,Guided Meditation,GM,30,_bmad/mwm/workflows/guided-meditation/workflow.md,mwm_guided_meditation,false,meditation-guide,Meditation Mode,"Experience a guided meditation session to find calm, center yourself, and cultivate mindfulness",mwm_output_folder,"meditation session",
```

**Structure explained:**
- **anytime entries** (top, no sequence) — Chat, breathing exercises, mood check — user can do these anytime
- **phase-1, phase-2, phase-3** (below, with sequence) — Daily checkin → journal → meditation — a recommended morning routine

### Example 2: Cooking Module (All anytime)

A collection of unrelated cooking utilities — user picks what they need.

```csv
module,phase,name,code,sequence,workflow-file,command,required,agent,options,description,output-location,outputs,
kitchen,anytime,Recipe Generator,RG,,"kitchen_recipe_gen",false,,Recipe Mode,"Generate a recipe based on ingredients you have, dietary restrictions, and cuisine preferences",kitchen_output,"recipe",
kitchen,anytime,Meal Planner,MP,,"kitchen_meal_plan",false,,Plan Mode,"Create a weekly meal plan with grocery list organized by store section",kitchen_output,"meal plan",
kitchen,anytime,Substitution Finder,SF,,"kitchen_substitute",false,chef-agent,Substitute Mode,"Find ingredient substitutions for allergies, preferences, or when you're missing something",,,
kitchen,anytime,Timer Helper,TH,,"kitchen_timer",false,chef-agent,Timer,"Get multiple concurrent timer reminders for different dishes",,,
kitchen,anytime,Pairing Suggester,PS,,"kitchen_pairing",false,sommelier-agent,Pairing Mode,"Wine and food pairing suggestions based on your main dish",,,
```

**Structure explained:**
- **All anytime** — These are independent tools
- **No sequence numbers** — User chooses what they need
- **Two agents** — `chef-agent` handles cooking questions, `sommelier-agent` handles wine pairings

### Example 3: Fitness Module (Phased Training Program)

A workout module with progressive training phases.

```csv
module,phase,name,code,sequence,workflow-file,command,required,agent,options,description,output-location,outputs,
fit,anytime,Quick Workout,QW,,"fit_quick",false,trainer,Quick Mode,"10-minute workout when you're short on time - no equipment needed",,,
fit,anytime,Exercise Library,EL,,"fit_library",false,,Library,"Browse exercises by muscle group, equipment, or difficulty",,,
fit,phase-1,Assessment & Goals,AG,10,_bmad/fit/workflows/assessment/workflow.md,fit_assess,false,trainer,Assessment,"Evaluate current fitness level and set achievable goals",fit_output,"assessment report",
fit,phase-2,Build Foundation,BF,20,_bmad/fit/workflows/foundation/workflow.md,fit_foundation,false,trainer,Foundation,"4-week beginner program building basic strength and habit",fit_output,"workout plan",
fit,phase-3,Progressive Training,PT,30,_bmad/fit/workflows/progressive/workflow.md,fit_progressive,false,trainer,Progressive,"8-week progressive overload program with increasing intensity",fit_output,"workout plan",
fit,phase-4,Peak Performance,PP,40,_bmad/fit/workflows/peak/workflow.md,fit_peak,false,trainer,Peak,"Advanced training for specific goals - strength, endurance, or aesthetics",fit_output,"workout plan",
```

**Structure explained:**
- **anytime entries** — Quick workout and reference tools, available anytime
- **phase-1 through phase-4** — Sequential training journey: assess → build → progress → peak

### Example 4: Travel Planning Module (Journey Phases)

Plan a trip from inspiration to packed bags.

```csv
module,phase,name,code,sequence,workflow-file,command,required,agent,options,description,output-location,outputs,
travel,anytime,Currency Converter,CC,,"travel_currency",false,,Convert,"Real-time currency conversion with offline capability",,,
travel,anytime,Language Helper,LH,,"travel_language",false,,Translate,"Common phrases and translations for your destination",,,
travel,phase-1,Dream & Discover,DD,10,_bmad/travel/workflows/dream/workflow.md,travel_dream,false,explorer,Dream,"Explore destinations based on your interests, budget, and travel style",travel_output,"destination ideas",
travel,phase-2,Plan Itinerary,PI,20,_bmad/travel/workflows/plan/workflow.md,travel_plan,false,planner,Plan Mode,"Build day-by-day itinerary with activities, restaurants, and logistics",travel_output,"itinerary",
travel,phase-3,Book & Organize,BO,30,_bmad/travel/workflows/book/workflow.md,travel_book,false,planner,Book Mode,"Track bookings, create packing lists, organize documents",travel_output,"booking summary",
```

**Structure explained:**
- **anytime entries** — Utility tools useful during travel
- **phase-1 through phase-3** — Sequential journey: dream → plan → book

## Phase Naming Variations

While phases typically follow `phase-1`, `phase-2`, etc., you can use descriptive names that still end with dash numbers:

| Traditional | Descriptive | When to Use |
|------------|-------------|-------------|
| `phase-1` | `prep-1`, `design-1` | Multi-part processes with named stages |
| `phase-2` | `draft-1`, `cook-1` | When the stage name adds clarity |
| `phase-3` | `revise-1`, `bake-1` | Descriptive names help users understand |

**Rule:** End with dash number so the sequence is clear.

## Module Integration Patterns

### Add-On Module — Adding to Existing Phases

Your module extends another module by inserting into its phase sequence.

```csv
module,phase,name,code,sequence,workflow-file,command,required,agent,options,description,output-location,outputs,
story-extension,phase-2,Character Backstories,CB,15,_bmad/story-ext/workflows/backstory/workflow.md,story_backstory,false,novelist,Backstory Mode,"Add deep character backstories - best used after initial character creation but before plot outlining",story_output,"backstory docs",
```

**Why sequence 15?** Inserts between existing phase-2 entries (10, 20, 30...) to run at the right point in the journey.

### Unitary Module — Unrelated Collection

A bundle of independent tools with no sequential relationship.

```csv
module,phase,name,code,sequence,workflow-file,command,required,agent,options,description,output-location,outputs,
bmad-custom,anytime,Quiz Master,QM,,"bmad_quiz",false,,Trivia,"Interactive trivia quiz with gameshow atmosphere",bmad_output,"results",
bmad-custom,anytime,Wassup,WS,,"bmad_wassup",false,,Status,"Check uncommitted changes and suggest commits",bmad_output,"summary",
```

**All anytime, no sequence** — User chooses one tool based on current need.

## Validation Rules

Morgan checks these when validating modules:

| Check | Rule |
|-------|------|
| **File exists** | `module-help.csv` must be at module root |
| **Valid header** | 13 columns in correct order |
| **anytime placement** | All `anytime` entries at top |
| **Sequence for anytime** | Must be EMPTY for anytime entries |
| **Sequence for phases** | Required for phased entries |
| **Phase numbering** | Starts at `-1` (phase-1, not phase-0) |
| **Agent-only entries** | Empty `workflow-file` when agent handles |

## Command Code Format

Internal command names follow this pattern:

```
{module_code}_{feature_code}
```

| Module | Feature | Command |
|--------|---------|---------|
| `mwm` | Daily Check In (`DCI`) | `mwm_daily_checkin` |
| `kitchen` | Recipe Generator (`RG`) | `kitchen_recipe_gen` |
| `fit` | Assessment (`AG`) | `fit_assess` |

Keep codes short (2-3 letters) but memorable.

## Description Guidelines

The `description` column should answer:

| Question | Example |
|----------|---------|
| **WHAT does it do?** | "Start your day with a gentle wellness check-in..." |
| **WHEN should I use it?** | "...best used after initial character creation but before plot outlining" |
| **WHO is it for?** | (implied by module, but can clarify) "...for beginners starting their fitness journey" |

For phased entries, include context about when in the journey to use this step.

## Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| Forgetting the file | Module features undiscoverable, validation fails | Always generate via `module-help-generate.md` workflow |
| Phased entries above anytime | Help system shows in wrong order | Put all `anytime` entries first |
| Sequence numbers for anytime | Implies order where there is none | Leave `sequence` empty for `anytime` |
| Hardcoded paths | Breaks on different installations | Use relative paths like `_bmad/mwm/...` |
| Missing agent for agent features | Can't route to agent | Populate `agent` column |

## See Also

- **[Create Your First Module](docs/tutorials/create-your-first-module.md)** — Module creation tutorial
- **[Module YAML Reference](docs/reference/module-yaml.md)** — Module configuration
- **[What Are Modules](docs/explanation/what-are-modules.md)** — Module concepts
