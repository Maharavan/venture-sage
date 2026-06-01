from abc import ABC
from pathlib import Path
from typing import Any

from pydantic import BaseModel
from strands import Agent

from config.settings import settings

class BaseAgent(ABC):
    def __init__(
        self,
        system_prompt: str,
        response_model: type[BaseModel],
        tools: list[Any] | None = None,
    ):
        self.system_prompt = system_prompt
        self.response_model = response_model
        self.model = settings.get_model()
        self.tools = tools or []
        self.agent = Agent(
            system_prompt=self.system_prompt,
            model=self.model,
            structured_output_model=self.response_model,
            tools=self.tools,
        )

    def run(self, query: str) -> BaseModel:
        """Execute the agent and return structured output."""
        response = self.agent(query)
        return response.structured_output

    @classmethod
    def load_prompt(cls, prompt_name: str) -> str:
        prompt_path = Path(__file__).parent.parent / "prompts" / prompt_name
        return prompt_path.read_text(encoding="utf-8")
