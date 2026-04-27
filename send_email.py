#!/usr/bin/env python3
"""发送财资日报邮件"""

import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

# 邮件配置
SENDER_EMAIL = "13911658378@139.com"
SENDER_PASSWORD = "f79d697414966c63d600"
RECEIVER_EMAIL = "13911658378@139.com"
SMTP_SERVER = "smtp.139.com"
SMTP_PORT = 465

# 读取HTML内容 - 财资日报
with open("/root/.openclaw/workspace/reports/finance_daily_20260408_v2.html", "r", encoding="utf-8") as f:
    html_content = f.read()

# 创建邮件
msg = MIMEMultipart()
msg['From'] = SENDER_EMAIL
msg['To'] = RECEIVER_EMAIL
msg['Subject'] = Header("财资日报 — 2026年4月8日（完整版）", "utf-8")

# 添加HTML内容
msg.attach(MIMEText(html_content, "html", "utf-8"))

# 发送邮件
try:
    server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
    server.login(SENDER_EMAIL, SENDER_PASSWORD)
    server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
    server.quit()
    print("✅ 邮件发送成功！")
except Exception as e:
    print(f"❌ 邮件发送失败: {e}")
