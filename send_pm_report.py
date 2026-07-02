#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, '/root/.openclaw/workspace/skills/email-reporter/scripts')
from email_reporter import EmailReporter

with open('/root/.openclaw/workspace/reports/pre_market_briefing_20260617.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

reporter = EmailReporter(
    email='13911658378@139.com',
    password='f79d697414966c63d600',
    provider='139'
)

result = reporter.send_email(
    to_email='13911658378@139.com',
    subject='盘前市场简报 — 2026年6月17日（周三）',
    content=html_content,
    content_type='html'
)

if result:
    print('✅ 邮件发送成功')
else:
    print('❌ 邮件发送失败')
    sys.exit(1)
