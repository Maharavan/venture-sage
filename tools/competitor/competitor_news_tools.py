from strands import tool
from typing import Dict, List
from services.newsapi_service import NewsApiService


@tool
def search_competitor_news_tool(competitors: List[str], limit: int = 5) -> Dict:
    """Search for news related to a specific competitor."""
    try:
        news_api = NewsApiService()
        news_results = {}
        for competitor in competitors:
            try:
                articles = news_api.search(competitor, limit)
                news_results[competitor] = [{"competitor": competitor, **a} for a in articles]
            except RuntimeError as e:
                news_results[competitor] = {"error": str(e)}
        return {
            "status": "success",
            "competitors_count": len(competitors),
            "article_count": sum(len(a) for a in news_results.values() if isinstance(a, list)),
            "news": news_results
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
