#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = ["pyyaml"]
# ///
"""Merge module configuration into shared _bmad/config.yaml.

Reads a module.yaml definition and a JSON answers file, then writes or updates
the shared config.yaml. Uses an anti-zombie pattern: if the module code already
exists in config, that entire section is removed before writing fresh values.

Exit codes: 0=success, 1=validation error, 2=runtime error
"""

import argparse
import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("Error: pyyaml is required (PEP 723 dependency)", file=sys.stderr)
    sys.exit(2)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Merge module config into shared _bmad/config.yaml with anti-zombie pattern."
    )
    parser.add_argument(
        "--config-path",
        required=True,
        help="Path to the target _bmad/config.yaml file",
    )
    parser.add_argument(
        "--module-yaml",
        required=True,
        help="Path to the module.yaml definition file",
    )
    parser.add_argument(
        "--answers",
        required=True,
        help="Path to JSON file with collected answers",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print detailed progress to stderr",
    )
    return parser.parse_args()


def load_yaml_file(path: str) -> dict:
    """Load a YAML file, returning empty dict if file doesn't exist."""
    file_path = Path(path)
    if not file_path.exists():
        return {}
    with open(file_path, "r", encoding="utf-8") as f:
        content = yaml.safe_load(f)
    return content if content else {}


def load_json_file(path: str) -> dict:
    """Load a JSON file."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def extract_module_metadata(module_yaml: dict) -> dict:
    """Extract non-variable metadata fields from module.yaml."""
    metadata_keys = ["name", "description", "default_selected"]
    return {k: module_yaml[k] for k in metadata_keys if k in module_yaml}


def merge_config(
    existing_config: dict,
    module_yaml: dict,
    answers: dict,
    verbose: bool = False,
) -> dict:
    """Merge answers into config, applying anti-zombie pattern.

    Args:
        existing_config: Current config.yaml contents (may be empty)
        module_yaml: The module definition
        answers: JSON with 'core' and/or 'module' keys
        verbose: Print progress to stderr

    Returns:
        Updated config dict ready to write
    """
    config = dict(existing_config)
    module_code = module_yaml.get("code")

    if not module_code:
        print("Error: module.yaml must have a 'code' field", file=sys.stderr)
        sys.exit(1)

    # Write core section if provided
    core_answers = answers.get("core")
    if core_answers:
        if verbose:
            print(f"Writing core config: {list(core_answers.keys())}", file=sys.stderr)
        config["core"] = core_answers

    # Anti-zombie: remove existing module section
    if module_code in config:
        if verbose:
            print(
                f"Removing existing '{module_code}' section (anti-zombie)",
                file=sys.stderr,
            )
        del config[module_code]

    # Build module section: metadata + variable values
    module_section = extract_module_metadata(module_yaml)
    module_answers = answers.get("module", {})
    module_section.update(module_answers)

    if verbose:
        print(
            f"Writing '{module_code}' section with keys: {list(module_section.keys())}",
            file=sys.stderr,
        )

    config[module_code] = module_section

    return config


def write_config(config: dict, config_path: str, verbose: bool = False) -> None:
    """Write config dict to YAML file, creating parent dirs as needed."""
    path = Path(config_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    if verbose:
        print(f"Writing config to {path}", file=sys.stderr)

    with open(path, "w", encoding="utf-8") as f:
        yaml.dump(
            config,
            f,
            default_flow_style=False,
            allow_unicode=True,
            sort_keys=False,
        )


def main():
    args = parse_args()

    # Load inputs
    module_yaml = load_yaml_file(args.module_yaml)
    if not module_yaml:
        print(f"Error: Could not load module.yaml from {args.module_yaml}", file=sys.stderr)
        sys.exit(1)

    answers = load_json_file(args.answers)
    existing_config = load_yaml_file(args.config_path)

    if args.verbose:
        exists = Path(args.config_path).exists()
        print(f"Config file exists: {exists}", file=sys.stderr)
        if exists:
            print(f"Existing sections: {list(existing_config.keys())}", file=sys.stderr)

    # Merge and write
    updated_config = merge_config(existing_config, module_yaml, answers, args.verbose)
    write_config(updated_config, args.config_path, args.verbose)

    # Output result summary as JSON
    module_code = module_yaml["code"]
    result = {
        "status": "success",
        "config_path": str(Path(args.config_path).resolve()),
        "module_code": module_code,
        "core_updated": "core" in answers and bool(answers["core"]),
        "module_keys": list(updated_config.get(module_code, {}).keys()),
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
