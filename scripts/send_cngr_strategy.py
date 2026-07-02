#!/usr/bin/env python3
"""发送中伟Covered Call策略报告到邮箱"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

EMAIL_SENDER = "13911658378@139.com"
EMAIL_PASSWORD = "f79d697414966c63d600"
SMTP_SERVER = "smtp.139.com"
SMTP_PORT = 25

report_path = "/root/.openclaw/workspace/reports/cngr_covered_call_strategy_20260601.html"

with open(report_path, 'rb') as f:
    attachment_data = f.read()

msg = MIMEMultipart()
msg['Subject'] = "中伟新材 USD/CNY Covered Call 策略方案"
msg['From'] = EMAIL_SENDER
msg['To'] = EMAIL_SENDER

text_content = """中伟新材 USD/CNY Covered Call 策略方案

核心判断：
• 中伟净敞口 = 美元多头（北美出口+资本层面 >> 香港购汇）
• 当前 USD/CNY 在岸6.7685，周降142点，DXY 98.91偏弱
• 2025年汇兑损益激增45% → 人民币升值时受损远大于受益

策略选择：Covered Call（排除 Covered Put，敞口方向不匹配）

具体参数：
• 标的：美元应收敞口（举例50M USD）
• 卖出 USD/CNY Call @6.85，3个月到期
• 期权费：年化2.0-2.5%（约CNY 186万）
• 执行价6.85高于即期1.2%，给美元反弹留空间

三种情景：
1. 人民币继续升值（6.60）：Call失效，期权费直接补贴损失 → 最优
2. 区间震荡（6.75）：Call失效，白赚期权费 → 好
3. 美元大涨（7.10）：收益被cap在6.85，少赚约1,064万 → 可接受（概率<15%）

为什么不选Covered Put：
中伟是美元多头，Covered Put要求美元空头。卖Put等于"赌美元不跌"，当前美元偏弱时方向性错误。

执行步骤：
1. 确认净美元敞口精确金额
2. 联系中银/工银/建银询价3个月Call @6.85
3. 首轮建议50%对冲比例，保留50%裸敞口
4. 到期前30天评估展期

详细分析见附件HTML文件。
"""

msg.attach(MIMEText(text_content, 'plain', 'utf-8'))

part = MIMEBase('application', 'octet-stream')
part.set_payload(attachment_data)
encoders.encode_base64(part)
part.add_header('Content-Disposition', 'attachment; filename="cngr_covered_call_strategy_20260601.html"')
msg.attach(part)

try:
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(EMAIL_SENDER, EMAIL_PASSWORD)
    server.sendmail(EMAIL_SENDER, EMAIL_SENDER, msg.as_string())
    server.quit()
    print("邮件发送成功")
except Exception as e:
    print(f"发送失败: {e}")
