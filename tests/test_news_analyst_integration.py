#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试新闻分析师与统一新闻工具的集成
"""

import os
import sys
from datetime import datetime

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_news_analyst_integration():
    """测试新闻分析师与统一新闻工具的集成"""
    
    print("🚀 开始测试新闻分析师集成...")
    
    try:
        # 导入必要的模块
        from tradingagents.agents.analysts.news_analyst import create_news_analyst
        from tradingagents.tools.unified_news_wrapper import get_stock_news_unified
        print("✅ 成功导入必要模块")

        # 创建模拟LLM
        class MockLLM:
            def __init__(self):
                self.__class__.__name__ = "MockLLM"

            def bind_tools(self, tools):
                return self

            def invoke(self, messages):
                # 模拟LLM响应
                class MockResult:
                    def __init__(self):
                        self.content = "模拟的分析报告"
                        self.tool_calls = []
                return MockResult()

        llm = MockLLM()
        print("✅ 创建模拟LLM成功")

        # 创建新闻分析师 (不再需要toolkit)
        news_analyst = create_news_analyst(llm)
        print("✅ 创建新闻分析师成功")

        # ... (后续测试代码保持不变) ...

        
        # 测试不同股票
        test_stocks = [
            ("000001", "平安银行 - A股"),
            ("00700", "腾讯控股 - 港股"),
            ("AAPL", "苹果公司 - 美股")
        ]
        
        for stock_code, description in test_stocks:
            print(f"\n{'='*60}")
            print(f"🔍 测试股票: {stock_code} ({description})")
            print(f"{'='*60}")
            
            try:
                # 调用新闻分析师
                start_time = datetime.now()
                result = news_analyst({
                    "messages": [],
                    "company_of_interest": stock_code,
                    "trade_date": "2025-07-28",
                    "session_id": f"test_{stock_code}"
                })
                end_time = datetime.now()
                
                print(f"⏱️ 分析耗时: {(end_time - start_time).total_seconds():.2f}秒")
                
                # 检查结果
                if result and "messages" in result and len(result["messages"]) > 0:
                    final_message = result["messages"][-1]
                    if hasattr(final_message, 'content'):
                        report = final_message.content
                        print(f"✅ 成功获取新闻分析报告")
                        print(f"📊 报告长度: {len(report)} 字符")
                        
                        # 显示报告摘要
                        if len(report) > 300:
                            print(f"📝 报告摘要: {report[:300]}...")
                        else:
                            print(f"📝 完整报告: {report}")
                        
                        # 检查是否包含真实新闻特征
                        news_indicators = ['发布时间', '新闻标题', '文章来源', '东方财富', '业绩', '营收']
                        has_real_news = any(indicator in report for indicator in news_indicators)
                        print(f"🔍 包含真实新闻特征: {'是' if has_real_news else '否'}")
                        
                        if has_real_news:
                            print("🎉 集成测试成功！")
                        else:
                            print("⚠️ 可能需要进一步优化")
                    else:
                        print("❌ 消息内容为空")
                else:
                    print("❌ 未获取到分析结果")
                    
            except Exception as e:
                print(f"❌ 测试股票 {stock_code} 时出错: {e}")
                import traceback
                traceback.print_exc()
        
        print(f"\n{'='*60}")
        print("🎉 新闻分析师集成测试完成!")
        print(f"{'='*60}")
        
    except Exception as e:
        print(f"❌ 测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_news_analyst_integration()