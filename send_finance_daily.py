#!/usr/bin/env python3
import sys
sys.path.insert(0, '/root/.openclaw/workspace/skills/email-reporter/scripts')
from email_reporter import EmailReporter

# 读取HTML内容
with open('/root/.openclaw/workspace/reports/finance_daily_20250415.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# 初始化发送器
reporter = EmailReporter(
    email='13911658378@139.com',
    password='f79d697414966c63d600',
    provider='139'
)

# 发送邮件
success = reporter.send_email(
    to_email='13911658378@139.com',
    subject='📊 财资日报 — 2026年4月15日（完整版）',
    content=html_content,
    content_type='html'
)

if success:
    print("✅ 财资日报发送成功！")
else:
    print("❌ 发送失败")
    sys.exit(1)
