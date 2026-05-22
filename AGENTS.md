# Agent Guide — Tabsirah (تبصرة)

**Read this first** before changing code, deploying, or debugging production.

**Last updated:** 2026-05-22  
**Production URL:** https://tabsirah.onrender.com  
**GitHub:** https://github.com/hussain-alayfei/tabsirah

---

## Quick facts

| Item | Value |
|------|--------|
| **Stack** | Flask + Gunicorn, MediaPipe (browser + optional server), **LightGBM** classifier |
| **Production model** | `models/model_lightgbm.p` (3-model LightGBM ensemble, 62 features) |
| **Python (Render)** | 3.11 (native runtime) |
| **Python (local `.python-version`)** | 3.11.10 preferred |
| **Deploy platform** | Render (Free tier) |
| **Production branch** | `main` → auto-deploy ON |

---

## Git repository status

### Remotes

```
origin  https://github.com/hussain-alayfei/tabsirah.git
```

### Branches

| Branch | Purpose | Notes |
|--------|---------|--------|
| `main` | **Production** | Deployed to Render; default branch |
| `develop` | Integration | Feature merges target |
| `master` | Legacy | Exists on remote; use `main` for new work |

### Recent production-related commits (newest first)

```
add6ac6  fix: classify from browser landmarks when server MediaPipe unavailable
d65206e  fix: use CPU delegate and Mesa libs for Render headless
ef5082e  fix: add lightgbm to requirements for Render deployment
09bd196  chore: update model to lightgbm
```

### Workflow rules for agents

1. **Do not commit** unless the user explicitly asks.
2. **Never commit** API keys, `.env`, or `~/.cursor/mcp.json`.
3. Production fixes → branch from `main` or commit directly to `main` only if user requests deploy.
4. Feature work → `develop` → PR → `main` (see [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md)).
5. After pushing to `main`, Render auto-deploys (if enabled).

---

## Architecture (prediction pipeline)

```
Browser                          Server (Flask)
────────                         ──────────────
Webcam
  → MediaPipe WASM (hand landmarks)  ← always runs in browser (green skeleton)
  → JPEG frame + 21 landmarks      → POST /predict
                                     → LightGBM classify_landmarks()  ← REQUIRED on Render
                                     → (optional) server MediaPipe on image
```

**Critical:** On Render (headless Linux), server MediaPipe often fails with `libGLESv2.so.2`. The app **must** still load LightGBM and classify using **client-sent landmarks**. Do not require server HandLandmarker for production.

Expected startup log on Render:

```
HandLandmarker unavailable (client-landmarks mode): libGLESv2.so.2: ...
Model loaded successfully.
```

This is **normal and OK** as long as `Model loaded successfully` appears.

---

## Render deployment checklist

### Required service settings

| Setting | Correct value |
|---------|----------------|
| **Runtime** | Python 3 (not Node) |
| **Branch** | `main` |
| **Build command** | `pip install -r requirements.txt` |
| **Start command** | `cd web_app && gunicorn app:app --bind 0.0.0.0:$PORT --timeout 120 --workers 1 --threads 2` |
| **Or** | Use root `Procfile` (same command) |
| **Auto-deploy** | Recommended: ON |

### `requirements.txt` must include

```
lightgbm
opencv-python-headless
mediapipe
scikit-learn
flask
gunicorn
numpy==1.26.4
```

(`numpy==1.26.4` pins for Render Python 3.11; local Python 3.14 may need unpinned numpy.)

### Optional: `Aptfile` (Mesa libs)

Present for server MediaPipe; **not required** if client-landmarks path works.

---

## Common production failures (do not repeat)

### 1. Predictions show `-` (no letter)

| Symptom | Cause | Fix |
|---------|--------|-----|
| `POST /predict` **200, ~62 bytes** | `classifier is None` — model failed at import | Ensure `lightgbm` in requirements; landmarks-only init in `inference_classifier.py` |
| Render log: `No module named 'lightgbm'` | Missing dependency | Add `lightgbm` to `requirements.txt`, redeploy |
| Render log: `libGLESv2.so.2` + no "Model loaded" | Whole classifier crashed on init | Load LightGBM **before** HandLandmarker; catch detector errors; use client landmarks |
| Runtime **Node** on Render | Wrong runtime | Switch to **Python 3** in dashboard |
| Green skeleton works, `-` in UI | Browser OK, server broken | Fix server (above), not browser |

### 2. Slow on Render Free (not a “broken model” issue)

- **0.1 CPU**, cold starts (~50s after idle), network latency to Virginia.
- Matplotlib font cache on first boot (~30s in logs).
- Upgrading instance helps **speed**, not the libGLES/lightgbm bugs.

### 3. Documentation drift

- `src/4_train_model.py` still trains Random Forest — production model was trained via Kaggle notebook with LightGBM.
- All docs updated 2026-05-22 to reflect current LightGBM ensemble pipeline.

---

## Key files

| File | Role |
|------|------|
| `web_app/app.py` | Flask routes; `/predict` accepts `{ image, landmarks? }` |
| `web_app/inference_classifier.py` | LightGBM ensemble + engineer_features + optional server MediaPipe |
| `web_app/constants.py` | **Single source of truth** for LABELS mapping (30 classes) |
| `web_app/templates/index.html` | Client MediaPipe + EMA smoothing; sends landmarks with each predict |
| `web_app/surah_data.py` | Surah content; only **Al-Kawthar** fully unlocked |
| `Procfile` | Render start command |
| `requirements.txt` | Must include `lightgbm` |

---

## Local development

```powershell
cd c:\Users\hussa\Desktop\tabsirah
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt lightgbm   # on Python 3.14, omit numpy pin if install fails
cd web_app
python app.py
```

Open http://127.0.0.1:5000

---

## Render MCP (optional)

Official MCP: `https://mcp.render.com/mcp` — configure in `~/.cursor/mcp.json` with Render API key.

Useful prompts: list services, get deploy history, pull error logs for `tabsirah`.

Service ID: `srv-d5nge0khg0os73df7qcg`

---

## Verification after deploy

1. Render logs: `Model loaded successfully`
2. Browser: hand skeleton visible
3. **الإشارة** shows Arabic letter (not `-`)
4. `/predict` response **> 62 bytes** when hand visible (contains `"prediction":"..."`)

---

## Related docs

- [README.md](README.md) — user-facing overview  
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) — system design, prediction pipeline, API  
- [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) — Render deploy, troubleshooting  
- [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md) — dev setup, git workflow  
- [CHANGELOG.md](CHANGELOG.md) — version history  
