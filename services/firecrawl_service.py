from firecrawl import FirecrawlApp
from .base_service import BaseService


class FirecrawlService(BaseService):
    def __init__(self):
        self._client = FirecrawlApp(api_key=self._require_env("FIRECRAWL_API_KEY"))

    def scrape_and_interact(self, url: str, prompt: str) -> str:
        result = self._client.scrape_url(url, params={"formats": ["markdown"]})
        return result.get("markdown", "")
