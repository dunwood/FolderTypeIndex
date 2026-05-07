# User Guide

## Installation

### Prerequisites

- Windows 10/11 or compatible OS
- Python 3.8+ (for v4 source)
- Git (for cloning the repository)

### Setup

```bash
# Clone the repository
git clone https://github.com/dunwood/FolderTypeIndex.git
cd FolderTypeIndex

# Navigate to v4 source
# Note: The main application code is in:
cd folder_type_index_v4_codex_import

# Follow v4-specific setup instructions there
```

## Configuration

### Creating Your First Index

1. Copy the example file:
```bash
cp examples/index_data.example.json index_data.json
```

2. Edit `index_data.json` with your actual paths:
```json
{
  "folders": [
    {
      "path": "D:/Your/Actual/Path",
      "type": "documents",
      "rules": {"extensions": [".pdf", ".docx"]}
    }
  ]
}
```

> ⚠️ **Important**: `index_data.json` contains your personal file paths and should NEVER be committed to version control.

### Import Format

For bulk imports, use `folder_type_index_import.json`:

```json
{
  "import_version": "1.0",
  "entries": [
    {
      "source_path": "C:/Example/Docs",
      "target_type": "reference",
      "metadata": {"category": "research"}
    }
  ]
}
```

See [IMPORT_FORMAT.md](IMPORT_FORMAT.md) for full specification.

## Basic Operations

### Indexing Files

```bash
# Run the indexer (from v4 source directory)
python main.py --index
```

### Searching

```bash
# Search by folder type
python main.py --search --type documents

# Search by keyword
python main.py --search --query "project report"
```

### Exporting Results

```bash
# Export index to JSON
python main.py --export --output my_index.json
```

## Examples

Browse the `examples/` directory for:
- `index_data.example.json` - Sample index structure
- `folder_type_index_import.example.json` - Sample import format

> All example paths are fictional and for demonstration only.

## Troubleshooting

### Common Issues

**Index not updating**:
- Check file permissions
- Ensure paths in config are accessible
- Verify `index_data.json` syntax

**GUI not launching**:
- Check Python dependencies
- Run from command line to see error output
- Verify display environment

### Getting Help

1. Check [DEV_NOTES.md](DEV_NOTES.md) for technical details
2. Review [SAFETY_RULES.md](SAFETY_RULES.md) for data handling guidelines
3. Open an issue on GitHub with:
   - Error messages
   - Steps to reproduce
   - Your OS and Python version

## Next Steps

- Explore advanced folder type rules
- Customize the GUI theme
- Contribute to the project (see CONTRIBUTING.md)
