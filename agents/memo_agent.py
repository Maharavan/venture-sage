from typing import Dict

from .base_agent import BaseAgent
from .investment_agent import InvestmentAnalysis
from pydantic import BaseModel


class MemoReport(BaseModel):
    executive_summary: str
    market_analysis: str
    competition_analysis: str
    founder_analysis: str
    financial_analysis: str
    risk_analysis: str
    key_strengths: list[str]
    key_concerns: list[str]
    investment_thesis: str
    recommendation: str
    next_steps: list[str]
    conclusion: str

class MemoAgent(BaseAgent):
    def __init__(self):
        markdown_prompt = self.load_prompt("memo_agent_prompt.md")

        super().__init__(
            system_prompt=markdown_prompt,
            response_model=MemoReport,
        )

    def analyze(self, context: Dict) -> MemoReport:
        """Generate an investment memo based on the provided analysis data."""
        risk_details = context.get("investment_agent","")

        if risk_details and isinstance(risk_details,InvestmentAnalysis):
            risk_details = risk_details.model_dump_json()
            return self.run(risk_details)
        return None