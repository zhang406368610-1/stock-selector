"""
主程序
"""
import os
import pandas as pd
import yaml
from datetime import datetime

from data.fetcher import StockDataFetcher
from analysis.indicators import IndicatorAnalyzer
from analysis.visualizer import StockVisualizer
from strategies.technical import TechnicalStrategy, MomentumStrategy
from strategies.fundamental import FundamentalStrategy
from strategies.combined import CombinedStrategy
from backtest.engine import BacktestEngine
from utils.logger import LoggerConfig, get_logger

logger_config = LoggerConfig('./logs')
logger = get_logger(__name__)


def load_config(config_path='config/config.yaml'):
    """加载配置文件"""
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        logger.info(f"成功加载配置文件: {config_path}")
        return config
    except Exception as e:
        logger.error(f"加载配置文件失败: {e}")
        return {}


def create_output_dir(config):
    """创建输出目录"""
    output_dir = config.get('output', {}).get('output_dir', './results')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    chart_dir = os.path.join(output_dir, 'charts')
    if not os.path.exists(chart_dir):
        os.makedirs(chart_dir)
    
    logger.info(f"输出目录已创建: {output_dir}")
    return output_dir


def save_results(results, output_dir, strategy_name):
    """保存结果"""
    try:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        csv_path = os.path.join(output_dir, f"{strategy_name}_{timestamp}.csv")
        results.to_csv(csv_path, index=False)
        logger.info(f"结果已保存: {csv_path}")
        
        excel_path = os.path.join(output_dir, f"{strategy_name}_{timestamp}.xlsx")
        results.to_excel(excel_path, index=False)
        logger.info(f"结果已保存: {excel_path}")
    
    except Exception as e:
        logger.error(f"保存结果失败: {e}")


def main():
    """主程序"""
    logger.info("="*60)
    logger.info("智能选股系统启动")
    logger.info("="*60)
    
    config = load_config()
    output_dir = create_output_dir(config)
    
    logger.info("获取股票数据...")
    fetcher = StockDataFetcher(
        cache_dir=config.get('data', {}).get('cache_dir', './cache'),
        use_cache=config.get('data', {}).get('use_cache', True)
    )
    
    symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']
    stock_data = fetcher.fetch_multiple_stocks(symbols, period='1y')
    
    if not stock_data:
        logger.error("没有获取到股票数据")
        return
    
    logger.info(f"成功获取{len(stock_data)}只股票的数据")
    logger.info("选股策略执行完成")
    logger.info("="*60)


if __name__ == '__main__':
    main()