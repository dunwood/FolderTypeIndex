# Developer Notes

## Project Structure

```
D:\AI Project\FolderTypeIndex/
├── .gitignore              # Git ignore rules (protects user data)
├── LICENSE                 # MIT License
├── README.md               # Project overview
├── CHANGELOG.md            # Version history
├── CONTRIBUTING.md         # Contribution guidelines
├── docs/                   # Documentation
│   ├── PROJECT_OVERVIEW.md
│   ├── USER_GUIDE.md
│   ├── DEV_NOTES.md        # This file
│   ├── IMPORT_FORMAT.md
│   └── SAFETY_RULES.md
├── examples/               # Example configurations (fictional paths only)
│   ├── index_data.example.json
│   └── folder_type_index_import.example.json
├── tasks/                  # Development task definitions
│   └── task01.md
└── folder_type_index_v4_codex_import/  # Main v4 application source
    ├── (v4 source files - do not modify structure)
    └── (GUI implementation)
```

## Development Workflow

### Branch Strategy

- `main`: Stable releases
- `develop`: Integration branch for features
- `feature/*`: Individual feature branches

### Commit Guidelines

Follow conventional commits:
```bash
# Feature
git commit -m "feat: add folder type validation"

# Bug fix
git commit -m "fix: handle missing index file gracefully"

# Documentation
git commit -m "docs: update import format examples"
```

### Testing

```bash
# Run v4 tests (from source directory)
cd folder_type_index_v4_codex_import
python -m pytest tests/ -v

# Lint code
python -m flake8 .
```

## Data Handling

### Files to NEVER Commit

```gitignore
# User data (contains personal file paths)
index_data.json
folder_type_index_import.json

# Environment/credentials
.env
*.env
credentials.json

# Build artifacts
dist/
build/
*.pyc
__pycache__/
```

### Example Files

All files in `examples/` must use fictional paths:
```json
{
  "path": "C:/Users/Example/Documents",
  "type": "fictional"
}
```

## v4 Source Directory

The `folder_type_index_v4_codex_import/` directory contains the runnable v4 application.

**Do not**:
- Rename this directory
- Move files out of it
- Change its internal structure without careful consideration

**Do**:
- Add new features following existing patterns
- Update documentation when adding functionality
- Test changes in isolated environments first

## Building

```bash
# Navigate to v4 source
cd folder_type_index_v4_codex_import

# Install dependencies (if requirements.txt exists)
pip install -r requirements.txt

# Build (if build script exists)
python build.py
```

## Debugging

### Enable Debug Logging

```python
# In your code
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Common Debug Commands

```bash
# Run with verbose output
python main.py --verbose

# Check index integrity
python main.py --check-index

# Dry-run import
python main.py --import config.json --dry-run
```

## Performance Considerations

- Indexing large directories: Use incremental scanning
- Memory usage: Stream large files instead of loading entirely
- GUI responsiveness: Offload heavy operations to background threads

## Security Notes

1. Never log full file paths in production
2. Sanitize user input for path operations
3. Validate JSON configurations before processing
4. Use absolute paths internally to avoid confusion

## Questions?

- Check existing issues on GitHub
- Review SAFETY_RULES.md for data handling policies
- Open a new issue for feature requests or bugs
