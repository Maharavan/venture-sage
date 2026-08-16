from strands import tool
from typing import List, Optional, Dict
from services.feedparser_service import FeedparserService


@tool
def get_market_news(limit: int = 5, keywords: Optional[List[str]] = None) -> Dict:
    """Fetch the latest market news and trends."""
    try:
        svc = FeedparserService()
        if not keywords:
            return {"status": "ok", "results": {}}
        return {keyword: svc.search_news(keyword, limit) for keyword in keywords}
    except Exception as e:
        return {"status": "error", "message": str(e)}
