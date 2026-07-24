"""Contain, stage, and attest eval fixture evidence."""

from __future__ import annotations

import hashlib
import json
import stat
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


@dataclass(frozen=True)
class Fixture:
    __slots__ = ("source", "dest_rel", "content", "sha256", "mode")

    source: Path
    dest_rel: Path
    content: bytes
    sha256: str
    mode: int


class FixtureError(ValueError):
    pass


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def _fixture_relative_path(entry: str | Path) -> Path:
    rel = Path(str(entry))
    if rel.is_absolute() or ".." in rel.parts:
        raise FixtureError(
            f"fixture path must be relative without '..': {entry}"
        )
    if not rel.parts or rel == Path("."):
        raise FixtureError(f"fixture path must name a file: {entry}")
    return rel


def _contained(path: Path, root: Path, label: str) -> Path:
    root = root.resolve()
    resolved = path.resolve(strict=True)
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise FixtureError(f"{label} escapes trusted root: {path}") from exc
    return resolved


def resolve_fixtures(files: list, project_root: Path,
                     cases_dir: Path) -> list[Fixture]:
    roots = tuple(dict.fromkeys((project_root.resolve(), cases_dir.resolve())))
    fixtures: list[Fixture] = []
    destinations: set[Path] = set()
    for entry in files or []:
        rel = _fixture_relative_path(entry)
        if rel in destinations:
            raise FixtureError(f"duplicate fixture destination: {rel}")
        for root in roots:
            candidate = root / rel
            if candidate.exists() or candidate.is_symlink():
                source = _contained(candidate, root, "fixture source")
                if not source.is_file():
                    raise FixtureError(
                        f"fixture source is not a file: {candidate}"
                    )
                content = source.read_bytes()
                fixtures.append(Fixture(
                    source=source,
                    dest_rel=rel,
                    content=content,
                    sha256=sha256_bytes(content),
                    mode=stat.S_IMODE(source.stat().st_mode),
                ))
                destinations.add(rel)
                break
        else:
            raise FixtureError(f"fixture not found in trusted roots: {entry}")
    return fixtures


def _fixture_destination(root: Path, dest_rel: Path) -> Path:
    root = root.resolve()
    dest = root / dest_rel
    try:
        dest.resolve(strict=False).relative_to(root)
    except ValueError as exc:
        raise FixtureError(
            f"fixture destination escapes root: {dest_rel}"
        ) from exc
    current = root
    for part in dest_rel.parts[:-1]:
        current /= part
        if current.is_symlink():
            raise FixtureError(
                f"fixture destination traverses symlink: {dest_rel}"
            )
    if dest.is_symlink():
        raise FixtureError(f"fixture destination is a symlink: {dest_rel}")
    return dest


def stage_fixtures(fixtures: list[Fixture], cwd: Path) -> None:
    for fixture in fixtures:
        if sha256_file(fixture.source) != fixture.sha256:
            raise FixtureError(
                f"fixture source changed before staging: {fixture.dest_rel}"
            )
        dest = _fixture_destination(cwd, fixture.dest_rel)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(fixture.content)
        dest.chmod(fixture.mode)
        if sha256_file(dest) != fixture.sha256:
            raise FixtureError(
                f"staged fixture hash mismatch: {fixture.dest_rel}"
            )


def verify_staged_fixtures(fixtures: list[Fixture], cwd: Path) -> list[str]:
    errors: list[str] = []
    for fixture in fixtures:
        try:
            dest = _fixture_destination(cwd, fixture.dest_rel)
            actual = sha256_file(dest)
        except (FileNotFoundError, OSError, RuntimeError, ValueError) as exc:
            errors.append(f"{fixture.dest_rel}: {exc}")
            continue
        if actual != fixture.sha256:
            errors.append(
                f"{fixture.dest_rel}: expected {fixture.sha256}, got {actual}"
            )
    return errors


def _records_digest(records: list[dict]) -> str:
    canonical = json.dumps(
        sorted(records, key=lambda item: item["path"]),
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return f"sha256:{sha256_bytes(canonical)}"


def fixture_evidence_digest(fixtures: list[Fixture]) -> str:
    return _records_digest([{
        "path": fixture.dest_rel.as_posix(),
        "sha256": fixture.sha256,
        "size": len(fixture.content),
    } for fixture in fixtures])


def persist_fixture_evidence(fixtures: list[Fixture],
                             case_dir: Path) -> tuple[Path, str]:
    """Persist evidence after adapter exit and return its stdout trust anchor."""
    evidence_dir = case_dir / "fixture-evidence"
    if evidence_dir.exists() or evidence_dir.is_symlink():
        rejected = case_dir / f"fixture-evidence-rejected-{time.time_ns()}"
        evidence_dir.rename(rejected)
        raise FixtureError("fixture evidence path existed before persistence")
    snapshot_dir = evidence_dir / "snapshot"
    snapshot_dir.mkdir(parents=True)
    records = []
    for fixture in fixtures:
        dest = _fixture_destination(snapshot_dir, fixture.dest_rel)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(fixture.content)
        dest.chmod(0o400)
        records.append({
            "path": fixture.dest_rel.as_posix(),
            "sha256": fixture.sha256,
            "size": len(fixture.content),
        })
    digest = _records_digest(records)
    manifest_path = evidence_dir / "manifest.json"
    manifest_path.write_text(json.dumps({
        "schema": "bmad-fixture-evidence/v1",
        "captured_at": datetime.now(timezone.utc).strftime(
            "%Y-%m-%dT%H:%M:%SZ"
        ),
        "artifact_digest": digest,
        "fixtures": records,
    }, indent=2) + "\n", encoding="utf-8")
    manifest_path.chmod(0o400)
    for directory in sorted(
            (p for p in snapshot_dir.rglob("*") if p.is_dir()), reverse=True):
        directory.chmod(0o500)
    snapshot_dir.chmod(0o500)
    evidence_dir.chmod(0o500)
    validate_fixture_evidence(evidence_dir, digest)
    return evidence_dir, digest


def validate_fixture_evidence(evidence_dir: Path,
                              expected_digest: str) -> None:
    """Fail unless snapshot, manifest, and caller-held digest agree exactly."""
    manifest = json.loads(
        (evidence_dir / "manifest.json").read_text(encoding="utf-8")
    )
    if not isinstance(manifest, dict) or (
            manifest.get("schema") != "bmad-fixture-evidence/v1"):
        raise FixtureError("fixture evidence manifest schema is invalid")
    raw_records = manifest.get("fixtures")
    if not isinstance(raw_records, list):
        raise FixtureError("fixture evidence records are invalid")
    snapshot_dir = evidence_dir / "snapshot"
    records = []
    paths: set[Path] = set()
    for item in raw_records:
        if not isinstance(item, dict):
            raise FixtureError("fixture evidence record is invalid")
        rel = _fixture_relative_path(item.get("path", ""))
        if rel in paths:
            raise FixtureError(f"duplicate fixture evidence path: {rel}")
        content = _fixture_destination(snapshot_dir, rel).read_bytes()
        record = {
            "path": rel.as_posix(),
            "sha256": sha256_bytes(content),
            "size": len(content),
        }
        if record != item:
            raise FixtureError(f"fixture evidence hash mismatch: {rel}")
        records.append(record)
        paths.add(rel)
    actual_paths = {
        path.relative_to(snapshot_dir)
        for path in snapshot_dir.rglob("*") if path.is_file()
    }
    if actual_paths != paths:
        raise FixtureError("fixture evidence snapshot file set is invalid")
    actual_digest = _records_digest(records)
    if (actual_digest != expected_digest or
            manifest.get("artifact_digest") != expected_digest):
        raise FixtureError("fixture evidence digest mismatch")
