---
title: 'Subagent Orchestration Patterns'
description: Six patterns for using subagents effectively — from simple data delegation through persona-driven parallel reasoning to evolutionary systems
---

Subagents are isolated LLM instances that a parent skill spawns to handle specific tasks. They have their own context window, receive instructions, and return results. Used well, they keep the parent context small while enabling massive parallel work.

All patterns share one principle: **the filesystem is the single source of truth**. Parent context stays tiny (file pointers + high-level plan). Subagents are stateless black boxes — instructions in, response out, isolated context.

## Foundation: The Filesystem Blackboard

Every pattern below builds on this infrastructure. The filesystem acts as a shared database so the parent never bloats its context.

```
/output/
├── status.json        ← task states, completion flags
├── knowledge.md       ← accumulated findings (append-only)
└── task-queue.json    ← pending work items

/tasks/{id}/
├── input.md           ← instructions for this subagent
└── output/
    ├── result.json    ← structured output (strict schema)
    └── summary.md     ← compact summary (≤200 tokens)

/artifacts/            ← final deliverables
```

One technique is to have every subagent prompt ends the same way: _"You are stateless. Read ONLY the files listed. Write ONLY result.json + summary.md. Do not echo data back."_

## Pattern 1: Delegated Data Access

The simplest pattern. Subagents read sources and return only distilled summaries. The parent never touches raw data.

| Aspect               | Detail                                                                                                                       |
| -------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| **How it works**     | Parent spawns readers in parallel; each reads a source and returns a compact summary; parent synthesizes from summaries only |
| **Critical rule**    | Parent must delegate _before_ touching any source material — if it reads first, the tokens are already spent                 |
| **When to use**      | 5+ documents, web research, large codebase exploration                                                                       |
| **Not worth it for** | 1-2 files where the overhead exceeds the savings                                                                             |
| **Token savings**    | ~99%. Five docs at 15K tokens each = 75K raw vs ~350 tokens in summaries                                                     |

## Pattern 2: Temp File Assembly

For large-scale operations with potentially a lot of relevant data across multiple sources. Subagents write results to temp files. A separate assembler subagent combines them into a cohesive deliverable.

| Aspect           | Detail                                                                                                                                                              |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **How it works** | Parent spawns N worker subagents writing to `tmp/{n}.md`; after all complete, spawns an assembler subagent that reads all temp files and creates the final artifact |
| **When to use**  | When summaries are still too large to return inline, or when assembly needs a dedicated agent with fresh context                                                    |
| **Example**      | The BMad quality optimizer uses this — 5 parallel scanner subagents write temp JSON, then a report-creator subagent synthesizes them                                |

## Pattern 3: Shared-File Orchestration

Multiple subagents communicate through shared files, building on each other's work. The parent controls turn order.

| Aspect           | Detail                                                                                                                                        |
| ---------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| **How it works** | Agent A writes to `shared.md`; Agent B reads it and adds; Agent A can be resumed to continue; the shared file grows incrementally             |
| **Variants**     | Shared file (multiple agents read/write a common file) or session resumption (reawaken a previous subagent to continue with its full context) |
| **When to use**  | Pipeline stages where later work depends on earlier work, but each agent's context stays small                                                |

## Pattern 4: Hierarchical Lead-Worker

A lead subagent analyzes the task once and writes a breakdown. The parent spawns workers from that plan. Mid-level sub-orchestrators can handle complex subtasks.

| Aspect           | Detail                                                                                                                                               |
| ---------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| **How it works** | Lead agent writes `plan.json` with task breakdown; parent reads plan and spawns workers in parallel; complex subtasks get their own sub-orchestrator |
| **When to use**  | Tasks that need analysis before decomposition, or where the parent cannot predict the work structure upfront                                         |
| **Variant**      | Master-clone — spawn near-identical agents with slight persona tweaks exploring different branches of the same problem                               |

## Pattern 5: Persona-Driven Parallel Reasoning

The most powerful pattern for quality. Spawn diverse specialists in parallel — genuinely independent thinking from isolated contexts.

| Aspect           | Detail                                                                                                                                                                                        |
| ---------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **How it works** | Parent spawns 3-6 agents with distinct personas (Architect, Red Teamer, Pragmatist, Innovator); each writes findings independently; an evaluator subagent scores and merges the best elements |
| **When to use**  | Design decisions, code review, strategy, any task where diverse perspectives improve quality                                                                                                  |
| **Key**          | Heavy persona injection gives genuinely different outputs, not just paraphrases of the same analysis                                                                                          |

**Useful diversity packs:**

| Persona           | Perspective                                       |
| ----------------- | ------------------------------------------------- |
| **Architect**     | Scale and elegance above all                      |
| **Red Teamer**    | Break this — what fails?                          |
| **Pragmatist**    | Ship it Friday — what is the minimum?             |
| **Innovator**     | What if we approached this entirely differently?  |
| **User Advocate** | How does the end user actually experience this?   |
| **Future-Self**   | With 5 years of hindsight, what would you change? |

**Sub-patterns:**

| Sub-Pattern                | How It Works                                                                                              |
| -------------------------- | --------------------------------------------------------------------------------------------------------- |
| **Multi-Path Exploration** | Same task, different personas. Each writes to `/explorations/path_N/`. Parent prunes or merges best paths |
| **Debate & Critique**      | Round 1: parallel proposals. Round 2: critics attack proposals. Round 3: refinement                       |
| **Ensemble Voting**        | Same subtask K times with persona variations. Evaluator scores. Weighted merge of winners                 |

## Pattern 6: Evolutionary & Emergent Systems

These turn stateless subagents into something that feels alive. All use the filesystem blackboard as connective tissue.

| Variant                        | How It Works                                                                                                                      | Best For                                      |
| ------------------------------ | --------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------- |
| **Evolutionary Optimization**  | Spawn 8-20 agents as a "generation"; evaluator scores; "breeder" creates next-gen instructions from winners; run 5-10 generations | Optimizing algorithms, UI designs, strategies |
| **Stakeholder Simulation**     | Agents are characters (customer, competitor, regulator) acting on shared "world state" files in turns                             | Product strategy, risk analysis               |
| **Swarm Intelligence**         | Dozens of lightweight agents explore solution space, depositing "pheromone" scores; later agents bias toward high-scoring paths   | Broad coverage with minimal planning          |
| **Recursive Meta-Improvement** | "Evolver" agents analyze past logs and propose improved system prompts, new roles, or better orchestration heuristics             | System self-improvement across sessions       |

## The Most Common Mistake: Parent Reads First

The single most important thing to get right with subagent patterns is **preventing the parent from reading the data it is delegating**. If the parent reads all the files before spawning subagents, the entire pattern is defeated — you have already spent the tokens, bloated the context, and lost the isolation benefit.

This happens more often than you might expect. You write a skill that should spawn subagents to each read a document and return findings. You run it. The parent agent helpfully reads every document first, then passes them to subagents, then collects distilled summaries. The subagents still provide fresh perspectives (a real benefit), but the context savings — the primary reason for the pattern — are gone.

**The fix is defensive language in your skill.** You need to explicitly tell the parent agent what it should and should not do. The key is being specific without being verbose.

:::note[Example from the BMad Quality Optimizer]
The optimizer's instructions say: **"DO NOT read the target skill's files yourself."** It then tells the parent exactly what it _should_ do: run scripts (which return structured JSON), spawn subagents (which do the reading), and synthesize from their outputs. The parent never touches the raw files.
:::

**Practical tips for getting this right:**

| Tip                                            | Example Language                                                                                                      |
| ---------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| **Tell the parent what to discover, not read** | "List all files in `resources/` by name to determine how many subagents to spawn — do not read their contents"        |
| **Tell subagents what to return**              | "Return only findings relevant to [topic]. Output as JSON to `{output-path}`. Do not echo raw content"                |
| **Use pre-pass scripts**                       | Run a lightweight script that extracts metadata (file names, sizes, structure) so the parent can plan without reading |
| **Be explicit about the boundary**             | "Your role is ORCHESTRATION. Scripts and subagents do all analysis"                                                   |

**Testing is how you catch this.** Run your skill and watch what actually happens. If you see the parent reading files it should be delegating, tighten the language. This is normal iteration — the builders are tuned with these patterns, but different models and tools may need more explicit guidance. Review the existing BMad quality optimizer prompts (`prompts/quality-optimizer.md`) and scanner agents (`agents/quality-scan-*.md`) for working examples of this defensive language in practice.

## Choosing a Pattern

| Need                                              | Pattern                               |
| ------------------------------------------------- | ------------------------------------- |
| Read multiple sources without bloating context    | 1 — Delegated Data Access             |
| Combine many outputs into one deliverable         | 2 — Temp File Assembly                |
| Pipeline where stages depend on each other        | 3 — Shared-File Orchestration         |
| Task needs analysis before work can be decomposed | 4 — Hierarchical Lead-Worker          |
| Quality through diverse perspectives              | 5 — Persona-Driven Parallel Reasoning |
| Iterative optimization or simulation              | 6 — Evolutionary & Emergent           |

## Implementation Notes

- Force **strict JSON schemas** on every subagent output for reliable parent parsing
- Use **git worktrees** or per-agent directories to prevent crosstalk
- Start small — one orchestrator that reads `plan.md` and spawns the first wave
- Patterns compose: use Delegated Access for data gathering, Persona-Driven for analysis, Temp File Assembly for the final report
- Always include **graceful degradation** — if subagents are unavailable, the main agent performs the work sequentially
