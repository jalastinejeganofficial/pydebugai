# 🚀 Quick Reference - PyPI Trusted Publishing

## ⚡ 5-Minute Setup

### 1. On PyPI (https://pypi.org/manage/account/publishing/)
```
PyPI Project Name: pydebugai
Owner: YOUR_GITHUB_USERNAME
Repository: pydebugai
Workflow: publish.yml
Environment: pypi
```

### 2. On GitHub (already created ✅)
File: `.github/workflows/publish.yml` exists!

### 3. Push to GitHub
```bash
git add .
git commit -m "Setup automated PyPI publishing"
git push
```

### 4. Create Release
```bash
# Tag version
git tag v0.1.0
git push origin v0.1.0

# Or use GitHub CLI
gh release create v0.1.0 --title "v0.1.0" --notes "Initial release"
```

### 5. Watch it Publish! 🎉
- GitHub Actions: https://github.com/YOUR_USERNAME/pydebugai/actions
- PyPI: https://pypi.org/project/pydebugai/

---

## 📋 Checklist

- [ ] PyPI account created
- [ ] Trusted publisher added on PyPI
- [ ] Workflow file exists (`.github/workflows/publish.yml`) ✅
- [ ] Code pushed to GitHub
- [ ] GitHub environment "pypi" configured (optional but recommended)
- [ ] First release tag created
- [ ] Workflow ran successfully
- [ ] Package visible on PyPI

---

## 🔧 Common Commands

### Build Locally
```bash
python -m build
ls dist/
pip install dist/*.whl
```

### Create Release
```bash
git tag v0.1.1
git push origin v0.1.1
```

### Manual Workflow Trigger
- Go to: Actions → "Publish to PyPI" → "Run workflow"
- Select branch: `main`
- Click "Run workflow"

---

## 🆘 Troubleshooting

| Problem | Solution |
|---------|----------|
| Project name taken | Change to `pydebug-ai` everywhere |
| Workflow fails | Check OIDC permissions in workflow |
| Permission denied | Verify id-token: write in workflow |
| No package found | Run `python -m build` first |

---

## 📊 Verify Success

```bash
# Install from PyPI
pip install pydebugai

# Check version
pydebugai --version

# Should show: 0.1.0
```

---

## 🔗 Important Links

- **Your PyPI Project**: https://pypi.org/project/pydebugai/
- **GitHub Actions**: https://github.com/YOUR_USERNAME/pydebugai/actions
- **Trusted Publisher Settings**: https://pypi.org/manage/account/publishing/

---

**Full Guide**: See [`TRUSTED_PUBLISHER_SETUP.md`](TRUSTED_PUBLISHER_SETUP.md) for detailed instructions.
