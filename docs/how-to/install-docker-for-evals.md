---
title: 'Install Docker for Evals'
description: Install Docker Desktop so the eval runner can give you reproducible, hermetic test runs
---

Use Docker Desktop to give the eval runner a real isolation boundary. Without Docker, the runner falls back to local mode, which is best-effort and has known leak paths.

## When to Use This

- You plan to run trigger evals (local mode can leak host skills into the workspace)
- You want runs to be reproducible across machines
- You publish a module and want the same eval verdicts other developers see
- You want a guaranteed-empty `HOME` so global memory cannot influence results

## When to Skip This

- One-off iteration on artifact evals where local fallback is good enough for now
- A constrained environment where installing Docker is not feasible. The runner falls back to local mode and tells you it is doing so.

:::note[Prerequisites]

- Administrator access on your machine to install Docker Desktop
- A few GB of disk space for the Docker Desktop application and the eval-runner image
:::

## Why Docker

The eval runner needs to start each run from a clean slate. It is trying to measure the skill, not the host's accumulated state. Without isolation, three things contaminate the result.

1. **Global memory and CLAUDE.md.** Your `~/.claude/CLAUDE.md` and auto-memory load on every Claude Code invocation. They influence outputs in ways the skill author cannot control.
2. **Ancestor configuration.** A `CLAUDE.md` anywhere above the skill in the directory tree gets discovered and loaded.
3. **Host-installed skills.** When `claude -p` runs in a directory with `.claude/skills/` somewhere up the tree, those skills are discoverable and can fire instead of (or alongside) the skill under test. This is especially harmful for trigger evals.

Docker solves all three. The container has its own filesystem, its own `HOME`, and its own `.claude/`. Local mode patches `HOME` and creates a temp directory but cannot prevent ancestor discovery.

## Step 1: Install Docker Desktop

Download Docker Desktop for your platform:

| Platform | Where to Get It                                                                                       |
| -------- | ----------------------------------------------------------------------------------------------------- |
| macOS    | [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)                  |
| Windows  | [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)                  |
| Linux    | Docker Engine via your distribution's package manager, or Docker Desktop for Linux                    |

Follow the installer's prompts. On macOS, drag the Docker app to Applications and launch it. On Windows, the installer enables WSL 2 if needed.

## Step 2: Start Docker Desktop

Launch Docker Desktop. Wait for the whale icon to indicate Docker is running. The eval runner shells out to the `docker` CLI; if Docker is not running, the runner falls back to local mode and tells you why.

## Step 3: Verify Installation

Confirm Docker is reachable from your terminal:

```bash
docker info
```

A successful response means the eval runner can use Docker. An error means Docker is not running, or the CLI cannot reach the daemon.

## Step 4: Let the Runner Build the Image

The first time you invoke the eval runner with `--isolation docker` (or `auto` when Docker is available), the runner builds `bmad-eval-runner:latest` from a Dockerfile shipped with the skill. This takes a few minutes once. Subsequent runs reuse the cached image.

The image is a minimal Node 20 base with Claude Code, Python 3, and standard tools. Nothing skill-specific or user-specific lives in the image. Your credentials are mounted in at run time, not baked in.

:::tip[Credential Safety]
The Dockerfile contains no tokens, API keys, or credentials. Your authentication (macOS Keychain credential or `ANTHROPIC_API_KEY`) is staged into a per-run temp directory and mounted into the container as a read-only volume that disappears when the container exits.
:::

## What You Get

- Reproducible runs: the same eval produces the same workspace state on any machine with the image
- Real `HOME` isolation: the container's `/home/evaluator` is empty, not just overridden
- Trigger evals you can trust: only the synthetic skill staged for the test is discoverable, not your host's installed skills
- Network can be locked down per run if your evals do not need internet access

## Tips

- Rebuild the image with `python3 scripts/docker_setup.py --rebuild` if you ever need to reset it
- Per-eval container resource use is small (a few hundred MB). Parallel workers each spin up their own container.
- If `docker info` works in one terminal but not in your editor's integrated terminal, your shell PATH probably differs. Open a fresh terminal session.

## Next Steps

Run the eval runner against a skill: see [Run Evals Against a Skill](/how-to/run-evals-against-a-skill.md). For isolation internals, see the eval-runner skill's `references/isolation.md`.
