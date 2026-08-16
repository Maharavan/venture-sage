from typing import Dict

from pydantic import BaseModel, Field
from tools.founder import FOUNDER_TOOLS
from .base_agent import BaseAgent
from utils.console import print_error, print_warning

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
    summary: str = Field(
        description=(
            "2–4 sentences covering every data point collected: founders identified, education, "
            "professional experience, domain and technical expertise, previous startups and exits, "
            "founder-market fit, execution capability, and founder_score. "
            "End with one sentence on the team's credibility and ability to execute."
        )
    )


class FounderAgent(BaseAgent):
    def __init__(self):
        markdown_prompt = self.load_prompt("founder_agent_prompt.md")

        super().__init__(
            system_prompt=markdown_prompt,
            agent_name="FounderAgent",
            startup_description="Analyze founders, their experience, domain expertise, and execution capability.",
            response_model=FounderAnalysis,
            tools=FOUNDER_TOOLS,
        )

    def analyze(self, context: Dict) -> FounderAnalysis:
        """Analyze the founder based on the provided description."""
        retrieve_context = context.get("startup_description",  "")
        if not retrieve_context:
            print_warning("FounderAgent: no startup description in context, skipping.")
            return None
        try:
            return self.run(retrieve_context)
        except Exception as e:
            print_error(f"FounderAgent failed: {e}")
            return None
