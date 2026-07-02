#!/usr/bin/env python3
"""财资周报邮件发送脚本 - 第22周"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

EMAIL_SENDER = "13911658378@139.com"
EMAIL_PASSWORD = "f79d697414966c63d600"
SMTP_SERVER = "smtp.139.com"
SMTP_PORT = 25

report_path = "/root/.openclaw/workspace/reports/finance_weekly_2026w22.html"
with open(report_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

msg = MIMEMultipart('alternative')
msg['Subject'] = "财资周报 — 2026年第22周（5月25日-29日）"
msg['From'] = EMAIL_SENDER
msg['To'] = EMAIL_SENDER

text_content = """
财资周报 — 2026年第22周（5月25日-29日）

核心要点：
- USD/CNY中间价本周从6.8318渐进回落至6.8176，累计升值142点
- 央行本周逆回购净投放充裕，MLF加量至6000亿（净投放1000亿），利率1.40%不变
- Brent原油本周大跌约5%（96→91美元），主因美伊谈判"谅解备忘录"消息
- 但财新数据显示5/28海峡仅通行3艘次，美伊双方对协议内容严重分歧，油价反弹风险仍存
- 伦铜从13731回落至13636，伦铝3664微跌，宏观面美元走强+美伊缓和双重压制
- 碳酸锂本周先跌后涨（周初大跌4%，周五反弹+600），Q2去库预期支撑
- 现货白银收于75.25美元，全周波动剧烈（最高78.80，最低71.75）
- 现货黄金约4520美元，高位震荡

CFO视角行动建议：
1. USD/CNY即期6.7734逼近6.77关口，可小幅加仓3个月远期覆盖
2. 原油Q3需求锁定30-50%套保，避免协议落空后的反弹风险
3. 镍钴采购借回调窗口分批建仓Q3需求
4. 跟踪美伊谈判最终进展（特朗普"最终决定"）

完整报告：https://qinzheng1983.github.io/pre-market-dashboard/finance-weekly/2026w22.html
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
    print("邮件发送成功！")
    print(f"收件人: {EMAIL_SENDER}")
    print(f"主题: {msg['Subject']}")
except Exception as e:
    print(f"邮件发送失败: {e}")
