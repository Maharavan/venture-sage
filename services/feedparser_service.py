import feedparser
from typing import List, Dict, Any
from .base_service import BaseService


class FeedparserService(BaseService):
    _GOOGLE_NEWS_RSS = "https://news.google.com/rss/search?q={query}"
    _GOOGLE_TRENDS_RSS = "https://trends.google.com/trends/trendingsearches/daily/rss?geo=US"

    def search_news(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        feed = feedparser.parse(self._GOOGLE_NEWS_RSS.format(query=query))
        return [
            {"title": entry.title, "link": entry.link, "published": entry.published}
            for entry in feed.entries[:limit]
        ]

    def trending_searches(self, limit: int = 10) -> List[Dict[str, Any]]:
        feed = feedparser.parse(self._GOOGLE_TRENDS_RSS)
        return [
            {"title": entry.title, "link": entry.link, "published": entry.published}
            for entry in feed.entries[:limit]
        ]
