/**
 * PyDebugAI VSCode Extension — Main entry point.
 * Provides: DiagnosticProvider, HoverProvider, CodeActionProvider, SidebarWebview
 */

const vscode = require('vscode');
const http = require('http');

const EXTENSION_ID = 'pydebugai';
const SERVER_DEFAULT_PORT = 7432;

// ─── Utility: call local PyDebugAI server ─────────────────────────────────────

function callServer(path, method = 'GET', body = null) {
    return new Promise((resolve, reject) => {
        const config = vscode.workspace.getConfiguration(EXTENSION_ID);
        const port = config.get('serverPort', SERVER_DEFAULT_PORT);

        const postData = body ? JSON.stringify(body) : '';
        const options = {
            hostname: '127.0.0.1',
            port,
            path,
            method,
            headers: {
                'Content-Type': 'application/json',
                'Content-Length': Buffer.byteLength(postData),
            },
        };

        const req = http.request(options, (res) => {
            let data = '';
            res.on('data', chunk => data += chunk);
            res.on('end', () => {
                try { resolve(JSON.parse(data)); }
                catch (e) { reject(new Error('Invalid JSON from server')); }
            });
        });

        req.on('error', reject);
        if (postData) req.write(postData);
        req.end();
    });
}

// ─── Server availability check ────────────────────────────────────────────────

let _serverAvailable = false;

async function checkServer() {
    try {
        const res = await callServer('/status');
        _serverAvailable = res.status === 'ok';
    } catch {
        _serverAvailable = false;
    }
    return _serverAvailable;
}

// ─── Diagnostic Collection ────────────────────────────────────────────────────

const diagnosticCollection = vscode.languages.createDiagnosticCollection('pydebugai');

async function analyzeDocument(document, sidebarProvider) {
    if (document.languageId !== 'python') return;

    if (!_serverAvailable) {
        const ok = await checkServer();
        if (!ok) {
            vscode.window.setStatusBarMessage('$(warning) PyDebugAI server not running. Run: pydebugai serve', 5000);
            return;
        }
    }

    try {
        const config = vscode.workspace.getConfiguration(EXTENSION_ID);
        const execute = config.get('enableExecution', false);

        const result = await callServer('/analyze', 'POST', {
            code: document.getText(),
            file_path: document.uri.fsPath,
            execute,
        });

        updateDiagnostics(document, result);

        // Update sidebar
        if (sidebarProvider) {
            sidebarProvider.updateAnalysis(result);
        }

        // Status bar feedback
        const errCount = result.diagnostics?.filter(d => d.severity === 'error').length || 0;
        const suggCount = result.suggestions?.length || 0;
        if (errCount > 0) {
            vscode.window.setStatusBarMessage(
                `$(error) PyDebugAI: ${errCount} error(s) — ${suggCount} fix suggestion(s)`, 8000
            );
        } else {
            vscode.window.setStatusBarMessage('$(check) PyDebugAI: No errors detected', 5000);
        }

    } catch (err) {
        _serverAvailable = false;
    }
}

function updateDiagnostics(document, result) {
    const diagnostics = [];

    if (!result.diagnostics) return;

    for (const d of result.diagnostics) {
        const line = Math.max(0, (d.line || 1) - 1);
        const col = Math.max(0, d.col || 0);
        const range = new vscode.Range(
            new vscode.Position(line, col),
            new vscode.Position(line, Math.max(col + 1, 999)) // highlight to end of line
        );

        const severity = d.severity === 'error'
            ? vscode.DiagnosticSeverity.Error
            : d.severity === 'warning'
                ? vscode.DiagnosticSeverity.Warning
                : vscode.DiagnosticSeverity.Information;

        const diag = new vscode.Diagnostic(range, `[PyDebugAI] ${d.message}`, severity);
        diag.source = 'PyDebugAI';
        diag.code = d.category;

        // Attach suggestions for the Code Actions provider
        diag.relatedInformation = (result.suggestions || []).slice(0, 3).map(s =>
            new vscode.DiagnosticRelatedInformation(
                new vscode.Location(document.uri, range),
                `💡 ${s.title} (${Math.round((s.confidence || 0) * 100)}% confidence)`
            )
        );

        diagnostics.push(diag);
    }

    diagnosticCollection.set(document.uri, diagnostics);
}

// ─── Hover Provider ───────────────────────────────────────────────────────────

class PyDebugHoverProvider {
    constructor() { this._lastResult = null; }

    setResult(result) { this._lastResult = result; }

    provideHover(document, position) {
        if (!this._lastResult) return null;

        const diagnostics = diagnosticCollection.get(document.uri) || [];
        const matchingDiag = diagnostics.find(d => d.range.contains(position));
        if (!matchingDiag) return null;

        const suggestions = this._lastResult.suggestions?.slice(0, 2) || [];
        if (!suggestions.length) return null;

        const markdownLines = [
            '**🤖 PyDebugAI Fix Suggestions**\n',
            `**Error:** \`${matchingDiag.message.replace('[PyDebugAI] ', '')}\`\n`,
        ];

        for (const [i, s] of suggestions.entries()) {
            markdownLines.push(`**${i + 1}. ${s.title}** (${Math.round((s.confidence || 0) * 100)}% confidence)`);
            markdownLines.push(`> ${s.explanation}\n`);
            if (s.fix_code) {
                markdownLines.push('```python');
                markdownLines.push(s.fix_code);
                markdownLines.push('```');
            }
        }

        markdownLines.push(`\n_Open the **PyDebugAI panel** for full analysis_`);
        const md = new vscode.MarkdownString(markdownLines.join('\n'));
        md.isTrusted = true;
        return new vscode.Hover(md);
    }
}

// ─── Code Action Provider ─────────────────────────────────────────────────────

class PyDebugCodeActionProvider {
    constructor() { this._lastResult = null; }

    setResult(result) { this._lastResult = result; }

    provideCodeActions(document, range) {
        if (!this._lastResult) return [];

        const diagnostics = diagnosticCollection.get(document.uri) || [];
        const relevant = diagnostics.filter(d => d.range.intersection(range));
        if (!relevant.length) return [];

        const actions = [];
        const suggestions = this._lastResult.suggestions?.slice(0, 3) || [];

        for (const s of suggestions) {
            const action = new vscode.CodeAction(
                `💡 PyDebugAI: ${s.title}`,
                vscode.CodeActionKind.QuickFix
            );
            action.isPreferred = suggestions.indexOf(s) === 0;
            action.command = {
                command: 'pydebugai.openSidebar',
                title: 'Open PyDebugAI',
                arguments: [s],
            };
            action.diagnostics = relevant;
            actions.push(action);
        }

        return actions;
    }
}

// ─── Sidebar WebView Provider ─────────────────────────────────────────────────

class PyDebugSidebarProvider {
    constructor(extensionUri) {
        this._extensionUri = extensionUri;
        this._view = null;
        this._lastResult = null;
    }

    resolveWebviewView(webviewView) {
        this._view = webviewView;
        webviewView.webview.options = { enableScripts: true };
        webviewView.webview.html = this._getHtml(webviewView.webview);

        // Handle messages from the webview
        webviewView.webview.onDidReceiveMessage(async (msg) => {
            if (msg.type === 'feedback') {
                try {
                    await callServer('/feedback', 'POST', msg.data);
                    vscode.window.showInformationMessage('PyDebugAI: Feedback recorded! Thank you 🙏');
                } catch {}
            }
            if (msg.type === 'openLine') {
                const editor = vscode.window.activeTextEditor;
                if (editor && msg.line > 0) {
                    const pos = new vscode.Position(msg.line - 1, 0);
                    editor.selection = new vscode.Selection(pos, pos);
                    editor.revealRange(new vscode.Range(pos, pos));
                }
            }
        });

        // Send last result if we have it
        if (this._lastResult) this._postResult(this._lastResult);
    }

    updateAnalysis(result) {
        this._lastResult = result;
        if (this._view) this._postResult(result);
    }

    _postResult(result) {
        this._view.webview.postMessage({ type: 'analysis', data: result });
    }

    _getHtml(webview) {
        return `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>PyDebugAI</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: var(--vscode-font-family, 'Segoe UI', sans-serif);
    font-size: 13px;
    background: var(--vscode-sideBar-background, #1e1e1e);
    color: var(--vscode-foreground, #ccc);
    padding: 0;
    height: 100vh;
    overflow-y: auto;
  }
  .header {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    padding: 16px 12px;
    border-bottom: 1px solid #333;
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .header-title { font-size: 15px; font-weight: 700; color: #00d4ff; }
  .header-sub { font-size: 11px; color: #888; margin-top: 2px; }
  .status-bar {
    padding: 6px 12px;
    font-size: 11px;
    color: #888;
    background: #111;
    border-bottom: 1px solid #222;
    display: flex;
    align-items: center;
    gap: 6px;
  }
  .badge { 
    background: #e74c3c; 
    color: white; 
    border-radius: 10px; 
    padding: 1px 6px; 
    font-size: 10px;
    font-weight: bold;
  }
  .badge.ok { background: #27ae60; }
  .badge.warn { background: #f39c12; }
  .section { padding: 10px 12px; }
  .section-title {
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    color: #888;
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    gap: 6px;
  }
  .diag-item {
    background: #1e1e1e;
    border: 1px solid #333;
    border-left: 3px solid #e74c3c;
    border-radius: 4px;
    padding: 8px 10px;
    margin-bottom: 6px;
    cursor: pointer;
    transition: background 0.15s;
  }
  .diag-item:hover { background: #252526; }
  .diag-item.warn { border-left-color: #f39c12; }
  .diag-item.info { border-left-color: #3498db; }
  .diag-type { font-size: 10px; color: #e74c3c; font-weight: bold; margin-bottom: 2px; }
  .diag-item.warn .diag-type { color: #f39c12; }
  .diag-msg { font-size: 12px; color: #ddd; line-height: 1.4; }
  .diag-line { font-size: 10px; color: #666; margin-top: 3px; }
  .suggestion-card {
    background: #1a1a2e;
    border: 1px solid #2d3561;
    border-radius: 6px;
    padding: 10px 12px;
    margin-bottom: 8px;
    position: relative;
    overflow: hidden;
  }
  .suggestion-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 3px; height: 100%;
    background: linear-gradient(180deg, #00d4ff, #9b59b6);
  }
  .sugg-title { font-size: 13px; font-weight: 600; color: #00d4ff; margin-bottom: 4px; }
  .sugg-explanation { font-size: 12px; color: #aaa; line-height: 1.5; margin-bottom: 8px; }
  .sugg-code {
    background: #0d0d0d;
    border: 1px solid #333;
    border-radius: 4px;
    padding: 8px;
    font-family: 'Consolas', monospace;
    font-size: 11px;
    color: #7ec8e3;
    white-space: pre-wrap;
    margin-bottom: 8px;
    max-height: 120px;
    overflow-y: auto;
  }
  .sugg-meta {
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 6px;
  }
  .confidence-bar {
    height: 4px;
    background: #333;
    border-radius: 2px;
    flex: 1;
    min-width: 60px;
  }
  .confidence-fill {
    height: 100%;
    border-radius: 2px;
    background: linear-gradient(90deg, #9b59b6, #00d4ff);
    transition: width 0.3s;
  }
  .confidence-label { font-size: 10px; color: #888; white-space: nowrap; }
  .engine-badge {
    font-size: 9px;
    padding: 2px 6px;
    border-radius: 8px;
    background: #252526;
    color: #888;
    border: 1px solid #444;
  }
  .feedback-row { display: flex; gap: 6px; }
  .feedback-btn {
    background: none;
    border: 1px solid #444;
    color: #888;
    padding: 3px 8px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 12px;
    transition: all 0.15s;
  }
  .feedback-btn:hover { background: #252526; color: #eee; border-color: #666; }
  .feedback-btn.up:hover { border-color: #27ae60; color: #27ae60; }
  .feedback-btn.down:hover { border-color: #e74c3c; color: #e74c3c; }
  .empty-state {
    text-align: center;
    padding: 40px 20px;
    color: #555;
  }
  .empty-icon { font-size: 40px; margin-bottom: 12px; }
  .empty-text { font-size: 13px; }
  .run-output {
    background: #0d0d0d;
    border: 1px solid #333;
    border-radius: 4px;
    padding: 10px;
    font-family: 'Consolas', monospace;
    font-size: 11px;
    color: #7ec8e3;
    white-space: pre-wrap;
    max-height: 150px;
    overflow-y: auto;
  }
  .run-output.stderr { color: #e74c3c; }
  .divider { border: none; border-top: 1px solid #2a2a2a; margin: 4px 0; }
</style>
</head>
<body>

<div class="header">
  <span style="font-size:20px">🐛</span>
  <div>
    <div class="header-title">PyDebugAI</div>
    <div class="header-sub">AI-powered Python debugging</div>
  </div>
</div>

<div class="status-bar" id="statusBar">
  <span>⚡ Ready — save a Python file to analyze</span>
</div>

<div id="mainContent">
  <div class="empty-state">
    <div class="empty-icon">🔍</div>
    <div class="empty-text">Open a Python file and save it<br>to start AI debugging</div>
  </div>
</div>

<script>
  const vscode = acquireVsCodeApi();

  window.addEventListener('message', event => {
    const msg = event.data;
    if (msg.type === 'analysis') {
      renderAnalysis(msg.data);
    }
  });

  function renderAnalysis(result) {
    const container = document.getElementById('mainContent');
    const statusBar = document.getElementById('statusBar');
    const diags = result.diagnostics || [];
    const suggestions = result.suggestions || [];
    const exec = result.execution || null;

    const errorCount = diags.filter(d => d.severity === 'error').length;
    const warnCount = diags.filter(d => d.severity === 'warning').length;

    // Status bar
    if (errorCount > 0) {
      statusBar.innerHTML = '<span>❌ ' + errorCount + ' error(s) — ' + suggestions.length + ' AI fix(es) available</span>';
    } else if (warnCount > 0) {
      statusBar.innerHTML = '<span>⚠️ ' + warnCount + ' warning(s)</span>';
    } else {
      statusBar.innerHTML = '<span><span class="badge ok">✓</span> No errors detected!</span>';
    }

    let html = '';

    // Execution output
    if (exec) {
      html += '<div class="section">';
      html += '<div class="section-title">▶ Execution</div>';
      if (exec.stdout) {
        html += '<div class="run-output">' + escHtml(exec.stdout.trim()) + '</div>';
      }
      if (exec.stderr) {
        html += '<div class="run-output stderr" style="margin-top:6px">' + escHtml(exec.stderr.trim()) + '</div>';
      }
      if (exec.timed_out) {
        html += '<div style="color:#e74c3c;font-size:11px;margin-top:4px">⏱ Timed out</div>';
      }
      html += '<div style="font-size:10px;color:#555;margin-top:4px">Exit: ' + exec.exit_code + ' | ' + exec.execution_time_ms + 'ms</div>';
      html += '</div><hr class="divider">';
    }

    // Diagnostics
    if (diags.length > 0) {
      html += '<div class="section">';
      html += '<div class="section-title">🔍 Diagnostics (' + diags.length + ')</div>';
      for (const d of diags) {
        const cls = d.severity === 'error' ? '' : d.severity === 'warning' ? ' warn' : ' info';
        html += '<div class="diag-item' + cls + '" onclick="goToLine(' + d.line + ')">';
        html += '<div class="diag-type">' + d.category + '</div>';
        html += '<div class="diag-msg">' + escHtml(d.message) + '</div>';
        if (d.snippet) html += '<div class="diag-line" style="font-family:monospace">' + escHtml(d.snippet) + '</div>';
        html += '<div class="diag-line">Line ' + d.line + '</div>';
        html += '</div>';
      }
      html += '</div><hr class="divider">';
    }

    // Suggestions
    if (suggestions.length > 0) {
      html += '<div class="section">';
      html += '<div class="section-title">💡 AI Fix Suggestions (' + suggestions.length + ')</div>';
      suggestions.forEach((s, i) => {
        const pct = Math.round((s.confidence || 0) * 100);
        html += '<div class="suggestion-card">';
        html += '<div class="sugg-title">' + escHtml(s.title) + '</div>';
        html += '<div class="sugg-explanation">' + escHtml(s.explanation) + '</div>';
        if (s.fix_code) {
          html += '<div class="sugg-code">' + escHtml(s.fix_code) + '</div>';
        }
        html += '<div class="sugg-meta">';
        html += '<div style="display:flex;align-items:center;gap:6px;flex:1">';
        html += '<div class="confidence-bar"><div class="confidence-fill" style="width:' + pct + '%"></div></div>';
        html += '<div class="confidence-label">' + pct + '%</div>';
        html += '</div>';
        html += '<span class="engine-badge">' + (s.source || 'rule') + '</span>';
        html += '</div>';
        html += '<div class="feedback-row" style="margin-top:8px">';
        html += '<button class="feedback-btn up" onclick="sendFeedback(' + i + ', 1)">👍 Helpful</button>';
        html += '<button class="feedback-btn down" onclick="sendFeedback(' + i + ', -1)">👎 Not helpful</button>';
        html += '</div>';
        if (s.line) {
          html += '<div class="diag-line" style="margin-top:4px;cursor:pointer" onclick="goToLine(' + s.line + ')">→ Jump to line ' + s.line + '</div>';
        }
        html += '</div>';
      });
      html += '</div>';
    }

    if (!diags.length && !suggestions.length && !exec) {
      html = '<div class="empty-state"><div class="empty-icon">✅</div><div class="empty-text">No issues found.<br>Your code looks clean!</div></div>';
    }

    container.innerHTML = html;
  }

  function sendFeedback(idx, feedback) {
    vscode.postMessage({ type: 'feedback', data: { interaction_id: 0, selected_idx: idx, feedback } });
  }

  function goToLine(line) {
    vscode.postMessage({ type: 'openLine', line });
  }

  function escHtml(str) {
    if (!str) return '';
    return str.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
  }
</script>
</body>
</html>`;
    }
}

// ─── Activate ─────────────────────────────────────────────────────────────────

function activate(context) {
    const hoverProvider = new PyDebugHoverProvider();
    const actionProvider = new PyDebugCodeActionProvider();
    const sidebarProvider = new PyDebugSidebarProvider(context.extensionUri);

    // Wrap analysis to also update hover/action providers
    async function analyze(document) {
        if (document.languageId !== 'python') return;
        if (!_serverAvailable) {
            const ok = await checkServer();
            if (!ok) return;
        }
        try {
            const config = vscode.workspace.getConfiguration(EXTENSION_ID);
            const execute = config.get('enableExecution', false);
            const result = await callServer('/analyze', 'POST', {
                code: document.getText(),
                file_path: document.uri.fsPath,
                execute,
            });
            updateDiagnostics(document, result);
            hoverProvider.setResult(result);
            actionProvider.setResult(result);
            sidebarProvider.updateAnalysis(result);

            const errCount = result.diagnostics?.filter(d => d.severity === 'error').length || 0;
            if (errCount > 0) {
                vscode.window.setStatusBarMessage(
                    `$(error) PyDebugAI: ${errCount} error(s) — ${result.suggestions?.length || 0} fix(es)`, 8000
                );
            } else {
                vscode.window.setStatusBarMessage('$(check) PyDebugAI: No errors', 4000);
            }
        } catch {
            _serverAvailable = false;
        }
    }

    // Register sidebar
    context.subscriptions.push(
        vscode.window.registerWebviewViewProvider('pydebugai.sidebarView', sidebarProvider)
    );

    // Register language providers
    context.subscriptions.push(
        vscode.languages.registerHoverProvider('python', hoverProvider),
        vscode.languages.registerCodeActionsProvider('python', actionProvider, {
            providedCodeActionKinds: [vscode.CodeActionKind.QuickFix],
        }),
    );

    // On save
    const config = vscode.workspace.getConfiguration(EXTENSION_ID);
    if (config.get('analyzeOnSave', true)) {
        context.subscriptions.push(
            vscode.workspace.onDidSaveTextDocument(doc => analyze(doc))
        );
    }

    // On open
    context.subscriptions.push(
        vscode.workspace.onDidOpenTextDocument(doc => {
            if (doc.languageId === 'python') analyze(doc);
        })
    );

    // Commands
    context.subscriptions.push(
        vscode.commands.registerCommand('pydebugai.analyzeFile', () => {
            const editor = vscode.window.activeTextEditor;
            if (editor) analyze(editor.document);
        }),

        vscode.commands.registerCommand('pydebugai.startServer', async () => {
            const config = vscode.workspace.getConfiguration(EXTENSION_ID);
            const python = config.get('pythonPath', 'python');
            const terminal = vscode.window.createTerminal('PyDebugAI Server');
            terminal.sendText(`${python} -m pydebugai serve`);
            terminal.show();
            vscode.window.showInformationMessage('PyDebugAI server starting...');
        }),

        vscode.commands.registerCommand('pydebugai.showStats', async () => {
            try {
                const ok = await checkServer();
                if (!ok) throw new Error('Server not running');
                const stats = await callServer('/stats');
                vscode.window.showInformationMessage(
                    `PyDebugAI Stats: ${stats.total_interactions} interactions | ` +
                    `Estimated accuracy: ${stats.estimated_accuracy}%`
                );
            } catch {
                vscode.window.showErrorMessage('PyDebugAI server not running. Use "PyDebugAI: Start AI Server".');
            }
        }),

        vscode.commands.registerCommand('pydebugai.openSidebar', (suggestion) => {
            vscode.commands.executeCommand('workbench.view.extension.pydebugai-sidebar');
        }),
    );

    // Check server on startup
    checkServer().then(ok => {
        if (!ok) {
            vscode.window.showWarningMessage(
                'PyDebugAI server is not running. Analysis will not work.',
                'Start Server'
            ).then(choice => {
                if (choice === 'Start Server') {
                    vscode.commands.executeCommand('pydebugai.startServer');
                }
            });
        }
    });

    // Analyze active file on startup
    if (vscode.window.activeTextEditor) {
        analyze(vscode.window.activeTextEditor.document);
    }
}

function deactivate() {
    diagnosticCollection.dispose();
}

module.exports = { activate, deactivate };
