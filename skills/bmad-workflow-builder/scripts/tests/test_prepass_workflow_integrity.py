#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# ///
"""Tests for prepass-workflow-integrity.py.

Focuses on the discovery + cross-reference behaviour for the modern
`steps-c/step-NN-<slug>.md` layout (and nested `steps-c/sub/` subdirs)
that the prior version of the script could not see — producing
false-positive `critical/missing-stage` findings on every skill that
used the layout.
"""

from __future__ import annotations

import sys
import tempfile
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

import pytest

# Load the script as a module
_script_path = Path(__file__).resolve().parent.parent / 'prepass-workflow-integrity.py'
_spec = spec_from_file_location('prepass_workflow_integrity', _script_path)
_mod = module_from_spec(_spec)
_spec.loader.exec_module(_mod)


@pytest.fixture
def tmp_skill():
    """Yield (skill_path: Path) for a temp skill dir cleaned up at the end."""
    with tempfile.TemporaryDirectory() as td:
        yield Path(td)


def _write(p: Path, content: str = "stub") -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding='utf-8')


# ─── discover_step_files ─────────────────────────────────────────────────────


def test_discovers_steps_c_layout(tmp_skill):
    """The modern `steps-c/step-NN-<slug>.md` layout is found."""
    _write(tmp_skill / 'SKILL.md')
    _write(tmp_skill / 'steps-c' / 'step-01-detect.md')
    _write(tmp_skill / 'steps-c' / 'step-02-write.md')

    found = {p.name for p in _mod.discover_step_files(tmp_skill)}
    assert found == {'step-01-detect.md', 'step-02-write.md'}


def test_discovers_legacy_root_layout(tmp_skill):
    """The legacy `NN-<slug>.md` at skill root still works."""
    _write(tmp_skill / 'SKILL.md')
    _write(tmp_skill / '01-foo.md')
    _write(tmp_skill / '02-bar.md')

    found = {p.name for p in _mod.discover_step_files(tmp_skill)}
    assert found == {'01-foo.md', '02-bar.md'}


def test_discovers_nested_sub_directory(tmp_skill):
    """Nested `steps-c/sub/` (e.g. for sub-step files) is walked."""
    _write(tmp_skill / 'SKILL.md')
    _write(tmp_skill / 'steps-c' / 'step-01-main.md')
    _write(tmp_skill / 'steps-c' / 'sub' / 'step-01b-detail.md')
    _write(tmp_skill / 'steps-c' / 'sub' / 'step-01c-more.md')

    found = {str(p.relative_to(tmp_skill)).replace('\\', '/') for p in _mod.discover_step_files(tmp_skill)}
    assert found == {
        'steps-c/step-01-main.md',
        'steps-c/sub/step-01b-detail.md',
        'steps-c/sub/step-01c-more.md',
    }


def test_recognizes_letter_suffix_step_numbers(tmp_skill):
    """`step-01b-...` (sub-stage with letter suffix) is recognized."""
    _write(tmp_skill / 'SKILL.md')
    _write(tmp_skill / 'steps-c' / 'step-01-main.md')
    _write(tmp_skill / 'steps-c' / 'step-01b-detail.md')
    _write(tmp_skill / 'steps-c' / 'step-01c-extra.md')

    found = {p.name for p in _mod.discover_step_files(tmp_skill)}
    assert found == {'step-01-main.md', 'step-01b-detail.md', 'step-01c-extra.md'}


def test_skips_skill_md_and_non_numbered_md(tmp_skill):
    _write(tmp_skill / 'SKILL.md')
    _write(tmp_skill / 'README.md')
    _write(tmp_skill / 'steps-c' / 'README.md')
    _write(tmp_skill / 'steps-c' / 'step-01-yes.md')

    found = {p.name for p in _mod.discover_step_files(tmp_skill)}
    assert found == {'step-01-yes.md'}


def test_supports_steps_a_and_steps_b_subdirs(tmp_skill):
    """Other conventional stage subdirs (steps-a, steps-b, prompts) work too."""
    _write(tmp_skill / 'SKILL.md')
    _write(tmp_skill / 'steps-a' / 'step-01-a.md')
    _write(tmp_skill / 'steps-b' / 'step-01-b.md')
    _write(tmp_skill / 'prompts' / '01-legacy.md')

    found = {p.name for p in _mod.discover_step_files(tmp_skill)}
    assert found == {'step-01-a.md', 'step-01-b.md', '01-legacy.md'}


# ─── cross_reference_stages ─────────────────────────────────────────────────


_SKILL_MD_STEPS_C = """---
name: example
description: Example. Use when testing.
---

# Example

## Stages

| # | Step | File |
|---|------|------|
| 1 | Detect | steps-c/step-01-detect.md |
| 2 | Write  | steps-c/step-02-write.md |

## On Activation

Load `steps-c/step-01-detect.md`.
"""


_SKILL_MD_NESTED_SUB = """---
name: example
description: Example with nested sub. Use when testing.
---

# Example

## Stages

| # | Step | File |
|---|------|------|
| 1  | Main      | steps-c/step-01-main.md |
| 1b | Sub-step  | steps-c/sub/step-01b-detail.md |

## On Activation

Begin at `steps-c/step-01-main.md`.
"""


def test_cross_reference_no_false_positive_critical_for_steps_c(tmp_skill):
    """The bug this PR fixes: steps-c references must not produce missing-stage criticals."""
    _write(tmp_skill / 'SKILL.md', _SKILL_MD_STEPS_C)
    _write(tmp_skill / 'steps-c' / 'step-01-detect.md')
    _write(tmp_skill / 'steps-c' / 'step-02-write.md')

    summary, findings = _mod.cross_reference_stages(tmp_skill, _SKILL_MD_STEPS_C)
    missing = [f for f in findings if f.get('category') == 'missing-stage']
    # Orphan findings have category 'naming' AND an `issue` text that begins
    # with the canonical "Stage file exists but not referenced in SKILL.md"
    # prefix that prepass-workflow-integrity.py emits at line 276. Match the
    # exact shape — the prior `'orphaned' in issue` substring check was dead
    # code (the script never uses that word) and the `or 'not referenced'`
    # disjunct was un-parenthesised, so it would have matched any finding
    # regardless of category. CodeRabbit caught both bugs on PR #82.
    orphaned = [
        f for f in findings
        if f.get('category') == 'naming'
        and f.get('issue', '').startswith('Stage file exists but not referenced in SKILL.md')
    ]
    assert missing == [], f"unexpected missing-stage findings: {missing}"
    assert orphaned == [], f"unexpected orphaned-stage findings: {orphaned}"
    assert summary['total_stages'] == 2


def test_cross_reference_resolves_nested_sub_paths(tmp_skill):
    """`steps-c/sub/step-NN-...` references resolve against nested files."""
    _write(tmp_skill / 'SKILL.md', _SKILL_MD_NESTED_SUB)
    _write(tmp_skill / 'steps-c' / 'step-01-main.md')
    _write(tmp_skill / 'steps-c' / 'sub' / 'step-01b-detail.md')

    summary, findings = _mod.cross_reference_stages(tmp_skill, _SKILL_MD_NESTED_SUB)
    missing = [f for f in findings if f.get('category') == 'missing-stage']
    assert missing == [], f"unexpected missing-stage findings: {missing}"
    assert 'steps-c/sub/step-01b-detail.md' in summary['actual']


def test_letter_suffix_does_not_create_phantom_numbering_gap(tmp_skill):
    """1, 1b, 2, 3 is a well-formed sequence (1b is a sub-stage of 1, not a gap)."""
    _write(tmp_skill / 'SKILL.md', _SKILL_MD_NESTED_SUB)
    _write(tmp_skill / 'steps-c' / 'step-01-main.md')
    _write(tmp_skill / 'steps-c' / 'sub' / 'step-01b-detail.md')

    summary, findings = _mod.cross_reference_stages(tmp_skill, _SKILL_MD_NESTED_SUB)
    naming_gap_findings = [
        f for f in findings
        if f.get('category') == 'naming' and 'gap' in f.get('issue', '').lower()
    ]
    assert naming_gap_findings == [], f"unexpected gap finding: {naming_gap_findings}"


def test_genuinely_missing_stage_is_still_caught(tmp_skill):
    """Sanity: when SKILL.md references a file that truly doesn't exist, we still flag it."""
    skill_md = _SKILL_MD_STEPS_C  # references step-01 and step-02
    _write(tmp_skill / 'SKILL.md', skill_md)
    _write(tmp_skill / 'steps-c' / 'step-01-detect.md')
    # step-02 NOT created

    _summary, findings = _mod.cross_reference_stages(tmp_skill, skill_md)
    missing = [f for f in findings if f.get('category') == 'missing-stage']
    assert any('step-02-write.md' in f['issue'] for f in missing), \
        f"genuinely missing file was not flagged: {findings}"


def test_genuinely_orphaned_stage_is_still_caught(tmp_skill):
    """Sanity: when a step file exists but isn't referenced, we still flag it."""
    _write(tmp_skill / 'SKILL.md', _SKILL_MD_STEPS_C)
    _write(tmp_skill / 'steps-c' / 'step-01-detect.md')
    _write(tmp_skill / 'steps-c' / 'step-02-write.md')
    _write(tmp_skill / 'steps-c' / 'step-99-orphan.md')

    _summary, findings = _mod.cross_reference_stages(tmp_skill, _SKILL_MD_STEPS_C)
    # Use the same canonical-prefix match as test_cross_reference_no_false_positive_critical_for_steps_c
    # so both tests share one definition of "what an orphan finding looks like".
    orphan_msgs = [
        f['issue'] for f in findings
        if f.get('category') == 'naming'
        and f.get('issue', '').startswith('Stage file exists but not referenced in SKILL.md')
    ]
    assert any('step-99-orphan.md' in msg for msg in orphan_msgs), \
        f"orphaned file was not flagged: {findings}"
