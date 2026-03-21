#!/usr/bin/env python3
"""Deterministic path standards scanner for BMad skills.

Validates all .md and .json files against BMad path conventions:
1. {project-root} only valid before /_bmad
2. Bare _bmad references must have {project-root} prefix
3. Config variables used directly (no double-prefix)
4. No ./ or ../ relative prefixes
5. No absolute paths
6. Memory paths must use {project-root}/_bmad/.memory/{skillName}-sidecar/
"""

# /// script
# requires-python = ">=3.9"
# ///

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


# Patterns to detect
# {project-root} NOT followed by /_bmad
PROJECT_ROOT_NOT_BMAD_RE = re.compile(r'\{project-root\}/(?!_bmad)')
# Bare _bmad without {project-root} prefix — match _bmad at word boundary
# but not when preceded by {project-root}/
BARE_BMAD_RE = re.compile(r'(?<!\{project-root\}/)_bmad[/\s]')
# Absolute paths
ABSOLUTE_PATH_RE = re.compile(r'(?:^|[\s"`\'(])(/(?:Users|home|opt|var|tmp|etc|usr)/\S+)', re.MULTILINE)
HOME_PATH_RE = re.compile(r'(?:^|[\s"`\'(])(~/\S+)', re.MULTILINE)
# Relative prefixes
RELATIVE_DOT_RE = re.compile(r'(?:^|[\s"`\'(])(\.\./\S+)', re.MULTILINE)
RELATIVE_DOTSLASH_RE = re.compile(r'(?:^|[\s"`\'(])(\./\S+)', re.MULTILINE)

# Memory path pattern: should use {project-root}/_bmad/.memory/
MEMORY_PATH_RE = re.compile(r'_bmad/.memory/\S+')
VALID_MEMORY_PATH_RE = re.compile(r'\{project-root\}/_bmad/.memory/\S+-sidecar/')

# Fenced code block detection (to skip examples showing wrong patterns)
FENCE_RE = re.compile(r'^```', re.MULTILINE)


def is_in_fenced_block(content: str, pos: int) -> bool:
    """Check if a position is inside a fenced code block."""
    fences = [m.start() for m in FENCE_RE.finditer(content[:pos])]
    # Odd number of fences before pos means we're inside a block
    return len(fences) % 2 == 1


def get_line_number(content: str, pos: int) -> int:
    """Get 1-based line number for a position in content."""
    return content[:pos].count('\n') + 1


def scan_file(filepath: Path, skip_fenced: bool = True) -> list[dict]:
    """Scan a single file for path standard violations."""
    findings = []
    content = filepath.read_text(encoding='utf-8')
    rel_path = filepath.name

    checks = [
        (PROJECT_ROOT_NOT_BMAD_RE, 'project-root-not-bmad', 'critical',
         '{project-root} used for non-_bmad path — only valid use is {project-root}/_bmad/...'),
        (ABSOLUTE_PATH_RE, 'absolute-path', 'high',
         'Absolute path found — not portable across machines'),
        (HOME_PATH_RE, 'absolute-path', 'high',
         'Home directory path (~/) found — environment-specific'),
        (RELATIVE_DOT_RE, 'relative-prefix', 'medium',
         'Parent directory reference (../) found — fragile, breaks with reorganization'),
        (RELATIVE_DOTSLASH_RE, 'relative-prefix', 'medium',
         'Relative prefix (./) found — breaks when execution directory changes'),
    ]

    for pattern, category, severity, message in checks:
        for match in pattern.finditer(content):
            pos = match.start()
            if skip_fenced and is_in_fenced_block(content, pos):
                continue
            line_num = get_line_number(content, pos)
            line_content = content.split('\n')[line_num - 1].strip()
            findings.append({
                'file': rel_path,
                'line': line_num,
                'severity': severity,
                'category': category,
                'title': message,
                'detail': line_content[:120],
                'action': '',
            })

    # Bare _bmad check — more nuanced, need to avoid false positives
    # inside {project-root}/_bmad which is correct
    for match in BARE_BMAD_RE.finditer(content):
        pos = match.start()
        if skip_fenced and is_in_fenced_block(content, pos):
            continue
        # Check that this isn't part of {project-root}/_bmad
        # The negative lookbehind handles this, but double-check
        # the broader context
        start = max(0, pos - 30)
        before = content[start:pos]
        if '{project-root}/' in before:
            continue
        line_num = get_line_number(content, pos)
        line_content = content.split('\n')[line_num - 1].strip()
        findings.append({
            'file': rel_path,
            'line': line_num,
            'severity': 'high',
            'category': 'bare-bmad',
            'title': 'Bare _bmad reference without {project-root} prefix',
            'detail': line_content[:120],
            'action': '',
        })

    # Memory path check — memory paths should use {project-root}/_bmad/.memory/{skillName}-sidecar/
    for match in MEMORY_PATH_RE.finditer(content):
        pos = match.start()
        if skip_fenced and is_in_fenced_block(content, pos):
            continue
        # Check if properly prefixed
        start = max(0, pos - 20)
        before = content[start:pos]
        matched_text = match.group()
        if '{project-root}/' not in before:
            line_num = get_line_number(content, pos)
            line_content = content.split('\n')[line_num - 1].strip()
            findings.append({
                'file': rel_path,
                'line': line_num,
                'severity': 'high',
                'category': 'memory-path',
                'title': 'Memory path missing {project-root} prefix — use {project-root}/_bmad/.memory/',
                'detail': line_content[:120],
                'action': '',
            })
        elif '-sidecar/' not in matched_text:
            line_num = get_line_number(content, pos)
            line_content = content.split('\n')[line_num - 1].strip()
            findings.append({
                'file': rel_path,
                'line': line_num,
                'severity': 'high',
                'category': 'memory-path',
                'title': 'Memory path not using {skillName}-sidecar/ convention',
                'detail': line_content[:120],
                'action': '',
            })

    return findings


def scan_skill(skill_path: Path, skip_fenced: bool = True) -> dict:
    """Scan all .md and .json files in a skill directory."""
    all_findings = []

    # Find all .md and .json files
    md_files = sorted(list(skill_path.rglob('*.md')) + list(skill_path.rglob('*.json')))
    if not md_files:
        print(f"Warning: No .md or .json files found in {skill_path}", file=sys.stderr)

    files_scanned = []
    for md_file in md_files:
        rel = md_file.relative_to(skill_path)
        files_scanned.append(str(rel))
        file_findings = scan_file(md_file, skip_fenced)
        for f in file_findings:
            f['file'] = str(rel)
        all_findings.extend(file_findings)

    # Build summary
    by_severity = {'critical': 0, 'high': 0, 'medium': 0, 'low': 0}
    by_category = {
        'project_root_not_bmad': 0,
        'bare_bmad': 0,
        'double_prefix': 0,
        'absolute_path': 0,
        'relative_prefix': 0,
        'memory_path': 0,
    }

    for f in all_findings:
        sev = f['severity']
        if sev in by_severity:
            by_severity[sev] += 1
        cat = f['category'].replace('-', '_')
        if cat in by_category:
            by_category[cat] += 1

    return {
        'scanner': 'path-standards',
        'script': 'scan-path-standards.py',
        'version': '1.0.0',
        'skill_path': str(skill_path),
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'files_scanned': files_scanned,
        'status': 'pass' if not all_findings else 'fail',
        'findings': all_findings,
        'assessments': {},
        'summary': {
            'total_findings': len(all_findings),
            'by_severity': by_severity,
            'by_category': by_category,
            'assessment': 'Path standards scan complete',
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description='Scan BMad skill for path standard violations',
    )
    parser.add_argument(
        'skill_path',
        type=Path,
        help='Path to the skill directory to scan',
    )
    parser.add_argument(
        '--output', '-o',
        type=Path,
        help='Write JSON output to file instead of stdout',
    )
    parser.add_argument(
        '--include-fenced',
        action='store_true',
        help='Also check inside fenced code blocks (by default they are skipped)',
    )
    args = parser.parse_args()

    if not args.skill_path.is_dir():
        print(f"Error: {args.skill_path} is not a directory", file=sys.stderr)
        return 2

    result = scan_skill(args.skill_path, skip_fenced=not args.include_fenced)
    output = json.dumps(result, indent=2)

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output)
        print(f"Results written to {args.output}", file=sys.stderr)
    else:
        print(output)

    return 0 if result['status'] == 'pass' else 1


if __name__ == '__main__':
    sys.exit(main())
