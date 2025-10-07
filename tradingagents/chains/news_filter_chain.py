
import pandas as pd
import logging
from typing import Dict
from tradingagents.dataflows import akshare_utils
from tradingagents.utils.enhanced_news_filter import EnhancedNewsFilter, create_enhanced_news_filter

logger = logging.getLogger(__name__)

class NewsProcessingPipeline:
    """
    一个用于获取和过滤新闻的处理管道，借鉴了LangChain的组件化和链式思想。
    """
    def __init__(self, fetcher_function=akshare_utils.get_stock_news_em):
        """
        初始化管道。

        Args:
            fetcher_function: 用于获取原始新闻的函数。
                              默认为 akshare_utils.get_stock_news_em。
        """
        self._fetcher = fetcher_function
        self._filter_cache: Dict[str, EnhancedNewsFilter] = {}

    def _get_filter(self, symbol: str, **kwargs) -> EnhancedNewsFilter:
        """
        为指定的股票代码获取或创建一个过滤器实例。
        使用缓存避免重复加载模型。
        """
        cache_key = f"{symbol}-{kwargs.get('use_semantic', True)}-{kwargs.get('use_local_model', False)}"
        if cache_key not in self._filter_cache:
            logger.info(f"为 {symbol} 创建新的新闻过滤器实例...")
            self._filter_cache[cache_key] = create_enhanced_news_filter(
                ticker=symbol,
                use_semantic=kwargs.get('use_semantic', True),
                use_local_model=kwargs.get('use_local_model', False)
            )
        return self._filter_cache[cache_key]

    def run(
        self,
        symbol: str,
        max_news: int = 10,
        enable_filter: bool = True,
        min_score: float = 30.0,
        use_semantic: bool = True,
        use_local_model: bool = True,
    ) -> pd.DataFrame:
        """
        执行完整的新闻获取和过滤流程。

        Args:
            symbol (str): 股票代码.
            max_news (int): 要获取的最大新闻条数.
            enable_filter (bool): 是否启用过滤功能.
            min_score (float): 过滤时使用的最低相关性分数.
            use_semantic (bool): 是否在过滤时使用语义分析.
            use_local_model (bool): 是否在过滤时使用本地模型.

        Returns:
            pd.DataFrame: 处理后的新闻数据.
        """
        logger.info(f"开始为 {symbol} 执行新闻处理管道 (过滤: {'启用' if enable_filter else '禁用'})...")

        # 步骤 1: 数据获取 (Retriever step)
        try:
            news_df = self._fetcher(symbol, max_news=max_news)
            if news_df.empty:
                logger.warning(f"获取器未能为 {symbol} 获取到新闻。")
                return news_df
            logger.info(f"成功获取 {len(news_df)} 条关于 {symbol} 的原始新闻。")
        except Exception as e:
            logger.error(f"在管道的数据获取步骤中发生错误: {e}", exc_info=True)
            return pd.DataFrame()

        # 步骤 2: 过滤 (Transformer step)
        if not enable_filter:
            logger.info("过滤器被禁用，返回原始新闻。")
            return news_df

        try:
            filter_instance = self._get_filter(
                symbol,
                use_semantic=use_semantic,
                use_local_model=use_local_model
            )
            filtered_df = filter_instance.filter(news_df, min_score=min_score)
            logger.info(f"管道处理完成，返回 {len(filtered_df)} 条过滤后的新闻。")
            return filtered_df
        except Exception as e:
            logger.error(f"在管道的新闻过滤步骤中发生错误: {e}，将返回原始数据作为备用。", exc_info=True)
            return news_df


#   测试用例：
#   python -X utf8 tests/test_news_filtering.py