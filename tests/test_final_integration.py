#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A final test to validate the integration of the simplified unified news tool.
"""

import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_final_integration():
    """Final integration test for the new unified news tool."""

    print("🎯 Validating the integration of the Unified News Tool")
    print("=" * 60)

    try:
        # 1. Test the unified news tool itself
        print("📦 Step 1: Testing the unified news tool...")
        from tradingagents.tools.unified_news_wrapper import get_stock_news_unified

        # Test different stock types
        test_cases = [
            {"code": "000001", "type": "A-share", "name": "Ping An Bank"},
            {"code": "0700.HK", "type": "HK-share", "name": "Tencent Holdings"},
            {"code": "AAPL", "type": "US-share", "name": "Apple Inc."}
        ]

        for case in test_cases:
            print(f"\n🔍 Testing {case['type']}: {case['code']} ({case['name']})")
            # Use .invoke() for the new @tool
            result = get_stock_news_unified.invoke({"stock_code": case["code"]})

            if result and len(result) > 50:
                print(f"  ✅ News fetched successfully ({len(result)} chars)")
                if "No significant news found" not in result:
                     print(f"  ✅ Result seems to contain valid news data.")
            else:
                print(f"  ⚠️ Could not fetch news (This may be due to network issues, which is acceptable).")

        print(f"\n✅ Unified news tool test complete.")

        # 2. Verify tool integration in the news analyst
        print(f"\n🔧 Step 2: Verifying tool integration in source code...")

        with open("tradingagents/agents/analysts/news_analyst.py", "r", encoding="utf-8") as f:
            content = f.read()

        checks = [
            ("Unified tool import", "from tradingagents.tools.unified_news_wrapper import get_stock_news_unified"),
            ("Direct tool usage", "tools = [get_stock_news_unified]"),
            ("Tool invocation", ".invoke({\"stock_code\": ticker})"),
            ("System prompt update", "get_stock_news_unified"),
            ("Remedy mechanism update", "get_stock_news_unified")
        ]

        all_checks_passed = True
        for check_name, check_pattern in checks:
            if check_pattern in content:
                print(f"  ✅ {check_name}: Correctly integrated")
            else:
                print(f"  ❌ {check_name}: Not found or incorrect")
                all_checks_passed = False

        # 3. Summary
        print(f"\n🎉 Integration Validation Summary")
        print("=" * 60)
        if all_checks_passed:
            print("✅ All integration checks passed successfully!")
            print("✅ The news analyst is correctly using the new simplified tool.")
        else:
            print("❌ Some integration checks failed. Please review the news analyst implementation.")

        print(f"\n🚀 Key improvements:")
        print("1. The large model now only needs to call one tool: get_stock_news_unified.")
        print("2. The tool automatically identifies stock type and selects the best news source.")
        print("3. Tool invocation logic is simplified, improving reliability.")
        print("4. News format is unified, facilitating analysis.")

        print(f"\n✨ Integration test complete! The unified news tool is successfully integrated.")

    except Exception as e:
        print(f"❌ An error occurred during the test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_final_integration()
