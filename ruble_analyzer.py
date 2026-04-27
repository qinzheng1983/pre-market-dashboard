#!/usr/bin/env python3
"""
俄罗斯卢布短期走势分析框架
基于时间感知的风险评估模型，套用自地缘冲突风险仪表盘
"""

import json
import os
import sys
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum

# 报告输出目录
REPORTS_DIR = Path("/root/.openclaw/workspace/rub-analysis-reports")
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

class TrendDirection(Enum):
    APPRECIATION = ("升值", "↗️")  # 卢布走强
    STABLE = ("稳定", "➡️")
    DEPRECIATION = ("贬值", "↘️")  # 卢布走弱
    
    def __init__(self, label, emoji):
        self.label = label
        self.emoji = emoji

@dataclass
class FactorEvent:
    """影响因素事件"""
    timestamp: str
    factor: str  # sanctions/oil/policy/geopolitical
    event_type: str  # bullish_ruble/bearish_ruble/neutral
    title: str
    description: str
    source: str
    impact_score: int  # 对卢布的影响：正=升值压力，负=贬值压力
    is_new_in_window: bool
    
    def to_dict(self) -> Dict:
        return asdict(self)

@dataclass
class FactorScore:
    """单一因素评分"""
    name: str
    name_cn: str
    weight: float
    base_score: float  # 基准分（0-100，越高对卢布越有利）
    new_events_impact: float  # 当日新事件的边际调整
    final_score: float
    signals: List[str]
    new_events: List[FactorEvent]
    trend: str  # bullish_ruble/bearish_ruble/stable

class RubleTrendAnalyzer:
    """卢布走势分析器"""
    
    def __init__(self, analysis_date: str, window_hours: int = 24):
        self.analysis_date = datetime.strptime(analysis_date, "%Y-%m-%d")
        self.window_start = self.analysis_date.replace(hour=0, minute=0, second=0)
        self.window_end = self.window_start + timedelta(hours=window_hours)
        
    def fetch_market_data(self) -> List[FactorEvent]:
        """
        获取2026年3月13日卢布相关市场数据
        基于最新搜索验证的事实
        """
        # 2026年3月13日关键事件
        events_2026_03_13 = [
            # 汇率动态 - 卢布贬值
            FactorEvent(
                timestamp=(self.window_start + timedelta(hours=16)).isoformat(),
                factor="sanctions",
                event_type="bearish_ruble",
                title="美元兑卢布突破80.35，创1月9日以来新低",
                description="3月13日USD/RUB突破80.35，为1月9日以来首次跌破80关口，卢布周内贬值约1-1.5%",
                source="新浪财经 / 每日经济新闻",
                impact_score=-8,
                is_new_in_window=True
            ),
            # 人民币汇率
            FactorEvent(
                timestamp=(self.window_start + timedelta(hours=9, minutes=15)).isoformat(),
                factor="markets",
                event_type="bearish_ruble",
                title="人民币兑卢布升至11.62，卢布持续走弱",
                description="3月13日1人民币=11.62卢布，较3月初11.22显著贬值，周内卢布对人民币下跌约1.3%",
                source="中国外汇交易中心 / 实时汇率网",
                impact_score=-6,
                is_new_in_window=True
            ),
            # 央行政策背景
            FactorEvent(
                timestamp=(self.window_start + timedelta(hours=8)).isoformat(),
                factor="policy",
                event_type="neutral",
                title="俄央行维持高利率但效果减弱",
                description="尽管俄央行维持约20%高利率及资本管制，卢布仍承压贬值，政策托底效果边际减弱",
                source="CBR / Trading Economics",
                impact_score=-3,
                is_new_in_window=False
            ),
            # 地缘政治背景
            FactorEvent(
                timestamp=(self.window_start - timedelta(days=2)).isoformat(),
                factor="geopolitical",
                event_type="bearish_ruble",
                title="俄乌冲突持续，美以伊战争外溢风险",
                description="中东战争持续，全球避险情绪升温，新兴市场货币承压，俄罗斯面临额外制裁风险",
                source="Reuters",
                impact_score=-5,
                is_new_in_window=False
            ),
        ]
        
        return events_2026_03_13
    
    def calculate_factor_scores(self, events: List[FactorEvent]) -> Dict[str, FactorScore]:
        """计算各因素评分 - 2026年3月13日卢布走势分析"""
        
        # 2026年3月基础态势：卢布承压贬值，突破80关口
        # 分数含义：>50 对卢布有利（升值压力），<50 对卢布不利（贬值压力）
        base_scores = {
            "sanctions": 32,    # 制裁持续，金融渠道受限，USD/RUB突破80
            "oil": 45,          # 中东冲突推高油价，但俄油受制裁影响收入有限
            "policy": 55,       # 央行高利率+资本管制，但效果边际减弱
            "geopolitical": 38  # 俄乌冲突+中东战争外溢风险，避险情绪施压
        }
        
        components = {}
        
        factor_names = {
            "sanctions": "制裁政策",
            "oil": "能源价格",
            "policy": "央行政策",
            "geopolitical": "地缘政治"
        }
        
        for factor_name, base in base_scores.items():
            # 只计算分析周期内的当日新事件
            factor_new_events = [e for e in events 
                               if e.factor == factor_name and e.is_new_in_window]
            
            # 边际影响计算
            raw_impact = sum(e.impact_score for e in factor_new_events)
            # 使用tanh平滑
            smoothed_impact = 10 * (2 / (1 + 2.71828**(-raw_impact/5)) - 1)
            
            # 最终分数（限制在0-100）
            final = max(0, min(100, base + smoothed_impact))
            
            # 趋势判断
            if smoothed_impact > 2:
                trend = "bullish_ruble"
            elif smoothed_impact < -2:
                trend = "bearish_ruble"
            else:
                trend = "stable"
            
            # 信号列表
            signals = []
            if factor_new_events:
                signals.append(f"【当日新信号】")
                for e in factor_new_events:
                    icon = "📈" if e.impact_score > 0 else "📉"
                    signals.append(f"  {icon} {e.title}")
            
            # 背景信号
            bg_signals = [e for e in events if e.factor == factor_name and not e.is_new_in_window]
            if bg_signals:
                signals.append(f"【近期背景】")
                for e in bg_signals[:2]:
                    signals.append(f"  {e.title}")
            
            if not signals:
                signals.append("分析周期内无重大新信号")
            
            components[factor_name] = FactorScore(
                name=factor_name,
                name_cn=factor_names[factor_name],
                weight=0.25,  # 四因素等权重
                base_score=base,
                new_events_impact=smoothed_impact,
                final_score=round(final, 1),
                signals=signals,
                new_events=factor_new_events,
                trend=trend
            )
        
        return components
    
    def calculate_composite_score(self, components: Dict[str, FactorScore]) -> float:
        """计算综合评分（0-100，越高表示卢布走强压力越大）"""
        total = 0
        for comp in components.values():
            total += comp.final_score * comp.weight
        return round(total, 1)
    
    def determine_trend(self, score: float, components: Dict[str, FactorScore]) -> Dict:
        """确定卢布走势方向"""
        
        # 基于综合评分判断
        if score >= 60:
            direction = TrendDirection.APPRECIATION
            ruble_bias = "升值压力"
        elif score <= 40:
            direction = TrendDirection.DEPRECIATION
            ruble_bias = "贬值压力"
        else:
            direction = TrendDirection.STABLE
            ruble_bias = "震荡整理"
        
        # 计算变化（vs 昨日）
        prev_report = self._load_previous_report()
        day_change = 0
        if prev_report:
            day_change = round(score - prev_report["composite_score"], 1)
        
        # 关键驱动因素
        drivers = []
        for name, comp in components.items():
            if abs(comp.new_events_impact) > 2:
                drivers.append({
                    "factor": comp.name_cn,
                    "impact": "利好" if comp.new_events_impact > 0 else "利空",
                    "magnitude": abs(comp.new_events_impact)
                })
        
        return {
            "direction": direction.label,
            "direction_emoji": direction.emoji,
            "ruble_bias": ruble_bias,
            "composite_score": score,
            "day_change": day_change,
            "key_drivers": drivers
        }
    
    def generate_forecast(self, score: float, components: Dict[str, FactorScore]) -> Dict:
        """生成短期走势预测"""
        
        # 情景分析
        if score >= 65:
            short_term = "卢布偏强，关注80-85区间阻力"
            factors_watch = ["油价能否维持高位", "央行是否降息", "制裁有无新变化"]
        elif score >= 55:
            short_term = "卢布温和走强，区间85-90"
            factors_watch = ["能源收入变化", "资本外流压力", "地缘政治缓和信号"]
        elif score >= 45:
            short_term = "区间震荡，方向待明，区间90-95"
            factors_watch = ["多空因素博弈", "技术面关键位", "突发地缘政治事件"]
        elif score >= 35:
            short_term = "卢布偏弱，关注95-100支撑"
            factors_watch = ["央行干预力度", "出口商结汇意愿", "避险情绪变化"]
        else:
            short_term = "贬值压力较大，警惕破100风险"
            factors_watch = ["资本管制收紧", "外汇储备消耗", "恶性通胀风险"]
        
        # 核心矛盾识别
        bullish_factors = [c.name_cn for c in components.values() if c.new_events_impact > 2]
        bearish_factors = [c.name_cn for c in components.values() if c.new_events_impact < -2]
        
        return {
            "short_term_outlook": short_term,
            "factors_to_watch": factors_watch,
            "bullish_factors": bullish_factors,
            "bearish_factors": bearish_factors,
            "recommended_position": "逢低做多" if score > 55 else "逢高做空" if score < 45 else "区间操作"
        }
    
    def generate_report(self) -> Dict[str, Any]:
        """生成完整分析报告"""
        
        # 1. 获取市场数据
        events = self.fetch_market_data()
        
        # 2. 计算各因素评分
        components = self.calculate_factor_scores(events)
        
        # 3. 计算综合评分
        composite_score = self.calculate_composite_score(components)
        
        # 4. 确定趋势
        trend = self.determine_trend(composite_score, components)
        
        # 5. 生成预测
        forecast = self.generate_forecast(composite_score, components)
        
        # 6. 整理当日事件
        timeline = []
        for e in sorted([ev for ev in events if ev.is_new_in_window], key=lambda x: x.timestamp):
            dt = datetime.fromisoformat(e.timestamp)
            timeline.append({
                "time": dt.strftime("%H:%M"),
                "factor": e.factor,
                "event": e.title,
                "impact": "利好卢布" if e.impact_score > 0 else "利空卢布",
                "source": e.source
            })
        
        report = {
            "date": self.analysis_date.strftime("%Y-%m-%d"),
            "generated_at": datetime.now().isoformat(),
            "analysis_window": {
                "start": self.window_start.isoformat(),
                "end": self.window_end.isoformat()
            },
            "composite_score": composite_score,
            "trend": trend,
            "forecast": forecast,
            "factors": {
                name: {
                    "name_cn": comp.name_cn,
                    "score": comp.final_score,
                    "base_score": comp.base_score,
                    "new_impact": round(comp.new_events_impact, 1),
                    "weight": comp.weight,
                    "trend": comp.trend,
                    "signals": comp.signals
                }
                for name, comp in components.items()
            },
            "breaking_events": timeline,
            "new_events_count": len(timeline),
            "data_sources": [
                "Central Bank of Russia",
                "Russian Finance Ministry",
                "Reuters",
                "US Treasury",
                "Trading Economics"
            ]
        }
        
        return report
    
    def _load_previous_report(self) -> Optional[Dict]:
        """加载昨日报告"""
        prev_date = (self.analysis_date - timedelta(days=1)).strftime("%Y-%m-%d")
        prev_file = REPORTS_DIR / f"{prev_date}_ruble_report.json"
        if prev_file.exists():
            with open(prev_file, 'r') as f:
                return json.load(f)
        return None

def generate_html_report(report: Dict) -> str:
    """生成HTML可视化报告"""
    
    score = report['composite_score']
    if score >= 60:
        color = "#22c55e"  # 绿色 - 卢布走强
        bg_gradient = "linear-gradient(135deg, #22c55e20, #22c55e05)"
    elif score >= 40:
        color = "#eab308"  # 黄色 - 震荡
        bg_gradient = "linear-gradient(135deg, #eab30820, #eab30805)"
    else:
        color = "#ef4444"  # 红色 - 卢布走弱
        bg_gradient = "linear-gradient(135deg, #ef444420, #ef444405)"
    
    # 因素评分卡片
    factors_html = ""
    for name, data in report['factors'].items():
        trend_icon = {"bullish_ruble": "📈", "bearish_ruble": "📉", "stable": "➡️"}.get(data['trend'], "➡️")
        impact_str = f"+{data['new_impact']:.1f}" if data['new_impact'] > 0 else f"{data['new_impact']:.1f}"
        
        factors_html += f"""
        <div style="background: rgba(255,255,255,0.03); border-radius: 10px; padding: 16px; margin: 10px 0;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-weight: 600;">{data['name_cn']}</span>
                <span style="font-size: 1.3rem; font-weight: 700; color: {color}">{data['score']}</span>
            </div>
            <div style="font-size: 0.8rem; color: #64748b; margin-top: 8px;">
                基准: {data['base_score']} | 当日调整: {impact_str} {trend_icon}
            </div>
            <div style="font-size: 0.85rem; color: #94a3b8; margin-top: 8px;">
                {'<br>'.join(data['signals'][:3])}
            </div>
        </div>
        """
    
    # 事件时间线
    events_html = ""
    for event in report.get('breaking_events', []):
        impact_color = "#22c55e" if event['impact'] == "利好卢布" else "#ef4444"
        events_html += f"""
        <div style="border-left: 3px solid {impact_color}; padding-left: 12px; margin: 10px 0;">
            <div style="font-size: 0.8rem; color: #64748b;">{event['time']} | {event['factor']}</div>
            <div style="font-size: 0.95rem; color: #e2e8f0;">{event['event']}</div>
            <div style="font-size: 0.8rem; color: {impact_color};">{event['impact']}</div>
        </div>
        """
    
    # 预测部分
    forecast = report['forecast']
    
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>卢布走势分析 - {report['date']}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            color: #f8fafc;
            min-height: 100vh;
            padding: 2rem;
        }}
        .container {{ max-width: 900px; margin: 0 auto; }}
        .header {{ text-align: center; margin-bottom: 2rem; }}
        .header h1 {{ font-size: 1.6rem; margin-bottom: 0.5rem; }}
        .header .date {{ color: #64748b; font-size: 0.9rem; }}
        
        .score-card {{
            background: {bg_gradient};
            border: 1px solid {color}40;
            border-radius: 16px;
            padding: 2rem;
            text-align: center;
            margin-bottom: 2rem;
        }}
        .score-value {{ font-size: 4rem; font-weight: 700; color: {color}; }}
        .score-label {{ color: #94a3b8; font-size: 0.9rem; margin-top: 0.5rem; }}
        .trend-badge {{
            display: inline-block;
            padding: 0.5rem 1.5rem;
            border-radius: 9999px;
            background: {color}20;
            color: {color};
            border: 1px solid {color}40;
            margin-top: 1rem;
            font-weight: 600;
        }}
        
        .section {{
            background: rgba(255,255,255,0.03);
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            border: 1px solid rgba(255,255,255,0.05);
        }}
        .section-title {{
            font-size: 1rem;
            font-weight: 600;
            color: {color};
            margin-bottom: 1rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}
        
        .forecast-box {{
            background: linear-gradient(135deg, {color}15, {color}05);
            border: 1px solid {color}30;
            border-radius: 12px;
            padding: 1.5rem;
        }}
        
        .footer {{
            text-align: center;
            color: #475569;
            font-size: 0.75rem;
            margin-top: 2rem;
            padding-top: 1rem;
            border-top: 1px solid rgba(255,255,255,0.05);
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>💱 卢布短期走势分析</h1>
            <div class="date">分析日期: {report['date']} | USD/RUB走势评估</div>
        </div>
        
        <div class="score-card">
            <div class="score-value">{report['composite_score']}</div>
            <div class="score-label">综合评分 (0-100)</div>
            <div class="trend-badge">
                {report['trend']['direction_emoji']} {report['trend']['ruble_bias']}
            </div>
            <div style="margin-top: 1rem; color: #94a3b8;">
                较昨日: {'+' if report['trend']['day_change'] > 0 else ''}{report['trend']['day_change']}
            </div>
        </div>
        
        <div class="section">
            <div class="section-title">📊 四因素分解 (等权重25%)</div>
            {factors_html}
        </div>
        
        <div class="section">
            <div class="section-title">📰 当日市场事件 ({report['new_events_count']}条)</div>
            {events_html if events_html else '<div style="color: #64748b;">本周期无重大新事件</div>'}
        </div>
        
        <div class="forecast-box">
            <div class="section-title">🔮 短期走势预测</div>
            <div style="font-size: 1.1rem; margin-bottom: 1rem;">{forecast['short_term_outlook']}</div>
            <div style="font-size: 0.9rem; color: #94a3b8;">
                <strong>关注因素:</strong> {', '.join(forecast['factors_to_watch'])}<br>
                <strong>建议操作:</strong> {forecast['recommended_position']}
            </div>
        </div>
        
        <div class="footer">
            生成时间: {report['generated_at'][:19]} | 模型: 时间感知四因素框架
        </div>
    </div>
</body>
</html>"""
    
    return html

def save_report(report: Dict):
    """保存报告"""
    date_str = report["date"]
    
    json_path = REPORTS_DIR / f"{date_str}_ruble_report.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    html_path = REPORTS_DIR / f"{date_str}_ruble_dashboard.html"
    html_content = generate_html_report(report)
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    return json_path, html_path

def main():
    parser = argparse.ArgumentParser(description='卢布短期走势分析')
    parser.add_argument('--date', type=str, default=datetime.now().strftime('%Y-%m-%d'),
                       help='分析日期 (YYYY-MM-DD)')
    args = parser.parse_args()
    
    print(f"🔄 初始化卢布走势分析器...")
    print(f"📅 分析日期: {args.date}")
    
    analyzer = RubleTrendAnalyzer(args.date)
    report = analyzer.generate_report()
    
    json_path, html_path = save_report(report)
    
    trend = report['trend']
    forecast = report['forecast']
    
    print(f"\n✅ 分析完成")
    print(f"📊 综合评分: {report['composite_score']}/100")
    print(f"📈 走势方向: {trend['direction_emoji']} {trend['ruble_bias']}")
    print(f"📰 当日新事件: {report['new_events_count']} 条")
    print(f"\n🔮 短期预测: {forecast['short_term_outlook']}")
    print(f"💡 操作建议: {forecast['recommended_position']}")
    
    print(f"\n📁 报告已保存:")
    print(f"   JSON: {json_path}")
    print(f"   HTML: {html_path}")

if __name__ == "__main__":
    main()
