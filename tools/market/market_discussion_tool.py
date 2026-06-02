from strands import tool
from services.hackernews_service import HackerNewsService


@tool
def get_market_discussion(keywords: str, limit: int = 10) -> dict:
    """Fetch market discussion data for the given keywords."""
    try:
        results = HackerNewsService().search(keywords, limit)
        count = len(results)
        return {
            "status": "success",
            "keyword": keywords,
            "mention_count": count,
            "total_points": sum(item["points"] or 0 for item in results),
            "total_comments": sum(item["comments"] or 0 for item in results),
            "discussion_data": results,
            "average_points": round(sum(item["points"] or 0 for item in results) / count, 2) if count else 0,
            "average_comments": round(sum(item["comments"] or 0 for item in results) / count, 2) if count else 0
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
