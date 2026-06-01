from agents.supervisor_agent import SupervisorAgent
from config.agent_registry import get_agent

class DueDiligenceWorkflow:
    def __init__(self):
        """Initialize the workflow with necessary agents."""
        self.supervisor_agent = SupervisorAgent()

    def run(self, startup_description: str):
        """Run the due diligence workflow for a given startup description."""
        analysis = self.supervisor_agent.run(task_description=startup_description)
        print("Supervisor Agent Analysis:")
        print(f"Startup Type: {analysis}")
        print("Selected Agents and Tasks:")
        for selected in analysis.selected_agents:
            print(f"- Agent: {selected.agent}, Task: {selected.task} Stage: {selected.stage}")

        market_agent = get_agent("market_agent")
        market_agent.analyze_market(market_description=startup_description)
        

        
        
        