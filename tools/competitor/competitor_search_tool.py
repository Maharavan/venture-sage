import os
from tavily import TavilyClient
from strands import tool
from typing import Dict

@tool
def search_competitors(startup : str) -> Dict:
    """Search for competitors based on the provided startup."""
    
    try:
        api_key = os.getenv("TAVILY_API_KEY")
        if not api_key:
            return {
                "status": "error",
                "message": "TAVILY_API_KEY environment variable is not set."
            }
        client = TavilyClient(api_key=api_key)
        results = client.search(query=f"""
            Identify direct competitors,
            alternative products,
            and companies solving the same
            customer problem as {startup}
            """,
            max_results=5)
        
        competitors = []
        for item in results.get("results", []):
            competitors.append({
                "title": item.get("title"),
                "url": item.get("url"),
                "content": item.get("content")
            })

        return {
            "status": "success",
            "startup": startup,
            "competitors": competitors,
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }