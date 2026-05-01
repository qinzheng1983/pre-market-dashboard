#!/usr/bin/env python3
"""
使用 Tavily 获取实时中东局势数据并生成风险报告
"""
import os
from datetime import datetime

os.environ['TAVILY_API_KEY'] = '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'

from tavily import TavilyClient

client = TavilyClient()

print("=" * 70)
print("🔍 Tavily 实时数据获取 - 中东风险报告")
print("=" * 70)

# 获取实时新闻
queries = [
    ("Israel Iran conflict latest news today March 2026", "中东冲突最新"),
    ("Strait of Hormuz closed oil price Brent March 2026", "油价与霍尔木兹"),
    ("USD CNY exchange rate Middle East conflict impact", "汇率影响")
]

all_results = {}

for query, name in queries:
    print(f"\n🔍 搜索: {name}")
    result = client.search(
        query=query,
        max_results=5,
        search_depth="advanced",
        time_range="week",
        include_answer=True
    )
    all_results[name] = result
    print(f"   ✅ 获取 {len(result.get('results', []))} 条结果")

# 生成更新摘要
print("\n" + "=" * 70)
print("📊 实时数据摘要")
print("=" * 70)

print("\n🗞️ 中东冲突动态:")
for r in all_results["中东冲突最新"].get('results', [])[:3]:
    print(f"   • {r.get('title')}")
    print(f"     {r.get('url')}")

print("\n🛢️ 能源市场:")
for r in all_results["油价与霍尔木兹"].get('results', [])[:3]:
    print(f"   • {r.get('title')}")

print("\n💱 汇率影响:")
print(f"   AI分析: {all_results['汇率影响'].get('answer', 'N/A')[:200]}...")

print("\n" + "=" * 70)
print("✅ Tavily 实时数据获取完成")
print(f"📅 时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("💳 API Credits 消耗: ~6 (advanced 搜索 2 credits × 3)")
print("=" * 70)
