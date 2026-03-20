# 📸 Visual Guide - PyPI Trusted Publisher Setup

Step-by-step with screenshots description of what you'll see.

---

## 🎯 What You're Doing

You're connecting your GitHub repository to PyPI so that when you create a release on GitHub, it automatically publishes to PyPI without needing API tokens.

---

## 📋 Step 1: Go to PyPI Publishing Page

### URL to Visit
```
https://pypi.org/manage/account/publishing/
```

### How to Get There
1. Go to https://pypi.org
2. Click your username (top right)
3. Click "Account settings"
4. Scroll down to "Publishing" section
5. Click "Add publisher"

---

## 📝 Step 2: Fill the Form

You'll see a form that looks like this:

```
┌─────────────────────────────────────────────────────┐
│ Add a new pending publisher                         │
├─────────────────────────────────────────────────────┤
│                                                     │
│ [GitHub] ○ GitLab ○ Google ○ ActiveState           │
│                                                     │
│ PyPI Project Name (required)                        │
│ ┌─────────────────────────────────────────────┐    │
│ │ pydebugai                                   │    │
│ └─────────────────────────────────────────────┘    │
│                                                     │
│ Owner (required)                                    │
│ ┌─────────────────────────────────────────────┐    │
│ │ YOUR_GITHUB_USERNAME                        │    │
│ └─────────────────────────────────────────────┘    │
│                                                     │
│ Repository name (required)                          │
│ ┌─────────────────────────────────────────────┐    │
│ │ pydebugai                                   │    │
│ └─────────────────────────────────────────────┘    │
│                                                     │
│ Workflow name (required)                            │
│ ┌─────────────────────────────────────────────┐    │
│ │ publish.yml                                 │    │
│ └─────────────────────────────────────────────┘    │
│                                                     │
│ Environment name (optional)                         │
│ ┌─────────────────────────────────────────────┐    │
│ │ pypi                                        │    │
│ └─────────────────────────────────────────────┘    │
│                                                     │
│              [ Add pending publisher ]              │
└─────────────────────────────────────────────────────┘
```

### What to Enter

| Field | What to Type | Example |
|-------|--------------|---------|
| **PyPI Project Name** | `pydebugai` | If taken, try `pydebug-ai` |
| **Owner** | Your GitHub username | `jalas` or your org |
| **Repository name** | Your repo name | `pydebugai` |
| **Workflow name** | `publish.yml` | Exact filename |
| **Environment name** | `pypi` | Optional but recommended |

---

## ✅ Step 3: After Submitting

You'll see one of two things:

### If Project Doesn't Exist Yet (Most Likely)
```
┌─────────────────────────────────────────────┐
│ ✓ Pending publisher added successfully      │
├─────────────────────────────────────────────┤
│ Project: pydebugai                          │
│ Publisher: GitHub Actions                   │
│ Owner: YOUR_USERNAME                        │
│ Repo: pydebugai                             │
│ Workflow: publish.yml                       │
│ Environment: pypi                           │
│                                             │
│ ⚠️ This is a PENDING publisher.            │
│ The project will be created when first     │
│ used.                                       │
└─────────────────────────────────────────────┘
```

### If Project Already Exists
```
┌─────────────────────────────────────────────┐
│ ✓ Trusted publisher added successfully      │
├─────────────────────────────────────────────┤
│ Project: pydebugai (exists)                 │
│ Publisher: GitHub Actions                   │
│ Status: ACTIVE                              │
└─────────────────────────────────────────────┘
```

---

## 🔧 Step 4: Configure GitHub (Optional but Recommended)

### Go to GitHub Repository Settings

URL: `https://github.com/YOUR_USERNAME/pydebugai/settings/environments`

### Create Environment

1. Click "New environment"
2. Type: `pypi`
3. Click "Configure environment"

### You'll See:
```
┌─────────────────────────────────────────────┐
│ Environment: pypi                           │
├─────────────────────────────────────────────┤
│ ☑ Required reviewers                        │
│   ┌───────────────────────────────────┐    │
│   │ Add reviewers                     │    │
│   └───────────────────────────────────┘    │
│   Add people who must approve deployments  │
│                                             │
│ ☑ Deployment branches                       │
│   ○ All branches                            │
│   ● Selected branches: [main]              │
│   Only these branches can deploy           │
│                                             │
│ ☑ Wait timer                                │
│   ┌─────┐ minutes                          │
│   │  0  │                                  │
│   └─────┘                                  │
│   Delay before deployment starts           │
│                                             │
│          [ Save protection rules ]          │
└─────────────────────────────────────────────┘
```

### Recommended Settings:
- ✅ **Required reviewers**: Add yourself
- ✅ **Deployment branches**: `main` only
- ✅ **Wait timer**: 0 minutes (or 5 for safety)

Click **"Save protection rules"**

---

## 🚀 Step 5: Create Your First Release

### Option A: Via GitHub Web Interface

1. **Go to Releases**
   ```
   https://github.com/YOUR_USERNAME/pydebugai/releases
   ```

2. **Click "Create a new release"**

3. **Fill in the form:**
   ```
   ┌─────────────────────────────────────────┐
   │ Create a new release                    │
   ├─────────────────────────────────────────┤
   │ Tag version: v0.1.0                     │
   │ Target: main                            │
   │ Release title: PyDebugAI v0.1.0         │
   │                                         │
   │ Describe this release:                  │
   │ ┌───────────────────────────────────┐  │
   │ │ ## What's New                     │  │
   │ │ - Initial release                 │  │
   │ │ - AI-powered debugging            │  │
   │ └───────────────────────────────────┘  │
   │                                         │
   │         [ Publish release ]             │
   └─────────────────────────────────────────┘
   ```

4. **Click "Publish release"**

### Option B: Via Command Line

```bash
# Using git
git tag -a v0.1.0 -m "PyDebugAI v0.1.0"
git push origin v0.1.0

# Or using GitHub CLI
gh release create v0.1.0 --title "PyDebugAI v0.1.0" --notes "Initial release"
```

---

## 👀 Step 6: Watch the Workflow Run

### Go to Actions Tab

URL: `https://github.com/YOUR_USERNAME/pydebugai/actions`

### You'll See:
```
┌─────────────────────────────────────────────┐
│ Actions / Publish to PyPI #1                │
├─────────────────────────────────────────────┤
│ Trigger: Release published by YOUR_NAME     │
│ Status: ● In progress (or ✓ Success)       │
│                                             │
│ Jobs:                                       │
│ ▼ build-and-publish                         │
│   ✓ Checkout code (3s)                     │
│   ✓ Set up Python (8s)                     │
│   ✓ Install build dependencies (15s)       │
│   ✓ Build package (25s)                    │
│   ✓ Verify package structure (2s)          │
│   ● Publish to PyPI (running...)           │
│                                             │
│ Total runtime: 2m 34s                      │
└─────────────────────────────────────────────┘
```

### Click on "Publish to PyPI" to See Logs:
```
$ python -m build
Building wheel...
Creating dist/pydebugai-0.1.0-py3-none-any.whl
Creating dist/pydebugai-0.1.0.tar.gz

$ pypa/gh-action-pypi-publish@release/v1
Uploading pydebugai-0.1.0-py3-none-any.whl...
✓ Upload successful!
Uploading pydebugai-0.1.0.tar.gz...
✓ Upload successful!
```

---

## 🎉 Step 7: Verify on PyPI

### Visit Your Project Page

URL: `https://pypi.org/project/pydebugai/`

### You'll See:
```
┌─────────────────────────────────────────────┐
│ pydebugai                                   │
│ AI-powered Python debugging assistant       │
├─────────────────────────────────────────────┤
│ Latest version: 0.1.0                       │
│ Released: Mar 20, 2026                      │
│ License: MIT                                │
│                                             │
│ Installation:                               │
│ pip install pydebugai                       │
│                                             │
│ Project links:                              │
│ - Homepage: github.com/.../pydebugai       │
│ - Source: github.com/.../pydebugai         │
│ - Tracker: github.com/.../issues           │
│                                             │
│ [ Install button ]                          │
└─────────────────────────────────────────────┘
```

---

## ✅ Verification Checklist

After everything is done, verify:

### On Your Computer
```bash
# Fresh install from PyPI
pip uninstall pydebugai
pip install pydebugai

# Check it works
pydebugai --version
# Output: 0.1.0

# Test it
pydebugai run your_test_file.py
```

### On PyPI
- [ ] Project page exists: https://pypi.org/project/pydebugai/
- [ ] Version 0.1.0 is listed
- [ ] Download buttons work
- [ ] Description shows correctly

### On GitHub
- [ ] Release tagged v0.1.0 exists
- [ ] Actions workflow ran successfully (green checkmark)
- [ ] Workflow logs show "Upload successful"

---

## 🆘 What If Something Goes Wrong?

### Scenario 1: "Project name already exists"

**What you'll see:**
```
❌ Error: Project name 'pydebugai' is not available
```

**What to do:**
1. Choose a different name (e.g., `pydebug-ai`)
2. Update in ALL files:
   - `setup.py`: Change `name="pydebugai"` → `name="pydebug-ai"`
   - `pyproject.toml`: Change `name = "pydebugai"` → `name = "pydebug-ai"`
   - PyPI trusted publisher form
   - GitHub workflow environment URL
3. Delete old publisher on PyPI and add new one
4. Try again

### Scenario 2: Workflow Fails

**What you'll see:**
```
❌ Publish to PyPI (red X)
```

**What to do:**
1. Click on the failed job
2. Read the error message
3. Common fixes:
   - Missing permissions → Add `id-token: write`
   - No files found → Run `python -m build` first
   - Permission denied → Check OIDC setup

### Scenario 3: Nothing Happens

**What you'll see:**
- No workflow runs
- No actions triggered

**What to do:**
1. Check Actions tab is enabled
2. Verify `.github/workflows/publish.yml` exists
3. Check workflow syntax: https://rhysd.github.io/actionlint/
4. Try manual trigger: Actions → "Run workflow"

---

## 📞 Where to Get Help

### Documentation
- Full guide: [`TRUSTED_PUBLISHER_SETUP.md`](TRUSTED_PUBLISHER_SETUP.md)
- Quick reference: [`QUICK_REFERENCE.md`](QUICK_REFERENCE.md)
- Official PyPI docs: https://docs.pypi.org/trusted-publishers/

### Support Channels
- GitHub Issues (on your repo)
- Stack Overflow (tag: `pypi`, `github-actions`)
- PyPI Discord/Slack communities

---

## 🎯 Summary

You've set up:
1. ✅ Trusted publisher on PyPI (no API tokens needed!)
2. ✅ GitHub Actions workflow (automatic publishing)
3. ✅ Security environment (controlled access)
4. ✅ Automated releases (just tag and push!)

**Result**: Every time you create a GitHub release, your package automatically publishes to PyPI! 🎉

---

**Next Steps**: 
- Test with a practice release
- Share your package with the world!
- Monitor downloads on https://pepy.tech/

**Estimated Time**: 15-20 minutes total  
**Difficulty**: Beginner-friendly  
**Security**: 🔒 Maximum (OIDC, no tokens stored)
