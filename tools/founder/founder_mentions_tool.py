from strands import tool
import requests

@tool
def founder_mentions_tool(
    founder_name: str,
    limit: int = 10
) -> dict:
    """Search news mentions of a founder using GDELT."""

    try:

        response = requests.get(
            "https://api.gdeltproject.org/api/v2/doc/doc",
            params={
                "query": founder_name,
                "mode": "artlist",
                "format": "json",
                "maxrecords": limit
            },
            timeout=15
        )

        response.raise_for_status()

        data = response.json()

        articles = []

        for article in data.get("articles", []):

            articles.append({
                "title": article.get("title"),
                "url": article.get("url"),
                "domain": article.get("domain"),
                "seendate": article.get("seendate")
            })

        return {
            "status": "success",
            "founder": founder_name,
            "mention_count": len(articles),
            "articles": articles
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }