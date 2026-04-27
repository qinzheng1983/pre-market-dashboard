#!/usr/bin/env python3
"""
财资日报邮件发送脚本（更新版）
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
msg['Subject'] = f"财资日报 — 2026年4月24日（周五）16:58更新版"
msg['From'] = EMAIL_SENDER
msg['To'] = EMAIL_SENDER

text_content = """
财资日报 — 2026年4月24日（周五）16:58更新版

【重要数据修正】
布伦特原油：107.24美元（+2.07%）— Investing.com历史数据表验证
（之前版本误用4月23日数据105.10，特此更正）

【今日核心数据】
- USD/CNY中间价：6.8674（+24点，连续三日渐进贬值）
- 央行：50亿逆回购，净投放45亿，利率1.40%不变
- 下周提醒：6000亿MLF到期（4月27日下周一）
- 伦镍：18,775美元（+1.68%，14周高位），印尼HPM新政驱动
- 布伦特原油：107.24美元（+2.07%），霍尔木兹海峡封锁风险推升
- 黄金：4,694美元（隔夜收跌0.97%），日内收复4700美元
- 碳酸锂：生意社170,000元/吨（+0.59%），长江有色173,000元/吨
- 地缘：美伊局势急剧升级，特朗普宣布"彻底封锁"霍尔木兹海峡

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
