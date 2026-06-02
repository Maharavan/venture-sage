from strands import tool
from typing import List, Dict
from services.trends_service import TrendsService


@tool
def get_market_trends(keywords: List[str], timeframe='today 12-m') -> Dict:
    """Fetch market trends for the given keywords and timeframe."""
    try:
        trends = TrendsService().interest_over_time(keywords, timeframe)
        if not trends:
            return {"status": "No data", "keywords": keywords}
        return trends
    except Exception as e:
        return {"status": "error", "message": str(e)}
