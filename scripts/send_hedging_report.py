#!/usr/bin/env python3
"""
USD/CNY 套期保值分析报告邮件发送脚本
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
report_path = "/root/.openclaw/workspace/reports/usd_cny_hedging_analysis_20260420.html"
with open(report_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

# 创建邮件
msg = MIMEMultipart('alternative')
msg['Subject'] = f"USD/CNY套期保值量化分析报告 — {datetime.now().strftime('%Y年%m月%d日')}"
msg['From'] = EMAIL_SENDER
msg['To'] = EMAIL_SENDER  # 发送到发件人自己

# 纯文本版本
text_content = """
USD/CNY 套期保值量化分析报告

核心结论：
- 推荐套期保值比例：20% - 30%

关键数据：
1. 3个月套保成本（年化）：-2.38%（负成本=套保收益）
2. 近1年年化升值率：-4.43%（人民币升值）
3. 近3年年化升值率：-1.22%（人民币升值）
4. 近5年年化升值率：+1.11%（美元升值）
5. 近7年年化升值率：-0.17%（基本持平）

策略建议：
虽然当前掉期点为负值，套保产生正收益（约2.38%年化），但近1-3年数据显示人民币升值趋势明显。
建议采取"轻套保、留敞口"策略，套保比例控制在20%-30%，既可锁定部分风险，又保留人民币升值带来的汇兑收益空间。

详细数据请查看HTML报告附件。
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
