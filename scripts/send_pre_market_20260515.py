#!/usr/bin/env python3
"""
盘前简报邮件发送脚本
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

EMAIL_SENDER = "13911658378@139.com"
EMAIL_PASSWORD = "f79d697414966c63d600"
SMTP_SERVER = "smtp.139.com"
SMTP_PORT = 25

report_path = "/root/.openclaw/workspace/reports/pre_market_briefing_20260515.html"
with open(report_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

msg = MIMEMultipart('alternative')
msg['Subject'] = f"盘前简报 — 2026年5月15日（周五）09:20 行动导向v3.0"
msg['From'] = EMAIL_SENDER
msg['To'] = EMAIL_SENDER

text_content = """
盘前简报 — 2026年5月15日（周五）09:20 行动导向v3.0

【隔夜核心结论】
- 美股三大指数齐创新高，道指重新站上50,000点
- 中概股金龙指数跌3.37%，B站跌9.04%
- 人民币中间价6.8401（+30bp），在岸/离岸已升破6.80
- 黄金三连跌至$4,649，白银跌4.61%，避险资产遭抛售
- 原油Brent $106.55（+0.79%），霍尔木兹海峡船只恢复通行
- LME镍$18,935（-1.20%），碳酸锂期货跌4.57%

【HIGH风险预警】
1. 美联储高利率预期升温：CPI 3.8% + PPI 6.0%，CME定价未来12个月加息概率约50%
2. 黄金暴跌传导避险资产重估：印度将黄金进口关税从6%上调至15%

【今日5项行动】
1. 检查USD对冲覆盖率，若<60%建议在6.83-6.85补做3个月远期
2. 监控LME镍，跌破$18,500触发"关注"，跌破$18,000触发"加仓对冲"
3. 确认碳酸锂长单定价是否挂钩期货，评估Q2成本变化
4. 确认航运保险是否覆盖阿曼海域
5. 邮件北美销售负责人，确认Q2订单执行率（美国进口价格飙升+1.9%）

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
    server.sendmail(EMAIL_SENDER, [EMAIL_SENDER], msg.as_string())
    server.quit()
    print("邮件发送成功")
except Exception as e:
    print(f"邮件发送失败: {e}")
