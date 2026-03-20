# 🚀 PyDebugAI - Quick Start Guide

Get started with PyDebugAI in 5 minutes!

---

## ⚡ Installation (1 minute)

```bash
pip install pydebugai
```

**Done!** You're ready to debug.

---

## 🎯 Basic Usage (30 seconds)

Debug any Python file:

```bash
pydebugai run my_script.py
```

That's it! The AI will find errors and suggest fixes.

---

## 📖 Common Commands

| Command | What it does |
|---------|-------------|
| `pydebugai run file.py` | Analyze and fix a Python file |
| `pydebugai chat` | Interactive debugging session |
| `pydebugai serve` | Start API server for VSCode |
| `pydebugai --help` | Show all commands |

---

## 💡 Example Session

**Create a buggy file** (`test.py`):
```python
x = 10 / 0  # Oops!
print(undefined_var)  # Another error
```

**Run PyDebugAI**:
```bash
pydebugai run test.py
```

**Get instant feedback**:
```
❌ ZeroDivisionError: Division by zero
⚠️ NameError: 'undefined_var' is undefined

💡 Fix Suggestions:
1. Add check before division: if divisor != 0
2. Define variable first: undefined_var = ...
```

---

## 🎓 Pro Tips

### Faster Analysis
For quick checks without execution:
```bash
pydebugai run file.py --no-exec
```

### Deeper Analysis
For complex bugs (slower but more thorough):
```bash
pydebugai run file.py --deep
```

### Automation
Get JSON output for scripts/CI:
```bash
pydebugai run file.py --json > results.json
```

---

## 🧩 VSCode Integration

Want red squiggles and hover hints in VSCode?

1. **Install extension**:
   ```bash
   code --install-extension vscode-extension/pydebugai-0.1.0.vsix
   ```

2. **Start server**:
   ```bash
   pydebugai serve
   ```

3. **Code in VSCode** - AI catches errors automatically!

---

## ❓ Need Help?

### View all options:
```bash
pydebugai --help
```

### Read full docs:
- `README.md` - Complete feature list
- `USER_GUIDE.md` - Detailed usage examples
- `PUBLISHING_GUIDE.md` - How to publish online

### Get support:
- GitHub Issues (if published)
- Stack Overflow
- Documentation files

---

## 🎉 That's It!

You now know everything to start debugging with AI assistance!

**Next steps:**
1. Try it on your own Python files
2. Install the VSCode extension for real-time feedback
3. Share with fellow developers!

---

**Happy Coding! 🐛➡️✨**
