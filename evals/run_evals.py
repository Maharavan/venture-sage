"""CLI runner for all offline evals.

Usage:
    python -m evals.run_evals
    python -m evals.run_evals --suite guardrail
    python -m evals.run_evals --suite structural
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass, field

from rich import box
from rich.console import Console
from rich.table import Table

from evals.structural_evals import run_structural_evals
from evals.guardrail_evals import run_guardrail_evals

console = Console()


@dataclass
class SuiteReport:
    name: str
    total: int = 0
    passed: int = 0
    failed: int = 0
    warned: int = 0
    failures: list[tuple[str, str]] = field(default_factory=list)
    warnings: list[tuple[str, list[str]]] = field(default_factory=list)


def _run_suite(suite_name: str, results) -> SuiteReport:
    report = SuiteReport(name=suite_name)
    for r in results:
        report.total += 1
        if r.passed:
            report.passed += 1
            if r.warnings:
                report.warned += 1
                report.warnings.append((r.name, r.warnings))
        else:
            report.failed += 1
            report.failures.append((r.name, r.detail))
    return report


def _print_suite(report: SuiteReport) -> None:
    table = Table(
        title=f"[bold]{report.name}[/bold]",
        box=box.SIMPLE_HEAVY,
        border_style="bright_blue",
        title_justify="left",
    )
    table.add_column("Eval", style="cyan", no_wrap=True)
    table.add_column("Result", justify="center")
    table.add_column("Detail", style="dim")

    for name, detail in report.failures:
        table.add_row(name, "[bold red]FAIL[/bold red]", detail[:120])

    for name, warns in report.warnings:
        table.add_row(name, "[bold yellow]WARN[/bold yellow]", warns[0][:120])

    passed_clean = report.passed - report.warned
    if passed_clean > 0:
        table.add_row(
            f"({passed_clean} more passed cleanly)",
            "[bold green]PASS[/bold green]",
            "",
        )

    console.print(table)
    console.print(
        f"  [bold]{report.name}[/bold]: "
        f"[green]{report.passed}/{report.total} passed[/green]"
        + (f"  [red]{report.failed} failed[/red]" if report.failed else "")
        + (f"  [yellow]{report.warned} with warnings[/yellow]" if report.warned else "")
    )
    console.print()


def main(suite: str = "all") -> int:
    reports: list[SuiteReport] = []

    if suite in ("all", "guardrail"):
        console.print("[bold cyan]Running guardrail evals…[/bold cyan]")
        reports.append(_run_suite("Guardrail Evals", run_guardrail_evals()))

    if suite in ("all", "structural"):
        console.print("[bold cyan]Running structural evals…[/bold cyan]")
        reports.append(_run_suite("Structural Evals", run_structural_evals()))

    console.rule("[bold]Eval Summary[/bold]")
    for r in reports:
        _print_suite(r)

    total_failed = sum(r.failed for r in reports)
    total_passed = sum(r.passed for r in reports)
    total = sum(r.total for r in reports)

    if total_failed:
        console.print(f"[bold red]{total_failed}/{total} evals FAILED.[/bold red]")
        return 1

    console.print(f"[bold green]All {total_passed}/{total} evals passed.[/bold green]")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run due diligence pipeline evals")
    parser.add_argument(
        "--suite",
        choices=["all", "guardrail", "structural"],
        default="all",
        help="Which eval suite to run (default: all)",
    )
    args = parser.parse_args()
    sys.exit(main(suite=args.suite))
