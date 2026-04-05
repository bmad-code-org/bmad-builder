# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml"]
# ///
"""
Dream seed tracking and success rate analysis for Dream Weaver.

Reads seed-log.yaml and calculates incubation success rates,
technique effectiveness, and correlation stats.

Usage:
    uv run scripts/seed_tracker.py --seed-log PATH [--verbose]
"""

import argparse
import json
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

import yaml


def load_seed_log(seed_log_path: Path) -> list[dict]:
    """Load and parse seed-log.yaml."""
    try:
        content = seed_log_path.read_text(encoding="utf-8")
        data = yaml.safe_load(content)
        if not data or "seeds" not in data:
            return []
        return data["seeds"]
    except (yaml.YAMLError, FileNotFoundError):
        return []


def analyze_seeds(seeds: list[dict]) -> dict:
    """Analyze seed success rates and technique effectiveness."""
    if not seeds:
        return {
            "total_seeds": 0,
            "success_rate": 0,
            "technique_stats": {},
            "result_distribution": {},
        }

    # Result distribution
    result_counts = Counter()
    technique_results = {}

    for seed in seeds:
        result = seed.get("result", "pending")
        technique = seed.get("technique", "unknown")

        result_counts[result] += 1

        if technique not in technique_results:
            technique_results[technique] = Counter()
        technique_results[technique][result] += 1

    # Overall success rate (partial + full / total non-pending)
    resolved = sum(
        count for result, count in result_counts.items() if result != "pending"
    )
    successes = result_counts.get("partial", 0) + result_counts.get("full", 0)
    success_rate = round(successes / resolved, 2) if resolved > 0 else 0

    # Technique effectiveness
    technique_stats = {}
    for technique, results in technique_results.items():
        tech_resolved = sum(
            count for result, count in results.items() if result != "pending"
        )
        tech_successes = results.get("partial", 0) + results.get("full", 0)
        technique_stats[technique] = {
            "total": sum(results.values()),
            "resolved": tech_resolved,
            "successes": tech_successes,
            "success_rate": (
                round(tech_successes / tech_resolved, 2) if tech_resolved > 0 else 0
            ),
            "results": dict(results),
        }

    # Recent trend (last 5 resolved seeds)
    resolved_seeds = [s for s in seeds if s.get("result") not in ("pending", None)]
    recent = resolved_seeds[-5:] if len(resolved_seeds) >= 5 else resolved_seeds
    recent_successes = sum(
        1 for s in recent if s.get("result") in ("partial", "full")
    )
    recent_rate = (
        round(recent_successes / len(recent), 2) if recent else 0
    )

    return {
        "total_seeds": len(seeds),
        "pending": result_counts.get("pending", 0),
        "resolved": resolved,
        "success_rate": success_rate,
        "recent_trend_rate": recent_rate,
        "result_distribution": dict(result_counts),
        "technique_stats": technique_stats,
        "best_technique": (
            max(technique_stats, key=lambda t: technique_stats[t]["success_rate"])
            if technique_stats
            else None
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Analyze dream seed success rates"
    )
    parser.add_argument(
        "--seed-log", required=True, help="Path to seed-log.yaml"
    )
    parser.add_argument(
        "--verbose", action="store_true", help="Print diagnostics to stderr"
    )
    args = parser.parse_args()

    seed_log_path = Path(args.seed_log)
    if not seed_log_path.is_file():
        print(
            json.dumps({
                "script": "seed_tracker",
                "status": "error",
                "error": f"Seed log not found: {seed_log_path}",
            }),
            file=sys.stdout,
        )
        sys.exit(2)

    seeds = load_seed_log(seed_log_path)

    if args.verbose:
        print(f"Found {len(seeds)} seed entries", file=sys.stderr)

    analysis = analyze_seeds(seeds)

    output = {
        "script": "seed_tracker",
        "version": "1.0.0",
        "seed_log_path": str(seed_log_path),
        "timestamp": datetime.now().isoformat(),
        "status": "pass",
        "analysis": analysis,
    }

    print(json.dumps(output, indent=2))
    sys.exit(0)


if __name__ == "__main__":
    main()
