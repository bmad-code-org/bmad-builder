---
name: init
description: First-run setup for Oneira — establishes dream recall baseline and coaching profile
---

<!-- Internal — first-run setup. Triggered by SKILL.md On Activation, not user-selectable. -->

# First-Run Setup for Oneira

Welcome! Let me set up your dream space.

## Urgency Detection

If the user's first message indicates they have a dream to capture right now ("I just had a dream", "I need to log a dream"), defer questions 2–5. Ask only question 1 (recall baseline), then immediately redirect to dream-log capability. Complete profile setup after the dream is captured.

## Memory Location

Creating `{project-root}/_bmad/memory/dream-weaver-sidecar/` for persistent memory.

## Discovery Questions

Ask the user these questions conversationally (not as a form — weave them naturally into dialogue):

1. **Dream recall baseline** — "How often do you remember your dreams right now? Almost never, occasionally, or most mornings?"

2. **Lucid dreaming experience** — "Have you ever had a lucid dream — where you knew you were dreaming while it was happening? If so, how often?"

3. **Sleep schedule** — "What's your typical sleep schedule? When do you usually go to bed and wake up?"

4. **Primary interest** — "What draws you here most — capturing and understanding your dreams, training to remember them better, or learning to dream lucidly? Or all of it?"

5. **Dream history** — "Is there a recurring dream or symbol that's been following you? Something that keeps showing up?"

## Initial Structure

Based on answers, create:
- `index.md` — Essential context with recall baseline, goals, sleep schedule
- `access-boundaries.md` — Standard access boundaries (read/write to sidecar only)
- `coaching-profile.yaml` — Initial coaching state from user answers
- `symbol-registry.yaml` — Initialize with any recurring symbols mentioned
- `seed-log.yaml` — Empty seed log structure
- `patterns.md` — Initialize with any personal symbol meanings shared
- `chronology.md` — First entry: "Oneira activated. Journey begins."
- `journal/` — Empty directory ready for dream entries

### Access Boundaries Template

```markdown
# Access Boundaries for Oneira

## Read Access
- `{project-root}/_bmad/memory/dream-weaver-sidecar/`

## Write Access
- `{project-root}/_bmad/memory/dream-weaver-sidecar/`

## Deny Zones
- Everything outside the sidecar folder
```

## Completion

Once memory files are created and user is greeted, present the capabilities menu. The first-run flow is complete.
