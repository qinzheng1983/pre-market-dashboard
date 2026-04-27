#!/usr/bin/env python3
"""
财经日报生成器 v3.0 - PDF专业版
新增：汽车行业讯息模块 + UI美化
"""

from datetime import datetime
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT


class FinanceDailyReportPDF:
    """财经日报 PDF 专业版"""
    
    # 配色方案 - 专业金融风格
    COLORS = {
        'primary': colors.HexColor('#1a237e'),      # 深蓝
        'secondary': colors.HexColor('#c62828'),    # 红色（重要）
        'accent': colors.HexColor('#00695c'),       # 青绿
        'warning': colors.HexColor('#e65100'),      # 橙色（警告）
        'success': colors.HexColor('#2e7d32'),      # 绿色
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
        
        # 标题样式
        styles['Title'].fontName = cf
        styles['Title'].fontSize = 20
        styles['Title'].textColor = C['primary']
        styles['Title'].alignment = TA_CENTER
        styles['Title'].spaceAfter = 12
        
        # 自定义样式
        styles.add(ParagraphStyle('SectionHeader', fontName=cf, fontSize=14,
            textColor=C['white'], backColor=C['primary'],
            spaceBefore=20, spaceAfter=10, leading=20,
            leftIndent=0, rightIndent=0, borderPadding=8,
            alignment=TA_LEFT))
        
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
        
        styles.add(ParagraphStyle('TableHeader', fontName=cf, fontSize=9,
            textColor=C['white'], alignment=TA_CENTER))
        
        styles.add(ParagraphStyle('TableCell', fontName=cf, fontSize=9,
            textColor=C['dark'], alignment=TA_LEFT))
        
        return styles
    
    def get_today_data(self):
        """今日数据 - 2026年3月17日"""
        return {
            'market_summary': {
                'USDCNY': {'value': '6.8961', 'change': '+45bp', 'note': '中间价'},
                'USDCNY_Spot': {'value': '6.9004', 'change': '+0.06%', 'note': '市场汇率'},
                'Brent': {'value': '$103.14', 'change': '+2.67%', 'note': 'ICE期货'},
                'Gold': {'value': '$5,061.70', 'change': '+0.43%', 'note': 'COMEX'},
                'Shanghai': {'value': '3,341.00', 'change': '+0.53%', 'note': '上证指数'},
            },
            'fund_movement': [
                '央行开展逆回购操作，维护银行体系流动性合理充裕',
                'USD/CNY中间价报6.8961，较前一交易日调升45个基点',
                '银行间债市表现平稳，国债收益率维持震荡',
            ],
            'macro': [
                '中国2月官方制造业PMI为49.0%，环比下降0.3个百分点',
                '2026年政府工作报告明确GDP增长目标5%左右',
                '通胀水平维持低位运行，货币政策保持稳健',
            ],
            'domestic': [
                '国家能源局推进农村能源革命，扩大充电设施覆盖',
                '华为鸿蒙智行累计交付量达128万辆',
                '小米雷军提交建议案，涵盖人形机器人、智能驾驶',
            ],
            'international': [
                '美联储3月利率决议即将公布，市场预期维持不变',
                '欧元区1月失业率降至6.1%历史新低',
                '特朗普提名凯文·沃什出任下任美联储主席',
            ],
            'capital_market': [
                '美股：道指48,739点，标普500报6,869点，纳指22,807点',
                'A股：沪指3,341点，市场观望情绪浓厚',
                '港股：恒生指数24,231点，能源股受油价上涨提振',
            ],
            'commodity': [
                '布伦特原油报$103.14（+2.67%），霍尔木兹海峡封锁持续',
                'COMEX黄金报$5,061.70，地缘风险支撑避险需求',
                'WTI原油报$99.85（+2.62%），美国考虑暂缓《琼斯法案》',
            ],
            'geopolitics': [
                '【极高风险】3月16日伊朗最高领袖哈梅内伊遭袭身亡',
                '霍尔木兹海峡船舶流量下降93%，全球能源供应紧张',
                '伊拉克准备削减约300万桶/日石油产量',
            ],
            'auto_industry': [
                '【新能源汽车】长城汽车2月海外销量同比增长35%，新能源渗透率38%',
                '【动力电池】国内2月装机量同比增长42%，磷酸铁锂占比超70%',
                '【智能驾驶】工信部加快明确L3/L4级智驾安全准则',
                '【汽车芯片】1-2月集成电路出口额同比增长18.5%',
                '【充电设施】国家能源局：扩大农村充电设施覆盖范围',
                '【整车交付】华为鸿蒙智行累计交付128万辆，发布新一代激光雷达',
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
                    'policy': '推进农村能源革命，扩大充电设施覆盖，支持分布式光伏',
                    'interpretation': '利好新能源产业链，预计带动千亿级投资'
                },
                {
                    'dept': '工信部',
                    'aspect': '智能驾驶',
                    'policy': '加快明确L3/L4级智驾安全准则，纳入交通违法处罚',
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
    
    def create_header_section(self, story):
        """创建页眉"""
        styles = self.styles
        
        # 公司信息
        story.append(Paragraph(self.company_name, styles['Title']))
        story.append(Paragraph(f"{self.department}    {self.date}", styles['SmallText']))
        story.append(Spacer(1, 0.3*cm))
        
        # 密级标识
        story.append(Paragraph("□ 绝密    □ 机密    □ 秘密    ☑ 一般", styles['SmallText']))
        story.append(Spacer(1, 0.5*cm))
        
        # 主标题
        story.append(Paragraph("今日财经新闻（日报）", styles['Title']))
        story.append(Spacer(1, 0.8*cm))
    
    def create_market_summary_table(self, story, data):
        """市场行情摘要表"""
        styles = self.styles
        cf = self.chinese_font
        
        story.append(Paragraph("📊 市场行情摘要", styles['SubSection']))
        
        table_data = [['指标', '数值', '涨跌', '备注']]
        
        for key, item in data['market_summary'].items():
            name_map = {
                'USDCNY': 'USD/CNY 中间价',
                'USDCNY_Spot': 'USD/CNY 市场',
                'Brent': '布伦特原油',
                'Gold': '黄金期货',
                'Shanghai': '上证指数',
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
    
    def create_news_section(self, story, title, items, icon="📰"):
        """创建新闻区块"""
        styles = self.styles
        
        story.append(Paragraph(f"{icon} {title}", styles['SubSection']))
        
        for i, item in enumerate(items, 1):
            # 检查是否为高优先级（包含【】标记）
            if '【' in item and '】' in item:
                style = styles['Highlight']
            else:
                style = styles['CNBodyText']
            
            story.append(Paragraph(f"{i}. {item}", style))
        
        story.append(Spacer(1, 0.3*cm))
    
    def create_auto_section(self, story, data):
        """汽车行业讯息专区"""
        styles = self.styles
        cf = self.chinese_font
        
        story.append(Paragraph("🚗 三、汽车行业讯息", styles['SectionHeader']))
        story.append(Spacer(1, 0.3*cm))
        
        # 使用表格展示，更专业
        auto_data = [['细分领域', '关键讯息']]
        
        category_map = {
            '【新能源汽车】': '新能源整车',
            '【动力电池】': '动力电池',
            '【智能驾驶】': '智能驾驶',
            '【汽车芯片】': '汽车芯片',
            '【充电设施】': '充电设施',
            '【整车交付】': '整车交付',
        }
        
        for item in data['auto_industry']:
            category = '行业动态'
            content = item
            
            for key, value in category_map.items():
                if key in item:
                    category = value
                    content = item.replace(key, '').strip()
                    break
            
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
        story.append(Spacer(1, 0.5*cm))
    
    def create_policy_section(self, story, data):
        """国家政策区块"""
        styles = self.styles
        
        story.append(Paragraph("🏛️ 四、国家政策", styles['SectionHeader']))
        story.append(Spacer(1, 0.3*cm))
        
        for policy in data['policies']:
            # 部委标签
            story.append(Paragraph(f"▸ {policy['dept']} | {policy['aspect']}", styles['SubSection']))
            
            # 政策内容
            story.append(Paragraph(f"<b>政策：</b>{policy['policy']}", self.styles['CNBodyText']))
            story.append(Paragraph(f"<b>解读：</b>{policy['interpretation']}", self.styles['CNBodyText']))
            story.append(Spacer(1, 0.2*cm))
    
    def generate(self, output_path=None):
        """生成PDF报告"""
        print(f"\n{'='*60}")
        print(f"📰 财经日报 PDF 专业版 - {self.date}")
        print(f"{'='*60}\n")
        
        # 获取数据
        data = self.get_today_data()
        
        # 创建PDF
        if output_path is None:
            output_dir = Path("/root/.openclaw/workspace/finance-reports")
            output_dir.mkdir(parents=True, exist_ok=True)
            date_str = datetime.now().strftime("%Y%m%d")
            output_path = output_dir / f"财经日报_{date_str}_v3.pdf"
        
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
        self.create_header_section(story)
        
        # 2. 市场行情摘要
        self.create_market_summary_table(story, data)
        story.append(PageBreak())
        
        # 3. 一、聚焦热点
        story.append(Paragraph("📈 一、聚焦热点", self.styles['SectionHeader']))
        story.append(Spacer(1, 0.3*cm))
        
        self.create_news_section(story, "资金动向", data['fund_movement'], "💰")
        self.create_news_section(story, "宏观经济", data['macro'], "📊")
        self.create_news_section(story, "国内新闻", data['domestic'], "🇨🇳")
        self.create_news_section(story, "国际新闻", data['international'], "🌍")
        self.create_news_section(story, "资本市场", data['capital_market'], "📉")
        self.create_news_section(story, "黄金原油", data['commodity'], "🛢️")
        self.create_news_section(story, "地缘风险", data['geopolitics'], "⚠️")
        
        story.append(PageBreak())
        
        # 4. 二、聚焦热点详细（表格形式）
        story.append(Paragraph("📋 二、财经要闻详情", self.styles['SectionHeader']))
        story.append(Spacer(1, 0.3*cm))
        
        # 创建详细表格
        detail_data = [['分类', '要点内容']]
        detail_items = [
            ('资金动向', '央行逆回购操作维护流动性；USD/CNY调升45bp'),
            ('宏观经济', '2月PMI 49.0%，GDP目标5%左右'),
            ('国内新闻', '华为鸿蒙智行交付128万辆；小米提交机器人建议案'),
            ('国际新闻', '美联储利率决议待公布；欧失业率降至6.1%'),
            ('资本市场', '美股波动加大；A股观望情绪浓；港股能源股上涨'),
            ('商品市场', '原油$103.14(+2.67%)；黄金$5,061.70；地缘风险驱动'),
            ('地缘风险', '【极高】伊朗最高领袖遭袭；霍尔木兹海峡封锁93%'),
        ]
        
        for cat, content in detail_items:
            detail_data.append([cat, content])
        
        table = Table(detail_data, colWidths=[3*cm, 12*cm])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self.COLORS['primary']),
            ('TEXTCOLOR', (0, 0), (-1, 0), self.COLORS['white']),
            ('FONTNAME', (0, 0), (-1, -1), self.chinese_font),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('ALIGN', (0, 0), (0, -1), 'CENTER'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BACKGROUND', (0, 1), (-1, -1), self.COLORS['light_bg']),
            ('PADDING', (0, 0), (-1, -1), 6),
        ]))
        
        story.append(table)
        story.append(Spacer(1, 0.5*cm))
        
        # 5. 三、汽车行业讯息（新增）
        self.create_auto_section(story, data)
        
        story.append(PageBreak())
        
        # 6. 四、国家政策
        self.create_policy_section(story, data)
        
        # 7. 页脚
        story.append(Spacer(1, 1*cm))
        story.append(Paragraph(
            f"数据来源：央行/国家统计局/ICE期货/Investing.com | 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')} | Finance Daily Report v3.0",
            self.styles['SmallText']
        ))
        
        # 生成PDF
        doc.build(story)
        
        print(f"✅ PDF报告已生成: {output_path}")
        print(f"   文件大小: {Path(output_path).stat().st_size / 1024:.1f} KB")
        print(f"\n{'='*60}\n")
        
        return output_path


if __name__ == "__main__":
    report = FinanceDailyReportPDF(
        company_name="公司名称",
        department="财务管理部 资金管理科"
    )
    report.generate()
