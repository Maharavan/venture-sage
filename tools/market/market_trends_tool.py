from pytrends.request import TrendReq
from strands import tool
import pandas as pd
from typing import List,Dict

@tool
def get_market_trends(keywords:List[str], timeframe='today 12-m') -> Dict:
    """Fetch market trends for the given keywords and timeframe."""
    
    try:
        pytrends = TrendReq(hl='en-US', tz=360)
        trends: pd.DataFrame = pytrends.build_payload(keywords, timeframe=timeframe)
        trends = pytrends.interest_over_time()
        if trends.empty:
            return {
                "status": "No data",
                "keywords": keywords,
            }
        result = {}
        for keyword in keywords:
            result[keyword] = {
                "average_interest": round(float(trends[keyword].mean()), 2),
                "latest_interest": int(trends[keyword].iloc[-1]),
                "max_interest": int(trends[keyword].max())
            }

        return result
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }