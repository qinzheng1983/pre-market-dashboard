#!/usr/bin/env python3
"""
Real-time Data Adapter - 实时数据适配器
整合真实数据源，替代模拟数据
"""

import sys
sys.path.insert(0, '/root/.openclaw/workspace/skills/market-data-fetch/scripts')

import json
import subprocess
from datetime import datetime
from typing import Dict, List, Optional

class RealTimeDataAdapter:
    """实时数据适配器"""
    
    def __init__(self):
        self.data_quality_log = []
        
    def get_realtime_news(self, query: str = "Middle East Iran Israel conflict 2025 2026") -> List[Dict]:
        """
        获取实时新闻 - 使用 kimi-search 或 web_search
        注意：由于网络限制，当前返回提示信息
        """
        print("📡 尝试获取实时新闻...")
        
        # 记录数据质量
        self.data_quality_log.append({
            'timestamp': datetime.now().isoformat(),
            'source': 'kimi_search',
            'status': 'limited',
            'note': 'Network restrictions may apply'
        })
        
        # 由于网络限制，返回提示用户使用搜索工具
        return [{
            'source': 'System',
            'time': datetime.now().isoformat(),
            'headline': '[数据获取提示] 请使用 kimi-search 获取最新新闻',
            'impact': 'info',
            'category': 'system',
            'url': '使用: kimi_search --query "Israel Iran latest news 2025"'
        }]
    
    def get_realtime_fx_data(self, pairs: List[str] = None) -> Dict:
        """
        获取实时汇率数据
        优先使用 akshare (中国数据源)，其次 yfinance
        """
        print("📊 尝试获取实时市场数据...")
        
        if pairs is None:
            pairs = ['USDCNY', 'USDRUB', 'EURUSD']
            
        result = {}
        
        # 尝试使用 akshare 获取 USD/CNY (中国数据源)
        try:
            import akshare as ak
            print("   使用 AKShare 获取 USD/CNY...")
            fx_df = ak.currency_boc_safe()
            usdcny_row = fx_df[fx_df['货币对'] == 'USD/CNY']
            if not usdcny_row.empty:
                result['USDCNY'] = {
                    'rate': float(usdcny_row['现汇买入价'].iloc[0]),
                    'source': 'BOC (AKShare)',
                    'timestamp': datetime.now().isoformat(),
                    'status': 'real'
                }
        except Exception as e:
            print(f"   AKShare 失败: {e}")
            
        # 尝试使用 yfinance 获取其他汇率
        try:
            from fetch_market_data import MarketDataFetcher
            fetcher = MarketDataFetcher(demo_mode=False)
            
            if 'USDRUB' in pairs and 'USDRUB' not in result:
                rub_data = fetcher.get_fx('USDRUB=X')
                if rub_data and not rub_data.get('demo'):
                    result['USDRUB'] = {
                        'rate': rub_data['rate'],
                        'source': 'Yahoo Finance',
                        'timestamp': rub_data['timestamp'],
                        'status': 'real'
                    }
        except Exception as e:
            print(f"   Yahoo Finance 失败: {e}")
            
        # 如果真实数据获取失败，使用演示数据但明确标记
        if not result:
            print("   ⚠️ 无法获取实时数据，使用演示数据（已标记）")
            result = self._get_demo_fx_data()
            
        return result
    
    def _get_demo_fx_data(self) -> Dict:
        """获取演示汇率数据（明确标记）"""
        return {
            'USDCNY': {
                'rate': 7.2485,
                'source': 'DEMO DATA',
                'timestamp': datetime.now().isoformat(),
                'status': 'demo',
                'warning': '这是演示数据，请使用 akshare 获取真实汇率'
            },
            'USDRUB': {
                'rate': 92.35,
                'source': 'DEMO DATA',
                'timestamp': datetime.now().isoformat(),
                'status': 'demo',
                'warning': '这是演示数据'
            },
            '_data_quality': 'DEMO - 非真实数据'
        }
    
    def get_commodity_prices(self) -> Dict:
        """获取大宗商品价格"""
        print("📈 尝试获取商品价格...")
        
        result = {}
        
        # 尝试使用 yfinance
        try:
            from fetch_market_data import MarketDataFetcher
            fetcher = MarketDataFetcher(demo_mode=False)
            
            # 油价
            oil_data = fetcher.get_stock('BZ=F')  # 布伦特原油
            if oil_data and not oil_data.get('demo'):
                result['OIL_BRENT'] = {
                    'price': oil_data['price'],
                    'source': 'Yahoo Finance',
                    'timestamp': oil_data['timestamp'],
                    'status': 'real'
                }
                
            # 黄金
            gold_data = fetcher.get_stock('GC=F')
            if gold_data and not gold_data.get('demo'):
                result['GOLD'] = {
                    'price': gold_data['price'],
                    'source': 'Yahoo Finance',
                    'timestamp': gold_data['timestamp'],
                    'status': 'real'
                }
        except Exception as e:
            print(f"   获取失败: {e}")
            
        # 如果失败，使用演示数据
        if not result:
            result = {
                'OIL_BRENT': {
                    'price': 78.50,
                    'source': 'DEMO DATA',
                    'timestamp': datetime.now().isoformat(),
                    'status': 'demo',
                    'warning': '演示数据 - 请检查网络连接'
                },
                'GOLD': {
                    'price': 2185.00,
                    'source': 'DEMO DATA',
                    'timestamp': datetime.now().isoformat(),
                    'status': 'demo',
                    'warning': '演示数据'
                }
            }
            
        return result
    
    def get_data_quality_report(self) -> Dict:
        """获取数据质量报告"""
        return {
            'timestamp': datetime.now().isoformat(),
            'log': self.data_quality_log,
            'recommendations': [
                '使用 akshare 获取 USD/CNY: ak.fx_spot_quote()',
                '使用 yfinance 获取其他汇率: fetcher.get_fx()',
                '使用 kimi-search 获取新闻: kimi_search --query "Israel Iran news"',
                '使用 kalshi-trader 获取预测市场数据 (需API)'
            ]
        }

def print_data_source_guide():
    """打印数据源使用指南"""
    print("=" * 70)
    print("📚 真实数据获取指南")
    print("=" * 70)
    
    print("\n1️⃣ 汇率数据 (USD/CNY)")
    print("-" * 40)
    print("Python代码:")
    print("   import akshare as ak")
    print("   fx_df = ak.currency_boc_safe()")
    print("   usdcny = fx_df[fx_df['货币对'] == 'USD/CNY']")
    print("   print(usdcny['现汇买入价'])")
    
    print("\n2️⃣ 其他汇率 (USD/RUB, EUR/USD)")
    print("-" * 40)
    print("Python代码:")
    print("   from fetch_market_data import MarketDataFetcher")
    print("   fetcher = MarketDataFetcher()")
    print("   rub = fetcher.get_fx('USDRUB=X')")
    print("   print(rub['rate'])")
    
    print("\n3️⃣ 新闻数据")
    print("-" * 40)
    print("使用 kimi-search 工具:")
    print('   kimi_search --query "Israel Iran conflict latest"')
    print('   kimi_search --query "Middle East news 2025"')
    
    print("\n4️⃣ 预测市场数据")
    print("-" * 40)
    print("使用 kalshi-trader (需API Key和网络):")
    print("   python3 skills/kalshi-trader/scripts/kalshi_monitor.py --fed")
    
    print("\n5️⃣ 大宗商品价格")
    print("-" * 40)
    print("Python代码:")
    print("   oil = fetcher.get_stock('BZ=F')  # 布伦特原油")
    print("   gold = fetcher.get_stock('GC=F')  # 黄金")
    
    print("\n⚠️  当前限制:")
    print("   - 部分数据源需要外部网络访问")
    print("   - Yahoo Finance 可能有限速")
    print("   - Kalshi API 需要认证和网络")
    print("=" * 70)

def main():
    """测试数据适配器"""
    adapter = RealTimeDataAdapter()
    
    print("=" * 70)
    print("🧪 实时数据适配器测试")
    print("=" * 70)
    
    # 测试汇率数据
    print("\n测试1: 获取汇率数据")
    fx_data = adapter.get_realtime_fx_data()
    print(json.dumps(fx_data, indent=2, ensure_ascii=False))
    
    # 测试商品数据
    print("\n测试2: 获取商品数据")
    comm_data = adapter.get_commodity_prices()
    print(json.dumps(comm_data, indent=2, ensure_ascii=False))
    
    # 打印指南
    print_data_source_guide()

if __name__ == "__main__":
    main()
