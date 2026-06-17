from typing import Dict

from pydantic import BaseModel, Field
from tools.market import MARKET_TOOLS
from .base_agent import BaseAgent
from utils.console import print_error, print_warning

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
    summary: str = Field(
        description=(
            "2–4 sentences covering every data point collected: industry, market size (TAM/SAM/SOM), "
            "growth rate, market stage, top customer segments, key trends, opportunities, risks, and market_score. "
            "End with one sentence on the market's investment attractiveness."
        )
    )


class MarketAgent(BaseAgent):
    def __init__(self):
        markdown_prompt = self.load_prompt("market_agent_prompt.md")

        super().__init__(
            system_prompt=markdown_prompt,
            response_model=MarketAnalysis,
            tools=MARKET_TOOLS,
        )

    def analyze(self, context: Dict) -> MarketAnalysis:
        """Analyze the market based on the provided description."""
        retrieve_context = context.get("startup_description",  "")
        if not retrieve_context:
            print_warning("MarketAgent: no startup description in context, skipping.")
            return None
        try:
            return self.run(retrieve_context)
        except Exception as e:
            print_error(f"MarketAgent failed: {e}")
            return None
