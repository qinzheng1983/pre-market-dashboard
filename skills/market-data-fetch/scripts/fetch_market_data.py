#!/usr/bin/env python3
"""
市场数据获取工具 - 演示版本
支持模拟数据（当 API 受限时）
"""

import argparse
import json
from datetime import datetime, timedelta
from typing import Dict, Optional
import random

class MarketDataFetcher:
    """市场数据获取器"""
    
    def __init__(self, demo_mode=False):
        self.yf = None
        self.demo_mode = demo_mode
        self._init_yfinance()
        
    def _init_yfinance(self):
        """初始化 yfinance"""
        try:
            import yfinance as yf
            self.yf = yf
            print("✅ yfinance 已加载")
        except ImportError:
            print("❌ 请先安装 yfinance: pip install yfinance")
            
    def get_stock(self, ticker: str) -> Optional[Dict]:
        """获取股票实时数据"""
        if self.demo_mode:
            return self._get_demo_stock(ticker)
            
        if not self.yf:
            return None
            
        try:
            stock = self.yf.Ticker(ticker)
            info = stock.info
            
            # 获取实时报价
            hist = stock.history(period='1d')
            if hist.empty:
                return None
                
            current = hist['Close'].iloc[-1]
            prev_close = info.get('previousClose', current)
            change = current - prev_close
            change_pct = (change / prev_close) * 100 if prev_close else 0
            
            return {
                'ticker': ticker,
                'name': info.get('longName', ticker),
                'price': round(current, 2),
                'change': round(change, 2),
                'change_percent': round(change_pct, 2),
                'volume': info.get('volume', 0),
                'market_cap': info.get('marketCap'),
                'pe_ratio': info.get('trailingPE'),
                '52_week_high': info.get('fiftyTwoWeekHigh'),
                '52_week_low': info.get('fiftyTwoWeekLow'),
                'currency': info.get('currency', 'USD'),
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            print(f"⚠️  API 错误: {e}")
            print("🔄 切换到演示模式...")
            return self._get_demo_stock(ticker)
            
    def _get_demo_stock(self, ticker: str) -> Dict:
        """生成演示数据"""
        demo_data = {
            'AAPL': {'name': 'Apple Inc.', 'price': 223.45, 'currency': 'USD'},
            'TSLA': {'name': 'Tesla Inc.', 'price': 245.67, 'currency': 'USD'},
            'MSFT': {'name': 'Microsoft Corp.', 'price': 412.34, 'currency': 'USD'},
            'GOOGL': {'name': 'Alphabet Inc.', 'price': 178.90, 'currency': 'USD'},
            'AMZN': {'name': 'Amazon.com Inc.', 'price': 195.43, 'currency': 'USD'},
            'BTC-USD': {'name': 'Bitcoin USD', 'price': 68500.00, 'currency': 'USD'},
            'ETH-USD': {'name': 'Ethereum USD', 'price': 3650.00, 'currency': 'USD'},
            '^GSPC': {'name': 'S&P 500', 'price': 5780.20, 'currency': 'USD'},
            '^DJI': {'name': 'Dow Jones', 'price': 42150.50, 'currency': 'USD'},
            '^IXIC': {'name': 'NASDAQ', 'price': 18320.80, 'currency': 'USD'},
        }
        
        base = demo_data.get(ticker, {'name': ticker, 'price': 100.0, 'currency': 'USD'})
        
        # 添加随机波动
        change_pct = random.uniform(-2.0, 2.0)
        price = base['price'] * (1 + change_pct/100)
        change = price - base['price']
        
        return {
            'ticker': ticker,
            'name': base['name'],
            'price': round(price, 2),
            'change': round(change, 2),
            'change_percent': round(change_pct, 2),
            'volume': random.randint(10000000, 50000000),
            'market_cap': random.randint(1000000000000, 3000000000000),
            'pe_ratio': round(random.uniform(20, 40), 1),
            '52_week_high': round(price * 1.2, 2),
            '52_week_low': round(price * 0.8, 2),
            'currency': base['currency'],
            'timestamp': datetime.now().isoformat(),
            'demo': True
        }
            
    def get_history(self, ticker: str, period: str = '1mo') -> Optional[Dict]:
        """获取历史数据"""
        if self.demo_mode:
            return self._get_demo_history(ticker, period)
            
        if not self.yf:
            return None
            
        try:
            stock = self.yf.Ticker(ticker)
            hist = stock.history(period=period)
            
            if hist.empty:
                return None
                
            # 转换为字典格式
            data = []
            for date, row in hist.iterrows():
                data.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'open': round(row['Open'], 4),
                    'high': round(row['High'], 4),
                    'low': round(row['Low'], 4),
                    'close': round(row['Close'], 4),
                    'volume': int(row['Volume'])
                })
                
            return {
                'ticker': ticker,
                'period': period,
                'count': len(data),
                'data': data
            }
        except Exception as e:
            print(f"⚠️  API 错误: {e}")
            print("🔄 切换到演示模式...")
            return self._get_demo_history(ticker, period)
            
    def _get_demo_history(self, ticker: str, period: str) -> Dict:
        """生成演示历史数据"""
        # 解析周期
        days_map = {'1d': 1, '5d': 5, '1mo': 22, '3mo': 66, '6mo': 132, '1y': 252}
        days = days_map.get(period, 22)
        
        # 基础价格
        base_prices = {
            'AAPL': 220, 'TSLA': 240, 'MSFT': 410, 'GOOGL': 175,
            'AMZN': 190, 'BTC-USD': 68000, 'ETH-USD': 3600
        }
        base = base_prices.get(ticker, 100)
        
        data = []
        current = base
        
        for i in range(days, 0, -1):
            date = datetime.now() - timedelta(days=i)
            change = random.uniform(-0.02, 0.02)
            
            open_p = current
            close_p = current * (1 + change)
            high_p = max(open_p, close_p) * (1 + random.uniform(0, 0.01))
            low_p = min(open_p, close_p) * (1 - random.uniform(0, 0.01))
            
            data.append({
                'date': date.strftime('%Y-%m-%d'),
                'open': round(open_p, 4),
                'high': round(high_p, 4),
                'low': round(low_p, 4),
                'close': round(close_p, 4),
                'volume': random.randint(10000000, 50000000)
            })
            
            current = close_p
            
        return {
            'ticker': ticker,
            'period': period,
            'count': len(data),
            'data': data,
            'demo': True
        }
            
    def get_fx(self, pair: str) -> Optional[Dict]:
        """获取外汇汇率"""
        if self.demo_mode:
            return self._get_demo_fx(pair)
            
        if not self.yf:
            return None
            
        try:
            # Yahoo Finance 外汇格式: USDCNY=X
            fx = self.yf.Ticker(pair)
            hist = fx.history(period='5d')
            
            if hist.empty:
                return None
                
            current = hist['Close'].iloc[-1]
            prev = hist['Close'].iloc[-2] if len(hist) > 1 else current
            change = current - prev
            change_pct = (change / prev) * 100 if prev else 0
            
            return {
                'pair': pair.replace('=X', ''),
                'rate': round(current, 4),
                'change': round(change, 4),
                'change_percent': round(change_pct, 2),
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            print(f"⚠️  API 错误: {e}")
            print("🔄 切换到演示模式...")
            return self._get_demo_fx(pair)
            
    def _get_demo_fx(self, pair: str) -> Dict:
        """生成演示外汇数据"""
        fx_rates = {
            'USDCNY': 7.2456,
            'USDEUR': 0.9234,
            'USDJPY': 151.23,
            'USDGBP': 0.7890,
            'USDCAD': 1.3567,
            'USDAUD': 1.5234,
            'USDCHF': 0.8912,
        }
        
        base_pair = pair.replace('=X', '').upper()
        base = fx_rates.get(base_pair, 1.0)
        
        change_pct = random.uniform(-0.5, 0.5)
        rate = base * (1 + change_pct/100)
        change = rate - base
        
        return {
            'pair': base_pair,
            'rate': round(rate, 4),
            'change': round(change, 4),
            'change_percent': round(change_pct, 2),
            'timestamp': datetime.now().isoformat(),
            'demo': True
        }

def main():
    parser = argparse.ArgumentParser(description='市场数据获取工具')
    parser.add_argument('--ticker', type=str, help='股票代码 (如: AAPL)')
    parser.add_argument('--history', type=str, help='历史数据周期 (1d, 5d, 1mo, 3mo, 6mo, 1y)')
    parser.add_argument('--fx', type=str, help='外汇对 (如: USDCNY=X)')
    parser.add_argument('--crypto', type=str, help='加密货币 (如: BTC-USD)')
    parser.add_argument('--index', type=str, help='指数代码 (如: ^GSPC)')
    parser.add_argument('--json', action='store_true', help='输出 JSON 格式')
    parser.add_argument('--demo', action='store_true', help='强制使用演示模式')
    
    args = parser.parse_args()
    
    print("="*60)
    print("📊 Market Data Fetch - 市场数据获取")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    fetcher = MarketDataFetcher(demo_mode=args.demo)
    
    if args.ticker and args.history:
        # 获取历史数据
        print(f"\n📈 获取 {args.ticker} 历史数据 ({args.history})")
        print("-"*40)
        result = fetcher.get_history(args.ticker, args.history)
        
        if result:
            demo_flag = " [演示数据]" if result.get('demo') else ""
            print(f"\n✅ 获取成功{demo_flag}: {result['count']} 条数据\n")
            for item in result['data'][-5:]:  # 只显示最近5条
                print(f"{item['date']}: Open={item['open']}, Close={item['close']}, Vol={item['volume']}")
        else:
            print("❌ 获取失败")
            
    elif args.ticker:
        # 获取实时数据
        print(f"\n📈 获取 {args.ticker} 实时数据")
        print("-"*40)
        result = fetcher.get_stock(args.ticker)
        
        if result:
            demo_flag = " [演示数据]" if result.get('demo') else ""
            print(f"\n📌 {result['name']} ({result['ticker']}){demo_flag}")
            print(f"   价格: {result['price']} {result['currency']}")
            print(f"   涨跌: {result['change']} ({result['change_percent']}%)")
            print(f"   成交量: {result['volume']:,}")
            if result['market_cap']:
                print(f"   市值: {result['market_cap']:,}")
            if result['pe_ratio']:
                print(f"   市盈率: {result['pe_ratio']}")
                
            if args.json:
                print("\n" + json.dumps(result, indent=2))
        else:
            print("❌ 获取失败")
            
    elif args.fx:
        # 获取外汇
        print(f"\n💱 获取外汇 {args.fx}")
        print("-"*40)
        result = fetcher.get_fx(args.fx)
        
        if result:
            demo_flag = " [演示数据]" if result.get('demo') else ""
            print(f"\n✅ {result['pair']}{demo_flag}")
            print(f"   汇率: {result['rate']}")
            print(f"   涨跌: {result['change']} ({result['change_percent']}%)")
            
            if args.json:
                print("\n" + json.dumps(result, indent=2))
        else:
            print("❌ 获取失败")
            
    elif args.crypto:
        # 获取加密货币
        print(f"\n🪙 获取加密货币 {args.crypto}")
        print("-"*40)
        result = fetcher.get_stock(args.crypto)
        
        if result:
            demo_flag = " [演示数据]" if result.get('demo') else ""
            print(f"\n✅ {result['name']}{demo_flag}")
            print(f"   价格: ${result['price']}")
            print(f"   涨跌: {result['change_percent']}%")
            print(f"   成交量: {result['volume']:,}")
            
            if args.json:
                print("\n" + json.dumps(result, indent=2))
        else:
            print("❌ 获取失败")
            
    elif args.index:
        # 获取指数
        print(f"\n📊 获取指数 {args.index}")
        print("-"*40)
        result = fetcher.get_stock(args.index)
        
        if result:
            demo_flag = " [演示数据]" if result.get('demo') else ""
            print(f"\n✅ {result['name']}{demo_flag}")
            print(f"   点位: {result['price']}")
            print(f"   涨跌: {result['change']} ({result['change_percent']}%)")
            
            if args.json:
                print("\n" + json.dumps(result, indent=2))
        else:
            print("❌ 获取失败")
    else:
        parser.print_help()
        print("\n💡 示例用法:")
        print("   python3 fetch_market_data.py --ticker AAPL")
        print("   python3 fetch_market_data.py --ticker TSLA --history 30")
        print("   python3 fetch_market_data.py --fx USDCNY=X")
        print("   python3 fetch_market_data.py --crypto BTC-USD")
        print("   python3 fetch_market_data.py --index ^GSPC")
        print("\n   # 使用演示模式 (无需 API):")
        print("   python3 fetch_market_data.py --ticker AAPL --demo")
        
    print("\n" + "="*60)
    print("📊 数据源: Yahoo Finance (通过 yfinance)")
    print("⚠️  注意: 免费 API 有限速，演示模式用于测试")
    print("="*60)

if __name__ == "__main__":
    main()
