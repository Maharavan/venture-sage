from exa_py import Exa
from typing import List, Dict, Any
from .base_service import BaseService


class ExaService(BaseService):
    def __init__(self):
        self._client = Exa(api_key=self._require_env("EXA_API_KEY"))

    def search(self, query: str, num_results: int = 5) -> List[Dict[str, Any]]:
        results = self._client.search(query, num_results=num_results)
        return [
            {"title": r.title, "url": r.url, "text": r.text}
            for r in results.results
        ]

    def search_and_contents(self, query: str, num_results: int = 5) -> List[Dict[str, Any]]:
        results = self._client.search_and_contents(query, num_results=num_results, text=True)
        return [
            {"title": r.title, "url": r.url, "text": r.text[:3000] if r.text else ""}
            for r in results.results
        ]
