# Contributing to Tabsirah

Thank you for your interest in contributing to Tabsirah! This document provides guidelines for contributing to the project.

## 🌟 Ways to Contribute

### 1. Report Bugs
- Use GitHub Issues to report bugs
- Include clear reproduction steps
- Provide your environment details (OS, browser, Python version)
- Include screenshots if applicable

### 2. Suggest Features
- Open a feature request issue
- Explain the use case and benefit
- Consider implementation complexity

### 3. Submit Code
- Follow the development workflow below
- Ensure code quality and testing
- Update documentation as needed

---

## 🔧 Development Workflow

### Setup
```bash
# Fork and clone the repository
git clone https://github.com/YOUR_USERNAME/tabsirah.git
cd tabsirah

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run locally
cd web_app
python app.py
```

### Branching Strategy
```
main (production)
  ├── develop (integration)
  │   ├── feature/your-feature-name
  │   ├── bugfix/issue-number-description
  │   └── hotfix/critical-fix
```

### Making Changes

1. **Create a branch**
```bash
git checkout -b feature/your-feature-name
```

2. **Make your changes**
   - Write clean, readable code
   - Add comments for complex logic
   - Follow existing code style

3. **Test your changes**
   - Test manually in browser
   - Ensure camera and predictions work
   - Check responsive design

4. **Commit with good messages**
```bash
git commit -m "feat: Add new surah to practice mode"
git commit -m "fix: Resolve camera initialization issue"
git commit -m "docs: Update installation instructions"
```

**Commit Message Format:**
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes (formatting)
- `refactor:` Code refactoring
- `test:` Adding tests
- `chore:` Maintenance tasks

5. **Push and create Pull Request**
```bash
git push origin feature/your-feature-name
```

---

## 📋 Code Style Guidelines

### Python (Flask Backend)
- Follow PEP 8 style guide
- Use descriptive variable names
- Add docstrings to functions
- Keep functions small and focused

```python
def process_image(image_data: str) -> dict:
    """
    Process base64 image and return prediction results.
    
    Args:
        image_data: Base64 encoded image string
        
    Returns:
        dict: Prediction result with landmarks
    """
    # Implementation
```

### JavaScript (Frontend)
- Use camelCase for variables
- Use const/let instead of var
- Add comments for complex logic
- Keep functions pure when possible

```javascript
/**
 * Normalize Arabic character variants for image lookup
 * @param {string} char - Arabic character to normalize
 * @returns {string} Normalized character
 */
function normalizeChar(char) {
    // Implementation
}
```

### HTML/CSS
- Use Tailwind CSS utility classes
- Follow RTL-first design for Arabic
- Ensure responsive design (mobile-first)
- Use semantic HTML tags

---

## 🧪 Testing Guidelines

### Manual Testing Checklist
- [ ] Camera initializes correctly
- [ ] Hand detection works in real-time
- [ ] Predictions are accurate
- [ ] Navigation works on all pages
- [ ] Responsive on mobile, tablet, desktop
- [ ] Arabic text renders correctly (RTL)
- [ ] Error tracking works in Recitation mode
- [ ] Sign images load correctly

### Browser Testing
Test on:
- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

---

## 📝 Documentation Guidelines

### Code Comments
- Explain "why", not "what"
- Use clear, concise language
- Update comments when code changes

### README Updates
- Keep installation steps current
- Update feature list
- Add new screenshots if UI changes

### CHANGELOG
- Document all changes
- Follow Keep a Changelog format
- Update version numbers

---

## 🚀 Pull Request Process

1. **Before submitting:**
   - Ensure code works locally
   - Update documentation
   - Add entry to CHANGELOG.md
   - Rebase on latest main

2. **PR Description should include:**
   - What changes were made
   - Why the changes are needed
   - How to test the changes
   - Screenshots (if UI changes)
   - Related issue numbers

3. **Review Process:**
   - Maintainers will review your PR
   - Address any requested changes
   - Once approved, PR will be merged

---

## 🎯 Priority Areas

We especially welcome contributions in these areas:

### High Priority
- [ ] Add more surahs to the practice system
- [ ] Improve model accuracy for difficult signs
- [ ] Add user authentication
- [ ] Implement progress saving

### Medium Priority
- [ ] Mobile app (React Native/Flutter)
- [ ] Offline PWA mode
- [ ] Gamification features
- [ ] Advanced analytics

### Low Priority
- [ ] UI theme customization
- [ ] Additional languages
- [ ] Social sharing features

---

## 📞 Questions?

- **Documentation**: Read [COMPLETE_PROJECT_DOCUMENTATION.md](COMPLETE_PROJECT_DOCUMENTATION.md)
- **Issues**: Check existing GitHub issues
- **Contact**: Open a new issue for questions

---

## 🙏 Code of Conduct

### Our Standards
- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive feedback
- Assume good intentions

### Unacceptable Behavior
- Harassment or discrimination
- Trolling or insulting comments
- Publishing private information
- Other unprofessional conduct

---

## 📜 License

By contributing to Tabsirah, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing to Tabsirah! May Allah accept your efforts. Ameen.**
