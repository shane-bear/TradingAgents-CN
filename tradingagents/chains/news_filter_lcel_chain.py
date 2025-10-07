#!/usr/bin/env python3
"""
A LangChain component factory for news processing.

This module provides independent, composable LCEL Runnables (building blocks)
for fetching and filtering news, allowing for flexible chain construction.
"""

import asyncio
import pandas as pd
import logging
from typing import Dict, Any

from langchain_core.runnables import RunnableSerializable, RunnableConfig, RunnableLambda
from pydantic.v1 import BaseModel, Field

from tradingagents.dataflows import akshare_utils
from tradingagents.utils.enhanced_news_filter import EnhancedNewsFilter, create_enhanced_news_filter
from tradingagents.utils.news_filter import create_news_filter

logger = logging.getLogger(__name__)

# --- Input Schema ---
class NewsFilterInput(BaseModel):
    """Input schema for the news processing runnables."""
    symbol: str = Field(..., description="The stock ticker symbol.")
    max_news: int = Field(10, description="The maximum number of news articles to fetch.")
    min_score: float = Field(30.0, description="The minimum relevance score for filtering.")
    # Parameters for the enhanced filter
    use_semantic: bool = Field(True, description="Whether to use semantic analysis in the enhanced filter.")
    use_local_model: bool = Field(True, description="Whether to use a local model in the enhanced filter.")

# --- Runnable Building Blocks ---

# Block 1: The News Fetcher
# Takes an input dictionary and adds the raw news DataFrame to it.
fetcher_runnable = RunnableLambda(
    lambda x: {
        **x,
        "raw_news_df": akshare_utils.get_stock_news_em(x['symbol'], max_news=x['max_news'])
    },
    name="NewsFetcher"
)

# Block 2: The Simple Filter (NewsRelevanceFilter)
# Takes the output from the fetcher and applies the simple filter.
simple_filter_runnable = RunnableLambda(
    lambda x: create_news_filter(x['symbol']).filter_news(
        x['raw_news_df'], min_score=x['min_score']
    ) if not x['raw_news_df'].empty else pd.DataFrame(),
    name="SimpleRelevanceFilter"
)

# Block 3: The Enhanced Filter (Stateful Runnable)
class EnhancedNewsFilterRunnable(RunnableSerializable):
    """A stateful Runnable to cache and apply the EnhancedNewsFilter."""
    _filter_cache: Dict[str, EnhancedNewsFilter] = {}

    def _get_filter(self, config: Dict[str, Any]) -> EnhancedNewsFilter:
        symbol = config['symbol']
        use_semantic = config.get('use_semantic', True)
        use_local_model = config.get('use_local_model', True)
        cache_key = f"{symbol}-enhanced-{use_semantic}-{use_local_model}"
        if cache_key not in self._filter_cache:
            logger.info(f"Creating new EnhancedNewsFilter for {symbol}")
            self._filter_cache[cache_key] = create_enhanced_news_filter(ticker=symbol, use_semantic=use_semantic, use_local_model=use_local_model)
        return self._filter_cache[cache_key]

    def invoke(self, input: Dict[str, Any], config: RunnableConfig | None = None) -> pd.DataFrame:
        news_df = input['raw_news_df']
        if news_df.empty:
            return news_df
        filter_instance = self._get_filter(input)
        return filter_instance.filter(news_df, min_score=input['min_score'])

enhanced_filter_runnable = EnhancedNewsFilterRunnable(name="EnhancedNewsFilter")


# --- Example of how to compose these blocks ---
async def main():
    """Demonstrates how to flexibly compose chains with the exported runnables."""
    from tradingagents.utils.logging_manager import setup_logging
    # Use the detailed logging configuration from test_news_filtering.py as a reference
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

    print("--- 🚀 Demonstrating Flexible LCEL Chain Composition ---")

    # --- Composition 1: Chain with Simple Filter ---
    print("\n--- 🔗 1. Building and testing chain with SIMPLE filter ---")
    simple_chain = fetcher_runnable | simple_filter_runnable
    simple_chain = simple_chain.with_types(input_type=NewsFilterInput) # Add types for validation

    try:
        input_data = {"symbol": "600036", "max_news": 20, "min_score": 30}
        report = await simple_chain.ainvoke(input_data)
        print(f"✅ Simple chain returned: {len(report)} articles.")
    except Exception as e:
        print(f"--- ❌ Error: {e} ---")


    # --- Composition 2: Chain with Enhanced Filter ---
    print("\n--- 🔗 2. Building and testing chain with ENHANCED filter ---")
    enhanced_chain = fetcher_runnable | enhanced_filter_runnable
    enhanced_chain = enhanced_chain.with_types(input_type=NewsFilterInput)

    try:
        input_data = {"symbol": "600519", "max_news": 20, "min_score": 40}
        report = await enhanced_chain.ainvoke(input_data)
        print(f"✅ Enhanced chain returned: {len(report)} articles.")
    except Exception as e:
        print(f"--- ❌ Error: {e} ---")


    # --- Composition 3: Chain with NO Filter (just fetching) ---
    print("\n--- 🔗 3. Building and testing chain with NO filter ---")
    # You can get the raw DataFrame by selecting it from the fetcher's output
    no_filter_chain = fetcher_runnable | (lambda x: x['raw_news_df'])
    no_filter_chain = no_filter_chain.with_types(input_type=NewsFilterInput)

    try:
        input_data = {"symbol": "000001", "max_news": 5}
        report = await no_filter_chain.ainvoke(input_data)
        print(f"✅ No-filter chain returned: {len(report)} articles.")
        assert len(report) > 0
    except Exception as e:
        print(f"--- ❌ Error: {e} ---")

    print("\n--- ✅ Test Complete ---")


if __name__ == '__main__':
    # To run this test:
    # python -X utf8 -m tradingagents.chains.news_filter_lcel_chain
    asyncio.run(main())
