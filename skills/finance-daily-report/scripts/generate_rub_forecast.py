#!/usr/bin/env python3
"""
财经日报 - 卢布对人民币预测专题 v4.0
重点：基于最新市场信息的汇率预测分析
"""

from datetime import datetime
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_CENTER, TA_LEFT


class RUBCNYForecastReport:
    """卢布对人民币预测报告"""
    
    COLORS = {
        'primary': colors.HexColor('#1a237e'),
        'secondary': colors.HexColor('#c62828'),
        'accent': colors.HexColor('#00695c'),
        'rub': colors.HexColor('#1976d2'),
        'warning': colors.HexColor('#e65100'),
        'success': colors.HexColor('#2e7d32'),
        'dark': colors.HexColor('#212121'),
        'gray': colors.HexColor('#757575'),
        'light_bg': colors.HexColor('#f5f5f5'),
        'white': colors.white,
    }
    
    def __init__(self, company_name="公司名称", department="财务管理部 资金管理科", date=None):
        self.company_name = company_name
        self.department = department
        self.date = date or datetime.now().strftime("%Y年%m月%d日")
        self.chinese_font = self._register_fonts()
        self.styles = self._create_styles()
    
    def _register_fonts(self):
        font_paths = [
            '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc',
            '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc',
        ]
        for font_path in font_paths:
            if Path(font_path).exists():
                try:
                    font_name = Path(font_path).stem
                    pdfmetrics.registerFont(TTFont(font_name, font_path))
                    return font_name
                except:
                    continue
        return 'Helvetica'
    
    def _create_styles(self):
        styles = getSampleStyleSheet()
        cf = self.chinese_font
        C = self.COLORS
        
        styles['Title'].fontName = cf
        styles['Title'].fontSize = 20
        styles['Title'].textColor = C['primary']
        styles['Title'].alignment = TA_CENTER
        styles['Title'].spaceAfter = 12
        
        styles.add(ParagraphStyle('SectionHeader', fontName=cf, fontSize=14,
            textColor=C['white'], backColor=C['primary'],
            spaceBefore=20, spaceAfter=10, leading=22,
            borderPadding=8, alignment=TA_LEFT))
        
        styles.add(ParagraphStyle('ForecastSection', fontName=cf, fontSize=14,
            textColor=C['white'], backColor=C['success'],
            spaceBefore=20, spaceAfter=10, leading=22,
            borderPadding=8, alignment=TA_LEFT))
        
        styles.add(ParagraphStyle('SubSection', fontName=cf, fontSize=12,
            textColor=C['primary'], spaceBefore=15, spaceAfter=8,
            leading=16, fontWeight='bold'))
        
        styles.add(ParagraphStyle('CNBodyText', fontName=cf, fontSize=10,
            textColor=C['dark'], spaceAfter=6, leading=14,
            alignment=TA_LEFT))
        
        styles.add(ParagraphStyle('Highlight', fontName=cf, fontSize=10,
            textColor=C['secondary'], spaceAfter=6, leading=14))
        
        styles.add(ParagraphStyle('ForecastText', fontName=cf, fontSize=10,
            textColor=C['success'], spaceAfter=6, leading=14))
        
        styles.add(ParagraphStyle('SmallText', fontName=cf, fontSize=8,
            textColor=C['gray'], spaceAfter=4, leading=10))
        
        return styles
    
    def get_forecast_data(self):
        """预测数据 - 基于2026年3月17日最新市场信息"""
        return {
            'current_rates': {
                'USDRUB': {'value': '80.15', 'change': '+4.5%', 'note': '3月13日跌破80关口'},
                'CNYRUB': {'value': '11.62', 'change': '+4.3%', 'note': '1人民币兑卢布'},
                'USDRUB_Mar3': {'value': '76.68', 'note': '3月3日水平'},
                'CNYRUB_Mar3': {'value': '10.98', 'note': '3月3日水平'},
            },
            'forecast_scenarios': [
                {
                    'scenario': '乐观情景（部分制裁解除）',
                    'usd_rub': '77-78',
                    'cny_rub': '11.0-11.1',
                    'probability': '25%',
                    'driver': '若俄美会谈达成部分制裁解除协议'
                },
                {
                    'scenario': '基准情景（维持现状）',
                    'usd_rub': '81-82',
                    'cny_rub': '11.2',
                    'probability': '50%',
                    'driver': '到8月底，外贸与货币政策维持当前状态'
                },
                {
                    'scenario': '悲观情景（局势恶化）',
                    'usd_rub': '85',
                    'cny_rub': '11.3-11.4',
                    'probability': '25%',
                    'driver': '若地缘局势不利，制裁进一步收紧'
                },
            ],
            'key_factors': {
                'upward_pressure': [  # 卢布升值压力
                    '俄罗斯央行高利率政策（当前15.5%，预期年底13.5-14.5%）',
                    '通胀放缓趋势（2026年预期4.5%-5.5%，下半年接近4%）',
                    '俄美会谈可能带来地缘政治缓和',
                ],
                'downward_pressure': [  # 卢布贬值压力
                    '美伊冲突推高油价，通过汇率渠道产生通胀效应',
                    '跨境支付受阻，外汇短缺加剧',
                    '经常账户恶化，石油收入下降',
                    '央行上半年减少外汇销售',
                ]
            },
            'cbr_policy': [
                '下次利率决议：3月20日（本周五）18:30公布',
                '市场预期：可能继续降息50-100个基点至14.5-15.0%',
                '2026年基准利率预测区间：13.5%-14.5%',
                '央行表示如有必要将干预汇市，维持金融稳定',
            ],
            'expert_quotes': [
                {
                    'source': 'Alfa-Forex投资策略主管斯巴达克·索博列夫',
                    'quote': '若达成某种协议（部分解除制裁），美元兑卢布可能升至77-78；否则可能贬值至82-83，甚至更高。'
                },
                {
                    'source': 'BCS投资世界专家亚历山大·谢佩列夫',
                    'quote': '尽管当前基本面对卢布不利，但峰会结果仍可能对汇率产生一定影响。预计整体走势以温和贬值为主。'
                },
                {
                    'source': '实用投资学院创始人费奥多尔·西多罗夫',
                    'quote': '预计到年底利率可能降至13-15%，届时美元兑卢布汇率可能升至90-100。'
                },
            ],
            'trading_recommendation': {
                'short_term': '观望为主，等待3月20日利率决议和地缘政治明朗',
                'medium_term': '基准情景下，CNY/RUB或温和升至11.2-11.3区间',
                'hedging': '建议企业在11.0-11.2区间逐步建仓，防范贬值风险',
                'risk_alert': '地缘风险仍为主要不确定因素，需密切关注俄美会谈进展',
            }
        }
    
    def create_header(self, story):
        styles = self.styles
        
        story.append(Paragraph(self.company_name, styles['Title']))
        story.append(Paragraph(f"{self.department}    {self.date}", styles['SmallText']))
        story.append(Spacer(1, 0.3*cm))
        story.append(Paragraph("□ 绝密 □ 机密 □ 秘密 ☑ 一般", styles['SmallText']))
        story.append(Spacer(1, 0.5*cm))
        story.append(Paragraph("卢布对人民币汇率预测专题", styles['Title']))
        story.append(Spacer(1, 0.8*cm))
    
    def create_current_rates(self, story, data):
        """当前汇率"""
        styles = self.styles
        cf = self.chinese_font
        
        story.append(Paragraph("📊 当前汇率水平", styles['SubSection']))
        
        table_data = [['货币对', '当前汇率', '变动', '备注']]
        
        rates = data['current_rates']
        table_data.append(['USD/RUB', rates['USDRUB']['value'], rates['USDRUB']['change'], rates['USDRUB']['note']])
        table_data.append(['CNY/RUB', rates['CNYRUB']['value'], rates['CNYRUB']['change'], rates['CNYRUB']['note']])
        table_data.append(['USD/RUB (3月3日)', rates['USDRUB_Mar3']['value'], '-', rates['USDRUB_Mar3']['note']])
        table_data.append(['CNY/RUB (3月3日)', rates['CNYRUB_Mar3']['value'], '-', rates['CNYRUB_Mar3']['note']])
        
        table = Table(table_data, colWidths=[4*cm, 3*cm, 2.5*cm, 3*cm])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self.COLORS['primary']),
            ('TEXTCOLOR', (0, 0), (-1, 0), self.COLORS['white']),
            ('FONTNAME', (0, 0), (-1, -1), cf),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BACKGROUND', (0, 1), (-1, -1), self.COLORS['light_bg']),
            ('PADDING', (0, 0), (-1, -1), 8),
        ]))
        
        story.append(table)
        story.append(Spacer(1, 0.5*cm))
        
        # 关键变化
        story.append(Paragraph("🔍 关键变化", styles['SubSection']))
        story.append(Paragraph("• 3月13日卢布兑美元自1月9日以来首次跌破80关口", styles['Highlight']))
        story.append(Paragraph("• 3月以来卢布累计贬值约4.5%，波动加剧", styles['Highlight']))
        story.append(Paragraph("• 当前CNY/RUB约11.62，较3月3日的10.98升值约5.8%", styles['CNBodyText']))
        story.append(Spacer(1, 0.5*cm))
    
    def create_forecast_scenarios(self, story, data):
        """预测情景"""
        styles = self.styles
        cf = self.chinese_font
        
        story.append(Paragraph("📈 汇率预测情景（2026年）", styles['ForecastSection']))
        story.append(Spacer(1, 0.3*cm))
        
        table_data = [['情景', 'USD/RUB', 'CNY/RUB', '概率', '触发条件']]
        
        for scenario in data['forecast_scenarios']:
            table_data.append([
                scenario['scenario'],
                scenario['usd_rub'],
                scenario['cny_rub'],
                scenario['probability'],
                scenario['driver']
            ])
        
        table = Table(table_data, colWidths=[4.5*cm, 2.5*cm, 2.5*cm, 2*cm, 4*cm])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self.COLORS['success']),
            ('TEXTCOLOR', (0, 0), (-1, 0), self.COLORS['white']),
            ('FONTNAME', (0, 0), (-1, -1), cf),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#e8f5e9')),
            ('PADDING', (0, 0), (-1, -1), 6),
        ]))
        
        story.append(table)
        story.append(Spacer(1, 0.5*cm))
    
    def create_factors_analysis(self, story, data):
        """影响因素分析"""
        styles = self.styles
        
        story.append(Paragraph("⚖️ 影响因素分析", styles['SubSection']))
        
        # 升值压力
        story.append(Paragraph("▲ 卢布升值支撑因素", styles['ForecastText']))
        for factor in data['key_factors']['upward_pressure']:
            story.append(Paragraph(f"• {factor}", styles['CNBodyText']))
        story.append(Spacer(1, 0.3*cm))
        
        # 贬值压力
        story.append(Paragraph("▼ 卢布贬值压力因素", styles['Highlight']))
        for factor in data['key_factors']['downward_pressure']:
            story.append(Paragraph(f"• {factor}", styles['CNBodyText']))
    
    def create_cbr_policy(self, story, data):
        """央行政策"""
        styles = self.styles
        
        story.append(Paragraph("🏛️ 俄罗斯央行政策动态", styles['SubSection']))
        
        for item in data['cbr_policy']:
            if '3月20日' in item:
                story.append(Paragraph(f"• {item}", styles['Highlight']))
            else:
                story.append(Paragraph(f"• {item}", styles['CNBodyText']))
        story.append(Spacer(1, 0.3*cm))
    
    def create_expert_views(self, story, data):
        """专家观点"""
        styles = self.styles
        
        story.append(Paragraph("💬 专家观点", styles['SubSection']))
        
        for quote in data['expert_quotes']:
            story.append(Paragraph(f"▸ {quote['source']}", styles['SubSection']))
            story.append(Paragraph(f'"{quote["quote"]}"', styles['CNBodyText']))
            story.append(Spacer(1, 0.2*cm))
    
    def create_recommendations(self, story, data):
        """交易建议"""
        styles = self.styles
        cf = self.chinese_font
        
        story.append(Paragraph("🎯 交易建议与风险提示", styles['ForecastSection']))
        story.append(Spacer(1, 0.3*cm))
        
        rec = data['trading_recommendation']
        
        story.append(Paragraph("短期策略（1-4周）", styles['SubSection']))
        story.append(Paragraph(rec['short_term'], styles['CNBodyText']))
        story.append(Spacer(1, 0.2*cm))
        
        story.append(Paragraph("中期展望（1-3个月）", styles['SubSection']))
        story.append(Paragraph(rec['medium_term'], styles['CNBodyText']))
        story.append(Spacer(1, 0.2*cm))
        
        story.append(Paragraph("对冲建议", styles['SubSection']))
        story.append(Paragraph(rec['hedging'], styles['ForecastText']))
        story.append(Spacer(1, 0.2*cm))
        
        story.append(Paragraph("⚠️ 风险警示", styles['Highlight']))
        story.append(Paragraph(rec['risk_alert'], styles['Highlight']))
    
    def generate(self, output_path=None):
        """生成PDF报告"""
        print(f"\n{'='*60}")
        print(f"📰 卢布对人民币预测报告 - {self.date}")
        print(f"{'='*60}\n")
        
        data = self.get_forecast_data()
        
        if output_path is None:
            output_dir = Path("/root/.openclaw/workspace/finance-reports")
            output_dir.mkdir(parents=True, exist_ok=True)
            date_str = datetime.now().strftime("%Y%m%d")
            output_path = output_dir / f"卢布人民币预测_{date_str}.pdf"
        
        doc = SimpleDocTemplate(
            str(output_path),
            pagesize=A4,
            rightMargin=15*mm,
            leftMargin=15*mm,
            topMargin=15*mm,
            bottomMargin=15*mm
        )
        
        story = []
        
        # 1. 页眉
        self.create_header(story)
        
        # 2. 当前汇率
        self.create_current_rates(story, data)
        
        # 3. 预测情景
        self.create_forecast_scenarios(story, data)
        story.append(PageBreak())
        
        # 4. 影响因素
        self.create_factors_analysis(story, data)
        
        # 5. 央行政策
        self.create_cbr_policy(story, data)
        story.append(PageBreak())
        
        # 6. 专家观点
        self.create_expert_views(story, data)
        
        # 7. 交易建议
        self.create_recommendations(story, data)
        
        # 8. 页脚
        story.append(Spacer(1, 1*cm))
        story.append(Paragraph(
            f"数据来源：俄罗斯央行/Alfa-Forex/BCS/市场分析师 | 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')} | 仅供参考，不构成投资建议",
            self.styles['SmallText']
        ))
        
        doc.build(story)
        
        print(f"✅ 预测报告已生成: {output_path}")
        print(f"   文件大小: {Path(output_path).stat().st_size / 1024:.1f} KB")
        print(f"\n{'='*60}\n")
        
        return output_path


if __name__ == "__main__":
    report = RUBCNYForecastReport(
        company_name="公司名称",
        department="财务管理部 资金管理科"
    )
    report.generate()
