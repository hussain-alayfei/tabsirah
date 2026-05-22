# Git Workflow — Tabsirah

A practical branching guide for this repo. Written for a **solo developer today**,
but structured so it scales cleanly when the team grows.

> **The one rule that matters most:** Render auto-deploys the **`main`** branch.
> Whatever is on `main` goes live. So **`main` must always be in a working,
> deployable state.** Never commit experiments directly to `main`.

---

## 1. The branch model (at a glance)

```
  feature/*  ──▶  dev  ──▶  main  ──▶  Render (production)
  (your work)   (testing)  (stable)    (auto-deploy)
```

| Branch | Purpose | Who/what watches it | Rule |
|--------|---------|---------------------|------|
| `main` | **Production.** Mirror of what's live on Render. | Render auto-deploy | Only ever receives **tested** code, via merge from `dev`. Never commit here directly. |
| `dev` | **Integration.** Where finished work lands and gets tested together. | You | Should *usually* run, but it's OK if it's briefly broken while integrating. |
| `feature/*` | **One task each.** Short-lived. | You | Branch from `dev`, merge back to `dev` when done, then delete. |

Two permanent branches (`main`, `dev`) + as many short-lived `feature/*` as you need.

---

## 2. Why this model (and not something heavier)

There are three common models. Here's why this one fits you:

| Model | What it is | Fit for you |
|-------|-----------|-------------|
| **GitHub Flow** | Just `main` + feature branches. Merge straight to `main`. | Simplest, but **no buffer** — a bad merge goes straight to Render. Risky when `main` = production. |
| **This (main + dev + features)** | A "staging" buffer between your work and production. | ✅ **Best fit.** You get a place to integrate and test before anything reaches Render. Minimal overhead. |
| **Full Git Flow** | `main` + `develop` + `release/*` + `hotfix/*` + `feature/*`. | Overkill for a solo dev / small team. Too much ceremony. |

As the team grows, you only need to *add* rules (branch protection, pull requests,
CI) — you don't have to change the structure.

---

## 3. Daily workflow (solo)

### Start a new piece of work
```bash
git checkout dev
git pull origin dev                 # get latest
git checkout -b feature/smooth-skeleton   # descriptive name
```

### While working — commit small and often
```bash
git add -A
git commit -m "feat: add EMA smoothing to hand skeleton"
```

### Finish the feature → merge into dev
```bash
git checkout dev
git merge feature/smooth-skeleton
git push origin dev
git branch -d feature/smooth-skeleton     # delete the finished branch
```

### Test on `dev`
Run the app locally, run the tests:
```bash
.\venv\Scripts\python.exe -m pytest tests/ -v
.\venv\Scripts\python.exe web_app\app.py
```
If anything is broken, fix it on `dev` (or a new `feature/*`) **before** the next step.

---

## 4. Releasing to production (this is the deploy step)

Only when `dev` is tested and you're confident:

```bash
git checkout main
git merge dev                       # bring tested work into main
git tag -a v2.1.0 -m "Smoothing + cleanup"   # optional but recommended
git push origin main --tags
```

Pushing to `main` → **Render auto-deploys.** That's the entire deploy process.
Watch the Render dashboard logs for a minute to confirm a green build.

> **Tip:** tag every production release (`v2.1.0`, `v2.2.0`, …). If a deploy goes
> wrong, you can instantly redeploy the last good tag from the Render dashboard.

---

## 5. Hotfixes (urgent production bug)

If production is broken and you need to fix it *now* without shipping whatever
half-done work is sitting on `dev`:

```bash
git checkout main
git checkout -b hotfix/login-crash
# ... fix it ...
git commit -am "fix: handle null landmarks in classify_landmarks"
git checkout main
git merge hotfix/login-crash
git push origin main                # Render redeploys with just the fix
# then bring the fix back into dev so it isn't lost:
git checkout dev
git merge main
```

---

## 6. Commit message convention (Conventional Commits)

Use a short prefix so history is scannable and changelogs can be auto-generated:

| Prefix | Use for |
|--------|---------|
| `feat:` | a new feature |
| `fix:` | a bug fix |
| `docs:` | documentation only |
| `refactor:` | code change that isn't a feature or fix |
| `test:` | adding or fixing tests |
| `chore:` | tooling, deps, config, cleanup |

Examples:
```
feat: add seed-ensemble averaging to classifier
fix: load list-of-models pickle without crashing
chore: convert UTF-16 scripts to UTF-8
docs: rewrite architecture doc for LightGBM
```

---

## 7. Never commit these

| Don't commit | Why | Where it should live |
|--------------|-----|----------------------|
| **Secrets / tokens / `.env`** | Security incident if leaked | Environment variables (Render dashboard) |
| **`venv/`** | Huge, machine-specific | Recreate from `requirements.txt` |
| **`__pycache__/`, `*.pyc`, `.pytest_cache/`** | Generated | n/a |
| **`debug-*.log`, agent logs** | Noise | Local only |
| **`models/lightgbm_improved.p` (104 MB)** | **GitHub rejects files > 100 MB** — the push will fail | Keep local, or cloud storage (see §8) |
| **Raw dataset images** | Too large, regenerable | Kaggle / external storage |

All of these belong in `.gitignore`. The production model
`models/model_lightgbm.p` (~63 MB) *is* committed because Render needs it —
but see §8 for the better long-term option.

---

## 8. Large model files

GitHub warns above 50 MB and **hard-rejects above 100 MB**. Your production
model (~63 MB) works but triggers warnings; the 104 MB `lightgbm_improved.p`
**cannot be pushed at all.**

Two clean options:

1. **Now (simple):** keep only `model_lightgbm.p` in the repo, gitignore
   `lightgbm_improved.p`. Regenerate it from the Kaggle notebook when needed.
2. **Better (when ready):** use **Git LFS** for `models/*.p`:
   ```bash
   git lfs install
   git lfs track "models/*.p"
   git add .gitattributes
   ```
   LFS stores big files outside normal git history, so clones stay fast and
   GitHub's size limit no longer applies.

---

## 9. When the team grows (turn these on)

You don't need these solo, but flip them on the day a second developer joins:

- **Protect `main`** on GitHub: require pull requests, block direct pushes.
- **Pull Requests** instead of direct merges — even a 30-second self-review
  catches mistakes.
- **CI on every PR**: run `pytest` automatically (GitHub Actions). Block merge
  if tests fail.
- **CODEOWNERS / review required** once there are 3+ people.

---

## 10. Command cheat-sheet

```bash
# see where you are
git status
git branch                          # list local branches (* = current)

# start work
git checkout dev && git pull
git checkout -b feature/<name>

# save work
git add -A && git commit -m "feat: ..."

# finish feature
git checkout dev && git merge feature/<name> && git push origin dev
git branch -d feature/<name>

# deploy to production (Render auto-deploys main)
git checkout main && git merge dev && git push origin main --tags

# undo last commit but keep changes
git reset --soft HEAD~1

# discard ALL local changes (careful)
git checkout -- .
```
