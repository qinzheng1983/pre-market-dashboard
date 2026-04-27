#!/usr/bin/env python3
"""
发送盘前简报邮件 - 动态日期版本
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

    # 当前日期信息
    now = datetime.now()
    today_str = now.strftime("%Y%m%d")
    today_display = now.strftime("%Y年%m月%d日")

    # 星期几
    weekdays = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    weekday = weekdays[now.weekday()]

    # 读取HTML内容 - 尝试多个可能的文件名
    possible_paths = [
        f"/root/.openclaw/workspace/reports/pre_market_briefing_{today_str}_v2.html",
        f"/root/.openclaw/workspace/reports/pre_market_briefing_{today_str}.html",
        f"/root/.openclaw/workspace/reports/pre_market_briefing_{now.strftime('%Y-%m-%d')}.html",
    ]

    html_path = None
    for path in possible_paths:
        if os.path.exists(path):
            html_path = path
            break

    if not html_path:
        print(f"❌ 找不到报告文件，尝试了: {possible_paths}")
        return False

    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # 创建邮件
    msg = MIMEMultipart('alternative')
    msg['Subject'] = f"盘前市场简报 — {today_display}（{weekday}）"
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
        print(f"主题: 盘前市场简报 — {today_display}（{weekday}）")
        print(f"发送文件: {html_path}")
        return True

    except Exception as e:
        print(f"❌ 邮件发送失败: {e}")
        return False

if __name__ == "__main__":
    send_pre_market_email()
