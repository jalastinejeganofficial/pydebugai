"""
CLI Interface — `pydebugai` command.
Commands: run, analyze, chat, serve, stats
Rich terminal output with syntax highlighting.
"""
from __future__ import annotations
import sys
import json as _json
import time
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.syntax import Syntax
from rich.text import Text
from rich import box
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()

BANNER = """[bold cyan]
╔═══════════════════════════════════════════════════════════╗
║  ██████╗ ██╗   ██╗██████╗ ███████╗██████╗ ██╗   ██╗ ██╗  ║
║  ██╔══██╗╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗██║   ██║ ██║  ║
║  ██████╔╝ ╚████╔╝ ██║  ██║█████╗  ██████╔╝██║   ██║ ██║  ║
║  ██╔═══╝   ╚██╔╝  ██║  ██║██╔══╝  ██╔══██╗██║   ██║ ██║  ║
║  ██║        ██║   ██████╔╝███████╗██████╔╝╚██████╔╝ ██║  ║
║  ╚═╝        ╚═╝   ╚═════╝ ╚══════╝╚═════╝  ╚═════╝  ╚═╝  ║
║         AI-Powered Python Debugging Assistant v0.1.0       ║
╚═══════════════════════════════════════════════════════════╝
[/bold cyan]"""


def _get_orchestrator(enable_transformer: bool = False):
    from .engine.orchestrator import Orchestrator
    return Orchestrator(enable_transformer=enable_transformer)


def _print_result(result, show_code: bool = True):
    """Pretty-print an AnalysisResult to the terminal."""
    from .models import Severity, ErrorCategory

    # ── Execution output ──────────────────────────────────────────────────────
    if result.execution_result:
        er = result.execution_result
        if er.stdout:
            console.print(Panel(
                er.stdout.strip(), title="[green]✅ Program Output[/green]",
                border_style="green", expand=False,
            ))
        if er.timed_out:
            console.print(Panel(
                "[bold red]⏱ Execution timed out.[/bold red]",
                border_style="red",
            ))
        console.print(
            f"[dim]Exit code: {er.exit_code} | "
            f"Time: {er.execution_time_ms:.1f}ms[/dim]"
        )

    # ── Diagnostics ────────────────────────────────────────────────────────────
    if result.diagnostics:
        table = Table(title="🔍 Diagnostics", box=box.ROUNDED,
                      show_lines=True, border_style="red")
        table.add_column("Line", style="cyan", width=6)
        table.add_column("Type", style="yellow", width=18)
        table.add_column("Severity", width=10)
        table.add_column("Message", style="white")

        for d in result.diagnostics:
            sev_color = "red" if d.severity == Severity.ERROR else "yellow"
            table.add_row(
                str(d.line),
                d.category.value,
                f"[{sev_color}]{d.severity.value.upper()}[/{sev_color}]",
                d.message,
            )
        console.print()
        console.print(table)

    # ── Suggestions ────────────────────────────────────────────────────────────
    if result.suggestions:
        console.print()
        console.print("[bold magenta]💡 AI Fix Suggestions[/bold magenta]")
        console.print()
        for i, s in enumerate(result.top_suggestions(5), 1):
            confidence_bar = "█" * int(s.confidence * 10) + "░" * (10 - int(s.confidence * 10))
            confidence_pct = f"{s.confidence:.0%}"
            console.print(Panel(
                f"[bold white]{s.title}[/bold white]\n\n"
                f"[white]{s.explanation}[/white]\n\n"
                + (f"[bold green]Fix Code:[/bold green]\n"
                   f"[dim]{s.fix_code}[/dim]\n\n" if s.fix_code else "")
                + (f"[bold blue]References:[/bold blue] "
                   + ", ".join(s.references) if s.references else "")
                + f"\n[dim]Line: {s.line or '?'} | "
                  f"Engine: {s.source} | "
                  f"Confidence: {confidence_bar} {confidence_pct}[/dim]",
                title=f"[cyan]#{i} — {s.category.value}[/cyan]",
                border_style="magenta",
                expand=False,
            ))
    elif not result.has_errors():
        console.print(Panel(
            "[bold green]✅ No errors detected! Your code looks good.[/bold green]",
            border_style="green",
        ))


@click.group()
def main():
    """PyDebugAI — AI-powered Python debugging assistant."""
    pass


@main.command()
@click.argument("file", type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.option("--no-exec", is_flag=True, default=False,
              help="Static analysis only (don't execute the file)")
@click.option("--deep", is_flag=True, default=False,
              help="Enable CodeBERT deep analysis (slower, requires transformers)")
@click.option("--json", "output_json", is_flag=True, default=False,
              help="Output results as JSON")
def run(file: Path, no_exec: bool, deep: bool, output_json: bool):
    """Run and analyze a Python file for errors."""
    console.print(BANNER)

    with Progress(
        SpinnerColumn(), TextColumn("[progress.description]{task.description}"),
        transient=True, console=console,
    ) as progress:
        t = progress.add_task(f"Analyzing [cyan]{file.name}[/cyan]...", total=None)
        orc = _get_orchestrator(enable_transformer=deep)
        result = orc.analyze_file(str(file), execute=not no_exec)
        progress.remove_task(t)

    if output_json:
        click.echo(_json.dumps(result.to_dict(), indent=2))
    else:
        _print_result(result)


@main.command()
@click.option("--deep", is_flag=True, default=False,
              help="Enable CodeBERT analysis")
def chat(deep: bool):
    """Interactive debug chat — paste code or error messages."""
    console.print(BANNER)
    console.print("[bold cyan]Interactive Debug Mode[/bold cyan]")
    console.print("Type [bold]Python code[/bold] or [bold]error messages[/bold], "
                  "then press [bold]Enter twice[/bold] to analyze.")
    console.print("Commands: [dim]/quit[/dim] [dim]/stats[/dim]\n")

    orc = _get_orchestrator(enable_transformer=deep)

    while True:
        try:
            lines = []
            console.print("[bold white]>>> [/bold white]", end="")
            while True:
                line = input()
                if not line and lines:
                    break
                if line.strip() == "/quit":
                    console.print("[yellow]Goodbye! 👋[/yellow]")
                    sys.exit(0)
                if line.strip() == "/stats":
                    stats = orc.get_stats()
                    console.print_json(_json.dumps(stats))
                    lines = []
                    break
                lines.append(line)

            if not lines:
                continue

            code_or_error = "\n".join(lines)
            with Progress(SpinnerColumn(), TextColumn("Analyzing..."),
                          transient=True, console=console) as p:
                p.add_task("", total=None)
                from .executor import execute_snippet
                exec_result = execute_snippet(code_or_error)

            if exec_result.stderr:
                result = orc.analyze_code(
                    code_or_error, file_path="<chat>", execute=False
                )
                result.execution_result = exec_result
                # Re-run pipeline with the traceback
                result2 = orc.analyze_code(code_or_error, file_path="<chat>", execute=False)
                result2.execution_result = exec_result
                _print_result(result2)
            else:
                console.print(Panel(
                    exec_result.stdout or "[dim](no output)[/dim]",
                    title="[green]Output[/green]", border_style="green",
                ))

        except (KeyboardInterrupt, EOFError):
            console.print("\n[yellow]Goodbye! 👋[/yellow]")
            break


@main.command()
@click.option("--host", default="127.0.0.1", help="Host to bind")
@click.option("--port", default=7432, help="Port to listen on")
def serve(host: str, port: int):
    """Start the local API server (used by VSCode extension)."""
    console.print(BANNER)
    console.print(f"[bold green]Starting PyDebugAI server on http://{host}:{port}[/bold green]")
    import uvicorn
    from .server import app
    uvicorn.run(app, host=host, port=port, log_level="warning")


@main.command()
def stats():
    """Show self-learning statistics."""
    orc = _get_orchestrator()
    s = orc.get_stats()
    table = Table(title="📊 PyDebugAI Statistics", box=box.ROUNDED, border_style="cyan")
    table.add_column("Metric", style="bold white")
    table.add_column("Value", style="cyan")
    for k, v in s.items():
        table.add_row(k.replace("_", " ").title(), str(v))
    console.print()
    console.print(table)


if __name__ == "__main__":
    main()
