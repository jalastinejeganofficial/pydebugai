# 🔐 Add Your PyPI Token to GitHub Secrets - Quick Guide

## ⚠️ FIRST: Revoke Your Exposed Token!

**Your token was shared in chat - this is dangerous!**

### Immediate Actions:

1. **Go revoke it NOW**: https://pypi.org/manage/account/token/
   - Find the token you shared
   - Click "Revoke"
   - This makes it useless immediately

2. **Create a NEW token**:
   - Same page: Click "Add API token"
   - Name: `pydebugai-github-automation`
   - Scope: "Entire account (all projects)"
   - Click "Add token"
   - **COPY THE NEW TOKEN** (you won't see it again!)
   - Example format: `pypi-AgEIcHlwaS5vcmcCJDdlYzNiMGQ0...`

---

## ✅ Add Token to GitHub Secrets (3 Steps)

### Step 1: Go to Secrets Page

**URL**: https://github.com/jalastinejeganofficial/pydebugai/settings/secrets/actions

Or navigate manually:
1. Go to: https://github.com/jalastinejeganofficial/pydebugai
2. Click **"Settings"** tab (top menu)
3. Click **"Secrets and variables"** → **"Actions"**
4. Click **"New repository secret"** button

---

### Step 2: Fill in the Secret

You'll see a form. Fill it in like this:

```
┌─────────────────────────────────────────────┐
│ New repository secret                       │
├─────────────────────────────────────────────┤
│                                             │
│ Name:                                       │
│ ┌─────────────────────────────────────┐    │
│ │ PYPI_API_TOKEN                      │    │
│ └─────────────────────────────────────┘    │
│                                             │
│ Value:                                      │
│ ┌─────────────────────────────────────┐    │
│ │ pypi-YOUR_NEW_TOKEN_HERE            │    │
│ └─────────────────────────────────────┘    │
│      ^ Paste your ENTIRE new token here    │
│                                             │
│          [ Add secret ]                     │
└─────────────────────────────────────────────┘
```

**Important**:
- **Name**: Must be exactly `PYPI_API_TOKEN` (case-sensitive)
- **Value**: Paste your NEW token (the full thing with `pypi-` prefix)
- Example value: `pypi-AgEIcHlwaS5vcmcCJDdlYzNiMGQ0LTNhZDQtNDk0My1iNWU4LWE3OGE1YjNmMmJlMgACKlszLCI5NGNjMjkxMC00OTg4LTRkZTctYmIwMi0wYjU0YTViZDMyNjQiXQAABiD...`

Click **"Add secret"**

---

### Step 3: Verify It's Added

You should now see:

```
┌─────────────────────────────────────────────┐
│ Repository secrets                          │
├─────────────────────────────────────────────┤
│ Name                Updated                 │
├─────────────────────────────────────────────┤
│ PYPI_API_TOKEN      Just now                │
└─────────────────────────────────────────────┘
```

✅ **Done!** Your token is now securely stored and encrypted by GitHub.

---

## 🎯 What Happens Next

The workflow file `.github/workflows/publish.yml` will automatically use this token when publishing to PyPI.

When you create a release:
1. GitHub Actions builds your package
2. Uses the secret token to authenticate
3. Uploads to PyPI
4. **No tokens visible anywhere!** ✨

---

## 🔒 Security Notes

### Why GitHub Secrets?

- ✅ **Encrypted storage** - GitHub encrypts your tokens
- ✅ **Never in logs** - Tokens never appear in workflow logs
- ✅ **Never in repo** - Not committed to Git history
- ✅ **Automatic rotation** - Easy to update when needed
- ✅ **Industry standard** - Used by all professional projects

### What NOT to Do

❌ Don't paste tokens in chat (like you did - that's why we revoke!)  
❌ Don't commit tokens to Git  
❌ Don't hardcode in scripts  
❌ Don't email tokens  
❌ Don't reuse tokens across projects  

---

## 🆚 Two Methods Available

Your workflow now supports BOTH methods:

### Method 1: Trusted Publishing (OIDC) ⭐ BEST

**Already configured!** No tokens needed.

**How it works**:
- GitHub proves identity to PyPI via OIDC
- Temporary credentials (expire after workflow)
- Most secure option

**Setup**: Add trusted publisher on PyPI (see TRUSTED_PUBLISHER_SETUP.md)

### Method 2: API Token (Backup)

**What you just configured above**.

**How it works**:
- Uses `PYPI_API_TOKEN` secret
- Falls back if OIDC not available
- Good backup method

**Setup**: Just done! (add the secret above)

---

## 💻 Manual Upload (Optional)

If you want to upload manually from your computer:

### Create .pypirc File

**Windows location**: `%USERPROFILE%\.pypirc`  
**Linux/Mac location**: `~/.pypirc`

**Content**:
```ini
[pypi]
username = __token__
password = pypi-YOUR_ACTUAL_TOKEN_HERE
```

Replace `YOUR_ACTUAL_TOKEN_HERE` with your actual new token.

### Upload Command

```bash
# Build package first
python -m build

# Upload to PyPI
twine upload dist/*
```

Twine will read credentials from `.pypirc` automatically.

**Note**: For CI/CD, use GitHub Secrets instead (more secure).

---

## ✅ Complete Checklist

After adding the secret:

- [ ] Old token revoked on PyPI ✅
- [ ] New token created ✅
- [ ] Secret added as `PYPI_API_TOKEN` ✅
- [ ] Workflow updated (already done) ✅
- [ ] Ready to publish! ✅

---

## 🎉 You're All Set!

Now when you create a release, the workflow will:

1. Build your package automatically
2. Use the secret token to authenticate
3. Upload to PyPI securely
4. No tokens exposed anywhere!

**Next step**: Create a release and watch it publish! 🚀

```bash
git tag v0.1.0
git push origin v0.1.0
```

Then check: https://github.com/jalastinejeganofficial/pydebugai/actions

---

## 📞 Quick Links

- **Add Secret**: https://github.com/jalastinejeganofficial/pydebugai/settings/secrets/actions/new
- **View Secrets**: https://github.com/jalastinejeganofficial/pydebugai/settings/secrets/actions
- **PyPI Tokens**: https://pypi.org/manage/account/token/
- **Workflow File**: https://github.com/jalastinejeganofficial/pydebugai/blob/main/.github/workflows/publish.yml

---

## 🆘 Troubleshooting

### "Invalid or expired credentials"

**Fix**:
1. Verify token is correct (includes `pypi-` prefix)
2. Check token not revoked
3. Re-enter the secret carefully
4. Try creating another new token

### "Permission denied"

**Fix**:
1. Verify token has publishing permissions
2. Check project name matches exactly
3. Ensure you own the PyPI project

### Workflow still fails

**Fix**:
1. Check workflow logs for specific error
2. Verify secret name is exactly `PYPI_API_TOKEN`
3. Make sure no extra spaces in token value
4. Try re-entering the token

---

**Security Status**: 🔒 Maximum with GitHub Secrets  
**Ready to Deploy**: ✅ Yes  
**Token Management**: ✅ Secure and Encrypted
