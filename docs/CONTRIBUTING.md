# Contributing

How to contribute to Tabsirah, including development setup and git conventions.

---

## Development Setup

```bash
# Clone
git clone https://github.com/hussain-alayfei/tabsirah.git
cd tabsirah

# Virtual environment
python -m venv venv
# Windows: .\venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

# Install all deps (production + dev)
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/ -v

# Start the app
cd web_app && python app.py
```

---

## Git Workflow

### Branches

| Branch | Purpose |
|--------|---------|
| `main` | Production — auto-deploys to Render |
| `develop` | Integration branch for feature merges |
| Feature branches | `feature/description` or `fix/description` |

### Rules

1. **Never push directly to `main`** unless it's an urgent production fix
2. Feature work: branch from `develop` → PR → merge to `develop`
3. Releases: merge `develop` → `main` (triggers deploy)
4. Never commit `.env`, API keys, or `~/.cursor/mcp.json`

### Commit Messages

Use conventional commits:

```
feat: add new surah content
fix: resolve prediction null bug
docs: update architecture guide
chore: remove dead files
refactor: extract label constants
test: add engineer_features tests
```

---

## Code Guidelines

### Python
- Target Python 3.11 (Render runtime)
- UTF-8 encoding for all files
- Follow existing patterns in `web_app/`
- Import label mappings from `web_app/constants.py` — never duplicate

### JavaScript
- Inline in `templates/index.html` (monolith, for now)
- Use `const`/`let`, no `var`
- MediaPipe landmarks are smoothed via EMA before use

### Testing
- Tests live in `tests/`
- Run with `python -m pytest tests/ -v`
- At minimum, test any changes to `engineer_features()` or model loading

---

## How to Contribute

### Report Bugs
Open a GitHub issue with:
- Steps to reproduce
- Expected vs actual behavior
- Browser/OS info
- Console/server logs if available

### Submit Code
1. Fork the repo
2. Create a branch (`feature/my-change`)
3. Make your changes
4. Run tests: `python -m pytest tests/`
5. Submit a pull request to `develop`

### Add a New Surah
1. Add content in `web_app/surah_data.py`
2. Set `unlocked: True` if it should be immediately available
3. Test both Reading and Reciting modes

---

## Key Files to Know

| File | What it does |
|------|-------------|
| `web_app/app.py` | Flask routes |
| `web_app/inference_classifier.py` | LightGBM prediction pipeline |
| `web_app/constants.py` | Label mapping (single source of truth) |
| `web_app/surah_data.py` | Surah content |
| `web_app/templates/index.html` | Full frontend SPA |
| `requirements.txt` | Production dependencies |
| `Procfile` | Render start command |
