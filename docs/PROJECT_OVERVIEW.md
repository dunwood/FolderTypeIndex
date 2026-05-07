# Project Overview

## What is FolderTypeIndex?

FolderTypeIndex is a local file organization and indexing tool designed for personal knowledge management. It helps you categorize and track files based on custom folder type rules, all while keeping your data private on your local machine.

## Core Philosophy

- **Privacy First**: No cloud sync, no telemetry, your data stays yours
- **Local Only**: Operates entirely on your local filesystem
- **Flexible**: Define your own folder types and classification rules
- **Lightweight**: Fast indexing without heavy dependencies

## Architecture

```
FolderTypeIndex/
├── folder_type_index_v4_codex_import/  # Main v4 source code
├── docs/                                # Documentation
├── examples/                            # Sample configurations
├── tasks/                               # Development tasks
├── README.md
├── LICENSE
├── CHANGELOG.md
└── CONTRIBUTING.md
```

## Key Components

### Indexing Engine
- Scans local directories based on user-defined rules
- Builds a JSON-based index for fast lookups
- Supports custom folder type definitions

### Data Storage
- `index_data.json`: Main index file (user data, NOT committed)
- `folder_type_index_import.json`: Import configuration (user data, NOT committed)

### GUI (v4)
- Built with modern UI framework
- Visual folder type management
- Import/export utilities

## Use Cases

1. **Personal Knowledge Base**: Organize research papers, notes, and references
2. **Project Management**: Track files across multiple projects
3. **Media Libraries**: Categorize photos, videos, and documents
4. **Code Repositories**: Index source files by type and purpose

## Getting Started

See [USER_GUIDE.md](USER_GUIDE.md) for installation and usage instructions.
