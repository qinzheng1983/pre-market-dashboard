#!/usr/bin/env python3
"""
财资日报邮件发送脚本 — 2026年5月14日
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

EMAIL_SENDER = "13911658378@139.com"
EMAIL_PASSWORD = "f79d697414966c63d600"
SMTP_SERVER = "smtp.139.com"
SMTP_PORT = 25

report_path = "/root/.openclaw/workspace/reports/finance_daily_20260514.html"
with open(report_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

msg = MIMEMultipart('alternative')
msg['Subject'] = f"财资日报 — 2026年5月14日（周四）16:06 CFO结构版"
msg['From'] = EMAIL_SENDER
msg['To'] = EMAIL_SENDER

text_content = """
财资日报 — 2026年5月14日（周四）16:06 CFO结构版

【核心数据】
- USD/CNY中间价：6.8401（+30bp，人民币升值）
- 央行：LPR维持不变（1Y 3.00%，5Y 3.50%），4月买断式逆回购8000亿
- LME镍：$19,020（+1.57%，5/13收盘），库存275,778吨（-996吨）
- 碳酸锂：SMM 20.05万元/吨，5/14期货主力跌4.57%至192,620
- 黄金：$4,705/oz（+0.34%），美伊谈判僵局支撑避险
- 地缘：美伊谈判僵局，特朗普称伊朗回复"不可接受"

【风险仪表盘6项】
碳酸锂🔴偏高 | 地缘风险🔴高 | USD/CNY🟡关注 | 镍价🟢正常 | 央行🟢宽松

【对冲建议】
- USD/CNY：领子期权Put6.50/Call7.00（$196万成本，50%对冲$10亿Long敞口）
- 镍价：接近$20,000考虑增仓保护

详细报告请查看HTML附件。
"""

part1 = MIMEText(text_content, 'plain', 'utf-8')
part2 = MIMEText(html_content, 'html', 'utf-8')
msg.attach(part1)
msg.attach(part2)

try:
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(EMAIL_SENDER, EMAIL_PASSWORD)
    server.sendmail(EMAIL_SENDER, EMAIL_SENDER, msg.as_string())
    server.quit()
    print(f"✅ 邮件发送成功！")
    print(f"📧 收件人: {EMAIL_SENDER}")
    print(f"📨 主题: {msg['Subject']}")
except Exception as e:
    print(f"❌ 邮件发送失败: {e}")
