---
name: multi-search-engine
description: 多搜索引擎聚合工具 - 聚合 DuckDuckGo、SearXNG 等多个搜索引擎结果，提供更全面的搜索能力，无需 API Key。
metadata:
  version: 1.0.0
  author: openclaw
---

# Multi Search Engine - 多搜索引擎聚合工具

## 概述

聚合多个搜索引擎的结果，提供更全面的搜索能力。支持 DuckDuckGo、SearXNG 等无需 API Key 的搜索引擎。

## 功能特点

- 🔍 **多引擎聚合** - 同时查询多个搜索引擎
- 🆓 **无需 API Key** - 使用公共搜索引擎
- 📰 **新闻模式** - 专门优化新闻搜索
- 💰 **财经模式** - 专门优化财经信息搜索
- 📊 **结果去重** - 智能去重，提供更丰富的结果
- 🌐 **多源验证** - 通过多个引擎验证信息

## 使用方法

### 1. 基本搜索

```bash
python3 skills/multi-search-engine/scripts/multi_search.py "Python tutorial"
```

### 2. 获取更多结果

```bash
python3 skills/multi-search-engine/scripts/multi_search.py "USD CNY exchange rate" --limit 10
```

### 3. 财经搜索模式

```bash
python3 skills/multi-search-engine/scripts/multi_search.py "AAPL stock" --finance
```

### 4. 新闻搜索模式

```bash
python3 skills/multi-search-engine/scripts/multi_search.py "Israel Iran conflict" --news
```

### 5. JSON 格式输出

```bash
python3 skills/multi-search-engine/scripts/multi_search.py "Bitcoin price" --json
```

### 6. 列出可用引擎

```bash
python3 skills/multi-search-engine/scripts/multi_search.py --list-engines
```

## 支持的搜索引擎

| 引擎 | 状态 | 需要 API Key | 说明 |
|------|------|--------------|------|
| DuckDuckGo | ✅ 可用 | 否 | 隐私搜索引擎 |
| SearXNG | ✅ 可用 | 否 | 元搜索引擎 |
| Brave Search | 🔧 待配置 | 是 | 需要 API Key |
| Bing | 🔧 待配置 | 是 | 需要 API Key |

## 输出格式

### 文本格式

```
======================================================================
📊 搜索结果: 'USD CNY exchange rate'
======================================================================

📈 统计:
   使用引擎: duckduckgo, searx
   DuckDuckGo: 5 条结果
   SearXNG: 5 条结果
   去重后总计: 8 条

----------------------------------------------------------------------

1. USD to CNY Exchange Rate - USD/CNY Currency Rate - Reuters
   🔗 https://www.reuters.com/markets/currencies/usdcny...
   📝 Current exchange rate USD/CNY. Get live rates and charts...
   🔍 来源: DuckDuckGo

2. US Dollar to Chinese Yuan Exchange Rate. Convert USD/CNY
   🔗 https://wise.com/us/currency-converter/usd-to-cny...
   📝 Convert USD to CNY with the Wise Currency Converter...
   🔍 来源: SearXNG
...
```

### JSON 格式

```json
{
  "query": "USD CNY exchange rate",
  "engines_used": ["duckduckgo", "searx"],
  "engine_stats": {
    "DuckDuckGo": 5,
    "SearXNG": 5
  },
  "total_results": 8,
  "results": [
    {
      "title": "USD to CNY Exchange Rate...",
      "url": "https://...",
      "snippet": "Current exchange rate...",
      "engine": "DuckDuckGo",
      "rank": 1
    }
  ]
}
```

## Python API 使用

```python
from multi_search import MultiSearchEngine

# 创建搜索引擎
search = MultiSearchEngine()

# 基本搜索
results = search.search("Python tutorial", limit=5)

# 遍历结果
for result in results['results']:
    print(f"{result['title']}: {result['url']}")
    print(f"来源: {result['engine']}")
    
# 财经搜索
finance_results = search.search_finance("AAPL stock", limit=5)

# 新闻搜索
news_results = search.search_news("tech news", limit=5)
```

## 应用场景

### 1. 信息验证

通过多个搜索引擎验证信息的准确性：

```bash
python3 multi_search.py "Israel Iran conflict 2025" --news --limit 10
```

### 2. 市场研究

获取全面的市场信息：

```bash
python3 multi_search.py "China economy outlook 2025" --finance
```

### 3. 技术调研

技术问题的多角度解答：

```bash
python3 multi_search.py "Python async best practices"
```

### 4. 竞品分析

收集竞争对手信息：

```bash
python3 multi_search.py "OpenClaw alternatives" --limit 15
```

## 与其他 Skill 集成

### 与地缘风险 Dashboard 集成

```python
from multi_search import MultiSearchEngine
from risk_assessment import TimeAwareRiskAnalyzer

# 搜索最新地缘事件
search = MultiSearchEngine()
events = search.search_news("Israel Iran conflict", limit=10)

# 分析风险
analyzer = TimeAwareRiskAnalyzer("2026-03-16")
for event in events['results']:
    # 将搜索结果添加到风险分析
    analyzer.add_event(event['title'], event['url'])
```

### 与汇率预测集成

```python
from multi_search import MultiSearchEngine
from fx_forecaster import FXForecaster

search = MultiSearchEngine()
fetcher = MarketDataFetcher()
forecaster = FXForecaster()

# 搜索美联储政策预期
fed_news = search.search("Fed interest rate decision 2025", limit=5)
# 分析新闻情绪，调整预测模型
```

## 文件结构

```
skills/multi-search-engine/
├── SKILL.md                      # 本文件
└── scripts/
    └── multi_search.py           # 主脚本
```

## 网络要求

- 需要访问外部网络
- DuckDuckGo: https://duckduckgo.com
- SearXNG 实例: 多个公共实例

## 限制

- 受搜索引擎反爬机制限制
- 结果可能因网络环境而异
- 不建议高频大批量搜索

## 更新日志

### v1.0.0 (2026-03-16)
- 初始版本
- 支持 DuckDuckGo 和 SearXNG
- 新闻和财经搜索模式
- 结果去重和聚合
