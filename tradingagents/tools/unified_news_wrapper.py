#!/usr/bin/env python3
"""
Unified News Analysis Tool.
Integrates news fetching logic for different markets (A-shares, HK stocks, US stocks)
into a single tool, allowing the language model to call just one tool to get news
for all types of stocks.
"""

import logging
from datetime import datetime
from tradingagents.chains.news_data_chain import create_news_data_chain

logger = logging.getLogger(__name__)

class UnifiedNewsAnalyzer:
    """
    A unified news analyzer that integrates all news fetching logic.
    This class is now a lightweight wrapper around the LCEL-based news_fetcher_graph.
    """

    def __init__(self, toolkit):
        """
        Initializes the unified news analyzer.

        Args:
            toolkit: A toolkit containing various news fetching tools. This is kept for
                     compatibility but the new implementation primarily uses the LCEL graph.
        """
        self.toolkit = toolkit
        self.news_fetcher_graph = create_news_data_chain()

    def get_stock_news_unified(self, stock_code: str, max_news: int = 10, model_info: str = "") -> str:
        """
        Unified news fetching interface.
        Invokes the LCEL graph to automatically identify stock type and fetch news.

        Args:
            stock_code: The stock code.
            max_news: The maximum number of news articles (currently not used by the LCEL graph).
            model_info: Information about the current model, for special handling.

        Returns:
            str: Formatted news content.
        """
        logger.info(f"[Unified News Tool] Fetching news for {stock_code} using LCEL graph, model: {model_info}")

        try:
            # Invoke the LCEL graph with the stock code.
            # The graph expects a dictionary with a "ticker" key.
            result = self.news_fetcher_graph.invoke({"ticker": stock_code})

            logger.info(f"[Unified News Tool] LCEL graph execution successful. Result length: {len(result)} chars")
            logger.debug(f"[Unified News Tool] Result preview (first 1000 chars): {result[:1000]}")

            if not result or len(result.strip()) < 50:
                logger.warning("[Unified News Tool] Result is unusually short or empty.")
                return f"No significant news found for {stock_code} from available sources."

            return self._format_news_result(result, "LCEL News Graph", model_info)

        except Exception as e:
            logger.error(f"[Unified News Tool] Error executing LCEL news graph for {stock_code}: {e}", exc_info=True)
            return f"❌ Failed to fetch news for {stock_code} due to an internal error: {e}"

    def _format_news_result(self, news_content: str, source: str, model_info: str = "") -> str:
        """Formats the news result."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # This formatting can be further simplified or customized as needed.
        formatted_result = f"""
=== 📰 News Data Source: {source} ===
Fetch Time: {timestamp}
Data Length: {len(news_content)} chars
Model Info: {model_info if model_info else "N/A"}

=== 📋 News Content ===
{news_content}

=== ✅ Data Status ===
Status: Successfully fetched
Timestamp: {timestamp}
"""
        return formatted_result.strip()


def create_unified_news_tool(toolkit):
    """Creates the unified news tool function."""
    analyzer = UnifiedNewsAnalyzer(toolkit)

    def get_stock_news_unified(stock_code: str, max_news: int = 100, model_info: str = ""):
        """
        A unified tool to fetch news for a stock.

        Args:
            stock_code (str): The stock code (e.g., '000001' for A-shares, '0700.HK' for HK stocks, 'AAPL' for US stocks).
            max_news (int): The maximum number of news articles to return.
            model_info (str): Information on the current model for special handling.

        Returns:
            str: Formatted news content.
        """
        if not stock_code:
            return "❌ Error: No stock code provided."

        return analyzer.get_stock_news_unified(stock_code, max_news, model_info)

    get_stock_news_unified.name = "get_stock_news_unified"
    get_stock_news_unified.description = """
A unified news fetching tool that automatically retrieves news for the relevant market based on the stock code.
- Automatically identifies the stock type (A-share/HK-share/US-share).
- Selects the best news source based on the stock type.
- Uses a robust, fallback-enabled system to ensure high availability.
- Returns formatted news content.
"""

    return get_stock_news_unified
