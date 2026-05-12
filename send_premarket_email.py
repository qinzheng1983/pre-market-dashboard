#!/usr/bin/env python3
"""
发送盘前简报邮件
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# 配置
sender = "13911658378@139.com"
password = "f79d697414966c63d600"
recipient = "13911658378@139.com"
subject = "盘前简报 — 2026年5月12日（周一）09:20 行动导向版"

# 读取HTML附件
with open("reports/pre_market_briefing_20260512.html", "r", encoding="utf-8") as f:
    html_content = f.read()

# 创建简单邮件
msg = MIMEMultipart()
msg["From"] = sender
msg["To"] = recipient
msg["Subject"] = subject
msg.attach(MIMEText("盘前简报已生成：reports/pre_market_briefing_20260512.html\n\n核心数据速览：\n- USD/CNY中间价：6.8426（+41bp，央行连续两日大幅调升）\n- 布伦特原油：104.21美元（+2.88%，美伊谈判极其脆弱）\n- LME镍：19,190美元（+1.29%）\n- 美股：标普/纳指续创新高\n- A股：创业板大涨3.5%\n\n请查看workspace中的完整HTML报告。", "plain", "utf-8"))

# 发送
server = smtplib.SMTP_SSL("smtp.139.com", 465)
server.login(sender, password)
server.sendmail(sender, recipient, msg.as_string())
server.quit()

print("邮件发送成功！")
