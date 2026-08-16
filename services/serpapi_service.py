import serpapi
from typing import List, Dict, Any
from .base_service import BaseService


class SerpApiService(BaseService):
    def __init__(self):
        self._api_key = self._require_env("SERPAPI_API_KEY")
        self._client = serpapi.Client(api_key=self._api_key)

    def search(self, query: str, num: int = 5) -> List[Dict[str, Any]]:
        results = self._client.search({
            "q": query,
            "num": num,
        })
        return results.get("organic_results", [])
