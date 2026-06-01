from agents.supervisor_agent import SupervisorAgent

class DueDiligenceWorkflow:
    def __init__(self):
        """Initialize the workflow with necessary agents."""
        self.supervisor_agent = SupervisorAgent()

    def run(self, startup_description: str):
        analysis = self.supervisor_agent.run(task_description=startup_description)
        
        print("Supervisor Analysis:", analysis)