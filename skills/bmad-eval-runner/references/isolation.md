# Isolation Strategies

The eval runner offers two strategies. The intent is identical in both: every eval starts from a clean slate so the result reflects the skill itself, not the host's accumulated state.

## What we are isolating from

- The user's global `~/.claude/CLAUDE.md` (private global instructions)
- Any ancestor `CLAUDE.md` in the project tree above the skill
- Auto-memory at `~/.claude/projects/.../memory/MEMORY.md`
- Cached settings, MCP configurations, IDE integrations
- Prior conversation context bleeding via the shell

## Docker (preferred)

A single image, `bmad-eval-runner:latest`, is built once per machine. It contains Node 20, Claude Code (via `npm install -g @anthropic-ai/claude-code`), Python 3, and standard tools. The image is intentionally minimal — every eval starts from this baseline.

### Image build

`scripts/docker_setup.py --build` builds the image from `assets/Dockerfile`. This runs once. Re-runs are a no-op unless `--rebuild` is passed.

### Per-eval container

Each eval gets a fresh container:

```
docker run --rm \
  -v "<project-root>:/project:ro" \
  -v "<output-dir>/<eval-id>:/output" \
  -v "<fixtures-dir>:/fixtures:ro" \
  -e ANTHROPIC_API_KEY \
  -e EVAL_PROMPT \
  -e EVAL_ID \
  -e SKILL_PATH \
  bmad-eval-runner:latest \
  /bin/bash -c "/scripts/run_one_eval.sh"
```

Inside the container:

1. The project is copied from `/project` (read-only) to `/workspace` (writable, container-local). Copy is fast because the underlying layer is shared.
2. Fixtures are copied into `/workspace/fixtures/`.
3. `HOME` is `/home/evaluator`, an empty directory created by the image — no global `CLAUDE.md`, no memory.
4. `claude -p "$EVAL_PROMPT" --output-format stream-json --verbose` runs at `/workspace`.
5. The stream-json transcript is captured to `/output/transcript.jsonl`. Any files the skill writes under `/workspace` are rsynced to `/output/artifacts/` after the run completes.
6. The container exits and is removed automatically.

The host then has `<output-dir>/<eval-id>/transcript.jsonl`, `<output-dir>/<eval-id>/artifacts/`, and timing data. Nothing on the host is touched.

### Why Docker is preferred

- The image is reproducible — every run starts from byte-identical state.
- `HOME` is genuinely empty, not just overridden.
- Filesystem isolation is real, not just convention.
- Network can be locked down (`--network=none` for trigger evals; full network for artifact evals that may need it).

## Local fallback

When Docker is unavailable, the runner falls back to per-eval temp directories under `~/bmad-evals/<run-id>/<eval-id>/`. Layout:

```
~/bmad-evals/<run-id>/<eval-id>/
  workspace/         # the eval's working directory
    .home/           # HOME override — empty .claude/ inside
    project/         # rsync'd copy of <project-root>
    fixtures/        # staged fixture files
  transcript.jsonl   # claude -p stream output
  artifacts/         # files Claude wrote under workspace/
  metrics.json
```

Per-eval invocation roughly:

```
HOME="$WORKSPACE/.home" \
CLAUDE_CONFIG_DIR="$WORKSPACE/.home/.claude" \
ANTHROPIC_API_KEY="$ANTHROPIC_API_KEY" \
  claude -p "$EVAL_PROMPT" \
    --output-format stream-json --verbose \
    > transcript.jsonl
```

### Limitations of local mode

- `HOME` override prevents global `CLAUDE.md` and memory loading, but a stray ancestor `CLAUDE.md` above the project copy will still be discovered if `<project-root>` is itself nested. The runner detects this and either (a) walks up and copies just the project subtree, or (b) warns the user that ancestor discovery may still occur.
- Filesystem isolation is by convention only — the skill could write outside its workspace if it tries. We don't sandbox syscalls.
- Network is unrestricted.

Tell the user clearly when local mode is in use and that it is best-effort.

## Why not `--add-dir` only?

`claude -p --add-dir <skill>` would let Claude see the skill but would still inherit the user's `CLAUDE.md` and memory from the cwd's ancestors. The whole point of this runner is to test the skill, not the host's accumulated state. So we always either Docker-isolate or temp-dir-isolate.

## Artifact retention

Run folders are never deleted by this skill. Disk management is the user's responsibility. The runner emits the run folder path on completion; users who want to clean up old runs can delete `~/bmad-evals/<run-id>/` directly.
