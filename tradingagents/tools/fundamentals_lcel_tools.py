# tradingagents/tools/fundamentals_atomic_tools.py
from langchain_core.tools import tool
from typing import Optional, List, Dict, Any
import logging

# 1. Market Identification Tool
@tool
def market_identifier_tool(ticker: str) -> dict:
    """
    Identifies the market type (A-share, HK, US) and basic information for a given stock ticker.
    """
    from tradingagents.utils.stock_utils import StockUtils
    return StockUtils.get_market_info(ticker)

# 2. A-Share Data Source Tools
@tool
def get_a_share_fundamentals_optimized(ticker: str, start_date: str, end_date: str) -> List[str]:
    """
    Generates a fundamentals report for an A-share stock using OptimizedChinaDataProvider. Primary source.
    """
    logger = logging.getLogger(__name__)
    result_data = []

    logger.info(f"🇨🇳 [统一基本面工具] 处理A股数据...")
    logger.info(f"🔍 [股票代码追踪] 进入A股处理分支，ticker: '{ticker}'")

    try:
        # 获取股票价格数据
        from tradingagents.dataflows.interface import get_china_stock_data_unified
        logger.info(f"🔍 [股票代码追踪] 调用 get_china_stock_data_unified，传入参数: ticker='{ticker}', start_date='{start_date}', end_date='{end_date}'")
        stock_data = get_china_stock_data_unified(ticker, start_date, end_date)
        logger.info(f"🔍 [股票代码追踪] get_china_stock_data_unified 返回结果前200字符: {stock_data[:200] if stock_data else 'None'}")
        result_data.append(f"## A股价格数据\n{stock_data}")
    except Exception as e:
        logger.error(f"🔍 [股票代码追踪] get_china_stock_data_unified 调用失败: {e}")
        result_data.append(f"## A股价格数据\n获取失败: {e}")

    try:
        # 获取基本面数据
        from tradingagents.dataflows.optimized_china_data import OptimizedChinaDataProvider
        analyzer = OptimizedChinaDataProvider()
        logger.info(f"🔍 [股票代码追踪] 调用 OptimizedChinaDataProvider._generate_fundamentals_report，传入参数: ticker='{ticker}'")
        fundamentals_data = analyzer._generate_fundamentals_report(ticker, stock_data if 'stock_data' in locals() else "")
        logger.info(f"🔍 [股票代码追踪] _generate_fundamentals_report 返回结果前200字符: {fundamentals_data[:200] if fundamentals_data else 'None'}")
        result_data.append(f"## A股基本面数据\n{fundamentals_data}")
    except Exception as e:
        logger.error(f"🔍 [股票代码追踪] _generate_fundamentals_report 调用失败: {e}")
        result_data.append(f"## A股基本面数据\n获取失败: {e}")

    return result_data

# 3. Hong Kong Stock Data Source Tools
@tool
def get_hk_data_akshare_wip(ticker: str, start_date: str, end_date: str) -> str:
    """
    Fetches Hong Kong stock data from AKShare. This is the primary data source in original chain, in get_stock_fundamentals_unified_obsoleted()
    取出的只是一些简单的历史信息，完全谈不上基本面
    """
    from tradingagents.dataflows.akshare_utils import get_hk_stock_data_akshare
    print(f"--- Using AKShare for HK stock data of {ticker} ---")
    return get_hk_stock_data_akshare(ticker, start_date, end_date)

@tool
def get_hk_data_yahoo_wip(ticker: str, start_date: str, end_date: str) -> str:
    """
    Fetches Hong Kong stock data from Yahoo Finance. This is the first backup in original chain, in get_stock_fundamentals_unified_obsoleted()
    但是同上面 akshare 的问题一样，取的也是一些简单的历史信息，完全谈不上基本面
    """
    from tradingagents.dataflows.hk_stock_utils import get_hk_stock_data
    print(f"--- Using Yahoo Finance backup for HK stock data of {ticker} ---")
    return get_hk_stock_data(ticker, start_date, end_date)

@tool
def get_hk_data_finnhub_wip(ticker: str, start_date: str, end_date: str) -> str:
    """
    Fetches Hong Kong stock data from Finnhub. This is the second backup original chain, in get_stock_fundamentals_unified_obsoleted()
    但是同上面 akshare，yahoo 的问题一样，取的也是一些简单的历史信息，完全谈不上基本面
    而且函数里面又充满 fallback，看起来也很混乱
    """
    from tradingagents.dataflows.optimized_us_data import get_us_stock_data_cached
    print(f"--- Using Finnhub backup for HK stock data of {ticker} ---")
    return get_us_stock_data_cached(ticker, start_date, end_date)

# 4. US Stock Data Source Tools
@tool
def get_us_data_finnhub(ticker: str, curr_date: str) -> str:
    """
    Fetches US stock fundamentals data from Finnhub. This is the primary data source.
    """
    from tradingagents.dataflows.interface import get_fundamentals_finnhub
    return get_fundamentals_finnhub(ticker, curr_date)

@tool
def get_us_data_openai(ticker: str, curr_date: str) -> str:
    """
    Fetches US stock fundamentals data from OpenAI. This is a backup data source.
    """
    from tradingagents.dataflows.interface import get_fundamentals_openai
    return get_fundamentals_openai(ticker, curr_date)

@tool
def get_us_data_yahoo(ticker: str, curr_date: str, start_date: str, end_date: str) -> str:
    """
    Fetches and combines Yahoo Finance data, creating a comprehensive report with fundamentals and historical prices.
    """
    from tradingagents.dataflows.interface import get_fundamentals_yahoo
    from tradingagents.dataflows.hk_stock_utils import get_hk_stock_data

    # 1. Fetch fundamentals and price data
    fundamentals_report = get_fundamentals_yahoo(ticker, curr_date)

    price_report = get_hk_stock_data(ticker, start_date, end_date)

    #2. Combine reports with structured headers
    combined_report = (
        f"# Comprehensive Yahoo Finance Report for {ticker}\n\n"
        f"## Fundamental Analysis\n\n"
        f"{fundamentals_report}\n\n"
        f"## Historical Price Data\n\n"
        f"{price_report}"
    )
    return combined_report

# 5. Universal Report Formatting Tool
@tool
def format_fundamentals_report(
    ticker: str, market_info: Dict[str, Any], curr_date: str, results: List[str]
) -> str:
    """
    Integrates and formats the final fundamentals analysis report from various data pieces.
    """
    combined_result = f"""# {ticker} 基本面分析报告

**市场类型**: {market_info.get('market_name', '未知')}
**交易货币**: {market_info.get('currency_name', '未知')} ({market_info.get('currency_symbol', '')})
**报告日期**: {curr_date}

{chr(10).join(results)}

---
*数据来源: 带 fallback 机制的多数据源链*

"""
    return combined_result
