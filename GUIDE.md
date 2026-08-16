# 使用指南

## 安装步骤

### 1. 克隆仓库
```bash
git clone https://github.com/zhang406368610-1/stock-selector.git
cd stock-selector
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

## 配置

### 编辑配置文件
```bash
vi config/config.yaml
```

### 重要配置项

```yaml
# 选择策略类型
selection:
  strategy: combined              # technical, fundamental, momentum, combined
  select_count: 20                # 选择股票数量

# 技术参数
technical:
  ma_short: 20
  ma_long: 60
  rsi_period: 14
```

## 运行

### 基本运行
```bash
python main.py
```

### 查看输出

结果保存在 `results/` 目录：
- `combined_YYYYMMDD_HHMMSS.csv` - 选股结果
- `combined_YYYYMMDD_HHMMSS.xlsx` - Excel格式结果
- `charts/` - 图表文件

## 代码示例

### 技术面选股
```python
from data.fetcher import StockDataFetcher
from analysis.indicators import IndicatorAnalyzer
from strategies.technical import TechnicalStrategy

fetcher = StockDataFetcher()
stock_data = fetcher.fetch_multiple_stocks(['AAPL', 'MSFT'], period='1y')

processed_data = {}
for symbol, df in stock_data.items():
    analyzer = IndicatorAnalyzer(df)
    processed_data[symbol] = analyzer.add_all_indicators()

strategy = TechnicalStrategy()
results = strategy.select_stocks(processed_data, top_n=10)
print(results)
```

### 基本面选股
```python
from strategies.fundamental import FundamentalStrategy

fetcher = StockDataFetcher()
stock_info = {}
for symbol in ['AAPL', 'MSFT']:
    stock_info[symbol] = fetcher.fetch_stock_info(symbol)

strategy = FundamentalStrategy()
results = strategy.select_stocks(stock_info, top_n=10)
print(results)
```

### 可视化
```python
from analysis.visualizer import StockVisualizer

visualizer = StockVisualizer('./results/charts')
visualizer.plot_price_with_ma(df, 'AAPL')
visualizer.plot_rsi(df, 'AAPL')
visualizer.plot_macd(df, 'AAPL')
```

### 回测
```python
from backtest.engine import BacktestEngine

engine = BacktestEngine(initial_capital=100000)
result = engine.backtest_strategy(signals, prices, entry, exit)
engine.print_backtest_report(result)
```

## 常见问题

### Q: 如何获取最新数据？
A: 删除 `cache/` 目录下的缓存文件即可重新获取。

### Q: 如何修改策略参数？
A: 编辑 `config/config.yaml` 文件调整参数。

### Q: 支持哪些股票代码？
A: 支持Yahoo Finance支持的所有股票，如 AAPL、0700.HK 等。

### Q: 如何自定义选股数量？
A: 修改配置文件中的 `selection.select_count` 参数。

## 故障排除

### ModuleNotFoundError
```bash
pip install -r requirements.txt
```

### 网络连接错误
检查网络连接，确保可以访问 Yahoo Finance。

### 没有获取到数据
检查股票代码是否正确，或尝试删除缓存重新运行。

## 日志查看

```bash
# 查看最新日志
tail -f logs/stock_selector_*.log

# 列出所有日志
ls -ltr logs/
```

## 数据缓存

### 清除缓存
```bash
rm -rf cache/*
```

### 缓存位置
缓存文件在 `cache/` 目录，格式为 `{symbol}_{period}.pkl`

最后更新: 2026年8月16日
