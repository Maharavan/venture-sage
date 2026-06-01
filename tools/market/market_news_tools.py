from strands import tool
import feedparser
from typing import List,Dict

@tool
def get_market_news(limit: int = 5, keywords: List[str] = None) -> Dict:
    """Fetch the latest market news and trends."""
    results = {}
    try:
        for keyword in keywords:
            print(f"Fetching news for keyword: {keyword}")

            rss_url = (
                "https://news.google.com/rss/search"
                f"?q={keyword}"
            )
            feed = feedparser.parse(rss_url)
            news_items = []
            for entry in feed.entries[:limit]:
                news_items.append({
                    "title": entry.title,
                    "link": entry.link,
                    "published": entry.published
                })
            results[keyword] = news_items
        return results
                        
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }