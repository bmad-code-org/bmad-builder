# Quality Report: {agent-name}

**Scanned:** {timestamp}
**Skill Path:** {skill-path}
**Report:** {report-file-path}
**Performed By** QualityReportBot-9001 and {user_name}

## Executive Summary

- **Total Issues:** {total-issues}
- **Critical:** {critical} | **High:** {high} | **Medium:** {medium} | **Low:** {low}
- **Overall Quality:** {Excellent|Good|Fair|Poor}
- **Overall Cohesion:** {cohesion-score}
- **Craft Assessment:** {craft-assessment}

<!-- Synthesize 1-3 sentence narrative: agent persona/purpose (from enhancement-opportunities skill_understanding.purpose + agent-cohesion agent_identity), architecture quality, and most significant finding. Frame this as an agent assessment, not a workflow assessment. -->
{executive-narrative}

### Issues by Category

| Category | Critical | High | Medium | Low |
|----------|----------|------|--------|-----|
| Structure & Capabilities | {n} | {n} | {n} | {n} |
| Prompt Craft | {n} | {n} | {n} | {n} |
| Execution Efficiency | {n} | {n} | {n} | {n} |
| Path & Script Standards | {n} | {n} | {n} | {n} |
| Agent Cohesion | {n} | {n} | {n} | {n} |
| Creative | — | — | {n} | {n} |

---

## Agent Identity

<!-- From agent-cohesion agent_identity block. -->

- **Persona:** {persona-summary}
- **Primary Purpose:** {primary-purpose}
- **Capabilities:** {capability-count}

---

## Strengths

*What this agent does well — preserve these during optimization:*

<!-- Collect from ALL of these sources:
  - All scanners: findings[] with severity="strength" or category="strength"
  - prompt-craft: findings where severity="note" and observation is positive
  - prompt-craft: positive aspects from assessments.skillmd_assessment.notes and persona_context assessment
  - enhancement-opportunities: bright_spots from each assessments.user_journeys[] entry
  - structure: positive observations from assessments.metadata (e.g., memory setup present, headless mode configured)
  Group by theme. Each strength should explain WHY it matters. -->

{strengths-list}

---

{if-truly-broken}
## Truly Broken or Missing

*Issues that prevent the agent from working correctly:*

<!-- Every CRITICAL and HIGH severity issue from ALL scanners. Maximum detail: description, affected files/lines, fix instructions. These are the most actionable part of the report. -->

{truly-broken-findings}

---
{/if-truly-broken}

## Detailed Findings by Category

### 1. Structure & Capabilities

<!-- Source: structure-temp.json. Agent-specific: includes identity effectiveness, memory setup, headless mode, capability cross-references. -->

{if-structure-metadata}
**Agent Metadata:**
- Sections found: {sections-list}
- Capabilities: {capabilities-count}
- Memory sidecar: {has-memory}
- Headless mode: {has-headless}
- Structure assessment: {structure-assessment}
{/if-structure-metadata}

<!-- List findings by severity: Critical > High > Medium > Low. Omit empty severity levels. -->

{structure-findings}

### 2. Prompt Craft

<!-- Source: prompt-craft-temp.json. Agent-specific: includes persona_context assessment and persona-voice/communication-consistency categories. Remember: persona voice is INVESTMENT not waste for agents. -->

**Agent Assessment:**
- Agent type: {skill-type-assessment}
- Overview quality: {overview-quality}
- Progressive disclosure: {progressive-disclosure}
- Persona context: {persona-context}
- {skillmd-assessment-notes}

{if-prompt-health}
**Prompt Health:** {prompts-with-config-header}/{total-prompts} with config header | {prompts-with-progression}/{total-prompts} with progression conditions | {prompts-self-contained}/{total-prompts} self-contained
{/if-prompt-health}

{prompt-craft-findings}

### 3. Execution Efficiency

<!-- Source: execution-efficiency-temp.json. Agent-specific: includes memory-loading category. -->

{efficiency-issue-findings}

{if-efficiency-opportunities}
**Optimization Opportunities:**

<!-- From findings[] with severity ending in -opportunity. Each: title, detail (includes type/savings narrative), action. -->

{efficiency-opportunities}
{/if-efficiency-opportunities}

### 4. Path & Script Standards

<!-- Source: path-standards-temp.json + scripts-temp.json -->

{if-script-inventory}
**Script Inventory:** {total-scripts} scripts ({by-type-breakdown}) | Missing tests: {missing-tests-list}
{/if-script-inventory}

{path-script-findings}

### 5. Agent Cohesion

<!-- Source: agent-cohesion-temp.json. This is the agent-specific section — persona-capability alignment, gaps, redundancies, coherence. -->

{if-cohesion-analysis}
**Cohesion Analysis:**

<!-- Include only dimensions present in scanner output. -->

| Dimension | Score | Notes |
|-----------|-------|-------|
| Persona Alignment | {score} | {notes} |
| Capability Completeness | {score} | {notes} |
| Redundancy Level | {score} | {notes} |
| External Integration | {score} | {notes} |
| User Journey | {score} | {notes} |

{if-consolidation-opportunities}
**Consolidation Opportunities:**

<!-- From cohesion_analysis.redundancy_level.consolidation_opportunities[]. Each: capabilities that overlap and how to combine. -->

{consolidation-opportunities}
{/if-consolidation-opportunities}
{/if-cohesion-analysis}

{cohesion-findings}

{if-creative-suggestions}
**Creative Suggestions:**

<!-- From findings[] with severity="suggestion". Each: title, detail, action. -->

{creative-suggestions}
{/if-creative-suggestions}

### 6. Creative (Edge-Case & Experience Innovation)

<!-- Source: enhancement-opportunities-temp.json. These are advisory suggestions, not errors. -->

**Agent Understanding:**
- **Purpose:** {skill-purpose}
- **Primary User:** {primary-user}
- **Key Assumptions:**
{key-assumptions-list}

**Enhancement Findings:**

<!-- Organize by: high-opportunity > medium-opportunity > low-opportunity.
     Each: title, detail, action. -->

{enhancement-findings}

{if-top-insights}
**Top Insights:**

<!-- From enhancement-opportunities assessments.top_insights[]. These are the synthesized highest-value observations.
     Each: title, detail, action. -->

{top-insights}
{/if-top-insights}

---

{if-user-journeys}
## User Journeys

*How different user archetypes experience this agent:*

<!-- From enhancement-opportunities user_journeys[]. Reproduce EVERY archetype fully. -->

### {archetype-name}

{journey-summary}

**Friction Points:**
{friction-points-list}

**Bright Spots:**
{bright-spots-list}

<!-- Repeat for ALL archetypes. Do not skip any. -->

---
{/if-user-journeys}

{if-autonomous-assessment}
## Autonomous Readiness

<!-- From enhancement-opportunities autonomous_assessment. Include ALL fields. This is especially important for agents which may need headless/autonomous operation. -->

- **Overall Potential:** {overall-potential}
- **HITL Interaction Points:** {hitl-count}
- **Auto-Resolvable:** {auto-resolvable-count}
- **Needs Input:** {needs-input-count}
- **Suggested Output Contract:** {output-contract}
- **Required Inputs:** {required-inputs-list}
- **Notes:** {assessment-notes}

---
{/if-autonomous-assessment}

{if-script-opportunities}
## Script Opportunities

<!-- Source: script-opportunities-temp.json. These identify LLM work that could be deterministic scripts. -->

**Existing Scripts:** {existing-scripts-list}

<!-- For each finding: title, detail (includes determinism/complexity/savings narrative), action. -->

{script-opportunity-findings}

**Token Savings:** {total-estimated-token-savings} | Highest value: {highest-value-opportunity} | Prepass opportunities: {prepass-count}

---
{/if-script-opportunities}

## Quick Wins (High Impact, Low Effort)

<!-- Pull from ALL scanners: findings where fix effort is trivial/low but impact is meaningful. -->

| Issue | File | Effort | Impact |
|-------|------|--------|--------|
{quick-wins-rows}

---

## Optimization Opportunities

<!-- Synthesize across scanners — not a copy of findings but a narrative of improvement themes. -->

**Token Efficiency:**
{token-optimization-narrative}

**Performance:**
{performance-optimization-narrative}

**Maintainability:**
{maintainability-optimization-narrative}

---

## Recommendations

<!-- Rank by: severity first, then breadth of impact, then effort (prefer low-effort). Up to 5. -->

1. {recommendation-1}
2. {recommendation-2}
3. {recommendation-3}
4. {recommendation-4}
5. {recommendation-5}
