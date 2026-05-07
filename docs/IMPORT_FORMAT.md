# Import Format Specification

## Overview

This document describes the JSON format for `folder_type_index_import.json`, used for bulk importing folder type configurations.

## Schema

```json
{
  "import_version": "1.0",
  "created_at": "2026-05-08T00:00:00Z",
  "author": "optional-author-name",
  "entries": [
    {
      "source_path": "string (required)",
      "target_type": "string (required)",
      "rules": {
        "extensions": [".pdf", ".docx"],
        "patterns": ["*.report.*"],
        "exclude": ["temp/", "*.tmp"]
      },
      "metadata": {
        "category": "string",
        "tags": ["tag1", "tag2"],
        "priority": "high|medium|low"
      }
    }
  ]
}
```

## Field Descriptions

### Root Level

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `import_version` | string | Yes | Format version, currently "1.0" |
| `created_at` | string | No | ISO 8601 timestamp |
| `author` | string | No | Creator identifier |
| `entries` | array | Yes | List of import entries |

### Entry Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `source_path` | string | Yes | Source directory path (use forward slashes) |
| `target_type` | string | Yes | Folder type identifier |
| `rules` | object | No | Matching rules for files |
| `metadata` | object | No | Additional metadata |

### Rules Object

| Field | Type | Description |
|-------|------|-------------|
| `extensions` | array | File extensions to include (e.g., [".pdf"]) |
| `patterns` | array | Glob patterns for matching (e.g., ["*.report.*"]) |
| `exclude` | array | Paths/patterns to exclude from indexing |

### Metadata Object

| Field | Type | Description |
|-------|------|-------------|
| `category` | string | High-level category label |
| `tags` | array | Searchable tags |
| `priority` | string | Processing priority: high/medium/low |

## Example (Fictional Paths)

```json
{
  "import_version": "1.0",
  "entries": [
    {
      "source_path": "C:/Users/Example/Documents/Research",
      "target_type": "academic_papers",
      "rules": {
        "extensions": [".pdf", ".bib"],
        "exclude": ["drafts/", "*.tmp"]
      },
      "metadata": {
        "category": "research",
        "tags": ["papers", "citations"],
        "priority": "high"
      }
    },
    {
      "source_path": "D:/Example/Projects/Code",
      "target_type": "source_code",
      "rules": {
        "extensions": [".py", ".js", ".ts"],
        "patterns": ["src/**/*"]
      },
      "metadata": {
        "category": "development",
        "tags": ["code", "projects"]
      }
    }
  ]
}
```

> ⚠️ **Note**: All paths in this example are fictional. Replace with your actual paths when using.

## Validation

Before importing:

1. Verify all `source_path` values exist and are accessible
2. Ensure `target_type` values match your defined folder types
3. Test rules with a small subset first
4. Use `--dry-run` flag to preview changes:
   ```bash
   python main.py --import config.json --dry-run
   ```

## Migration Notes

### From v3 to v4

- `folder_type` field renamed to `target_type`
- `file_patterns` split into `extensions` and `patterns`
- `metadata` object now supports nested structures

## Troubleshooting

### Import Fails

1. Check JSON syntax: `python -m json.tool config.json`
2. Verify paths use forward slashes or escaped backslashes
3. Ensure no trailing commas in JSON arrays/objects
4. Check file permissions for source paths

### Unexpected Results

1. Review `rules.exclude` for over-filtering
2. Check `patterns` syntax (uses glob, not regex)
3. Verify `target_type` spelling matches your type definitions

## See Also

- [USER_GUIDE.md](USER_GUIDE.md) - Usage instructions
- [SAFETY_RULES.md](SAFETY_RULES.md) - Data handling policies
- [examples/folder_type_index_import.example.json](../examples/folder_type_index_import.example.json) - Working example
