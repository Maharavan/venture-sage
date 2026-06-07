from pydantic import BaseModel, Field
from tools.competitor import COMPETITOR_TOOLS
from .base_agent import BaseAgent

class CompetitionAnalysis(BaseModel):
    competitors: list[str]
    market_leader: str
    competitive_advantages: list[str]
    competitive_disadvantages: list[str]
    barriers_to_entry: list[str]
    competition_intensity: str
    competition_score: float = Field(description="Score from 0.0 to 10.0", le=10.0, ge=0.0)
    summary: str


class CompetitorAgent(BaseAgent):
    def __init__(self):
        markdown_prompt = self.load_prompt("competitor_agent_prompt.md")

        super().__init__(
            system_prompt=markdown_prompt,
            response_model=CompetitionAnalysis,
            tools=COMPETITOR_TOOLS,
        )

    def analyze_market(self, market_description: str) -> CompetitionAnalysis:
        """Analyze the market based on the provided description."""
        response = self.run(market_description)
        return response