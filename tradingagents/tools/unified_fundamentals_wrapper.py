# tradingagents/tools/unified_wrapper.py
from langchain_core.tools import tool
from typing import Annotated, Optional
from tradingagents.chains.fundamentals_data_chain import create_fundamentals_data_chain
import logging

logger = logging.getLogger(__name__)

@tool
def get_stock_fundamentals_unified(
    ticker: Annotated[str, "The stock ticker to analyze (e.g., '600519', '0700.HK', 'AAPL')."],
    start_date: Annotated[Optional[str], "The start date for data fetching (YYYY-MM-DD). Defaults to one year ago."] = None,
    end_date: Annotated[Optional[str], "The end date for data fetching (YYYY-MM-DD). Defaults to today."] = None,
    curr_date: Annotated[Optional[str], "The current date for the analysis (YYYY-MM-DD). Defaults to today."] = None
) -> str:
    """
    A unified tool for fetching stock fundamental data that is backward-compatible with the original interface.

    This tool serves as a simple wrapper around the more complex, modern LCEL chain.
    It automatically identifies the stock's market, selects the best data sources,
    and uses multiple fallbacks to ensure data availability.

    Note: The date parameters (start_date, end_date, curr_date) are accepted for compatibility
    but the underlying chain may override them with its own default logic for consistency.
    """
    logger.info(f"📦 [Unified Wrapper] `get_stock_fundamentals_unified` called for ticker: {ticker}")
    logger.warning("📦 [Unified Wrapper] This tool is a backward-compatibility layer. "
                   "For new implementations, consider using the Fundamentals Analyst Agent directly.")

    try:
        # Create an instance of the modern, robust data fetching chain.
        fundamentals_data_chain = create_fundamentals_data_chain()

        # Invoke the chain. The chain is designed to accept a ticker string as its primary input.
        # The internal logic of the chain handles date calculations.
        report = fundamentals_data_chain.invoke(ticker)

        logger.info(f"📦 [Unified Wrapper] Successfully generated report for {ticker} via LCEL chain.")
        return report

    except Exception as e:
        logger.error(f"❌ [Unified Wrapper] An unexpected error occurred while running the "
                     f"underlying data chain for {ticker}: {e}", exc_info=True)
        return f"在为 {ticker} 获取基本面数据时，统一接口发生严重错误: {e}"

# Example of how this wrapper can be used directly:
# if __name__ == '__main__':
#     logging.basicConfig(level=logging.INFO)
#
#     print("--- Testing Unified Wrapper Tool ---")
#
#     # The call signature is the same as the old function.
#     report = get_stock_fundamentals_unified.invoke({"ticker": "AAPL"})
#
#     print("\n--- Report for AAPL ---")
#     print(report)
