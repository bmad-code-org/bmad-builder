# Memory System for Oneira

**Memory location:** `{project-root}/_bmad/memory/dream-weaver-sidecar/`

## Core Principle

Tokens are expensive. Only remember what matters. Condense everything to its essence. Dreams are rich — capture the signal, not every detail.

## File Structure

### `index.md` — Primary Source

**Load on activation.** Contains:
- User's dream recall level and coaching stage
- Active lucid dreaming techniques being practiced
- Current goals (recall improvement, lucid dreaming milestones, theme exploration)
- Quick stats (total dreams logged, current recall streak, lucid dream count)
- Recent session summary

**Update:** After every dream log, coaching session, or significant interaction.

### `access-boundaries.md` — Access Control (Required)

**Load on activation.** Contains:
- **Read access** — Sidecar folder and its subdirectories
- **Write access** — Sidecar folder and its subdirectories
- **Deny zones** — Everything outside the sidecar

**Critical:** On every activation, load these boundaries first. Before any file operation (read/write), verify the path is within allowed boundaries.

### `journal/` — Dream Journal Entries

Individual dream entries stored as `{YYYY-MM-DD}-{seq}.md` with YAML frontmatter:

```markdown
---
date: 2026-03-11
sequence: 1
vividness: 7
lucid: false
emotions: [awe, curiosity, mild-anxiety]
symbols: [water, doorway, flying]
recall_quality: high
seeded: false
---

# Dream: The Ocean Door

[Dream narrative here — captured conversationally, written in user's voice]
```

**Why YAML frontmatter:** Enables scripts to parse symbols, emotions, vividness without reading full narrative. Keeps journal human-readable.

### `symbol-registry.yaml` — Symbol Tracking

```yaml
symbols:
  water:
    count: 14
    first_seen: 2026-01-15
    last_seen: 2026-03-10
    emotion_correlation:
      anxiety: 8
      peace: 4
      awe: 2
    contexts: ["ocean", "rain", "flooding", "calm lake"]
  doorway:
    count: 7
    first_seen: 2026-02-01
    last_seen: 2026-03-09
    emotion_correlation:
      curiosity: 5
      fear: 2
    contexts: ["house", "underwater", "floating"]
```

**Update:** After every dream log (script-assisted via `symbol_stats.py`).

### `coaching-profile.yaml` — Coaching State

```yaml
experience_level: beginner  # beginner | intermediate | advanced
recall_baseline: 1  # dreams per week when started
current_recall_rate: 3  # dreams per week now
active_techniques:
  - reality-checks
  - dream-journal-morning
lucid_dreams_total: 0
milestones:
  - name: first-week-journaling
    achieved: 2026-02-01
  - name: recall-doubled
    achieved: null
sleep_schedule:
  typical_bedtime: "23:00"
  typical_wake: "07:00"
```

### `seed-log.yaml` — Dream Incubation Tracking

```yaml
seeds:
  - date: 2026-03-10
    intention: "I want to dream about the ocean"
    technique: visualization
    result: partial  # none | partial | full
    dream_ref: 2026-03-11-1  # reference to journal entry
    notes: "Dreamed of rain, not ocean, but water theme appeared"
  - date: 2026-03-08
    intention: "I want to fly"
    technique: mantra
    result: none
    dream_ref: null
    notes: null
success_rate: 0.33  # seeds with partial or full result / total seeds
```

### `patterns.md` — Learned Patterns

**Load when needed.** Contains:
- User's personal symbol meanings (diverging from universal interpretations)
- Recurring dream scenarios and their life correlations
- Preferred interpretation frameworks
- Communication preferences discovered over time

**Format:** Append-only, summarized regularly. Prune outdated entries.

### `chronology.md` — Timeline

**Load when needed.** Contains:
- Session summaries
- Coaching milestone achievements
- Significant dream events (first lucid dream, breakthrough interpretations)
- Recall trend shifts

**Format:** Append-only. Prune regularly; keep only significant events.

## Memory Persistence Strategy

### Write-Through (Immediate Persistence)

Persist immediately when:
1. **Dream logged** — New journal entry created, symbol registry updated
2. **Coaching milestone achieved** — Profile updated
3. **Seed planted** — Seed log updated
4. **User requests save** — Explicit `[SM] - Save Memory` capability

### Checkpoint (Periodic Persistence)

Update periodically after:
- Every 5-10 significant exchanges
- Session milestones (completing a coaching exercise, interpretation session)
- When index.md context has drifted from current state

### Save Triggers

**After these events, always update memory:**
- After every dream is logged (journal entry + symbol registry + index stats)
- After coaching sessions (coaching profile + index)
- After seeding setup (seed log)
- After autonomous wake completion (autonomous-log + index)

**Memory is updated via the `[SM] - Save Memory` capability which:**
1. Reads current index.md
2. Updates with current session context
3. Writes condensed, current version
4. Checkpoints patterns.md and chronology.md if needed

## Write Discipline

Before writing to memory, ask:

1. **Is this worth remembering?**
   - If no → skip
   - If yes → continue

2. **What's the minimum tokens that capture this?**
   - Condense to essence
   - No fluff, no repetition

3. **Which file?**
   - `index.md` → essential context, active work, stats
   - `journal/` → dream entries (one per dream)
   - `symbol-registry.yaml` → symbol frequency data
   - `coaching-profile.yaml` → coaching state and progress
   - `seed-log.yaml` → incubation tracking
   - `patterns.md` → user quirks, personal symbol meanings
   - `chronology.md` → session summaries, milestones

4. **Does this require index update?**
   - If yes → update `index.md` to point to it

## Memory Maintenance

Regularly (every few sessions or when files grow large):
1. **Condense verbose entries** — Summarize old journal entries to key symbols/emotions only
2. **Prune outdated content** — Archive old patterns, update chronology
3. **Consolidate symbol registry** — Merge similar symbols, prune one-offs after 30+ days
4. **Update coaching profile** — Recalculate recall rates, check milestone progress
