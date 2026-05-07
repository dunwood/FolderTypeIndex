# Contributing to FolderTypeIndex

Thank you for your interest in contributing to FolderTypeIndex! This document provides guidelines for contributing to the project.

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for all contributors.

## How to Contribute

### Reporting Issues

1. Check existing issues to avoid duplicates
2. Use the issue template if available
3. Include:
   - Clear description of the issue
   - Steps to reproduce (if applicable)
   - Expected vs actual behavior
   - Environment details (OS, Python version, etc.)

### Submitting Pull Requests

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Make your changes
4. Test thoroughly
5. Commit with clear messages: `git commit -m "feat: add your feature"`
6. Push to your fork and open a PR

### Commit Message Format

We follow conventional commits:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Formatting, no code changes
- `refactor:` Code refactoring
- `test:` Adding tests
- `chore:` Maintenance tasks

## Development Setup

```bash
# Clone your fork
git clone https://github.com/your-username/FolderTypeIndex.git
cd FolderTypeIndex

# The v4 source code is in:
# folder_type_index_v4_codex_import/
```

## Important Safety Rules

⚠️ **When contributing, please remember**:

1. Never commit user data files (`index_data.json`, `folder_type_index_import.json`)
2. Never commit `.env` files or credentials
3. Use fictional paths in examples and tests
4. Respect user privacy - the tool operates on local files only
5. Test changes in isolated directories first

## Questions?

Open an issue or contact the maintainer at the GitHub repository.
