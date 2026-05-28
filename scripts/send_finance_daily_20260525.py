#!/usr/bin/env python3
"""
财资日报邮件发送脚本 — 2026-05-25
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

EMAIL_SENDER = "13911658378@139.com"
EMAIL_PASSWORD = "f79d697414966c63d600"
SMTP_SERVER = "smtp.139.com"
SMTP_PORT = 25

report_path = "/root/.openclaw/workspace/reports/finance_daily_20260525.html"
with open(report_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

msg = MIMEMultipart('alternative')
msg['Subject'] = "财资日报 — 2026年5月25日（周一）19:22 CFO结构版 v4.1"
msg['From'] = EMAIL_SENDER
msg['To'] = EMAIL_SENDER

text_content = """
财资日报 — 2026年5月25日（周一）19:22 CFO结构版 v4.1

【核心数据】
- USD/CNY中间价：6.8318（+55点，人民币升值）
- 离岸6.7852（-0.18%），在岸/离岸价差466点
- 碳酸锂183,250元/吨（+5,250，+2.95%），超预算22.2%
- 布伦特原油95.04（-5.16%），美伊缓和驱动暴跌
- 黄金4,571（+1.43%），反弹
- 央行MLF：6,000亿操作，净投放1,000亿
- 钴价426,800元/吨（生意社基准价）
- A股科创50涨5.88%创历史新高

【风险仪表盘6项】
镍价波动🟡中 | USD/CNY净敞口🔴高 | 碳酸锂价格🔴高 | 地缘风险🟡中 | 原油价格🔴高 | 央行流动性🟢低

【对冲建议优先级】
买入USD/CNY看跌期权 > 领子期权 > 远期锁汇

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
