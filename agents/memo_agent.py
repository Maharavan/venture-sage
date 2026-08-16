from typing import Dict

from .base_agent import BaseAgent
from .investment_agent import InvestmentAnalysis
from pydantic import BaseModel
from utils.console import print_error, print_warning


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

    @property
    def summary(self) -> str:
        return self.executive_summary

class MemoAgent(BaseAgent):
    def __init__(self):
        markdown_prompt = self.load_prompt("memo_agent_prompt.md")

        super().__init__(
            system_prompt=markdown_prompt,
            agent_name="MemoAgent",
            startup_description="Generate a final investment memo synthesising all prior due diligence agent outputs.",
            response_model=MemoReport,
        )

    def analyze(self, context: Dict) -> MemoReport:
        """Generate an investment memo based on the provided analysis data."""
        investment_details = context.get("investment_agent")

        if not investment_details:
            print_warning("MemoAgent: investment_agent result missing from context, skipping.")
            return None
        if not isinstance(investment_details, InvestmentAnalysis):
            print_error(f"MemoAgent: expected InvestmentAnalysis, got {type(investment_details).__name__}.")
            return None
        try:
            return self.run(investment_details.model_dump_json())
        except Exception as e:
            print_error(f"MemoAgent failed: {e}")
            return None