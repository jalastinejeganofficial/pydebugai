# PyDebugAI 🐛

> **AI-powered Python debugging assistant** — like ChatGPT, but exclusively for Python errors.
> Installable via `pip`. Runs in your terminal and in VSCode.

---

## Features

| Feature | Description |
|---------|-------------|
| 🔍 **AST Static Analysis** | Catches errors before running — undefined names, division by zero, type mismatches |
| 🤖 **Rule Engine** | 60+ hand-crafted rules for instant, deterministic fixes |
| 🧠 **ML Classifier** | TF-IDF + Random Forest classifies error types with high confidence |
| 📝 **Levenshtein Fixer** | Detects typos in variable/function names and suggests corrections |
| 🚀 **CodeBERT** | Deep semantic code understanding via HuggingFace transformers |
| 📚 **Self-Learning** | SQLite + RLHF-lite — improves from every upvote/downvote |
| 🧩 **VSCode Extension** | Red squiggles, hover hints, quick-fix menu, sidebar chat panel |
| 💻 **CLI Runner** | `pydebugai run file.py` — run and debug from your terminal |

---

## Quick Start

### 1. Install via pip

```bash
pip install pydebugai
```

Or install from source (this repo):

```bash
cd c:\new-model-ai
pip install -e .
```

### 2. Run the CLI

```bash
# Analyze a Python file
pydebugai run my_script.py

# Interactive chat mode (paste code or errors)
pydebugai chat

# Start the local API server (required for VSCode extension)
pydebugai serve

# Show self-learning statistics
pydebugai stats
```

### 3. Install the VSCode Extension

```bash
# Install from .vsix (after packaging)
code --install-extension vscode-extension/pydebugai-0.1.0.vsix
```

Or in VSCode: `Extensions → Install from VSIX...`

Then start the server in your terminal:

```bash
pydebugai serve
```

The extension will:
- Show **red squiggles** on error lines
- Display **hover hints** with fix suggestions
- Offer **💡 Fix with PyDebugAI** in the quick-fix menu
- Open the **sidebar panel** with full AI analysis

---

## AI Algorithms

```
User Code
    │
    ├─► AST Analyzer (static, instant)
    │       └─ SyntaxError, IndentationError, undefined names,
    │          division by zero, comparison style warnings
    │
    ├─► Code Executor (subprocess, safe)
    │       └─ Captures stdout / stderr / exit code
    │
    ├─► Error Parser (regex traceback parser)
    │       └─ Extracts: exception type, message, file, line, col
    │
    ├─► Rule Engine (60+ rules, deterministic)
    │       └─ Pattern-match → instant fix suggestion
    │
    ├─► ML Classifier (TF-IDF + Random Forest)
    │       └─ Classifies error type → boosts rule confidence
    │
    ├─► Levenshtein Fixer (edit distance)
    │       └─ "Did you mean 'print'?" for NameError/AttributeError
    │
    ├─► CodeBERT (HuggingFace, optional)
    │       └─ Semantic embeddings → cosine similarity retrieval
    │
    └─► Orchestrator → Merge, Deduplicate, Rank by confidence
                └─► Top-10 suggestions → CLI / VSCode / API
```

### Self-Learning Loop (RLHF-lite)

```
User gives thumbs-up / thumbs-down on suggestion
    → Stored in SQLite (pydebugai/data/feedback.db)
    → Positive samples accumulate
    → Every 25 positive samples → auto-retrain ML classifier
    → Model improves over time per user
```

---

## CLI Examples

```bash
# Run and auto-debug a buggy file
pydebugai run tests/samples/buggy_sample.py

# Get output as JSON (pipe to other tools)
pydebugai run my_script.py --json

# Static analysis only (don't execute)
pydebugai run my_script.py --no-exec

# Deep analysis with CodeBERT (slower)
pydebugai run my_script.py --deep

# Interactive REPL
pydebugai chat
>>> x = 10 / 0
# (press Enter twice)
# → AI prints fix suggestions
```

---

## API (for VSCode extension & custom integrations)

Start server: `pydebugai serve` (default: `http://localhost:7432`)

```bash
# Analyze code
curl -X POST http://localhost:7432/analyze \
  -H "Content-Type: application/json" \
  -d '{"code": "print(udefined)"}'

# Record feedback
curl -X POST http://localhost:7432/feedback \
  -H "Content-Type: application/json" \
  -d '{"interaction_id": 1, "selected_idx": 0, "feedback": 1}'

# Health check
curl http://localhost:7432/status

# Stats
curl http://localhost:7432/stats
```

---

## Requirements

### Minimal (fast startup, no ML)
```
click, rich, fastapi, uvicorn, pydantic
```

### Full AI features
```
scikit-learn    # ML classifier
transformers    # CodeBERT
torch           # PyTorch backend
python-Levenshtein  # fast edit distance
```

Install all:
```bash
pip install -r requirements.txt
```

---

## Running Tests

```bash
cd c:\new-model-ai
python tests/test_error_parser.py
python tests/test_ast_analyzer.py
python tests/test_rule_engine.py
```

---

## VSCode Extension Settings

| Setting | Default | Description |
|---------|---------|-------------|
| `pydebugai.serverPort` | `7432` | Local server port |
| `pydebugai.analyzeOnSave` | `true` | Auto-analyze on save |
| `pydebugai.enableExecution` | `false` | Run code during analysis |
| `pydebugai.pythonPath` | `python` | Python interpreter path |

---

## License
MIT © PyDebugAI Team
