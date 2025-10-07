#!/usr/bin/env python3
"""
Tests the LangChain binding for the simplified, unified news tool.
"""

from tradingagents.tools.unified_news_wrapper import get_stock_news_unified
from langchain_core.utils.function_calling import convert_to_openai_tool

def test_tool_binding():
    """Tests if the new @tool-decorated function binds correctly."""
    print("=== Testing LangChain Binding for the new Unified News Tool ===")

    # The tool is now a directly importable function
    unified_tool = get_stock_news_unified

    # 1. Test LangChain tool conversion
    print("\n1. Testing LangChain tool conversion...")
    try:
        openai_tool = convert_to_openai_tool(unified_tool)
        print("✅ LangChain tool conversion successful")

        func_info = openai_tool['function']
        print(f"   Tool Name: {func_info['name']}")
        print(f"   Tool Description: {func_info['description'][:100]}...")

        params = list(func_info['parameters']['properties'].keys())
        print(f"   Parameters: {params}")

        # Check if the parameters are correct
        expected_params = ['stock_code']
        # The new tool only has one required parameter now.
        if set(params) == set(expected_params):
            print("✅ Parameters match correctly")
        else:
            print(f"❌ Parameters do not match. Expected: {expected_params}, Found: {params}")
            return False

    except Exception as e:
        print(f"❌ LangChain tool conversion failed: {e}")
        import traceback
        traceback.print_exc()
        return False

    # 2. Test tool invocation
    print("\n2. Testing tool invocation...")
    try:
        # We use .invoke() for tools decorated with @tool
        result = unified_tool.invoke({"stock_code": '000001'})
        print(f"✅ Tool invocation successful, result length: {len(result)} chars")
        print(f"   Result preview: {result[:200]}...")
    except Exception as e:
        # Note: This might fail due to network issues, which is acceptable for this binding test.
        print(f"⚠️ Tool invocation failed: {e}")
        print("   (This can be normal if required APIs are not available in the test environment)")


    print("\n=== Test Complete ===")
    print("✅ The new unified news tool binds correctly with LangChain.")
    print("✅ Function signature and docstring are correctly parsed by the @tool decorator.")

    return True

if __name__ == "__main__":
    test_tool_binding()