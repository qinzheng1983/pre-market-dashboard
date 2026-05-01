#!/usr/bin/env python3
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

# 139邮箱配置
sender_email = "13911658378@139.com"
password = "f79d697414966c63d600"
receiver_email = "baichiyishi@outlook.com"

# 创建邮件
msg = MIMEMultipart('alternative')
msg['Subject'] = Header("盘前市场简报 — 2026年4月10日（周五）", 'utf-8')
msg['From'] = sender_email
msg['To'] = receiver_email

# HTML内容
html_content = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>盘前市场简报</title>
</head>
<body style="font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px;">
    <div style="background-color: #1a1a2e; color: white; padding: 20px; text-align: center;">
        <h1>盘前市场简报</h1>
        <p>2026年4月10日（星期五）| 数据截止：2026年4月9日</p>
    </div>
    
    <div style="background-color: #fff8e1; padding: 15px; margin: 20px 0; border-left: 4px solid #f39c12;">
        <strong>今日重点关注</strong>：<br>
        1. 美伊停火协议生效但变数仍存：首轮会谈4月11日将在伊斯兰堡举行<br>
        2. 美股七连涨：标普500、纳指均录得七连涨，半导体指数创历史新高
    </div>

    <h2 style="color: #1a1a2e; border-left: 3px solid #e94560; padding-left: 10px;">全球市场概览</h2>
    <table style="width: 100%; border-collapse: collapse;">
        <tr style="background-color: #1a1a2e; color: white;">
            <th style="padding: 10px; text-align: left;">市场</th>
            <th style="padding: 10px; text-align: left;">收盘点位</th>
            <th style="padding: 10px; text-align: left;">涨跌</th>
        </tr>
        <tr><td style="padding: 10px; border-bottom: 1px solid #ddd;">标普500</td><td style="padding: 10px; border-bottom: 1px solid #ddd;">6,824.66</td><td style="padding: 10px; border-bottom: 1px solid #ddd; color: #e94560;">+0.62%</td></tr>
        <tr style="background-color: #f8f9fa;"><td style="padding: 10px; border-bottom: 1px solid #ddd;">纳斯达克</td><td style="padding: 10px; border-bottom: 1px solid #ddd;">22,822.42</td><td style="padding: 10px; border-bottom: 1px solid #ddd; color: #e94560;">+0.83%</td></tr>
        <tr><td style="padding: 10px; border-bottom: 1px solid #ddd;">道琼斯</td><td style="padding: 10px; border-bottom: 1px solid #ddd;">48,185.80</td><td style="padding: 10px; border-bottom: 1px solid #ddd; color: #e94560;">+0.58%</td></tr>
        <tr style="background-color: #f8f9fa;"><td style="padding: 10px; border-bottom: 1px solid #ddd;">布伦特原油</td><td style="padding: 10px; border-bottom: 1px solid #ddd;">$95.92</td><td style="padding: 10px; border-bottom: 1px solid #ddd; color: #e94560;">+1.23%</td></tr>
        <tr style="background-color: #ffe6e6;"><td style="padding: 10px; border-bottom: 1px solid #ddd;"><strong>USD/CNY</strong></td><td style="padding: 10px; border-bottom: 1px solid #ddd;"><strong>6.8649</strong></td><td style="padding: 10px; border-bottom: 1px solid #ddd; color: #27ae60;">+31点</td></tr>
    </table>

    <h2 style="color: #1a1a2e; border-left: 3px solid #e94560; padding-left: 10px;">重点关注事件</h2>
    <ul>
        <li><span style="background-color: #e94560; color: white; padding: 2px 8px; border-radius: 3px; font-size: 12px;">高度警惕</span> <strong>美伊停火协议变数</strong>：以色列4月9日大规模空袭黎巴嫩（254人死亡、1165人受伤），伊朗叫停霍尔木兹海峡通航。</li>
        <li><span style="background-color: #e94560; color: white; padding: 2px 8px; border-radius: 3px; font-size: 12px;">高度警惕</span> <strong>霍尔木兹海峡通航</strong>：正常每日100+艘，目前仅20+艘，阿联酋称"海峡并未开放"。</li>
        <li><span style="background-color: #f39c12; color: white; padding: 2px 8px; border-radius: 3px; font-size: 12px;">关注</span> <strong>美伊首轮会谈</strong>：4月11日在伊斯兰堡举行，美方代表团包括副总统万斯。</li>
    </ul>

    <h2 style="color: #1a1a2e; border-left: 3px solid #e94560; padding-left: 10px;">对冲建议</h2>
    <ul>
        <li><strong>汇率对冲</strong>：USD/CNY维持80-90%对冲比例</li>
        <li><strong>能源敞口</strong>：警惕布伦特$95-105区间高波动</li>
        <li><strong>黄金配置</strong>：$4,700-4,800区间择机增持</li>
    </ul>

    <hr style="margin: 30px 0;">
    <p style="font-size: 12px; color: #666; text-align: center;">
        数据来源：中国外汇交易中心、新浪财经、财新网、新华社 | 质量评级：⭐⭐⭐⭐⭐
    </p>
</body>
</html>"""

# 添加HTML内容
msg.attach(MIMEText(html_content, 'html', 'utf-8'))

# 尝试发送
try:
    print("📡 尝试连接 smtp.139.com:465...")
    context = ssl.create_default_context()
    server = smtplib.SMTP_SSL("smtp.139.com", 465, context=context, timeout=30)
    print("✅ SSL连接成功")
    
    print(f"🔐 登录 {sender_email}...")
    server.login(sender_email, password)
    print("✅ 登录成功")
    
    print(f"📤 发送邮件到 {receiver_email}...")
    server.sendmail(sender_email, receiver_email, msg.as_string())
    print(f"✅ 邮件发送成功到 {receiver_email}!")
    server.quit()
    
except Exception as e:
    print(f"❌ 发送失败: {e}")
    print("\n⚠️ 139邮箱限制发送到外部邮箱（如Outlook）")
    print("💡 解决方案：配置Outlook SMTP后重试")
    exit(1)
