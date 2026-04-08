"""PromptPressure CLI – entry point for all commands."""

from __future__ import annotations

import json
import sys
from enum import Enum
from pathlib import Path
from typing import Annotated, Optional

import typer
from rich.console import Console
from rich.table import Table

from promptpressure import __version__
from promptpressure.core.runner import run_scan
from promptpressure.core.schema import severity_meets_threshold
from promptpressure.suites.registry import MODES

app = typer.Typer(
    name="promptpressure",
    help="Pressure-test your AI before attackers do.",
    no_args_is_help=True,
)
console = Console()
err_console = Console(stderr=True)


class FailOnLevel(str, Enum):
    none = "none"
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"promptpressure {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: Annotated[
        Optional[bool],
        typer.Option(
            "--version",
            callback=_version_callback,
            is_eager=True,
            help="Show version and exit.",
        ),
    ] = None,
) -> None:
    pass


# ---------------------------------------------------------------------------
# scan command
# ---------------------------------------------------------------------------

@app.command()
def scan(
    url: Annotated[str, typer.Option("--url", help="Target base URL (OpenAI-compatible endpoint).")],
    mode: Annotated[str, typer.Option("--mode", help="Scan mode (quick_check, full, pi_suite, …).")] = "quick_check",
    output_json: Annotated[
        Optional[Path],
        typer.Option("--output-json", help="Write JSON results to this file."),
    ] = None,
    fail_on: Annotated[
        FailOnLevel,
        typer.Option("--fail-on", help="Exit non-zero if any finding meets/exceeds this severity."),
    ] = FailOnLevel.high,
    auth_header: Annotated[
        Optional[str],
        typer.Option("--auth-header", help='Authorization header, e.g. "Authorization: Bearer sk-..."'),
    ] = None,
    header: Annotated[
        Optional[list[str]],
        typer.Option("--header", help="Extra header in 'Key: Value' form (repeatable)."),
    ] = None,
    timeout: Annotated[int, typer.Option("--timeout", help="Per-request timeout in seconds.")] = 30,
) -> None:
    """Run a security scan against an OpenAI-compatible AI endpoint."""

    if mode not in MODES:
        err_console.print(
            f"[red]Unknown mode '{mode}'. Run [bold]promptpressure list-suites[/bold] to see options.[/red]"
        )
        raise typer.Exit(2)

    # Build headers dict
    extra_headers: dict[str, str] = {}
    if auth_header:
        key, _, value = auth_header.partition(":")
        extra_headers[key.strip()] = value.strip()
    if header:
        for h in header:
            key, _, value = h.partition(":")
            extra_headers[key.strip()] = value.strip()

    scenarios = MODES[mode]["scenarios"]
    total = len(scenarios)

    console.print(f"\n[bold]PromptPressure[/bold] v{__version__}  |  mode=[cyan]{mode}[/cyan]  |  target=[dim]{url}[/dim]")
    console.print(f"Running [bold]{total}[/bold] scenarios …\n")

    completed = 0

    def on_start(sid: str, name: str) -> None:
        nonlocal completed
        completed += 1
        console.print(f"  [{completed:>2}/{total}] [dim]{sid}[/dim] {name}")

    result = run_scan(
        url=url,
        mode=mode,
        headers=extra_headers if extra_headers else None,
        scanner_version=__version__,
        timeout=timeout,
        on_scenario_start=on_start,
    )

    # Print summary
    _print_summary(result)

    # Write JSON
    if output_json:
        output_json.write_text(json.dumps(result.to_dict(), indent=2))
        console.print(f"\n[green]Results written to[/green] {output_json}")

    # Exit code
    worst = _worst_severity(result)
    if worst and severity_meets_threshold(worst, fail_on.value):
        raise typer.Exit(1)


def _worst_severity(result) -> str | None:  # type: ignore[no-untyped-def]
    order = ["low", "medium", "high", "critical"]
    found = {f.severity for f in result.findings}
    for sev in reversed(order):
        if sev in found:
            return sev
    return None


def _print_summary(result) -> None:  # type: ignore[no-untyped-def]
    badge_color = {
        "secure": "green",
        "needs_attention": "yellow",
        "vulnerable": "red",
        "critical_risk": "bold red",
    }.get(result.badge, "white")

    console.print()
    console.rule("[bold]Scan Summary[/bold]")
    console.print(f"  Score : [bold]{result.score}/100[/bold]")
    console.print(f"  Badge : [{badge_color}]{result.badge.upper()}[/{badge_color}]")
    console.print(f"  Findings: {len(result.findings)}")

    if result.findings:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("ID", style="dim", width=8)
        table.add_column("Severity", width=10)
        table.add_column("Title")

        sev_colors = {
            "critical": "bold red",
            "high": "red",
            "medium": "yellow",
            "low": "cyan",
        }
        for f in result.findings:
            color = sev_colors.get(f.severity, "white")
            table.add_row(f.scenario_id, f"[{color}]{f.severity.upper()}[/{color}]", f.title)

        console.print()
        console.print(table)


# ---------------------------------------------------------------------------
# list-suites command
# ---------------------------------------------------------------------------

@app.command(name="list-suites")
def list_suites() -> None:
    """List available scan suites and modes with scenario counts."""
    table = Table(show_header=True, header_style="bold blue")
    table.add_column("Mode", style="bold", width=16)
    table.add_column("Scenarios", justify="right", width=10)
    table.add_column("Description")

    for name, info in MODES.items():
        count = len(info["scenarios"])
        table.add_row(name, str(count), info["description"])

    console.print("\n[bold]PromptPressure – Available Suites & Modes[/bold]\n")
    console.print(table)
    console.print()


# ---------------------------------------------------------------------------
# mock-agent command
# ---------------------------------------------------------------------------

@app.command(name="mock-agent")
def mock_agent(
    port: Annotated[int, typer.Option("--port", help="Port to listen on.")] = 8010,
    mode: Annotated[
        str,
        typer.Option(
            "--mode",
            help="Vulnerability mode: leaky_system_prompt | refusal_overdisclosure | tool_abuse_sim",
        ),
    ] = "leaky_system_prompt",
) -> None:
    """Start a local mock AI agent with intentional vulnerabilities for testing."""
    from promptpressure.mock_agent.server import SUPPORTED_MODES, serve_forever

    if mode not in SUPPORTED_MODES:
        err_console.print(
            f"[red]Unknown mock mode '{mode}'. Supported: {', '.join(SUPPORTED_MODES)}[/red]"
        )
        raise typer.Exit(2)

    console.print(
        f"\n[bold]PromptPressure Mock Agent[/bold]  mode=[cyan]{mode}[/cyan]  port=[cyan]{port}[/cyan]"
    )
    console.print(f"  Endpoint: [link]http://localhost:{port}/v1/chat/completions[/link]")
    console.print("  Run scanner: [bold]promptpressure scan --url http://localhost:{port}[/bold]\n")
    serve_forever(port, mode)


if __name__ == "__main__":
    app()
