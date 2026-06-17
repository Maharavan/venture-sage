from typing import Dict, Literal

from pydantic import BaseModel, Field
from tools.finance import FINANCIAL_TOOLS
from .base_agent import BaseAgent
from utils.console import print_error, print_warning


class FundingRound(BaseModel):
    round_name: str
    amount_raised: str | None = None
    date: str | None = None
    lead_investors: list[str] = Field(default_factory=list)
    participating_investors: list[str] = Field(default_factory=list)


class FinanceAnalysis(BaseModel):
    funding_rounds: list[FundingRound] = Field(default_factory=list)
    total_funding: str | None = None
    valuation: str | None = None
    revenue_signals: list[str] = Field(default_factory=list)
    burn_rate_signals: list[str] = Field(default_factory=list)
    financial_strengths: list[str] = Field(default_factory=list)
    financial_risks: list[str] = Field(default_factory=list)
    finance_score: float = Field(description="Score from 0.0 to 10.0", le=10.0, ge=0.0)
    score_category: Literal["Exceptional", "Strong", "Moderate", "Weak", "High Risk"]
    score_rationale: str
    investment_recommendation: Literal["Strong Invest", "Invest", "Monitor", "Pass"]
    funding_summary: str

    @property
    def summary(self) -> str:
        return self.funding_summary

class FinancialAgent(BaseAgent):
    def __init__(self):
        markdown_prompt = self.load_prompt("financial_agent_prompt.md")

        super().__init__(
            system_prompt=markdown_prompt,
            response_model=FinanceAnalysis,
            tools=FINANCIAL_TOOLS,
        )

    def analyze(self, context: Dict) -> FinanceAnalysis:
        """Analyze the financial data based on the provided funding info."""
        retrieve_context = context.get("startup_description",  "")
        if not retrieve_context:
            print_warning("FinancialAgent: no startup description in context, skipping.")
            return None
        try:
            return self.run(retrieve_context)
        except Exception as e:
            print_error(f"FinancialAgent failed: {e}")
            return None
