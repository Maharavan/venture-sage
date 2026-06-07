from rich.console import Console
from utils.console import print_error, print_success
from cli.commands import (
    show_agents,
    show_help,
    clear_current_session,
    analyze_startup,
    make_agent_command,
    chat_with_last_agent
)

_AGENT_COMMANDS = {
    "/market":     "market_agent",
    "/competition":"competition_agent",
    "/founder":    "founder_agent",
    "/finance":    "finance_agent",
    "/risk":       "risk_agent",
    "/investment": "investment_agent",
    "/memo":       "memo_agent",
}

_HANDLERS = {
    "/agents":  show_agents,
    "/help":    show_help,
    "/clear":   clear_current_session,
    "/analyze": analyze_startup,
    **{cmd: make_agent_command(agent) for cmd, agent in _AGENT_COMMANDS.items()},
}

class ChatTerminal:
    """Interactive chat terminal for the CLI.

    Provides a simple loop that reads user input from a Rich Console
    and dispatches commands registered in _HANDLERS.
    """
    def __init__(self):
        """Create a ChatTerminal and initialize a Rich Console instance."""
        self._console = Console()

    def chat_ui(self) -> None:
        """Run the chat UI loop, reading input from self._console."""
        while True:
            try:
                user_input = self._console.input("\n[green]you >[/green] ").strip()
            except (EOFError, KeyboardInterrupt):
                print_success("Thanks for using Due Diligence AI. Goodbye!")
                return

            parts = user_input.split(None, 1)
            command = parts[0] if parts else ""
            args = parts[1] if len(parts) > 1 else ""

            if command == "/exit":
                print_success("Thanks for using Due Diligence AI. Goodbye!")
                return

            handler = _HANDLERS.get(command)
            if handler:
                handler(args)
            elif command.startswith('/'):
                print_error(f"Unknown command: {command!r}. Type /help for available commands.")
            else:
                chat_with_last_agent(user_input)