# 🔐 PyPI Trusted Publisher Setup Guide (GitHub Actions)

Complete step-by-step guide to configure automated PyPI publishing using GitHub Actions and OpenID Connect (OIDC).

---

## 🎯 What This Does

**Trusted Publishing** allows GitHub Actions to publish your package to PyPI **without storing API tokens**. Instead, it uses OIDC (OpenID Connect) for secure, automatic authentication.

### Benefits
- ✅ **No API tokens to manage or rotate**
- ✅ **Automatic expiration** (tokens last only for the workflow run)
- ✅ **Fine-grained permissions** (only publish, nothing else)
- ✅ **Audit trail** (all publishes logged in both GitHub and PyPI)
- ✅ **Secure by default** (uses OIDC federation)

---

## 📋 Prerequisites Checklist

Before you start:

- [ ] Create PyPI account at https://pypi.org/account/register/
- [ ] Verify your email address on PyPI
- [ ] Have a GitHub account
- [ ] Push your code to GitHub (repository must exist)
- [ ] Ensure your project has `pyproject.toml` or `setup.py` ✅ (you have both!)

---

## 🚀 Step-by-Step Setup

### **Step 1: Add Trusted Publisher on PyPI**

1. **Go to PyPI Account Settings**
   - Visit: https://pypi.org/manage/account/publishing/
   - Or: Click your username → "Account settings" → "Add publisher"

2. **Fill in the Form**

   Based on your PyDebugAI project:

   ```
   PyPI Project Name*: pydebugai
   Owner*: YOUR_GITHUB_USERNAME
   Repository name*: pydebugai
   Workflow name*: publish.yml
   Environment name (optional): pypi
   ```

   **Field Explanations**:

   | Field | Value | Notes |
   |-------|-------|-------|
   | **PyPI Project Name** | `pydebugai` | Must match exactly what will be on PyPI |
   | **Owner** | Your GitHub username | e.g., `jalas` or your org name |
   | **Repository name** | `pydebugai` | Your repo name (case-insensitive) |
   | **Workflow name** | `publish.yml` | The file we created above |
   | **Environment** | `pypi` | Recommended for extra security |

3. **Click "Add pending publisher"**
   - If project doesn't exist yet → becomes "pending"
   - If project exists → immediately active

4. **Copy the configuration** (optional but helpful)
   - PyPI will show you a summary
   - Save it for reference

---

### **Step 2: Configure GitHub Repository**

#### 2a. Create Publishing Workflow ✅ (Already Done!)

I've already created `.github/workflows/publish.yml` for you with:

```yaml
name: Publish to PyPI

on:
  release:
    types: [published]  # Triggers when you create a GitHub release
  workflow_dispatch:     # Allows manual trigger

permissions:
  contents: read
  id-token: write  # ⭐ Required for OIDC

jobs:
  build-and-publish:
    runs-on: ubuntu-latest
    
    environment:
      name: pypi
      url: https://pypi.org/p/pydebugai
    
    steps:
      - uses: actions/checkout@v4
      
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      
      - run: pip install build twine
      
      - run: python -m build
      
      - uses: pypa/gh-action-pypi-publish@release/v1
```

#### 2b. Create GitHub Environment (Recommended)

1. **Go to Repository Settings**
   - Visit: `https://github.com/YOUR_USERNAME/pydebugai/settings/environments`
   - Or: Repo → Settings → Environments → "New environment"

2. **Create Environment**
   ```
   Name: pypi
   ```

3. **Configure Protection Rules** (optional but recommended)
   - ✅ **Required reviewers**: Add yourself or trusted collaborators
   - ✅ **Deployment branches**: Select "Selected branches" → `main` only
   - ✅ **Wait timer**: Optional delay before deployment

4. **Save protection rules**

---

### **Step 3: Push Everything to GitHub**

Commit and push all files:

```bash
cd c:\new-model-ai

# Initialize git if not already done
git init
git add .
git commit -m "Setup PyPI trusted publishing with GitHub Actions"

# Add remote (replace with your actual repo URL)
git remote add origin https://github.com/YOUR_USERNAME/pydebugai.git

# Push to GitHub
git branch -M main
git push -u origin main
```

---

### **Step 4: Create Your First Release**

The workflow triggers when you create a **GitHub Release**:

#### Option A: Via GitHub Web UI

1. **Go to Releases Page**
   - Visit: `https://github.com/YOUR_USERNAME/pydebugai/releases`
   - Or: Repo → "Releases" → "Create a new release"

2. **Choose Tag Version**
   ```
   Tag version: v0.1.0
   Target: main
   Release title: PyDebugAI v0.1.0 - Initial Release
   ```

3. **Write Release Notes**
   ```markdown
   ## What's New
   
   - Initial release of PyDebugAI
   - AI-powered Python debugging
   - 600+ training samples
   - VSCode extension support
   
   ## Installation
   
   ```bash
   pip install pydebugai
   ```
   
   ## Features
   
   - AST static analysis
   - Rule engine with 60+ rules
   - ML classifier
   - Levenshtein fixer
   ```

4. **Click "Publish release"**

#### Option B: Via Git Command Line

```bash
# Tag your release
git tag -a v0.1.0 -m "PyDebugAI v0.1.0 - Initial Release"
git push origin v0.1.0

# Or use GitHub CLI
gh release create v0.1.0 --title "PyDebugAI v0.1.0" --notes "Initial release"
```

---

### **Step 5: Watch the Magic Happen!**

Once you create the release:

1. **GitHub Actions Automatically Starts**
   - Visit: `https://github.com/YOUR_USERNAME/pydebugai/actions`
   - You'll see "Publish to PyPI" workflow running

2. **Workflow Steps** (takes ~2-5 minutes)
   - ✅ Checkout code
   - ✅ Set up Python
   - ✅ Install dependencies
   - ✅ Build package (`.tar.gz` and `.whl`)
   - ✅ Upload to PyPI via OIDC

3. **Check Results**
   - Green checkmark = Success! ✅
   - Red X = Check logs for errors ❌

4. **Verify on PyPI**
   - Visit: `https://pypi.org/project/pydebugai/`
   - Your package should appear!
   - Version 0.1.0 should be listed

---

## 🧪 Testing Before Publishing

### Test Locally First

```bash
# Build the package
python -m build

# Check structure
ls -la dist/
# Should show:
# - pydebugai-0.1.0-py3-none-any.whl
# - pydebugai-0.1.0.tar.gz

# Test installation locally
pip install dist/pydebugai-0.1.0-py3-none-any.whl

# Verify it works
pydebugai --version
```

### Test on TestPyPI (Optional)

Before publishing to real PyPI, test on TestPyPI:

1. **Create TestPyPI account**: https://test.pypi.org/account/register/

2. **Add separate trusted publisher** for TestPyPI following same steps

3. **Modify workflow** to use TestPyPI:

```yaml
- uses: pypa/gh-action-pypi-publish@release/v1
  with:
    repository-url: https://test.pypi.org/legacy/
```

---

## 🔧 Troubleshooting

### Issue: "Project name already exists"

**Problem**: Someone else owns `pydebugai` on PyPI

**Solutions**:
1. Choose a unique name in ALL places:
   - `setup.py`: `name="pydebug-ai"`
   - `pyproject.toml`: `name = "pydebug-ai"`
   - PyPI trusted publisher form
   - GitHub workflow environment URL

2. Update everywhere:

```python
# setup.py
name="pydebug-ai",  # Changed from pydebugai
```

```toml
# pyproject.toml
name = "pydebug-ai",
```

---

### Issue: "Publisher already exists" or "Forbidden"

**Problem**: Configuration mismatch

**Check**:
1. GitHub username matches exactly (case-sensitive for some parts)
2. Repository name is correct
3. Workflow filename is exactly `publish.yml`
4. Environment name matches (`pypi`)

**Fix**: Delete and recreate the publisher on PyPI

---

### Issue: Workflow fails with "No package found"

**Problem**: Build didn't create distribution files

**Solution**:
```bash
# Test build manually
python -m build

# Check dist/ folder exists and has files
ls -la dist/
```

Ensure `pyproject.toml` and `setup.py` are correct.

---

### Issue: "Permission denied" or "Insufficient permissions"

**Problem**: Missing OIDC permissions

**Solution**: Verify workflow has:

```yaml
permissions:
  contents: read
  id-token: write  # ⭐ This is required!
```

---

### Issue: Environment protection blocking deploy

**Problem**: Manual approval required

**Solution**:
- Go to GitHub → Repo → Settings → Environments → pypi
- Either remove required reviewers OR
- Approve the deployment manually in Actions tab

---

## 📊 Monitoring and Maintenance

### Check Publishing History

**On GitHub**:
- Visit: `https://github.com/YOUR_USERNAME/pydebugai/actions`
- See all workflow runs
- Click on each to view logs

**On PyPI**:
- Visit: `https://pypi.org/manage/project/pydebugai/releases/`
- See all versions
- View publish timestamps and publisher info

### Update Package

To publish a new version:

1. **Update version numbers**:
   ```python
   # setup.py
   version="0.1.1",  # Bump version
   ```

   ```toml
   # pyproject.toml
   version = "0.1.1",
   ```

   ```python
   # pydebugai/__init__.py
   __version__ = "0.1.1"
   ```

2. **Commit and push**:
   ```bash
   git add .
   git commit -m "Bump version to 0.1.1"
   git push
   ```

3. **Create new release**:
   ```bash
   gh release create v0.1.1 --title "PyDebugAI v0.1.1" --notes "Bug fixes"
   ```

4. **Workflow automatically publishes!** ✅

---

## 🔐 Security Best Practices

### 1. Use GitHub Environments ✅ (You configured this!)

```yaml
environment:
  name: pypi
  url: https://pypi.org/p/pydebugai
```

This adds:
- Required reviewers
- Branch restrictions
- Wait timers
- Deployment history

### 2. Limit to Main Branch Only

In environment settings:
- ✅ **Deployment branches**: `main` only
- ❌ Prevent accidental publishes from feature branches

### 3. Require Approval for First Deploy

Add yourself as required reviewer:
- Prevents unauthorized publishes
- Adds audit trail

### 4. Monitor OIDC Logs

Check GitHub Actions logs for:
- Who triggered the workflow
- What commit was published
- OIDC token exchange details

---

## 🎉 Success Checklist

After everything is set up:

- [ ] Trusted publisher added on PyPI ✅
- [ ] GitHub workflow created (`.github/workflows/publish.yml`) ✅
- [ ] Code pushed to GitHub ✅
- [ ] GitHub environment configured ✅
- [ ] First release created ✅
- [ ] Workflow ran successfully ✅
- [ ] Package visible on PyPI ✅
- [ ] Package installable via pip ✅

```bash
# Final verification
pip install pydebugai
pydebugai --version
```

---

## 📚 Additional Resources

### Official Documentation

- [PyPI Trusted Publishers](https://docs.pypi.org/trusted-publishers/)
- [GitHub Actions OIDC](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/about-security-hardening-with-openid-connect)
- [gh-action-pypi-publish](https://github.com/pypa/gh-action-pypi-publish)

### Examples

- [Real-world trusted publisher examples](https://github.com/pypa/gh-action-pypi-publish/tree/main/examples)
- [PyPA sample workflows](https://github.com/pypa/sampleproject)

### Tools

- **GitHub CLI**: `gh release create` for easy releases
- **Build**: `python -m build` for local testing
- **Twine**: `twine check dist/*` to verify packages

---

## 🆘 Need Help?

### Common Questions

**Q: Can I use this with GitLab instead of GitHub?**  
A: Yes! PyPI also supports GitLab CI/CD with OIDC. Choose "GitLab" tab in the publisher form.

**Q: What if I want to publish manually sometimes?**  
A: The workflow includes `workflow_dispatch` trigger, allowing manual runs from Actions tab.

**Q: Can multiple people publish?**  
A: Yes, give them commit access + add them as environment reviewers.

**Q: How do I rotate credentials?**  
A: No need! OIDC tokens expire after each workflow run automatically.

**Q: What if GitHub is down?**  
A: Keep an API token as backup in your PyPI account settings.

---

## 🎯 Next Steps After Setup

1. **Test the workflow**: Create a test release (v0.1.0-test)
2. **Announce your package**: Share on social media, Reddit, etc.
3. **Monitor downloads**: Use https://pepy.tech/projects/pydebugai
4. **Collect feedback**: Watch GitHub issues and PyPI downloads
5. **Plan next release**: Roadmap features based on user feedback

---

**🎊 Congratulations! You now have automated, secure PyPI publishing!**

Your package will automatically publish whenever you create a GitHub release, with no manual intervention or API token management needed! 🚀

---

**Last Updated**: March 2026  
**Status**: ✅ Ready to Use  
**Estimated Setup Time**: 15-20 minutes
