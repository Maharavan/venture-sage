from strands import tool
from typing import List, Dict, Any
from services.exa_service import ExaService


@tool
def get_revenue_signals_tool(companies: List[str]) -> Dict[str, Any]:
    """Retrieve revenue signals including ARR, MRR, customer growth, and monetization indicators."""
    try:
        exa = ExaService()
        result = {}
        for company in companies:
            query = f"""
                {company}
                ARR MRR revenue customers enterprise customers
                annual recurring revenue pricing growth
                """
            result[company] = exa.search_and_contents(query)
        return {"status": "success", "data": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}
