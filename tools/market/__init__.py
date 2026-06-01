from .market_news_tools import get_market_news
from .market_discussion_tool import get_market_discussion
from .market_trends_tool import get_market_trends

MARKET_TOOLS = [
    get_market_news,
    get_market_discussion,
    get_market_trends
]
__all__ = [
    MARKET_TOOLS
]