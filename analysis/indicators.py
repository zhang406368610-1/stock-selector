"""
技术指标计算模块
"""
import numpy as np
import pandas as pd
import ta
from utils.logger import get_logger

logger = get_logger(__name__)


class TechnicalIndicators:
    """技术指标计算类"""
    
    @staticmethod
    def calculate_ma(data, period=20):
        """
        计算移动平均线
        
        Args:
            data: 价格序列
            period: 周期
        
        Returns:
            Series: MA值
        """
        return data.rolling(window=period).mean()
    
    @staticmethod
    def calculate_ema(data, period=20):
        """
        计算指数移动平均线
        
        Args:
            data: 价格序列
            period: 周期
        
        Returns:
            Series: EMA值
        """
        return data.ewm(span=period, adjust=False).mean()
    
    @staticmethod
    def calculate_rsi(data, period=14):
        """
        计算相对强弱指数
        
        Args:
            data: 价格序列
            period: 周期
        
        Returns:
            Series: RSI值
        """
        delta = data.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    @staticmethod
    def calculate_macd(data, fast=12, slow=26, signal=9):
        """
        计算MACD指标
        
        Args:
            data: 价格序列
            fast: 快速周期
            slow: 慢速周期
            signal: 信号周期
        
        Returns:
            DataFrame: MACD、信号线和柱状图
        """
        ema_fast = data.ewm(span=fast, adjust=False).mean()
        ema_slow = data.ewm(span=slow, adjust=False).mean()
        
        macd = ema_fast - ema_slow
        signal_line = macd.ewm(span=signal, adjust=False).mean()
        histogram = macd - signal_line
        
        return pd.DataFrame({
            'MACD': macd,
            'Signal': signal_line,
            'Histogram': histogram
        })
    
    @staticmethod
    def calculate_bollinger_bands(data, period=20, std=2):
        """
        计算布林带
        
        Args:
            data: 价格序列
            period: 周期
            std: 标准差倍数
        
        Returns:
            DataFrame: 上轨、中轨、下轨
        """
        sma = data.rolling(window=period).mean()
        std_dev = data.rolling(window=period).std()
        
        upper = sma + (std * std_dev)
        lower = sma - (std * std_dev)
        
        return pd.DataFrame({
            'Upper': upper,
            'Middle': sma,
            'Lower': lower
        })
    
    @staticmethod
    def calculate_atr(high, low, close, period=14):
        """
        计算平均真实波幅
        
        Args:
            high: 最高价
            low: 最低价
            close: 收盘价
            period: 周期
        
        Returns:
            Series: ATR值
        """
        tr1 = high - low
        tr2 = abs(high - close.shift())
        tr3 = abs(low - close.shift())
        
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        atr = tr.rolling(window=period).mean()
        
        return atr
    
    @staticmethod
    def calculate_volume_ma(volume, period=20):
        """
        计算成交量移动平均
        
        Args:
            volume: 成交量序列
            period: 周期
        
        Returns:
            Series: 成交量MA
        """
        return volume.rolling(window=period).mean()
    
    @staticmethod
    def calculate_obv(close, volume):
        """
        计算能量潮指标
        
        Args:
            close: 收盘价
            volume: 成交量
        
        Returns:
            Series: OBV值
        """
        obv = np.zeros(len(close))
        for i in range(1, len(close)):
            if close.iloc[i] > close.iloc[i-1]:
                obv[i] = obv[i-1] + volume.iloc[i]
            elif close.iloc[i] < close.iloc[i-1]:
                obv[i] = obv[i-1] - volume.iloc[i]
            else:
                obv[i] = obv[i-1]
        
        return pd.Series(obv, index=close.index)
    
    @staticmethod
    def calculate_stochastic(high, low, close, period=14, smooth=3):
        """
        计算随机指标
        
        Args:
            high: 最高价
            low: 最低价
            close: 收盘价
            period: 周期
            smooth: 平滑周期
        
        Returns:
            DataFrame: K值和D值
        """
        lowest_low = low.rolling(window=period).min()
        highest_high = high.rolling(window=period).max()
        
        k = 100 * ((close - lowest_low) / (highest_high - lowest_low))
        d = k.rolling(window=smooth).mean()
        
        return pd.DataFrame({
            'K': k,
            'D': d
        })


class IndicatorAnalyzer:
    """指标分析器"""
    
    def __init__(self, df):
        """
        初始化指标分析器
        
        Args:
            df: 包含OHLCV数据的DataFrame
        """
        self.df = df.copy()
        self.logger = logger
    
    def add_all_indicators(self):
        """添加所有技术指标"""
        self.logger.info("计算所有技术指标...")
        
        # 移动平均线
        self.df['MA20'] = TechnicalIndicators.calculate_ma(self.df['Close'], 20)
        self.df['MA60'] = TechnicalIndicators.calculate_ma(self.df['Close'], 60)
        self.df['EMA12'] = TechnicalIndicators.calculate_ema(self.df['Close'], 12)
        self.df['EMA26'] = TechnicalIndicators.calculate_ema(self.df['Close'], 26)
        
        # RSI
        self.df['RSI14'] = TechnicalIndicators.calculate_rsi(self.df['Close'], 14)
        
        # MACD
        macd_df = TechnicalIndicators.calculate_macd(self.df['Close'])
        self.df = pd.concat([self.df, macd_df], axis=1)
        
        # 布林带
        bb_df = TechnicalIndicators.calculate_bollinger_bands(self.df['Close'])
        self.df = pd.concat([self.df, bb_df], axis=1)
        
        # ATR
        self.df['ATR14'] = TechnicalIndicators.calculate_atr(
            self.df['High'], self.df['Low'], self.df['Close'], 14
        )
        
        # 成交量
        self.df['Volume_MA20'] = TechnicalIndicators.calculate_volume_ma(self.df['Volume'], 20)
        self.df['OBV'] = TechnicalIndicators.calculate_obv(self.df['Close'], self.df['Volume'])
        
        # 随机指标
        stoch_df = TechnicalIndicators.calculate_stochastic(
            self.df['High'], self.df['Low'], self.df['Close']
        )
        self.df = pd.concat([self.df, stoch_df], axis=1)
        
        self.logger.info("技术指标计算完成")
        return self.df
    
    def get_indicators(self):
        """获取指标数据"""
        return self.df