from agents.base_agent import BaseAgent
from tools.risk import RISK_TOOLS
from pydantic import BaseModel, Field
from .market_agent import MarketAnalysis
from .competitor_agent import CompetitionAnalysis
from .financial_agent import FinanceAnalysis
from .founder_agent import FounderAnalysis

class RiskAnalysis(BaseModel):
    technology_risks: list[str] = Field(default_factory=list)
    market_risks: list[str] = Field(default_factory=list)
    regulatory_risks: list[str] = Field(default_factory=list)
    operational_risks: list[str] = Field(default_factory=list)
    execution_risks: list[str] = Field(default_factory=list)
    risk_mitigations: list[str] = Field(default_factory=list)
    risk_score: float = Field(description="Risk score from 0.0 to 10.0", le=10.0, ge=0.0)
    score_category: str = Field(description="Low Risk, Moderate Risk, Elevated Risk, High Risk, Critical Risk")
    score_rationale: str
    key_risks: list[str] = Field(default_factory=list, description="Top risks investors should monitor")
    recommendation: str
    summary: str

class RiskAgent(BaseAgent):
    def __init__(self):
        markdown_prompt = self.load_prompt("risk_agent_prompt.md")

        super().__init__(
            system_prompt=markdown_prompt,
            response_model=RiskAnalysis,
            tools=RISK_TOOLS,
        )

    def analyze_risk(self, market_details: MarketAnalysis, competitor_details: CompetitionAnalysis, financial_details: FinanceAnalysis,
                     founder_details: FounderAnalysis) -> RiskAnalysis:
        """Analyze the risk profile based on the provided description."""
        
        multi_query = f"""
        
        Market Agent: {market_details.model_dump_json()}
        Competitor Agent: {competitor_details.model_dump_json()}
        Founder Agent: {founder_details.model_dump_json()}
        Financial Agent: {financial_details.model_dump_json()}

        """
        response = self.run(multi_query)
        return response