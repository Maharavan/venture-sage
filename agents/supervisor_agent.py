from strands import Agent
from config.agent_registry import get_enabled_agents_with_descriptions
from config.settings import settings
from pathlib import Path
from pydantic import BaseModel

class SelectedAgent(BaseModel):
    agent: str
    task: str

class SupervisorAnalysis(BaseModel):
    startup_type: str
    selected_agents: list[SelectedAgent]

class SupervisorAgent:
    def __init__(self):
        self.retrieve_model = settings.get_model()
        self.enabled_agents = get_enabled_agents_with_descriptions()
    
    def run(self, task_description: str) -> SupervisorAnalysis:
        """Select the most appropriate agent based on the task description and agent capabilities.
        """

        prompt_path = Path(__file__).parent.parent / "prompts" / "supervisor_agent_prompt.md"

        markdown_prompt = prompt_path.read_text(encoding="utf-8")

        SYSTEM_PROMPT = markdown_prompt.replace(
            "{agent_descriptions}",
            self.enabled_agents
        )

        agent = Agent(
            system_prompt=SYSTEM_PROMPT,
            model=self.retrieve_model,
            structured_output_model=SupervisorAnalysis
            
        )
        response = agent(task_description)

        return response