from pydantic import BaseModel, Field
from tools.finance import FINANCIAL_TOOLS
from .base_agent import BaseAgent
from typing import List, Optional


class FundingRound(BaseModel):
    round_name: str
    amount_raised: Optional[str] = None
    date: Optional[str] = None
    lead_investors: List[str] = Field(default_factory=list)
    participating_investors: List[str] = Field(default_factory=list)


class FinanceAnalysis(BaseModel):
    funding_rounds: List[FundingRound] = Field(default_factory=list)
    total_funding: Optional[str] = None
    valuation: Optional[str] = None
    revenue_signals: List[str] = Field(default_factory=list)
    burn_rate_signals: List[str] = Field(default_factory=list)
    financial_strengths: List[str] = Field(default_factory=list)
    financial_risks: List[str] = Field(default_factory=list)
    finance_score: float = Field(
        description="Score from 0.0 to 10.0"
    )
    score_category: str = Field(
        description="Exceptional, Strong, Moderate, Weak, High Risk"
    )
    score_rationale: str
    investment_recommendation: str
    funding_summary: str

class FinancialAgent(BaseAgent):
    def __init__(self):
        markdown_prompt = self.load_prompt("financial_agent_prompt.md")

        super().__init__(
            system_prompt=markdown_prompt,
            response_model=FinanceAnalysis,
            tools=FINANCIAL_TOOLS,
        )

    def analyze_finance(self, funding_info: str) -> FinanceAnalysis:
        """Analyze the founder based on the provided description."""
        response = self.run(funding_info)
        return response