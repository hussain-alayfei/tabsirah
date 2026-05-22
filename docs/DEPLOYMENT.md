# Deployment

Production deployment guide for Tabsirah on Render.

---

## Quick Reference

| Item | Value |
|------|-------|
| **Platform** | Render (Free tier) |
| **URL** | https://tabsirah.onrender.com |
| **Service ID** | `srv-d5nge0khg0os73df7qcg` |
| **Runtime** | Python 3 (not Node) |
| **Branch** | `main` → auto-deploy ON |
| **Python version** | 3.11 |

---

## Render Service Settings

| Setting | Value |
|---------|-------|
| Runtime | **Python 3** |
| Branch | `main` |
| Build command | `pip install -r requirements.txt` |
| Start command | `cd web_app && gunicorn app:app --bind 0.0.0.0:$PORT --timeout 120 --workers 1 --threads 2` |
| Auto-deploy | ON (recommended) |

The `Procfile` at repo root contains the same start command.

---

## Required Dependencies (`requirements.txt`)

```
opencv-python-headless
mediapipe
scikit-learn
flask
gunicorn
lightgbm
numpy==1.26.4
```

`numpy==1.26.4` is pinned for Render's Python 3.11. Local Python 3.14 may need an unpinned version.

---

## Expected Startup Logs

Normal healthy startup on Render:

```
HandLandmarker unavailable (client-landmarks mode): libGLESv2.so.2: ...
[inference] Loaded 3 model(s), use_engineered=True, n_features_expected=62
Model loaded successfully.
```

The `HandLandmarker unavailable` message is **expected and OK** — the app uses client-sent landmarks instead.

---

## Verification After Deploy

1. **Render logs**: Confirm `Model loaded successfully` appears
2. **Browser**: Hand skeleton visible (green overlay)
3. **الإشارة badge**: Shows an Arabic letter (not `-`) when hand is visible
4. **`/predict` response**: >62 bytes when hand visible (contains `"prediction":"..."`)

---

## Common Production Failures

### Predictions show `-` (no letter)

| Symptom | Cause | Fix |
|---------|-------|-----|
| `POST /predict` 200, ~62 bytes | `classifier is None` — model failed at import | Ensure `lightgbm` in requirements; check startup logs |
| `No module named 'lightgbm'` in logs | Missing dependency | Add `lightgbm` to `requirements.txt`, redeploy |
| `libGLESv2` + no "Model loaded" | Whole classifier crashed during init | LightGBM must load **before** HandLandmarker; catch detector errors |
| Runtime set to **Node** on Render | Wrong runtime | Switch to **Python 3** in dashboard |
| Green skeleton works, `-` in UI | Browser detection OK, server broken | Fix server classifier (above) |

### Slow on Render Free Tier

- 0.1 CPU, cold starts ~50s after idle, network latency
- Matplotlib font cache on first boot (~30s)
- Upgrading instance helps **speed**, not the lightgbm/libGLES bugs

### Feature Mismatch Errors

If you see `[inference] feature mismatch: got X, model expects Y` in logs:
- The model expects 62 features but `use_engineered` is False, or vice versa
- Check the pickle's `use_engineered` flag matches the model's `n_features_in_`

---

## Render MCP (Optional)

Official MCP: `https://mcp.render.com/mcp`

Configure in `~/.cursor/mcp.json` with your Render API key.

Useful for: listing services, deploy history, pulling error logs.

---

## Local Development

```powershell
cd c:\Users\hussa\Desktop\tabsirah
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
cd web_app
python app.py
```

Open http://127.0.0.1:5000

---

## Deploy Workflow

1. Make changes on `dev` (or a feature branch merged into `dev`)
2. Test locally (`python web_app/app.py`)
3. Push to `dev` — **CI runs automatically** (GitHub Actions pytest)
4. Confirm CI passes (green check on GitHub)
5. Merge `dev` → `main` (or `git checkout main && git merge dev`)
6. Push `main` — Render auto-deploys within ~2 minutes
7. Check Render logs and verify (see checklist above)

**Never push directly to `main` without testing locally and confirming CI passes first.**
