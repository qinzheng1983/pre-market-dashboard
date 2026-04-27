#!/usr/bin/env python3
"""
盘前市场简报 - 2026年3月26日
发送专业HTML邮件到指定邮箱
"""

import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# 邮箱配置
EMAIL_SENDER = "13911658378@139.com"
EMAIL_PASSWORD = "f79d697414966c63d600"  # 139邮箱授权码
SMTP_SERVER = "smtp.139.com"
SMTP_PORT = 465

# 收件人
TO_EMAIL = "13911658378@139.com"

# 邮件主题
SUBJECT = "📊 盘前市场简报 — 2026年3月26日（周四）"

# HTML邮件内容
HTML_CONTENT = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>盘前市场简报 — 2026年3月26日</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Microsoft YaHei', sans-serif;
            background: #f5f7fa;
            color: #333;
            line-height: 1.6;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: #ffffff;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }
        .header {
            background: linear-gradient(135deg, #1a237e 0%, #283593 100%);
            color: white;
            padding: 30px 25px;
            text-align: center;
        }
        .header h1 {
            font-size: 24px;
            font-weight: 600;
            margin-bottom: 8px;
            letter-spacing: 1px;
        }
        .header .date {
            font-size: 14px;
            opacity: 0.9;
        }
        .section {
            padding: 20px 25px;
            border-bottom: 1px solid #f0f0f0;
        }
        .section:last-child {
            border-bottom: none;
        }
        .section-title {
            font-size: 16px;
            font-weight: 600;
            color: #1a237e;
            margin-bottom: 15px;
            padding-left: 12px;
            border-left: 4px solid #1a237e;
        }
        .data-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 12px;
            margin-bottom: 15px;
        }
        .data-card {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 6px;
            border-left: 3px solid #ddd;
        }
        .data-card.up { border-left-color: #d32f2f; }
        .data-card.down { border-left-color: #388e3c; }
        .data-card.neutral { border-left-color: #757575; }
        .data-label {
            font-size: 12px;
            color: #666;
            margin-bottom: 4px;
        }
        .data-value {
            font-size: 18px;
            font-weight: 600;
            color: #333;
        }
        .data-change {
            font-size: 13px;
            margin-top: 4px;
        }
        .up { color: #d32f2f; }
        .down { color: #388e3c; }
        .risk-list {
            list-style: none;
        }
        .risk-list li {
            padding: 10px 0;
            border-bottom: 1px dashed #eee;
            display: flex;
            align-items: flex-start;
        }
        .risk-list li:last-child {
            border-bottom: none;
        }
        .risk-badge {
            display: inline-block;
            padding: 2px 8px;
            border-radius: 3px;
            font-size: 11px;
            font-weight: 600;
            margin-right: 10px;
            flex-shrink: 0;
        }
        .risk-high { background: #ffebee; color: #c62828; }
        .risk-medium { background: #fff3e0; color: #ef6c00; }
        .risk-low { background: #e8f5e9; color: #2e7d32; }
        .risk-content {
            flex: 1;
        }
        .risk-title {
            font-weight: 600;
            color: #333;
            margin-bottom: 4px;
        }
        .risk-desc {
            font-size: 13px;
            color: #666;
        }
        .event-list {
            list-style: none;
        }
        .event-list li {
            padding: 8px 0;
            font-size: 14px;
            display: flex;
            align-items: center;
        }
        .event-list li::before {
            content: "•";
            color: #1a237e;
            font-weight: bold;
            margin-right: 10px;
        }
        .advice-box {
            background: #e3f2fd;
            padding: 15px;
            border-radius: 6px;
            border-left: 3px solid #1976d2;
        }
        .advice-box ol {
            margin-left: 20px;
            font-size: 14px;
        }
        .advice-box li {
            margin-bottom: 8px;
            color: #333;
        }
        .quote-box {
            background: #f5f5f5;
            padding: 15px;
            border-radius: 6px;
            margin: 10px 0;
        }
        .quote-box p {
            font-size: 14px;
            color: #555;
            font-style: italic;
        }
        .quote-box .source {
            font-size: 12px;
            color: #888;
            margin-top: 8px;
            font-style: normal;
        }
        .footer {
            background: #f8f9fa;
            padding: 20px 25px;
            text-align: center;
            font-size: 12px;
            color: #888;
        }
        .disclaimer {
            margin-top: 10px;
            padding-top: 10px;
            border-top: 1px solid #e0e0e0;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            font-size: 13px;
            margin: 10px 0;
        }
        th, td {
            padding: 10px;
            text-align: left;
            border-bottom: 1px solid #eee;
        }
        th {
            background: #f5f5f5;
            font-weight: 600;
            color: #555;
        }
        .conditions-list {
            margin: 10px 0 10px 25px;
            font-size: 13px;
        }
        .conditions-list li {
            margin-bottom: 5px;
            color: #555;
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <div class="header">
            <h1>📊 盘前市场简报</h1>
            <div class="date">2026年3月26日（周四）| 数据截至：2026-03-25收盘</div>
        </div>

        <!-- 美股 -->
        <div class="section">
            <div class="section-title">🇺🇸 美股行情（2026-03-25收盘）</div>
            <div class="data-grid">
                <div class="data-card down">
                    <div class="data-label">道琼斯指数</div>
                    <div class="data-value">46,124.06</div>
                    <div class="data-change down">▼ 0.18%</div>
                </div>
                <div class="data-card down">
                    <div class="data-label">标普500指数</div>
                    <div class="data-value">6,556.37</div>
                    <div class="data-change down">▼ 0.37%</div>
                </div>
                <div class="data-card down">
                    <div class="data-label">纳斯达克指数</div>
                    <div class="data-value">21,761.89</div>
                    <div class="data-change down">▼ 0.84%</div>
                </div>
            </div>
            <p style="font-size:13px;color:#666;">💡 美股三大指数全线收跌，科技股跌幅居前。VIX波动率指数显示市场避险情绪持续。</p>
        </div>

        <!-- A股 -->
        <div class="section">
            <div class="section-title">🇨🇳 A股行情（2026-03-25收盘）</div>
            <div class="data-grid">
                <div class="data-card up">
                    <div class="data-label">上证综指</div>
                    <div class="data-value">3,931.84</div>
                    <div class="data-change up">▲ +1.30% (+50.56点)</div>
                </div>
                <div class="data-card up">
                    <div class="data-label">深证成指</div>
                    <div class="data-value">13,801.00</div>
                    <div class="data-change up">▲ +1.95% (+264.44点)</div>
                </div>
            </div>
            <table>
                <tr>
                    <th>市场</th>
                    <th>成交额</th>
                </tr>
                <tr>
                    <td>沪市</td>
                    <td>9,679 亿元</td>
                </tr>
                <tr>
                    <td>深市</td>
                    <td>12,120 亿元</td>
                </tr>
            </table>
            <p style="font-size:13px;color:#666;">💡 A股强势反弹，沪深两市成交额突破2.1万亿，市场情绪回暖。</p>
        </div>

        <!-- 汇率 -->
        <div class="section">
            <div class="section-title">💱 汇率数据（2026-03-25/26）</div>
            <table>
                <tr>
                    <th>汇率类型</th>
                    <th>数值</th>
                    <th>变动</th>
                </tr>
                <tr>
                    <td>USD/CNY 中间价</td>
                    <td>6.8911</td>
                    <td class="up">较上日 +32基点</td>
                </tr>
                <tr>
                    <td>离岸 USD/CNH</td>
                    <td>6.9023</td>
                    <td>3月25日数据</td>
                </tr>
                <tr>
                    <td>中行折算价</td>
                    <td>689.11</td>
                    <td>100美元兑人民币</td>
                </tr>
            </table>
        </div>

        <!-- 大宗商品 -->
        <div class="section">
            <div class="section-title">🛢️ 大宗商品</div>
            <div class="data-grid">
                <div class="data-card neutral">
                    <div class="data-label">布伦特原油</div>
                    <div class="data-value">$102-107</div>
                    <div class="data-change">高位震荡</div>
                </div>
                <div class="data-card neutral">
                    <div class="data-label">WTI原油</div>
                    <div class="data-value">$88-91</div>
                    <div class="data-change">震荡上行</div>
                </div>
                <div class="data-card neutral">
                    <div class="data-label">现货黄金</div>
                    <div class="data-value">$4,560-4,650</div>
                    <div class="data-change">避险支撑</div>
                </div>
                <div class="data-card neutral">
                    <div class="data-label">现货白银</div>
                    <div class="data-value">同步上涨</div>
                    <div class="data-change">跟随黄金</div>
                </div>
            </div>
            <p style="font-size:13px;color:#666;">💡 受霍尔木兹海峡局势影响，油价维持高位震荡；黄金避险需求支撑价格。</p>
        </div>

        <!-- 地缘政治风险 -->
        <div class="section">
            <div class="section-title">🔴 地缘政治风险</div>
            <ul class="risk-list">
                <li>
                    <span class="risk-badge risk-high">极高</span>
                    <div class="risk-content">
                        <div class="risk-title">霍尔木兹海峡局势</div>
                        <div class="risk-desc">伊朗军方声明海峡局势由其掌控，敌对势力不得通行。通航量较冲突前下降95%。</div>
                    </div>
                </li>
                <li>
                    <span class="risk-badge risk-high">极高</span>
                    <div class="risk-content">
                        <div class="risk-title">美伊谈判僵局</div>
                        <div class="risk-desc">伊朗拒绝美方15点停火提议，提出五项条件：</div>
                    </div>
                </li>
            </ul>
            <ol class="conditions-list">
                <li>全面停止侵略和暗杀</li>
                <li>确保不再发动战争的保证</li>
                <li>战争赔款</li>
                <li>结束所有战线战争</li>
                <li>国际社会承认伊朗对霍尔木兹海峡主权</li>
            </ol>
            <ul class="risk-list">
                <li>
                    <span class="risk-badge risk-high">极高</span>
                    <div class="risk-content">
                        <div class="risk-title">军事部署升级</div>
                        <div class="risk-desc">美军82空降师部分部队部署中东，海军陆战队远征部队增援。</div>
                    </div>
                </li>
                <li>
                    <span class="risk-badge risk-medium">高</span>
                    <div class="risk-content">
                        <div class="risk-title">伊朗警告</div>
                        <div class="risk-desc">若遭挑衅可能开启曼德海峡新战线。</div>
                    </div>
                </li>
            </ul>
        </div>

        <!-- 机构观点 -->
        <div class="section">
            <div class="section-title">🏦 机构观点</div>
            <div class="quote-box">
                <p>"能源冲击打乱美联储计划，通胀风险支持维持利率不变。"</p>
                <div class="source">—— 美联储理事古尔斯比</div>
            </div>
            <div class="quote-box">
                <p>市场普遍预期美联储降息时点推迟至9月。能源危机转化为全球债券危机的担忧升温。</p>
                <div class="source">—— 市场共识</div>
            </div>
        </div>

        <!-- 重点关注事件 -->
        <div class="section">
            <div class="section-title">📅 重点关注事件</div>
            <ul class="event-list">
                <li><span class="risk-badge risk-high">🔴</span> 美伊五天谈判期限（3月28日截止）- 进展缓慢</li>
                <li><span class="risk-badge risk-high">🔴</span> 霍尔木兹海峡通航量较冲突前下降95%</li>
                <li><span class="risk-badge risk-medium">🟡</span> 美国副总统万斯可能周末赴巴基斯坦参与谈判</li>
                <li><span class="risk-badge risk-medium">🟡</span> 德国3月IFO商业景气指数</li>
                <li><span class="risk-badge risk-medium">🟡</span> 英国2月CPI数据</li>
            </ul>
        </div>

        <!-- 对冲建议 -->
        <div class="section">
            <div class="section-title">🛡️ 对冲建议（财资角度）</div>
            <div class="advice-box">
                <ol>
                    <li><strong>USD/CNY对冲比例：</strong>建议维持80-90%</li>
                    <li><strong>关键区间：</strong>关注6.90-6.95区间突破情况</li>
                    <li><strong>通胀风险：</strong>能源价格持续上涨可能加剧输入性通胀压力</li>
                    <li><strong>先行指标：</strong>建议监控霍尔木兹海峡通航数据作为先行指标</li>
                </ol>
            </div>
        </div>

        <!-- Footer -->
        <div class="footer">
            <p>数据来源：Wind、Bloomberg、Reuters、Tavily实时搜索</p>
            <p>报告生成时间：2026年3月26日 07:56 (GMT+8)</p>
            <div class="disclaimer">
                <p>免责声明：本报告基于公开信息整理，仅供参考，不构成投资建议。市场有风险，投资需谨慎。</p>
            </div>
        </div>
    </div>
</body>
</html>"""

def send_email():
    """发送邮件"""
    try:
        # 创建邮件
        msg = MIMEMultipart()
        msg['From'] = EMAIL_SENDER
        msg['To'] = TO_EMAIL
        msg['Subject'] = SUBJECT
        
        # 添加HTML内容
        msg.attach(MIMEText(HTML_CONTENT, 'html', 'utf-8'))
        
        # 连接SMTP服务器
        print("📡 正在连接 139邮箱服务器...")
        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, timeout=10)
        print("🔒 SSL连接已建立")
        
        # 登录
        print(f"🔐 正在登录 {EMAIL_SENDER}...")
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        
        # 发送邮件
        print(f"📤 正在发送邮件到 {TO_EMAIL}...")
        server.send_message(msg)
        server.quit()
        
        print("✅ 邮件发送成功！")
        return True
        
    except Exception as e:
        print(f"❌ 发送失败: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("📊 盘前市场简报邮件发送工具")
    print("=" * 60)
    print(f"发件人: {EMAIL_SENDER}")
    print(f"收件人: {TO_EMAIL}")
    print(f"主题: {SUBJECT}")
    print("=" * 60)
    
    success = send_email()
    
    print("=" * 60)
    if success:
        print("✅ 任务完成：盘前简报已发送至邮箱")
    else:
        print("❌ 任务失败：请检查邮箱配置")
    print("=" * 60)
