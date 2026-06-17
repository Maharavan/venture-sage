from typing import Dict

from pydantic import BaseModel, Field
from tools.competitor import COMPETITOR_TOOLS
from .base_agent import BaseAgent
from utils.console import print_error, print_warning

class CompetitionAnalysis(BaseModel):
    competitors: list[str]
    market_leader: str
    competitive_advantages: list[str]
    competitive_disadvantages: list[str]
    barriers_to_entry: list[str]
    competition_intensity: str
    competition_score: float = Field(description="Score from 0.0 to 10.0", le=10.0, ge=0.0)
    summary: str = Field(
        description=(
            "2–4 sentences covering every data point collected: competitors identified, market leader, "
            "competitive advantages and disadvantages, barriers to entry, competition intensity, and competition_score. "
            "End with one sentence on the startup's competitive position."
        )
    )


class CompetitorAgent(BaseAgent):
    def __init__(self):
        markdown_prompt = self.load_prompt("competitor_agent_prompt.md")

        super().__init__(
            system_prompt=markdown_prompt,
            response_model=CompetitionAnalysis,
            tools=COMPETITOR_TOOLS,
        )

    def analyze(self, context: Dict) -> CompetitionAnalysis:
        """Analyze the market based on the provided description."""
        retrieve_context = context.get("startup_description",  "")
        if not retrieve_context:
            print_warning("CompetitorAgent: no startup description in context, skipping.")
            return None
        try:
            return self.run(retrieve_context)
        except Exception as e:
            print_error(f"CompetitorAgent failed: {e}")
            return None
