#!/usr/bin/env python3
"""Adversarial checks for fixture containment and immutable evidence."""

import json
import sys
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS_DIR))

import run_evals  # noqa: E402


def fixture(root: Path, rel: str = "fixture.txt", content: bytes = b"trusted"):
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content)
    return run_evals.resolve_fixtures([rel], root, root)


@pytest.mark.parametrize("entry", ["/etc/passwd", "../outside.txt"])
def test_rejects_absolute_and_parent_paths(tmp_path, entry):
    with pytest.raises(ValueError, match="relative without"):
        run_evals.resolve_fixtures([entry], tmp_path, tmp_path)


def test_rejects_source_symlink_escape(tmp_path):
    trusted = tmp_path / "trusted"
    trusted.mkdir()
    outside = tmp_path / "outside.txt"
    outside.write_text("secret", encoding="utf-8")
    (trusted / "escape.txt").symlink_to(outside)

    with pytest.raises(ValueError, match="escapes trusted root"):
        run_evals.resolve_fixtures(["escape.txt"], trusted, trusted)


def test_rejects_destination_symlink_escape(tmp_path):
    source = tmp_path / "source"
    fixtures = fixture(source, "nested/fixture.txt")
    cwd = tmp_path / "cwd"
    cwd.mkdir()
    outside = tmp_path / "outside"
    outside.mkdir()
    (cwd / "nested").symlink_to(outside, target_is_directory=True)

    with pytest.raises(ValueError, match="destination (escapes|traverses)"):
        run_evals.stage_fixtures(fixtures, cwd)


def test_detects_source_hash_change_before_staging(tmp_path):
    source = tmp_path / "source"
    fixtures = fixture(source)
    (source / "fixture.txt").write_text("changed", encoding="utf-8")

    with pytest.raises(ValueError, match="source changed"):
        run_evals.stage_fixtures(fixtures, tmp_path / "cwd")


def test_detects_post_run_mutation_and_preserves_snapshot(tmp_path):
    source = tmp_path / "source"
    fixtures = fixture(source)
    run_dir = tmp_path / "run"
    case_dir = run_dir / "skill" / "mutation"
    adapter = {
        "invocation": [
            sys.executable,
            "-c",
            "from pathlib import Path; Path('fixture.txt').write_text('changed')",
        ]
    }

    result = run_evals.run_case(
        {"id": "mutation", "input": "test"}, case_dir, run_dir,
        adapter, 10, "skill", None, fixtures,
    )

    assert result["status"] == "fixture-integrity-error"
    evidence = case_dir / "fixture-evidence"
    assert (evidence / "snapshot" / "fixture.txt").read_bytes() == b"trusted"
    manifest = json.loads((evidence / "manifest.json").read_text())
    assert manifest["fixtures"][0]["sha256"] == fixtures[0].sha256


def test_detects_manifest_write_attempt(tmp_path):
    source = tmp_path / "source"
    fixtures = fixture(source)
    run_dir = tmp_path / "run"
    case_dir = run_dir / "skill" / "manifest-write"
    adapter = {
        "invocation": [
            sys.executable,
            "-c",
            "from pathlib import Path; p=Path('../fixture-evidence'); "
            "p.mkdir(); (p/'manifest.json').write_text('forged')",
        ]
    }

    result = run_evals.run_case(
        {"id": "manifest-write", "input": "test"}, case_dir, run_dir,
        adapter, 10, "skill", None, fixtures,
    )

    assert result["status"] == "fixture-integrity-error"
    assert "existed before persistence" in result["error_tail"]
    assert not (case_dir / "fixture-evidence").exists()
    assert len(list(case_dir.glob("fixture-evidence-rejected-*"))) == 1


def test_cli_fails_when_adapter_mutates_fixture(tmp_path):
    project = tmp_path / "project"
    project.mkdir()
    (project / "fixture.txt").write_text("trusted", encoding="utf-8")
    cases = project / "cases.json"
    cases.write_text(json.dumps({"cases": [{
        "id": "mutation",
        "input": "test",
        "rubric": [],
        "files": ["fixture.txt"],
    }]}), encoding="utf-8")
    skill = tmp_path / "skill"
    skill.mkdir()
    (skill / "SKILL.md").write_text("# test", encoding="utf-8")
    adapter = tmp_path / "adapter.json"
    adapter.write_text(json.dumps({"invocation": [
        sys.executable,
        "-c",
        "from pathlib import Path; Path('fixture.txt').write_text('changed')",
    ]}), encoding="utf-8")
    output = tmp_path / "output"

    exit_code = run_evals.main([
        "--cases", str(cases),
        "--skill-path", str(skill),
        "--project-root", str(project),
        "--output-dir", str(output),
        "--adapter", str(adapter),
        "--workers", "1",
        "--quiet",
    ])

    assert exit_code == 1
    summary_path = next(output.glob("*/execution-summary.json"))
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    assert summary["results"][0]["status"] == "fixture-integrity-error"


def test_cli_fails_when_source_changes_before_staging(tmp_path, monkeypatch):
    project = tmp_path / "project"
    project.mkdir()
    source = project / "fixture.txt"
    source.write_text("trusted", encoding="utf-8")
    cases = project / "cases.json"
    cases.write_text(json.dumps({"cases": [{
        "id": "source-race",
        "input": "test",
        "rubric": [],
        "files": ["fixture.txt"],
    }]}), encoding="utf-8")
    skill = tmp_path / "skill"
    skill.mkdir()
    (skill / "SKILL.md").write_text("# test", encoding="utf-8")
    original_resolve = run_evals.resolve_fixtures

    def resolve_then_mutate(files, project_root, cases_dir):
        fixtures = original_resolve(files, project_root, cases_dir)
        source.write_text("changed", encoding="utf-8")
        return fixtures

    monkeypatch.setattr(run_evals, "resolve_fixtures", resolve_then_mutate)
    output = tmp_path / "output"

    exit_code = run_evals.main([
        "--cases", str(cases),
        "--skill-path", str(skill),
        "--project-root", str(project),
        "--output-dir", str(output),
        "--workers", "1",
        "--quiet",
    ])

    assert exit_code == 1
    summary_path = next(output.glob("*/execution-summary.json"))
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    assert summary["results"][0]["status"] == "fixture-integrity-error"


def test_parent_held_digest_detects_evidence_tamper(tmp_path):
    """chmod 0400 is not the trust boundary; parent-held digest is."""
    import fixture_integrity as fi

    source = tmp_path / "source"
    fixtures = fixture(source)
    case_dir = tmp_path / "case"
    case_dir.mkdir()
    trusted = fi.fixture_evidence_digest(fixtures)
    evidence_dir, digest = fi.persist_fixture_evidence(fixtures, case_dir)
    assert digest == trusted
    fi.validate_fixture_evidence(evidence_dir, trusted)

    # Same-UID process can still rewrite after chmod; digest must catch it.
    snap = evidence_dir / "snapshot" / "fixture.txt"
    snap.chmod(0o600)
    snap.write_bytes(b"forged")
    snap.chmod(0o400)

    with pytest.raises(ValueError, match="digest mismatch|hash mismatch"):
        fi.validate_fixture_evidence(evidence_dir, trusted)


def test_run_dir_is_exclusive(tmp_path):
    project = tmp_path / "project"
    project.mkdir()
    cases = project / "cases.json"
    cases.write_text(json.dumps({"cases": [{
        "id": "empty",
        "input": "test",
        "rubric": [],
        "files": [],
    }]}), encoding="utf-8")
    skill = tmp_path / "skill"
    skill.mkdir()
    (skill / "SKILL.md").write_text("# test", encoding="utf-8")
    output = tmp_path / "output"

    # Force collision on run id
    fixed = "fixed-run-id"
    monkey_ids = iter([fixed, fixed])

    def fixed_id(label):
        return next(monkey_ids)

    original = run_evals.new_run_id
    run_evals.new_run_id = fixed_id
    try:
        assert run_evals.main([
            "--cases", str(cases),
            "--skill-path", str(skill),
            "--project-root", str(project),
            "--output-dir", str(output),
            "--workers", "1",
            "--quiet",
        ]) == 0
        with pytest.raises(FileExistsError):
            run_evals.main([
                "--cases", str(cases),
                "--skill-path", str(skill),
                "--project-root", str(project),
                "--output-dir", str(output),
                "--workers", "1",
                "--quiet",
            ])
    finally:
        run_evals.new_run_id = original
