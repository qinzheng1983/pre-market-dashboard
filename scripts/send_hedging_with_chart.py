#!/usr/bin/env python3
"""
USD/CNY 套期保值分析报告 - 生成柱状图图片并发送邮件
"""
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from datetime import datetime
import io

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial Unicode MS', 'SimHei', 'Noto Sans CJK SC']
plt.rcParams['axes.unicode_minus'] = False

# 邮件配置
EMAIL_SENDER = "13911658378@139.com"
EMAIL_PASSWORD = "f79d697414966c63d600"
SMTP_SERVER = "smtp.139.com"
SMTP_PORT = 25

def create_chart():
    """生成柱状图"""
    categories = [
        '3M Hedging\nCost (Ann.)',
        '1Y\nAppreciation', 
        '3Y\nAppreciation',
        '5Y\nAppreciation', 
        '7Y\nAppreciation'
    ]
    values = [-2.38, -4.43, -1.22, 1.11, -0.17]
    
    colors = ['#e94560', '#27ae60', '#27ae60', '#ff6b6b', '#6c757d']
    edge_colors = ['#c73e54', '#219a52', '#219a52', '#e94560', '#5a6268']
    
    fig, ax = plt.subplots(figsize=(12, 7))
    
    bars = ax.bar(categories, values, color=colors, edgecolor=edge_colors, linewidth=2, width=0.6)
    
    # 添加数值标签
    for bar, val in zip(bars, values):
        height = bar.get_height()
        y_pos = height + 0.15 if height >= 0 else height - 0.35
        color = '#1a1a2e'
        ax.annotate(f'{val:+.2f}%',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 5 if height >= 0 else -15),
                    textcoords="offset points",
                    ha='center', va='bottom' if height >= 0 else 'top',
                    fontsize=14, fontweight='bold', color=color)
    
    # 添加零线
    ax.axhline(y=0, color='#1a1a2e', linestyle='-', linewidth=1.5)
    
    # 添加区域标注
    ax.fill_between(range(len(categories)), 0, 5, alpha=0.08, color='#e94560', label='USD Appreciation Zone')
    ax.fill_between(range(len(categories)), -6, 0, alpha=0.08, color='#27ae60', label='CNY Appreciation Zone')
    
    # 标题和标签
    ax.set_title('USD/CNY Hedging Cost vs Historical Annualized Appreciation Rate\n(Quantitative Analysis for Hedging Ratio Decision)', 
                 fontsize=16, fontweight='bold', color='#1a1a2e', pad=20)
    ax.set_ylabel('Annualized Percentage (%)', fontsize=13, fontweight='bold', color='#1a1a2e')
    
    # Y轴设置
    ax.set_ylim(-6, 3)
    ax.set_yticks(np.arange(-6, 4, 1))
    ax.set_yticklabels([f'{x}%' for x in range(-6, 4, 1)], fontsize=11)
    
    # X轴设置
    ax.tick_params(axis='x', labelsize=11)
    ax.set_xticklabels(categories, fontsize=11)
    
    # 网格
    ax.yaxis.grid(True, linestyle='--', alpha=0.4)
    ax.set_axisbelow(True)
    
    # 边框
    for spine in ax.spines.values():
        spine.set_color('#dee2e6')
        spine.set_linewidth(1)
    
    # 图例
    ax.legend(loc='upper right', fontsize=10, framealpha=0.9)
    
    plt.tight_layout()
    
    # 保存到内存
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=150, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    buf.seek(0)
    plt.close()
    
    return buf.read()

def create_html_content():
    """创建HTML正文"""
    html = """<html>
<head>
<style>
body { font-family: Arial, 'Microsoft YaHei', sans-serif; margin: 20px; background: #f5f5f5; }
.container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; }
h1 { color: #1a1a2e; text-align: center; border-bottom: 3px solid #e94560; padding-bottom: 15px; }
h2 { color: #1a1a2e; border-left: 4px solid #e94560; padding-left: 10px; margin-top: 30px; }
.highlight { background: #e94560; color: white; padding: 20px; border-radius: 5px; text-align: center; margin: 20px 0; }
.highlight .big { font-size: 32px; font-weight: bold; }
table { width: 100%; border-collapse: collapse; margin: 20px 0; font-size: 14px; }
th { background: #1a1a2e; color: white; padding: 12px; text-align: center; }
td { padding: 10px; border: 1px solid #ddd; text-align: center; }
.positive { color: #27ae60; font-weight: bold; }
.negative { color: #e94560; font-weight: bold; }
.chart-note { background: #fff3cd; padding: 15px; border-radius: 5px; margin: 15px 0; color: #856404; }
.footer { text-align: center; color: #999; font-size: 12px; margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; }
</style>
</head>
<body>
<div class="container">
<h1>USD/CNY 套期保值量化分析报告</h1>

<div class="highlight">
<div style="font-size: 14px; margin-bottom: 10px; opacity: 0.9;">基于掉期点与历史升值率的套保比例建议</div>
<div class="big">推荐套保比例：20% - 30%</div>
</div>

<div class="chart-note">
<b>📊 柱状图说明：</b>请查看邮件附件中的 <b>usd_cny_hedging_chart.png</b> 获取完整柱状图可视化
</div>

<h2>核心数据汇总</h2>
<table>
<tr><th>指标</th><th>数值</th><th>说明</th></tr>
<tr><td>USD/CNY现汇汇率</td><td>6.8200</td><td>2026-04-17</td></tr>
<tr><td>3个月掉期点</td><td class="negative">-406 Pips</td><td>央行数据</td></tr>
<tr><td>套保成本(年化)</td><td class="positive">-2.38%</td><td>负成本=收益</td></tr>
<tr><td>近1年年化升值率</td><td class="positive">-4.43%</td><td>人民币升值</td></tr>
<tr><td>近3年年化升值率</td><td class="positive">-1.22%</td><td>人民币升值</td></tr>
<tr><td>近5年年化升值率</td><td class="negative">+1.11%</td><td>美元升值</td></tr>
<tr><td>近7年年化升值率</td><td>-0.17%</td><td>基本持平</td></tr>
</table>

<h2>计算方法</h2>
<p><b>套保成本年化：</b></p>
<p style="background: #f0f0f0; padding: 15px; border-radius: 5px; font-family: monospace;">
(-406/10000) / 6.82 × 4 × 100% = <span class="positive"><b>-2.38%</b></span>
</p>

<p><b>年化升值率（对数法）：</b></p>
<p style="background: #f0f0f0; padding: 15px; border-radius: 5px; font-family: monospace;">
ln(6.82/7.129) / 1 = <span class="positive"><b>-4.43%</b></span> (1年)<br>
ln(6.82/7.075) / 3 = <span class="positive"><b>-1.22%</b></span> (3年)<br>
ln(6.82/6.452) / 5 = <span class="negative"><b>+1.11%</b></span> (5年)
</p>

<h2>策略建议</h2>
<p>当前3个月掉期点为负值，套保产生约<b>2.38%</b>的年化正收益，是难得的套保窗口期。</p>
<p>但近1-3年数据显示人民币升值趋势明显（年均升值1-4%），过度套保将面临较大机会成本。</p>
<p>建议采取<b>"轻套保、留敞口"</b>策略，套保比例控制在<b style="color: #e94560;">20%-30%</b>，既可锁定部分风险，又保留人民币升值带来的汇兑收益空间。</p>

<div class="footer">
报告日期：2026年4月20日 | 数据来源：中国货币网 / CEIC / Investing.com<br>
本报告由 OpenClaw AI 生成，仅供参考
</div>
</div>
</body>
</html>"""
    return html

def send_email():
    """发送邮件"""
    # 生成图表
    chart_image = create_chart()
    
    # 创建邮件
    msg = MIMEMultipart('related')
    msg['Subject'] = f"USD/CNY套保分析-带柱状图-{datetime.now().strftime('%Y%m%d')}"
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_SENDER
    
    # HTML正文
    html_content = create_html_content()
    msg.attach(MIMEText(html_content, 'html', 'utf-8'))
    
    # 添加图表图片
    image = MIMEImage(chart_image)
    image.add_header('Content-ID', '<chart>')
    image.add_header('Content-Disposition', 'attachment', filename='usd_cny_hedging_chart.png')
    msg.attach(image)
    
    # 发送
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, EMAIL_SENDER, msg.as_string())
        server.quit()
        print("✅ 邮件发送成功！")
        print(f"📧 收件人: {EMAIL_SENDER}")
        print(f"📨 主题: {msg['Subject']}")
        print(f"📊 附件: usd_cny_hedging_chart.png (柱状图)")
    except Exception as e:
        print(f"❌ 邮件发送失败: {e}")

if __name__ == "__main__":
    send_email()
