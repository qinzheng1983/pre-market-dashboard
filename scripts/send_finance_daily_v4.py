#!/usr/bin/env python3
"""发送财资日报邮件"""

import sys
import os

# 添加邮件发送工具到路径
sys.path.insert(0, '/root/.openclaw/workspace/skills/email-reporter/scripts')

from email_reporter import EmailReporter

# 读取HTML报告
html_path = '/root/.openclaw/workspace/reports/finance_daily_20260612_v4.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

# 初始化发送器
reporter = EmailReporter(
    email="13911658378@139.com",
    password="f79d697414966c63d600",
    provider="139"
)

# 发送邮件
reporter.send_email(
    to_email="13911658378@139.com",
    subject="财资日报 — 2026年6月12日（周五）CFO结构版 v4.1",
    content=html_content,
    content_type="html"
)

print("邮件发送成功！")
