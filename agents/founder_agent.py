from pydantic import BaseModel, Field
from tools.founder import FOUNDER_TOOLS
from .base_agent import BaseAgent

class FounderAnalysis(BaseModel):
    founders: list[str]
    education: list[str]
    professional_experience: list[str]
    domain_expertise: list[str]
    technical_expertise: list[str]
    previous_startups: list[str]
    previous_exits: list[str]
    strengths: list[str]
    risks: list[str]
    founder_market_fit: str
    execution_capability: str
    founder_score: float = Field(description="Score from 0.0 to 10.0", le=10.0, ge=0.0)
    summary: str


class FounderAgent(BaseAgent):
    def __init__(self):
        markdown_prompt = self.load_prompt("founder_agent_prompt.md")

        super().__init__(
            system_prompt=markdown_prompt,
            response_model=FounderAnalysis,
            tools=FOUNDER_TOOLS,
        )

    def analyze_founder(self, founder_description: str) -> FounderAnalysis:
        """Analyze the founder based on the provided description."""
        response = self.run(founder_description)
        return response