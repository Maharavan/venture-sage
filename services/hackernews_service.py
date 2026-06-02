import requests
from typing import List, Dict, Any
from .base_service import BaseService


class HackerNewsService(BaseService):
    _BASE_URL = "https://hn.algolia.com/api/v1/search"

    def search(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        response = requests.get(
            self._BASE_URL,
            params={"query": query, "hitsPerPage": limit}
        )
        response.raise_for_status()
        return [
            {
                "title": hit.get("title"),
                "url": hit.get("url"),
                "points": hit.get("points"),
                "created_at": hit.get("created_at"),
                "author": hit.get("author"),
                "comments": hit.get("num_comments"),
                "story_text": hit.get("story_text")
            }
            for hit in response.json().get("hits", [])
        ]
