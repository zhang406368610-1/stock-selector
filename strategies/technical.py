"""
技术面选股策略
"""
import pandas as pd
from utils.logger import get_logger

logger = get_logger(__name__)


class TechnicalStrategy:
    """技术面选股策略类"""
    
    def __init__(self, config=None):
        """
        初始化技术面策略
        
        Args:
            config: 配置字典
        """
        self.config = config or {}
        self.logger = logger
    
    def calculate_technical_score(self, df):
        """
        计算技术面评分
        
        Args:
            df: 包含技术指标的DataFrame
        
        Returns:
            float: 评分 (0-100)
        """
        score = 0
        
        try:
            if 'MA20' in df.columns and 'MA60' in df.columns:
                latest_close = df['Close'].iloc[-1]
                latest_ma20 = df['MA20'].iloc[-1]
                latest_ma60 = df['MA60'].iloc[-1]
                
                if latest_close > latest_ma20 > latest_ma60:
                    score += 30
                elif latest_close > latest_ma20:
                    score += 15
                elif latest_close > latest_ma60:
                    score += 10
            
            if 'RSI14' in df.columns:
                rsi = df['RSI14'].iloc[-1]
                if 30 < rsi < 70:
                    score += 15
                if rsi < 30:
                    score += 20
                if 40 < rsi < 60:
                    score += 10
            
            if 'MACD' in df.columns and 'Signal' in df.columns:
                macd = df['MACD'].iloc[-1]
                signal = df['Signal'].iloc[-1]
                histogram = df['Histogram'].iloc[-1]
                
                if macd > signal and histogram > 0:
                    score += 25
                elif macd > signal:
                    score += 15
                if histogram > 0:
                    score += 10
            
            if 'Upper' in df.columns and 'Lower' in df.columns:
                close = df['Close'].iloc[-1]
                upper = df['Upper'].iloc[-1]
                lower = df['Lower'].iloc[-1]
                middle = df['Middle'].iloc[-1]
                
                if close < lower:
                    score += 20
                elif close < middle:
                    score += 10
                elif close > upper:
                    score += 5
            
            if 'Volume' in df.columns and 'Volume_MA20' in df.columns:
                volume = df['Volume'].iloc[-1]
                volume_ma = df['Volume_MA20'].iloc[-1]
                
                if volume > volume_ma * 1.5:
                    score += 15
                elif volume > volume_ma:
                    score += 10
        
        except Exception as e:
            self.logger.warning(f"计算技术面评分失败: {e}")
        
        return min(score, 100)
    
    def select_stocks(self, stock_data_dict, top_n=20):
        """
        根据技术面选择股票
        
        Args:
            stock_data_dict: {股票代码: DataFrame} 字典
            top_n: 返回前N只股票
        
        Returns:
            DataFrame: 选中的股票及其评分
        """
        results = []
        
        for symbol, df in stock_data_dict.items():
            try:
                if df.empty or len(df) < 60:
                    continue
                
                score = self.calculate_technical_score(df)
                price = df['Close'].iloc[-1]
                
                results.append({
                    'Symbol': symbol,
                    'Score': score,
                    'Price': price,
                    'Strategy': 'Technical'
                })
            except Exception as e:
                self.logger.debug(f"处理{symbol}时出错: {e}")
        
        results_df = pd.DataFrame(results)
        if results_df.empty:
            return results_df
        
        results_df = results_df.sort_values('Score', ascending=False).head(top_n)
        self.logger.info(f"技术面策略选中{len(results_df)}只股票")
        
        return results_df


class MomentumStrategy:
    """动量策略类"""
    
    def __init__(self, config=None):
        """
        初始化动量策略
        
        Args:
            config: 配置字典
        """
        self.config = config or {}
        self.logger = logger
    
    def calculate_momentum_score(self, df, period=20):
        """
        计算动量评分
        
        Args:
            df: 价格数据DataFrame
            period: 计算周期
        
        Returns:
            float: 评分 (0-100)
        """
        score = 0
        
        try:
            if len(df) < period:
                return 0
            
            returns = (df['Close'].iloc[-1] - df['Close'].iloc[-period]) / df['Close'].iloc[-period] * 100
            
            if returns > 20:
                score = 100
            elif returns > 15:
                score = 80
            elif returns > 10:
                score = 60
            elif returns > 5:
                score = 40
            elif returns > 0:
                score = 20
            else:
                score = 0
            
            if 'Volume' in df.columns and 'Volume_MA20' in df.columns:
                volume = df['Volume'].iloc[-1]
                volume_ma = df['Volume_MA20'].iloc[-1]
                if volume > volume_ma:
                    score = min(score + 20, 100)
        
        except Exception as e:
            self.logger.warning(f"计算动量评分失败: {e}")
        
        return score
    
    def select_stocks(self, stock_data_dict, period=20, top_n=20):
        """
        根据动量选择股票
        
        Args:
            stock_data_dict: {股票代码: DataFrame} 字典
            period: 计算周期
            top_n: 返回前N只股票
        
        Returns:
            DataFrame: 选中的股票及其评分
        """
        results = []
        
        for symbol, df in stock_data_dict.items():
            try:
                if df.empty or len(df) < period:
                    continue
                
                score = self.calculate_momentum_score(df, period)
                returns = (df['Close'].iloc[-1] - df['Close'].iloc[-period]) / df['Close'].iloc[-period] * 100
                price = df['Close'].iloc[-1]
                
                results.append({
                    'Symbol': symbol,
                    'Score': score,
                    'Return': returns,
                    'Price': price,
                    'Strategy': 'Momentum'
                })
            except Exception as e:
                self.logger.debug(f"处理{symbol}时出错: {e}")
        
        results_df = pd.DataFrame(results)
        if results_df.empty:
            return results_df
        
        results_df = results_df.sort_values('Score', ascending=False).head(top_n)
        self.logger.info(f"动量策略选中{len(results_df)}只股票")
        
        return results_df