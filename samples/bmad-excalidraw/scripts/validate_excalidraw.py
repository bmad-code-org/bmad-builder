# /// script
# requires-python = ">=3.9"
# ///
"""
Excalidraw File Validator

Validates .excalidraw files for structural correctness.

Usage:
    uv run validate_excalidraw.py path/to/diagram.excalidraw
    uv run validate_excalidraw.py path/to/diagram.excalidraw -o report.json

Exit codes: 0=pass, 1=fail, 2=error
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

VALID_ELEMENT_TYPES = {
    "rectangle", "ellipse", "diamond", "arrow", "line",
    "freedraw", "text", "image", "frame",
}

VALID_FILL_STYLES = {"solid", "hachure", "cross-hatch", "zigzag", "dots", "dashed", "zigzag-line"}
VALID_STROKE_STYLES = {"solid", "dashed", "dotted"}
VALID_TEXT_ALIGN = {"left", "center", "right"}
VALID_VERTICAL_ALIGN = {"top", "middle"}
VALID_ARROWHEADS = {None, "arrow", "bar", "dot", "triangle"}


def validate(file_path):
    """Validate an .excalidraw file and return findings."""
    findings = []

    try:
        data = json.loads(Path(file_path).read_text())
    except json.JSONDecodeError as e:
        findings.append({
            "severity": "critical",
            "category": "parse",
            "location": {"file": str(file_path)},
            "issue": f"Invalid JSON: {e}",
            "fix": "Fix JSON syntax errors",
        })
        return findings
    except FileNotFoundError:
        findings.append({
            "severity": "critical",
            "category": "file",
            "location": {"file": str(file_path)},
            "issue": "File not found",
            "fix": "Check the file path",
        })
        return findings

    # Top-level structure
    if data.get("type") != "excalidraw":
        findings.append({
            "severity": "critical",
            "category": "structure",
            "location": {"file": str(file_path)},
            "issue": f"Invalid type field: '{data.get('type')}', expected 'excalidraw'",
            "fix": "Set type to 'excalidraw'",
        })

    if "elements" not in data:
        findings.append({
            "severity": "critical",
            "category": "structure",
            "location": {"file": str(file_path)},
            "issue": "Missing 'elements' array",
            "fix": "Add 'elements' array",
        })
        return _build_result(file_path, findings)

    if not isinstance(data["elements"], list):
        findings.append({
            "severity": "critical",
            "category": "structure",
            "location": {"file": str(file_path)},
            "issue": "'elements' must be an array",
            "fix": "Change 'elements' to an array",
        })
        return _build_result(file_path, findings)

    # Validate elements
    seen_ids = set()
    element_ids = {e.get("id") for e in data["elements"] if e.get("id")}

    for i, elem in enumerate(data["elements"]):
        loc = {"file": str(file_path), "element_index": i, "element_id": elem.get("id")}

        # Required fields
        if "id" not in elem:
            findings.append({
                "severity": "critical",
                "category": "element",
                "location": loc,
                "issue": f"Element {i} missing 'id'",
                "fix": "Add unique 'id' to element",
            })
        elif elem["id"] in seen_ids:
            findings.append({
                "severity": "critical",
                "category": "element",
                "location": loc,
                "issue": f"Duplicate element ID: '{elem['id']}'",
                "fix": "Use unique IDs for all elements",
            })
        else:
            seen_ids.add(elem["id"])

        if "type" not in elem:
            findings.append({
                "severity": "critical",
                "category": "element",
                "location": loc,
                "issue": f"Element {i} missing 'type'",
                "fix": "Add valid element type",
            })
        elif elem["type"] not in VALID_ELEMENT_TYPES:
            findings.append({
                "severity": "high",
                "category": "element",
                "location": loc,
                "issue": f"Invalid element type: '{elem['type']}'",
                "fix": f"Use one of: {', '.join(sorted(VALID_ELEMENT_TYPES))}",
            })

        # Position and size
        for field in ("x", "y", "width", "height"):
            if field not in elem:
                findings.append({
                    "severity": "high",
                    "category": "element",
                    "location": loc,
                    "issue": f"Element missing '{field}'",
                    "fix": f"Add '{field}' (number)",
                })

        # Type-specific validation
        if elem.get("type") == "text":
            if "text" not in elem:
                findings.append({
                    "severity": "high",
                    "category": "text",
                    "location": loc,
                    "issue": "Text element missing 'text' field",
                    "fix": "Add 'text' field with content",
                })
            if elem.get("textAlign") and elem["textAlign"] not in VALID_TEXT_ALIGN:
                findings.append({
                    "severity": "medium",
                    "category": "text",
                    "location": loc,
                    "issue": f"Invalid textAlign: '{elem['textAlign']}'",
                    "fix": f"Use one of: {', '.join(VALID_TEXT_ALIGN)}",
                })

        if elem.get("type") in ("arrow", "line"):
            if "points" not in elem:
                findings.append({
                    "severity": "high",
                    "category": "linear",
                    "location": loc,
                    "issue": "Arrow/line missing 'points' array",
                    "fix": "Add 'points' array with at least 2 points",
                })
            elif len(elem.get("points", [])) < 2:
                findings.append({
                    "severity": "high",
                    "category": "linear",
                    "location": loc,
                    "issue": "Arrow/line needs at least 2 points",
                    "fix": "Add start and end points: [[0,0],[dx,dy]]",
                })

            # Validate bindings reference existing elements
            for binding_key in ("startBinding", "endBinding"):
                binding = elem.get(binding_key)
                if binding and isinstance(binding, dict):
                    ref_id = binding.get("elementId")
                    if ref_id and ref_id not in element_ids:
                        findings.append({
                            "severity": "medium",
                            "category": "binding",
                            "location": loc,
                            "issue": f"{binding_key} references non-existent element '{ref_id}'",
                            "fix": "Fix element ID reference or remove binding",
                        })

        # Validate style properties
        if elem.get("fillStyle") and elem["fillStyle"] not in VALID_FILL_STYLES:
            findings.append({
                "severity": "low",
                "category": "style",
                "location": loc,
                "issue": f"Non-standard fillStyle: '{elem['fillStyle']}'",
                "fix": f"Use one of: {', '.join(sorted(VALID_FILL_STYLES))}",
            })

        if elem.get("strokeStyle") and elem["strokeStyle"] not in VALID_STROKE_STYLES:
            findings.append({
                "severity": "low",
                "category": "style",
                "location": loc,
                "issue": f"Non-standard strokeStyle: '{elem['strokeStyle']}'",
                "fix": f"Use one of: {', '.join(sorted(VALID_STROKE_STYLES))}",
            })

    return _build_result(file_path, findings)


def _build_result(file_path, findings):
    """Build the structured validation result."""
    severity_counts = {"critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0}
    for f in findings:
        severity_counts[f["severity"]] = severity_counts.get(f["severity"], 0) + 1

    status = "pass"
    if severity_counts["critical"] > 0 or severity_counts["high"] > 0:
        status = "fail"
    elif severity_counts["medium"] > 0:
        status = "warning"

    return {
        "script": "validate-excalidraw",
        "version": "1.0.0",
        "skill_path": str(file_path),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": status,
        "findings": findings,
        "summary": {
            "total": len(findings),
            **severity_counts,
        },
    }


def main():
    parser = argparse.ArgumentParser(description="Validate .excalidraw files")
    parser.add_argument("file", help="Path to .excalidraw file")
    parser.add_argument("-o", "--output", help="Output report to file (JSON)")

    args = parser.parse_args()
    result = validate(args.file)

    output = json.dumps(result, indent=2)
    if args.output:
        Path(args.output).write_text(output)
        print(f"Report written to {args.output}", file=sys.stderr)
    else:
        print(output)

    if result["status"] == "fail":
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
