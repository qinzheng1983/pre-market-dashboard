#!/usr/bin/env python3
"""
Email Reporter - 邮件报告发送工具
支持 139邮箱、Outlook等SMTP发送
高信息密度版: 完整报告内容 + PDF附件
"""

import argparse
import smtplib
import os
import sys
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

class EmailReporter:
    """邮件报告发送器"""
    
    SMTP_CONFIGS = {
        '139': {'server': 'smtp.139.com', 'port': 465, 'use_ssl': True, 'use_tls': False},
        'outlook': {'server': 'smtp.office365.com', 'port': 587, 'use_ssl': False, 'use_tls': True},
        'qq': {'server': 'smtp.qq.com', 'port': 465, 'use_ssl': True, 'use_tls': False},
        '163': {'server': 'smtp.163.com', 'port': 465, 'use_ssl': True, 'use_tls': False},
        'gmail': {'server': 'smtp.gmail.com', 'port': 587, 'use_ssl': False, 'use_tls': True}
    }
    
    def __init__(self, email: str = None, password: str = None, provider: str = None):
        self.email = email or os.getenv('EMAIL_SENDER')
        self.password = password or os.getenv('EMAIL_PASSWORD')
        self.provider = provider or self._detect_provider(self.email)
        
    def _detect_provider(self, email: str) -> str:
        if not email:
            return '139'
        domain = email.split('@')[-1].lower()
        if '139.com' in domain:
            return '139'
        elif 'outlook' in domain or 'hotmail' in domain or 'live' in domain:
            return 'outlook'
        elif 'qq.com' in domain:
            return 'qq'
        elif '163.com' in domain:
            return '163'
        elif 'gmail.com' in domain:
            return 'gmail'
        return '139'
    
    def send_email(self, to_email: str, subject: str, content: str, 
                   content_type: str = 'html', attachment_path: str = None) -> bool:
        """发送邮件"""
        if not self.email or not self.password:
            print("❌ 错误: 邮箱或密码未设置")
            return False
        
        config = self.SMTP_CONFIGS.get(self.provider, self.SMTP_CONFIGS['139'])
        
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email
            msg['To'] = to_email
            msg['Subject'] = subject
            
            msg.attach(MIMEText(content, content_type, 'utf-8'))
            
            if attachment_path and os.path.exists(attachment_path):
                with open(attachment_path, 'rb') as f:
                    # 根据文件类型设置正确的MIME类型
                    filename = os.path.basename(attachment_path)
                    if filename.endswith('.pdf'):
                        part = MIMEBase('application', 'pdf')
                    else:
                        part = MIMEBase('application', 'octet-stream')
                    part.set_payload(f.read())
                encoders.encode_base64(part)
                # RFC 2231编码支持中文文件名
                from email.header import Header
                part.add_header('Content-Disposition', 'attachment', filename=filename)
                msg.attach(part)
                print(f"   📎 附件已添加: {filename} ({os.path.getsize(attachment_path)//1024}KB)")
            
            print(f"   📡 连接 {config['server']}:{config['port']}...")
            
            try:
                server = smtplib.SMTP_SSL(config['server'], 465, timeout=10)
                print("   🔒 使用 SSL 连接 (端口 465)")
            except:
                server = smtplib.SMTP(config['server'], config['port'], timeout=10)
                print("   🔒 使用 TLS 连接 (端口 587)")
                if config['use_tls']:
                    server.starttls()
            
            print(f"   🔐 登录 {self.email}...")
            server.login(self.email, self.password)
            
            print(f"   📤 发送邮件到 {to_email}...")
            server.send_message(msg)
            server.quit()
            
            print("   ✅ 邮件发送成功!")
            return True
            
        except Exception as e:
            print(f"   ❌ 发送失败: {e}")
            return False
    
    def generate_pdf_report(self) -> str:
        """生成PDF报告"""
        try:
            from pdf_generator import create_risk_report_pdf
            output_path = '/root/.openclaw/workspace/skills/geopol-risk-dashboard/reports/middle_east_risk_report.pdf'
            create_risk_report_pdf(output_path)
            return output_path
        except Exception as e:
            print(f"   ⚠️ PDF生成失败: {e}")
            return None
    
    def send_risk_report(self, to_email: str, use_pdf: bool = True):
        """发送地缘风险报告 - 高信息密度版"""
        today = datetime.now().strftime('%Y年%m月%d日 %H:%M')
        subject = f"中东地缘冲突风险报告 - {today}"
        
        # 读取完整报告内容
        report_path = '/root/.openclaw/workspace/skills/geopol-risk-dashboard/reports/middle_east_risk_latest.md'
        if os.path.exists(report_path):
            with open(report_path, 'r', encoding='utf-8') as f:
                md_content = f.read()
        else:
            md_content = "报告内容暂不可用"
        
        # 构建简洁HTML (减少被拦截概率)
        html_content = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
body{{font-family:Arial,sans-serif;line-height:1.6;color:#333;max-width:800px;margin:0 auto;padding:20px;}}
h1{{color:#c41e3a;border-bottom:2px solid #c41e3a;padding-bottom:10px;}}
h2{{color:#333;border-left:4px solid #c41e3a;padding-left:10px;margin-top:25px;}}
h3{{color:#555;margin-top:20px;}}
table{{width:100%;border-collapse:collapse;margin:15px 0;font-size:13px;}}
th,td{{border:1px solid #ccc;padding:8px;text-align:left;}}
th{{background:#444;color:white;}}
tr:nth-child(even){{background:#f5f5f5;}}
pre{{background:#f8f9fa;padding:15px;overflow-x:auto;white-space:pre-wrap;font-family:monospace;font-size:13px;border:1px solid #ddd;border-radius:4px;}}
</style>
</head>
<body>
<h1>中东地缘冲突风险报告</h1>
<p><strong>报告时间:</strong> {today} | <strong>风险等级:</strong> 极高(9/10) | <strong>数据来源:</strong> Tavily实时搜索</p>
<hr>
<pre>{md_content}</pre>
<hr>
<p style="color:#666;font-size:12px;text-align:center;">
本报告由 OpenClaw 地缘冲突风险仪表盘自动生成<br>
详细PDF版本请查看邮件附件 | 下次更新: 每日 06:00<br>
免责声明: 本报告基于公开信息分析，不构成投资建议
</p>
</body>
</html>"""
        
        # 生成PDF
        pdf_path = None
        if use_pdf:
            print("   📄 生成PDF报告...")
            pdf_path = self.generate_pdf_report()
        
        return self.send_email(to_email, subject, html_content, 'html', pdf_path)

def main():
    parser = argparse.ArgumentParser(
        description='Email Reporter - 邮件报告发送工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 发送测试邮件
  EMAIL_SENDER=13911658378@139.com EMAIL_PASSWORD=xxx email_reporter.py test
  
  # 发送风险报告 (完整内容 + PDF附件)
  EMAIL_SENDER=13911658378@139.com EMAIL_PASSWORD=xxx email_reporter.py report
  
  # 发送风险报告 (无PDF)
  EMAIL_SENDER=13911658378@139.com EMAIL_PASSWORD=xxx email_reporter.py report --no-pdf

139邮箱授权码获取:
  1. 登录 139邮箱 (mail.10086.cn)
  2. 设置 → 账户 → POP3/IMAP/SMTP服务
  3. 开启 SMTP 服务
  4. 获取授权码 (不是登录密码)
        """
    )
    
    parser.add_argument('action', choices=['test', 'report', 'send'], 
                       help='操作: test=测试, report=发送风险报告, send=自定义发送')
    parser.add_argument('--to', default='13911658378@139.com',
                       help='收件人邮箱 (默认: 13911658378@139.com)')
    parser.add_argument('--subject', help='邮件主题')
    parser.add_argument('--content', help='邮件内容')
    parser.add_argument('--attachment', help='附件路径')
    parser.add_argument('--provider', choices=['139', 'outlook', 'qq', '163', 'gmail'],
                       help='邮箱服务商 (默认自动检测)')
    parser.add_argument('--no-pdf', action='store_true',
                       help='不生成PDF附件')
    
    args = parser.parse_args()
    
    print("=" * 70)
    print("📧 Email Reporter - 邮件报告发送工具")
    print("=" * 70)
    
    reporter = EmailReporter(provider=args.provider)
    
    if args.action == 'test':
        print("\n📤 发送测试邮件...")
        content = f"""<!DOCTYPE html>
<html>
<head>
<style>
body{{font-family:Arial,sans-serif;background:#f5f7fa;padding:40px;}}
.box{{background:white;padding:30px;border-radius:10px;text-align:center;max-width:500px;margin:0 auto;}}
h2{{color:#28a745;}}
.info{{color:#666;margin:15px 0;}}
.time{{color:#999;font-size:12px;}}
</style>
</head>
<body>
<div class="box">
<h2>✅ 邮件发送测试成功!</h2>
<p class="info">您的邮箱配置正确，可以正常接收报告。</p>
<p class="info"><strong>发件人:</strong> {reporter.email}</p>
<p class="info"><strong>收件人:</strong> {args.to}</p>
<p class="time">发送时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
</div>
</body>
</html>"""
        success = reporter.send_email(args.to, "✅ 邮件发送测试", content, 'html')
        
    elif args.action == 'report':
        print("\n📤 发送地缘风险报告 (高信息密度版)...")
        success = reporter.send_risk_report(args.to, use_pdf=not args.no_pdf)
        
    elif args.action == 'send':
        if not args.subject or not args.content:
            print("❌ 错误: --subject 和 --content 必填")
            return
        print(f"\n📤 发送邮件到 {args.to}...")
        success = reporter.send_email(args.to, args.subject, args.content, 
                                     'html' if '<' in args.content else 'plain',
                                     args.attachment)
    
    print("\n" + "=" * 70)
    if success:
        print("✅ 操作完成")
    else:
        print("❌ 操作失败，请检查配置")
    print("=" * 70)

if __name__ == "__main__":
    main()
