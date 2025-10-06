# scripts/test_lcel_phase1.py
"""
This script is a standalone test to verify the successful refactoring of the
news fetching logic in Phase 1. It directly invokes the news data chain
to test its routing and data fetching capabilities for different market types.
"""
import sys
import os
import asyncio
import logging

# Ensure the project root is in the Python path to allow for correct module imports.
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import the chain creation function from the new module
from tradingagents.chains.news_data_chain import create_news_data_chain

async def run_test():
    """Asynchronously runs tests for different market stocks."""

    # Create an instance of the news data chain
    news_fetcher_graph = create_news_data_chain()

    test_cases = [
        {"market": "A-share", "input": {"ticker": "600999"}},
        {"market": "HK-share", "input": {"ticker": "0700.HK"}},
        {"market": "US-share", "input": {"ticker": "AAPL"}},
        {"market": "US-share with custom look back", "input": {"ticker": "TSLA", "look_back_days": 1}},
    ]

    print("--- Starting Phase 1 LCEL Refactoring Verification Test ---\n")

    for test in test_cases:
        market = test["market"]
        input_data = test["input"]
        ticker = input_data["ticker"]

        print(f"--- Testing {market}: {input_data} ---")
        try:
            # The graph expects a dictionary with a 'ticker' key.
            # We use ainvoke for asynchronous execution.
            result = await news_fetcher_graph.ainvoke(input_data)

            print(f"SUCCESS: News fetched for {ticker}.")
            print("--- Result Preview (first 500 characters) ---")
            # Ensure the output is encoded correctly for printing
            print(result[:500].encode('utf-8', 'ignore').decode('utf-8', 'ignore'))
            print("-------------------------------------------\n")

        except Exception as e:
            print(f"FAILED: An error occurred while fetching news for {ticker}.")
            print(f"Error details: {e}\n")
            logging.exception(f"Exception for ticker {ticker}:")


if __name__ == "__main__":
    # Setup a basic logger to see potential warnings from the tools, forcing UTF-8 encoding
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', encoding='utf-8')

    # Run the async test function
    asyncio.run(run_test())
