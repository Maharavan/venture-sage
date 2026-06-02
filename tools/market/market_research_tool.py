from strands import tool
from typing import List, Dict, Any
from services.exa_service import ExaService


@tool
def get_market_research_tool(markets: List[str]) -> Dict[str, Any]:
    """
    Retrieve market research information including market size,
    growth, customer segments, industry trends, opportunities,
    and risks.
    """
    try:
        exa = ExaService()
        result = {}
        for market in markets:
            query = f"""
            {market} market size growth rate industry trends
            customer segments opportunities risks TAM SAM CAGR
            """
            result[market] = exa.search(query)
        return {"status": "success", "data": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}
