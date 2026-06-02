import requests
from typing import List, Dict, Any
from .base_service import BaseService


class GdeltService(BaseService):
    _BASE_URL = "https://api.gdeltproject.org/api/v2/doc/doc"

    def search(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        response = requests.get(
            self._BASE_URL,
            params={"query": query, "mode": "artlist", "format": "json", "maxrecords": limit},
            timeout=15
        )
        response.raise_for_status()
        data = response.json()
        return [
            {
                "title": article.get("title"),
                "url": article.get("url"),
                "domain": article.get("domain"),
                "seendate": article.get("seendate")
            }
            for article in data.get("articles", [])
        ]
