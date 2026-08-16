# Stock Selector - 智能选股系统

一个完整的Python股票选股系统，提供多种选股策略、技术分析、基本面分析和回测功能。

## 核心功能

- 多数据源支持 - Yahoo Finance数据获取
- 多维度选股 - 技术面、基本面、动量、综合策略
- 技术指标库 - MA、RSI、MACD、布林带、ATR等20+指标
- 完整回测系统 - 历史数据回测、收益计算、风险分析
- 可视化分析 - 交互式图表展示
- 灵活配置 - YAML配置文件，轻松定制策略

## 项目结构

```
stock-selector/
├── README.md                    # 项目说明
├── GUIDE.md                     # 使用指南
├── requirements.txt             # 依赖包
├── config/
│   └── config.yaml             # 配置文件
├── data/
│   ├── __init__.py
│   └── fetcher.py              # 数据获取模块
├── strategies/
│   ├── __init__.py
│   ├── technical.py            # 技术面策略
│   ├── fundamental.py          # 基本面策略
│   └── combined.py             # 综合策略
├── analysis/
│   ├── __init__.py
│   ├── indicators.py           # 技术指标计算
│   └── visualizer.py           # 数据可视化
├── backtest/
│   ├── __init__.py
│   └── engine.py               # 回测引擎
├── utils/
│   ├── __init__.py
│   └── logger.py               # 日志工具
└── main.py                      # 主程序
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 运行选股

```bash
python main.py
```

### 3. 查看结果

结果保存在 `results/` 目录下

## 支持的策略

### 技术面策略 (TechnicalStrategy)
- 移动平均线 (MA) 判断趋势
- 相对强弱指数 (RSI) 判断超买超卖
- MACD 确认趋势转变
- 布林带 识别支撑阻力
- 成交量 验证价格行动

### 基本面策略 (FundamentalStrategy)
- PE估值筛选
- PB估值筛选
- ROE收益率分析
- 毛利率评估
- 债务水平分析

### 动量策略 (MomentumStrategy)
- 短期涨幅排序
- 成交量确认
- 快速捕捉上升趋势

### 综合策略 (CombinedStrategy)
- 多策略融合
- 权重自定义配置
- 综合评分排序

## 技术指标

支持20+技术指标：MA、EMA、RSI、MACD、Bollinger Bands、ATR、Volume MA、OBV、Stochastic等

## 配置说明

编辑 `config/config.yaml` 配置选股参数：

```yaml
# 选择策略
selection:
  strategy: combined              # 可选: technical, fundamental, momentum, combined
  select_count: 20                # 选择前N只股票

# 技术面参数
technical:
  ma_short: 20                    # 短期MA周期
  ma_long: 60                     # 长期MA周期
  rsi_period: 14                  # RSI周期

# 基本面参数
fundamental:
  pe_min: 5                       # PE最小值
  pe_max: 50                      # PE最大值
  pb_min: 0.5                     # PB最小值
  pb_max: 5                       # PB最大值
```

## 使用示例

### 示例1: 技术面选股

```python
from data.fetcher import StockDataFetcher
from analysis.indicators import IndicatorAnalyzer
from strategies.technical import TechnicalStrategy

# 获取数据
fetcher = StockDataFetcher()
stock_data = fetcher.fetch_multiple_stocks(['AAPL', 'MSFT'], period='1y')

# 计算指标
processed_data = {}
for symbol, df in stock_data.items():
    analyzer = IndicatorAnalyzer(df)
    processed_data[symbol] = analyzer.add_all_indicators()

# 运行策略
strategy = TechnicalStrategy()
results = strategy.select_stocks(processed_data, top_n=10)
print(results)
```

### 示例2: 可视化分析

```python
from analysis.visualizer import StockVisualizer

visualizer = StockVisualizer('./results/charts')
visualizer.plot_price_with_ma(df, 'AAPL')
visualizer.plot_rsi(df, 'AAPL')
visualizer.plot_macd(df, 'AAPL')
```

### 示例3: 回测策略

```python
from backtest.engine import BacktestEngine
import numpy as np

engine = BacktestEngine(initial_capital=100000)
result = engine.backtest_strategy(
    signals,
    prices,
    entry_prices,
    exit_prices
)
engine.print_backtest_report(result)
```

## 输出结果

选股结果包含：
- Symbol: 股票代码
- Score: 综合评分 (0-100)
- Technical: 技术面评分
- Momentum: 动量评分
- Fundamental: 基本面评分
- Price: 当前价格
- Strategy: 使用的策略

## 日志文件

日志保存在 `logs/` 目录，每次运行生成新的日志文件

## 缓存管理

数据缓存在 `cache/` 目录，可以手动删除缓存强制重新获取数据：

```bash
rm -rf cache/*
```

## 许可证

MIT License

## 声明

本系统仅供学习交流使用，不构成投资建议。使用本系统进行的投资决策造成的任何损失，本项目作者概不负责。
