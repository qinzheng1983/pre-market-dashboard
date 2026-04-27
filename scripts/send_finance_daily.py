#!/usr/bin/env python3
"""
财资日报邮件发送脚本
"""
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# 邮件配置
EMAIL_SENDER = "13911658378@139.com"
EMAIL_PASSWORD = "f79d697414966c63d600"  # 授权码
SMTP_SERVER = "smtp.139.com"
SMTP_PORT = 25

# 读取HTML报告
report_path = "/root/.openclaw/workspace/reports/finance_daily_report_20260424.html"
with open(report_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

# 创建邮件
msg = MIMEMultipart('alternative')
msg['Subject'] = f"财资日报 — 2026年4月24日（周五）"
msg['From'] = EMAIL_SENDER
msg['To'] = EMAIL_SENDER  # 发送到发件人自己

# 纯文本版本
text_content = """
财资日报 — 2026年4月24日

核心要点：
- USD/CNY中间价：6.8674（+24点，人民币小幅贬值）
- 央行逆回购：50亿元，净投放45亿元
- 伦镍大涨1.68%创14周高位（18,775美元/吨）
- 布伦特原油：105.10美元/桶（+3.10%）
- 现货黄金：4,694.83美元/盎司
- 地缘风险：美伊谈判僵局，霍尔木兹海峡军事化风险陡增

详细报告请查看HTML附件。
"""

# 添加纯文本和HTML内容
part1 = MIMEText(text_content, 'plain', 'utf-8')
part2 = MIMEText(html_content, 'html', 'utf-8')

msg.attach(part1)
msg.attach(part2)

# 发送邮件
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
