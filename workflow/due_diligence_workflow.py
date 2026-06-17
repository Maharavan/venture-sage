from config.agent_registry import get_agent, required_agents_for_execution, AGENT_REGISTRY
from utils.console import print_error, print_info, print_warning, print_agent_summary
from guardrails.output_guardrails import validate_output_quality
import asyncio


async def run_agent(agent, workflow_context):
    try:
        instance = get_agent(agent)
        print_info(f"{agent} thinking…")
        result = await asyncio.to_thread(instance.analyze, workflow_context)
        if result is None:
            print_error(f"{agent} returned no result.")
            return agent, None

        quality = validate_output_quality(result, agent)
        for warning in quality.warnings:
            print_warning(warning)
        for error in quality.errors:
            print_error(error)
        if not quality.passed:
            print_error(f"{agent} output failed quality check — treating as failed.")
            return agent, None

        summary = getattr(result, "summary", None)
        if summary:
            print_agent_summary(agent, summary)
        return agent, result
    except ValueError as e:
        print_error(f"{agent} not found in registry: {e}")
        return agent, None
    except Exception as e:
        print_error(f"{agent} failed: {e}")
        return agent, None


async def due_dil_workflow(required_agent: str, startup_description: str) -> dict:
    """Run the due diligence workflow up to and including required_agent."""
    stage_wise = required_agents_for_execution(required_agent)
    workflow_context = {"startup_description": startup_description}
    failed_agents: set[str] = set()

    for stage in sorted(stage_wise.keys()):
        agents_in_stage = stage_wise[stage]

        # Drop any agent whose dependencies all failed — nothing useful to pass it.
        
        runnable = [
            a for a in agents_in_stage
            if not all(dep in failed_agents for dep in AGENT_REGISTRY[a]["depends_on"])
            or not AGENT_REGISTRY[a]["depends_on"]
        ]

        blocked = set(agents_in_stage) - set(runnable)
        for a in blocked:
            print_warning(f"Skipping {a} — required dependencies failed.")
            failed_agents.add(a)

        if not runnable:
            print_warning(f"Stage {stage} has no runnable agents — stopping workflow.")
            break

        outcomes = await asyncio.gather(*[run_agent(a, workflow_context) for a in runnable])

        for agent, result in outcomes:
            workflow_context[agent] = result
            if result is None:
                failed_agents.add(agent)

    return workflow_context
