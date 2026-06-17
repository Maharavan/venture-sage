"""Command implementations and utilities for the AWS Strand CLI."""

import asyncio
from rich import box
from rich.console import Console
from rich.table import Table
from utils.console import console, print_error, print_info, print_success
from config.agent_registry import AGENT_REGISTRY, get_agent
from cli.registry import COMMANDS
from guardrails.input_guardrails import validate_startup_description

AGENT_LABEL = "[bold magenta]agent >[/bold magenta]"
_input_console = Console()

_last_agent: object | None = None

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
        print_error("No startup description provided — aborting.")
        return

    guard = validate_startup_description(description)
    if not guard.passed:
        print_error(f"Input rejected: {guard.reason}")
        return

    print_info(f"Starting [bold]{agent_name}[/bold] workflow…")
    try:
        asyncio.run(due_dil_workflow(agent_name, description))
        _last_agent = get_agent(agent_name=agent_name).agent
        print_success("Workflow complete.")
    except Exception as e:
        print_error(f"Workflow failed: {e}")

def chat_with_last_agent(message: str) -> None:
    """Send a message to the most recently executed agent."""
    if _last_agent is None:
        print_error("No agent has run yet — use a command first.")
        return
    _last_agent(message, structured_output_model=None)

def analyze_startup(args: str = "") -> None:
    """Run the memo_agent workflow for startup analysis."""
    run_agent_workflow("memo_agent", args)

def make_agent_command(agent_name: str):
    """Agent command created for execution"""
    def handler(args: str = ""):
        run_agent_workflow(agent_name, args)
    return handler