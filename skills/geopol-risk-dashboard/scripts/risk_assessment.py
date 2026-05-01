#!/usr/bin/env python3
"""
Geopolitical Risk Assessment Dashboard - Time-Aware Version v2
关键修复：严格时间线验证，明确区分实时数据与历史数据
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

# Configuration
REPORTS_DIR = Path("/root/.openclaw/workspace/geopol-risk-reports")
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

# 数据新鲜度配置
MAX_DATA_AGE_HOURS = 48

class DataMode(Enum):
    REALTIME = "realtime"
    HISTORICAL = "historical"
    SIMULATION = "simulation"
    STALE = "stale"

class RiskLevel(Enum):
    LOW = (0, 30, "LOW", "🟢")
    ELEVATED = (30, 50, "ELEVATED", "🟡")
    HIGH = (50, 70, "HIGH", "🟠")
    CRITICAL = (70, 100, "CRITICAL", "🔴")
    
    def __init__(self, min_val, max_val, label, emoji):
        self.min_val = min_val
        self.max_val = max_val
        self.label = label
        self.emoji = emoji
    
    @classmethod
    def from_score(cls, score: float):
        for level in cls:
            if level.min_val <= score < level.max_val:
                return level
        return cls.CRITICAL if score >= 70 else cls.LOW

@dataclass
class RiskEvent:
    timestamp: str
    actual_date: str
    category: str
    sub_category: str
    event_type: str
    title: str
    description: str
    source: str
    impact_score: int
    is_new_in_window: bool
    verified: bool = False
    
    def to_dict(self):
        return asdict(self)

@dataclass
class ComponentScore:
    name: str
    weight: float
    base_score: float
    new_events_impact: float
    final_score: float
    signals: List[str]
    new_events: List[RiskEvent]
    trend: str

class TimeAwareRiskAnalyzer:
    def __init__(self, analysis_date: str, window_hours: int = 24, use_historical: bool = False):
        self.analysis_date = datetime.strptime(analysis_date, "%Y-%m-%d")
        self.window_start = self.analysis_date.replace(hour=0, minute=0, second=0)
        self.window_end = self.window_start + timedelta(hours=window_hours)
        self.use_historical = use_historical
        self.data_mode = DataMode.REALTIME
        self.warnings = []
        
    def validate_data_freshness(self, events: List[RiskEvent]) -> bool:
        if not events:
            return False
        matching_events = [e for e in events if e.actual_date == self.analysis_date.strftime("%Y-%m-%d")]
        if len(matching_events) == 0:
            event_dates = set(e.actual_date for e in events)
            self.warnings.append(
                f"数据日期不匹配: 分析日期为 {self.analysis_date.strftime('%Y-%m-%d')}，"
                f"但事件日期为 {', '.join(sorted(event_dates))}"
            )
            return False
        return True
    
    def fetch_realtime_data(self) -> List[RiskEvent]:
        # TODO: 接入真实搜索API
        return []
    
    def fetch_historical_data(self, target_date: str) -> List[RiskEvent]:
        historical_db = {
            "2025-03-13": [
                RiskEvent(
                    timestamp="2025-03-13T14:00:00",
                    actual_date="2025-03-13",
                    category="official",
                    sub_category="us_policy",
                    event_type="escalation",
                    title="美国制裁伊朗石油部长及航运网络",
                    description="美国财政部宣布制裁伊朗石油部长Mohsen Paknejad及17家航运公司",
                    source="US Treasury / Reuters",
                    impact_score=+6,
                    is_new_in_window=True,
                    verified=True
                ),
                RiskEvent(
                    timestamp="2025-03-13T10:30:00",
                    actual_date="2025-03-13",
                    category="diplomatic",
                    sub_category="e3_policy",
                    event_type="escalation",
                    title="英国威胁触发JCPOA回弹制裁机制",
                    description="英国在联合国安理会会议上威胁启动JCPOA回弹机制",
                    source="UK/UNSC / Reuters",
                    impact_score=+5,
                    is_new_in_window=True,
                    verified=True
                ),
                RiskEvent(
                    timestamp="2025-03-13T09:00:00",
                    actual_date="2025-03-13",
                    category="official",
                    sub_category="internal",
                    event_type="stable",
                    title="哈梅内伊任命新的执法部队意识形态负责人",
                    description="伊朗最高领袖任命Ali Shirazi为执法部队政治意识形态组织负责人",
                    source="Defapress / ISW",
                    impact_score=+1,
                    is_new_in_window=True,
                    verified=True
                ),
            ],
            "2025-03-12": [
                RiskEvent(
                    timestamp="2025-03-12T18:00:00",
                    actual_date="2025-03-12",
                    category="official",
                    sub_category="regional",
                    event_type="escalation",
                    title="伊朗、俄罗斯、中国外长准备北京会晤",
                    description="三国副外长级会议定于3月14日在北京举行",
                    source="Reuters / ISW",
                    impact_score=+3,
                    is_new_in_window=False,
                    verified=True
                ),
            ],
            "2025-03-11": [
                RiskEvent(
                    timestamp="2025-03-11T12:00:00",
                    actual_date="2025-03-11",
                    category="military",
                    sub_category="proxy",
                    event_type="escalation",
                    title="胡塞武装宣布恢复对国际航运的攻击",
                    description="也门胡塞武装宣布自3月11日起恢复对国际航运的攻击行动",
                    source="Houthi Statement / ISW",
                    impact_score=+5,
                    is_new_in_window=False,
                    verified=True
                ),
                RiskEvent(
                    timestamp="2025-03-11T10:00:00",
                    actual_date="2025-03-11",
                    category="markets",
                    sub_category="currency",
                    event_type="escalation",
                    title="伊朗里亚尔跌至历史新低",
                    description="伊朗货币兑美元汇率跌至923,050:1的历史新低",
                    source="Reuters / Al Jazeera",
                    impact_score=+4,
                    is_new_in_window=False,
                    verified=True
                ),
            ],
        }
        return historical_db.get(target_date, [])
    
    def get_data(self):
        target_date = self.analysis_date.strftime("%Y-%m-%d")
        
        # 1. 尝试获取实时数据
        realtime_events = self.fetch_realtime_data()
        if realtime_events and self.validate_data_freshness(realtime_events):
            return realtime_events, DataMode.REALTIME
        
        # 2. 检查是否允许使用历史数据
        if not self.use_historical:
            self.warnings.append(
                f"无 {target_date} 的实时数据可用。"
                f"请使用 --use-historical 参数查看历史归档，或接入实时API。"
            )
            return [], DataMode.STALE
        
        # 3. 获取历史数据
        historical_events = self.fetch_historical_data(target_date)
        
        if historical_events:
            if all(e.actual_date == target_date for e in historical_events):
                return historical_events, DataMode.HISTORICAL
            else:
                self.warnings.append(
                    f"历史数据日期不匹配: 请求 {target_date}，"
                    f"获得 {historical_events[0].actual_date}"
                )
                return historical_events, DataMode.HISTORICAL
        
        # 4. 无数据可用
        self.warnings.append(f"无 {target_date} 的数据可用（实时或历史）")
        return [], DataMode.STALE
    
    def calculate_component_scores(self, events: List[RiskEvent]) -> Dict[str, ComponentScore]:
        base_scores = {
            "official": 52,
            "military": 38,
            "markets": 48,
            "diplomatic": 42
        }
        
        components = {}
        
        for comp_name, base in base_scores.items():
            comp_new_events = [e for e in events 
                              if e.category == comp_name and e.is_new_in_window]
            
            raw_impact = sum(e.impact_score for e in comp_new_events)
            smoothed_impact = 12 * (2 / (1 + 2.71828**(-raw_impact/6)) - 1)
            final = max(0, min(100, base + smoothed_impact))
            
            if smoothed_impact > 2:
                trend = "escalating"
            elif smoothed_impact < -2:
                trend = "de-escalating"
            else:
                trend = "stable"
            
            signals = []
            if comp_new_events:
                signals.append("【当日新信号】")
                for e in comp_new_events:
                    signals.append(f"  (+{e.impact_score}) {e.title}")
            
            bg_signals = [e for e in events if e.category == comp_name and not e.is_new_in_window]
            if bg_signals:
                signals.append("【近期背景】")
                for e in bg_signals[:2]:
                    signals.append(f"  ({e.actual_date}) {e.title}")
            
            if not signals:
                signals.append("分析周期内无重大新信号")
            
            components[comp_name] = ComponentScore(
                name=comp_name,
                weight={"official": 0.30, "military": 0.30, "markets": 0.30, "diplomatic": 0.10}[comp_name],
                base_score=base,
                new_events_impact=smoothed_impact,
                final_score=round(final, 1),
                signals=signals,
                new_events=comp_new_events,
                trend=trend
            )
        
        return components
    
    def calculate_total_risk(self, components: Dict[str, ComponentScore]) -> float:
        total = 0
        for comp in components.values():
            total += comp.final_score * comp.weight
        return round(total, 1)
    
    def generate_report(self) -> Dict[str, Any]:
        # 1. 获取数据及模式
        events, data_mode = self.get_data()
        self.data_mode = data_mode
        
        # 2. 计算评分
        components = self.calculate_component_scores(events)
        total_score = self.calculate_total_risk(components)
        risk_level = RiskLevel.from_score(total_score)
        
        # 3. 与昨日对比
        prev_report = self._load_previous_report()
        day_change = 0
        trend = "STABLE"
        
        if prev_report and self.data_mode != DataMode.STALE:
            day_change = round(total_score - prev_report.get("total_score", total_score), 1)
            if day_change > 3:
                trend = "ESCALATING"
            elif day_change < -3:
                trend = "DE-ESCALATING"
        
        # 4. 生成时间线
        timeline = []
        for e in sorted(events, key=lambda x: x.timestamp):
            if e.is_new_in_window:
                dt = datetime.fromisoformat(e.timestamp)
                timeline.append({
                    "time": dt.strftime("%H:%M"),
                    "date": e.actual_date,
                    "category": e.category,
                    "event": e.title,
                    "impact": "high" if e.impact_score > 5 else "medium" if e.impact_score > 2 else "low",
                    "source": e.source,
                    "verified": e.verified
                })
        
        # 5. 构建报告
        target_date = self.analysis_date.strftime("%Y-%m-%d")
        
        mode_descriptions = {
            "realtime": "实时API数据",
            "historical": "历史归档数据",
            "simulation": "模拟/测试数据",
            "stale": "数据过期或不可用"
        }
        
        report = {
            "metadata": {
                "version": "2.0",
                "generated_at": datetime.now().isoformat(),
                "data_mode": self.data_mode.value,
                "analysis_date": target_date,
                "warnings": self.warnings
            },
            "data_quality": {
                "mode": self.data_mode.value,
                "mode_description": mode_descriptions.get(self.data_mode.value, "未知"),
                "event_count": len(events),
                "new_events_count": len(timeline),
                "warnings": self.warnings
            },
            "date": target_date,
            "analysis_window": {
                "start": self.window_start.isoformat(),
                "end": self.window_end.isoformat(),
                "description": f"{target_date} 00:00 - 24:00"
            },
            "total_score": total_score if events else None,
            "risk_level": risk_level.label if events else "UNKNOWN",
            "risk_emoji": risk_level.emoji if events else "⚪",
            "trend": trend if events else "UNKNOWN",
            "day_change": day_change if prev_report else None,
            "baseline_context": {
                "period": "2025年3月基础态势",
                "description": "制裁+谈判博弈期，无直接军事冲突",
                "key_factors": [
                    "特朗普政府'极限施压'政策（NSPM-2）",
                    "美伊间接谈判僵持（阿曼渠道）",
                    "伊朗里亚尔持续贬值",
                    "胡塞武装红海袭扰"
                ]
            } if events else None,
            "components": {
                name: {
                    "score": comp.final_score,
                    "base_score": comp.base_score,
                    "new_impact": round(comp.new_events_impact, 1),
                    "weight": comp.weight,
                    "trend": comp.trend,
                    "signals": comp.signals
                }
                for name, comp in components.items()
            } if events else {},
            "breaking_events": timeline,
            "data_sources": [
                "ISW Iran Update (March 2025)",
                "Reuters - Middle East",
                "US Treasury Press Release",
                "UN Security Council Meeting Records"
            ] if self.data_mode == DataMode.HISTORICAL else [
                "实时数据API（待接入）"
            ],
            "time_line_validation": {
                "analysis_date": target_date,
                "data_mode": self.data_mode.value,
                "included_dates": list(set(e.actual_date for e in events)) if events else [],
                "excluded": [
                    "2025年6月'12日战争'历史事件",
                    "2026年预测/模拟场景",
                    "未经验证的社交媒体传言"
                ]
            },
            "hedging_recommendation": self._get_hedging_advice(risk_level.label if events else "UNKNOWN", trend) if events else "无数据可用，无法生成建议"
        }
        
        return report
    
    def _load_previous_report(self) -> Optional[Dict]:
        prev_date = (self.analysis_date - timedelta(days=1)).strftime("%Y-%m-%d")
        prev_file = REPORTS_DIR / f"{prev_date}_report.json"
        if prev_file.exists():
            with open(prev_file, 'r') as f:
                return json.load(f)
        return None
    
    def _get_hedging_advice(self, level: str, trend: str) -> str:
        advice_map = {
            ("LOW", "STABLE"): "标准对冲比例（50-60%）。关注谈判进展，准备应对潜在波动。",
            ("LOW", "ESCALATING"): "考虑提升对冲至60-70%。制裁升级信号出现，需提高警惕。",
            ("ELEVATED", "STABLE"): "维持60-70%对冲比例。地缘压力持续，但无急剧恶化迹象。",
            ("ELEVATED", "ESCALATING"): "提升至70-80%对冲。新制裁或代理人冲突风险上升。",
            ("HIGH", "STABLE"): "保持70-80%高对冲。基础风险高企，密切监测每日新信号。",
            ("HIGH", "ESCALATING"): "提升至80-90%最大对冲。冲突升级概率增加，准备应急预案。",
            ("CRITICAL", "_"): "紧急：90%+全额对冲。重大冲突风险，启动危机应对流程。"
        }
        key = (level, trend) if level != "CRITICAL" else ("CRITICAL", "_")
        return advice_map.get(key, "维持当前对冲水平，持续监测。")

def generate_html_dashboard(report: Dict) -> str:
    # 数据模式标签
    mode_colors = {
        "realtime": ("#22c55e", "实时数据"),
        "historical": ("#eab308", "历史归档"),
        "simulation": ("#a855f7", "模拟数据"),
        "stale": ("#ef4444", "数据不可用")
    }
    mode_color, mode_label = mode_colors.get(report['data_quality']['mode'], ("#94a3b8", "未知"))
    
    level_colors = {
        "LOW": "#22c55e",
        "ELEVATED": "#eab308", 
        "HIGH": "#f97316",
        "CRITICAL": "#ef4444",
        "UNKNOWN": "#64748b"
    }
    
    color = level_colors.get(report['risk_level'], "#64748b")
    has_data = report['total_score'] is not None
    
    # 警告框
    warnings_html = ""
    if report['metadata']['warnings']:
        warnings_list = "<br>".join(report['metadata']['warnings'])
        warnings_html = f'<div class="warning-box" style="background: rgba(239, 68, 68, 0.15); border: 1px solid rgba(239, 68, 68, 0.4); border-radius: 12px; padding: 1rem; margin-bottom: 1.5rem;"><div style="font-weight: 600; color: #ef4444; margin-bottom: 0.5rem;">⚠️ 数据质量警告</div>{warnings_list}</div>'
    
    # 分数显示
    if has_data:
        dc = report['day_change'] if report['day_change'] is not None else 0
        dc_str = f"{'+' if dc > 0 else ''}{dc}" if report['day_change'] is not None else "N/A"
        score_display = f'<div class="score-card" style="background: linear-gradient(135deg, {color}20, {color}05); border: 1px solid {color}40; border-radius: 16px; padding: 2rem; text-align: center; margin-bottom: 2rem;"><div class="score-value" style="font-size: 4rem; font-weight: 700; color: {color};">{report["total_score"]}</div><div class="score-label" style="color: #94a3b8; font-size: 0.9rem; margin-top: 0.5rem;">综合风险指数</div><div class="risk-badge" style="display: inline-block; padding: 0.5rem 1.5rem; border-radius: 9999px; background: {color}20; color: {color}; border: 1px solid {color}40; margin-top: 1rem; font-weight: 600;">{report["risk_emoji"]} {report["risk_level"]} RISK</div><div style="margin-top: 1rem; color: #94a3b8;">较昨日: {dc_str} | 趋势: {report["trend"]}</div></div>'
    else:
        score_display = f'<div class="score-card" style="background: linear-gradient(135deg, {mode_color}20, {mode_color}05); border: 1px solid {mode_color}40; border-radius: 16px; padding: 2rem; text-align: center; margin-bottom: 2rem;"><div class="score-value" style="font-size: 3rem; font-weight: 700; color: {mode_color};">无数据</div><div class="score-label" style="color: #94a3b8; font-size: 0.9rem; margin-top: 0.5rem;">{report["data_quality"]["mode_description"]}</div></div>'
    
    # 组件和时间线内容
    main_content = ""
    if has_data:
        # 组件
        comp_names = {"official": "📢 官方态度", "military": "⚔️ 军事行动", "markets": "📈 金融市场", "diplomatic": "🌍 外交信号"}
        components_html = ""
        for name, data in report['components'].items():
            impact_str = f"+{data['new_impact']:.1f}" if data['new_impact'] > 0 else f"{data['new_impact']:.1f}"
            trend_icon = {"escalating": "🔺", "stable": "➡️", "de-escalating": "🔻"}.get(data['trend'], "➡️")
            signals_str = "<br>".join(data['signals'][:2])
            components_html += f'<div class="component-box" style="background: rgba(255,255,255,0.03); border-radius: 10px; padding: 16px; margin: 10px 0;"><div style="display: flex; justify-content: space-between; align-items: center;"><span style="font-weight: 600;">{comp_names.get(name, name)}</span><span style="font-size: 1.3rem; font-weight: 700; color: {color}">{data["score"]}</span></div><div style="font-size: 0.8rem; color: #64748b; margin-top: 8px;">基准: {data["base_score"]} | 当日调整: {impact_str} {trend_icon}</div><div style="font-size: 0.85rem; color: #94a3b8; margin-top: 8px;">{signals_str}</div></div>'
        
        # 事件
        events_html = ""
        for event in report.get('breaking_events', []):
            impact_color = {"high": "#ef4444", "medium": "#f97316", "low": "#22c55e"}.get(event['impact'], "#94a3b8")
            verified_badge = "✓" if event.get('verified') else "?"
            events_html += f'<div class="event-row" style="border-left: 3px solid {impact_color}; padding-left: 12px; margin: 10px 0;"><div style="font-size: 0.8rem; color: #64748b;">{event["date"]} {event["time"]} | {event["category"]} | 验证: {verified_badge}</div><div style="font-size: 0.95rem; color: #e2e8f0;">{event["event"]}</div><div style="font-size: 0.75rem; color: #475569;">来源: {event["source"]}</div></div>'
        
        sources_str = "<br>".join(report.get('data_sources', []))
        included_dates = ", ".join(report.get('time_line_validation', {}).get('included_dates', []))
        excluded_items = ", ".join(report.get('time_line_validation', {}).get('excluded', []))
        
        main_content = f'<div class="section"><div class="section-title">📊 维度分解</div>{components_html}</div><div class="section"><div class="section-title">📰 分析周期内新事件 ({report.get("new_events_count", 0)}条)</div>{events_html if events_html else "<div style=\"color: #64748b;\">本周期无重大新事件</div>"}</div><div class="recommendation"><div class="section-title">💡 对冲建议</div><div style="font-size: 1.05rem; line-height: 1.6;">{report["hedging_recommendation"]}</div></div><div class="section" style="font-size: 0.85rem; color: #64748b;"><div class="section-title">📋 数据来源与时间线验证</div><div style="margin-bottom: 8px;"><strong>数据模式:</strong> {report["data_quality"]["mode_description"]}</div><div style="margin-bottom: 8px;"><strong>已验证来源：</strong></div><div>{sources_str}</div><div style="margin-top: 12px; padding: 8px; background: rgba(234, 179, 8, 0.1); border-radius: 6px;"><strong>时间线验证：</strong><br>分析日期: {report.get("time_line_validation", {}).get("analysis_date", "N/A")}<br>包含日期: {included_dates}<br>排除: {excluded_items}</div></div>'
    
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>地缘冲突风险日报 - {report['date']}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); color: #f8fafc; min-height: 100vh; padding: 2rem; }}
        .container {{ max-width: 900px; margin: 0 auto; }}
        .header {{ text-align: center; margin-bottom: 2rem; }}
        .header h1 {{ font-size: 1.6rem; margin-bottom: 0.5rem; }}
        .header .date {{ color: #64748b; font-size: 0.9rem; }}
        .data-mode-badge {{ display: inline-block; padding: 0.25rem 0.75rem; border-radius: 9999px; background: {mode_color}20; color: {mode_color}; border: 1px solid {mode_color}40; font-size: 0.8rem; font-weight: 600; margin-top: 0.5rem; }}
        .section {{ background: rgba(255,255,255,0.03); border-radius: 12px; padding: 1.5rem; margin-bottom: 1.5rem; border: 1px solid rgba(255,255,255,0.05); }}
        .section-title {{ font-size: 1rem; font-weight: 600; color: {color if has_data else mode_color}; margin-bottom: 1rem; text-transform: uppercase; letter-spacing: 0.05em; }}
        .recommendation {{ background: linear-gradient(135deg, {color if has_data else mode_color}15, {color if has_data else mode_color}05); border: 1px solid {color if has_data else mode_color}30; border-radius: 12px; padding: 1.5rem; }}
        .footer {{ text-align: center; color: #475569; font-size: 0.75rem; margin-top: 2rem; padding-top: 1rem; border-top: 1px solid rgba(255,255,255,0.05); }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔥 地缘冲突风险仪表盘</h1>
            <div class="date">伊朗局势评估 | 分析周期: {report['analysis_window']['description']}</div>
            <div class="data-mode-badge">{mode_label}</div>
        </div>
        {warnings_html}
        {score_display}
        {main_content}
        <div class="footer">生成时间: {report['metadata']['generated_at'][:19]} | 版本: {report['metadata']['version']} | 数据模式: {report['data_quality']['mode']}</div>
    </div>
</body>
</html>"""
    return html

def save_report(report: Dict):
    date_str = report["date"]
    json_path = REPORTS_DIR / f"{date_str}_report.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    html_path = REPORTS_DIR / f"{date_str}_dashboard.html"
    html_content = generate_html_dashboard(report)
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    return json_path, html_path

def main():
    parser = argparse.ArgumentParser(description='Time-Aware Geopolitical Risk Assessment v2')
    parser.add_argument('--date', type=str, default=datetime.now().strftime('%Y-%m-%d'),
                       help='分析日期 (YYYY-MM-DD)')
    parser.add_argument('--window', type=int, default=24,
                       help='分析窗口小时数 (默认24)')
    parser.add_argument('--use-historical', action='store_true',
                       help='允许使用历史归档数据（当无实时数据时）')
    args = parser.parse_args()
    
    print(f"🔄 初始化时间感知风险分析器 v2.0...")
    print(f"📅 分析日期: {args.date}")
    print(f"⏱️ 分析窗口: {args.window}小时")
    print(f"📚 历史模式: {'已启用' if args.use_historical else '未启用'}")
    
    analyzer = TimeAwareRiskAnalyzer(args.date, args.window, args.use_historical)
    report = analyzer.generate_report()
    
    json_path, html_path = save_report(report)
    
    print(f"\n{'='*50}")
    print(f"📊 数据质量: {report['data_quality']['mode_description']}")
    
    if report['metadata']['warnings']:
        print(f"\n⚠️ 警告:")
        for w in report['metadata']['warnings']:
            print(f"   {w}")
    
    if report['total_score'] is not None:
        print(f"\n✅ 风险评估完成")
        print(f"📊 综合风险指数: {report['total_score']} ({report['risk_level']})")
        dc = report['day_change']
        print(f"📈 较昨日变化: {f'{dc:+.1f}' if dc is not None else 'N/A'} ({report['trend']})")
        print(f"📰 分析周期内新事件: {report['data_quality']['new_events_count']} 条")
    else:
        print(f"\n❌ 无数据可用")
        print(f"   提示: 使用 --use-historical 查看历史归档数据")
    
    print(f"\n📁 报告已保存:")
    print(f"   JSON: {json_path}")
    print(f"   HTML: {html_path}")
    
    print(f"\n✅ 时间线验证:")
    print(f"   分析日期: {report['time_line_validation']['analysis_date']}")
    included = report['time_line_validation']['included_dates']
    print(f"   包含日期: {', '.join(included) if included else '无'}")

if __name__ == "__main__":
    main()
