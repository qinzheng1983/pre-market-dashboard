#!/usr/bin/env python3
import sys
sys.path.insert(0, '/root/.openclaw/workspace/skills/email-reporter/scripts')

from email_reporter import EmailReporter
import os

# 读取HTML文件
with open('/root/.openclaw/workspace/reports/pre_market_briefing_20260410.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# 初始化发送器
reporter = EmailReporter(
    email="13911658378@139.com",
    password="f79d697414966c63d600",
    provider="139"
)

# 发送邮件
reporter.send_email(
    to_email="baichiyishi@outlook.com",
    subject="盘前市场简报 — 2026年4月10日（周五）",
    content=html_content,
    content_type="html"
)

print("邮件发送成功！")
