#!/usr/bin/env python3
"""
获取真实市场数据 - 用于地缘风险报告
时间: 2026年3月16日
"""

import yfinance as yf
from datetime import datetime, timedelta
import json

def get_real_market_data():
    """获取真实市场数据"""
    
    print("=" * 70)
    print("📊 获取真实市场数据")
    print(f"查询时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    # 定义要获取的资产
    assets = {
        'DXY': {'ticker': 'DX-Y.NYB', 'name': '美元指数', 'type': 'index'},
        'GC': {'ticker': 'GC=F', 'name': '黄金期货', 'type': 'commodity'},
        'CL': {'ticker': 'CL=F', 'name': 'WTI原油', 'type': 'commodity'},
        'BRENT': {'ticker': 'BZ=F', 'name': '布伦特原油', 'type': 'commodity'},
        'USDCNY': {'ticker': 'CNY=X', 'name': 'USD/CNY', 'type': 'fx'},
    }
    
    results = {}
    
    for key, info in assets.items():
        try:
            ticker = yf.Ticker(info['ticker'])
            
            # 获取历史数据 (近30天)
            hist = ticker.history(period='30d')
            
            if hist.empty:
                print(f"⚠️ {info['name']} ({info['ticker']}): 无数据")
                continue
            
            # 获取最新数据
            latest = hist.iloc[-1]
            prev = hist.iloc[-2] if len(hist) > 1 else latest
            
            current_price = round(latest['Close'], 4)
            prev_price = round(prev['Close'], 4)
            change = round(current_price - prev_price, 4)
            change_pct = round((change / prev_price) * 100, 2)
            
            # 计算30天统计
            high_30d = round(hist['High'].max(), 4)
            low_30d = round(hist['Low'].min(), 4)
            start_price = round(hist['Close'].iloc[0], 4)
            total_change_pct = round(((current_price - start_price) / start_price) * 100, 2)
            
            results[key] = {
                'name': info['name'],
                'ticker': info['ticker'],
                'current': current_price,
                'previous': prev_price,
                'change': change,
                'change_pct': change_pct,
                'high_30d': high_30d,
                'low_30d': low_30d,
                'start_30d': start_price,
                'total_change_pct': total_change_pct,
                'timestamp': datetime.now().isoformat()
            }
            
            print(f"✅ {info['name']}: {current_price} ({change_pct:+.2f}%)")
            
        except Exception as e:
            print(f"❌ {info['name']} ({info['ticker']}): {e}")
    
    # 打印汇总
    print("\n" + "=" * 70)
    print("📊 30天数据汇总")
    print("=" * 70)
    print(f"{'资产':<20} {'当前价格':<15} {'30天前':<15} {'变化':<10}")
    print("-" * 70)
    
    for key, data in results.items():
        print(f"{data['name']:<20} {data['current']:<15} {data['start_30d']:<15} {data['total_change_pct']:+.2f}%")
    
    # 保存到文件
    output_file = '/root/.openclaw/workspace/skills/geopol-risk-dashboard/data/real_market_data.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 数据已保存: {output_file}")
    
    return results

if __name__ == "__main__":
    get_real_market_data()
