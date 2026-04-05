# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml"]
# ///
"""
Symbol frequency analysis for Dream Weaver journal entries.

Scans journal folder for dream entries with YAML frontmatter,
extracts symbols, and outputs frequency statistics as JSON.

Usage:
    uv run scripts/symbol_stats.py --journal-path PATH [--days N] [--verbose]
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


def scan_journal(journal_path: Path, days: int | None = None) -> list[dict]:
    """Scan journal entries and extract frontmatter data."""
    entries = []
    cutoff = None
    if days:
        cutoff = datetime.now().date() - timedelta(days=days)

    for file in sorted(journal_path.glob("*.md")):
        fm = parse_frontmatter(file)
        if not fm or "symbols" not in fm:
            continue

        entry_date = fm.get("date")
        if isinstance(entry_date, str):
            try:
                entry_date = datetime.strptime(entry_date, "%Y-%m-%d").date()
            except ValueError:
                continue

        if cutoff and entry_date and entry_date < cutoff:
            continue

        entries.append({
            "file": file.name,
            "date": str(entry_date) if entry_date else None,
            "symbols": fm.get("symbols", []),
            "emotions": fm.get("emotions", []),
            "vividness": fm.get("vividness"),
            "lucid": fm.get("lucid", False),
        })

    return entries


def analyze_symbols(entries: list[dict]) -> dict:
    """Analyze symbol frequency and emotion correlations."""
    symbol_count = Counter()
    symbol_emotions = defaultdict(Counter)
    symbol_dates = defaultdict(list)
    symbol_contexts = defaultdict(set)

    for entry in entries:
        symbols = entry.get("symbols", [])
        emotions = entry.get("emotions", [])
        date = entry.get("date")

        for symbol in symbols:
            symbol = symbol.lower().strip()
            symbol_count[symbol] += 1
            if date:
                symbol_dates[symbol].append(date)
            for emotion in emotions:
                symbol_emotions[symbol][emotion.lower().strip()] += 1

    results = {}
    for symbol, count in symbol_count.most_common():
        dates = sorted(symbol_dates[symbol])
        results[symbol] = {
            "count": count,
            "first_seen": dates[0] if dates else None,
            "last_seen": dates[-1] if dates else None,
            "emotion_correlation": dict(symbol_emotions[symbol]),
        }

    return results


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Analyze dream journal symbol frequency"
    )
    parser.add_argument(
        "--journal-path", required=True, help="Path to journal folder"
    )
    parser.add_argument(
        "--days", type=int, default=None, help="Limit to last N days"
    )
    parser.add_argument(
        "--verbose", action="store_true", help="Print diagnostics to stderr"
    )
    args = parser.parse_args()

    journal_path = Path(args.journal_path)
    if not journal_path.is_dir():
        print(
            json.dumps({
                "script": "symbol_stats",
                "status": "error",
                "error": f"Journal path not found: {journal_path}",
            }),
            file=sys.stdout,
        )
        sys.exit(2)

    entries = scan_journal(journal_path, args.days)

    if args.verbose:
        print(f"Found {len(entries)} journal entries", file=sys.stderr)

    symbols = analyze_symbols(entries)

    output = {
        "script": "symbol_stats",
        "version": "1.0.0",
        "journal_path": str(journal_path),
        "timestamp": datetime.now().isoformat(),
        "status": "pass",
        "entries_scanned": len(entries),
        "unique_symbols": len(symbols),
        "symbols": symbols,
        "summary": {
            "total_symbols": sum(s["count"] for s in symbols.values()),
            "unique_symbols": len(symbols),
            "top_5": [
                {"symbol": s, "count": symbols[s]["count"]}
                for s in list(symbols.keys())[:5]
            ],
        },
    }

    print(json.dumps(output, indent=2))
    sys.exit(0)


if __name__ == "__main__":
    main()
