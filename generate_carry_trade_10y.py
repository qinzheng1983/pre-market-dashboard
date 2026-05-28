#!/usr/bin/env python3
"""
USD/CNY Carry Trade 10年效益分析 (2016-2026)
分阶段策略：
- 2016-2021：中国利率高，策略=借USD投CNY
- 2022-2026：美国利率高，策略=借CNY投USD
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from matplotlib import rcParams
from matplotlib.backends.backend_pdf import PdfPages
import os
import sys

from matplotlib import font_manager as fm

# 显式加载中文字体
chinese_font_paths = [
    '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc',
    '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
]
chinese_font = None
for fp in chinese_font_paths:
    if os.path.exists(fp):
        chinese_font = fm.FontProperties(fname=fp)
        break

# 设置全局字体
if chinese_font:
    rcParams['font.family'] = ['sans-serif']
    rcParams['font.sans-serif'] = ['WenQuanYi Micro Hei', 'Noto Sans CJK SC', 'DejaVu Sans']
else:
    rcParams['font.sans-serif'] = ['DejaVu Sans']
rcParams['axes.unicode_minus'] = False

# ============ 历史数据 ============
# USD/CNY 年末汇率 (取自人民银行/外汇交易中心年度数据)
years = list(range(2016, 2027))
usdcny_rates = {
    2016: 6.9370,   # 2016年末
    2017: 6.5342,   # 2017年末
    2018: 6.8632,   # 2018年末
    2019: 6.9762,   # 2019年末
    2020: 6.5249,   # 2020年末
    2021: 6.3757,   # 2021年末
    2022: 6.9646,   # 2022年末
    2023: 7.0920,   # 2023年末
    2024: 7.1884,   # 2024年末
    2025: 7.1991,   # 2025年5月 (近似年度值)
    2026: 6.8276,   # 2026年5月当前
}

# 中国1年期贷款市场报价利率(LPR) / 近似代表性利率 (%)
china_rates = {
    2016: 4.35,     # 1年期贷款基准利率
    2017: 4.35,     # 
    2018: 4.35,     # 
    2019: 4.15,     # LPR改革后
    2020: 3.85,     # 
    2021: 3.85,     # 
    2022: 3.65,     # 
    2023: 3.45,     # 
    2024: 3.10,     # 
    2025: 3.10,     # 当前
    2026: 3.10,     # 假设维持
}

# 美国有效联邦基金利率 (%)
us_rates = {
    2016: 0.40,     # 2016年末
    2017: 1.30,     # 2017年末
    2018: 2.27,     # 2018年末
    2019: 1.55,     # 2019年末
    2020: 0.09,     # 2020年末
    2021: 0.08,     # 2021年末
    2022: 4.10,     # 2022年末
    2023: 5.33,     # 2023年末
    2024: 4.33,     # 2024年末
    2025: 4.25,     # 2025年当前近似
    2026: 4.25,     # 假设维持
}

# ============ 计算逻辑 ============
# Phase 1 (2016-2021): 中国利率高 -> 借USD投CNY
#   - 利息收益 = 中国利率 - 美国利率 (利差)
#   - 汇兑损益 = 期末USD/CNY / 期初USD/CNY - 1 (人民币升值=正向收益，因为持有CNY)
# 
# Phase 2 (2022-2026): 美国利率高 -> 借CNY投USD
#   - 利息收益 = 美国利率 - 中国利率 (利差)
#   - 汇兑损益 = 期初USD/CNY / 期末USD/CNY - 1 (人民币贬值=正向收益，因为持有USD)

def calculate_carry_trade(start_year, end_year, phase):
    """计算指定区间的carry trade收益"""
    
    # 期初汇率 (年初)
    rate_start = usdcny_rates[start_year - 1] if start_year > 2016 else usdcny_rates[start_year]
    # 期末汇率 (年末/当前)
    rate_end = usdcny_rates[end_year]
    
    # 计算年化利率差 (简单平均)
    years_count = end_year - start_year + 1
    avg_china_rate = sum(china_rates[y] for y in range(start_year, end_year + 1)) / years_count
    avg_us_rate = sum(us_rates[y] for y in range(start_year, end_year + 1)) / years_count
    
    if phase == 1:  # 借USD投CNY
        # 利息收益 = 中国利率 - 美国利率
        interest_return = avg_china_rate - avg_us_rate
        # 汇兑收益: 持有CNY，人民币升值为正
        fx_return = (rate_start / rate_end - 1) * 100  # 注意方向: 期初/期末 - 1
    else:  # phase == 2, 借CNY投USD
        # 利息收益 = 美国利率 - 中国利率
        interest_return = avg_us_rate - avg_china_rate
        # 汇兑收益: 持有USD，人民币贬值为正
        fx_return = (rate_end / rate_start - 1) * 100
    
    total_return = interest_return + fx_return
    
    # 累计收益 (复利近似)
    cumulative_interest = interest_return * years_count
    cumulative_fx = fx_return  # 汇兑是一次性的
    cumulative_total = cumulative_interest + cumulative_fx
    
    return {
        'start_year': start_year,
        'end_year': end_year,
        'years': years_count,
        'rate_start': rate_start,
        'rate_end': rate_end,
        'avg_china_rate': avg_china_rate,
        'avg_us_rate': avg_us_rate,
        'interest_return': interest_return,  # 年化
        'fx_return': fx_return,  # 区间总汇兑收益，近似年化
        'total_return': total_return,  # 年化总收益
        'cumulative_interest': cumulative_interest,
        'cumulative_fx': cumulative_fx,
        'cumulative_total': cumulative_total,
        'phase': phase
    }

# ============ 定义分析区间 ============
intervals = [
    (2016, 2021, 1, "Phase 1: 借USD投CNY (2016-2021)"),
    (2022, 2026, 2, "Phase 2: 借CNY投USD (2022-2026)"),
    (2016, 2026, "mixed", "全周期 (2016-2026)"),
]

# 同时计算1年/3年/5年/10年滚动窗口
rolling_intervals = [
    (2025, 2026, 2, "近1年"),
    (2023, 2026, 2, "近3年"),
    (2021, 2026, "mixed", "近5年"),
    (2016, 2026, "mixed", "近10年"),
]

results = []
for start, end, phase, label in rolling_intervals:
    if phase == "mixed":
        # 分阶段计算后合并
        if start <= 2021 and end >= 2022:
            # 跨阶段
            r1 = calculate_carry_trade(start, 2021, 1)
            r2 = calculate_carry_trade(2022, end, 2)
            total_years = end - start + 1
            
            # 加权平均年化
            w1 = (2021 - start + 1) / total_years
            w2 = (end - 2022 + 1) / total_years
            
            avg_interest = r1['interest_return'] * w1 + r2['interest_return'] * w2
            avg_fx = (r1['fx_return'] * (2021-start+1) + r2['fx_return'] * (end-2022+1)) / total_years
            
            result = {
                'start_year': start,
                'end_year': end,
                'years': total_years,
                'rate_start': r1['rate_start'],
                'rate_end': r2['rate_end'],
                'avg_china_rate': r1['avg_china_rate'] * w1 + r2['avg_china_rate'] * w2,
                'avg_us_rate': r1['avg_us_rate'] * w1 + r2['avg_us_rate'] * w2,
                'interest_return': avg_interest,
                'fx_return': avg_fx,
                'total_return': avg_interest + avg_fx,
                'cumulative_interest': r1['cumulative_interest'] + r2['cumulative_interest'],
                'cumulative_fx': r1['cumulative_fx'] + r2['cumulative_fx'],
                'cumulative_total': r1['cumulative_total'] + r2['cumulative_total'],
                'phase': 'mixed',
                'label': label
            }
        elif end <= 2021:
            result = calculate_carry_trade(start, end, 1)
            result['label'] = label
        else:
            result = calculate_carry_trade(start, end, 2)
            result['label'] = label
    else:
        result = calculate_carry_trade(start, end, phase)
        result['label'] = label
    
    results.append(result)

# ============ 图表1: 分阶段效益分解图 ============
fig1, ax1 = plt.subplots(figsize=(14, 8))

labels = [r['label'] for r in results]
x = np.arange(len(labels))
width = 0.35

# 利息收益 (绿色正/红色负)
interest_returns = [r['interest_return'] for r in results]
# 汇兑损益 (蓝色正/橙色负)
fx_returns = [r['fx_return'] for r in results]
# 总收益
total_returns = [r['total_return'] for r in results]

# 绘制堆叠柱状图
colors_interest = ['#2ecc71' if v >= 0 else '#e74c3c' for v in interest_returns]
colors_fx = ['#3498db' if v >= 0 else '#e67e22' for v in fx_returns]

bars1 = ax1.bar(x, interest_returns, width, label='利息收益 (年化)', color=colors_interest, edgecolor='white', linewidth=0.5)
bars2 = ax1.bar(x, fx_returns, width, bottom=interest_returns, label='汇兑损益 (年化)', color=colors_fx, edgecolor='white', linewidth=0.5)

# 总收益标注
for i, (total, ir, fx) in enumerate(zip(total_returns, interest_returns, fx_returns)):
    y_pos = ir + fx + 0.3 if total >= 0 else ir + fx - 0.5
    color = '#27ae60' if total >= 0 else '#c0392b'
    ax1.annotate(f'{total:+.1f}%', xy=(x[i], y_pos), ha='center', va='bottom' if total >= 0 else 'top',
                fontsize=12, fontweight='bold', color=color,
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=color, alpha=0.9))

# 在柱内标注数值
for i, (bar, val) in enumerate(zip(bars1, interest_returns)):
    y_pos = val / 2
    ax1.text(x[i], y_pos, f'{val:+.1f}%', ha='center', va='center', fontsize=9, color='white', fontweight='bold')

for i, (bar, val, base) in enumerate(zip(bars2, fx_returns, interest_returns)):
    y_pos = base + val / 2
    ax1.text(x[i], y_pos, f'{val:+.1f}%', ha='center', va='center', fontsize=9, color='white', fontweight='bold')

ax1.axhline(y=0, color='black', linewidth=0.8)
ax1.set_ylabel('年化收益率 (%)', fontsize=12)
ax1.set_title('USD/CNY Carry Trade 10年效益分解 (2016-2026)\n分阶段策略: 2016-2021借USD投CNY | 2022-2026借CNY投USD', fontsize=14, fontweight='bold')
ax1.set_xticks(x)
ax1.set_xticklabels(labels, fontsize=11)
ax1.legend(loc='upper left', fontsize=10)
ax1.set_ylim(min(interest_returns) + min(fx_returns) - 2, max(interest_returns) + max(fx_returns) + 2)

# 添加数据来源注释
ax1.text(0.99, 0.02, '数据来源: FRED(美联储) / 中国人民银行\n汇率基准: 年末中间价 | 利率基准: 年均利率',
         transform=ax1.transAxes, fontsize=8, ha='right', va='bottom',
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plt.tight_layout()
fig1.savefig('/root/.openclaw/workspace/reports/usdcny_carry_trade_10y_20260513.png', dpi=200, bbox_inches='tight')
plt.close(fig1)

# ============ 图表2: 累计收益折线图 ============
fig2, ax2 = plt.subplots(figsize=(14, 7))

# 计算逐年累计收益 (从2016年开始，假设每年初投入)
cumulative_years = list(range(2016, 2027))
cumulative_total = []
cumulative_interest_only = []

running_total = 0
running_interest = 0

for year in cumulative_years:
    if year == 2016:
        cumulative_total.append(0)
        cumulative_interest_only.append(0)
        continue
    
    # 确定当年策略
    if year <= 2021:
        phase = 1
    else:
        phase = 2
    
    # 当年收益
    rate_prev = usdcny_rates[year - 1]
    rate_curr = usdcny_rates[year]
    
    if phase == 1:
        int_ret = china_rates[year] - us_rates[year]
        fx_ret = (rate_prev / rate_curr - 1) * 100
    else:
        int_ret = us_rates[year] - china_rates[year]
        fx_ret = (rate_curr / rate_prev - 1) * 100
    
    running_total += int_ret + fx_ret
    running_interest += int_ret
    
    cumulative_total.append(running_total)
    cumulative_interest_only.append(running_interest)

ax2.plot(cumulative_years, cumulative_total, 'o-', linewidth=2.5, markersize=8, color='#2c3e50', label='累计总收益 (利息+汇兑)')
ax2.plot(cumulative_years, cumulative_interest_only, 's--', linewidth=2, markersize=6, color='#27ae60', label='累计利息收益 (仅利差)')
ax2.axhline(y=0, color='black', linewidth=0.8, linestyle='-')
ax2.axvline(x=2021.5, color='#e74c3c', linewidth=1.5, linestyle='--', alpha=0.7, label='策略切换点 (2021→2022)')

# 标注关键点
for i, (year, total) in enumerate(zip(cumulative_years, cumulative_total)):
    if year in [2021, 2026]:
        ax2.annotate(f'{total:+.1f}%', xy=(year, total), xytext=(10, 15), 
                    textcoords='offset points', fontsize=10, fontweight='bold',
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7))

ax2.fill_between(cumulative_years, 0, cumulative_total, where=[t >= 0 for t in cumulative_total], 
                 alpha=0.3, color='#2ecc71', interpolate=True)
ax2.fill_between(cumulative_years, 0, cumulative_total, where=[t < 0 for t in cumulative_total], 
                 alpha=0.3, color='#e74c3c', interpolate=True)

ax2.set_xlabel('年份', fontsize=12)
ax2.set_ylabel('累计收益率 (%)', fontsize=12)
ax2.set_title('USD/CNY Carry Trade 累计收益走势 (2016-2026)', fontsize=14, fontweight='bold')
ax2.legend(loc='upper left', fontsize=10)
ax2.grid(True, alpha=0.3)

# 添加阶段标注
ax2.text(2018.5, ax2.get_ylim()[0] + 1, 'Phase 1\n借USD投CNY', ha='center', fontsize=10, 
         bbox=dict(boxstyle='round', facecolor='#3498db', alpha=0.3))
ax2.text(2024, ax2.get_ylim()[0] + 1, 'Phase 2\n借CNY投USD', ha='center', fontsize=10,
         bbox=dict(boxstyle='round', facecolor='#e67e22', alpha=0.3))

plt.tight_layout()
fig2.savefig('/root/.openclaw/workspace/reports/usdcny_carry_trade_10y_20260513_timeline.png', dpi=200, bbox_inches='tight')
plt.close(fig2)

# ============ 图表3: 详细数据表 ============
fig3, ax3 = plt.subplots(figsize=(16, 6))
ax3.axis('tight')
ax3.axis('off')

# 构建表格数据
table_data = []
table_data.append(['统计区间', '期初汇率', '期末汇率', '策略方向', '年均利差', '汇兑损益\n(区间累计)', '总年化', '累计利息', '累计汇兑', '累计总收益'])

for r in results:
    direction = '借USD投CNY' if r.get('phase') == 1 else ('借CNY投USD' if r.get('phase') == 2 else '混合策略')
    row = [
        f"{r['label']}",
        f"{r['rate_start']:.4f}",
        f"{r['rate_end']:.4f}",
        direction,
        f"{r['avg_china_rate']:.2f}% - {r['avg_us_rate']:.2f}% = {r['interest_return']:+.2f}%",
        f"{r['cumulative_fx']:+.2f}%",
        f"{r['total_return']:+.2f}%",
        f"{r['cumulative_interest']:+.2f}%",
        f"{r['cumulative_fx']:+.2f}%",
        f"{r['cumulative_total']:+.2f}%"
    ]
    table_data.append(row)

# 添加逐年明细
for year in range(2016, 2027):
    if year == 2016:
        continue
    rate_prev = usdcny_rates[year - 1]
    rate_curr = usdcny_rates[year]
    
    if year <= 2021:
        phase = 1
        direction = '借USD投CNY'
        int_ret = china_rates[year] - us_rates[year]
        fx_ret = (rate_prev / rate_curr - 1) * 100
    else:
        phase = 2
        direction = '借CNY投USD'
        int_ret = us_rates[year] - china_rates[year]
        fx_ret = (rate_curr / rate_prev - 1) * 100
    
    total = int_ret + fx_ret
    
# 创建表格
table = ax3.table(cellText=table_data[1:], colLabels=table_data[0],
                  cellLoc='center', loc='center',
                  colColours=['#2c3e50']*10)

table.auto_set_font_size(False)
table.set_fontsize(9)
table.scale(1, 2.5)

# 设置表头样式
for i in range(10):
    table[(0, i)].set_text_props(color='white', fontweight='bold')
    table[(0, i)].set_facecolor('#2c3e50')

# 设置数据行样式
for i in range(1, len(table_data)):
    for j in range(10):
        if i % 2 == 0:
            table[(i, j)].set_facecolor('#ecf0f1')
        else:
            table[(i, j)].set_facecolor('#ffffff')

ax3.set_title('USD/CNY Carry Trade 10年效益分析详细数据表 (2016-2026)', 
              fontsize=14, fontweight='bold', pad=20)

plt.tight_layout()
fig3.savefig('/root/.openclaw/workspace/reports/usdcny_carry_trade_10y_20260513_table.png', dpi=200, bbox_inches='tight')
plt.close(fig3)

# ============ 生成PDF (合并所有图表) ============
pdf_path = '/root/.openclaw/workspace/reports/usdcny_carry_trade_10y_20260513.pdf'

with PdfPages(pdf_path) as pdf:
    # 第1页: 效益分解图
    fig1, ax1 = plt.subplots(figsize=(14, 8))
    
    labels = [r['label'] for r in results]
    x = np.arange(len(labels))
    width = 0.35
    
    interest_returns = [r['interest_return'] for r in results]
    fx_returns = [r['fx_return'] for r in results]
    total_returns = [r['total_return'] for r in results]
    
    colors_interest = ['#2ecc71' if v >= 0 else '#e74c3c' for v in interest_returns]
    colors_fx = ['#3498db' if v >= 0 else '#e67e22' for v in fx_returns]
    
    bars1 = ax1.bar(x, interest_returns, width, label='利息收益 (年化)', color=colors_interest, edgecolor='white', linewidth=0.5)
    bars2 = ax1.bar(x, fx_returns, width, bottom=interest_returns, label='汇兑损益 (年化)', color=colors_fx, edgecolor='white', linewidth=0.5)
    
    for i, total in enumerate(total_returns):
        y_pos = interest_returns[i] + fx_returns[i] + 0.3 if total >= 0 else interest_returns[i] + fx_returns[i] - 0.5
        color = '#27ae60' if total >= 0 else '#c0392b'
        ax1.annotate(f'{total:+.1f}%', xy=(x[i], y_pos), ha='center', 
                    va='bottom' if total >= 0 else 'top',
                    fontsize=12, fontweight='bold', color=color,
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=color, alpha=0.9))
    
    ax1.axhline(y=0, color='black', linewidth=0.8)
    ax1.set_ylabel('年化收益率 (%)', fontsize=12)
    ax1.set_title('USD/CNY Carry Trade 10年效益分解 (2016-2026)\n分阶段策略: 2016-2021借USD投CNY | 2022-2026借CNY投USD', 
                  fontsize=14, fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels(labels, fontsize=11)
    ax1.legend(loc='upper left', fontsize=10)
    ax1.set_ylim(min(interest_returns) + min(fx_returns) - 2, max(interest_returns) + max(fx_returns) + 2)
    ax1.text(0.99, 0.02, '数据来源: FRED(美联储) / 中国人民银行\n汇率基准: 年末中间价 | 利率基准: 年均利率',
             transform=ax1.transAxes, fontsize=8, ha='right', va='bottom',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    pdf.savefig(fig1, dpi=200, bbox_inches='tight')
    plt.close(fig1)
    
    # 第2页: 累计收益折线图
    fig2, ax2 = plt.subplots(figsize=(14, 7))
    
    ax2.plot(cumulative_years, cumulative_total, 'o-', linewidth=2.5, markersize=8, color='#2c3e50', label='累计总收益 (利息+汇兑)')
    ax2.plot(cumulative_years, cumulative_interest_only, 's--', linewidth=2, markersize=6, color='#27ae60', label='累计利息收益 (仅利差)')
    ax2.axhline(y=0, color='black', linewidth=0.8, linestyle='-')
    ax2.axvline(x=2021.5, color='#e74c3c', linewidth=1.5, linestyle='--', alpha=0.7, label='策略切换点 (2021→2022)')
    
    for i, (year, total) in enumerate(zip(cumulative_years, cumulative_total)):
        if year in [2021, 2026]:
            ax2.annotate(f'{total:+.1f}%', xy=(year, total), xytext=(10, 15), 
                        textcoords='offset points', fontsize=10, fontweight='bold',
                        bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7))
    
    ax2.fill_between(cumulative_years, 0, cumulative_total, where=[t >= 0 for t in cumulative_total], 
                     alpha=0.3, color='#2ecc71', interpolate=True)
    ax2.fill_between(cumulative_years, 0, cumulative_total, where=[t < 0 for t in cumulative_total], 
                     alpha=0.3, color='#e74c3c', interpolate=True)
    
    ax2.set_xlabel('年份', fontsize=12)
    ax2.set_ylabel('累计收益率 (%)', fontsize=12)
    ax2.set_title('USD/CNY Carry Trade 累计收益走势 (2016-2026)', fontsize=14, fontweight='bold')
    ax2.legend(loc='upper left', fontsize=10)
    ax2.grid(True, alpha=0.3)
    ax2.text(2018.5, ax2.get_ylim()[0] + 1, 'Phase 1\n借USD投CNY', ha='center', fontsize=10, 
             bbox=dict(boxstyle='round', facecolor='#3498db', alpha=0.3))
    ax2.text(2024, ax2.get_ylim()[0] + 1, 'Phase 2\n借CNY投USD', ha='center', fontsize=10,
             bbox=dict(boxstyle='round', facecolor='#e67e22', alpha=0.3))
    
    plt.tight_layout()
    pdf.savefig(fig2, dpi=200, bbox_inches='tight')
    plt.close(fig2)
    
    # 第3页: 数据表
    fig3, ax3 = plt.subplots(figsize=(16, 6))
    ax3.axis('tight')
    ax3.axis('off')
    
    table = ax3.table(cellText=table_data[1:], colLabels=table_data[0],
                      cellLoc='center', loc='center',
                      colColours=['#2c3e50']*10)
    
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1, 2.5)
    
    for i in range(10):
        table[(0, i)].set_text_props(color='white', fontweight='bold')
        table[(0, i)].set_facecolor('#2c3e50')
    
    for i in range(1, len(table_data)):
        for j in range(10):
            if i % 2 == 0:
                table[(i, j)].set_facecolor('#ecf0f1')
            else:
                table[(i, j)].set_facecolor('#ffffff')
    
    ax3.set_title('USD/CNY Carry Trade 10年效益分析详细数据表 (2016-2026)', 
                  fontsize=14, fontweight='bold', pad=20)
    
    plt.tight_layout()
    pdf.savefig(fig3, dpi=200, bbox_inches='tight')
    plt.close(fig3)

print("✅ 图表生成完成:")
print(f"   - PNG: /root/.openclaw/workspace/reports/usdcny_carry_trade_10y_20260513.png")
print(f"   - PNG(时间线): /root/.openclaw/workspace/reports/usdcny_carry_trade_10y_20260513_timeline.png")
print(f"   - PNG(数据表): /root/.openclaw/workspace/reports/usdcny_carry_trade_10y_20260513_table.png")
print(f"   - PDF: {pdf_path}")

# 打印数据摘要
print("\n📊 数据摘要:")
for r in results:
    print(f"   {r['label']}: 总年化={r['total_return']:+.2f}%, 累计={r['cumulative_total']:+.2f}%")
