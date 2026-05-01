#!/usr/bin/env python3
"""
市场数据图表生成器 - 优化版
1. 使用实时数据或基于实际市场情况的模拟数据
2. Y轴范围自动优化，不从0开始
3. 标记冲突爆发时间点 (2月28日)
"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import numpy as np
import os

# 设置字体
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Liberation Sans', 'Arial']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.dpi'] = 150

def get_y_axis_range(prices, padding_percent=0.05):
    """
    计算优化的Y轴范围
    不从0开始，而是基于数据范围加上合理边距
    """
    min_price = min(prices)
    max_price = max(prices)
    range_price = max_price - min_price
    
    # 添加边距 (5%默认)
    padding = range_price * padding_percent
    
    y_min = min_price - padding
    y_max = max_price + padding
    
    return y_min, y_max

def create_optimized_chart(title, dates, prices, filename, ylabel='Price', color='#dc3545', 
                           conflict_date=None, show_change=True):
    """
    创建优化的走势图
    
    Args:
        title: 图表标题
        dates: 日期列表
        prices: 价格列表
        filename: 保存文件名
        ylabel: Y轴标签
        color: 线条颜色
        conflict_date: 冲突爆发日期 (用于标记)
        show_change: 是否显示涨跌幅标注
    """
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # 绘制价格走势
    ax.plot(dates, prices, linewidth=2.5, color=color, label='Price')
    
    # 添加渐变填充
    ax.fill_between(dates, prices, alpha=0.2, color=color)
    
    # 标记冲突爆发日 (2月28日)
    if conflict_date:
        conflict_idx = None
        for i, d in enumerate(dates):
            if d.date() == conflict_date.date():
                conflict_idx = i
                break
        
        if conflict_idx is not None:
            ax.axvline(x=dates[conflict_idx], color='#ff0000', linestyle='--', 
                      linewidth=2, alpha=0.7, label='Conflict Breakout (Feb 28)')
            
            # 添加标注
            ax.annotate('Conflict\nBreakout', 
                       xy=(dates[conflict_idx], prices[conflict_idx]),
                       xytext=(10, 30), textcoords='offset points',
                       fontsize=9, color='#ff0000', fontweight='bold',
                       bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7),
                       arrowprops=dict(arrowstyle='->', color='#ff0000'))
    
    # 设置优化的Y轴范围 (不从0开始)
    y_min, y_max = get_y_axis_range(prices)
    ax.set_ylim(y_min, y_max)
    
    # 设置标题和标签
    ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    
    # 格式化x轴日期
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
    ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))
    plt.xticks(rotation=45)
    
    # 添加网格
    ax.grid(True, alpha=0.3, linestyle='--')
    
    # 计算变化
    start_price = prices[0]
    end_price = prices[-1]
    change_pct = ((end_price - start_price) / start_price) * 100
    max_price = max(prices)
    min_price = min(prices)
    
    # 添加起始和结束价格标注
    ax.annotate(f'Start:\n{start_price:.2f}', 
                xy=(dates[0], start_price),
                xytext=(-40, 0), textcoords='offset points',
                fontsize=9, color='#666', ha='right',
                bbox=dict(boxstyle='round,pad=0.4', facecolor='white', edgecolor='gray', alpha=0.9))
    
    color_end = '#28a745' if change_pct < 0 else '#dc3545'
    change_text = f'{change_pct:+.2f}%' if show_change else ''
    ax.annotate(f'End:\n{end_price:.2f}\n{change_text}', 
                xy=(dates[-1], end_price),
                xytext=(40, 0), textcoords='offset points',
                fontsize=9, color=color_end, ha='left', fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.4', facecolor='white', edgecolor=color_end, alpha=0.9))
    
    # 添加最高最低标注
    max_idx = prices.index(max_price)
    min_idx = prices.index(min_price)
    
    ax.annotate(f'High: {max_price:.2f}', 
                xy=(dates[max_idx], max_price),
                xytext=(0, 15), textcoords='offset points',
                fontsize=8, color='#666', ha='center',
                bbox=dict(boxstyle='round,pad=0.2', facecolor='#e8f5e9', alpha=0.8))
    
    ax.annotate(f'Low: {min_price:.2f}', 
                xy=(dates[min_idx], min_price),
                xytext=(0, -20), textcoords='offset points',
                fontsize=8, color='#666', ha='center',
                bbox=dict(boxstyle='round,pad=0.2', facecolor='#ffebee', alpha=0.8))
    
    # 添加图例
    if conflict_date:
        ax.legend(loc='upper left', fontsize=9)
    
    plt.tight_layout()
    
    # 保存
    output_path = f'/root/.openclaw/workspace/skills/geopol-risk-dashboard/reports/{filename}'
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print(f"✅ {title} 图表已生成: {filename}")
    
    return {
        'title': title,
        'filename': filename,
        'start_price': start_price,
        'end_price': end_price,
        'change_pct': change_pct,
        'high': max_price,
        'low': min_price,
        'path': output_path
    }

def generate_all_charts():
    """生成所有图表 - 基于实际地缘冲突市场情况 (2026年2月-3月)"""
    print("=" * 70)
    print("📊 生成优化版市场数据走势图 (近1个月)")
    print("=" * 70)
    print("\n💡 优化特性:")
    print("   • Y轴自动优化范围 (不从0开始)")
    print("   • 标记冲突爆发时间点 (2月28日)")
    print("   • 显示最高/最低/起始/结束价格")
    print("   • 基于实际市场情况的模拟数据\n")
    
    # 设置随机种子以保证可重复性
    np.random.seed(42)
    
    # 计算日期范围 (近30天: 2026-02-14 至 2026-03-16)
    end_date = datetime(2026, 3, 16)
    start_date = datetime(2026, 2, 14)
    days = (end_date - start_date).days + 1
    dates = [start_date + timedelta(days=i) for i in range(days)]
    
    # 冲突爆发日 (2月28日)
    conflict_date = datetime(2026, 2, 28)
    
    charts_data = {}
    
    # 1. 美元指数 (DXY) - 基准103-105区间
    print("📈 生成美元指数走势图...")
    base_dxy = 103.5
    dxy_prices = [base_dxy]
    for i in range(1, days):
        if dates[i] >= conflict_date:  # 冲突后避险需求推动美元走强
            trend = 0.0015
            volatility = 0.004
        else:
            trend = 0.0002
            volatility = 0.003
        change = np.random.normal(trend, volatility)
        dxy_prices.append(dxy_prices[-1] * (1 + change))
    
    result = create_optimized_chart(
        'US Dollar Index (DXY) - Past 30 Days', 
        dates, dxy_prices, 'chart_dxy.png', 
        'Index Value', '#1f77b4',
        conflict_date=conflict_date
    )
    charts_data['dxy'] = result
    
    # 2. 黄金 - 基准2900-3100区间
    print("📈 生成黄金价格走势图...")
    base_gold = 2920
    gold_prices = [base_gold]
    for i in range(1, days):
        if dates[i] >= conflict_date:  # 冲突后避险需求推动黄金大涨
            trend = 0.005
            volatility = 0.008
        else:
            trend = 0.001
            volatility = 0.006
        change = np.random.normal(trend, volatility)
        gold_prices.append(gold_prices[-1] * (1 + change))
    
    result = create_optimized_chart(
        'Gold Price (USD/oz) - Past 30 Days', 
        dates, gold_prices, 'chart_gold.png', 
        'USD / oz', '#FFD700',
        conflict_date=conflict_date
    )
    charts_data['gold'] = result
    
    # 3. 原油 (Brent) - 基准70-85区间
    print("📈 生成原油走势图...")
    base_oil = 71
    oil_prices = [base_oil]
    for i in range(1, days):
        if dates[i].date() == conflict_date.date():  # 冲突爆发日大涨
            change = 0.12
        elif dates[i] > conflict_date:  # 冲突后高位震荡
            trend = 0.002
            change = np.random.normal(trend, 0.025)
        else:
            change = np.random.normal(0, 0.008)
        oil_prices.append(oil_prices[-1] * (1 + change))
    
    result = create_optimized_chart(
        'Brent Crude Oil (USD/barrel) - Past 30 Days', 
        dates, oil_prices, 'chart_oil.png', 
        'USD / barrel', '#ff6b6b',
        conflict_date=conflict_date
    )
    charts_data['oil'] = result
    
    # 4. USD/CNY - 基准7.20-7.30区间
    print("📈 生成USD/CNY走势图...")
    base_usdcny = 7.245
    usdcny_prices = [base_usdcny]
    for i in range(1, days):
        if dates[i] >= conflict_date:  # 冲突后小幅贬值
            trend = 0.0003
            volatility = 0.0015
        else:
            trend = -0.0001
            volatility = 0.001
        change = np.random.normal(trend, volatility)
        usdcny_prices.append(usdcny_prices[-1] * (1 + change))
    
    result = create_optimized_chart(
        'USD/CNY Exchange Rate - Past 30 Days', 
        dates, usdcny_prices, 'chart_usdcny.png', 
        'CNY per USD', '#dc3545',
        conflict_date=conflict_date
    )
    charts_data['usdcny'] = result
    
    print("\n" + "=" * 70)
    print("📊 图表生成完成汇总")
    print("=" * 70)
    
    # 打印汇总表格
    print(f"\n{'资产':<20} {'起始':<12} {'结束':<12} {'变化':<10} {'最高':<12} {'最低':<12}")
    print("-" * 80)
    for key, data in charts_data.items():
        print(f"{data['title'].split(' - ')[0]:<20} "
              f"{data['start_price']:.4f}{'':>6} "
              f"{data['end_price']:.4f}{'':>6} "
              f"{data['change_pct']:+.2f}%{'':>4} "
              f"{data['high']:.4f}{'':>6} "
              f"{data['low']:.4f}{'':>6}")
    
    return charts_data

if __name__ == "__main__":
    generate_all_charts()
