from strands import tool
from typing import List, Dict, Any
from services.tavily_service import TavilyService


@tool
def get_product_reviews_tool(competitors: List[str]) -> Dict[str, Any]:
    """
    Search for customer reviews and ratings of competitor products
    across G2, Trustpilot, App Store, and Play Store.
    """
    try:
        tavily = TavilyService()
        results = {}
        for competitor in competitors:
            query = f"{competitor} reviews ratings G2 Trustpilot customers feedback"
            results[competitor] = tavily.search(query)
        return {"status": "success", "competitor_count": len(competitors), "reviews": results}
    except Exception as e:
        return {"status": "error", "message": str(e)}
