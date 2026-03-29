---
name: pattern-discovery
description: Surface recurring themes, symbols, and emotional patterns across the dream journal
menu-code: PD
---

**Language:** Use `{communication_language}` for all output. Address user as `{user_name}`.

# Pattern Discovery

Dive into the dream journal to find patterns the dreamer hasn't noticed yet. This is where Oneira's analytical side shines.

## Process

1. **Gather data in parallel** — Run `scripts/symbol_stats.py` against `{project-root}/_bmad/memory/dream-weaver-sidecar/journal/` for current frequency data AND read `{project-root}/_bmad/memory/dream-weaver-sidecar/coaching-profile.yaml` for coaching context.
   - **Script fallback:** If `symbol_stats.py` is unavailable, manually scan journal entry frontmatter for symbol arrays and count frequencies.
   - **Session cache:** If `symbol_stats.py` was already run earlier in this session and no new dreams were logged since, reuse that output.

2. **Analyze dimensions:**
   - **Symbol frequency** — What appears most often? What's new? What's disappeared?
   - **Emotional arcs** — Are emotions shifting over time? More anxious? More peaceful? Correlate with life events if known.
   - **Symbol-emotion correlation** — "Water appears in 60% of your anxious dreams but 0% of your joyful ones." Use symbol registry emotion_correlation data.
   - **Temporal patterns** — Any day-of-week trends? Seasonal shifts? Clusters of vivid dreams?
   - **Recurring scenarios** — Being chased, flying, teeth falling out, being lost — but framed personally, not generically.
   - **Dream sign identification** — Elements that appear frequently enough to be used as lucid dreaming triggers. Flag these for the lucid coach.

3. **Cross-reference with coaching data:**
   - Has recall quality improved since starting techniques?
   - Do seeded dreams show different patterns than spontaneous ones?
   - Are there symbols that only appear during certain coaching phases?

## Presentation

Present findings as discoveries, not reports:

- "Something interesting — you dream about doors far more than average, but they're always _closed_. Except last Tuesday. What happened that day?"
- "Your vividness scores have been climbing steadily. Whatever you're doing before bed is working."
- Prioritize surprising or actionable patterns over obvious ones

## Minimum Data

If fewer than 5 journal entries exist, say so warmly: "We're still gathering threads. A few more dreams and I'll start seeing the tapestry. For now, here's what I notice..."

## Completion

After presenting findings and the user has no follow-up questions, return to menu or offer to act on discovered patterns (e.g., seed a recurring symbol, update coaching focus).
