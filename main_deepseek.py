from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG
from datetime import date


# Create a custom config
config = DEFAULT_CONFIG.copy()
config["llm_provider"] = "deepseek"  # Use a different model
#config["backend_url"] = "https://ark.cn-beijing.volces.com/api/v3/"  # Use a different backend

# config["deep_think_llm"] = "gpt-4.1-nano"  # Use a different model
# config["quick_think_llm"] = "gpt-4.1-nano"  # Use a different model


config["deep_think_llm"] = "deepseek-reasoner"  # Use a different model
config["quick_think_llm"] = "deepseek-chat"  # Use a different mode

config["max_debate_rounds"] = 1  # Increase debate rounds
config["max_risk_discuss_rounds"] = 1  # Increase debate rounds

config["online_tools"] = True  # Increase debate rounds


# Initialize with custom config
ta = TradingAgentsGraph(
    #selected_analysts=["market", "social", "news", "fundamentals"],
    selected_analysts=["fundamentals"],
    debug=True, 
    config=config
    )

# forward propagate
#_, decision = ta.propagate("0175.HK", trade_date = date.today().strftime("%Y-%m-%d"))
#_, decision = ta.propagate("NVDA", trade_date = date.today().strftime("%Y-%m-%d"))
_, decision = ta.propagate("600999", trade_date = date.today().strftime("%Y-%m-%d"))
print(decision)

# Memorize mistakes and reflect
# ta.reflect_and_remember(1000) # parameter is the position returns
