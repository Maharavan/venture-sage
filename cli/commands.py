"""Command implementations and utilities for the AWS Strand CLI."""

import asyncio
import json
from datetime import datetime
from pathlib import Path
from rich import box
from rich.console import Console
from rich.table import Table
from utils.console import console, print_error, print_info, print_success
from config.agent_registry import AGENT_REGISTRY, get_agent
from cli.registry import COMMANDS
from guardrails.input_guardrails import validate_startup_description

AGENT_LABEL = "[bold magenta]agent >[/bold magenta]"
_input_console = Console()

_last_base_agent: object | None = None
_last_context: dict | None = None


def _error(msg: str) -> None:
    console.print(AGENT_LABEL)
    print_error(msg)

def _info(msg: str) -> None:
    console.print(AGENT_LABEL)
    print_info(msg)

def _success(msg: str) -> None:
    console.print(AGENT_LABEL)
    print_success(msg)

def show_agents(args: str = "") -> None:
    """Display a table of enabled agents and their details."""
    table = Table(
        title="Available Agents",
        box=box.SIMPLE_HEAVY,
        border_style="bright_blue",
        title_justify="left",
    )
    table.add_column("Agent", style="bold cyan", no_wrap=True)
    table.add_column("Stage", justify="center", style="yellow")
    table.add_column("Domain", style="green")
    table.add_column("Description", style="dim")
    for name, info in AGENT_REGISTRY.items():
        if info["enabled"]:
            table.add_row(name, str(info["stage"]), info["domain"], info["description"])
    console.print(AGENT_LABEL)
    console.print(table)


def show_help(args: str = "") -> None:
    """Display the set of registered CLI commands and descriptions."""
    table = Table(
        title="Help — Available Commands",
        box=box.SIMPLE_HEAVY,
        border_style="bright_blue",
        title_justify="left",
    )
    table.add_column("Command", style="bold cyan", no_wrap=True)
    table.add_column("Description", style="dim")
    for name, desc in COMMANDS.items():
        table.add_row(name, desc)
    console.print(AGENT_LABEL)
    console.print(table)


def clear_current_session(args: str = "") -> None:
    """Clear the current console session output."""
    console.clear()


def _prompt_startup_description() -> str | None:
    """Prompt the user for a startup description and return it if provided."""
    try:
        desc = _input_console.input("[cyan]Startup description[/cyan]: ").strip()
    except (EOFError, KeyboardInterrupt):
        return None
    return desc or None


def run_agent_workflow(agent_name: str, args: str = "") -> None:
    """Execute the due diligence workflow for a named agent."""
    from workflow.due_diligence_workflow import due_dil_workflow
    global _last_agent
    description = args.strip() or _prompt_startup_description()
    if not description:
        _error("No startup description provided — aborting.")
        return

    guard = validate_startup_description(description)
    if not guard.passed:
        _error(f"Input rejected: {guard.reason}")
        return

    _info(f"Starting {agent_name} workflow…")
    try:
        global _last_context, _last_base_agent
        _last_context = asyncio.run(due_dil_workflow(agent_name, description))
        _last_base_agent = get_agent(agent_name=agent_name)
        _success("Workflow complete.")
    except Exception as e:
        _error(f"Workflow failed: {e}")

def chat_with_last_agent(message: str) -> None:
    """Send a free-form follow-up message to the most recently executed agent."""
    if _last_base_agent is None:
        _error("No agent has run yet — use a command first.")
        return
    _last_base_agent.chat(message)

def analyze_startup(args: str = "") -> None:
    """Run the memo_agent workflow for startup analysis."""
    run_agent_workflow("memo_agent", args)

def make_agent_command(agent_name: str):
    """Agent command created for execution"""
    def handler(args: str = ""):
        run_agent_workflow(agent_name, args)
    return handler

def export_memo_report(args: str = "") -> None:
    """Export the last memo_agent result as Markdown and JSON files."""
    if _last_context is None:
        _error("No workflow has run yet — use /memo first.")
        return

    memo = _last_context.get("memo_agent")
    if memo is None:
        _error("No memo report found — run /memo to generate one.")
        return

    fmt = args.strip().lower() or "md"
    if fmt not in ("md", "json"):
        _error("Unsupported format — use: /memo-export md  or  /memo-export json")
        return

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = Path("exports")
    out_dir.mkdir(exist_ok=True)

    if fmt == "json":
        path = out_dir / f"memo_{timestamp}.json"
        path.write_text(memo.model_dump_json(indent=2))
    else:
        path = out_dir / f"memo_{timestamp}.md"
        lines = [
            f"# Investment Memo\n",
            f"_Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}_\n",
            f"---\n",
            f"## Executive Summary\n{memo.executive_summary}\n",
            f"## Market Analysis\n{memo.market_analysis}\n",
            f"## Competition Analysis\n{memo.competition_analysis}\n",
            f"## Founder Analysis\n{memo.founder_analysis}\n",
            f"## Financial Analysis\n{memo.financial_analysis}\n",
            f"## Risk Analysis\n{memo.risk_analysis}\n",
            f"## Key Strengths\n" + "\n".join(f"- {s}" for s in memo.key_strengths) + "\n",
            f"## Key Concerns\n" + "\n".join(f"- {c}" for c in memo.key_concerns) + "\n",
            f"## Investment Thesis\n{memo.investment_thesis}\n",
            f"## Recommendation\n{memo.recommendation}\n",
            f"## Next Steps\n" + "\n".join(f"1. {s}" for s in memo.next_steps) + "\n",
            f"## Conclusion\n{memo.conclusion}\n",
        ]
        path.write_text("\n".join(lines))

    _success(f"Memo exported → {path}")
