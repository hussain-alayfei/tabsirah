# 🌳 Branch Strategy: Development vs Production

## Problem Solved ✅

You wanted **TWO versions** of your codebase:
1. **Production** - Clean, minimal, deployed code
2. **Development** - All scripts, tools, and experimental features

**Solution**: Use Git branches!

---

## 📊 Your Current Setup

### `main` Branch (Production - Clean!)
```
main branch
├── Core application (web_app/)
├── Training scripts (src/3_process_data.py, src/4_train_model.py)
├── Models (models/)
├── Documentation
└── Production configs (Procfile, requirements.txt)

❌ NO development helper scripts
❌ NO experimental code
✅ Only what's needed to run in production
```

**Use for**: Deployment to Render, sharing with users

### `develop` Branch (Development - Full Toolkit!)
```
develop branch
├── Everything from main branch
├── PLUS: src/1_download_data.py
├── PLUS: src/2_verify_mapping.py
├── PLUS: src/5_update_app.py
├── PLUS: src/sync_images.py
├── PLUS: copy_signs.py
├── PLUS: verify_images.py
└── PLUS: Any experimental features

✅ ALL development scripts
✅ ALL tools and helpers
✅ Experimental code
```

**Use for**: Training models, adding features, testing

---

## 🔄 How to Switch Between Them

### Work on Development (Train Models, Add Features)
```bash
# Switch to develop branch
git checkout develop

# Now you have ALL scripts available!
ls src/
# Output: 1_download_data.py, 2_verify_mapping.py, 3_process_data.py, 
#         4_train_model.py, 5_update_app.py, sync_images.py

# Train your model
python src/3_process_data.py
python src/4_train_model.py

# Make changes, commit
git add .
git commit -m "feat: Improve model accuracy"
```

### Deploy to Production (Push to Render)
```bash
# Switch to main branch
git checkout main

# Merge stable features from develop
git merge develop

# Push to production
git push origin main
# (Render auto-deploys from main)
```

---

## 📋 Complete Workflow

### Scenario 1: Train a New Model

```bash
# 1. Switch to develop
git checkout develop

# 2. Download fresh data (if needed)
python src/1_download_data.py

# 3. Verify mappings
python src/2_verify_mapping.py

# 4. Process data
python src/3_process_data.py

# 5. Train model
python src/4_train_model.py

# 6. Test the new model locally
cd web_app
python app.py

# 7. If good, commit
git add models/model_arabic.p
git commit -m "feat: Retrained model with new data - 97% accuracy"

# 8. Merge to main for production
git checkout main
git merge develop
git push origin main
```

### Scenario 2: Add a New Feature

```bash
# 1. Start from develop
git checkout develop

# 2. Create feature branch
git checkout -b feature/add-user-auth

# 3. Make changes
# ... code ...

# 4. Commit
git commit -m "feat: Add user authentication"

# 5. Merge back to develop
git checkout develop
git merge feature/add-user-auth

# 6. Test thoroughly, then merge to main
git checkout main
git merge develop
git push origin main
```

### Scenario 3: Quick Production Hotfix

```bash
# 1. Start from main
git checkout main

# 2. Create hotfix branch
git checkout -b hotfix/fix-camera-bug

# 3. Fix the bug
# ... fix ...

# 4. Commit
git commit -m "hotfix: Fix camera initialization on Safari"

# 5. Merge to main (production)
git checkout main
git merge hotfix/fix-camera-bug
git push origin main

# 6. Also merge to develop (keep it updated)
git checkout develop
git merge hotfix/fix-camera-bug
```

---

## 🎯 Quick Reference

| Task | Branch | Command |
|------|--------|---------|
| Train model | `develop` | `git checkout develop` |
| Add feature | `develop` | `git checkout develop` |
| Test locally | `develop` | `git checkout develop` |
| Deploy to Render | `main` | `git checkout main; git push` |
| Hotfix production | `main` | `git checkout main` |
| Experiment | `develop` | `git checkout develop` |

---

## 📁 Files Comparison

### Files ONLY in `develop` (Not in `main`)
- ✅ `src/1_download_data.py` - Download dataset
- ✅ `src/2_verify_mapping.py` - Verify mappings
- ✅ `src/5_update_app.py` - Update helper
- ✅ `src/sync_images.py` - Sync images
- ✅ `copy_signs.py` - Copy signs
- ✅ `verify_images.py` - Verify images

### Files in BOTH branches
- ✅ `src/3_process_data.py` - Process data (needed for retraining)
- ✅ `src/4_train_model.py` - Train model (needed for retraining)
- ✅ All production code (web_app/, models/, etc.)

---

## 🚀 Current Status

```
main (production)
│
├── 07f6a69 - chore: Update .gitignore for production
├── 26a47cd - docs: Add production readiness summary
├── da758b6 - docs: Add Git workflow guide
└── 01299ba - chore: Clean up codebase for production

develop (development)
│
└── 43f2e7e - feat(dev): Restore development scripts ✨ NEW
    │
    └── (includes all commits from main)
```

**You are currently on**: `develop` ✅  
**Ready to**: Train models, develop features, experiment!

---

## 💡 Key Benefits

### Clean Production ✅
- Main branch has ONLY production code
- Smaller repo size for deployment
- Faster deployment times
- Professional structure

### Full Development Toolkit ✅
- Develop branch has ALL tools
- Easy to train and experiment
- All helper scripts available
- No restrictions

### Best of Both Worlds ✅
- Production is clean and fast
- Development has everything you need
- Easy to switch with `git checkout`
- Organized and professional

---

## 🔍 Check Which Branch You're On

```bash
# See current branch
git branch

# Output:
#   main
# * develop  ← You're here (asterisk shows current branch)

# See all branches
git branch -a

# See file differences between branches
git diff main develop
```

---

## ⚠️ Important Notes

1. **Never commit directly to `main`**
   - Always work in `develop` or feature branches
   - Only merge to `main` when ready to deploy

2. **Keep `develop` up to date**
   - Regularly merge `main` into `develop` to stay in sync
   - `git checkout develop; git merge main`

3. **Production deploys from `main`**
   - Render auto-deploys when you push to `main`
   - Test everything in `develop` first!

4. **Development scripts stay in `develop`**
   - Don't merge dev scripts to `main`
   - Keep production clean

---

## 🎉 Summary

You now have:
- **`main`** - Clean production code (deployed to Render)
- **`develop`** - Full development toolkit (all scripts available)

**To train models**: `git checkout develop; python src/4_train_model.py`  
**To deploy**: `git checkout main; git push origin main`

**Perfect separation of concerns!** 🚀
