from strands import Agent
from agents.base_agent import BaseAgent
from tools.risk import RISK_TOOLS
from pydantic import BaseModel, Field
from typing import List


class RiskAnalysis(BaseModel):
    technology_risks: List[str] = Field(default_factory=list)

    market_risks: List[str] = Field(default_factory=list)

    regulatory_risks: List[str] = Field(default_factory=list)

    operational_risks: List[str] = Field(default_factory=list)

    execution_risks: List[str] = Field(default_factory=list)
    risk_mitigations: List[str] = Field(default_factory=list)
    risk_score: float = Field(
        description="Risk score from 0.0 to 10.0"
    )
    score_category: str = Field(
        description="Low Risk, Moderate Risk, Elevated Risk, High Risk, Critical Risk"
    )
    score_rationale: str
    key_risks: List[str] = Field(
        default_factory=list,
        description="Top risks investors should monitor"
    )
    recommendation: str
    summary: str

class FinancialAgent(BaseAgent):
    def __init__(self):
        markdown_prompt = self.load_prompt("risk_agent_prompt.md")

        super().__init__(
            system_prompt=markdown_prompt,
            response_model=RiskAnalysis,
            tools=RISK_TOOLS,
        )

    def analyze_finance(self, risk_info: str) -> RiskAnalysis:
        """Analyze the founder based on the provided description."""
        response = self.run(risk_info)
        return response