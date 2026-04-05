# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml"]
# ///
"""
Dream recall metrics calculator for Dream Weaver.

Analyzes journal entries to calculate recall rates, streaks,
vividness trends, and quality distributions.

Usage:
    uv run scripts/recall_metrics.py --journal-path PATH [--verbose]
"""

import argparse
import json
import sys
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from pathlib import Path

import yaml


def parse_frontmatter(file_path: Path) -> dict | None:
    """Extract YAML frontmatter from a markdown file."""
    try:
        content = file_path.read_text(encoding="utf-8")
        if not content.startswith("---"):
            return None
        end = content.index("---", 3)
        return yaml.safe_load(content[3:end])
    except (ValueError, yaml.YAMLError):
        return None


def scan_journal(journal_path: Path) -> list[dict]:
    """Scan all journal entries and extract metadata."""
    entries = []
    for file in sorted(journal_path.glob("*.md")):
        fm = parse_frontmatter(file)
        if not fm:
            continue

        entry_date = fm.get("date")
        if isinstance(entry_date, str):
            try:
                entry_date = datetime.strptime(entry_date, "%Y-%m-%d").date()
            except ValueError:
                continue

        entries.append({
            "file": file.name,
            "date": entry_date,
            "vividness": fm.get("vividness"),
            "recall_quality": fm.get("recall_quality", "medium"),
            "lucid": fm.get("lucid", False),
        })

    return entries


def calculate_metrics(entries: list[dict]) -> dict:
    """Calculate recall metrics from journal entries."""
    if not entries:
        return {
            "total_dreams": 0,
            "dreams_per_week": 0,
            "current_streak": 0,
            "longest_streak": 0,
            "avg_vividness": 0,
            "vividness_trend": "insufficient_data",
            "quality_distribution": {},
            "lucid_count": 0,
            "weekly_counts": [],
        }

    # Group by date
    dreams_by_date = defaultdict(list)
    for entry in entries:
        if entry["date"]:
            dreams_by_date[entry["date"]].append(entry)

    sorted_dates = sorted(dreams_by_date.keys())

    if not sorted_dates:
        return {"total_dreams": len(entries), "error": "no_dated_entries"}

    # Date range
    first_date = sorted_dates[0]
    last_date = sorted_dates[-1]
    total_days = max((last_date - first_date).days, 1)
    total_weeks = max(total_days / 7, 1)

    # Dreams per week
    dreams_per_week = round(len(entries) / total_weeks, 1)

    # Streak calculation
    today = datetime.now().date()
    current_streak = 0
    check_date = today
    while check_date in dreams_by_date or check_date == today:
        if check_date in dreams_by_date:
            current_streak += 1
        elif check_date != today:
            break
        check_date -= timedelta(days=1)

    longest_streak = 0
    streak = 0
    for i, date in enumerate(sorted_dates):
        if i == 0 or (date - sorted_dates[i - 1]).days == 1:
            streak += 1
        else:
            longest_streak = max(longest_streak, streak)
            streak = 1
    longest_streak = max(longest_streak, streak)

    # Vividness
    vividness_scores = [
        e["vividness"] for e in entries if e["vividness"] is not None
    ]
    avg_vividness = (
        round(sum(vividness_scores) / len(vividness_scores), 1)
        if vividness_scores
        else 0
    )

    # Vividness trend (compare first half to second half)
    vividness_trend = "insufficient_data"
    if len(vividness_scores) >= 4:
        mid = len(vividness_scores) // 2
        first_half = sum(vividness_scores[:mid]) / mid
        second_half = sum(vividness_scores[mid:]) / (len(vividness_scores) - mid)
        diff = second_half - first_half
        if diff > 0.5:
            vividness_trend = "improving"
        elif diff < -0.5:
            vividness_trend = "declining"
        else:
            vividness_trend = "stable"

    # Quality distribution
    quality_counts = Counter(e["recall_quality"] for e in entries)

    # Lucid count
    lucid_count = sum(1 for e in entries if e.get("lucid"))

    # Weekly counts (last 8 weeks)
    weekly_counts = []
    for weeks_ago in range(7, -1, -1):
        week_start = today - timedelta(weeks=weeks_ago, days=today.weekday())
        week_end = week_start + timedelta(days=6)
        count = sum(
            len(dreams)
            for date, dreams in dreams_by_date.items()
            if week_start <= date <= week_end
        )
        weekly_counts.append({
            "week_start": str(week_start),
            "count": count,
        })

    return {
        "total_dreams": len(entries),
        "dreams_per_week": dreams_per_week,
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "avg_vividness": avg_vividness,
        "vividness_trend": vividness_trend,
        "quality_distribution": dict(quality_counts),
        "lucid_count": lucid_count,
        "weekly_counts": weekly_counts,
        "date_range": {
            "first": str(first_date),
            "last": str(last_date),
            "total_days": total_days,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Calculate dream recall metrics"
    )
    parser.add_argument(
        "--journal-path", required=True, help="Path to journal folder"
    )
    parser.add_argument(
        "--verbose", action="store_true", help="Print diagnostics to stderr"
    )
    args = parser.parse_args()

    journal_path = Path(args.journal_path)
    if not journal_path.is_dir():
        print(
            json.dumps({
                "script": "recall_metrics",
                "status": "error",
                "error": f"Journal path not found: {journal_path}",
            }),
            file=sys.stdout,
        )
        sys.exit(2)

    entries = scan_journal(journal_path)

    if args.verbose:
        print(f"Found {len(entries)} journal entries", file=sys.stderr)

    metrics = calculate_metrics(entries)

    output = {
        "script": "recall_metrics",
        "version": "1.0.0",
        "journal_path": str(journal_path),
        "timestamp": datetime.now().isoformat(),
        "status": "pass",
        "metrics": metrics,
    }

    print(json.dumps(output, indent=2))
    sys.exit(0)


if __name__ == "__main__":
    main()


