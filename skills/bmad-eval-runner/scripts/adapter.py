"""Trusted adapter configuration helpers for the eval runners.

Adapter configuration is executable configuration: it chooses the subprocess
argv and which host environment variables are forwarded. It must therefore be
selected by an explicit command-line option or an operator-controlled
environment variable, never by a file shipped beside an untrusted eval bundle.
"""

from __future__ import annotations

import json
import os
from collections.abc import Mapping
from pathlib import Path


def find_adapter(explicit: Path | None, _data_file: Path) -> Path | None:
    """Return only explicitly selected adapter configuration.

    ``data_file`` is accepted to keep the call contract clear at both runner
    sites, but its parent directory is deliberately never searched. Cases and
    query bundles are untrusted input and may contain an adjacent adapter that
    would otherwise control command execution.
    """
    if explicit is not None:
        candidate = explicit.expanduser()
        return candidate if candidate.is_file() else None

    env_path = os.environ.get("BMAD_EVAL_ADAPTER")
    if env_path:
        candidate = Path(env_path).expanduser()
        if candidate.is_file():
            return candidate
    return None


def load_adapter(path: Path) -> dict:
    """Load and minimally validate a trusted adapter configuration."""
    cfg = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(cfg, dict):
        raise ValueError(f"adapter config must be a JSON object: {path}")
    if ("invocation" not in cfg
            or not isinstance(cfg["invocation"], list)
            or not cfg["invocation"]):
        raise ValueError("adapter config missing 'invocation' argv list")
    return cfg


def build_argv(invocation: list, prompt: str, cwd: str) -> list[str]:
    """Expand the supported prompt, query, and cwd argv placeholders."""
    argv: list[str] = []
    for tok in invocation:
        tok = str(tok)
        tok = (tok.replace("{prompt}", prompt)
               .replace("{query}", prompt)
               .replace("{cwd}", cwd))
        argv.append(tok)
    return argv


def build_case_env(adapter: Mapping | None, home_dir: Path,
                   host_env: Mapping[str, str]) -> dict[str, str]:
    """Build the minimal subprocess environment from trusted config."""
    adapter = adapter or {}
    env = {
        "PATH": host_env.get("PATH", ""),
        "HOME": str(home_dir),
        "CLAUDE_CONFIG_DIR": str(home_dir / ".claude"),
    }
    auth_env = adapter.get("auth_env")
    if auth_env:
        val = host_env.get(str(auth_env))
        if val:
            env[str(auth_env)] = val
    for key in adapter.get("env_passthrough") or []:
        val = host_env.get(str(key))
        if val is not None:
            env[str(key)] = val
    return env
