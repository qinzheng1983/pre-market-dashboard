#!/usr/bin/env python3
"""
财资周报邮件发送脚本 - 附件形式
发送2026年第22周（5月25日-29日）周报
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime

EMAIL_SENDER = "13911658378@139.com"
EMAIL_PASSWORD = "f79d697414966c63d600"
SMTP_SERVER = "smtp.139.com"
SMTP_PORT = 25

report_path = "/root/.openclaw/workspace/reports/finance_weekly_2026w22.html"

# 读取HTML文件内容用于附件
with open(report_path, 'rb') as f:
    attachment_data = f.read()

# 构建邮件
msg = MIMEMultipart()
msg['Subject'] = "财资周报 — 2026年第22周（5月25日-29日）"
msg['From'] = EMAIL_SENDER
msg['To'] = EMAIL_SENDER

# 邮件正文（纯文字摘要）
text_content = """财资周报 — 2026年第22周（5月25日-29日）

核心要点：
- USD/CNY中间价本周累计升值142点（6.8318→6.8176），即期跌至6.7685
- 在岸-中间价差扩大至490点，结汇推动即期更快升值
- DXY本周走弱：99.24→98.91，美伊"和平预期"压制美元
- Brent原油本周跌约5%（96→91美元），但"和平"可信度存疑
- 伦镍本周反弹2.1%（18,700→19,090），津巴布韦矿产新政+印尼MHP紧缺支撑
- 伦锌3,532→3,544震荡；伦锡54,600→54,720
- 碳酸锂先跌后涨，周五SMM电池级指数177,627元/吨
- 央行逆回购+MLF净投放充裕，月末小幅净回笼300亿

下周前瞻（6月1日-5日）：
- 6/1-2：美伊谈判最终进展（特朗普"最终决定"）
- 6/2：中国5月PMI
- 6/3：美国5月非农就业 + OPEC+会议
- 6/5：美国5月CPI

详细报告请查看附件中的HTML文件。
"""

msg.attach(MIMEText(text_content, 'plain', 'utf-8'))

# 添加HTML附件
part = MIMEBase('application', 'octet-stream')
part.set_payload(attachment_data)
encoders.encode_base64(part)
part.add_header(
    'Content-Disposition',
    'attachment; filename="finance_weekly_2026w22.html"'
)
msg.attach(part)

try:
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(EMAIL_SENDER, EMAIL_PASSWORD)
    server.sendmail(EMAIL_SENDER, EMAIL_SENDER, msg.as_string())
    server.quit()
    print(f"邮件发送成功！")
    print(f"收件人: {EMAIL_SENDER}")
    print(f"主题: {msg['Subject']}")
    print(f"附件: finance_weekly_2026w22.html ({len(attachment_data)} bytes)")
except Exception as e:
    print(f"邮件发送失败: {e}")
