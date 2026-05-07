# Safety Rules

## Critical: Data Protection Guidelines

FolderTypeIndex operates on your personal files. Follow these rules to protect your data and privacy.

## 🚫 Never Commit These Files

The following files contain your personal data and must NEVER be added to version control:

```
index_data.json                    # Your actual file index
folder_type_index_import.json      # Your import configurations
.env, *.env                        # Environment variables/credentials
*.log                              # Application logs (may contain paths)
```

These are already listed in `.gitignore`. Verify before committing:

```bash
git status --short
# Review output - reject any of the above files
```

## 🔐 Path Handling Rules

### In Code
- Use `pathlib.Path` for cross-platform path handling
- Never hardcode absolute paths in source code
- Sanitize user input before path operations
- Log relative paths, not full absolute paths

### In Examples/Documentation
- Always use fictional paths:
  ```json
  // ✅ Good
  "path": "C:/Users/Example/Documents"
  
  // ❌ Bad
  "path": "D:/AI Project/MyRealData"
  ```

### In Configuration Files
- Users should edit `index_data.json` locally only
- Never share your config files with real paths publicly
- Use environment variables for sensitive path prefixes

## 🛡️ File Operation Safety

### Read Operations
- Always check file/directory existence before access
- Handle permission errors gracefully
- Never follow symlinks outside designated roots

### Write Operations
- Create backups before modifying user data files
- Use atomic writes (write to temp, then rename)
- Never overwrite files without explicit user confirmation

### Delete Operations
- ⚠️ FolderTypeIndex should NEVER delete user files
- Only remove entries from the index, not the actual files
- If cleanup is needed, require explicit user confirmation with full path display

## 🌐 Privacy Principles

1. **Local Only**: No network calls for indexing operations
2. **No Telemetry**: Do not collect usage statistics without opt-in
3. **No Cloud Sync**: User data stays on their machine
4. **Transparent**: Log what operations are performed
5. **Reversible**: All index changes can be undone

## 🔍 Before Pushing to GitHub

Run this checklist:

```bash
# 1. Check for sensitive files
git status --short | grep -E "(index_data|import.json|.env)"
# Should return nothing

# 2. Verify .gitignore is working
git check-ignore -v index_data.json
# Should show it is ignored

# 3. Review staged changes
git diff --cached --name-only
# Confirm no user data files are included

# 4. Scan for hardcoded paths
grep -r "D:/AI Project" --include="*.md" --include="*.json" examples/
# Should only find fictional example paths
```

## 🧪 Testing Guidelines

### Test Data
- Create test directories in isolated locations (e.g., `C:/tmp/test_fti/`)
- Use clearly fake file names: `test_doc_001.pdf`, not `tax_return_2025.pdf`
- Clean up test data after tests complete

### Example Files
- All files in `examples/` must use fictional paths
- Add a comment header to example JSON files:
  ```json
  // ⚠️ This is an example. Replace paths with your actual directories.
  // Do not commit your real paths to version control.
  ```

## 🚨 Incident Response

### If You Accidentally Commit Sensitive Data

1. **Do not push** - stop immediately
2. Remove the file from staging: `git reset HEAD filename`
3. Verify it is in `.gitignore`
4. If already pushed:
   - Use `git filter-branch` or BFG to remove from history
   - Rotate any exposed credentials
   - Consider the repository compromised if secrets were exposed

### If User Reports Data Exposure

1. Acknowledge and investigate immediately
2. Review `.gitignore` and documentation for gaps
3. Update safety rules if needed
4. Notify affected users if their data was exposed

## 📋 Quick Reference

| Do | Don'\''t |
|----|----------|
| Use fictional paths in examples | Hardcode your real paths in code |
| Test in isolated directories | Test on production data |
| Log relative paths | Log full absolute paths |
| Require confirmation for destructive ops | Auto-delete user files |
| Document safety rules | Assume users know the risks |

## Questions?

- Review [CONTRIBUTING.md](../CONTRIBUTING.md) for contribution guidelines
- Check [DEV_NOTES.md](DEV_NOTES.md) for technical implementation notes
- Open an issue to report safety concerns or suggest improvements
