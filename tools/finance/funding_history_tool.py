from strands import tool
from typing import List, Dict, Any
from services.exa_service import ExaService


@tool
def get_funding_history_tool(companies: List[str]) -> Dict[str, Any]:
    """
    Retrieve funding rounds, investors, valuations,
    and fundraising history for companies.
    """
    try:
        exa = ExaService()
        results = {}
        for company in companies:
            query = f"""
            {company} funding rounds investors valuation
            total funding raised series seed funding
            fundraising history venture capital
            """
            results[company] = exa.search_and_contents(query)
        return {"status": "success", "data": results}
    except Exception as e:
        return {"status": "error", "message": str(e)}
