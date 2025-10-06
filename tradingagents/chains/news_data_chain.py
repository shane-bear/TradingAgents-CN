# tradingagents/chains/news_data_chain.py
"""
This module creates the LangChain Expression Language (LCEL) chain for fetching news.
It abstracts the logic of routing and fallbacks into a single, composable chain.
"""
import re
from langchain_core.runnables import RunnableBranch, RunnablePassthrough
from tradingagents.tools.news_lcel_tools import (
    realtime_news_tool,
    google_news_tool,
    global_news_openai_tool,
    finnhub_news_tool
)

def _identify_stock_type(stock_code: str) -> str:
    """Identifies the stock type (A-share, HK, US) from its code."""
    stock_code = stock_code.upper().strip()

    # A-share patterns
    if re.match(r'^(00|30|60|68)\d{4}$', stock_code) or re.match(r'^(SZ|SH)\d{6}$', stock_code):
        return "A-share"
    # HK-share patterns
    elif re.match(r'^\d{4,5}\.HK$', stock_code) or (re.match(r'^\d{4,5}$', stock_code) and len(stock_code) <= 5):
        return "HK-share"
    # US-share patterns (default)
    else:
        return "US-share"

def create_news_data_chain():
    """
    Creates an integrated LCEL chain for fetching news, handling different
    markets and fallbacks automatically.

    The chain takes a dictionary which must contain a "ticker" key, and can
    optionally contain "hours_back" and "look_back_days". It returns a
    string containing the fetched news.
    """
    # Step 1: Define Market-Specific Data Fetching Chains
    # For A-shares: Priority is Realtime -> Google -> OpenAI Global
    a_share_chain = realtime_news_tool.with_fallbacks(
        fallbacks=[google_news_tool, global_news_openai_tool]
    )

    # For HK-shares: Priority is Google -> OpenAI Global -> Realtime
    hk_share_chain = google_news_tool.with_fallbacks(
        fallbacks=[global_news_openai_tool, realtime_news_tool]
    )

    # For US-shares: Priority is OpenAI Global -> Google -> Finnhub
    us_share_chain = global_news_openai_tool.with_fallbacks(
        fallbacks=[google_news_tool, finnhub_news_tool]
    )

    # Step 2: Create the Router
    # This branch directs the input to the correct market-specific chain.
    news_router = RunnableBranch(
        (lambda x: _identify_stock_type(x['ticker']) == "A-share", a_share_chain),
        (lambda x: _identify_stock_type(x['ticker']) == "HK-share", hk_share_chain),
        us_share_chain,  # Default case for US shares
    )

    # Step 3: Prepare the Input
    # This runnable ensures that default values for optional parameters are set.
    # It takes the input dictionary, adds defaults if keys are missing, and
    # passes the completed dictionary to the router. LangChain automatically
    # maps the dictionary keys to the arguments of the invoked tool.
    prepare_input = RunnablePassthrough.assign(
        hours_back=lambda x: x.get("hours_back", 6),
        look_back_days=lambda x: x.get("look_back_days", 7)
    )

    # Step 4: Assemble the Final Chain
    final_chain = prepare_input | news_router

    return final_chain
