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

FINDERS = [run_evals.find_adapter, run_triggers.find_adapter]


def write_adapter(path: Path) -> None:
    path.write_text(json.dumps({"invocation": ["trusted-runtime"]}),
                    encoding="utf-8")


def test_sibling_adapter_is_ignored():
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        data_file = root / "cases.json"
        sibling = root / "adapter.json"
        data_file.write_text("[]", encoding="utf-8")
        write_adapter(sibling)
        with patch.dict(os.environ, {}, clear=True):
            for find in FINDERS:
                assert find(None, data_file) is None, find.__module__


def test_explicit_adapter_is_used_even_beside_bundle():
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        data_file = root / "queries.json"
        explicit = root / "trusted" / "adapter.json"
        data_file.write_text("[]", encoding="utf-8")
        (root / "trusted").mkdir()
        write_adapter(explicit)
        (root / "adapter.json").write_text(
            json.dumps({"invocation": ["attacker-controlled"]}),
            encoding="utf-8",
        )
        with patch.dict(os.environ, {}, clear=True):
            for find in FINDERS:
                assert find(explicit, data_file) == explicit


def test_operator_environment_adapter_is_used():
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        data_file = root / "cases.json"
        configured = root / "trusted-adapter.json"
        data_file.write_text("[]", encoding="utf-8")
        write_adapter(configured)
        with patch.dict(os.environ,
                        {"BMAD_EVAL_ADAPTER": str(configured)}, clear=True):
            for find in FINDERS:
                assert find(None, data_file) == configured


if __name__ == "__main__":
    test_sibling_adapter_is_ignored()
    test_explicit_adapter_is_used_even_beside_bundle()
    test_operator_environment_adapter_is_used()
    print("ok: adapter selection requires explicit trusted configuration")
