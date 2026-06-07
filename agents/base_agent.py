"""BaseAgent

Provides a singleton abstract base class wrapper around a Strands Agent
configured with streaming output and a summarizing conversation manager.
"""

import logging
from abc import ABC
from pathlib import Path
from typing import Any

from pydantic import BaseModel
from strands import Agent
from strands.agent.conversation_manager import SummarizingConversationManager
from config.settings import settings
from rich.console import Console

# Suppress all SDK/transport logging before any agent is constructed.
for _log in ["strands", "botocore", "boto3", "httpx", "urllib3",
             "strands.agent", "strands.tools", "strands.event_loop",
             "strands.models", "strands.experimental.bidi"]:
    logging.getLogger(_log).setLevel(logging.CRITICAL)

_stream_console = Console(highlight=False)

def _stream_callback(**kwargs):
    if "data" in kwargs and kwargs["data"]:
        _stream_console.print(kwargs["data"], end="", markup=False, highlight=False)

class BaseAgent(ABC):
    _instance = None
    def __new__(cls,*args,**kwargs):
        """Ensure a single shared instance (singleton).

        Subsequent constructions return the same instance. This simplifies
        usage in scripts that import and instantiate the agent multiple
        times during a process lifetime.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    def __init__(
        self,
        system_prompt: str,
        response_model: type[BaseModel],
        tools: list[Any] | None = None,
    ):
        """Construct the agent.

        Args:
            system_prompt: System prompt text used to initialize the agent.
            response_model: Pydantic model type for structured outputs.
            tools: Optional list of tool objects to register with the agent.
        """
        self.system_prompt = system_prompt
        self.response_model = response_model
        self.model = settings.get_model()
        self.tools = tools or []
        self.agent = Agent(
            system_prompt=self.system_prompt,
            model=self.model,
            structured_output_model=self.response_model,
            tools=self.tools,
            callback_handler=_stream_callback,
            conversation_manager=SummarizingConversationManager(
                summary_ratio=0.3,
                preserve_recent_messages=10
            )
        )

    def run(self, query: str) -> BaseModel:
        """Run the agent on a query and return the structured output model."""
        response = self.agent(query)
        _stream_console.print()
        return response.structured_output

    @classmethod
    def load_prompt(cls, prompt_name: str) -> str:
        """Load a prompt file by name from the repository prompts directory.

        Returns the file contents as a UTF-8 string.
        """
        prompt_path = Path(__file__).parent.parent / "prompts" / prompt_name
        return prompt_path.read_text(encoding="utf-8")
