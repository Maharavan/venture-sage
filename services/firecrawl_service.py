from firecrawl import Firecrawl
from .base_service import BaseService


class FirecrawlService(BaseService):
    def __init__(self):
        self._client = Firecrawl(api_key=self._require_env("FIRECRAWL_API_KEY"))

    def scrape_and_interact(self, url: str, prompt: str) -> str:
        result = self._client.scrape(url, formats=["markdown"])
        scrape_id = result.metadata.scrape_id
        response = self._client.interact(scrape_id, prompt=prompt)
        self._client.stop_interaction(scrape_id)
        return response.output
