# Git Workflow Guide for Tabsirah

This document explains the branching strategy and git workflow for the Tabsirah project.

## 📊 Branching Strategy

```
main (production)
  ↓
develop (integration)
  ├── feature/add-new-surah
  ├── feature/user-authentication
  ├── bugfix/camera-initialization
  ├── bugfix/arabic-normalization
  └── hotfix/critical-security-fix
```

### Branch Types

| Branch Type | Naming | Purpose | Base Branch | Merge To |
|------------|---------|---------|-------------|----------|
| **main** | `main` | Production-ready code (Deployment) | - | - |
| **master** | `master` | Legacy/Active Production (Recent Fixes) | - | `main`, `develop` |
| **develop** | `develop` | Integration branch | `main`, `master` | `main` |
| **feature** | `feature/description` | New features | `develop` | `develop` |
| **bugfix** | `bugfix/description` | Bug fixes | `develop` | `develop` |
| **hotfix** | `hotfix/description` | Critical production fixes | `main` | `main` + `develop` |
| **release** | `release/v1.2.3` | Release preparation | `develop` | `main` + `develop` |

---

## 🔄 Workflow

### 1. Feature Development

```bash
# Start from develop
git checkout develop
git pull origin develop

# Create feature branch
git checkout -b feature/add-surah-al-baqarah

# Make changes
# ... edit files ...

# Commit with good message
git add .
git commit -m "feat: Add Surah Al-Baqarah to practice mode

- Add Arabic text and metadata
- Create sign image mappings
- Update surah list in UI
- Add tests for new surah"

# Push to remote
git push origin feature/add-surah-al-baqarah

# Create Pull Request on GitHub: feature/add-surah-al-baqarah → develop
```

### 2. Bug Fixes

```bash
# Start from develop
git checkout develop
git pull origin develop

# Create bugfix branch
git checkout -b bugfix/fix-camera-initialization

# Make changes
git add .
git commit -m "fix: Resolve camera initialization on Safari

- Add fallback for getUserMedia API
- Handle permission denial gracefully
- Add browser compatibility check

Fixes #42"

# Push and create PR
git push origin bugfix/fix-camera-initialization
```

### 3. Hotfix (Critical Production Bug)

```bash
# Start from main (production)
git checkout main
git pull origin main

# Create hotfix branch
git checkout -b hotfix/security-patch

# Make changes
git add .
git commit -m "hotfix: Fix XSS vulnerability in prediction endpoint

- Sanitize user input
- Add content security policy
- Update dependencies

SECURITY: CVE-2026-XXXX"

# Merge to main
git checkout main
git merge hotfix/security-patch
git tag -a v2.0.1 -m "Security patch"
git push origin main --tags

# Also merge to develop
git checkout develop
git merge hotfix/security-patch
git push origin develop
```

### 4. Release Process

```bash
# Create release branch from develop
git checkout develop
git pull origin develop
git checkout -b release/v2.1.0

# Update version numbers
# ... edit CHANGELOG.md ...
# ... edit package version ...

git commit -m "chore: Prepare release v2.1.0"

# Merge to main
git checkout main
git merge release/v2.1.0
git tag -a v2.1.0 -m "Release version 2.1.0"
git push origin main --tags

# Merge back to develop
git checkout develop
git merge release/v2.1.0
git push origin develop

# Delete release branch
git branch -d release/v2.1.0
```

---

## 📝 Commit Message Guidelines

### Format
```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types
- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Code formatting (no code change)
- **refactor**: Code refactoring
- **test**: Adding tests
- **chore**: Maintenance tasks
- **perf**: Performance improvement
- **ci**: CI/CD changes

### Examples

#### Good Commits
```bash
# Feature
git commit -m "feat(ui): Add hand skeleton visualization

- Implement real-time green overlay
- Show 21 landmark points
- Add toggle in settings

Closes #23"

# Bug Fix
git commit -m "fix(prediction): Normalize Arabic character variants

- Map أ, إ, آ to ا
- Map ى to ي
- Map ة to ه

Fixes #45"

# Documentation
git commit -m "docs: Update installation guide for Windows users

- Add PowerShell commands
- Include firewall configuration
- Add troubleshooting section"
```

#### Bad Commits
```bash
# Too vague
git commit -m "fix bug"

# Not descriptive
git commit -m "update"

# Multiple unrelated changes
git commit -m "add feature, fix bug, update docs"
```

---

## 🏷️ Tagging Releases

### Semantic Versioning
```
v[MAJOR].[MINOR].[PATCH]

Example: v2.1.3
- MAJOR: Breaking changes (v2.0.0 → v3.0.0)
- MINOR: New features (v2.0.0 → v2.1.0)
- PATCH: Bug fixes (v2.0.0 → v2.0.1)
```

### Create Tag
```bash
# Annotated tag (recommended)
git tag -a v2.1.0 -m "Release version 2.1.0 - User authentication"

# Push tags
git push origin v2.1.0

# Or push all tags
git push origin --tags

# List tags
git tag -l
```

---

## 🔍 Useful Commands

### Check Status
```bash
git status              # See changes
git diff                # See unstaged changes
git diff --staged       # See staged changes
git log --oneline -10   # See recent commits
```

### Undo Changes
```bash
# Undo unstaged changes
git checkout -- <file>

# Unstage file
git restore --staged <file>

# Amend last commit
git commit --amend

# Reset to previous commit (dangerous!)
git reset --hard HEAD~1
```

### Branch Management
```bash
# List branches
git branch -a

# Switch branch
git checkout develop

# Create and switch
git checkout -b feature/new-feature

# Delete local branch
git branch -d feature/old-feature

# Delete remote branch
git push origin --delete feature/old-feature
```

### Sync with Remote
```bash
# Fetch changes
git fetch origin

# Pull changes
git pull origin main

# Push changes
git push origin main

# Force push (be careful!)
git push origin main --force
```

---

## 🚨 Best Practices

### DO ✅
- Write clear, descriptive commit messages
- Commit frequently with logical changes
- Pull before pushing
- Review your changes before committing
- Use branches for all changes
- Keep commits focused (one feature/fix per commit)
- Tag releases

### DON'T ❌
- Commit directly to `main`
- Use `--force` push on shared branches
- Commit large binary files
- Mix unrelated changes in one commit
- Ignore merge conflicts
- Push sensitive data (API keys, passwords)

---

## 📞 Help

### Common Issues

**Q: I committed to main by mistake!**
```bash
# Move commit to new branch
git branch feature/my-feature
git reset --hard HEAD~1
git checkout feature/my-feature
```

**Q: I need to undo my last commit**
```bash
# Keep changes, undo commit
git reset --soft HEAD~1

# Discard everything
git reset --hard HEAD~1
```

**Q: I have merge conflicts**
```bash
# See conflicted files
git status

# Edit files, remove conflict markers (<<<<, ====, >>>>)
# Then:
git add <resolved-files>
git commit
```

---

## 🔗 Resources

- [Git Documentation](https://git-scm.com/doc)
- [Semantic Versioning](https://semver.org/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Git Flow](https://nvie.com/posts/a-successful-git-branching-model/)

---

**Current Repository Status:**
- ✅ Git initialized
- ✅ Main branch set up
- ✅ Develop branch created
- ✅ Clean commit history
- ✅ Ready for GitHub push
