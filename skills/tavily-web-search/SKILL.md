---
name: tavily-web-search
description: Tavily Web Search - AI 实时网页搜索工具。专为 LLM 和 AI Agent 设计的高性能搜索 API，每月 1000 次免费额度。
metadata:
  version: 1.0.0
  author: openclaw
  requires:
    - tavily-python>=0.7.0
    - TAVILY_API_KEY (环境变量)
---

# Tavily Web Search - AI 实时网页搜索

## 概述

Tavily 是一个专为 AI 和 LLM 设计的实时网页搜索 API，提供：

- 🔍 **实时搜索** - 访问最新网页数据
- 🤖 **AI 优化** - 专为 LLM 和 Agent 设计
- 📊 **智能答案** - 自动生成综合答案
- 🆓 **免费额度** - 每月 1000 Credits

## 安装

```bash
# 安装 SDK
pip install tavily-python --break-system-packages

# 验证安装
python3 -c "from tavily import TavilyClient; print('✅ Tavily 已安装')"
```

## 配置 API Key

### 1. 获取 API Key

1. 访问 https://app.tavily.com
2. 注册/登录账户
3. 创建 API Key
4. **每月 1000 Credits 免费额度，无需信用卡**

### 2. 设置环境变量

```bash
# Linux/macOS
export TAVILY_API_KEY="tvly-xxxxxxxx"

# 添加到 ~/.bashrc 或 ~/.zshrc 使其永久生效
echo 'export TAVILY_API_KEY="tvly-xxxxxxxx"' >> ~/.bashrc
source ~/.bashrc
```

### 3. 验证配置

```bash
python3 skills/tavily-web-search/scripts/tavily_search.py --check
```

## 使用方法

### 命令行工具

```bash
# 基础搜索
python3 skills/tavily-web-search/scripts/tavily_search.py "Israel Iran conflict"

# 深度搜索 (消耗 2 Credits)
python3 skills/tavily-web-search/scripts/tavily_search.py "China economy 2025" --depth advanced --max 10

# 获取最新新闻 (最近一周)
python3 skills/tavily-web-search/scripts/tavily_search.py "Middle East" --news

# 时间范围过滤
python3 skills/tavily-web-search/scripts/tavily_search.py "BTC price" --time-range day

# 从 URL 提取内容
python3 skills/tavily-web-search/scripts/tavily_search.py "https://example.com/article" --extract

# 简洁模式
python3 skills/tavily-web-search/scripts/tavily_search.py "OpenAI latest" --compact

# 原始 JSON 输出
python3 skills/tavily-web-search/scripts/tavily_search.py "AI news" --raw
```

### Python API

```python
from tavily import TavilyClient
import os

# 初始化客户端 (从环境变量读取 API Key)
client = TavilyClient()

# 基础搜索
response = client.search(
    query="Israel Iran latest conflict",
    max_results=5,
    search_depth="basic",
    include_answer=True
)

# 打印 AI 生成的答案
print(response['answer'])

# 打印搜索结果
for result in response['results']:
    print(f"{result['title']}: {result['url']}")
    print(f"{result['content'][:200]}...")
```

### 高级用法

```python
from tavily import TavilyClient

client = TavilyClient()

# 深度搜索 (更详细的分析)
response = client.search(
    query="China economy outlook 2025",
    max_results=10,
    search_depth="advanced",  # 消耗 2 Credits
    include_answer=True,
    include_raw_content=True,  # 包含原始网页内容
    time_range="month"  # 最近一个月
)

# 从 URL 提取内容
extract_response = client.extract(
    urls=["https://example.com/article1", "https://example.com/article2"],
    extract_depth="advanced",
    max_chars=4000
)
```

## 输出示例

### 标准搜索

```
======================================================================
🔍 搜索结果
======================================================================

🤖 AI 答案:
The Israel-Iran conflict has escalated recently with...

📊 找到 5 条结果:

1. Israel-Iran tensions escalate after missile test
   🔗 https://reuters.com/...
   📄 Tensions between Israel and Iran have escalated...
   📅 2026-03-16

2. US imposes new sanctions on Iran
   🔗 https://bloomberg.com/...
   📄 The United States announced new sanctions...
   📅 2026-03-15
```

### JSON 输出

```json
{
  "answer": "综合答案...",
  "query": "Israel Iran conflict",
  "results": [
    {
      "title": "文章标题",
      "url": "https://...",
      "content": "内容摘要...",
      "published_date": "2026-03-16"
    }
  ]
}
```

## 定价

| 功能 | Credits | 说明 |
|------|---------|------|
| Basic 搜索 | 1 | 标准搜索结果 |
| Advanced 搜索 | 2 | 深度分析 + 更详细内容 |
| Extract 内容 | 1 | 从 URL 提取内容 |
| 每月免费额度 | 1000 | 无需信用卡 |

## 应用场景

### 1. 实时新闻获取

```python
from tavily_web_search import TavilySearchClient

client = TavilySearchClient()

# 获取最新地缘冲突新闻
news = client.get_news("Israel Iran conflict", max_results=10)

for item in news['results']:
    print(f"{item['title']}: {item['published_date']}")
```

### 2. 与地缘风险分析集成

```python
# 在综合分析中使用 Tavily
from tavily import TavilyClient
from comprehensive_analysis import ComprehensiveRiskAnalyzer

analyzer = ComprehensiveRiskAnalyzer()
client = TavilyClient()

# 获取实时新闻
news_results = client.search(
    query="Israel Iran conflict latest news today",
    max_results=10,
    time_range="day",
    search_depth="advanced"
)

# 将真实新闻输入到分析器
for news in news_results['results']:
    analyzer.add_news_item(news)
```

### 3. 研究模式

```python
# 深度研究特定主题
response = client.search(
    query="US China trade war impact on global economy 2025",
    max_results=20,
    search_depth="advanced",
    include_answer=True,
    include_raw_content=True
)

# 使用 AI 生成的答案作为研究摘要
research_summary = response['answer']
```

## 参数说明

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| query | str | 必填 | 搜索查询 |
| max_results | int | 5 | 最大结果数 (1-20) |
| search_depth | str | "basic" | basic(1C) 或 advanced(2C) |
| include_answer | bool | True | 包含 AI 答案 |
| include_raw_content | bool | False | 包含原始网页内容 |
| time_range | str | None | day/week/month/year |
| include_domains | list | None | 限定域名 |
| exclude_domains | list | None | 排除域名 |

## 与其他 Skill 集成

### 与中东风险分析集成

```python
# 在 optimized_analysis.py 中使用 Tavily
from tavily import TavilyClient

def gather_news_data(self):
    client = TavilyClient()
    
    # 搜索最新新闻
    results = client.search(
        query="Israel Iran conflict latest news today",
        max_results=10,
        time_range="day",
        search_depth="advanced"
    )
    
    # 转换为统一格式
    news_items = []
    for result in results['results']:
        news_items.append({
            'source': result.get('source', 'Tavily'),
            'headline': result['title'],
            'content': result['content'],
            'url': result['url'],
            'published_date': result.get('published_date'),
            'is_real_data': True  # 标记为真实数据
        })
    
    return news_items
```

## 文件结构

```
skills/tavily-web-search/
├── SKILL.md                      # 本文件
└── scripts/
    └── tavily_search.py          # 主脚本
```

## 参考资料

- [Tavily 官网](https://tavily.com)
- [Python SDK 文档](https://docs.tavily.com/sdk/python/quick-start)
- [API 文档](https://docs.tavily.com/documentation/api-reference)

## 更新日志

### v1.0.0 (2026-03-16)
- 初始版本
- 集成 Tavily Python SDK
- 支持搜索、提取、新闻模式
- 命令行工具和 Python API
