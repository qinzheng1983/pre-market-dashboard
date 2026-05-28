#!/usr/bin/env python3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

# 配置
sender = '13911658378@139.com'
password = 'f79d697414966c63d600'
receiver = '13911658378@139.com'
subject = '盘前简报 — 2026年5月28日（周四）08:45 CFO结构版 v3.0'

# 读取HTML内容
with open('/root/.openclaw/workspace/reports/pre_market_briefing_20260528.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# 构造邮件
msg = MIMEMultipart()
msg['From'] = sender
msg['To'] = receiver
msg['Subject'] = Header(subject, 'utf-8')

msg.attach(MIMEText(html_content, 'html', 'utf-8'))

# 发送
try:
    server = smtplib.SMTP_SSL('smtp.139.com', 465)
    server.login(sender, password)
    server.sendmail(sender, [receiver], msg.as_string())
    server.quit()
    print("✅ 邮件发送成功")
except Exception as e:
    print(f"❌ 邮件发送失败: {e}")
