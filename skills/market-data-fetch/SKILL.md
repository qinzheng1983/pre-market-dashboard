---
name: market-data-fetch
description: 市场数据获取工具。支持 Yahoo Finance、Alpha Vantage 等多种数据源，获取股票、外汇、加密货币等实时和历史价格数据。包含演示模式用于测试。
metadata:
  version: 1.0.0
  author: openclaw
  requires:
    - yfinance>=1.2.0
    - pandas-datareader>=0.10.0
---

# Market Data Fetch - 市场数据获取工具

## 概述

本 skill 提供多种市场数据源的统一接口，支持获取：

- 📈 **股票数据** - 实时价格、历史K线、财务报表
- 💱 **外汇数据** - 汇率、历史走势
- 🪙 **加密货币** - BTC、ETH 等主流币种
- 📊 **指数数据** - 全球主要股指

## 安装

```bash
# 安装依赖（已完成）
pip install yfinance pandas-datareader --break-system-packages

# 验证安装
python3 -c "import yfinance; print('✅ yfinance', yfinance.__version__)"
```

✅ **已安装**: yfinance 1.2.0, pandas-datareader 0.10.0

## 使用方法

### 1. 命令行工具

```bash
# 获取股票实时价格
python3 skills/market-data-fetch/scripts/fetch_market_data.py --ticker AAPL

# 获取历史数据
python3 skills/market-data-fetch/scripts/fetch_market_data.py --ticker TSLA --history 30

# 获取外汇汇率
python3 skills/market-data-fetch/scripts/fetch_market_data.py --fx USD/CNY

# 获取加密货币
python3 skills/market-data-fetch/scripts/fetch_market_data.py --crypto BTC-USD

# 获取指数
python3 skills/market-data-fetch/scripts/fetch_market_data.py --index ^GSPC

# 使用演示模式 (无需 API，用于测试)
python3 skills/market-data-fetch/scripts/fetch_market_data.py --ticker AAPL --demo
```

### 2. Python API

```python
from fetch_market_data import MarketDataFetcher

# 创建获取器
demo_mode = True  # 设为 False 使用真实 API
fetcher = MarketDataFetcher(demo_mode=demo_mode)

# 获取股票数据
stock = fetcher.get_stock('AAPL')
print(f"价格: {stock['price']}, 涨跌: {stock['change_percent']}%")

# 获取历史数据
hist = fetcher.get_history('AAPL', period='1mo')
print(hist['data'][-5:])  # 最近5天

# 获取外汇
fx = fetcher.get_fx('USDCNY=X')
print(f"汇率: {fx['rate']}")
```

## 支持的数据源

| 数据源 | 类型 | 免费额度 | 特点 | 状态 |
|--------|------|----------|------|------|
| Yahoo Finance | 股票/外汇/加密 | 无限制 | 通过 yfinance | ⚠️ 当前限速 |
| Alpha Vantage | 股票/外汇 | 500次/天 | 需要 API Key | 可选 |
| pandas_datareader | 多源 | 取决于源 | FRED、世界银行 | 可选 |
| **演示模式** | 模拟数据 | 无限制 | 用于测试 | ✅ 可用 |

## 演示模式

当 Yahoo Finance API 受限时，自动切换到演示模式：

```python
fetcher = MarketDataFetcher(demo_mode=True)

# 或使用命令行参数
python3 fetch_market_data.py --ticker AAPL --demo
```

演示数据包含：
- 主要股票: AAPL, TSLA, MSFT, GOOGL, AMZN
- 外汇: USDCNY, USDEUR, USDJPY 等
- 加密货币: BTC-USD, ETH-USD
- 指数: ^GSPC, ^DJI, ^IXIC

## 输出格式

### 股票实时数据

```json
{
  "ticker": "AAPL",
  "name": "Apple Inc.",
  "price": 223.45,
  "change": 2.35,
  "change_percent": 1.06,
  "volume": 45678900,
  "market_cap": 3400000000000,
  "pe_ratio": 32.5,
  "currency": "USD",
  "timestamp": "2026-03-16T09:30:00",
  "demo": true
}
```

### 外汇数据

```json
{
  "pair": "USDCNY",
  "rate": 7.2456,
  "change": 0.0123,
  "change_percent": 0.17,
  "timestamp": "2026-03-16T09:30:00",
  "demo": true
}
```

## 应用场景

### 1. 汇率预测辅助

```python
from fetch_market_data import MarketDataFetcher
from fx_forecaster import FXForecaster

fetcher = MarketDataFetcher(demo_mode=True)
forecaster = FXForecaster(base_fx=7.25)

# 获取 USD/CNY 历史数据
usdcny = fetcher.get_history('USDCNY=X', period='6mo')
closes = [d['close'] for d in usdcny['data']]

# 计算波动率
import numpy as np
returns = [(closes[i] - closes[i-1]) / closes[i-1] 
           for i in range(1, len(closes))]
volatility = np.std(returns) * np.sqrt(252)

print(f"USD/CNY 年化波动率: {volatility:.2%}")

# 添加到预测模型
forecaster.add_volatility_signal(volatility)
```

### 2. 市场情绪监测

```python
fetcher = MarketDataFetcher(demo_mode=True)

# 获取 VIX 波动率指数
vix = fetcher.get_stock('^VIX')
print(f"VIX: {vix['price']} ({vix['change_percent']}%)")

# 获取原油价格 (地缘风险指标)
oil = fetcher.get_stock('CL=F')
print(f"原油: ${oil['price']}")

# 获取黄金价格 (避险资产)
gold = fetcher.get_stock('GC=F')
print(f"黄金: ${gold['price']}")
```

### 3. 与地缘风险 skill 整合

```python
# 完整示例见 examples/usage_examples.py
python3 skills/market-data-fetch/examples/usage_examples.py
```

## 文件结构

```
skills/market-data-fetch/
├── SKILL.md                      # 本文件
├── scripts/
│   └── fetch_market_data.py      # 主脚本
└── examples/
    └── usage_examples.py         # 使用示例
```

## 数据限制

- **Yahoo Finance**: 无限制，但数据可能有15-20分钟延迟，当前环境受限速
- **演示模式**: 无限制，数据为模拟生成，仅用于测试
- **实时性**: 免费数据源通常有延迟，不适合高频交易

## 参考链接

- [yfinance GitHub](https://github.com/ranaroussi/yfinance)
- [pandas-datareader Docs](https://pandas-datareader.readthedocs.io/)
- [Yahoo Finance](https://finance.yahoo.com)

## 更新日志

### v1.0.0 (2026-03-16)
- 初始版本
- 集成 yfinance 1.2.0
- 支持股票、外汇、加密货币
- 添加演示模式
