"""
数据可视化模块
"""
import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from utils.logger import get_logger

logger = get_logger(__name__)

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False


class StockVisualizer:
    """股票数据可视化类"""
    
    def __init__(self, output_dir='./results/charts'):
        """
        初始化可视化器
        
        Args:
            output_dir: 输出目录
        """
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        sns.set_style("whitegrid")
        self.logger = logger
    
    def plot_price_with_ma(self, df, symbol, save=True):
        """
        绘制价格和移动平均线
        
        Args:
            df: 包含数据的DataFrame
            symbol: 股票代码
            save: 是否保存图表
        """
        try:
            fig, ax = plt.subplots(figsize=(14, 6))
            
            ax.plot(df.index, df['Close'], label='Close Price', linewidth=2, color='black')
            
            if 'MA20' in df.columns:
                ax.plot(df.index, df['MA20'], label='MA20', linewidth=1.5, alpha=0.7)
            
            if 'MA60' in df.columns:
                ax.plot(df.index, df['MA60'], label='MA60', linewidth=1.5, alpha=0.7)
            
            ax.set_title(f'{symbol} 价格和移动平均线', fontsize=14, fontweight='bold')
            ax.set_xlabel('日期', fontsize=12)
            ax.set_ylabel('价格', fontsize=12)
            ax.legend(loc='best')
            ax.grid(True, alpha=0.3)
            
            plt.tight_layout()
            
            if save:
                filepath = os.path.join(self.output_dir, f'{symbol}_price_ma.png')
                plt.savefig(filepath, dpi=300, bbox_inches='tight')
                self.logger.info(f"已保存图表: {filepath}")
            
            plt.show()
        except Exception as e:
            self.logger.error(f"绘制价格图表失败: {e}")
    
    def plot_rsi(self, df, symbol, save=True):
        """
        绘制RSI指标
        
        Args:
            df: 包含数据的DataFrame
            symbol: 股票代码
            save: 是否保存图表
        """
        try:
            if 'RSI14' not in df.columns:
                self.logger.warning("数据中不包含RSI14指标")
                return
            
            fig, ax = plt.subplots(figsize=(14, 6))
            
            ax.plot(df.index, df['RSI14'], label='RSI14', linewidth=2, color='blue')
            ax.axhline(y=70, color='r', linestyle='--', label='Overbought (70)')
            ax.axhline(y=30, color='g', linestyle='--', label='Oversold (30)')
            ax.fill_between(df.index, 70, 100, alpha=0.1, color='red')
            ax.fill_between(df.index, 0, 30, alpha=0.1, color='green')
            
            ax.set_title(f'{symbol} RSI 指标', fontsize=14, fontweight='bold')
            ax.set_xlabel('日期', fontsize=12)
            ax.set_ylabel('RSI', fontsize=12)
            ax.set_ylim([0, 100])
            ax.legend(loc='best')
            ax.grid(True, alpha=0.3)
            
            plt.tight_layout()
            
            if save:
                filepath = os.path.join(self.output_dir, f'{symbol}_rsi.png')
                plt.savefig(filepath, dpi=300, bbox_inches='tight')
                self.logger.info(f"已保存图表: {filepath}")
            
            plt.show()
        except Exception as e:
            self.logger.error(f"绘制RSI图表失败: {e}")
    
    def plot_macd(self, df, symbol, save=True):
        """
        绘制MACD指标
        
        Args:
            df: 包含数据的DataFrame
            symbol: 股票代码
            save: 是否保存图表
        """
        try:
            if 'MACD' not in df.columns:
                self.logger.warning("数据中不包含MACD指标")
                return
            
            fig, ax = plt.subplots(figsize=(14, 6))
            
            ax.plot(df.index, df['MACD'], label='MACD', linewidth=2, color='blue')
            ax.plot(df.index, df['Signal'], label='Signal', linewidth=2, color='red')
            ax.bar(df.index, df['Histogram'], label='Histogram', alpha=0.3, color='gray')
            ax.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
            
            ax.set_title(f'{symbol} MACD 指标', fontsize=14, fontweight='bold')
            ax.set_xlabel('日期', fontsize=12)
            ax.set_ylabel('MACD', fontsize=12)
            ax.legend(loc='best')
            ax.grid(True, alpha=0.3)
            
            plt.tight_layout()
            
            if save:
                filepath = os.path.join(self.output_dir, f'{symbol}_macd.png')
                plt.savefig(filepath, dpi=300, bbox_inches='tight')
                self.logger.info(f"已保存图表: {filepath}")
            
            plt.show()
        except Exception as e:
            self.logger.error(f"绘制MACD图表失败: {e}")
    
    def plot_bollinger_bands(self, df, symbol, save=True):
        """
        绘制布林带
        
        Args:
            df: 包含数据的DataFrame
            symbol: 股票代码
            save: 是否保存图表
        """
        try:
            if 'Upper' not in df.columns:
                self.logger.warning("数据中不包含布林带指标")
                return
            
            fig, ax = plt.subplots(figsize=(14, 6))
            
            ax.plot(df.index, df['Close'], label='Close Price', linewidth=2, color='black')
            ax.plot(df.index, df['Upper'], label='Upper Band', linewidth=1.5, color='red', linestyle='--')
            ax.plot(df.index, df['Middle'], label='Middle Band', linewidth=1.5, color='blue')
            ax.plot(df.index, df['Lower'], label='Lower Band', linewidth=1.5, color='green', linestyle='--')
            ax.fill_between(df.index, df['Upper'], df['Lower'], alpha=0.1, color='blue')
            
            ax.set_title(f'{symbol} 布林带', fontsize=14, fontweight='bold')
            ax.set_xlabel('日期', fontsize=12)
            ax.set_ylabel('价格', fontsize=12)
            ax.legend(loc='best')
            ax.grid(True, alpha=0.3)
            
            plt.tight_layout()
            
            if save:
                filepath = os.path.join(self.output_dir, f'{symbol}_bollinger_bands.png')
                plt.savefig(filepath, dpi=300, bbox_inches='tight')
                self.logger.info(f"已保存图表: {filepath}")
            
            plt.show()
        except Exception as e:
            self.logger.error(f"绘制布林带图表失败: {e}")
    
    def plot_volume(self, df, symbol, save=True):
        """
        绘制成交量
        
        Args:
            df: 包含数据的DataFrame
            symbol: 股票代码
            save: 是否保存图表
        """
        try:
            fig, ax = plt.subplots(figsize=(14, 6))
            
            colors = ['green' if df['Close'].iloc[i] >= df['Close'].iloc[i-1] else 'red' 
                     for i in range(1, len(df))]
            colors.insert(0, 'gray')
            
            ax.bar(df.index, df['Volume'], color=colors, alpha=0.6, label='Volume')
            
            if 'Volume_MA20' in df.columns:
                ax.plot(df.index, df['Volume_MA20'], label='Volume MA20', 
                       linewidth=2, color='blue')
            
            ax.set_title(f'{symbol} 成交量', fontsize=14, fontweight='bold')
            ax.set_xlabel('日期', fontsize=12)
            ax.set_ylabel('成交量', fontsize=12)
            ax.legend(loc='best')
            ax.grid(True, alpha=0.3)
            
            plt.tight_layout()
            
            if save:
                filepath = os.path.join(self.output_dir, f'{symbol}_volume.png')
                plt.savefig(filepath, dpi=300, bbox_inches='tight')
                self.logger.info(f"已保存图表: {filepath}")
            
            plt.show()
        except Exception as e:
            self.logger.error(f"绘制成交量图表失败: {e}")
    
    def plot_selection_results(self, results, save=True):
        """
        绘制选股结果
        
        Args:
            results: 选股结果DataFrame
            save: 是否保存图表
        """
        try:
            # 绘制评分分布
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
            
            # 评分柱状图
            results_sorted = results.sort_values('Score', ascending=False).head(20)
            ax1.barh(results_sorted['Symbol'], results_sorted['Score'], color='steelblue')
            ax1.set_xlabel('评分', fontsize=12)
            ax1.set_title('选股评分Top 20', fontsize=14, fontweight='bold')
            ax1.grid(True, alpha=0.3, axis='x')
            
            # 评分分布直方图
            ax2.hist(results['Score'], bins=30, color='steelblue', alpha=0.7, edgecolor='black')
            ax2.set_xlabel('评分', fontsize=12)
            ax2.set_ylabel('频数', fontsize=12)
            ax2.set_title('评分分布', fontsize=14, fontweight='bold')
            ax2.grid(True, alpha=0.3)
            
            plt.tight_layout()
            
            if save:
                filepath = os.path.join(self.output_dir, 'selection_results.png')
                plt.savefig(filepath, dpi=300, bbox_inches='tight')
                self.logger.info(f"已保存图表: {filepath}")
            
            plt.show()
        except Exception as e:
            self.logger.error(f"绘制选股结果图表失败: {e}")