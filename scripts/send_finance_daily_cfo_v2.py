#!/usr/bin/env python3
"""
财资日报邮件发送脚本（v2 CFO结构版）
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

EMAIL_SENDER = "13911658378@139.com"
EMAIL_PASSWORD = "f79d697414966c63d600"
SMTP_SERVER = "smtp.139.com"
SMTP_PORT = 25

report_path = "/root/.openclaw/workspace/reports/finance_daily_20260424.html"
with open(report_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

msg = MIMEMultipart('alternative')
msg['Subject'] = f"财资日报 — 2026年4月24日（周五）17:23 CFO结构版"
msg['From'] = EMAIL_SENDER
msg['To'] = EMAIL_SENDER

text_content = """
财资日报 — 2026年4月24日（周五）17:23 CFO结构版

【核心数据】
- USD/CNY中间价：6.8674（+24点，连续三日渐进贬值，累计+80点/周）
- 央行：50亿逆回购，净投放45亿，利率1.40%
- 下周提醒：6000亿MLF到期（4月27日下周一）
- 伦镍：18,775美元（+1.68%，14周高位），印尼HPM新政+节能降碳政策
- 布伦特原油：107.24美元（+2.07%），Investing.com历史数据表验证
- 黄金：4,694美元（隔夜-0.97%），日内4,677美元
- 碳酸锂：生意社170,000元/吨（+0.59%），长江有色173,000元/吨
- 地缘：特朗普宣布"彻底封锁"霍尔木兹海峡，下令对伊朗船只开火，以色列准备重启战争

【风险仪表盘6项】
地缘风险🔴极高 | 汇率波动🔴高 | 原油价格🔴高 | 印尼政策🔴高 | 大宗商品🟡中 | 央行流动性🟢低

【对冲建议优先级】
领子期权（Collar）> 买入看跌期权 > 远期购汇

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
