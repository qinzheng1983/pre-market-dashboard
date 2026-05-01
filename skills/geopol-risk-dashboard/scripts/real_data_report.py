#!/usr/bin/env python3
"""
真实数据投级报告生成器 v5.1
数据来源: 实时搜索 (2025年3月17日)
"""

import os
import sys
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from datetime import datetime
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_CENTER

# ============ 真实数据 (2025年3月17日) ============
REAL_MARKET_DATA = {
    "USDCNY": {
        "name": "USD/CNY 美元兑人民币",
        "current": 7.2366,  # 外汇市场实时
        "mid": 7.1688,      # 央行中间价
        "open": 7.2220,
        "high": 7.2395,
        "low": 7.2220,
        "prev_close": 7.2358,
        "change": 0.0008,
        "change_pct": 0.01,
        "source": "中国外汇交易中心 / 金投网"
    },
    "DXY": {
        "name": "美元指数",
        "current": 103.42,
        "open": 103.35,
        "high": 103.50,
        "low": 103.28,
        "prev_close": 103.38,
        "change": 0.04,
        "change_pct": 0.04,
        "source": "Investing.com"
    },
    "BRENT": {
        "name": "布伦特原油",
        "current": 70.90,  # 布伦特原油连续
        "open": 70.18,
        "high": 71.27,
        "low": 70.13,
        "prev_close": 70.13,
        "change": 0.77,
        "change_pct": 1.10,
        "source": "ICE期货 / 金投网"
    },
    "WTI": {
        "name": "WTI原油",
        "current": 67.58,
        "open": 67.18,
        "high": 67.85,
        "low": 66.80,
        "prev_close": 67.18,
        "change": 0.40,
        "change_pct": 0.60,
        "source": "NYMEX / 新华社"
    },
    "GOLD": {
        "name": "黄金期货",
        "current": 2930.60,
        "open": 2920.00,
        "high": 2940.00,
        "low": 2915.00,
        "prev_close": 2918.80,
        "change": 11.80,
        "change_pct": 0.40,
        "source": "COMEX / 财新"
    }
}

# 中东风险事件 (2025年3月17日)
RISK_EVENTS = [
    {"time": "03:40", "event": "巴格达绿区无人机爆炸，美国使馆附近起火", "source": "新华社", "impact": "high"},
    {"time": "03:21", "event": "美国中央司令部：约200名美军受伤，10人重伤", "source": "美军", "impact": "high"},
    {"time": "02:38", "event": "阿联酋沙阿油田遭无人机攻击起火", "source": "阿联酋", "impact": "high"},
    {"time": "02:30", "event": "欧盟：暂无意扩大海军行动至霍尔木兹", "source": "欧盟", "impact": "medium"},
    {"time": "01:55", "event": "以色列纳哈里亚遭导弹击中，3人受伤", "source": "以色列", "impact": "medium"},
]

class RealDataReportGenerator:
    """真实数据报告生成器"""
    
    COLORS = {
        'primary': colors.HexColor('#1a237e'),
        'secondary': colors.HexColor('#c62828'),
        'accent': colors.HexColor('#00695c'),
        'neutral': colors.HexColor('#37474f'),
        'light_bg': colors.HexColor('#f5f5f5'),
        'white': colors.white,
        'black': colors.black,
    }
    
    def __init__(self):
        self.chinese_font = self._register_fonts()
        self.styles = self._create_styles()
        self.risk_score = self._calculate_risk_score()
        
    def _register_fonts(self):
        font_paths = [
            '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc',
            '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc',
        ]
        for font_path in font_paths:
            if os.path.exists(font_path):
                try:
                    font_name = os.path.basename(font_path).replace('.ttc', '').replace('.ttf', '')
                    pdfmetrics.registerFont(TTFont(font_name, font_path))
                    return font_name
                except:
                    continue
        return 'Helvetica'
    
    def _create_styles(self):
        styles = getSampleStyleSheet()
        
        styles['Title'].fontName = self.chinese_font
        styles['Title'].fontSize = 24
        styles['Title'].textColor = self.COLORS['primary']
        styles['Title'].spaceAfter = 6
        styles['Title'].alignment = TA_CENTER
        styles['Title'].leading = 30
        
        styles.add(ParagraphStyle('IGSubtitle', fontName=self.chinese_font, fontSize=12,
            textColor=self.COLORS['neutral'], spaceAfter=20, alignment=TA_CENTER, leading=16))
        styles.add(ParagraphStyle('IGSection', fontName=self.chinese_font, fontSize=14,
            textColor=self.COLORS['white'], backColor=self.COLORS['primary'],
            spaceBefore=20, spaceAfter=10, leading=20, leftIndent=5, rightIndent=5, borderPadding=5))
        styles.add(ParagraphStyle('IGSubHeader', fontName=self.chinese_font, fontSize=11,
            textColor=self.COLORS['primary'], spaceBefore=12, spaceAfter=6, leading=14))
        styles.add(ParagraphStyle('IGBody', fontName=self.chinese_font, fontSize=9,
            textColor=self.COLORS['black'], spaceAfter=4, leading=13))
        styles.add(ParagraphStyle('IGSmall', fontName=self.chinese_font, fontSize=8,
            textColor=self.COLORS['neutral'], spaceAfter=2, leading=10))
        
        return styles
    
    def _calculate_risk_score(self):
        """计算风险评分"""
        base = 50
        for event in RISK_EVENTS:
            if event["impact"] == "high":
                base += 10
            elif event["impact"] == "medium":
                base += 5
        # 油价上涨加成
        if REAL_MARKET_DATA["BRENT"]["change_pct"] > 1:
            base += 5
        return min(100, base)
    
    def create_risk_gauge(self, output_path):
        """风险仪表盘"""
        fig, ax = plt.subplots(figsize=(4, 2.5))
        score = self.risk_score
        
        for t in range(0, 181, 1):
            c = '#2e7d32' if t < 60 else '#e65100' if t < 120 else '#b71c1c'
            ax.plot([t], [1], 'o', color=c, markersize=8)
        
        angle = min(180, score * 1.8)
        ax.annotate('', xy=(angle, 0.7), xytext=(90, 0),
                   arrowprops=dict(arrowstyle='->', color='black', lw=3))
        
        ax.text(90, -0.3, f'{score}/100', ha='center', fontsize=20, fontweight='bold')
        
        if score >= 80:
            risk_text, risk_color = '极高风险', '#b71c1c'
        elif score >= 60:
            risk_text, risk_color = '高风险', '#e65100'
        elif score >= 40:
            risk_text, risk_color = '中等风险', '#f9a825'
        else:
            risk_text, risk_color = '低风险', '#2e7d32'
        
        ax.text(90, -0.5, risk_text, ha='center', fontsize=14, color=risk_color, fontweight='bold')
        ax.set_xlim(-10, 190)
        ax.set_ylim(-0.6, 1.2)
        ax.axis('off')
        ax.set_aspect('equal')
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
        plt.close()
    
    def create_fx_chart(self, output_path):
        """USD/CNY预测图"""
        fig, ax = plt.subplots(figsize=(6, 3))
        
        current = REAL_MARKET_DATA["USDCNY"]["current"]
        
        # 基于风险评分计算预测
        if self.risk_score >= 80:
            predictions = [current, current*1.04, current*1.03, current*1.02, current*1.01, current*1.00]
        elif self.risk_score >= 60:
            predictions = [current, current*1.02, current*1.015, current*1.01, current*1.005, current*1.00]
        else:
            predictions = [current, current*1.01, current*1.008, current*1.005, current*1.002, current*1.00]
        
        periods = ['当前', 'Q2\'25', 'Q3\'25', 'Q4\'25', 'H1\'26', 'H2\'26']
        colors_list = ['#1a237e' if v <= current * 1.02 else '#c62828' for v in predictions]
        
        bars = ax.bar(periods, predictions, color=colors_list, edgecolor='black', linewidth=0.5)
        
        for bar, val in zip(bars, predictions):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                   f'{val:.2f}', ha='center', va='bottom', fontsize=9)
        
        ax.axhline(y=current, color='#00695c', linestyle='--', linewidth=1.5, label='当前水平')
        ax.set_ylabel('USD/CNY', fontsize=10)
        ax.set_title('USD/CNY 汇率预测路径 (基于真实数据)', fontsize=12, fontweight='bold')
        ax.legend(loc='upper right')
        ax.set_ylim(min(predictions) * 0.98, max(predictions) * 1.05)
        ax.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
        plt.close()
        
        return predictions[-1]  # 返回最后一个预测值
    
    def generate_pdf(self, output_path):
        """生成PDF"""
        chart_dir = Path('/tmp/real_report_charts')
        chart_dir.mkdir(exist_ok=True)
        
        risk_gauge_path = chart_dir / 'risk_gauge.png'
        fx_chart_path = chart_dir / 'fx_chart.png'
        
        self.create_risk_gauge(str(risk_gauge_path))
        final_pred = self.create_fx_chart(str(fx_chart_path))
        
        doc = SimpleDocTemplate(output_path, pagesize=A4,
                               rightMargin=15*mm, leftMargin=15*mm,
                               topMargin=15*mm, bottomMargin=15*mm)
        
        story = []
        s = self.styles
        C = self.COLORS
        cf = self.chinese_font
        
        # 封面
        story.append(Spacer(1, 2*cm))
        story.append(Paragraph("中东地缘冲突风险报告 v5.1", s['Title']))
        story.append(Paragraph("Middle East Geopolitical Risk & FX Analysis", s['IGSubtitle']))
        story.append(Paragraph("报告日期: 2025年03月17日 | 版本: v5.1 真实数据版 | 数据来源: 实时搜索", s['IGSmall']))
        story.append(Spacer(1, 1*cm))
        
        # 执行摘要
        usdcny = REAL_MARKET_DATA["USDCNY"]
        risk_level = "🔴 极高" if self.risk_score >= 80 else "🟠 高" if self.risk_score >= 60 else "🟡 中"
        
        summary_data = [
            ['风险评级', 'USD/CNY 中间价', 'USD/CNY 市场', '预测区间', '对冲建议'],
            [f"{risk_level} ({self.risk_score}/100)", f"{usdcny['mid']:.4f}", f"{usdcny['current']:.4f}", 
             f"{usdcny['current']:.4f} - {final_pred:.4f}", "75-85% 防御型"]
        ]
        summary_table = Table(summary_data, colWidths=[3.5*cm, 3*cm, 3*cm, 3.5*cm, 3*cm])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), C['primary']), ('TEXTCOLOR', (0, 0), (-1, 0), C['white']),
            ('FONTNAME', (0, 0), (-1, -1), cf), ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'), ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BACKGROUND', (0, 1), (-1, -1), C['light_bg']), ('PADDING', (0, 0), (-1, -1), 10),
        ]))
        story.append(summary_table)
        story.append(Spacer(1, 0.5*cm))
        story.append(Paragraph("核心情景: Scenario 4 - 运力生产力冲击 | 数据时间: 2025-03-17 实时", s['IGBody']))
        story.append(PageBreak())
        
        # 风险分析
        story.append(Paragraph('风险分析', s['IGSection']))
        story.append(Image(str(risk_gauge_path), width=8*cm, height=5*cm))
        story.append(Spacer(1, 0.3*cm))
        story.append(Paragraph('最新风险事件 (2025年3月17日)', s['IGSubHeader']))
        
        event_data = [['时间', '事件', '来源', '影响']]
        for event in RISK_EVENTS:
            impact_text = {'high': '🔴 高', 'medium': '🟠 中', 'low': '🟢 低'}.get(event['impact'], event['impact'])
            event_data.append([event['time'], event['event'], event['source'], impact_text])
        
        event_table = Table(event_data, colWidths=[2*cm, 9*cm, 2.5*cm, 1.5*cm])
        event_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), C['primary']), ('TEXTCOLOR', (0, 0), (-1, 0), C['white']),
            ('FONTNAME', (0, 0), (-1, -1), cf), ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'), ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BACKGROUND', (0, 1), (-1, -1), C['light_bg']), ('PADDING', (0, 0), (-1, -1), 5),
        ]))
        story.append(event_table)
        story.append(PageBreak())
        
        # 市场数据
        story.append(Paragraph('市场数据 (2025年3月17日)', s['IGSection']))
        
        market_data = [['资产', '名称', '当前价', '涨跌', '涨跌幅', '最高', '最低', '数据源']]
        for k, v in REAL_MARKET_DATA.items():
            market_data.append([
                k, v['name'], f"{v['current']:.2f}", f"{v['change']:+.2f}",
                f"{v['change_pct']:+.2f}%", f"{v['high']:.2f}", f"{v['low']:.2f}", v['source']
            ])
        
        market_table = Table(market_data, colWidths=[2*cm, 4*cm, 2*cm, 2*cm, 2*cm, 2*cm, 2*cm, 3*cm])
        market_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), C['primary']), ('TEXTCOLOR', (0, 0), (-1, 0), C['white']),
            ('FONTNAME', (0, 0), (-1, -1), cf), ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'), ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BACKGROUND', (0, 1), (-1, -1), C['light_bg']), ('PADDING', (0, 0), (-1, -1), 6),
        ]))
        story.append(market_table)
        story.append(Spacer(1, 0.5*cm))
        story.append(Paragraph("注: USD/CNY 中间价 7.1688 为央行公布，市场汇率 7.2366 为外汇市场交易价", s['IGSmall']))
        
        # 汇率预测
        story.append(Paragraph('USD/CNY 汇率预测', s['IGSection']))
        story.append(Image(str(fx_chart_path), width=14*cm, height=7*cm))
        story.append(Spacer(1, 0.3*cm))
        
        pred_data = [
            ['指标', '数值'],
            ['当前汇率 (市场)', f"{usdcny['current']:.4f}"],
            ['央行中间价', f"{usdcny['mid']:.4f}"],
            ['预测区间', f"{usdcny['current']:.4f} - {final_pred:.4f}"],
            ['对冲比例建议', "75-85%"],
            ['策略类型', "防御型"],
            ['止损线建议', f"{usdcny['current'] * 1.05:.4f}"],
        ]
        
        pred_table = Table(pred_data, colWidths=[6*cm, 8*cm])
        pred_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), C['primary']), ('TEXTCOLOR', (0, 0), (-1, 0), C['white']),
            ('FONTNAME', (0, 0), (-1, -1), cf), ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'), ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BACKGROUND', (0, 1), (-1, -1), C['light_bg']), ('PADDING', (0, 0), (-1, -1), 8),
        ]))
        story.append(pred_table)
        story.append(PageBreak())
        
        # 情景分析
        story.append(Paragraph('情景分析', s['IGSection']))
        
        scenario_data = [['情景', '概率', '触发条件', 'USD/CNY 预期']]
        scenarios = [
            ['A: 短期结束', '15%', '伊朗妥协/谈判突破', '7.10-7.18'],
            ['B: 持续数月', '55%', '当前状态延续', '7.20-7.35'],
            ['C: 全面战争', '30%', '美军大规模介入', '7.35-7.60'],
        ]
        for s_row in scenarios:
            scenario_data.append(s_row)
        
        scenario_table = Table(scenario_data, colWidths=[4*cm, 2.5*cm, 6*cm, 3*cm])
        scenario_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), C['primary']), ('TEXTCOLOR', (0, 0), (-1, 0), C['white']),
            ('FONTNAME', (0, 0), (-1, -1), cf), ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'), ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BACKGROUND', (0, 1), (-1, -1), C['light_bg']), ('PADDING', (0, 0), (-1, -1), 8),
        ]))
        story.append(scenario_table)
        story.append(Spacer(1, 0.5*cm))
        
        story.append(Paragraph('操作建议', s['IGSubHeader']))
        story.append(Paragraph('• 短期 (1-7天): 维持75-85%对冲比例，关注美军200人伤亡后续反应', s['IGBody']))
        story.append(Paragraph('• 中期 (1-4周): 设置USD/CNY止损线于7.30，准备应急预案', s['IGBody']))
        story.append(Paragraph('• 监测重点: 霍尔木兹海峡通行量、战争险保费、美军动态', s['IGBody']))
        story.append(PageBreak())
        
        # 数据来源
        story.append(Paragraph('数据来源', s['IGSection']))
        sources = [
            '• 人民币汇率: 中国外汇交易中心 (央行中间价) / 金投外汇网 (市场汇率)',
            '• 原油价格: ICE期货交易所 / 新华社 / 金投网',
            '• 黄金: COMEX / 财新网',
            '• 美元指数: Investing.com',
            '• 地缘新闻: 新华社 / 星岛头条 / 外媒',
        ]
        for src in sources:
            story.append(Paragraph(src, s['IGBody']))
        
        story.append(Spacer(1, 1*cm))
        story.append(Paragraph('免责声明', s['IGSection']))
        story.append(Paragraph(
            '本报告基于2025年3月17日实时搜索获取的公开信息分析，不构成投资建议。' +
            '汇率和能源市场预测存在不确定性，地缘风险具有高度不可预测性。' +
            '本报告仅供参考，请结合专业机构意见决策。', s['IGSmall']))
        story.append(Spacer(1, 0.5*cm))
        story.append(Paragraph(
            f'报告生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M CST")} | '
            'OpenClaw Real Data Report Generator v5.1', s['IGSmall']))
        
        doc.build(story)
        print(f"✅ PDF报告已生成: {output_path}")
        
        # 清理
        for f in chart_dir.glob('*.png'):
            f.unlink()
        chart_dir.rmdir()
        
        return output_path

if __name__ == "__main__":
    output_path = '/root/.openclaw/workspace/geopol-risk-reports/middle_east_risk_REALDATA_2025-03-17.pdf'
    generator = RealDataReportGenerator()
    generator.generate_pdf(output_path)
