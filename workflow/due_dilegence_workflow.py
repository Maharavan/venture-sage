from agents.supervisor_agent import SupervisorAgent
from config.agent_registry import get_agent
import asyncio

class DueDiligenceWorkflow:
    def __init__(self):
        """Initialize the workflow with necessary agents."""
        self.supervisor_agent = SupervisorAgent()

    def run(self, startup_description: str):
        """Run the due diligence workflow for a given startup description."""
        analysis = self.supervisor_agent.run(task_description=startup_description)
        print("Supervisor Agent Analysis:")
        print(f"Startup Type: {analysis.selected_agents}")
        # print("Selected Agents and Tasks:")
        # for selected in analysis.selected_agents:
        #     print(f"- Agent: {selected.agent}, Task: {selected.task} Stage: {selected.stage}")

        # # Stage 1 — parallel research agents
        # market_agent = get_agent("market_agent")
        # competition_agent = get_agent("competition_agent")
        # founder_agent = get_agent("founder_agent")
        # finance_agent = get_agent("finance_agent")
        # risk_agent = get_agent("risk_agent")
        # investment_agent = get_agent("investment_agent")
        # memo_agent = get_agent("memo_agent")




        # market_result = market_agent.analyze_market(market_description=startup_description)
        # competition_result = competition_agent.analyze_market(market_description=startup_description)
        # founder_result = founder_agent.analyze_founder(founder_description=startup_description)
        # finance_result = finance_agent.analyze_finance(funding_info=startup_description)

        # # Stage 2 — risk assessment
        # risk_result = risk_agent.analyze_risk(
        #     market_details=market_result,
        #     competitor_details=competition_result,
        #     financial_details=finance_result,
        #     founder_details=founder_result,
        # )

        # # Stage 3 — investment scoring
        # investment_result = investment_agent.analyze_investment(risk_details=risk_result)

        # # Stage 4 — memo generation
        # memo_result = memo_agent.generate_memo(investment_info=investment_result)

        # print(memo_result)
