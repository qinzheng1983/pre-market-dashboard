#!/usr/bin/env python3
"""
发送盘前简报邮件
"""
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# 邮件配置
EMAIL_SENDER = "13911658378@139.com"
EMAIL_PASSWORD = "f79d697414966c63d600"
SMTP_SERVER = "smtp.139.com"
SMTP_PORT = 465

# 收件人
TO_EMAIL = "13911658378@139.com"

# 读取HTML报告
with open('/root/.openclaw/workspace/reports/pre_market_briefing_20260414.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# 创建邮件
msg = MIMEMultipart()
msg['From'] = EMAIL_SENDER
msg['To'] = TO_EMAIL
msg['Subject'] = f"盘前简报 - 2026年4月14日 | 五星数据质量评级"

# 添加HTML内容
msg.attach(MIMEText(html_content, 'html', 'utf-8'))

# 发送邮件
try:
    print(f"📡 连接 {SMTP_SERVER}:{SMTP_PORT}...")
    server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, timeout=10)
    print(f"🔐 登录 {EMAIL_SENDER}...")
    server.login(EMAIL_SENDER, EMAIL_PASSWORD)
    print(f"📤 发送邮件到 {TO_EMAIL}...")
    server.send_message(msg)
    server.quit()
    print("✅ 盘前简报邮件发送成功!")
except Exception as e:
    print(f"❌ 发送失败: {e}")
    exit(1)
