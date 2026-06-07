from .base_agent import BaseAgent
from pydantic import BaseModel, Field
from .risk_agent import RiskAnalysis

class InvestmentAnalysis(BaseModel):
    investment_strengths: list[str] = Field(default_factory=list)
    investment_weaknesses: list[str] = Field(default_factory=list)
    opportunities: list[str] = Field(default_factory=list)
    threats: list[str] = Field(default_factory=list)
    investment_score: float = Field(description="Score from 0.0 to 10.0", le=10.0, ge=0.0)
    score_category: str = Field(
        description="Exceptional, Strong, Moderate, Weak, High Risk"
    )
    score_rationale: str
    recommendation: str = Field(
        description="Strong Invest, Invest, Monitor, Pass"
    )
    investment_thesis: str
    executive_summary: str

class InvestmentAgent(BaseAgent):
    def __init__(self):
        markdown_prompt = self.load_prompt("investment_agent_prompt.md")

        super().__init__(
            system_prompt=markdown_prompt,
            response_model=InvestmentAnalysis,
        )

    def analyze_investment(self, risk_details: RiskAnalysis) -> InvestmentAnalysis:
        """Analyze the investment opportunity based on the provided description."""
        response = self.run(risk_details.model_dump_json())
        return response