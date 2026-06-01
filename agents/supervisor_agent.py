from config.agent_registry import get_enabled_agents_with_descriptions_and_stage
from pydantic import BaseModel
from .base_agent import BaseAgent

class SelectedAgent(BaseModel):
    agent: str
    task: str
    stage: int
    
class SupervisorAnalysis(BaseModel):
    startup_type: str
    selected_agents: list[SelectedAgent]

class SupervisorAgent(BaseAgent):
    def __init__(self):
        
        self.enabled_agents = get_enabled_agents_with_descriptions_and_stage()
        markdown_prompt = self.load_prompt("supervisor_agent_prompt.md")

        system_prompt = markdown_prompt.replace(
            "{agent_descriptions}",
            self.enabled_agents
        )

        super().__init__(
            system_prompt=system_prompt,
            response_model=SupervisorAnalysis,
        )

    def run(self, task_description: str) -> SupervisorAnalysis:
        """Select the most appropriate agent based on the task description and agent capabilities."""
        return super().run(task_description)
