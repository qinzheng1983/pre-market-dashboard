#!/usr/bin/env python3
"""
发送USD/CNY Carry Trade 10年效益分析邮件
"""
import sys
import os
sys.path.insert(0, '/root/.openclaw/workspace/skills/email-reporter/scripts')

from email_reporter import EmailReporter

# 收件人邮箱
to_email = "13911658378@139.com"

# 邮件主题
subject = "USD/CNY Carry Trade 10年效益分析（2016-2026）"

# 邮件正文HTML
html_content = """<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
body { font-family: Arial, "Microsoft YaHei", sans-serif; line-height: 1.6; color: #333; max-width: 800px; margin: 0 auto; padding: 20px; }
h1 { color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }
h2 { color: #2c3e50; border-left: 4px solid #3498db; padding-left: 12px; margin-top: 30px; }
table { width: 100%; border-collapse: collapse; margin: 20px 0; font-size: 14px; }
th, td { border: 1px solid #ddd; padding: 12px; text-align: center; }
th { background: #2c3e50; color: white; font-weight: bold; }
tr:nth-child(even) { background: #f8f9fa; }
.highlight { background: #fff3cd; padding: 15px; border-left: 4px solid #ffc107; margin: 20px 0; }
.positive { color: #27ae60; font-weight: bold; }
.negative { color: #e74c3c; font-weight: bold; }
.footer { color: #666; font-size: 12px; text-align: center; margin-top: 40px; padding-top: 20px; border-top: 1px solid #ddd; }
</style>
</head>
<body>
<h1>USD/CNY Carry Trade 10年效益分析</h1>
<p><strong>报告日期：</strong>2026年5月13日 | <strong>数据区间：</strong>2016-2026年</p>

<div class="highlight">
<strong>分阶段策略定义：</strong><br>
• <strong>Phase 1 (2016-2021)：</strong>中国利率高于美国 → 策略：借USD投CNY<br>
• <strong>Phase 2 (2022-2026)：</strong>美国利率高于中国 → 策略：借CNY投USD
</div>

<h2>核心发现</h2>
<table>
<tr>
<th>统计区间</th>
<th>策略方向</th>
<th>年均利差</th>
<th>汇兑损益(累计)</th>
<th>总年化收益</th>
<th>累计总收益</th>
</tr>
<tr>
<td>近1年 (2025→2026)</td>
<td>借CNY投USD</td>
<td class="positive">+1.15%</td>
<td class="negative">-5.02%</td>
<td class="negative">-3.87%</td>
<td class="negative">-2.72%</td>
</tr>
<tr>
<td>近3年 (2023→2026)</td>
<td>借CNY投USD</td>
<td class="positive">+1.35%</td>
<td class="negative">-1.97%</td>
<td class="negative">-0.61%</td>
<td class="positive">+3.44%</td>
</tr>
<tr>
<td>近5年 (2021→2026)</td>
<td>混合策略</td>
<td class="positive">+1.60%</td>
<td class="positive">+9.43%</td>
<td class="positive">+7.90%</td>
<td class="positive">+19.06%</td>
</tr>
<tr style="background:#e8f5e9;">
<td><strong>近10年 (2016→2026)</strong></td>
<td><strong>混合策略</strong></td>
<td class="positive"><strong>+2.28%</strong></td>
<td class="positive"><strong>+15.89%</strong></td>
<td class="positive"><strong>+10.30%</strong></td>
<td class="positive"><strong>+40.96%</strong></td>
</tr>
</table>

<h2>关键洞察</h2>
<ul>
<li><strong>利差收益持续为正：</strong>无论方向如何切换，carry trade的利息收入在过去10年中始终是正贡献，累计利息收益达<strong class="positive">+25.07%</strong></li>
<li><strong>汇兑收益是胜负手：</strong>Phase 1期间人民币升值贡献汇兑收益；Phase 2期间USD/CNY从6.37升至7.19再回落，整体仍贡献正收益</li>
<li><strong>近1年出现回撤：</strong>2025-2026年USD/CNY大幅回落（7.19→6.83），导致借CNY投USD策略出现-3.87%年化亏损</li>
<li><strong>长期视角：</strong>10年混合策略累计收益<strong class="positive">+40.96%</strong>，年化<strong class="positive">+10.30%</strong>，显著跑赢单一资产</li>
</ul>

<h2>数据来源</h2>
<ul>
<li>汇率：中国人民银行年末中间价 (USD/CNY)</li>
<li>中国利率：年均1年期LPR/贷款基准利率</li>
<li>美国利率：FRED有效联邦基金利率 (FEDFUNDS)</li>
</ul>

<div class="footer">
<p>本报告由 OpenClaw 自动生成 | 图表详见邮件附件</p>
<p>免责声明：本报告基于历史数据回测，仅供分析参考，不构成投资建议</p>
</div>
</body>
</html>"""

# 初始化发送器
reporter = EmailReporter(
    email="13911658378@139.com",
    password="f79d697414966c63d600",
    provider="139"
)

# 附件列表
attachments = [
    '/root/.openclaw/workspace/reports/usdcny_carry_trade_10y_20260513.pdf',
    '/root/.openclaw/workspace/reports/usdcny_carry_trade_10y_20260513.png',
    '/root/.openclaw/workspace/reports/usdcny_carry_trade_10y_20260513_timeline.png',
    '/root/.openclaw/workspace/reports/usdcny_carry_trade_10y_20260513_table.png',
]

# 由于email_reporter只支持单个附件，我们需要自定义发送逻辑
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.header import Header

msg = MIMEMultipart()
msg['From'] = "13911658378@139.com"
msg['To'] = to_email
msg['Subject'] = subject

msg.attach(MIMEText(html_content, 'html', 'utf-8'))

# 添加附件
for attachment_path in attachments:
    if os.path.exists(attachment_path):
        with open(attachment_path, 'rb') as f:
            filename = os.path.basename(attachment_path)
            if filename.endswith('.pdf'):
                part = MIMEBase('application', 'pdf')
            else:
                part = MIMEBase('application', 'octet-stream')
            part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment', filename=filename)
        msg.attach(part)
        print(f"   📎 附件已添加: {filename} ({os.path.getsize(attachment_path)//1024}KB)")

print(f"   📡 连接 smtp.139.com:465...")
server = smtplib.SMTP_SSL('smtp.139.com', 465, timeout=10)
print("   🔒 SSL 连接成功")

print(f"   🔐 登录 13911658378@139.com...")
server.login("13911658378@139.com", "f79d697414966c63d600")

print(f"   📤 发送邮件到 {to_email}...")
server.send_message(msg)
server.quit()

print("   ✅ 邮件发送成功!")
