#!/usr/bin/env python3
"""
Kalshi 宏观经济监测工具 (简化版)
使用 requests 直接访问 Kalshi 公共 API
"""

import argparse
import json
import requests
from datetime import datetime

KALSHI_API_BASE = "https://api.elections.kalshi.com/trade-api/v2"

def format_probability(price):
    """格式化概率"""
    if price is None:
        return "N/A"
    return f"{price*100:.1f}%"

def get_markets(series_ticker=None, status="open", limit=50):
    """获取市场列表"""
    url = f"{KALSHI_API_BASE}/markets"
    params = {"status": status, "limit": limit}
    if series_ticker:
        params["series_ticker"] = series_ticker
    
    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"❌ API 请求失败: {e}")
        return None

def get_fed_markets():
    """获取美联储利率市场"""
    print("\n🏦 美联储利率决策市场")
    print("=" * 60)
    
    data = get_markets(series_ticker="FED", limit=20)
    if not data or 'markets' not in data:
        print("未找到开放的 Fed 市场")
        return
    
    markets = data['markets']
    if not markets:
        print("未找到 Fed 市场数据")
        return
    
    for market in markets[:10]:  # 最多显示10个
        ticker = market.get('ticker', 'N/A')
        title = market.get('title', 'No title')
        yes_price = market.get('yes_ask') or market.get('last_price')
        volume = market.get('volume', 0)
        
        print(f"\n📌 {title}")
        print(f"   代码: {ticker}")
        print(f"   YES概率: {format_probability(yes_price)}")
        print(f"   交易量: {volume:,}")

def search_markets(query):
    """搜索市场"""
    print(f"\n🔍 搜索: '{query}'")
    print("=" * 60)
    
    data = get_markets(limit=100)
    if not data or 'markets' not in data:
        print("未找到市场数据")
        return
    
    query_lower = query.lower()
    matched = []
    
    for market in data['markets']:
        title = (market.get('title') or '').lower()
        ticker = (market.get('ticker') or '').lower()
        if query_lower in title or query_lower in ticker:
            matched.append(market)
    
    if not matched:
        print(f"未找到包含 '{query}' 的市场")
        return
    
    print(f"找到 {len(matched)} 个匹配市场:\n")
    
    for market in matched[:10]:
        ticker = market.get('ticker', 'N/A')
        title = market.get('title', 'No title')
        yes_price = market.get('yes_ask') or market.get('last_price')
        volume = market.get('volume', 0)
        
        print(f"📌 {title}")
        print(f"   代码: {ticker}")
        print(f"   YES概率: {format_probability(yes_price)}")
        print(f"   交易量: {volume:,}")
        print()

def get_trending_markets():
    """获取热门市场"""
    print("\n🔥 热门预测市场")
    print("=" * 60)
    
    data = get_markets(limit=50)
    if not data or 'markets' not in data:
        print("未找到市场数据")
        return
    
    # 按交易量排序
    markets = sorted(
        data['markets'],
        key=lambda x: x.get('volume', 0),
        reverse=True
    )
    
    print(f"交易量排名前 {min(10, len(markets))} 的市场:\n")
    
    for market in markets[:10]:
        ticker = market.get('ticker', 'N/A')
        title = market.get('title', 'No title')
        yes_price = market.get('yes_ask') or market.get('last_price')
        volume = market.get('volume', 0)
        
        print(f"📌 {title}")
        print(f"   代码: {ticker}")
        print(f"   YES概率: {format_probability(yes_price)}")
        print(f"   交易量: {volume:,}")
        print()

def get_econ_calendar():
    """获取经济日历"""
    print("\n📅 重要经济指标预测")
    print("=" * 60)
    
    # 关键经济指标关键词
    key_terms = ['CPI', 'GDP', 'FED', 'INFLATION', 'EMPLOYMENT', 'RATES']
    
    data = get_markets(limit=100)
    if not data or 'markets' not in data:
        print("未找到市场数据")
        return
    
    matched = []
    for market in data['markets']:
        title = (market.get('title') or '').upper()
        ticker = (market.get('ticker') or '').upper()
        for term in key_terms:
            if term in title or term in ticker:
                matched.append(market)
                break
    
    if not matched:
        print("未找到经济指标市场")
        return
    
    # 去重
    seen = set()
    unique = []
    for m in matched:
        if m['ticker'] not in seen:
            seen.add(m['ticker'])
            unique.append(m)
    
    print(f"找到 {len(unique)} 个经济指标市场:\n")
    
    for market in unique[:15]:
        ticker = market.get('ticker', 'N/A')
        title = market.get('title', 'No title')
        yes_price = market.get('yes_ask') or market.get('last_price')
        volume = market.get('volume', 0)
        
        print(f"📊 {title}")
        print(f"   代码: {ticker}")
        print(f"   市场概率: {format_probability(yes_price)}")
        print(f"   交易量: {volume:,}")
        print()

def export_json():
    """导出市场数据为 JSON"""
    data = get_markets(limit=100)
    if not data or 'markets' not in data:
        print("未找到市场数据")
        return
    
    export_data = []
    for market in data['markets']:
        export_data.append({
            'ticker': market.get('ticker'),
            'title': market.get('title'),
            'yes_price': market.get('yes_ask') or market.get('last_price'),
            'volume': market.get('volume', 0),
            'status': market.get('status')
        })
    
    output_file = '/root/.openclaw/workspace/geopol-risk-reports/kalshi_markets_export.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(export_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ 已导出 {len(export_data)} 个市场到: {output_file}")

def main():
    parser = argparse.ArgumentParser(description='Kalshi 宏观经济监测工具')
    parser.add_argument('--fed', action='store_true', help='获取美联储利率市场')
    parser.add_argument('--search', type=str, help='搜索特定市场')
    parser.add_argument('--trending', action='store_true', help='获取热门市场')
    parser.add_argument('--econ', action='store_true', help='获取经济日历')
    parser.add_argument('--export', action='store_true', help='导出市场数据为JSON')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("🎯 Kalshi 宏观经济监测工具")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    if not any([args.fed, args.search, args.trending, args.econ, args.export]):
        parser.print_help()
        print("\n💡 示例用法:")
        print("   python3 kalshi_monitor.py --fed")
        print("   python3 kalshi_monitor.py --search 'CPI'")
        print("   python3 kalshi_monitor.py --trending")
        return
    
    if args.fed:
        get_fed_markets()
    
    if args.search:
        search_markets(args.search)
    
    if args.trending:
        get_trending_markets()
    
    if args.econ:
        get_econ_calendar()
    
    if args.export:
        export_json()
    
    print("\n" + "=" * 60)
    print("📊 数据来源: Kalshi Prediction Markets (CFTC Regulated)")
    print("⚠️  免责声明: 市场概率仅供参考，不构成投资建议")
    print("=" * 60)

if __name__ == "__main__":
    main()
