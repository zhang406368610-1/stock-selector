"""
综合选股策略
"""
import pandas as pd
from utils.logger import get_logger
from strategies.technical import TechnicalStrategy, MomentumStrategy
from strategies.fundamental import FundamentalStrategy

logger = get_logger(__name__)


class CombinedStrategy:
    """综合选股策略"""
    
    def __init__(self, config=None):
        self.config = config or {}
        self.technical_strategy = TechnicalStrategy(config)
        self.fundamental_strategy = FundamentalStrategy(config)
        self.momentum_strategy = MomentumStrategy(config)
        self.logger = logger
    
    def select_stocks(self, stock_data_dict, stock_info_dict=None, weights=None, top_n=20):
        """
        综合选股
        
        Args:
            stock_data_dict: {股票代码: 价格DataFrame} 字典
            stock_info_dict: {股票代码: 信息字典} 字典
            weights: 各策略权重
            top_n: 返回前N只股票
        
        Returns:
            DataFrame: 综合评分最高的股票
        """
        if weights is None:
            weights = {
                'technical': 0.4,
                'momentum': 0.3,
                'fundamental': 0.2,
                'value': 0.1
            }
        
        results = {}
        
        try:
            technical_results = self.technical_strategy.select_stocks(
                stock_data_dict, top_n=len(stock_data_dict) * 2
            )
            for _, row in technical_results.iterrows():
                symbol = row['Symbol']
                if symbol not in results:
                    results[symbol] = {}
                results[symbol]['technical'] = row['Score']
            
            momentum_results = self.momentum_strategy.select_stocks(
                stock_data_dict, top_n=len(stock_data_dict) * 2
            )
            for _, row in momentum_results.iterrows():
                symbol = row['Symbol']
                if symbol not in results:
                    results[symbol] = {}
                results[symbol]['momentum'] = row['Score']
            
            if stock_info_dict:
                fundamental_results = self.fundamental_strategy.select_stocks(
                    stock_info_dict, top_n=len(stock_info_dict) * 2
                )
                for _, row in fundamental_results.iterrows():
                    symbol = row['Symbol']
                    if symbol not in results:
                        results[symbol] = {}
                    results[symbol]['fundamental'] = row['Score']
            
            combined_results = []
            for symbol, scores in results.items():
                combined_score = 0
                
                if 'technical' in scores:
                    combined_score += scores['technical'] * weights.get('technical', 0)
                
                if 'momentum' in scores:
                    combined_score += scores['momentum'] * weights.get('momentum', 0)
                
                if 'fundamental' in scores:
                    combined_score += scores['fundamental'] * weights.get('fundamental', 0)
                
                combined_results.append({
                    'Symbol': symbol,
                    'Score': combined_score,
                    'Technical': scores.get('technical', 0),
                    'Momentum': scores.get('momentum', 0),
                    'Fundamental': scores.get('fundamental', 0),
                    'Strategy': 'Combined'
                })
            
            results_df = pd.DataFrame(combined_results)
            if results_df.empty:
                return results_df
            
            results_df = results_df.sort_values('Score', ascending=False).head(top_n)
            self.logger.info(f"综合策略选中{len(results_df)}只股票")
            
            return results_df
        
        except Exception as e:
            self.logger.error(f"综合选股失败: {e}")
            return pd.DataFrame()