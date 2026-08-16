"""
股票数据获取模块
支持从Yahoo Finance获取数据
"""
import os
import pickle
from datetime import datetime, timedelta
import pandas as pd
import yfinance as yf
from utils.logger import get_logger

logger = get_logger(__name__)


class StockDataFetcher:
    """股票数据获取器"""
    
    def __init__(self, cache_dir='./cache', use_cache=True):
        """
        初始化数据获取器
        
        Args:
            cache_dir: 缓存目录
            use_cache: 是否使用缓存
        """
        self.cache_dir = cache_dir
        self.use_cache = use_cache
        
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
        
        logger.info(f"初始化数据获取器，缓存目录: {cache_dir}")
    
    def _get_cache_path(self, symbol, period):
        """获取缓存文件路径"""
        return os.path.join(self.cache_dir, f"{symbol}_{period}.pkl")
    
    def _load_cache(self, symbol, period):
        """从缓存加载数据"""
        cache_path = self._get_cache_path(symbol, period)
        if os.path.exists(cache_path):
            try:
                with open(cache_path, 'rb') as f:
                    data = pickle.load(f)
                logger.debug(f"从缓存加载 {symbol} 数据")
                return data
            except Exception as e:
                logger.warning(f"缓存加载失败: {e}")
                return None
        return None
    
    def _save_cache(self, symbol, period, data):
        """保存数据到缓存"""
        try:
            cache_path = self._get_cache_path(symbol, period)
            with open(cache_path, 'wb') as f:
                pickle.dump(data, f)
            logger.debug(f"已缓存 {symbol} 数据")
        except Exception as e:
            logger.warning(f"缓存保存失败: {e}")
    
    def fetch_stock_data(self, symbol, period='1y', start=None, end=None):
        """
        获取单只股票数据
        
        Args:
            symbol: 股票代码 (如: 'AAPL', '0700.HK')
            period: 数据周期 ('1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y')
            start: 开始日期 (格式: 'YYYY-MM-DD')
            end: 结束日期 (格式: 'YYYY-MM-DD')
        
        Returns:
            DataFrame: 包含OHLCV数据
        """
        # 先尝试从缓存加载
        if self.use_cache and start is None and end is None:
            cached_data = self._load_cache(symbol, period)
            if cached_data is not None:
                return cached_data
        
        try:
            logger.info(f"获取 {symbol} 数据，周期: {period}")
            
            ticker = yf.Ticker(symbol)
            if start and end:
                data = ticker.history(start=start, end=end)
            else:
                data = ticker.history(period=period)
            
            if data.empty:
                logger.warning(f"未获取到 {symbol} 的数据")
                return pd.DataFrame()
            
            # 保存到缓存
            if self.use_cache and start is None and end is None:
                self._save_cache(symbol, period, data)
            
            logger.info(f"成功获取 {symbol} 数据，共 {len(data)} 条记录")
            return data
        
        except Exception as e:
            logger.error(f"获取 {symbol} 数据失败: {e}")
            return pd.DataFrame()
    
    def fetch_multiple_stocks(self, symbols, period='1y', start=None, end=None):
        """
        获取多只股票数据
        
        Args:
            symbols: 股票代码列表
            period: 数据周期
            start: 开始日期
            end: 结束日期
        
        Returns:
            dict: 股票代码 -> DataFrame 的字典
        """
        data_dict = {}
        for symbol in symbols:
            data = self.fetch_stock_data(symbol, period, start, end)
            if not data.empty:
                data_dict[symbol] = data
        
        logger.info(f"成功获取 {len(data_dict)}/{len(symbols)} 只股票的数据")
        return data_dict
    
    def fetch_stock_info(self, symbol):
        """
        获取股票基本信息和财务数据
        
        Args:
            symbol: 股票代码
        
        Returns:
            dict: 股票信息
        """
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            logger.info(f"成功获取 {symbol} 的基本信息")
            return info
        except Exception as e:
            logger.error(f"获取 {symbol} 基本信息失败: {e}")
            return {}
    
    def get_current_price(self, symbol):
        """
        获取当前价格
        
        Args:
            symbol: 股票代码
        
        Returns:
            float: 当前价格
        """
        try:
            ticker = yf.Ticker(symbol)
            price = ticker.info.get('currentPrice')
            if price is None:
                # 备用方案：获取最后一次成交价
                data = ticker.history(period='1d')
                if not data.empty:
                    price = data['Close'].iloc[-1]
            return price
        except Exception as e:
            logger.error(f"获取 {symbol} 当前价格失败: {e}")
            return None


class StockListFetcher:
    """获取股票列表"""
    
    @staticmethod
    def get_sp500_stocks():
        """获取标准普尔500指数成分股"""
        try:
            logger.info("获取S&P 500成分股...")
            url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
            tables = pd.read_html(url)
            df = tables[0]
            symbols = df['Symbol'].tolist()
            logger.info(f"成功获取 {len(symbols)} 只S&P 500成分股")
            return symbols
        except Exception as e:
            logger.error(f"获取S&P 500成分股失败: {e}")
            return []
    
    @staticmethod
    def get_nasdaq_stocks():
        """获取纳斯达克100指数成分股"""
        try:
            logger.info("获取NASDAQ-100成分股...")
            url = "https://en.wikipedia.org/wiki/Nasdaq-100"
            tables = pd.read_html(url)
            # NASDAQ表格位置可能变化，需要查找正确的表
            for table in tables:
                if 'Ticker' in table.columns:
                    symbols = table['Ticker'].tolist()
                    logger.info(f"成功获取 {len(symbols)} 只NASDAQ-100成分股")
                    return symbols
        except Exception as e:
            logger.error(f"获取NASDAQ-100成分股失败: {e}")
        return []
    
    @staticmethod
    def get_custom_stocks(symbols):
        """
        使用自定义股票列表
        
        Args:
            symbols: 股票代码列表
        
        Returns:
            list: 股票代码列表
        """
        logger.info(f"使用自定义股票列表，共 {len(symbols)} 只")
        return symbols