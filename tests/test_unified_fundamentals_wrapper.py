
import unittest
from unittest.mock import patch, MagicMock
import logging

# Configure logging to capture output for tests
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Ensure the logger for the wrapper is available
logger = logging.getLogger('tradingagents.tools.unified_fundamentals_wrapper')


class TestUnifiedFundamentalsWrapper(unittest.TestCase):

    @patch('tradingagents.tools.unified_fundamentals_wrapper.create_fundamentals_data_chain')
    def test_successful_invocation(self, mock_create_chain):
        """
        Tests a successful call to the unified fundamentals tool wrapper.
        """
        print("\\n--- Running Test: test_successful_invocation ---")

        # Arrange: Configure the mock chain to return a successful report
        mock_chain_instance = MagicMock()
        mock_chain_instance.invoke.return_value = "## 📈 AAPL 基本面分析报告\\n- **数据来源**: 模拟数据源\\n- **分析**: 模拟分析内容"
        mock_create_chain.return_value = mock_chain_instance

        # Dynamically import the tool after setting up mocks if needed, or ensure it's loaded correctly
        from tradingagents.tools.unified_fundamentals_wrapper import get_stock_fundamentals_unified

        # Act: Call the tool's invoke method
        ticker_to_test = "AAPL"
        result = get_stock_fundamentals_unified.invoke({"ticker": ticker_to_test})

        # Assert: Verify the behavior
        # 1. Check that the chain creator was called
        mock_create_chain.assert_called_once()

        # 2. Check that the chain's invoke method was called with the correct ticker
        mock_chain_instance.invoke.assert_called_once_with(ticker_to_test)

        # 3. Check that the result is the expected report
        self.assertIn("AAPL 基本面分析报告", result)
        self.assertIn("模拟分析内容", result)

        print(f"✅ Test Passed: Successfully invoked wrapper for {ticker_to_test} and got expected report.")

    @patch('tradingagents.tools.unified_fundamentals_wrapper.create_fundamentals_data_chain')
    def test_invocation_with_exception(self, mock_create_chain):
        """
        Tests how the wrapper handles an exception from the underlying LCEL chain.
        """
        print("\\n--- Running Test: test_invocation_with_exception ---")

        # Arrange: Configure the mock chain to raise an exception
        mock_chain_instance = MagicMock()
        mock_chain_instance.invoke.side_effect = ValueError("LCEL chain execution failed")
        mock_create_chain.return_value = mock_chain_instance

        from tradingagents.tools.unified_fundamentals_wrapper import get_stock_fundamentals_unified

        # Act: Call the tool's invoke method, expecting an error
        ticker_to_test = "FAIL.TICKER"
        result = get_stock_fundamentals_unified.invoke({"ticker": ticker_to_test})

        # Assert: Verify the error handling
        # 1. Check that the chain creator was called
        mock_create_chain.assert_called_once()

        # 2. Check that the chain's invoke method was called
        mock_chain_instance.invoke.assert_called_once_with(ticker_to_test)

        # 3. Check that the result is a user-friendly error message
        self.assertIn(f"在为 {ticker_to_test} 获取基本面数据时，统一接口发生严重错误", result)
        self.assertIn("LCEL chain execution failed", result)

        print(f"✅ Test Passed: Correctly handled exception for {ticker_to_test}.")

    @patch('tradingagents.tools.unified_fundamentals_wrapper.create_fundamentals_data_chain')
    def test_tool_with_a_share_ticker(self, mock_create_chain):
        """
        Tests the wrapper with a sample A-share ticker.
        """
        print("\\n--- Running Test: test_tool_with_a_share_ticker ---")

        # Arrange
        mock_chain_instance = MagicMock()
        mock_chain_instance.invoke.return_value = "Mock A-Share Report"
        mock_create_chain.return_value = mock_chain_instance

        from tradingagents.tools.unified_fundamentals_wrapper import get_stock_fundamentals_unified

        # Act
        ticker_to_test = "600519"
        result = get_stock_fundamentals_unified.invoke({"ticker": ticker_to_test})

        # Assert
        mock_chain_instance.invoke.assert_called_once_with(ticker_to_test)
        self.assertEqual(result, "Mock A-Share Report")

        print(f"✅ Test Passed: Wrapper correctly handled A-share ticker {ticker_to_test}.")


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
