from pytrends.request import TrendReq
from typing import List, Dict, Any
from .base_service import BaseService


class TrendsService(BaseService):
    def __init__(self):
        self._client = TrendReq(hl='en-US', tz=360)

    def interest_over_time(self, keywords: List[str], timeframe: str = 'today 12-m') -> Dict[str, Any]:
        self._client.build_payload(keywords, timeframe=timeframe)
        trends = self._client.interest_over_time()
        if trends.empty:
            return {}
        return {
            keyword: {
                "average_interest": round(float(trends[keyword].mean()), 2),
                "latest_interest": int(trends[keyword].iloc[-1]),
                "max_interest": int(trends[keyword].max())
            }
            for keyword in keywords
        }
