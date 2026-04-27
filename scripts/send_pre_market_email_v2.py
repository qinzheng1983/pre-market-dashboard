#!/usr/bin/env python3
"""
发送盘前简报邮件 - 2026年4月14日版本
"""

import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import ssl
from datetime import datetime

def send_pre_market_email():
    # 邮件配置
    sender = "13911658378@139.com"
    password = "f79d697414966c63d600"  # 邮箱授权码
    receiver = "13911658378@139.com"   # 发送给自己
    
    # 139邮箱SMTP设置 - 使用SSL端口
    smtp_server = "smtp.139.com"
    smtp_port = 465
    
    # 当前日期
    today = datetime.now().strftime("%Y%m%d")
    
    # 读取HTML内容 - 使用最新生成的文件
    html_path = f"/root/.openclaw/workspace/reports/pre_market_briefing_{today}_v2.html"
    
    # 如果v2版本不存在，尝试普通版本
    if not os.path.exists(html_path):
        html_path = f"/root/.openclaw/workspace/reports/pre_market_briefing_{today}.html"
    
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # 创建邮件
    msg = MIMEMultipart('alternative')
    msg['Subject'] = f"盘前市场简报 — 2026年4月14日（周二）"
    msg['From'] = sender
    msg['To'] = receiver
    
    # 添加HTML内容
    html_part = MIMEText(html_content, 'html', 'utf-8')
    msg.attach(html_part)
    
    try:
        # 连接SMTP服务器 - 使用SSL
        context = ssl.create_default_context()
        server = smtplib.SMTP_SSL(smtp_server, smtp_port, context=context)
        server.login(sender, password)
        
        # 发送邮件
        server.sendmail(sender, receiver, msg.as_string())
        server.quit()
        
        print("✅ 邮件发送成功！")
        print(f"收件人: {receiver}")
        print(f"主题: 盘前市场简报 — 2026年4月14日（周二）")
        print(f"发送文件: {html_path}")
        return True
        
    except Exception as e:
        print(f"❌ 邮件发送失败: {e}")
        return False

if __name__ == "__main__":
    send_pre_market_email()
