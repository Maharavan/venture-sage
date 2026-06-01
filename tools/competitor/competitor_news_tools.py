import os
import requests
from strands import tool
from typing import Dict,List

@tool
def search_competitor_news_tool(competitors: List[str],limit: int = 5) -> Dict:
    """Search for news related to a specific competitor."""
    try:
        news_results = {}
        api_key = os.getenv("NEWSAPI_KEY")
        if not api_key:
            return {
                "status": "error",
                "message": "NEWSAPI_KEY environment variable is not set."
            }
        for competitor in competitors:
            response = requests.get(f"https://newsapi.org/v2/everything",params={
                "q": competitor,
                "apiKey": api_key,
                "pageSize": limit,
                "sortBy": "publishedAt"
            },timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get("status") != "ok":
                    news_results[competitor] = {
                        "error": f"API error: {data.get('message', 'Unknown error')}"
                    }
                    continue
                news_results[competitor] = []
                for article in data.get("articles", []):
                    news_results[competitor].append({
                        "competitor": competitor,
                        "title": article.get("title"),
                        "description": article.get("description"),
                        "url": article.get("url"),
                        "publishedAt": article.get("publishedAt"),
                        "source": article.get("source", {}).get("name")
                    })
            else:
                news_results[competitor] = {
                    "error": f"Failed to fetch news. Status code: {response.status_code}"
                }
        return {
            "status": "success",
            "competitors_count": len(competitors),
            "article_count": sum(len(articles) for articles in news_results.values() if isinstance(articles, list)),
            "news": news_results
        }
    
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
