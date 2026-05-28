#!/usr/bin/env python3
"""
财资日报邮件发送脚本（2026-05-26 CFO结构版）
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

EMAIL_SENDER = "13911658378@139.com"
EMAIL_PASSWORD = "f79d697414966c63d600"
SMTP_SERVER = "smtp.139.com"
SMTP_PORT = 25

report_path = "/root/.openclaw/workspace/reports/finance_daily_20260526.html"
with open(report_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

msg = MIMEMultipart('alternative')
msg['Subject'] = f"财资日报 — 2026年5月26日（周二）16:06 CFO结构版 v4.1"
msg['From'] = EMAIL_SENDER
msg['To'] = EMAIL_SENDER

text_content = """
财资日报 — 2026年5月26日（周二）16:06 CFO结构版 v4.1

【核心数据】
- USD/CNY中间价：6.8288（+30bp，创三年新高，人民币升值）
- 央行：2490亿逆回购，净投放2485亿，利率1.40%
- 5/25加码：逆回购2580亿+MLF 6000亿，净投放3570亿
- 伦镍：18,680美元（-1.06%，盘中），超预算$2,680
- 碳酸锂：179,532元/吨（-2.34%），超预算19.69%
- 布伦特原油：95.83美元（+2.34%），5/25暴跌后反弹
- 黄金：4,532美元（-0.84%），5/25避险大涨后回调
- 美伊：协议草案达成，60天停火，待正式签署

【风险仪表盘6项】
镍价🔴高 | 碳酸锂🔴高 | 汇率🔴高 | 地缘🟡中高 | 原油🟡中 | 央行🟢低

【对我司影响】
- 净Long USD $9.5亿/月敞口，人民币升值711点→月度净不利约321万元
- 镍价超预算16.75%，年增成本约2.68亿
- 碳酸锂超预算19.69%，年增成本约1.48亿

【对冲建议】
买入USD/CNY看跌期权（执行价6.80，保护$10亿）> 领子期权 > 镍价长单重谈

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
