"""
回测引擎
"""
import pandas as pd
import numpy as np
from utils.logger import get_logger

logger = get_logger(__name__)


class BacktestEngine:
    """回测引擎类"""
    
    def __init__(self, initial_capital=100000, commission=0.001, slippage=0.0005):
        """
        初始化回测引擎
        
        Args:
            initial_capital: 初始资金
            commission: 交易手续费率
            slippage: 滑点
        """
        self.initial_capital = initial_capital
        self.commission = commission
        self.slippage = slippage
        self.logger = logger
    
    def backtest_strategy(self, signal_data, stock_price, entry_price, exit_price):
        """
        执行回测
        
        Args:
            signal_data: 买卖信号 (1: 买, -1: 卖, 0: 持有)
            stock_price: 股票价格序列
            entry_price: 买入价格
            exit_price: 卖出价格
        
        Returns:
            dict: 回测结果
        """
        capital = self.initial_capital
        position = 0
        portfolio_value = [capital]
        trades = []
        
        try:
            for i in range(len(signal_data)):
                signal = signal_data[i]
                price = stock_price[i]
                
                if signal == 1 and position == 0:
                    actual_price = price * (1 + self.slippage)
                    shares = int(capital / (actual_price * (1 + self.commission)))
                    
                    if shares > 0:
                        cost = shares * actual_price * (1 + self.commission)
                        capital -= cost
                        position = shares
                        
                        trades.append({
                            'Date': i,
                            'Type': 'BUY',
                            'Price': actual_price,
                            'Shares': shares,
                            'Cost': cost
                        })
                
                elif signal == -1 and position > 0:
                    actual_price = price * (1 - self.slippage)
                    revenue = position * actual_price * (1 - self.commission)
                    capital += revenue
                    
                    trades.append({
                        'Date': i,
                        'Type': 'SELL',
                        'Price': actual_price,
                        'Shares': position,
                        'Revenue': revenue
                    })
                    
                    position = 0
                
                if position > 0:
                    current_value = capital + position * price
                else:
                    current_value = capital
                
                portfolio_value.append(current_value)
            
            final_value = portfolio_value[-1]
            total_return = (final_value - self.initial_capital) / self.initial_capital * 100
            annual_return = total_return / (len(portfolio_value) / 252)
            
            cumulative_max = np.maximum.accumulate(portfolio_value)
            drawdown = (np.array(portfolio_value) - cumulative_max) / cumulative_max * 100
            max_drawdown = drawdown.min()
            
            returns = pd.Series(portfolio_value).pct_change().dropna()
            sharpe_ratio = returns.mean() / returns.std() * np.sqrt(252) if returns.std() > 0 else 0
            
            result = {
                'Initial Capital': self.initial_capital,
                'Final Value': final_value,
                'Total Return %': total_return,
                'Annual Return %': annual_return,
                'Max Drawdown %': max_drawdown,
                'Sharpe Ratio': sharpe_ratio,
                'Trade Count': len(trades),
                'Portfolio Values': portfolio_value,
                'Trades': trades
            }
            
            self.logger.info(f"回测完成: 总收益{total_return:.2f}%, 最大回枕{max_drawdown:.2f}%")
            return result
        
        except Exception as e:
            self.logger.error(f"回测失败: {e}")
            return {}
    
    def backtest_simple(self, df, buy_signal_col, sell_signal_col):
        """
        简单回测
        
        Args:
            df: 包含价格和信号的DataFrame
            buy_signal_col: 买入信号列
            sell_signal_col: 卖出信号列
        
        Returns:
            dict: 回测结果
        """
        signals = np.zeros(len(df))
        for i in range(len(df)):
            if df[buy_signal_col].iloc[i]:
                signals[i] = 1
            elif df[sell_signal_col].iloc[i]:
                signals[i] = -1
        
        return self.backtest_strategy(
            signals,
            df['Close'].values,
            df['Close'].values,
            df['Close'].values
        )
    
    def calculate_win_rate(self, trades):
        """
        计算胜率
        
        Args:
            trades: 交易记录列表
        
        Returns:
            float: 胜率
        """
        if not trades:
            return 0
        
        winning_trades = 0
        buy_price = None
        
        for trade in trades:
            if trade['Type'] == 'BUY':
                buy_price = trade['Price']
            elif trade['Type'] == 'SELL' and buy_price:
                if trade['Price'] > buy_price:
                    winning_trades += 1
        
        return winning_trades / (len(trades) // 2) * 100 if trades else 0
    
    def print_backtest_report(self, result):
        """
        打印回测报告
        
        Args:
            result: 回测结果
        """
        print("\n" + "="*60)
        print("回测结果报告")
        print("="*60)
        print(f"\u521d始资金: ${result.get('Initial Capital', 0):,.2f}")
        print(f"最终资产: ${result.get('Final Value', 0):,.2f}")
        print(f"总收益: {result.get('Total Return %', 0):.2f}%")
        print(f"年化收益: {result.get('Annual Return %', 0):.2f}%")
        print(f"最大回枕: {result.get('Max Drawdown %', 0):.2f}%")
        print(f"夕支比: {result.get('Sharpe Ratio', 0):.4f}")
        print(f"交易次数: {result.get('Trade Count', 0)}")
        print(f"胜率: {self.calculate_win_rate(result.get('Trades', [])):.2f}%")
        print("="*60 + "\n")