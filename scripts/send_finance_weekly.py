#!/usr/bin/env python3
"""
财资周报邮件发送脚本
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

EMAIL_SENDER = "13911658378@139.com"
EMAIL_PASSWORD = "f79d697414966c63d600"
SMTP_SERVER = "smtp.139.com"
SMTP_PORT = 25

report_path = "/root/.openclaw/workspace/reports/finance_weekly_2026w17.html"
with open(report_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

msg = MIMEMultipart('alternative')
msg['Subject'] = f"财资周报 — 2026年第17周（4月20日-4月24日）"
msg['From'] = EMAIL_SENDER
msg['To'] = EMAIL_SENDER

text_content = """
财资周报 — 2026年第17周（4月20日-4月24日）

核心要点：
- USD/CNY中间价本周累计+80点（6.8594→6.8674），人民币渐进贬值
- 央行本周地量操作：50亿/日，累计净投放225亿，利率1.40%不变
- 伦镍大涨1.68%创14周高位（18,775美元），印尼HPM新政+节能降碳驱动
- 布伦特原油突破100美元（105.10），霍尔木兹海峡军事化风险推升
- 现货黄金维持4,694美元高位震荡
- 地缘风险：美伊谈判僵局→军事对峙，以色列准备重启战争
- 电解钴41.3万/吨，延续阴跌，硫酸钴成本可控
- 宁德时代Q4钠电池量产，碳酸锂16-17万/吨推升钠电经济性

CFO视角行动建议：
1. 本周内完成Q2敞口重估，明确净头寸方向
2. 若净敞口为负，启动远期购汇+领子期权组合
3. 关注美伊局势→若USD/CNY突破6.95，启动紧急对冲
4. 与合作银行沟通最新场外期权报价

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
