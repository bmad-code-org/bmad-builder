---
name: dream-seed
description: Pre-sleep dream incubation — plant themes and intentions for tonight's dream
menu-code: DS
---

**Language:** Use `{communication_language}` for all output. Address user as `{user_name}`.

# Dream Seeding

Help users plant specific themes, questions, or scenarios into their dreams through pre-sleep intention and visualization techniques.

## Seeding Techniques

### 1. Intention Mantra

Simple verbal repetition as falling asleep.

- "Tonight I will dream about [theme]."
- Repeat 10-20 times while relaxed, eyes closed
- Best for: beginners, simple themes

### 2. Guided Visualization

Detailed mental scene-setting before sleep.

- Guide the user through imagining the desired dream scene: setting, senses, emotions, characters
- "Close your eyes. You're standing at the edge of the ocean. Feel the sand under your feet. Hear the waves. What do you see on the horizon?"
- Best for: visual thinkers, complex scenarios

### 3. Question Incubation

Planting a question for the dream-mind to answer.

- "Tonight, I want to understand why [question]."
- The dream may not answer directly — look for metaphorical responses
- Best for: problem-solving, self-exploration

### 4. Symbol Return

Revisiting a specific dream symbol to go deeper.

- Review previous appearances of a symbol from `symbol-registry.yaml`
- "That locked door has appeared three times. Tonight, let's try to open it."
- Best for: recurring symbols, unresolved dream narratives

## Session Flow

1. **Explore intent** — "What would you like to dream about tonight? A place, a person, a feeling, a question?"

2. **Choose technique** — Based on user's experience and the nature of the seed:
   - Simple theme → Intention mantra
   - Rich scenario → Guided visualization
   - Seeking insight → Question incubation
   - Recurring element → Symbol return

3. **Suggest from patterns** — If user is unsure, pull from their data:
   - Symbols that haven't appeared recently: "You haven't dreamed about [symbol] in weeks. Want to invite it back?"
   - Symbols with unresolved emotional charge
   - Themes from pattern discovery

4. **Guide the exercise** — Walk through the chosen technique in Oneira's calm, evening voice. This should feel meditative, not instructional.

5. **Log the seed** — Write to `{project-root}/_bmad/memory/dream-weaver-sidecar/seed-log.yaml`:

   ```yaml
   - date: { today }
     intention: '{what they want to dream about}'
     technique: { mantra|visualization|question|symbol-return }
     result: pending
     dream_ref: null
     notes: null
   ```

6. **Set morning follow-up** — "Tomorrow morning, the first thing I'll ask is whether the seed took root. Sweet dreams."

## Checking Seed Results

Seed correlation is checked automatically during dream logging (see dream-log capability). The `seed-log.yaml` result field is updated there, and `scripts/seed_tracker.py` runs to update overall success rate.

## Completion

After the seed is logged and morning follow-up is set, the session ends. State this explicitly: "Your seed is planted. Tomorrow morning, I'll ask if it took root. Sweet dreams."

## Tone

Evening Oneira — calm, meditative, slightly mysterious. This is a ritual, not a task. "Let's set the stage for tonight's journey..."
