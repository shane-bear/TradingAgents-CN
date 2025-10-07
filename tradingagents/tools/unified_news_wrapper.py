#!/usr/bin/env python3
"""
Unified News Analysis Tool.
A simplified, tool-based wrapper for fetching news for any stock.
"""

import logging
from typing import Annotated, Optional
from langchain_core.tools import tool
from tradingagents.chains.news_data_chain import create_news_data_chain

logger = logging.getLogger(__name__)

@tool
def get_stock_news_unified(
    stock_code: Annotated[str, "The stock ticker to analyze (e.g., '600519', '0700.HK', 'AAPL')."]
) -> str:
    """
    A unified tool for fetching stock news.

    This tool automatically identifies the stock's market (A-share, HK-share, US-share),
    selects the best data sources, and uses multiple fallbacks to ensure data availability.
    """
    logger.info(f"📰 [Unified News Tool] `get_stock_news_unified` called for ticker: {stock_code}")

    if not stock_code:
        return "❌ Error: No stock code provided."

    try:
        # Create an instance of the modern, robust data fetching chain.
        news_data_chain = create_news_data_chain()

        # Invoke the chain. The chain is designed to accept a dictionary with a ticker.
        report = news_data_chain.invoke({"ticker": stock_code})

        logger.info(f"📰 [Unified News Tool] Successfully generated news report for {stock_code} via LCEL chain.")

        if not report or len(report.strip()) < 50:
             logger.warning(f"[Unified News Tool] Result for {stock_code} is unusually short or empty.")
             return f"No significant news found for {stock_code} from available sources."

        return report

    except Exception as e:
        logger.error(f"❌ [Unified News Tool] An unexpected error occurred while running the "
                     f"underlying data chain for {stock_code}: {e}", exc_info=True)
        return f"在为 {stock_code} 获取新闻数据时，统一接口发生严重错误: {e}"

if __name__ == "__main__":
    # This block allows the script to be run directly for testing.
    # To see detailed logs, set the project's log level environment variable,
    # e.g., TRADINGAGENTS_LOG_LEVEL=DEBUG python -m tradingagents.tools.unified_news_wrapper
    from tradingagents.utils.logging_manager import setup_logging
    setup_logging()

    print("--- 🚀 Testing Unified News Wrapper Tool ---")

    test_tickers = [
        "000001",    # A-share (Ping An Bank)
        "0700.HK",   # HK-share (Tencent)
        "AAPL"       # US-share (Apple)
    ]

    for ticker in test_tickers:
        print(f"\n--- 📰 Report for {ticker} ---")
        try:
            # The tool's invoke method expects a dictionary.
            report = get_stock_news_unified.invoke({"stock_code": ticker})
            print(report)
        except Exception as e:
            print(f"--- ❌ Error fetching report for {ticker}: {e} ---")

    print("\n--- ✅ Test Complete ---")
