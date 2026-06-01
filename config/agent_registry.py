# from agents.market_agent import MarketAgent
# from agents.competition_agent import CompetitionAgent
# from agents.founder_agent import FounderAgent
# from agents.finance_agent import FinanceAgent
# from agents.risk_agent import RiskAgent
# from agents.investment_agent import InvestmentAgent
# from agents.reporting.memo_agent import MemoAgent


AGENT_REGISTRY = {
    "market_agent": {
        # "instance": MarketAgent(),
        "domain": "research",
        "description": (
            "Analyze TAM, SAM, SOM, market size, "
            "industry trends and growth."
        ),
        "depends_on": [],
        "stage": 1,
        "enabled": True
    },

    "competition_agent": {
        # "instance": CompetitionAgent(),
        "domain": "research",
        "description": (
            "Analyze competitors, positioning, "
            "market share and differentiation."
        ),
        "depends_on": [],
        "stage": 1,
        "enabled": True
    },

    "founder_agent": {
        # "instance": FounderAgent(),
        "domain": "research",
        "description": (
            "Analyze founders, leadership team, "
            "experience and prior exits."
        ),
        "depends_on": [],
        "stage": 1,
        "enabled": True
    },

    "finance_agent": {
        # "instance": FinanceAgent(),
        "domain": "research",
        "description": (
            "Analyze funding history, valuation, "
            "revenue and burn rate."
        ),
        "depends_on": [],
        "stage": 1,
        "enabled": True
    },

    "risk_agent": {
        # "instance": RiskAgent(),
        "domain": "analysis",
        "description": (
            "Assess execution risk, market risk, "
            "competitive risk and financial risk."
        ),
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
        # "instance": InvestmentAgent(),
        "domain": "analysis",
        "description": (
            "Generate investment score and recommendation."
        ),
        "depends_on": [
            "risk_agent"
        ],
        "stage": 3,
        "enabled": True
    },

    "memo_agent": {
        # "instance": MemoAgent(),
        "domain": "reporting",
        "description": (
            "Generate final investment memo."
        ),
        "depends_on": [
            "investment_agent"
        ],
        "stage": 4,
        "enabled": True
    }
}

def get_agent(agent_name):
    """Fetch an agent instance by name if it is enabled."""
    agent_info = AGENT_REGISTRY.get(agent_name)
    if agent_info and agent_info["enabled"]:
        return agent_info["instance"]
    else:
        raise ValueError(f"Agent '{agent_name}' not found or not enabled.")
    
def get_enabled_agents():
    """Return a list of all enabled agent instances."""
    return [agent_info["instance"] for agent_info in AGENT_REGISTRY.values() if agent_info["enabled"]]


def get_enabled_agents_with_descriptions():
    """Return a list of tuples containing agent names and descriptions for enabled agents."""
    return "\n".join(
        f"- {agent_name}: {agent_info['description']}"
        for agent_name, agent_info in AGENT_REGISTRY.items()
        if agent_info["enabled"]
    )