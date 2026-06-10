from agents.supervisor_agent import SupervisorAgent
from config.agent_registry import get_agent
import asyncio
from collections import defaultdict

async def run_agent(agent, workflow_context):
    #  agent run planned

    instance = get_agent(agent)
    result = instance.analyze(workflow_context)

    return agent,result

async def due_diligence_workflow(startup_description: str):
    """Run the due diligence workflow for a given startup description."""
    # parallel fan-in fan out
    supervisor_agent = SupervisorAgent()
    stage_wise = defaultdict(list)
    analysis = supervisor_agent.run(task_description=startup_description)
    print("Supervisor Agent Analysis:")
    print(f"Startup Type: {analysis.selected_agents}")
    print("Selected Agents and Tasks:")
    for selected in analysis.selected_agents:
        print(f"- Agent: {selected.agent}, Task: {selected.task} Stage: {selected.stage}")
        stage_wise[selected.stage].append(selected.agent)

    sorted_keys = sorted(stage_wise.keys())
    workflow_context = {
        "supervisor_agent":startup_description
    }

    for stage in sorted_keys:
        tasks = [
            run_agent(
                agent,
                workflow_context
            )
            for agent in stage_wise[stage]
        ]
        outcomes = await asyncio.gather(*tasks)

        for agent,result in outcomes:
            workflow_context[agent] = result
    print(workflow_context)    
