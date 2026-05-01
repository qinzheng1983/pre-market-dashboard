#!/usr/bin/env python3
"""
市场数据获取工具使用示例
展示如何与地缘风险 skill 和汇率预测 skill 集成
"""

import sys
sys.path.insert(0, '/root/.openclaw/workspace/skills/market-data-fetch/scripts')
sys.path.insert(0, '/root/.openclaw/workspace/skills/geopol-risk-dashboard/scripts')

from fetch_market_data import MarketDataFetcher
from fx_forecaster import FXForecaster

def example_1_basic_stock():
    """示例1: 获取股票数据"""
    print("\n" + "="*60)
    print("示例1: 获取股票实时数据")
    print("="*60)
    
    fetcher = MarketDataFetcher(demo_mode=True)
    
    # 获取苹果股票
    aapl = fetcher.get_stock('AAPL')
    print(f"\n🍎 Apple (AAPL):")
    print(f"   价格: ${aapl['price']}")
    print(f"   涨跌: {aapl['change_percent']}%")
    print(f"   市值: ${aapl['market_cap']/1e12:.2f}T")
    
    # 获取特斯拉
    tsla = fetcher.get_stock('TSLA')
    print(f"\n🚗 Tesla (TSLA):")
    print(f"   价格: ${tsla['price']}")
    print(f"   涨跌: {tsla['change_percent']}%")

def example_2_fx_data():
    """示例2: 获取外汇数据"""
    print("\n" + "="*60)
    print("示例2: 获取外汇汇率")
    print("="*60)
    
    fetcher = MarketDataFetcher(demo_mode=True)
    
    # 获取 USD/CNY
    usdcny = fetcher.get_fx('USDCNY=X')
    print(f"\n💱 USD/CNY:")
    print(f"   汇率: {usdcny['rate']}")
    print(f"   涨跌: {usdcny['change_percent']}%")
    
    # 获取 EUR/USD
    eurusd = fetcher.get_fx('USDEUR=X')
    print(f"\n💱 EUR/USD:")
    print(f"   汇率: {eurusd['rate']}")
    print(f"   涨跌: {eurusd['change_percent']}%")

def example_3_crypto():
    """示例3: 获取加密货币"""
    print("\n" + "="*60)
    print("示例3: 获取加密货币")
    print("="*60)
    
    fetcher = MarketDataFetcher(demo_mode=True)
    
    # 获取比特币
    btc = fetcher.get_stock('BTC-USD')
    print(f"\n🪙 Bitcoin (BTC):")
    print(f"   价格: ${btc['price']:,.2f}")
    print(f"   涨跌: {btc['change_percent']}%")
    
    # 获取以太坊
    eth = fetcher.get_stock('ETH-USD')
    print(f"\n🪙 Ethereum (ETH):")
    print(f"   价格: ${eth['price']:,.2f}")
    print(f"   涨跌: {eth['change_percent']}%")

def example_4_integration():
    """示例4: 与汇率预测 skill 集成"""
    print("\n" + "="*60)
    print("示例4: 与汇率预测集成")
    print("="*60)
    
    fetcher = MarketDataFetcher(demo_mode=True)
    forecaster = FXForecaster(base_fx=7.25)
    
    # 获取市场数据
    print("\n📊 获取市场信号...")
    
    # VIX 波动率指数 (市场情绪)
    try:
        vix = fetcher.get_stock('^VIX')
        vix_level = vix['price']
        print(f"   VIX: {vix_level} ({vix['change_percent']}%)")
        # VIX > 20 通常表示市场恐慌
        if vix_level > 20:
            forecaster.add_signal('market_fear', 0.15, vix_level/50)
    except:
        pass
    
    # 原油价格 (地缘风险传导)
    try:
        oil = fetcher.get_stock('CL=F')
        oil_price = oil['price']
        print(f"   原油: ${oil_price}")
        forecaster.add_oil_price_signal(oil_price)
    except:
        pass
    
    # 黄金价格 (避险资产)
    try:
        gold = fetcher.get_stock('GC=F')
        gold_price = gold['price']
        print(f"   黄金: ${gold_price}")
    except:
        pass
    
    # 添加其他信号
    forecaster.add_geopol_signal(63.5)  # 地缘风险
    forecaster.add_interest_rate_signal(2.0, 4.5)  # 中美利差
    
    # 生成预测
    print("\n📈 生成汇率预测...")
    report = forecaster.generate_report()
    
    print(f"\n💱 预期汇率: {report['expected_fx']}")
    print(f"📊 趋势: {report['composite']['trend']}")
    print(f"💪 信心度: {report['composite']['intensity']}")
    print(f"🛡️  对冲建议: {report['hedge_recommendation']['hedge_ratio']}%")

def example_5_history():
    """示例5: 获取历史数据"""
    print("\n" + "="*60)
    print("示例5: 获取历史数据")
    print("="*60)
    
    fetcher = MarketDataFetcher(demo_mode=True)
    
    # 获取 USD/CNY 历史数据
    print("\n📊 USD/CNY 历史走势 (1个月):")
    usdcny_hist = fetcher.get_history('USDCNY=X', period='1mo')
    
    if usdcny_hist:
        data = usdcny_hist['data']
        print(f"   数据点数: {len(data)}")
        print(f"   区间: {data[0]['date']} 至 {data[-1]['date']}")
        print(f"   期初: {data[0]['close']}")
        print(f"   期末: {data[-1]['close']}")
        
        # 计算波动率
        import numpy as np
        closes = [d['close'] for d in data]
        returns = [(closes[i] - closes[i-1]) / closes[i-1] for i in range(1, len(closes))]
        volatility = np.std(returns) * np.sqrt(252) * 100  # 年化波动率
        print(f"   年化波动率: {volatility:.2f}%")

def main():
    print("="*60)
    print("📚 Market Data Fetch - 使用示例")
    print("="*60)
    
    # 运行所有示例
    example_1_basic_stock()
    example_2_fx_data()
    example_3_crypto()
    example_4_integration()
    example_5_history()
    
    print("\n" + "="*60)
    print("✅ 所有示例运行完成")
    print("="*60)
    print("\n💡 提示:")
    print("   1. 使用 --demo 参数启用演示模式")
    print("   2. 移除 --demo 可获取真实数据 (受 API 限速)")
    print("   3. 可与其他 skill 组合使用")
    print("="*60)

if __name__ == "__main__":
    main()
