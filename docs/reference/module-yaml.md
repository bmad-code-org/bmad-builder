---
title: "Module YAML Reference"
description: Configuration for BMad module.yaml files
---

Complete reference for `module.yaml` configuration files.

## Module File Location

The `module.yaml` file is located at:

```
your-module/src/module.yaml
```

## Basic Structure

```yaml
name: "Module Name"
code: "module-code"
version: "0.1.0"
description: "What this module does"
```

## Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Display name of the module |
| `code` | string | Unique module identifier (kebab-case) |
| `version` | string | Semantic version (e.g., `0.1.0`) |
| `description` | string | Short description of module purpose |

## Install Configuration

### Install Questions

Questions asked during module installation:

```yaml
install:
  - question: "What's your experience level?"
    config_key: "experience_level"
    options:
      - "beginner"
      - "intermediate"
      - "advanced"
```

| Field | Type | Description |
|-------|------|-------------|
| `question` | string | Question text |
| `config_key` | string | Config key to store answer |
| `options` | array | Available options (optional) |

### Configuration Values

Default configuration for the module:

```yaml
config:
  output_folder: "_module-output"
  enabled_features:
    - feature1
    - feature2
  user_name: "{user_name}"
```

## Complete Example

```yaml
name: "My Custom Module"
code: "my-custom-module"
version: "0.1.0"
description: "A module that does useful things"

# Install questions
install:
  - question: "What's your primary use case?"
    config_key: "use_case"
    options:
      - "development"
      - "documentation"
      - "testing"

  - question: "Enable advanced features?"
    config_key: "advanced_enabled"
    options:
      - "yes"
      - "no"

# Configuration
config:
  output_folder: "_my-module-output"
  max_iterations: 10
  default_language: "english"

# Optional: Module dependencies
requires:
  - "bmm"
```

## Validation Rules

When validating modules, Morgan checks:

- ✅ Required fields present
- ✅ `code` is valid kebab-case
- ✅ `version` follows semantic versioning
- ✅ `config_key` values are unique
- ✅ Options arrays are valid (if provided)

## See Also

- **[Builder Commands](docs/reference/builder-commands.md)** — Module commands
- **[Create Your First Module](docs/tutorials/create-your-first-module.md)** — Module creation tutorial
- **[What Are Modules](docs/explanation/what-are-modules.md)** — Module concepts
