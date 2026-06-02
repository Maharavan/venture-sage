from tavily import TavilyClient
from typing import List, Dict, Any
from .base_service import BaseService


class TavilyService(BaseService):
    def __init__(self):
        self._client = TavilyClient(api_key=self._require_env("TAVILY_API_KEY"))

    def search(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        results = self._client.search(query=query, max_results=max_results)
        return [
            {"title": item.get("title"), "url": item.get("url"), "content": item.get("content")}
            for item in results.get("results", [])
        ]
