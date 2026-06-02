from strands import tool
from typing import Dict
from services.tavily_service import TavilyService


@tool
def search_competitors(startup: str) -> Dict:
    """Search for competitors based on the provided startup."""
    try:
        competitors = TavilyService().search(
            query=f"""
            Identify direct competitors,
            alternative products,
            and companies solving the same
            customer problem as {startup}
            """
        )
        return {"status": "success", "startup": startup, "competitors": competitors}
    except Exception as e:
        return {"status": "error", "message": str(e)}
