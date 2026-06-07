from collections import defaultdict
from typing import List

from agents.market_agent import MarketAgent
from agents.competitor_agent import CompetitorAgent
from agents.founder_agent import FounderAgent
from agents.financial_agent import FinancialAgent
from agents.risk_agent import RiskAgent
from agents.investment_agent import InvestmentAgent
from agents.memo_agent import MemoAgent


AGENT_REGISTRY = {
    "market_agent": {
        "instance": MarketAgent(),
        "domain": "research",
        "description": (
            "Analyze TAM, SAM, SOM, market size, "
            "industry trends and growth."
        ),
        "workflow_required": False,
        "depends_on": [],
        "stage": 1,
        "enabled": True
    },

    "competition_agent": {
        "instance": CompetitorAgent(),
        "domain": "research",
        "description": (
            "Analyze competitors, positioning, "
            "market share and differentiation."
        ),
        "workflow_required": False,
        "depends_on": [],
        "stage": 1,
        "enabled": True
    },

    "founder_agent": {
        "instance": FounderAgent(),
        "domain": "research",
        "description": (
            "Analyze founders, leadership team, "
            "experience and prior exits."
        ),
        "workflow_required": False,
        "depends_on": [],
        "stage": 1,
        "enabled": True
    },

    "finance_agent": {
        "instance": FinancialAgent(),
        "domain": "research",
        "description": (
            "Analyze funding history, valuation, "
            "revenue and burn rate."
        ),
        "workflow_required": False,
        "depends_on": [],
        "stage": 1,
        "enabled": True
    },

    "risk_agent": {
        "instance": RiskAgent(),
        "domain": "analysis",
        "description": (
            "Assess execution risk, market risk, "
            "competitive risk and financial risk."
        ),
        "workflow_required": True,
        "depends_on": [
            "market_agent",
            "competition_agent",
            "founder_agent",
            "finance_agent"
        ],
        "stage": 2,
        "enabled": True
    },

    "investment_agent": {
        "instance": InvestmentAgent(),
        "domain": "analysis",
        "description": (
            "Generate investment score and recommendation."
        ),
        "workflow_required": True,
        "depends_on": [
            "risk_agent"
        ],
        "stage": 3,
        "enabled": True
    },

    "memo_agent": {
        "instance": MemoAgent(),
        "domain": "reporting",
        "description": (
            "Generate final investment memo/report."
        ),
        "workflow_required": True,
        "depends_on": [
            "investment_agent"
        ],
        "stage": 4,
        "enabled": True
    }
}

def get_agent(agent_name) -> object:
    """Fetch an agent instance by name if it is enabled."""
    agent_info = AGENT_REGISTRY.get(agent_name)
    if agent_info and agent_info["enabled"]:
        return agent_info["instance"]
    else:
        raise ValueError(f"Agent '{agent_name}' not found or not enabled.")
    
def get_enabled_agents() -> List[tuple]:
    """Return a list of all enabled agents."""
    return [(agent_name,agent_info) for agent_name,agent_info in AGENT_REGISTRY.items() if agent_info["enabled"]]

def get_supervisor_visible_agents() -> str:
    """Return a string containing agent names and descriptions for enabled agents."""
    enabled_agents = get_enabled_agents()
    return "\n".join(
        f"- {agent_name}: {agent_info['description']} (Stage: {agent_info['stage']})"
        for agent_name, agent_info in enabled_agents
    )


def provide_available_agents() -> str:
    """Return a string containing agent names and descriptions for enabled agents."""

    enabled_agents = get_enabled_agents()
    
    return "\n".join(
        f"{agent_name}: {agent_info['description']}"
        for agent_name,agent_info in enabled_agents
    )

def required_agents_for_execution(required_agent: str) -> dict:
    """BFS from required_agent through its dependency graph.

    Returns a dict mapping stage number -> list of agent names,
    covering every agent that must run (in order) to produce the
    requested agent's output.
    """
    queue = [required_agent]
    visited: set = set()

    while queue:
        agent = queue.pop(0)
        if agent in visited:
            continue
        visited.add(agent)
        queue.extend(AGENT_REGISTRY[agent]["depends_on"])

    result: dict = defaultdict(list)
    for agent_name in visited:
        stage = AGENT_REGISTRY[agent_name]["stage"]
        result[stage].append(agent_name)

    return dict(result)