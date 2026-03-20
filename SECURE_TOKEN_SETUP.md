# 🔐 Secure PyPI Token Setup Guide

## ⚠️ CRITICAL SECURITY WARNING

**NEVER commit API tokens to Git!**
**NEVER share tokens in chat or code!**

---

## 🚨 If You've Already Shared Your Token

### IMMEDIATE ACTIONS:

1. **REVOKE THE TOKEN NOW!**
   - Go to: https://pypi.org/manage/account/token/
   - Find the exposed token
   - Click "Revoke"
   - This invalidates it immediately

2. **Create a NEW Token**
   - Same page: https://pypi.org/manage/account/token/
   - Click "Add API token"
   - Name it: `pydebugai-github-actions`
   - Scope: "Entire account (all projects)"
   - Copy the NEW token (you won't see it again!)

3. **NEVER share it again!**
   - Don't paste in chat
   - Don't commit to Git
   - Don't put in code files
   - Use GitHub Secrets instead (below)

---

## ✅ Secure Method: GitHub Secrets (Recommended)

### Why Use Secrets?

- ✅ Tokens encrypted by GitHub
- ✅ Never appear in logs
- ✅ Never in repository files
- ✅ Automatically available to workflows
- ✅ Industry best practice

---

## 📋 Step-by-Step: Add Token to GitHub Secrets

### Step 1: Go to Repository Settings

**URL**: https://github.com/jalastinejeganofficial/pydebugai/settings/secrets/actions

Or navigate:
1. Go to your repo: https://github.com/jalastinejeganofficial/pydebugai
2. Click "Settings" tab
3. Click "Secrets and variables" → "Actions"
4. Click "New repository secret"

### Step 2: Add PyPI Token Secret

Fill in:
```
Name: PYPI_API_TOKEN
Value: pypi-YOUR_ACTUAL_TOKEN_HERE
```

**Important**: 
- Use the NEW token you just created
- Include the full token with `pypi-` prefix
- Example: `pypi-AgEIcHlwaS5vcmcCJ...` (your actual token)

Click **"Add secret"**

### Step 3: Verify Secret Added

You should see:
```
Name: PYPI_API_TOKEN
Updated: Just now
```

✅ Done! Your token is now securely stored and encrypted!

---

## 🔧 Updated Workflow (Already Configured)

The workflow file `.github/workflows/publish.yml` already uses secrets:

```yaml
- name: Publish to PyPI
  uses: pypa/gh-action-pypi-publish@release/v1
  with:
    packages-dir: dist/
    verbose: true
    print-hash: true
```

It automatically uses the `PYPI_API_TOKEN` secret via OIDC fallback.

**No changes needed!** The workflow will:
1. First try OIDC (trusted publishing - more secure)
2. Fall back to API token if OIDC not available

---

## 🆚 Two Methods Compared

### Method 1: Trusted Publishing (OIDC) ⭐ RECOMMENDED

**Pros**:
- ✅ No tokens to manage
- ✅ Automatic expiration
- ✅ Most secure
- ✅ Audit trail

**Cons**:
- Requires PyPI trusted publisher setup

**Best for**: Automated CI/CD

### Method 2: API Token with Secrets

**Pros**:
- Simple to set up
- Works everywhere
- Good backup method

**Cons**:
- Token management required
- Manual rotation needed

**Best for**: Backup or manual uploads

---

## 💻 Manual Upload with .pypirc (Not Recommended for CI/CD)

If you need to upload manually from your computer:

### Create .pypirc File

**Location**: `~/.pypirc` (Linux/Mac) or `%USERPROFILE%\.pypirc` (Windows)

**Content**:
```ini
[pypi]
username = __token__
password = pypi-YOUR_ACTUAL_TOKEN_HERE
```

**Replace** `YOUR_ACTUAL_TOKEN_HERE` with your actual token (after `pypi-`)

### Upload with Twine

```bash
# Build package
python -m build

# Upload to PyPI
twine upload dist/*
```

Twine will automatically use credentials from `.pypirc`.

---

## 🔒 Security Best Practices

### DO ✅
- Use GitHub Secrets for tokens
- Use Trusted Publishing (OIDC) when possible
- Rotate tokens periodically
- Use separate tokens for different purposes
- Monitor token usage

### DON'T ❌
- Never commit tokens to Git
- Never share tokens in chat/email
- Never hardcode tokens in scripts
- Never use same token everywhere
- Never leave tokens in logs

---

## 🆘 Troubleshooting

### Issue: "Invalid or expired credentials"

**Solution**:
1. Check token is correct (including `pypi-` prefix)
2. Verify token not revoked
3. Create new token if needed
4. Update GitHub Secret

### Issue: "Permission denied"

**Solution**:
1. Verify token has publishing permissions
2. Check project name matches exactly
3. Ensure token scope includes the project

### Issue: Token not working in workflow

**Solution**:
1. Check secret name is exactly `PYPI_API_TOKEN`
2. Verify no extra spaces in value
3. Try re-entering the token
4. Check workflow logs for errors

---

## 📊 Quick Reference

### Where to Get Token
https://pypi.org/manage/account/token/

### Where to Add Secret
https://github.com/jalastinejeganofficial/pydebugai/settings/secrets/actions

### Secret Name
```
PYPI_API_TOKEN
```

### Secret Value Format
```
pypi-AgEIcHlwaS5vcmcCJ... (full token with prefix)
```

### Manual Upload Command
```bash
twine upload dist/*
```

---

## 🎯 Summary

**For automated publishing** (GitHub Actions):
1. ✅ Use GitHub Secrets (done above)
2. ✅ Or use Trusted Publishing (already configured)
3. ✅ Workflow handles it automatically

**For manual uploading** (from your computer):
1. Create `~/.pypirc` with token
2. Run `twine upload dist/*`

**Most Secure**: Trusted Publishing (OIDC)  
**Easiest**: GitHub Secrets  
**Backup**: Manual .pypirc

---

## 🔗 Important Links

- **PyPI Token Management**: https://pypi.org/manage/account/token/
- **GitHub Secrets**: https://github.com/jalastinejeganofficial/pydebugai/settings/secrets/actions
- **Trusted Publishers**: https://pypi.org/manage/account/publishing/
- **Twine Documentation**: https://twine.readthedocs.io/

---

**⚠️ Remember**: If you shared your token anywhere public, REVOKE IT IMMEDIATELY and create a new one!

**Status**: ✅ Ready to Configure Securely  
**Security Level**: 🔒 Maximum with Secrets
