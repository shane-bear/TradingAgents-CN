# tradingagents/chains/fundamentals_data_chain.py
from langchain_core.runnables import RunnableBranch, RunnableLambda, RunnablePassthrough
from tradingagents.tools.fundamentals_lcel_tools import (
    market_identifier_tool,
    get_a_share_fundamentals_optimized,
    get_hk_data_akshare_wip, get_hk_data_yahoo_wip, get_hk_data_finnhub_wip,
    get_us_data_finnhub, get_us_data_openai, get_us_data_yahoo,
    format_fundamentals_report
)
from datetime import datetime, timedelta

def create_fundamentals_data_chain():
    """
    Creates an integrated LCEL chain for fetching fundamental data,
    handling different markets and fallbacks automatically.

    The chain takes a ticker string as input and returns a formatted report string.
    """

    # Step 1: Market Identification and Context Setup
    # This initial step takes the input ticker, identifies the market,
    # and prepares all necessary date parameters.
    market_identification_step = RunnableLambda(
        lambda ticker: {
            "ticker": ticker,
            "market_info": market_identifier_tool.invoke(ticker),
            "start_date": (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d'),
            "end_date": datetime.now().strftime('%Y-%m-%d'),
            "curr_date": datetime.now().strftime('%Y-%m-%d')
        }
    ) | RunnableLambda(
        lambda x: {
            "ticker": x["ticker"],
            "market_type": x["market_info"].get("market_name", "Unknown"),
            "market_info": x["market_info"],
            "start_date": x["start_date"],
            "end_date": x["end_date"],
            "curr_date": x["curr_date"]
        }
    )

    # Step 2: Define Market-Specific Data Fetching Chains with Fallbacks
    a_share_combined_chain = get_a_share_fundamentals_optimized
    
    # HK data chain: Tries Yahoo -> Finnhub -> AKShare -> Final failure message.
    hk_data_chain = get_us_data_yahoo.with_fallbacks(
        fallbacks=[
            get_us_data_finnhub.with_fallbacks([
                get_hk_data_akshare_wip.with_fallbacks([
                    get_hk_data_yahoo_wip.with_fallbacks([
                        get_hk_data_finnhub_wip.with_fallbacks([
                            RunnableLambda(lambda x: f"⚠️ 港股 {x['ticker']} 数据获取失败。")
                        ])
                    ])
                ])
            ])
        ]
    ) | RunnableLambda(lambda x: [f"## 🇭🇰 港股数据\n{x}"])

    # US data chain: Tries Finnhub -> Yahoo -> OpenAI -> Final failure message.
    us_data_chain = get_us_data_finnhub.with_fallbacks(
        fallbacks=[
            get_us_data_yahoo.with_fallbacks([
                get_us_data_openai.with_fallbacks([
                    RunnableLambda(lambda x: f"⚠️ 美股 {x['ticker']} 数据获取失败。")
                ])
            ])
        ]
    ) | RunnableLambda(lambda x: [f"## 🇺🇸 美股数据\n{x}"])

    # Step 3: Create the Router
    # This branch directs the input to the correct market-specific chain.
    router = RunnableBranch(
        (lambda x: x["market_type"] == "中国A股", a_share_combined_chain),
        (lambda x: x["market_type"] == "港股", hk_data_chain),
        us_data_chain  # Default case for US stocks
    )

    # Step 4: Assemble the Final Chain
    # The final chain pipes all steps together:
    # 1. Identify market.
    # 2. Pass context to the router and execute the appropriate data fetching chain.
    # 3. Format the final report.
    final_chain = (
        market_identification_step
        | RunnablePassthrough.assign(results=router)
        | RunnableLambda(
            lambda x: format_fundamentals_report.invoke({
                "ticker": x["ticker"],
                "market_info": x["market_info"],
                "curr_date": x["curr_date"],
                "results": x["results"]
            })
        )
    )

    return final_chain

# Example of how to create and use the chain:
# if __name__ == '__main__':
#     # This is for testing purposes.
#     # You would typically import create_fundamentals_data_chain elsewhere.
#     fundamentals_chain = create_fundamentals_data_chain()

#     # Test with an A-share ticker
#     print("--- Testing A-Share ---")
#     a_share_report = fundamentals_chain.invoke("600519")
#     print(a_share_report)

#     # Test with a Hong Kong ticker
#     print("\n--- Testing HK Stock ---")
#     hk_stock_report = fundamentals_chain.invoke("0700.HK")
#     print(hk_stock_report)

#     # Test with a US ticker
#     print("\n--- Testing US Stock ---")
#     us_stock_report = fundamentals_chain.invoke("AAPL")
#     print(us_stock_report)
