#!/usr/bin/env python3
"""
财经日报生成器 v3.1 - 卢布专题版
新增：俄罗斯/卢布专门板块
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


class FinanceDailyReportRUB:
    """财经日报 卢布专题版"""
    
    COLORS = {
        'primary': colors.HexColor('#1a237e'),
        'secondary': colors.HexColor('#c62828'),
        'accent': colors.HexColor('#00695c'),
        'rub': colors.HexColor('#1976d2'),  # 卢布蓝色
        'warning': colors.HexColor('#e65100'),
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
        """注册中文字体"""
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
        """创建样式"""
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
            leftIndent=0, rightIndent=0, borderPadding=8,
            alignment=TA_LEFT))
        
        styles.add(ParagraphStyle('RUBSection', fontName=cf, fontSize=14,
            textColor=C['white'], backColor=C['rub'],
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
        
        styles.add(ParagraphStyle('SmallText', fontName=cf, fontSize=8,
            textColor=C['gray'], spaceAfter=4, leading=10))
        
        return styles
    
    def get_today_data(self):
        """今日数据 - 2026年3月17日（卢布专题）"""
        return {
            'market_summary': {
                'USDCNY': {'value': '6.8961', 'change': '+45bp', 'note': '中间价'},
                'USDRUB': {'value': '80.15', 'change': '+4.5%', 'note': '跌破80关口'},
                'CNYRUB': {'value': '11.62', 'change': '+4.3%', 'note': '1人民币'},
                'Brent': {'value': '$103.14', 'change': '+2.67%', 'note': 'ICE期货'},
                'Gold': {'value': '$5,061.70', 'change': '+0.43%', 'note': 'COMEX'},
            },
            'rub_focus': {
                'rate_now': '1美元 = 80.15卢布（3月13日跌破80关口）',
                'rate_march3': '1美元 = 76.68卢布；1人民币 = 10.98卢布（3月3日）',
                'rate_change': '3月13日卢布兑美元自1月9日以来首次跌破80关口',
                'trend': '近期卢布因美伊冲突及制裁影响波动加剧',
            },
            'rub_policy': [
                '俄罗斯央行基准利率：15.5%（2月13日降息50个基点，连续第六次降息）',
                '下次利率决议：3月20日（本周五）18:30公布',
                '2026年通胀预期：4.5%-5.5%，预计下半年回落至4%目标附近',
                '当前年化通胀率：6.3%（1月受一次性因素影响略有抬头）',
            ],
            'rub_economy': [
                '2025年全年通胀率降至5.6%，较2024年下降3.9个百分点',
                '劳动力市场紧张局势逐步缓解，失业率处于历史低位',
                '俄罗斯经济继续回归平衡增长轨道',
                '普京预计2026年通胀率有望进一步降至5%',
            ],
            'rub_risk': [
                '【汇率风险】卢布兑美元3月以来贬值超4%，跨境支付受阻',
                '【制裁影响】俄气银行等金融机构受制裁，外汇短缺加剧',
                '【地缘风险】美伊冲突推高油价，通过汇率渠道产生通胀效应',
                '【政策应对】俄央行表示如有必要将干预汇市，维持金融稳定',
            ],
            'fund_movement': [
                '央行开展逆回购操作，维护银行体系流动性合理充裕',
                'USD/CNY中间价报6.8961，较前一交易日调升45个基点',
                '银行间债市表现平稳，国债收益率维持震荡走势',
            ],
            'macro': [
                '中国2月官方制造业PMI为49.0%，环比下降0.3个百分点',
                '2026年政府工作报告明确GDP增长目标5%左右',
                '通胀水平维持低位运行，货币政策保持稳健中性',
            ],
            'geopolitics': [
                '【极高风险】3月16日伊朗最高领袖哈梅内伊遭袭身亡',
                '霍尔木兹海峡船舶流量下降93%，全球能源供应紧张',
                '伊拉克准备削减约300万桶/日石油产量',
            ],
            'auto_industry': [
                ('新能源整车', '长城汽车2月海外销量同比增长35%，新能源渗透率达38%'),
                ('动力电池', '国内2月装机量同比增长42%，磷酸铁锂电池占比超70%'),
                ('智能驾驶', '工信部加快明确L3/L4级智驾安全准则'),
                ('汽车芯片', '1-2月集成电路出口额同比增长18.5%'),
                ('充电设施', '国家能源局：扩大农村充电设施覆盖范围'),
                ('整车交付', '华为鸿蒙智行累计交付128万辆'),
            ],
            'policies': [
                {
                    'dept': '财政部',
                    'aspect': '国债发行',
                    'policy': '拟续发行320亿元50年期记账式附息国债，票面利率维持2.28%',
                    'interpretation': '长期国债发行维持稳定利率，有利于企业锁定长期融资成本'
                },
                {
                    'dept': '国家能源局',
                    'aspect': '农村能源',
                    'policy': '推进农村能源革命，扩大农村充电设施覆盖，支持分布式光伏',
                    'interpretation': '利好新能源产业链，预计带动千亿级投资'
                },
                {
                    'dept': '工信部',
                    'aspect': '智能驾驶',
                    'policy': '加快明确L3/L4级智能驾驶安全准则',
                    'interpretation': '智能驾驶法规加速完善，关注自动驾驶技术领先企业'
                },
                {
                    'dept': '央行',
                    'aspect': '货币政策',
                    'policy': '开展逆回购操作，维护流动性合理充裕',
                    'interpretation': '货币政策保持稳健，有利于金融市场稳定运行'
                },
            ]
        }
    
    def create_header(self, story):
        """创建页眉"""
        styles = self.styles
        
        story.append(Paragraph(self.company_name, styles['Title']))
        story.append(Paragraph(f"{self.department}    {self.date}", styles['SmallText']))
        story.append(Spacer(1, 0.3*cm))
        story.append(Paragraph("□ 绝密 □ 机密 □ 秘密 ☑ 一般", styles['SmallText']))
        story.append(Spacer(1, 0.5*cm))
        story.append(Paragraph("今日财经新闻（日报）", styles['Title']))
        story.append(Spacer(1, 0.8*cm))
    
    def create_market_table(self, story, data):
        """市场行情表"""
        styles = self.styles
        cf = self.chinese_font
        
        story.append(Paragraph("📊 市场行情摘要", styles['SubSection']))
        
        table_data = [['指标', '数值', '涨跌', '备注']]
        
        for key, item in data['market_summary'].items():
            name_map = {
                'USDCNY': 'USD/CNY 中间价',
                'USDRUB': 'USD/RUB 卢布',
                'CNYRUB': 'CNY/RUB 卢布',
                'Brent': '布伦特原油',
                'Gold': '黄金期货',
            }
            table_data.append([
                name_map.get(key, key),
                item['value'],
                item['change'],
                item['note']
            ])
        
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
    
    def create_rub_section(self, story, data):
        """卢布专题板块"""
        styles = self.styles
        cf = self.chinese_font
        
        story.append(Paragraph("🇷🇺 一、卢布汇率专题", styles['RUBSection']))
        story.append(Spacer(1, 0.3*cm))
        
        # 汇率速览表
        story.append(Paragraph("💱 汇率速览", styles['SubSection']))
        
        rub_table = [
            ['时间', '汇率', '备注'],
            ['当前（3月17日）', '1 USD = 80.15 RUB', '跌破80关口'],
            ['3月3日', '1 USD = 76.68 RUB', '1 CNY = 10.98 RUB'],
            ['3月以来变动', '贬值 +4.5%', '波动加剧'],
        ]
        
        table = Table(rub_table, colWidths=[4*cm, 4*cm, 4.5*cm])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self.COLORS['rub']),
            ('TEXTCOLOR', (0, 0), (-1, 0), self.COLORS['white']),
            ('FONTNAME', (0, 0), (-1, -1), cf),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#e3f2fd')),
            ('PADDING', (0, 0), (-1, -1), 8),
        ]))
        story.append(table)
        story.append(Spacer(1, 0.4*cm))
        
        # 俄罗斯央行政策
        story.append(Paragraph("🏛️ 俄罗斯央行政策", styles['SubSection']))
        for item in data['rub_policy']:
            story.append(Paragraph(f"• {item}", styles['CNBodyText']))
        story.append(Spacer(1, 0.3*cm))
        
        # 俄罗斯经济
        story.append(Paragraph("📈 俄罗斯经济概况", styles['SubSection']))
        for item in data['rub_economy']:
            story.append(Paragraph(f"• {item}", styles['CNBodyText']))
        story.append(Spacer(1, 0.3*cm))
        
        # 风险预警
        story.append(Paragraph("⚠️ 风险预警", styles['SubSection']))
        for item in data['rub_risk']:
            if '【' in item:
                story.append(Paragraph(f"• {item}", styles['Highlight']))
            else:
                story.append(Paragraph(f"• {item}", styles['CNBodyText']))
    
    def create_news_section(self, story, title, items, icon="📰"):
        """创建新闻区块"""
        styles = self.styles
        
        story.append(Paragraph(f"{icon} {title}", styles['SubSection']))
        
        for i, item in enumerate(items, 1):
            if '【' in item and '】' in item:
                style = styles['Highlight']
            else:
                style = styles['CNBodyText']
            story.append(Paragraph(f"{i}. {item}", style))
        
        story.append(Spacer(1, 0.3*cm))
    
    def create_auto_section(self, story, data):
        """汽车行业"""
        styles = self.styles
        cf = self.chinese_font
        
        story.append(Paragraph("🚗 三、汽车行业讯息", styles['SectionHeader']))
        story.append(Spacer(1, 0.3*cm))
        
        auto_data = [['细分领域', '关键讯息']]
        for category, content in data['auto_industry']:
            auto_data.append([category, content])
        
        table = Table(auto_data, colWidths=[3*cm, 12*cm])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self.COLORS['accent']),
            ('TEXTCOLOR', (0, 0), (-1, 0), self.COLORS['white']),
            ('FONTNAME', (0, 0), (-1, -1), cf),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('ALIGN', (0, 0), (0, -1), 'CENTER'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BACKGROUND', (0, 1), (-1, -1), self.COLORS['light_bg']),
            ('PADDING', (0, 0), (-1, -1), 6),
        ]))
        story.append(table)
    
    def create_policy_section(self, story, data):
        """国家政策"""
        styles = self.styles
        
        story.append(Paragraph("🏛️ 四、国家政策", styles['SectionHeader']))
        story.append(Spacer(1, 0.3*cm))
        
        for policy in data['policies']:
            story.append(Paragraph(f"▸ {policy['dept']} | {policy['aspect']}", styles['SubSection']))
            story.append(Paragraph(f"<b>政策：</b>{policy['policy']}", styles['CNBodyText']))
            story.append(Paragraph(f"<b>解读：</b>{policy['interpretation']}", styles['CNBodyText']))
            story.append(Spacer(1, 0.2*cm))
    
    def generate(self, output_path=None):
        """生成PDF"""
        print(f"\n{'='*60}")
        print(f"📰 财经日报 卢布专题版 - {self.date}")
        print(f"{'='*60}\n")
        
        data = self.get_today_data()
        
        if output_path is None:
            output_dir = Path("/root/.openclaw/workspace/finance-reports")
            output_dir.mkdir(parents=True, exist_ok=True)
            date_str = datetime.now().strftime("%Y%m%d")
            output_path = output_dir / f"财经日报_{date_str}_RUB.pdf"
        
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
        
        # 2. 市场行情
        self.create_market_table(story, data)
        
        # 3. 卢布专题
        self.create_rub_section(story, data)
        story.append(PageBreak())
        
        # 4. 其他要闻
        story.append(Paragraph("📈 二、聚焦热点", self.styles['SectionHeader']))
        self.create_news_section(story, "资金动向", data['fund_movement'], "💰")
        self.create_news_section(story, "宏观经济", data['macro'], "📊")
        self.create_news_section(story, "地缘风险", data['geopolitics'], "⚠️")
        
        # 5. 汽车行业
        self.create_auto_section(story, data)
        story.append(PageBreak())
        
        # 6. 国家政策
        self.create_policy_section(story, data)
        
        # 7. 页脚
        story.append(Spacer(1, 1*cm))
        story.append(Paragraph(
            f"数据来源：央行/俄罗斯央行/ICE期货/Investing.com | 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')} | Finance Daily Report v3.1 RUB",
            self.styles['SmallText']
        ))
        
        doc.build(story)
        
        print(f"✅ PDF报告已生成: {output_path}")
        print(f"   文件大小: {Path(output_path).stat().st_size / 1024:.1f} KB")
        print(f"\n{'='*60}\n")
        
        return output_path


if __name__ == "__main__":
    report = FinanceDailyReportRUB(
        company_name="公司名称",
        department="财务管理部 资金管理科"
    )
    report.generate()
