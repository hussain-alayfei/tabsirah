# 🎯 Quick Future Workflow (Simple!)

## For Daily Work (90% of the time)

```bash
# 1. Always work on develop
git checkout develop

# 2. Make changes (code, train models, etc.)
# ... do your work ...

# 3. Commit your changes
git add .
git commit -m "feat: what you did"

# 4. Keep working on develop!
```

**That's it!** Stay on `develop` for everything.

---

## To Deploy to Production (When Ready)

```bash
# 1. Switch to main
git checkout main

# 2. Merge your work from develop
git merge develop

# 3. Push to Render (auto-deploys)
git push origin main

# 4. Go back to develop
git checkout develop
```

---

## 🎯 Golden Rules

| Rule | Command |
|------|---------|
| **Train models?** | Stay on `develop` |
| **Add features?** | Stay on `develop` |
| **Test locally?** | Stay on `develop` |
| **Deploy to Render?** | Merge `develop` → `main`, push |

---

## ⚡ Super Quick Reference

```bash
# Check which branch you're on
git branch

# Switch to develop (for work)
git checkout develop

# Switch to main (to deploy only)
git checkout main

# See your scripts
ls src/
# develop: 6 files ✅
# main: 2 files (production)
```

**Default mode: Stay on `develop`!** 🚀

That's all you need to remember! 😊