from strands import tool
from services.gdelt_service import GdeltService


@tool
def get_founder_mentions_tool(founder_name: str, limit: int = 10) -> dict:
    """Search news mentions of a founder using GDELT."""
    try:
        articles = GdeltService().search(founder_name, limit)
        return {
            "status": "success",
            "founder": founder_name,
            "mention_count": len(articles),
            "articles": articles
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
