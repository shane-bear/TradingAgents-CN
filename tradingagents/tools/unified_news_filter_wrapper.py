#!/usr/bin/env python3
"""
Unified News Filter Tool.
A simplified, tool-based wrapper for the enhanced news filtering LCEL chain.
"""

import logging
from typing import Annotated
from langchain_core.tools import tool
import pandas as pd

# Import the composable runnables from the LCEL chain factory
from tradingagents.chains.news_filter_lcel_chain import fetcher_runnable, enhanced_filter_runnable

logger = logging.getLogger(__name__)

@tool
def get_filtered_stock_news(
    symbol: Annotated[str, "The stock ticker symbol for an A-share stock, e.g., '600519', '000001'."],
    max_news: Annotated[int, "The maximum number of news articles to fetch before filtering."] = 20,
    min_score: Annotated[float, "The minimum relevance score (0-100) for news to be included."] = 40.0,
    use_semantic: Annotated[bool, "Whether to use semantic analysis in the enhanced filter."] = True,
    use_local_model: Annotated[bool, "Whether to use a local model in the enhanced filter."] = True,
) -> str:
    """
    Fetches, filters, and analyzes news for a given Chinese A-share stock using an
    enhanced, AI-powered relevance filter. It identifies the most impactful news
    by analyzing relevance, sentiment, and semantic content, returning a concise
    report of the most important articles. This tool is specifically optimized for A-shares.
    """
    logger.info(f"📰 [Filtered News Tool] `get_filtered_stock_news` called for symbol: {symbol}")

    try:
        # Step 1: Compose the chain from the imported building blocks.
        # This mirrors the logic from the second test case in the source file.
        enhanced_chain = fetcher_runnable | enhanced_filter_runnable

        # Step 2: Prepare the input for the chain.
        input_data = {
            "symbol": symbol,
            "max_news": max_news,
            "min_score": min_score,
            "use_semantic": use_semantic,
            "use_local_model": use_local_model
        }

        # Step 3: Invoke the chain synchronously.
        # The chain will fetch news and then pass it to the enhanced filter.
        filtered_df = enhanced_chain.invoke(input_data)

        # Step 4: Format the output for the LLM.
        if not isinstance(filtered_df, pd.DataFrame) or filtered_df.empty:
            logger.warning(f"📰 [Filtered News Tool] No news found or returned for {symbol} after filtering.")
            return f"No relevant news found for {symbol} with the specified criteria."

        logger.info(f"📰 [Filtered News Tool] Successfully filtered {len(filtered_df)} news articles for {symbol}.")

        # Convert the DataFrame to a more readable markdown format.
        report = f"# Enhanced News Analysis Report for {symbol}\n\n"
        report += filtered_df.to_markdown(index=False)

        return report

    except Exception as e:
        logger.error(f"❌ [Filtered News Tool] An unexpected error occurred for symbol {symbol}: {e}", exc_info=True)
        return f"An error occurred while fetching or filtering news for {symbol}: {e}"

# --- Example Usage ---
if __name__ == '__main__':
    import asyncio
    from tradingagents.utils.logging_manager import setup_logging

    # Setup detailed logging to observe the chain's execution
    log_config = {
        'level': 'DEBUG',
        'handlers': {
            'console': {'enabled': True, 'level': 'DEBUG', 'colored': True},
            'file': {'enabled': False},
            'structured': {'enabled': False}
        },
        'format': {
             'console': '%(asctime)s | %(name)-40s | %(levelname)-8s | %(message)s'
        },
        'loggers': {
            'tradingagents': {'level': 'DEBUG'},
            '__main__': {'level': 'DEBUG'},
            'urllib3': {'level': 'WARNING'},
        },
        'docker': {'enabled': False}
    }
    setup_logging(log_config)

    print("--- 🚀 Testing Unified News Filter Wrapper Tool ---")

    # Test case mirrors the one from news_filter_lcel_chain.py
    test_symbol = "600519"  # 贵州茅台
    print(f"\n--- 📰 Report for {test_symbol} ---")
    try:
        # The @tool decorator's invoke method expects a dictionary.
        report = get_filtered_stock_news.invoke({"symbol": test_symbol})
        print(report)
    except Exception as e:
        print(f"--- ❌ Error fetching report for {test_symbol}: {e} ---")

    print("\n--- ✅ Test Complete ---")
