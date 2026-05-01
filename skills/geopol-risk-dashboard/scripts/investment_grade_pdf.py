#!/usr/bin/env python3
"""
投级PDF报告生成器 v5.0
- 专业排版 + 颜色编码 + 图表
- ReportLab + matplotlib
"""

import os
import sys
import json
import matplotlib
matplotlib.use('Agg')  # 无GUI模式
import matplotlib.pyplot as plt
from datetime import datetime
from pathlib import Path

# ReportLab imports
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, 
    PageBreak, Image
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_CENTER

class InvestmentGradePDFGenerator:
    """投级PDF报告生成器"""
    
    # 投行风格配色
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
        
        # 修改现有样式
        styles['Title'].fontName = self.chinese_font
        styles['Title'].fontSize = 24
        styles['Title'].textColor = self.COLORS['primary']
        styles['Title'].spaceAfter = 6
        styles['Title'].alignment = TA_CENTER
        styles['Title'].leading = 30
        
        # 新增样式
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
    
    def create_risk_gauge(self, score, output_path):
        fig, ax = plt.subplots(figsize=(4, 2.5))
        theta = range(0, 181, 1)
        for t in theta:
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
    
    def create_fx_chart(self, predictions, current, output_path):
        fig, ax = plt.subplots(figsize=(6, 3))
        
        periods = ['当前', 'Q2\'26', 'Q3\'26', 'Q4\'26', 'H1\'27', 'H2\'27']
        values = [current, predictions['Q2_2026'], predictions['Q3_2026'], 
                 predictions['Q4_2026'], predictions['H1_2027'], predictions['H2_2027']]
        
        colors_list = ['#1a237e' if v <= current * 1.02 else '#c62828' for v in values]
        bars = ax.bar(periods, values, color=colors_list, edgecolor='black', linewidth=0.5)
        
        for bar, val in zip(bars, values):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                   f'{val:.2f}', ha='center', va='bottom', fontsize=9)
        
        ax.axhline(y=current, color='#00695c', linestyle='--', linewidth=1.5, label='当前水平')
        ax.set_ylabel('USD/CNY', fontsize=10)
        ax.set_title('USD/CNY 汇率预测路径', fontsize=12, fontweight='bold')
        ax.legend(loc='upper right')
        ax.set_ylim(min(values) * 0.98, max(values) * 1.05)
        ax.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
        plt.close()
    
    def generate_pdf(self, json_report_path, output_pdf_path):
        with open(json_report_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        chart_dir = Path('/tmp/report_charts')
        chart_dir.mkdir(exist_ok=True)
        
        risk_gauge_path = chart_dir / 'risk_gauge.png'
        fx_chart_path = chart_dir / 'fx_prediction.png'
        
        self.create_risk_gauge(data['metadata']['risk_score'], str(risk_gauge_path))
        self.create_fx_chart(data['fx_prediction']['predictions'], 
                           data['fx_prediction']['current'], str(fx_chart_path))
        
        doc = SimpleDocTemplate(output_pdf_path, pagesize=A4,
                               rightMargin=15*mm, leftMargin=15*mm,
                               topMargin=15*mm, bottomMargin=15*mm)
        
        story = []
        s = self.styles
        C = self.COLORS
        cf = self.chinese_font
        
        # 封面
        story.append(Spacer(1, 2*cm))
        story.append(Paragraph(data['metadata']['title'], s['Title']))
        story.append(Paragraph(data['metadata']['subtitle'], s['IGSubtitle']))
        story.append(Paragraph(f"报告日期: {data['metadata']['date']} | 版本: {data['metadata']['version']}", s['IGSmall']))
        story.append(Spacer(1, 1*cm))
        
        # 执行摘要
        summary_data = [
            ['风险评级', 'USD/CNY 当前', '预测区间', '对冲建议'],
            [data['executive_summary']['risk_rating'], data['executive_summary']['fx_current'],
             data['executive_summary']['fx_prediction'], data['executive_summary']['hedge_recommendation']]
        ]
        summary_table = Table(summary_data, colWidths=[4*cm, 3*cm, 4*cm, 4*cm])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), C['primary']), ('TEXTCOLOR', (0, 0), (-1, 0), C['white']),
            ('FONTNAME', (0, 0), (-1, -1), cf), ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'), ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BACKGROUND', (0, 1), (-1, -1), C['light_bg']), ('PADDING', (0, 0), (-1, -1), 10),
        ]))
        story.append(summary_table)
        story.append(Spacer(1, 0.5*cm))
        story.append(Paragraph(f"核心情景: {data['executive_summary']['key_scenario']}", s['IGBody']))
        story.append(PageBreak())
        
        # 风险分析
        story.append(Paragraph('风险分析', s['IGSection']))
        story.append(Image(str(risk_gauge_path), width=8*cm, height=5*cm))
        story.append(Spacer(1, 0.3*cm))
        story.append(Paragraph('最新风险事件', s['IGSubHeader']))
        
        event_data = [['时间', '事件', '来源', '影响']]
        for event in data['risk_events'][:6]:
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
        story.append(Paragraph('市场数据', s['IGSection']))
        market_data = [['资产', '名称', '当前价', '涨跌', '涨跌幅', '最高', '最低', '数据源']]
        for k, v in data['market_data'].items():
            market_data.append([k, v['name'], f"{v['current']:.2f}", f"{v['change']:+.2f}",
                              f"{v['change_pct']:+.2f}%", f"{v['high']:.2f}", f"{v['low']:.2f}", v['source']])
        
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
        
        # 汇率预测
        story.append(Paragraph('USD/CNY 汇率预测', s['IGSection']))
        story.append(Image(str(fx_chart_path), width=14*cm, height=7*cm))
        story.append(Spacer(1, 0.3*cm))
        
        pred = data['fx_prediction']
        pred_data = [['指标', '数值'],
            ['当前汇率', f"{pred['current']:.4f}"],
            ['预测区间 (7天)', f"{pred['range_low']:.4f} - {pred['range_high']:.4f}"],
            ['对冲比例建议', pred['hedge_ratio']],
            ['策略类型', pred['strategy']],
            ['止损线', f"{pred['stop_loss']:.4f}"]]
        
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
        for name, info in data['scenario_analysis'].items():
            scenario_data.append([name.replace('A_', 'A: ').replace('B_', 'B: ').replace('C_', 'C: '),
                                info['probability'], info['trigger'], info['usdcny']])
        
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
        story.append(Paragraph('• 短期 (1-7天): 维持75-85%对冲比例，关注美军伤亡后续反应', s['IGBody']))
        story.append(Paragraph('• 中期 (1-4周): 设置USD/CNY止损线于7.30，准备应急预案', s['IGBody']))
        story.append(Paragraph('• 风险监测: 每日跟踪霍尔木兹海峡通行量、战争险保费、美军动态', s['IGBody']))
        story.append(PageBreak())
        
        # 数据来源与免责声明
        story.append(Paragraph('数据来源', s['IGSection']))
        for source in data['data_sources']:
            story.append(Paragraph(f'• {source}', s['IGBody']))
        
        story.append(Spacer(1, 1*cm))
        story.append(Paragraph('免责声明', s['IGSection']))
        story.append(Paragraph(data['metadata']['disclaimer'] + 
            ' 汇率和能源市场预测存在不确定性，地缘风险具有高度不可预测性。本报告仅供参考，请结合专业机构意见决策。', s['IGSmall']))
        story.append(Spacer(1, 0.5*cm))
        story.append(Paragraph(f'报告生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M CST")} | OpenClaw Investment Grade Report Generator v5.0', s['IGSmall']))
        
        doc.build(story)
        print(f"✅ PDF报告已生成: {output_pdf_path}")
        
        # 清理
        for f in chart_dir.glob('*.png'):
            f.unlink()
        chart_dir.rmdir()
        
        return output_pdf_path

if __name__ == "__main__":
    json_path = '/root/.openclaw/workspace/geopol-risk-reports/investment_grade_report_2026-03-17.json'
    pdf_path = '/root/.openclaw/workspace/geopol-risk-reports/investment_grade_report_2026-03-17.pdf'
    
    generator = InvestmentGradePDFGenerator()
    generator.generate_pdf(json_path, pdf_path)
