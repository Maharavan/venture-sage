import os
import serpapi
from strands import tool
from typing import Dict, List
from firecrawl import Firecrawl

@tool
def competitor_pricing_tool(
competitors: List[str]
) -> Dict:
    """
    Find official pricing pages and extract
    basic pricing information.
    """

    try:
        serp_api_key = os.getenv("SERPAPI_API_KEY")

        if not serp_api_key:
            return {
                "status": "error",
                "message": "SERPAPI_API_KEY environment variable is not set."
            }

        client = serpapi.Client()

        results = {}
        
        for company in competitors:

            search_results = client.search({
                "q": f"{company} pricing plans",
                "num": 5,
                "api_key": serp_api_key
            })

            pricing_url = None

            for result in search_results.get(
                "organic_results",
                []
            ):

                link = result.get("link", "")

                if "pricing" in link.lower() or "plan" in link.lower():
                    pricing_url = link
                    break

            if not pricing_url:
                results[company] = {
                    "status": "not_found"
                }
                continue

            try:
                firecrawl_api_key = os.getenv("FIRECRAWL_API_KEY")
                if not firecrawl_api_key:
                    return {
                        "status": "error",
                        "message": "FIRECRAWL_API_KEY not set"
                    }


                app = Firecrawl(api_key=firecrawl_api_key)

                result = app.scrape(pricing_url,formats=["markdown"])
                scrape_id = result.metadata.scrape_id
                response = app.interact(scrape_id, prompt="List the pricing ")
                print(response.output)

                app.stop_interaction(scrape_id)
                
                results[company] = {
                    "status": "success",
                    "pricing_url": pricing_url,
                    "pricing_data": response.output
                }


            except Exception as pricing_error:

                results[company] = {
                    "status": "pricing_page_error",
                    "pricing_url": pricing_url,
                    "message": str(pricing_error)
                }

        return {
            "status": "success",
            "competitor_count": len(competitors),
            "pricing_results": results
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }