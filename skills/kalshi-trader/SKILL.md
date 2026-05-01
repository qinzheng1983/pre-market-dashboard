---
name: kalshi-trader
description: Kalshi 预测市场宏观经济监测工具。查询 Kalshi API 获取经济事件概率（美联储利率、CPI、GDP等），用于宏观风险监测和决策支持。
metadata:
  version: 1.0.0
  author: openclaw
  requires:
    - kalshi-python>=2.1.4
---

# Kalshi Trader - 宏观经济预测市场监测

## 概述

Kalshi 是美国 CFTC 监管的事件预测市场，允许交易各种事件结果的概率合约。本 skill 提供对 Kalshi API 的访问，用于监测宏观经济事件的市场隐含概率。

### 核心功能

- 📊 **经济数据概率**: 获取 CPI、GDP、就业数据等的市场预测概率
- 🏦 **美联储政策**: 监测加息/降息概率
- 📈 **市场情绪**: 查看各类事件的交易量和市场情绪
- 🔍 **市场扫描**: 搜索特定事件合约

## 安装状态

✅ **Python 包已安装**: kalshi-python 2.1.4

```bash
# 基础安装（已完成）
pip install kalshi-python --break-system-packages --force-reinstall --no-deps
pip install pydantic python-dateutil lazy-imports --break-system-packages

# 验证安装
python3 -c "from kalshi_python import KalshiClient; print('✅ Kalshi 客户端已就绪')"
```

⚠️ **网络限制**: 当前环境无法直接访问 Kalshi API (api.elections.kalshi.com)

## 使用方法

### 1. 命令行工具 (本地网络环境)

```bash
# 获取美联储利率市场
python3 skills/kalshi-trader/scripts/kalshi_monitor.py --fed

# 搜索通胀相关市场
python3 skills/kalshi-trader/scripts/kalshi_monitor.py --search "CPI"

# 获取热门市场
python3 skills/kalshi-trader/scripts/kalshi_monitor.py --trending

# 获取经济日历
python3 skills/kalshi-trader/scripts/kalshi_monitor.py --econ

# 导出市场数据
python3 skills/kalshi-trader/scripts/kalshi_monitor.py --export
```

### 2. Python API 使用示例

```python
from kalshi_python import KalshiClient, MarketsApi

# 创建客户端
client = KalshiClient()
markets_api = MarketsApi(client)

# 获取市场列表
markets = markets_api.get_markets(status="open", limit=20)

for market in markets.markets:
    print(f"{market.ticker}: {market.title}")
    print(f"  YES价格: {market.yes_ask}")  # 隐含概率
    print(f"  交易量: {market.volume}")
```

### 3. 直接 HTTP API (无需 SDK)

```python
import requests

KALSHI_API = "https://api.elections.kalshi.com/trade-api/v2"

# 获取市场列表
response = requests.get(f"{KALSHI_API}/markets", params={
    "status": "open",
    "series_ticker": "FED",
    "limit": 20
})

data = response.json()
for market in data['markets']:
    print(f"{market['ticker']}: {market['title']}")
    print(f"  概率: {market.get('yes_ask', 'N/A')}")
```

## 常用市场代码

### 美联储利率
| 代码 | 描述 |
|------|------|
| FED-25M-5.25 | 美联储利率维持在 5.25% |
| FED-25M-5.50 | 美联储利率上调至 5.50% |

### 经济指标
| 代码 | 描述 |
|------|------|
| ECON-CPI-YYYY | CPI 通胀数据 |
| ECON-GDP-YYYY | GDP 增长率 |
| ECON-NFP-YYYY | 非农就业数据 |
| ECON-UR-YYYY | 失业率 |

## 输出格式

### 市场数据 JSON 结构

```json
{
  "ticker": "FED-25M-5.25",
  "title": "Will the Fed keep rates at 5.25%?",
  "status": "open",
  "yes_price": 0.65,
  "no_price": 0.35,
  "volume": 1250000,
  "open_interest": 850000,
  "settlement_date": "2025-03-19"
}
```

### 概率解释

- **YES价格**: 市场隐含的事件发生概率 (0.00 - 1.00)
- **价格0.65** = 65% 概率
- **交易量**: 反映市场关注度和流动性

## 应用场景

### 1. 宏观经济监测

```python
# 每日检查关键经济指标概率
key_events = ["CPI", "GDP", "NFP", "FED"]
for event in key_events:
    markets = markets_api.get_markets(event_ticker=f"ECON-{event}-2025")
    # 记录概率变化，监测预期偏差
```

### 2. 汇率预测辅助

结合地缘风险 skill 使用：

```python
# 获取美联储政策概率
fed_markets = markets_api.get_markets(series_ticker="FED")
rate_hike_prob = fed_markets.markets[0].yes_ask

# 用于 USD/CNY 预测
if rate_hike_prob > 0.7:
    # 加息概率高 → 美元走强预期
    fx_forecaster.add_signal("fed_hike_prob", rate_hike_prob)
```

### 3. 风险管理

- 监测尾部风险事件的概率变化
- 跟踪市场对经济衰退的预期
- 评估地缘政治事件的市场定价

## 演示数据

由于当前网络限制，提供以下模拟输出示例：

```
🏦 美联储利率决策市场
============================================================

📌 Will the Fed keep rates at 5.25% in March 2025?
   代码: FED-25M-5.25
   YES概率: 65.0%
   交易量: 1,250,000

📌 Will the Fed raise rates to 5.50% in March 2025?
   代码: FED-25M-5.50
   YES概率: 25.0%
   交易量: 890,000
```

## 文件结构

```
skills/kalshi-trader/
├── SKILL.md                      # 本文件
└── scripts/
    └── kalshi_monitor.py         # 监测工具脚本
```

## 数据限制

- **只读查询**: 无需认证，但有速率限制
- **交易功能**: 需要 API 密钥和资金账户
- **市场覆盖**: 仅限 CFTC 监管的美国合规市场
- **网络要求**: 需要访问 api.elections.kalshi.com

## 参考链接

- [Kalshi 官网](https://kalshi.com)
- [API 文档](https://trading-api.readme.io/reference)
- [Python SDK](https://github.com/kalshi/kalshi-python)

## 更新日志

### v1.0.0 (2026-03-16)
- 初始版本
- 基础市场查询功能
- 宏观经济事件监测
- 安装 kalshi-python 2.1.4
