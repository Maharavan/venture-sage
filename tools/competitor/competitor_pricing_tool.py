from strands import tool
from typing import Dict, List
from services.serpapi_service import SerpApiService
from services.firecrawl_service import FirecrawlService


@tool
def search_competitor_pricing_tool(competitors: List[str]) -> Dict:
    """
    Find official pricing pages and extract
    basic pricing information.
    """
    try:
        serp = SerpApiService()
        firecrawl = FirecrawlService()
        results = {}
        for company in competitors:
            organic = serp.search(f"{company} pricing plans in official website")
            pricing_url = next(
                (r.get("link") for r in organic
                 if "pricing" in r.get("link", "").lower() or "plan" in r.get("link", "").lower()),
                None
            )
            if not pricing_url:
                results[company] = {"status": "not_found"}
                continue
            try:
                pricing_data = firecrawl.scrape_and_interact(pricing_url, "List the pricing")
                results[company] = {
                    "status": "success",
                    "pricing_url": pricing_url,
                    "pricing_data": pricing_data
                }
            except Exception as pricing_error:
                results[company] = {
                    "status": "pricing_page_error",
                    "pricing_url": pricing_url,
                    "message": str(pricing_error)
                }
        return {"status": "success", "competitor_count": len(competitors), "pricing_results": results}
    except Exception as e:
        return {"status": "error", "message": str(e)}
