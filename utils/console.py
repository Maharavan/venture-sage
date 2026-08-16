from rich import box
from rich.console import Console
from rich.markdown import Markdown
from rich.markup import escape
from rich.panel import Panel
import pyfiglet

console = Console()
AGENT_LABEL = "[bold magenta]agent >[/bold magenta]"

def _error(msg: str) -> None:
    console.print(AGENT_LABEL)
    print_error(msg)

def _info(msg: str) -> None:
    console.print(AGENT_LABEL)
    print_info(msg)

def _success(msg: str) -> None:
    console.print(AGENT_LABEL)
    print_success(msg)
def print_error(message: str) -> None:
    console.print(f"\n[bold red]Error:[/bold red] [red]{escape(message)}[/red]")


def print_success(message: str) -> None:
    console.print(f"\n[bold green]✔[/bold green] [green]{escape(message)}[/green]")


def print_warning(message: str) -> None:
    console.print(f"\n[bold yellow]Warning:[/bold yellow] [yellow]{escape(message)}[/yellow]")


def print_info(message: str) -> None:
    console.print(f"\n[bold cyan]Info:[/bold cyan] [cyan]{escape(message)}[/cyan]")


def print_agent_summary(agent_name: str, summary: str) -> None:
    console.print(Panel(
        Markdown(summary) if summary.lstrip().startswith("#") else escape(summary),
        title=f"[bold cyan]{agent_name}[/bold cyan]",
        subtitle="[dim]summary[/dim]",
        border_style="green",
        box=box.SIMPLE_HEAVY,
        padding=(1, 2),
    ))


def print_banner() -> None:
    ascii_art = pyfiglet.figlet_format("VENTURE SAGE", font="slant")
    banner_text = (
        "🤖 [bold cyan]AI-Powered Startup Due Diligence on AWS Bedrock[/bold cyan]\n"
        "[dim]Strands Agents SDK · Amazon Nova Pro · Multi-Agent Pipeline[/dim]"
    )
    panel = Panel(
        f"[bold magenta]{ascii_art}[/]\n{banner_text}",
        title="[bold yellow]📊 Due Diligence AI[/bold yellow]",
        subtitle="[italic dim]Powered by AWS Bedrock · Strands Agents SDK[/italic dim]",
        box=box.HEAVY,
        border_style="bright_blue",
        expand=True,
        highlight=True,
    )
    console.print(panel)
