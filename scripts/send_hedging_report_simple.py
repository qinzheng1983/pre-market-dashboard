#!/usr/bin/env python3
"""
USD/CNY 套期保值分析报告邮件发送脚本 - 简化版
"""
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# 邮件配置
EMAIL_SENDER = "13911658378@139.com"
EMAIL_PASSWORD = "f79d697414966c63d600"  # 授权码
SMTP_SERVER = "smtp.139.com"
SMTP_PORT = 25

# 创建邮件
msg = MIMEMultipart('alternative')
msg['Subject'] = f"USD/CNY套保分析报告 - {datetime.now().strftime('%Y%m%d')}"
msg['From'] = EMAIL_SENDER
msg['To'] = EMAIL_SENDER

# 简化HTML内容
html_content = """<html>
<head>
<style>
body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
.container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; }
h1 { color: #1a1a2e; text-align: center; border-bottom: 3px solid #e94560; padding-bottom: 15px; }
h2 { color: #1a1a2e; border-left: 4px solid #e94560; padding-left: 10px; margin-top: 30px; }
.highlight { background: #e94560; color: white; padding: 15px; border-radius: 5px; text-align: center; font-size: 18px; margin: 20px 0; }
table { width: 100%; border-collapse: collapse; margin: 20px 0; font-size: 14px; }
th { background: #1a1a2e; color: white; padding: 12px; text-align: left; }
td { padding: 10px; border-bottom: 1px solid #ddd; }
.positive { color: green; font-weight: bold; }
.negative { color: #e94560; font-weight: bold; }
.method { background: #f0f4f8; padding: 15px; border-radius: 5px; margin: 15px 0; font-family: monospace; font-size: 13px; }
.footer { text-align: center; color: #999; font-size: 12px; margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; }
</style>
</head>
<body>
<div class="container">
<h1>USD/CNY 套期保值量化分析报告</h1>

<div class="highlight">
推荐套期保值比例：20% - 30%
</div>

<h2>核心指标摘要</h2>
<table>
<tr><th>指标</th><th>数值</th><th>说明</th></tr>
<tr><td>USD/CNY现汇汇率</td><td>6.8200</td><td>2026-04-17</td></tr>
<tr><td>3个月掉期点</td><td>-406 Pips</td><td>2026-03数据</td></tr>
<tr><td>套保成本（年化）</td><td class="positive">-2.38%</td><td>负成本=套保有收益</td></tr>
<tr><td>近1年升值率</td><td class="positive">-4.43%</td><td>人民币升值</td></tr>
<tr><td>近3年升值率</td><td class="positive">-1.22%</td><td>人民币升值</td></tr>
<tr><td>近5年升值率</td><td class="negative">+1.11%</td><td>美元升值</td></tr>
<tr><td>近7年升值率</td><td>-0.17%</td><td>基本持平</td></tr>
</table>

<h2>套保成本计算</h2>
<div class="method">
公式：套保成本 = (掉期点/10000) / 即期汇率 * (12/3) * 100%<br>
代入：(-406/10000) / 6.82 * 4 * 100% = <b>-2.38%</b>
</div>

<h2>年化升值率计算（对数法）</h2>
<div class="method">
公式：年化升值率 = ln(期末汇率/期初汇率) / 年数 * 100%<br><br>
近1年：ln(6.82/7.129) = <span class="positive">-4.43%</span><br>
近3年：ln(6.82/7.075)/3 = <span class="positive">-1.22%</span><br>
近5年：ln(6.82/6.452)/5 = <span class="negative">+1.11%</span><br>
近7年：ln(6.82/6.8985)/7 = -0.17%
</div>

<h2>策略建议</h2>
<p><b>1. 套保成本优势</b><br>
当前3个月掉期点为负值，套保产生约2.38%的年化额外收益，是难得的套保窗口期。</p>

<p><b>2. 汇率趋势风险</b><br>
近1-3年数据显示人民币升值趋势明显（年均升值1-4%），过度套保可能错失升值收益。</p>

<p><b>3. 操作建议</b><br>
• 基础套保：20%（锁定最低风险）<br>
• 适度套保：20%-30%（平衡风险与收益）<br>
• 不建议超过：50%（机会成本过高）<br>
• 关注6.90-7.00区间加仓套保机会</p>

<div class="footer">
报告日期：2026年4月20日<br>
数据来源：中国货币网 / CEIC / Investing.com / IRS<br>
本报告由 OpenClaw AI 生成，仅供参考
</div>
</div>
</body>
</html>"""

# 纯文本版本
text_content = """
USD/CNY 套期保值量化分析报告
================================

推荐套期保值比例：20% - 30%

【核心指标】
USD/CNY现汇汇率：6.8200 (2026-04-17)
3个月掉期点：-406 Pips
套保成本（年化）：-2.38% (负成本=套保有收益)

【历史年化升值率】
近1年：-4.43% (人民币升值)
近3年：-1.22% (人民币升值)
近5年：+1.11% (美元升值)
近7年：-0.17% (基本持平)

【计算方法】
套保成本 = (掉期点/10000) / 即期汇率 * (12/3) * 100%
= (-406/10000) / 6.82 * 4 * 100% = -2.38%

年化升值率 = ln(期末汇率/期初汇率) / 年数 * 100%
近1年：ln(6.82/7.129) = -4.43%

【策略建议】
虽然当前套保产生正收益(2.38%)，但人民币升值趋势明显。
建议轻套保、留敞口，套保比例20%-30%为宜。

报告日期：2026年4月20日
数据来源：中国货币网 / CEIC / Investing.com
"""

# 添加内容
part1 = MIMEText(text_content, 'plain', 'utf-8')
part2 = MIMEText(html_content, 'html', 'utf-8')

msg.attach(part1)
msg.attach(part2)

# 发送邮件
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
