import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os

# 配置
sender_email = "13911658378@139.com"
sender_password = "f79d697414966c63d600"
receiver_email = "13911658378@139.com"
subject = "盘前简报 — 2026年6月4日（周四）08:30 CFO结构版"

# 读取HTML文件
report_path = "/root/.openclaw/workspace/reports/pre_market_briefing_20260604.html"
with open(report_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

# 创建邮件
msg = MIMEMultipart('alternative')
msg['From'] = sender_email
msg['To'] = receiver_email
msg['Subject'] = subject

# 添加HTML正文
msg.attach(MIMEText(html_content, 'html', 'utf-8'))

# 添加附件
with open(report_path, 'rb') as f:
    attachment = MIMEBase('application', 'octet-stream')
    attachment.set_payload(f.read())
    encoders.encode_base64(attachment)
    attachment.add_header(
        'Content-Disposition',
        'attachment; filename="pre_market_briefing_20260604.html"'
    )
    msg.attach(attachment)

# 发送邮件
try:
    server = smtplib.SMTP_SSL("smtp.139.com", 465)
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, receiver_email, msg.as_string())
    server.quit()
    print("✅ 邮件发送成功")
except Exception as e:
    print(f"❌ 邮件发送失败: {e}")
