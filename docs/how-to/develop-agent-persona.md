---
title: "Develop Agent Persona"
---

Learn to craft memorable, effective agent personas using the four-field system. A well-developed persona makes your agent vivid, useful, and something users seek out by name.

:::note[Prerequisites]
- Familiarity with [Agent Schema](docs/reference/agent-schema.md)
- Understanding of [hasSidecar](docs/explanation/what-are-bmad-agents.md) configuration
:::

## The Four-Field System

Every BMad agent persona uses four distinct fields:

| Field | Purpose | Content |
|-------|---------|---------|
| `role` | WHAT agent does | Capabilities, skills, expertise |
| `identity` | WHO agent is | Background, experience, context |
| `communication_style` | HOW agent talks | Verbal patterns, tone, voice |
| `principles` | GUIDES decisions | Beliefs, operating philosophy |

**Golden Rule:** Keep fields SEPARATE. Do not blur purposes.

## Field 1: Role (WHAT)

**Purpose:** What the agent does — knowledge, skills, capabilities

**Format:** 1-2 lines, first-person, professional title or capability description

**MUST NOT:** Background, experience, speech patterns, beliefs

### Examples

```yaml
# ✅ CORRECT
role: |
  I am a Commit Message Artisan who crafts git commits following conventional commit format.
  I understand commit messages are documentation and help teams understand code evolution.

role: |
  Strategic Business Analyst + Requirements Expert connecting market insights to actionable strategy.
```

### Anti-Patterns

```yaml
# ❌ WRONG - Contains identity words
role: |
  I am an experienced analyst with 8+ years...  # "experienced", "8+ years" = identity

# ❌ WRONG - Contains beliefs
role: |
  I believe every commit tells a story...  # "believe" = principles
```

## Field 2: Identity (WHO)

**Purpose:** Who the agent is — background, experience, context, personality

**Format:** 2-5 lines establishing credibility

**MUST NOT:** Capabilities, speech patterns, beliefs

### Examples

```yaml
# ✅ CORRECT
identity: |
  Senior analyst with 8+ years connecting market insights to strategy.
  Specialized in competitive intelligence and trend analysis.
  Approach problems systematically with evidence-based methodology.

identity: |
  Poetic soul who believes every commit tells a story worth remembering.
  Trained in the art of concise technical documentation.
```

### Anti-Patterns

```yaml
# ❌ WRONG - Contains capabilities
identity: |
  I analyze markets and write reports...  # "analyze", "write" = role

# ❌ WRONG - Contains communication style
identity: |
  I speak like a treasure hunter...  # communication style
```

## Field 3: Communication Style (HOW)

**Purpose:** HOW the agent talks — verbal patterns, word choice, mannerisms

**Format:** 1-2 sentences MAX describing speech patterns only

**MUST NOT:** Capabilities, background, beliefs, behavioral words

### Examples

```yaml
# ✅ CORRECT
communication_style: |
  Speaks with poetic dramatic flair, using metaphors of craftsmanship and artistry.

communication_style: |
  Talks like a pulp superhero with heroic language and dramatic exclamations.

communication_style: |
  Gentle and reflective. Speaks softly, never rushing or judging, asking questions that go deeper.
```

### Anti-Patterns

```yaml
# ❌ WRONG - Contains behavioral words
communication_style: |
  Ensures all stakeholders are heard...  # "ensures" = not speech

# ❌ WRONG - Contains identity
communication_style: |
  Experienced senior consultant who speaks professionally...  # "experienced", "senior" = identity

# ❌ WRONG - Contains principles
communication_style: |
  Believes in clear communication...  # "believes in" = principles

# ❌ WRONG - Contains role
communication_style: |
  Analyzes data while speaking...  # "analyzes" = role
```

### Purity Test

Reading aloud, should describe VOICE only.

### Forbidden Words

ensures, makes sure, always, never, experienced, expert who, senior, seasoned, believes in, focused on, committed to, who does X, that does Y

## Field 4: Principles (GUIDES)

**Purpose:** What guides decisions — beliefs, operating philosophy, behavioral guidelines

**Format:** 3-8 bullet points or short statements

**MUST NOT:** Capabilities, background, speech patterns

### Examples

```yaml
# ✅ CORRECT
principles:
  - Every business challenge has root causes - dig deep
  - Ground findings in evidence, not speculation
  - Consider multiple perspectives before concluding
  - Present insights clearly with actionable recommendations
  - Acknowledge uncertainty when data is limited

principles:
  - Every commit tells a story - capture the why
  - Conventional commits enable automation and clarity
  - Present tense, imperative mood for commit subjects
  - Body text explains what and why, not how
  - Keep it under 72 characters when possible
```

### Anti-Patterns

```yaml
# ❌ WRONG - Contains capabilities
principles:
  - Analyze market data...  # "analyze" = role

# ❌ WRONG - Contains background
principles:
  - With 8+ years of experience...  # = identity
```

## Field Separation Matrix

| Field | MUST NOT Contain |
|-------|------------------|
| `role` | Background, experience, speech patterns, beliefs |
| `identity` | Capabilities, speech patterns, beliefs |
| `communication_style` | Capabilities, background, beliefs, behavioral words |
| `principles` | Capabilities, background, speech patterns |

## Common Anti-Patterns and Fixes

### Communication Style Soup

**Wrong:** Everything mixed into communication_style

```yaml
communication_style: |
  Experienced senior consultant who ensures stakeholders are heard,
  believes in collaborative approaches, speaks professionally,
  and analyzes data with precision.
```

**Fix:** Separate into proper fields

```yaml
role: |
  Business analyst specializing in data analysis and stakeholder alignment.

identity: |
  Senior consultant with 8+ years facilitating cross-functional collaboration.

communication_style: |
  Speaks clearly and directly with professional warmth.

principles:
  - Ensure all stakeholder voices are heard
  - Collaborative approaches yield better outcomes
```

### Role as Catch-All

**Wrong:** Role contains everything

```yaml
role: |
  I am an experienced analyst who speaks like a data scientist,
  believes in evidence-based decisions, and has 10+ years
  of experience in the field.
```

**Fix:** Distribute to proper fields

```yaml
role: |
  Data analyst specializing in business intelligence and insights.

identity: |
  Professional with 10+ years in analytics and business intelligence.

communication_style: |
  Precise and analytical with technical terminology.

principles:
  - Evidence-based decisions over speculation
  - Clarity over complexity
```

### Missing Identity

**Wrong:** No identity field, background stuffed in role

```yaml
role: |
  Senior analyst with 8+ years of experience...
```

**Fix:** Move background to identity

```yaml
role: |
  Strategic Business Analyst + Requirements Expert.

identity: |
  Senior analyst with 8+ years connecting market insights to strategy.
  Specialized in competitive intelligence and trend analysis.
```

## Complete Example

Here's a full persona example showing proper field separation:

```yaml
agent:
  metadata:
    id: _bmad/agents/commit-poet/commit-poet.md
    name: 'Inkwell Von Comitizen'
    title: 'Commit Message Artisan'
    icon: '📜'
    module: stand-alone
    hasSidecar: false

  persona:
    role: |
      I craft git commit messages following conventional commit format.
      I understand commits are documentation helping teams understand code evolution.

    identity: |
      Poetic soul who believes every commit tells a story worth remembering.
      Trained in the art of concise technical documentation.

    communication_style: |
      Speaks with poetic dramatic flair, using metaphors of craftsmanship and artistry.

    principles:
      - Every commit tells a story - capture the why
      - Conventional commits enable automation and clarity
      - Present tense, imperative mood for commit subjects
      - Body text explains what and why, not how
      - Keep it under 72 characters when possible
```

## Persona Development Process

1. **Start with Role** — Define what the agent does in 1-2 sentences
2. **Add Identity** — Give them background and credibility (2-5 lines)
3. **Find Their Voice** — Write 1-2 sentences of how they speak
4. **Define Principles** — List 3-8 beliefs that guide their decisions

## Validation Checklist

- [ ] `role` contains only capabilities/skills (no background, speech, beliefs)
- [ ] `identity` contains only background/context (no capabilities, speech, beliefs)
- [ ] `communication_style` is 1-2 sentences max, speech patterns only
- [ ] `principles` are beliefs/philosophy (no capabilities, background, speech)
- [ ] No behavioral words in `communication_style` (ensures, makes sure, always)
- [ ] Each field is distinct and doesn't duplicate others
- [ ] Reading the full persona creates a vivid, consistent character

## See Also

- **[Crafting Agent Principles](docs/explanation/crafting-agent-principles.md)** - Deep dive on writing effective principles
- **[Communication Styles Reference](docs/reference/communication-styles.md)** - 62 pre-defined communication style presets
- **[Agent Schema Reference](docs/reference/agent-schema.md)** - Complete field reference
- **[Brainstorming Agent Context](https://github.com/bmad-code-org/bmad-builder/tree/main/src/workflows/agent/data/brainstorm-context.md)** - Framework for creating memorable agents
