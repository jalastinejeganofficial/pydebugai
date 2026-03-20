# 💻 PyDebugAI - User Guide

Welcome to PyDebugAI! This guide shows you how to use the tool effectively.

---

## 📥 Installation

### Option 1: Install from PyPI (Recommended)

```bash
pip install pydebugai
```

### Option 2: Install from Source

```bash
cd c:\new-model-ai
pip install -e .
```

### Verify Installation

```bash
pydebugai --version
```

---

## 🚀 Quick Start

### Basic Usage

The simplest way to debug a Python file:

```bash
pydebugai run your_script.py
```

This will:
1. Execute your Python code
2. Catch any errors
3. Provide AI-powered fix suggestions

### Example Session

```bash
pydebugai run tests/samples/buggy_sample.py
```

Output:
```
╔═══════════════════════════════════════════════════════════╗
║         AI-Powered Python Debugging Assistant v0.1.0       ║
╚═══════════════════════════════════════════════════════════╝

🔍 Diagnostics
┌────────┬────────────────────┬────────────┬─────────────────┐
│ Line   │ Type               │ Severity   │ Message         │
├────────┼────────────────────┼────────────┼─────────────────┤
│ 11     │ ZeroDivisionError  │ ERROR      │ Division by     │
│        │                    │            │ zero            │
└────────┴────────────────────┴────────────┴─────────────────┘

💡 AI Fix Suggestions

#1 — ZeroDivisionError
Division By Zero
You're dividing a number by zero...

Fix Code:
if divisor != 0:
    result = numerator / divisor
else:
    result = 0
```

---

## 📋 CLI Commands Reference

### `pydebugai run` - Analyze a File

**Usage:**
```bash
pydebugai run <file.py> [options]
```

**Options:**

| Option | Description |
|--------|-------------|
| `--no-exec` | Static analysis only (don't execute the file) |
| `--deep` | Enable CodeBERT deep analysis (slower, more accurate) |
| `--json` | Output results as JSON (for piping to other tools) |

**Examples:**

```bash
# Basic analysis
pydebugai run script.py

# Static analysis only (safer for untrusted code)
pydebugai run script.py --no-exec

# Deep AI analysis (uses transformers)
pydebugai run script.py --deep

# Get JSON output for automation
pydebugai run script.py --json > results.json
```

---

### `pydebugai chat` - Interactive Mode

Start an interactive debugging session:

```bash
pydebugai chat
```

Then paste your code or error traceback:

```
>>> x = 10 / 0
>>> 
```

(Press Enter twice to submit)

The AI will analyze and provide suggestions.

---

### `pydebugai serve` - Start API Server

Start a local REST API server for VSCode extension or custom integrations:

```bash
pydebugai serve
```

Default: http://localhost:7432

**Server Endpoints:**

- `GET /status` - Health check
- `POST /analyze` - Analyze code snippet
- `POST /feedback` - Submit feedback
- `GET /stats` - View statistics

---

### `pydebugai stats` - View Statistics

Show self-learning statistics:

```bash
pydebugai stats
```

Displays:
- Number of feedback samples collected
- ML classifier accuracy
- Most common errors detected

---

## 🎯 Common Use Cases

### 1. Debug a Script That Won't Run

```bash
pydebugai run my_buggy_script.py
```

The AI will:
- Execute the script in a safe environment
- Capture the error
- Explain what went wrong
- Suggest fixes

### 2. Check Code Before Running (Static Analysis)

For untrusted code or when you want to avoid execution:

```bash
pydebugai run suspicious_script.py --no-exec
```

This catches:
- Syntax errors
- Undefined variables
- Type mismatches
- Import errors

### 3. Get Detailed AI Analysis

For complex bugs, use deep analysis:

```bash
pydebugai run complex_module.py --deep
```

This uses CodeBERT (transformer model) for deeper understanding.

### 4. Automate Debugging in CI/CD

Use JSON output for integration with other tools:

```bash
pydebugai run tests.py --json > bug_report.json
```

Parse the JSON in your pipeline to:
- Fail builds on critical errors
- Generate bug reports
- Track error trends

---

## 🔍 Understanding the Output

### Diagnostics Table

Shows all detected issues:

- **Line**: Where the error occurred
- **Type**: Error category (NameError, TypeError, etc.)
- **Severity**: ERROR (must fix) or WARNING (should fix)
- **Message**: Human-readable explanation

### Fix Suggestions

Each suggestion includes:

1. **Title**: Brief description
2. **Explanation**: Why this error occurred
3. **Fix Code**: Exact code snippet to fix it
4. **Confidence**: How sure the AI is (0-100%)
5. **Engine**: Which AI component found this

### Confidence Levels

- **90-100%** (█████████░): Very confident - apply this fix first
- **70-89%** (███████░░░): Likely correct - review carefully
- **50-69%** (█████░░░░░): Possible fix - use judgment
- **<50%** (██░░░░░░░░): Low confidence - consider alternative approaches

---

## 🧩 VSCode Extension Integration

For the best debugging experience, install the VSCode extension alongside the CLI.

### Setup

1. Install the extension from VSIX:
   ```bash
   code --install-extension vscode-extension/pydebugai-0.1.0.vsix
   ```

2. Start the server:
   ```bash
   pydebugai serve
   ```

3. Open your Python file in VSCode

### Features

Once connected, you get:

- 🔴 **Red squiggles** under error lines
- 💡 **Quick fixes** in the lightbulb menu
- 📝 **Hover hints** showing AI suggestions
- 🖥️ **Sidebar panel** with full analysis

---

## 🎓 Learning Examples

### Example 1: NameError (Undefined Variable)

**Buggy Code:**
```python
result = myundefinedvar + 10
```

**PyDebugAI Output:**
```
⚠️ NameError: 'myundefinedvar' is used before it is defined

Suggestion:
- Did you mean to define this variable first?
- Check for typos (did you mean 'my_defined_var'?)
```

### Example 2: ZeroDivisionError

**Buggy Code:**
```python
average = total / count  # count might be 0
```

**PyDebugAI Output:**
```
❌ ZeroDivisionError: Division by zero

Fix:
if count != 0:
    average = total / count
else:
    average = 0  # or handle appropriately
```

### Example 3: TypeError

**Buggy Code:**
```python
total = "100" + 50
```

**PyDebugAI Output:**
```
❌ TypeError: Can't concatenate str and int

Fix:
total = int("100") + 50  # Convert string to int
# OR
total = "100" + str(50)  # Convert int to string
```

### Example 4: AttributeError on None

**Buggy Code:**
```python
val = None
val.strip()
```

**PyDebugAI Output:**
```
❌ AttributeError: 'NoneType' object has no attribute 'strip'

Fix:
if val is not None:
    val.strip()
```

---

## ⚙️ Configuration

### Environment Variables

Customize behavior with environment variables:

```bash
# Set custom server port
export PYDEBUGAI_PORT=8000

# Disable ML features for faster startup
export PYDEBUGAI_NO_ML=1

# Enable verbose logging
export PYDEBUGAI_VERBOSE=1
```

### Settings File

Create `~/.pydebugai/config.json`:

```json
{
  "server_port": 7432,
  "enable_deep_analysis": false,
  "auto_execute": true,
  "max_suggestions": 5
}
```

---

## 🐛 Troubleshooting

### Issue: "Command not found: pydebugai"

**Solution:** Make sure pip installed the package correctly:

```bash
pip show pydebugai
```

If not found, reinstall:

```bash
pip uninstall pydebugai
pip install pydebugai
```

### Issue: ML classifier training fails

**Message:** "too few samples" or "not enough data"

**Solution:** This is normal for fresh installs. The classifier needs feedback data. Use the tool regularly and provide thumbs up/down to improve accuracy.

### Issue: Server won't start

**Solution:** Check if port 7432 is already in use:

```bash
# Windows
netstat -ano | findstr :7432

# Linux/Mac
lsof -i :7432
```

Kill the process or use a different port:

```bash
PYDEBUGAI_PORT=8000 pydebugai serve
```

### Issue: Slow performance

**Solution:** Disable heavy AI features:

```bash
pydebugai run script.py --no-exec
```

Or set environment variable:

```bash
export PYDEBUGAI_NO_ML=1
```

---

## 📚 Advanced Features

### Custom Rules

Add your own debugging rules in `~/.pydebugai/rules.json`:

```json
{
  "custom_rules": [
    {
      "pattern": "open\\(.*\\)",
      "message": "Consider using 'with open()' for automatic resource management",
      "severity": "warning"
    }
  ]
}
```

### Plugin System

PyDebugAI supports custom plugins. Create a Python module that implements:

```python
def analyze(code: str) -> List[Suggestion]:
    """Return list of suggestions for given code."""
    pass
```

Register in `~/.pydebugai/plugins.json`:

```json
{
  "plugins": ["my_custom_plugin"]
}
```

---

## 🆘 Getting Help

### Documentation

- README.md - Full project overview
- PUBLISHING_GUIDE.md - How to publish online
- This file - User guide

### Community Support

- GitHub Issues: Report bugs or request features
- Stack Overflow: Ask questions with tag `pydebugai`
- Discord/Slack: Join Python developer communities

### Direct Support

Contact: pydebugai@example.com (if you set this up)

---

## 🎉 Best Practices

1. **Run Early, Run Often**: Check your code frequently as you write
2. **Review All Suggestions**: Don't just apply the first fix - read explanations
3. **Provide Feedback**: Vote on suggestions to improve the AI
4. **Use Static Analysis First**: For untrusted code, use `--no-exec`
5. **Combine with Tests**: Use PyDebugAI alongside unit tests
6. **Learn From Errors**: Read explanations to understand root causes

---

**Happy Debugging! 🐛➡️✅**

May your code always run bug-free (or at least have great AI help when it doesn't)!
