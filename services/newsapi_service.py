import requests
from typing import List, Dict, Any
from .base_service import BaseService


class NewsApiService(BaseService):
    _BASE_URL = "https://newsapi.org/v2/everything"

    def __init__(self):
        self._api_key = self._require_env("NEWSAPI_KEY")

    def search(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        response = requests.get(
            self._BASE_URL,
            params={"q": query, "apiKey": self._api_key, "pageSize": limit, "sortBy": "publishedAt"},
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        if data.get("status") != "ok":
            raise RuntimeError(data.get("message", "Unknown NewsAPI error"))
        return [
            {
                "title": article.get("title"),
                "description": article.get("description"),
                "url": article.get("url"),
                "publishedAt": article.get("publishedAt"),
                "source": article.get("source", {}).get("name")
            }
            for article in data.get("articles", [])
        ]
