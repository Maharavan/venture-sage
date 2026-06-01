import os
import serpapi
import requests
from bs4 import BeautifulSoup
from strands import tool
from typing import Dict, List

@tool
def competitor_pricing_tool(
competitors: List[str]
) -> Dict:
    """
    Find official pricing pages and extract
    basic pricing information.
    """

    try:
        api_key = os.getenv("SERPAPI_API_KEY")

        if not api_key:
            return {
                "status": "error",
                "message": "SERPAPI_API_KEY environment variable is not set."
            }

        client = serpapi.Client()

        results = {}
        pricing_keywords = [
            "pricing",
            "plans",
            "subscriptions",
            "billing",
            "cost"
        ]
        for company in competitors:

            search_results = client.search({
                "q": f"{company} {' '.join(pricing_keywords)}",
                "num": 5,
                "api_key": api_key
            })

            pricing_url = None

            for result in search_results.get(
                "organic_results",
                []
            ):

                link = result.get("link", "")

                if "pricing" in link.lower():
                    pricing_url = link
                    break

            if not pricing_url:
                results[company] = {
                    "status": "not_found"
                }
                continue

            try:
                response = requests.get(
                    pricing_url,
                    timeout=10
                )

                soup = BeautifulSoup(
                    response.text,
                    "html.parser"
                )

                page_text = soup.get_text(
                    separator=" ",
                    strip=True
                )

                

                results[company] = {
                    "status": "success",
                    "pricing_url": pricing_url,
                    "page_preview": page_text
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

if __name__ == "__main__":
    # Example usage
    competitors = ["claude", "openai", "gemini"]
    pricing_info = competitor_pricing_tool(competitors)
    print(pricing_info)