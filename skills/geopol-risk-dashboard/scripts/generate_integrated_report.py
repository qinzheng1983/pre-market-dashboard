#!/usr/bin/env python3
"""
整合报告生成器：地缘风险 + 汇率预测
"""

import sys
sys.path.insert(0, '/root/.openclaw/workspace/skills/geopol-risk-dashboard/scripts')

from fx_forecaster import FXForecaster
from datetime import datetime
import json

def generate_integrated_report():
    """生成整合报告"""
    
    print("="*60)
    print("🌍 中东地缘风险与 USD/CNY 汇率预测报告")
    print(f"📅 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    # 初始化预测器
    forecaster = FXForecaster(base_fx=7.25)
    
    # 添加当前市场信号
    print("\n📊 输入信号:")
    print("-"*40)
    
    # 1. 地缘风险 (基于最新搜索结果)
    risk_score = 63.5
    print(f"🌐 地缘风险评分: {risk_score}/100 (HIGH)")
    forecaster.add_geopol_signal(risk_score)
    
    # 2. 中美利差
    cn_rate = 2.0
    us_rate = 4.5
    print(f"💰 中美利差: {us_rate - cn_rate:.1f}% (中国{cn_rate}% vs 美国{us_rate}%)")
    forecaster.add_interest_rate_signal(cn_rate, us_rate)
    
    # 3. 贸易顺差 (2025年中国月均)
    trade_balance = 800
    print(f"📦 贸易顺差: {trade_balance}亿美元/月")
    forecaster.add_trade_signal(trade_balance)
    
    # 4. 资本流动 (近期北向资金)
    capital_flow = -50
    print(f"💸 资本流动: {capital_flow}亿美元 (净流出)")
    forecaster.add_capital_flow_signal(capital_flow)
    
    # 5. 原油价格
    oil_price = 75
    print(f"🛢️  原油价格: ${oil_price}/桶")
    forecaster.add_oil_price_signal(oil_price)
    
    # 生成报告
    report = forecaster.generate_report()
    
    # 输出综合信号
    print("\n📈 综合信号分析:")
    print("-"*40)
    composite = report["composite"]
    print(f"   净信号得分: {composite['net_score']}")
    print(f"   升值信号: {composite['bullish_score']}")
    print(f"   贬值信号: {composite['bearish_score']}")
    print(f"   趋势判断: {composite['trend'].upper()} ({composite['intensity']})")
    
    # 输出情景分析
    print("\n🎯 三种情景预测:")
    print("-"*40)
    for scenario in report["scenarios"]:
        prob = scenario['probability'] * 100
        fx_low, fx_high = scenario['fx_range']
        print(f"\n   {scenario['name']} (概率: {prob:.0f}%)")
        print(f"   汇率区间: {fx_low:.2f} - {fx_high:.2f}")
        print(f"   触发因素: {scenario['catalyst']}")
        print(f"   对冲比例: {scenario['hedge_ratio']}%")
    
    # 输出预期汇率
    print(f"\n💱 预期汇率 (加权平均): {report['expected_fx']}")
    
    # 输出对冲建议
    print("\n💡 对冲建议:")
    print("-"*40)
    hedge = report["hedge_recommendation"]
    print(f"   推荐对冲比例: {hedge['hedge_ratio']}%")
    print(f"   策略类型: {hedge['strategy']}")
    print(f"   信心水平: {hedge['confidence']}")
    print(f"\n   推荐产品:")
    for product in hedge['products']:
        print(f"      • {product}")
    
    # 关键监测点
    print("\n⚠️  关键监测点:")
    print("-"*40)
    print("   1. 美伊谈判进展 (下一次: 2026-04-15)")
    print("   2. 美联储利率决议 (下一次: 2026-03-20)")
    print("   3. 霍尔木兹海峡航运状况")
    print("   4. 中国贸易数据 (每月10日左右发布)")
    print("   5. 北向资金流向 (每日)")
    
    # 保存报告
    output_file = "/root/.openclaw/workspace/geopol-risk-reports/integrated_fx_forecast_2026-03-16.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\n📁 报告已保存: {output_file}")
    print("="*60)
    
    return report

if __name__ == "__main__":
    generate_integrated_report()
