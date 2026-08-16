from enum import Enum
from typing import Dict, Literal

from .base_agent import BaseAgent
from pydantic import BaseModel, Field
from .risk_agent import RiskAnalysis
from .market_agent import MarketAnalysis
from .competitor_agent import CompetitionAnalysis
from .founder_agent import FounderAnalysis
from .financial_agent import FinanceAnalysis
from utils.console import print_error, print_warning


InvestmentRecommendation = Literal[
    "STRONG INVEST",
    "INVEST",
    "MONITOR",
    "PASS",
]

ScoreCategory = Literal[
    "Exceptional",
    "Strong",
    "Moderate",
    "Weak",
    "High Risk",
]

class InvestmentAnalysis(BaseModel):
    investment_strengths: list[str] = Field(default_factory=list)
    investment_weaknesses: list[str] = Field(default_factory=list)
    opportunities: list[str] = Field(default_factory=list)
    threats: list[str] = Field(default_factory=list)
    investment_score: float = Field(description="Score from 0.0 to 10.0", le=10.0, ge=0.0)
    score_category: ScoreCategory = Field(
        description="Exceptional, Strong, Moderate, Weak, High Risk"
    )
    score_rationale: str
    recommendation: InvestmentRecommendation
    investment_thesis: str
    executive_summary: str = Field(
        description=(
            "3–5 sentences synthesising all upstream agent findings: market opportunity and score, "
            "competitive position and score, founder quality and score, financial health and score, "
            "risk profile and score, top SWOT points, investment_score, score_category, and recommendation. "
            "End with a clear one-sentence investment verdict."
        )
    )

    @property
    def summary(self) -> str:
        return self.executive_summary

class InvestmentAgent(BaseAgent):
    def __init__(self):
        markdown_prompt = self.load_prompt("investment_agent_prompt.md")

        super().__init__(
            system_prompt=markdown_prompt,
            agent_name="InvestmentAgent",
            startup_description="Generate investment score, SWOT analysis and recommendation based on all prior agent outputs.",
            response_model=InvestmentAnalysis,
        )

    def analyze(self, context: Dict) -> InvestmentAnalysis:
        """Analyze the investment opportunity based on the provided description."""
        risk_details = context.get("risk_agent")
        if not isinstance(risk_details, RiskAnalysis):
            print_warning(f"InvestmentAgent: expected RiskAnalysis, got {type(risk_details).__name__}, skipping.")
            return None

        market_details = context.get("market_agent", "")
        competitor_details = context.get("competition_agent", "")
        founder_details = context.get("founder_agent", "")
        finance_details = context.get("finance_agent", "")

        if isinstance(market_details, MarketAnalysis):
            market_details = market_details.model_dump_json()
        if isinstance(competitor_details, CompetitionAnalysis):
            competitor_details = competitor_details.model_dump_json()
        if isinstance(founder_details, FounderAnalysis):
            founder_details = founder_details.model_dump_json()
        if isinstance(finance_details, FinanceAnalysis):
            finance_details = finance_details.model_dump_json()

        multi_query = f"""
        Market Agent: {market_details}
        Competitor Agent: {competitor_details}
        Founder Agent: {founder_details}
        Financial Agent: {finance_details}
        Risk Agent: {risk_details.model_dump_json()}
        """
        try:
            return self.run(multi_query)
        except Exception as e:
            print_error(f"InvestmentAgent failed: {e}")
            return None