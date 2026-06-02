from strands import tool
from typing import Dict, List
from services.serpapi_service import SerpApiService


@tool
def get_team_growth_tool(companies: List[str]) -> Dict:
    """Retrieve team size, hiring velocity, and headcount growth as a burn rate signal."""
    try:
        serp = SerpApiService()
        results = {}
        for company in companies:
            query = f"{company} team size employee growth hiring headcount engineering team"
            results[company] = serp.search(query)
        return {"status": "success", "company_count": len(companies), "results": results}
    except Exception as e:
        return {"status": "error", "message": str(e)}
