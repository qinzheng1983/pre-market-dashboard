#!/usr/bin/env python3
"""
Optimized Comprehensive Analysis - 优化版综合分析
明确区分真实数据与模拟数据，提供数据质量报告
"""

import sys
sys.path.insert(0, '/root/.openclaw/workspace/skills/geopol-risk-dashboard/scripts')

import json
import argparse
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class RiskAssessment:
    """风险评估结果"""
    timestamp: str
    region: str
    risk_score: float
    risk_level: str
    trend: str
    key_events: List[Dict]
    outlook: str
    data_quality: str  # 新增：数据质量标记

@dataclass
class FXAnalysis:
    """汇率分析结果"""
    pair: str
    current_rate: float
    predicted_range: tuple
    impact_factors: List[str]
    recommendation: str
    data_source: str  # 新增：数据来源
    data_status: str  # 新增：数据状态 (real/demo)

class OptimizedComprehensiveAnalyzer:
    """优化版综合风险分析器"""
    
    def __init__(self):
        self.report_data = {}
        self.data_sources = {}  # 追踪数据来源
        
    def gather_news_data(self, query: str = "Middle East Iran Israel conflict") -> List[Dict]:
        """获取新闻数据 - 明确标记为模拟数据"""
        print("📡 新闻数据采集...")
        
        # 重要提示：由于网络限制，当前使用结构化模板
        # 建议用户使用 kimi-search 获取真实新闻
        
        news_items = [
            {
                "source": "[数据来源提示]",
                "time": datetime.now().isoformat(),
                "headline": "请使用以下命令获取真实新闻数据",
                "impact": "info",
                "category": "system",
                "action_required": "运行: kimi_search --query 'Israel Iran latest news'",
                "is_real_data": False
            },
            {
                "source": "Template",
                "time": (datetime.now() - timedelta(hours=2)).isoformat(),
                "headline": "[示例] 美国制裁伊朗石油出口 (需验证)",
                "impact": "high",
                "category": "sanctions",
                "is_real_data": False,
                "warning": "这是模板数据，非实时新闻"
            },
            {
                "source": "Template",
                "time": (datetime.now() - timedelta(hours=4)).isoformat(),
                "headline": "[示例] 红海航运安全局势 (需验证)",
                "impact": "medium",
                "category": "shipping",
                "is_real_data": False,
                "warning": "这是模板数据，非实时新闻"
            }
        ]
        
        self.data_sources['news'] = {
            'status': 'template',
            'note': '使用结构化模板，建议用 kimi-search 获取真实新闻'
        }
        
        print(f"   ⚠️  使用模板数据（非实时），建议用 kimi-search 获取真实新闻")
        return news_items
    
    def gather_market_data(self) -> Dict:
        """采集市场数据 - 尝试真实数据源"""
        print("📊 市场数据采集...")
        
        market_data = {}
        data_status = {}
        
        # 1. 尝试 AKShare 获取 USD/CNY (中国银行数据源)
        try:
            import akshare as ak
            print("   尝试 AKShare 获取 USD/CNY...")
            fx_df = ak.fx_spot_quote()
            if fx_df is not None and not fx_df.empty:
                # 查找 USD/CNY
                usdcny_row = fx_df[fx_df['货币对'] == 'USD/CNY']
                if not usdcny_row.empty:
                    buy_rate = usdcny_row['买报价'].iloc[0]
                    sell_rate = usdcny_row['卖报价'].iloc[0]
                    if pd.notna(buy_rate):
                        market_data['USDCNY'] = {
                            'rate': float(buy_rate),
                            'sell_rate': float(sell_rate),
                            'source': 'AKShare (中国银行)',
                            'status': 'real',
                            'timestamp': datetime.now().isoformat()
                        }
                        data_status['USDCNY'] = '✅ 真实数据 (AKShare)'
                        print(f"   ✅ USD/CNY: {buy_rate} (AKShare)")
        except Exception as e:
            print(f"   ❌ AKShare 失败: {e}")
            data_status['USDCNY'] = f'❌ 失败: {e}'
        
        # 2. 尝试 yfinance 获取其他数据
        try:
            sys.path.insert(0, '/root/.openclaw/workspace/skills/market-data-fetch/scripts')
            from fetch_market_data import MarketDataFetcher
            fetcher = MarketDataFetcher(demo_mode=False)
            
            # USD/RUB
            print("   尝试 yfinance 获取 USD/RUB...")
            rub_data = fetcher.get_fx('USDRUB=X')
            if rub_data and not rub_data.get('demo'):
                market_data['USDRUB'] = {
                    'rate': rub_data['rate'],
                    'source': 'Yahoo Finance',
                    'status': 'real',
                    'timestamp': rub_data.get('timestamp', datetime.now().isoformat())
                }
                data_status['USDRUB'] = '✅ 真实数据 (Yahoo)'
                print(f"   ✅ USD/RUB: {rub_data['rate']} (Yahoo)")
            else:
                raise Exception("返回演示数据或失败")
        except Exception as e:
            print(f"   ❌ Yahoo Finance 失败: {e}")
            data_status['USDRUB'] = f'❌ 失败: {e}'
        
        # 3. 尝试获取油价
        try:
            from fetch_market_data import MarketDataFetcher
            fetcher = MarketDataFetcher(demo_mode=False)
            
            print("   尝试获取油价...")
            oil_data = fetcher.get_stock('BZ=F')
            if oil_data and not oil_data.get('demo'):
                market_data['OIL_BRENT'] = {
                    'price': oil_data['price'],
                    'source': 'Yahoo Finance',
                    'status': 'real',
                    'timestamp': oil_data.get('timestamp', datetime.now().isoformat())
                }
                data_status['OIL_BRENT'] = '✅ 真实数据 (Yahoo)'
                print(f"   ✅ 油价: {oil_data['price']} (Yahoo)")
            else:
                raise Exception("返回演示数据")
        except Exception as e:
            print(f"   ❌ 油价获取失败: {e}")
            data_status['OIL_BRENT'] = f'❌ 失败: {e}'
        
        # 4. 对于失败的数据，使用演示数据但明确标记
        if 'USDCNY' not in market_data:
            print("   ⚠️  USD/CNY 使用演示数据")
            market_data['USDCNY'] = {
                'rate': 7.2485,
                'source': 'DEMO DATA (演示数据)',
                'status': 'demo',
                'timestamp': datetime.now().isoformat(),
                'warning': '这是演示数据，请使用 akshare 获取真实汇率: ak.fx_spot_quote()'
            }
        
        if 'USDRUB' not in market_data:
            print("   ⚠️  USD/RUB 使用演示数据")
            market_data['USDRUB'] = {
                'rate': 92.35,
                'source': 'DEMO DATA (演示数据)',
                'status': 'demo',
                'timestamp': datetime.now().isoformat(),
                'warning': '这是演示数据'
            }
        
        if 'OIL_BRENT' not in market_data:
            print("   ⚠️  油价使用演示数据")
            market_data['OIL_BRENT'] = {
                'price': 78.50,
                'source': 'DEMO DATA (演示数据)',
                'status': 'demo',
                'timestamp': datetime.now().isoformat(),
                'warning': '这是演示数据'
            }
        
        # 黄金和美元指数
        market_data['GOLD'] = {
            'price': 2185.00,
            'source': 'DEMO DATA (演示数据)',
            'status': 'demo',
            'timestamp': datetime.now().isoformat()
        }
        market_data['DXY'] = {
            'value': 103.85,
            'source': 'DEMO DATA (演示数据)',
            'status': 'demo',
            'timestamp': datetime.now().isoformat()
        }
        
        self.data_sources['market'] = data_status
        
        print(f"\n   数据获取状态:")
        for key, status in data_status.items():
            print(f"      {key}: {status}")
        
        return market_data
    
    def assess_geopol_risk(self, news_items: List[Dict]) -> RiskAssessment:
        """评估地缘风险"""
        print("🔥 地缘风险评估...")
        
        # 检查是否有真实新闻数据
        has_real_news = any(n.get('is_real_data', False) for n in news_items)
        
        if not has_real_news:
            print("   ⚠️  使用基于模板的风险评估（非实时）")
        
        # 基于新闻计算风险分数
        base_score = 50
        
        for news in news_items:
            if news.get('impact') == "high":
                base_score += 8
            elif news.get('impact') == "medium":
                base_score += 4
            elif news.get('impact') == "low":
                base_score += 1
        
        risk_score = min(100, max(0, base_score))
        
        if risk_score >= 70:
            risk_level = "🔴 HIGH"
            trend = "escalating"
        elif risk_score >= 50:
            risk_level = "🟠 ELEVATED"
            trend = "stable"
        elif risk_score >= 30:
            risk_level = "🟡 MODERATE"
            trend = "stable"
        else:
            risk_level = "🟢 LOW"
            trend = "de-escalating"
        
        if trend == "escalating":
            outlook = "风险持续升级，建议密切监控军事动态和制裁政策"
        elif trend == "stable":
            outlook = "风险维持在高位，关注外交谈判进展"
        else:
            outlook = "风险趋于缓和，但仍需保持警惕"
        
        data_quality = "TEMPLATE DATA (模板数据)" if not has_real_news else "REAL DATA (真实数据)"
        
        return RiskAssessment(
            timestamp=datetime.now().isoformat(),
            region="Middle East (Israel-Iran)",
            risk_score=risk_score,
            risk_level=risk_level,
            trend=trend,
            key_events=news_items,
            outlook=outlook,
            data_quality=data_quality
        )
    
    def analyze_usdcny(self, market_data: Dict, risk_assessment: RiskAssessment) -> FXAnalysis:
        """USD/CNY 汇率分析"""
        print("💱 USD/CNY 分析...")
        
        usdcny_data = market_data.get('USDCNY', {})
        current = usdcny_data.get('rate', 7.2485)
        data_source = usdcny_data.get('source', 'DEMO')
        data_status = usdcny_data.get('status', 'demo')
        
        risk_score = risk_assessment.risk_score
        
        if risk_score >= 70:
            predicted_low = current * 1.02
            predicted_high = current * 1.08
            factors = [
                "地缘冲突升级导致避险需求上升",
                "油价上涨推升中国进口成本",
                "资本外流压力增加"
            ]
            recommendation = "提升至75-85%对冲比例，考虑购买美元看涨期权"
        elif risk_score >= 50:
            predicted_low = current * 1.01
            predicted_high = current * 1.05
            factors = [
                "地缘紧张局势支撑美元",
                "中美利差维持高位",
                "贸易顺差部分抵消贬值压力"
            ]
            recommendation = "维持65-75%对冲比例，关注谈判进展"
        else:
            predicted_low = current * 0.98
            predicted_high = current * 1.02
            factors = [
                "地缘风险缓和",
                "人民币资产吸引力回升"
            ]
            recommendation = "维持50-60%对冲比例"
        
        return FXAnalysis(
            pair="USD/CNY",
            current_rate=current,
            predicted_range=(round(predicted_low, 4), round(predicted_high, 4)),
            impact_factors=factors,
            recommendation=recommendation,
            data_source=data_source,
            data_status=data_status
        )
    
    def generate_report(self) -> str:
        """生成优化版报告"""
        print("\n" + "="*70)
        print("📋 生成优化版报告...")
        print("="*70)
        
        # 采集数据
        news = self.gather_news_data()
        market = self.gather_market_data()
        
        # 分析
        risk = self.assess_geopol_risk(news)
        usdcny = self.analyze_usdcny(market, risk)
        
        # 生成报告
        report = []
        report.append("# 🌍 优化版地缘风险与汇率分析报告")
        report.append(f"\n**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"**数据周期**: 实时数据尝试 + 模拟数据补充")
        report.append(f"**报告版本**: v3.1 (数据质量优化版)")
        
        # ⚠️ 数据质量警告
        report.append("\n---\n")
        report.append("## ⚠️ 数据质量声明")
        report.append("\n**重要提示**: 本报告的数据来源情况如下：")
        report.append("\n| 数据类型 | 来源 | 状态 |")
        report.append("|----------|------|------|")
        
        # 市场数据状态
        for key, data in market.items():
            if isinstance(data, dict):
                status = "✅ 真实" if data.get('status') == 'real' else "⚠️ 演示"
                source = data.get('source', 'Unknown')
                report.append(f"| {key} | {source} | {status} |")
        
        report.append(f"| 新闻数据 | Template | ⚠️ 模板 |")
        
        report.append("\n**获取真实数据的方法**:")
        report.append("```bash")
        report.append("# 1. 获取 USD/CNY (推荐)")
        report.append("python3 -c \"import akshare as ak; print(ak.fx_spot_quote())\"")
        report.append("")
        report.append("# 2. 获取新闻")
        report.append('kimi_search --query "Israel Iran conflict latest 2025"')
        report.append("")
        report.append("# 3. 获取市场数据")
        report.append("python3 skills/market-data-fetch/scripts/fetch_market_data.py --fx USDCNY=X")
        report.append("```")
        
        # 执行摘要
        report.append("\n---\n")
        report.append("## 📌 执行摘要")
        report.append(f"\n- **地缘风险等级**: {risk.risk_level} ({risk.risk_score}/100)")
        report.append(f"  - *数据质量: {risk.data_quality}*")
        report.append(f"- **USD/CNY 当前**: {usdcny.current_rate}")
        report.append(f"  - *数据来源: {usdcny.data_source} ({usdcny.data_status})*")
        report.append(f"- **预测区间**: {usdcny.predicted_range[0]} - {usdcny.predicted_range[1]}")
        report.append(f"- **对冲建议**: {usdcny.recommendation}")
        
        # 详细分析...
        # (此处省略详细分析部分，与之前类似)
        
        return "\n".join(report)

def main():
    parser = argparse.ArgumentParser(description='Optimized Geopolitical Risk & FX Analysis')
    parser.add_argument('--output', type=str, default='optimized_report.md', help='输出文件名')
    
    args = parser.parse_args()
    
    print("="*70)
    print("🌍 优化版地缘风险与汇率分析系统")
    print("="*70)
    print("\n✨ 优化特性:")
    print("   - 明确标记真实数据与演示数据")
    print("   - 提供数据获取方法指南")
    print("   - 优先尝试真实数据源 (AKShare, Yahoo Finance)")
    print()
    
    analyzer = OptimizedComprehensiveAnalyzer()
    report = analyzer.generate_report()
    
    # 保存报告
    output_path = f"/root/.openclaw/workspace/geopol-risk-reports/{args.output}"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n✅ 报告已保存: {output_path}")
    print("\n⚠️  提示: 本报告包含演示数据，请参考报告中的'数据质量声明'部分")
    print("   了解如何获取真实数据。")

if __name__ == "__main__":
    # 导入 pandas 用于 akshare
    try:
        import pandas as pd
    except ImportError:
        pass
    
    main()
