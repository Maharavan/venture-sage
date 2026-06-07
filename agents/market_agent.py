from pydantic import BaseModel, Field
from tools.market import MARKET_TOOLS
from .base_agent import BaseAgent

class MarketAnalysis(BaseModel):
    industry: str
    market_size: str
    growth_rate: str
    market_stage: str

    customer_segments: list[str] = Field(
        default_factory=list
    )

    key_trends: list[str] = Field(
        default_factory=list
    )

    opportunities: list[str] = Field(
        default_factory=list
    )

    risks: list[str] = Field(
        default_factory=list
    )

    market_score: float = Field(description="Score from 0.0 to 10.0", le=10.0, ge=0.0)
    summary: str


class MarketAgent(BaseAgent):
    def __init__(self):
        markdown_prompt = self.load_prompt("market_agent_prompt.md")

        super().__init__(
            system_prompt=markdown_prompt,
            response_model=MarketAnalysis,
            tools=MARKET_TOOLS,
        )

    def analyze_market(self, market_description: str) -> MarketAnalysis:
        """Analyze the market based on the provided description."""
        response = self.run(market_description)
        return response