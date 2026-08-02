#!/usr/bin/env python3
"""Guard the adapter trust boundary in both eval runners."""

import json
import os
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

SCRIPTS_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS_DIR))

import run_evals  # noqa: E402
import run_triggers  # noqa: E402

FINDERS = [
    ("run_evals", run_evals.find_adapter),
    ("run_triggers", run_triggers.find_adapter),
]


def write_adapter(path: Path) -> None:
    path.write_text(json.dumps({"invocation": ["trusted-runtime"]}),
                    encoding="utf-8")


def test_sibling_adapter_is_ignored():
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        data_file = root / "cases.json"
        data_file.write_text("[]", encoding="utf-8")
        for filename in ("adapter.json", ".bmad-eval-adapter.json"):
            write_adapter(root / filename)
        with patch.dict(os.environ, {}, clear=True):
            for runner, find in FINDERS:
                assert find(None, data_file) is None, runner


def test_explicit_adapter_is_used_even_beside_bundle():
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        data_file = root / "queries.json"
        explicit = root / "trusted" / "adapter.json"
        configured = root / "trusted" / "env-adapter.json"
        data_file.write_text("[]", encoding="utf-8")
        (root / "trusted").mkdir()
        write_adapter(explicit)
        write_adapter(configured)
        for filename in ("adapter.json", ".bmad-eval-adapter.json"):
            (root / filename).write_text(
                json.dumps({"invocation": ["attacker-controlled"]}),
                encoding="utf-8",
            )
        with patch.dict(os.environ,
                        {"BMAD_EVAL_ADAPTER": str(configured)}, clear=True):
            for runner, find in FINDERS:
                assert find(explicit, data_file) == explicit, runner


def test_operator_environment_adapter_is_used():
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        data_file = root / "cases.json"
        configured = root / "trusted-adapter.json"
        data_file.write_text("[]", encoding="utf-8")
        write_adapter(configured)
        with patch.dict(os.environ,
                        {"BMAD_EVAL_ADAPTER": str(configured)}, clear=True):
            for runner, find in FINDERS:
                assert find(None, data_file) == configured, runner


def test_empty_invocation_is_rejected():
    with tempfile.TemporaryDirectory() as temp:
        config = Path(temp) / "empty.json"
        config.write_text(json.dumps({"invocation": []}), encoding="utf-8")
        for runner in (run_evals, run_triggers):
            try:
                runner.load_adapter(config)
            except ValueError as exc:
                assert "invocation" in str(exc), runner.__name__
            else:
                raise AssertionError(
                    f"{runner.__name__} accepted an empty invocation")


if __name__ == "__main__":
    test_sibling_adapter_is_ignored()
    test_explicit_adapter_is_used_even_beside_bundle()
    test_operator_environment_adapter_is_used()
    test_empty_invocation_is_rejected()
    print("ok: adapter selection requires explicit trusted configuration")
