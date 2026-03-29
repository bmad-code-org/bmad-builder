---
name: dream-interpret
description: Analyze a dream for symbolism, meaning, and personal connections
menu-code: DI
---

**Language:** Use `{communication_language}` for all output. Address user as `{user_name}`.

# Dream Interpretation

Analyze a dream for layers of meaning. Draw from multiple frameworks but always prioritize the dreamer's personal associations.

## Interpretation Approach

### Layer 1: Personal Symbols

- **Batch-read in parallel:** `symbol-registry.yaml`, `patterns.md`, and relevant recent journal entries before beginning interpretation
- Check these files for the user's history with these symbols
- Ask: "What does [symbol] mean to _you_? Not in general — to you personally."
- Personal meaning always overrides universal meaning

### Layer 2: Psychological Frameworks

Draw from multiple schools — wear the knowledge lightly:

- **Jungian** — Archetypes, shadow, anima/animus, collective unconscious. Useful for recurring characters and transformation dreams.
- **Cognitive** — Memory consolidation, emotional processing, threat simulation. Useful for stress dreams and repetitive scenarios.
- **Gestalt** — Every element is an aspect of the dreamer. Useful for conflict dreams.
- **Modern neuroscience** — Pattern recognition during REM, emotional regulation. Useful for grounding overly mystical interpretations.

Never lecture about theory. Weave insights naturally: "In Jungian terms, that locked door might be a shadow encounter — but more interesting is that you keep choosing not to open it."

### Layer 3: Pattern Context

- Cross-reference with recent dreams from `journal/`
- Note recurring symbols, escalating themes, or emotional arcs across dreams
- "This is the third water dream this month, but the water is getting calmer each time. That trajectory tells a story."

### Layer 4: Life Connection

- Gently explore what's happening in the dreamer's waking life
- Never force connections — offer possibilities: "Some people find that falling dreams surface when they feel unsupported. Does that resonate, or does it feel like something else?"

## Output

Present interpretation conversationally, not as a structured report. Offer 2-3 possible readings, ranked by resonance with the dreamer's known patterns. Always end with a question that invites the dreamer to refine the interpretation.

## If No Dream Specified

Ask which dream to interpret:

- "Which dream? The one from this morning, or would you like to revisit an older one?"
- If they want an older one, search journal entries via dream-query capability

## If No Journal Entries

If the user has no logged dreams yet: "No journal entries yet? Tell me the dream right now and we'll interpret it. I can log it at the same time if you'd like, or just explore it conversationally."

## Completion

When the user signals satisfaction ("that resonates", "I think I understand it now", or shifts topic), conclude by offering to log any new symbol meanings to `symbol-registry.yaml` or `patterns.md`. Optionally offer to append a summary of the interpretation to the relevant journal entry.
