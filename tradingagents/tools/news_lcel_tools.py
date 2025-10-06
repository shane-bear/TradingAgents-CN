# tradingagents/tools/news_lcel_tools.py
"""
This module defines LangChain Expression Language (LCEL) compatible tools for fetching news.

Each function is wrapped with the `@tool` decorator, making it a standardized,
composable component that can be used in LangChain chains and agents. These tools
encapsulate the logic for fetching news from various data sources.
"""

from langchain_core.tools import tool
from typing import Annotated
from datetime import datetime

# Import the underlying data fetching functions from the dataflows module.
# Using 'fetch_' prefix to distinguish from the tool functions.
from tradingagents.dataflows.interface import (
    get_finnhub_news as fetch_finnhub_news,
    get_google_news as fetch_google_news,
    get_stock_news_openai as fetch_stock_news_openai,
    get_global_news_openai as fetch_global_news_openai,
)
from tradingagents.dataflows.realtime_news_utils import (
    get_realtime_stock_news as fetch_realtime_stock_news,
)


@tool
def finnhub_news_tool(
    ticker: Annotated[str, "The ticker symbol for the company, e.g., 'AAPL', 'TSM'."],
    look_back_days: Annotated[int, "How many days to look back for news."] = 7,
) -> str:
    """
    Fetches company-specific news from Finnhub. Best for US stocks.
    It may return an error message if data is not available locally.
    """
    curr_date = datetime.now().strftime("%Y-%m-%d")
    return fetch_finnhub_news(ticker=ticker, curr_date=curr_date, look_back_days=look_back_days)


@tool
def google_news_tool(
    ticker: Annotated[str, "The ticker symbol for the company, which will be used as the search query."],
    look_back_days: Annotated[int, "How many days to look back for news."] = 7,
) -> str:
    """
    Fetches news from Google News based on a ticker.
    This is a reliable source for all market types but may have some delay.
    """
    curr_date = datetime.now().strftime("%Y-%m-%d")
    return fetch_google_news(query=ticker, curr_date=curr_date, look_back_days=look_back_days)


@tool
def realtime_news_tool(
    ticker: Annotated[str, "The ticker symbol of the stock."],
    hours_back: Annotated[int, "How many hours to look back for real-time news."] = 6,
) -> str:
    """
    Fetches real-time news from a variety of aggregated sources.
    This tool is particularly effective for Chinese A-shares as it prioritizes
    sources like East Money (东方财富). It should be the first choice for A-share news.
    """
    curr_date = datetime.now().strftime("%Y-%m-%d")
    return fetch_realtime_stock_news(ticker=ticker, curr_date=curr_date, hours_back=hours_back)


@tool
def stock_news_openai_tool(
    ticker: Annotated[str, "The ticker symbol of the stock."]
) -> str:
    """
    Uses an OpenAI model with web search capabilities to find recent news and discussions
    on social media about a specific stock.
    """
    curr_date = datetime.now().strftime("%Y-%m-%d")
    return fetch_stock_news_openai(ticker=ticker, curr_date=curr_date)


@tool
def global_news_openai_tool() -> str:
    """
    Uses an OpenAI model with web search capabilities to find global and macroeconomic news
    that is relevant for trading purposes. This tool is not specific to any single stock.
    """
    curr_date = datetime.now().strftime("%Y-%m-%d")
    return fetch_global_news_openai(curr_date=curr_date)
