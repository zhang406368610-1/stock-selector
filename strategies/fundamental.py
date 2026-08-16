"""
基本面选股策略
"""
import pandas as pd
from utils.logger import get_logger

logger = get_logger(__name__)


class FundamentalStrategy:
    """基本面选股策略类"""
    
    def __init__(self, config=None):
        """
        初始化基本面策略
        
        Args:
            config: 配置字典
        """
        self.config = config or {}
        self.logger = logger
    
    def calculate_fundamental_score(self, info):
        """
        计算基本面评分
        
        Args:
            info: 股票信息字典
        
        Returns:
            float: 评分 (0-100)
        """
        score = 0
        
        try:
            pe = info.get('trailingPE')
            if pe and 0 < pe < 50:
                if pe < 15:
                    score += 30
                elif pe < 25:
                    score += 25
                elif pe < 35:
                    score += 15
                else:
                    score += 5
            
            pb = info.get('priceToBook')
            if pb and 0 < pb < 10:
                if pb < 1.5:
                    score += 25
                elif pb < 2.5:
                    score += 20
                elif pb < 4:
                    score += 10
            
            roe = info.get('returnOnEquity')
            if roe:
                roe_pct = roe * 100
                if roe_pct > 20:
                    score += 20
                elif roe_pct > 15:
                    score += 15
                elif roe_pct > 10:
                    score += 10
            
            margin = info.get('grossMargins')
            if margin:
                margin_pct = margin * 100
                if margin_pct > 30:
                    score += 15
                elif margin_pct > 20:
                    score += 10
                elif margin_pct > 10:
                    score += 5
            
            debt_ratio = info.get('debtToEquity')
            if debt_ratio:
                if debt_ratio < 1:
                    score += 10
                elif debt_ratio < 2:
                    score += 5
        
        except Exception as e:
            self.logger.warning(f"计算基本面评分失败: {e}")
        
        return min(score, 100)
    
    def select_stocks(self, stock_info_dict, top_n=20):
        """
        根据基本面选择股票
        
        Args:
            stock_info_dict: {股票代码: 信息字典} 字典
            top_n: 返回前N只股票
        
        Returns:
            DataFrame: 选中的股票及其评分
        """
        results = []
        
        for symbol, info in stock_info_dict.items():
            try:
                if not info:
                    continue
                
                score = self.calculate_fundamental_score(info)
                price = info.get('currentPrice', 0)
                pe = info.get('trailingPE')
                pb = info.get('priceToBook')
                
                results.append({
                    'Symbol': symbol,
                    'Score': score,
                    'Price': price,
                    'PE': pe,
                    'PB': pb,
                    'Strategy': 'Fundamental'
                })
            except Exception as e:
                self.logger.debug(f"处理{symbol}时出错: {e}")
        
        results_df = pd.DataFrame(results)
        if results_df.empty:
            return results_df
        
        results_df = results_df.sort_values('Score', ascending=False).head(top_n)
        self.logger.info(f"基本面策略选中{len(results_df)}只股票")
        
        return results_df