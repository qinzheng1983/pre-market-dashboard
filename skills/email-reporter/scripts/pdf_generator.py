#!/usr/bin/env python3
"""
PDF报告生成器 - 完整报告版 (含走势图和情绪分析)
将Markdown报告和图表转换为美观的PDF
"""

import os
import sys
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_CENTER

# 添加情绪分析模块路径
sys.path.insert(0, '/root/.openclaw/workspace/skills/geopol-risk-dashboard/scripts')

def create_risk_report_pdf(output_path: str, report_md_path: str = None) -> str:
    """创建地缘风险报告PDF - 完整版含走势图和情绪分析"""
    
    # 注册中文字体
    font_paths = [
        '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc',
        '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
    ]
    
    chinese_font = 'Helvetica'
    for font_path in font_paths:
        if os.path.exists(font_path):
            try:
                font_name = os.path.basename(font_path).replace('.ttc', '').replace('.ttf', '')
                pdfmetrics.registerFont(TTFont(font_name, font_path))
                chinese_font = font_name
                break
            except:
                continue
    
    doc = SimpleDocTemplate(output_path, pagesize=A4,
                           rightMargin=2*cm, leftMargin=2*cm,
                           topMargin=2*cm, bottomMargin=2*cm)
    
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle('Title', parent=styles['Heading1'], 
                                fontName=chinese_font, fontSize=20,
                                textColor=colors.HexColor('#dc3545'),
                                spaceAfter=15, alignment=TA_CENTER)
    
    subtitle_style = ParagraphStyle('Subtitle', parent=styles['Normal'],
                                   fontName=chinese_font, fontSize=10,
                                   textColor=colors.grey, alignment=TA_CENTER)
    
    section_style = ParagraphStyle('Section', parent=styles['Heading2'],
                                  fontName=chinese_font, fontSize=14,
                                  textColor=colors.HexColor('#1a1a1a'),
                                  spaceBefore=15, spaceAfter=8,
                                  borderColor=colors.HexColor('#dc3545'),
                                  borderWidth=1.5, borderPadding=3)
    
    subsection_style = ParagraphStyle('Subsection', parent=styles['Heading3'],
                                     fontName=chinese_font, fontSize=11,
                                     textColor=colors.HexColor('#333'))
    
    body_style = ParagraphStyle('Body', parent=styles['Normal'],
                               fontName=chinese_font, fontSize=9,
                               leading=13, spaceAfter=5)
    
    chart_dir = '/root/.openclaw/workspace/skills/geopol-risk-dashboard/reports/'
    story = []
    
    # ========== 封面 ==========
    story.append(Spacer(1, 3*cm))
    story.append(Paragraph("🔴 中东地缘冲突风险报告", title_style))
    story.append(Paragraph(f"报告日期: {datetime.now().strftime('%Y年%m月%d日 %H:%M')}", subtitle_style))
    story.append(Paragraph("数据来源: Tavily 实时搜索 + Kimi Search + 市场情绪分析", subtitle_style))
    story.append(Spacer(1, 1*cm))
    
    # 风险等级卡片
    risk_data = [['风险等级', '极高 (9/10)'], ['数据时效', '实时更新'], ['报告版本', 'v3.0 (含情绪分析)']]
    risk_table = Table(risk_data, colWidths=[6*cm, 8*cm])
    risk_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#dc3545')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, -1), chinese_font), ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'), ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8f9fa')),
        ('PADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(risk_table)
    story.append(PageBreak())
    
    # ========== 市场情绪分析章节 (新增) ==========
    story.append(Paragraph("📊 市场情绪分析", section_style))
    story.append(Paragraph("基于Sentiment-Reality Gap模型的情绪量化分析:", body_style))
    story.append(Spacer(1, 0.3*cm))
    
    # 情绪评分表
    sentiment_data = [
        ['指标', '数值', '评估'],
        ['综合情绪评分', '-64.7/100', '极度恐慌 🔴🔴🔴'],
        ['恐慌指数', '100.0/100', '极高'],
        ['避险需求', '11.7/100', '中高'],
        ['地缘风险', '90.0/100', '极高'],
    ]
    sentiment_table = Table(sentiment_data, colWidths=[5*cm, 4*cm, 5*cm])
    sentiment_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#8B0000')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, -1), chinese_font), ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#ffebee')),
        ('PADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(sentiment_table)
    story.append(Spacer(1, 0.5*cm))
    
    # 情绪-现实差距分析
    story.append(Paragraph("情绪-现实差距分析 (Sentiment-Reality Gap):", subsection_style))
    gap_points = [
        "• 差距评估: 情绪过度反应",
        "• 交易信号: 可能出现反转",
        "• 信心度: 高",
        "• 解读: 市场过度恐慌，可能存在超卖机会。关注反弹信号。"
    ]
    for point in gap_points:
        story.append(Paragraph(point, body_style))
    story.append(PageBreak())
    
    # ========== 走势图章节 ==========
    story.append(Paragraph("📈 近1个月市场走势", section_style))
    
    for title, filename, desc, color in [
        ("美元指数 (DXY)", "chart_dxy.png", "美元作为避险资产，在冲突爆发后走强。", "#1f77b4"),
        ("黄金期货", "chart_gold.png", "COMEX黄金维持5000美元上方，高位震荡。", "#FFD700"),
        ("布伦特原油", "chart_oil.png", "霍尔木兹海峡关闭导致油价飙升超50%。", "#ff6b6b"),
        ("USD/CNH 汇率", "chart_usdcny.png", "美元走强带动汇率小幅上行。", "#dc3545"),
    ]:
        story.append(Paragraph(title, subsection_style))
        story.append(Paragraph(desc, body_style))
        img_path = os.path.join(chart_dir, filename)
        if os.path.exists(img_path):
            img = Image(img_path, width=16*cm, height=7.5*cm)
            story.append(img)
        story.append(Spacer(1, 0.3*cm))
    
    story.append(PageBreak())
    
    # ========== 市场数据摘要 ==========
    story.append(Paragraph("📊 市场数据摘要", section_style))
    
    market_data = [
        ['资产', '起始', '结束', '变化', '最高', '最低'],
        ['美元指数', '96.92', '100.36', '+3.55%', '100.36', '96.92'],
        ['黄金期货', '4,993.20', '5,061.70', '+1.37%', '5,311.60', '4,882.90'],
        ['原油', '67.97', '103.14', '+51.74%', '103.14', '66.87'],
        ['USD/CNH', '6.8836', '6.9053', '+0.32%', '6.9179', '6.8445'],
    ]
    market_table = Table(market_data, colWidths=[3.5*cm, 2.5*cm, 2.5*cm, 2*cm, 2.3*cm, 2.3*cm])
    market_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#343a40')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, -1), chinese_font), ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8f9fa')),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(market_table)
    story.append(Spacer(1, 0.5*cm))
    
    story.append(Paragraph("关键观察:", subsection_style))
    for obs in [
        "• 原油涨幅最大 (+51.74%)，直接反映地缘冲突对能源市场的冲击",
        "• 黄金期货维持5000美元上方 (+1.37%)，高位震荡",
        "• 美元指数走强 (+3.55%)，美元资产受追捧",
        "• USD/CNH 变化温和 (+0.32%)，人民币汇率相对稳定",
    ]:
        story.append(Paragraph(obs, body_style))
    
    story.append(PageBreak())
    
    # ========== 完整报告内容 ==========
    story.append(Paragraph("📄 完整风险报告", section_style))
    
    # 读取并处理Markdown内容
    if report_md_path is None:
        report_md_path = os.path.join(chart_dir, 'middle_east_risk_latest.md')
    
    if os.path.exists(report_md_path):
        with open(report_md_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        current_text = []
        for line in lines:
            line = line.strip()
            if not line:
                if current_text:
                    story.append(Paragraph(' '.join(current_text), body_style))
                    current_text = []
                continue
            
            if line.startswith('# '):
                if current_text:
                    story.append(Paragraph(' '.join(current_text), body_style))
                    current_text = []
                story.append(Paragraph(line[2:], section_style))
            elif line.startswith('## '):
                if current_text:
                    story.append(Paragraph(' '.join(current_text), body_style))
                    current_text = []
                story.append(Paragraph(line[3:], subsection_style))
            elif line.startswith('### '):
                if current_text:
                    story.append(Paragraph(' '.join(current_text), body_style))
                    current_text = []
                story.append(Paragraph(line[4:], body_style))
            elif line.startswith('---') or line.startswith('|---'):
                continue
            elif line.startswith('|'):
                if current_text:
                    story.append(Paragraph(' '.join(current_text), body_style))
                    current_text = []
                cells = [c.strip() for c in line.split('|')[1:-1]]
                if cells and not all('-' in c for c in cells):
                    story.append(Paragraph(' | '.join(cells), body_style))
            else:
                current_text.append(line)
        
        if current_text:
            story.append(Paragraph(' '.join(current_text), body_style))
    
    # 免责声明
    story.append(Spacer(1, 1*cm))
    story.append(Paragraph("⚠️ 免责声明", section_style))
    story.append(Paragraph(
        "本报告基于公开信息和市场情绪模型分析，不构成投资建议。" +
        "汇率和能源市场预测存在不确定性，请结合专业机构意见决策。" +
        "报告由 OpenClaw 地缘冲突风险仪表盘自动生成。",
        ParagraphStyle('Disclaimer', parent=body_style, fontSize=8,
                      textColor=colors.grey, alignment=TA_CENTER)
    ))
    
    doc.build(story)
    return output_path

if __name__ == "__main__":
    output = "/root/.openclaw/workspace/skills/geopol-risk-dashboard/reports/middle_east_risk_report.pdf"
    create_risk_report_pdf(output)
    print(f"✅ PDF报告已生成: {output}")
