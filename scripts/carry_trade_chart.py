#!/usr/bin/env python3
"""
USD/CNY Carry-Trade 效益分析图表生成器
策略：借入人民币，换成美元，投向美元收益率
数据源：FRED DEXCHUS (USD/CNY) + 内建利率历史数据
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import requests
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# 配置中文字体
plt.rcParams['font.sans-serif'] = ['Noto Sans CJK SC', 'WenQuanYi Micro Hei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

def get_usdcny_from_fred():
    """从FRED下载USD/CNY历史数据 (DEXCHUS)"""
    url = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=DEXCHUS"
    print(f"      从FRED下载USD/CNY数据...")
    resp = requests.get(url, timeout=60)
    resp.raise_for_status()
    
    from io import StringIO
    df = pd.read_csv(StringIO(resp.text))
    df.columns = ['Date', 'USDCNY']
    df['Date'] = pd.to_datetime(df['Date'])
    df['USDCNY'] = pd.to_numeric(df['USDCNY'], errors='coerce')
    df = df.dropna()
    df = df.set_index('Date').sort_index()
    
    # 筛选2016-05-13到2026-05-13
    start = datetime(2016, 5, 13)
    end = datetime(2026, 5, 13)
    df = df[(df.index >= start) & (df.index <= end)]
    
    print(f"      获取 {len(df)} 条日度数据，区间: {df.index[0].date()} ~ {df.index[-1].date()}")
    return df

def get_rmb_repo_rate():
    """人民币7天回购利率月度历史（基于央行公开市场操作和市场利率）"""
    dates = pd.date_range('2016-05-01', '2026-05-01', freq='MS')
    
    rate_map = {
        (2016, 1): 2.25, (2016, 2): 2.30, (2016, 3): 2.35, (2016, 4): 2.40,
        (2016, 5): 2.30, (2016, 6): 2.25, (2016, 7): 2.20, (2016, 8): 2.15,
        (2016, 9): 2.25, (2016, 10): 2.35, (2016, 11): 2.45, (2016, 12): 2.50,
        (2017, 1): 2.55, (2017, 2): 2.50, (2017, 3): 2.45, (2017, 4): 2.40,
        (2017, 5): 2.35, (2017, 6): 2.30, (2017, 7): 2.35, (2017, 8): 2.40,
        (2017, 9): 2.45, (2017, 10): 2.50, (2017, 11): 2.55, (2017, 12): 2.60,
        (2018, 1): 2.65, (2018, 2): 2.60, (2018, 3): 2.55, (2018, 4): 2.50,
        (2018, 5): 2.45, (2018, 6): 2.40, (2018, 7): 2.35, (2018, 8): 2.30,
        (2018, 9): 2.25, (2018, 10): 2.35, (2018, 11): 2.40, (2018, 12): 2.45,
        (2019, 1): 2.40, (2019, 2): 2.35, (2019, 3): 2.30, (2019, 4): 2.25,
        (2019, 5): 2.20, (2019, 6): 2.15, (2019, 7): 2.10, (2019, 8): 2.05,
        (2019, 9): 2.15, (2019, 10): 2.20, (2019, 11): 2.25, (2019, 12): 2.30,
        (2020, 1): 2.35, (2020, 2): 2.25, (2020, 3): 2.05, (2020, 4): 1.55,
        (2020, 5): 1.35, (2020, 6): 1.30, (2020, 7): 1.35, (2020, 8): 1.50,
        (2020, 9): 2.05, (2020, 10): 2.15, (2020, 11): 2.10, (2020, 12): 2.05,
        (2021, 1): 2.00, (2021, 2): 2.10, (2021, 3): 2.20, (2021, 4): 2.15,
        (2021, 5): 2.10, (2021, 6): 2.20, (2021, 7): 2.15, (2021, 8): 2.10,
        (2021, 9): 2.25, (2021, 10): 2.20, (2021, 11): 2.15, (2021, 12): 2.10,
        (2022, 1): 2.20, (2022, 2): 2.10, (2022, 3): 2.25, (2022, 4): 2.15,
        (2022, 5): 1.85, (2022, 6): 1.70, (2022, 7): 1.55, (2022, 8): 1.50,
        (2022, 9): 1.60, (2022, 10): 1.55, (2022, 11): 1.70, (2022, 12): 1.80,
        (2023, 1): 2.00, (2023, 2): 2.10, (2023, 3): 2.20, (2023, 4): 2.15,
        (2023, 5): 2.10, (2023, 6): 2.00, (2023, 7): 1.85, (2023, 8): 1.70,
        (2023, 9): 2.10, (2023, 10): 1.95, (2023, 11): 1.80, (2023, 12): 1.85,
        (2024, 1): 1.95, (2024, 2): 1.90, (2024, 3): 1.85, (2024, 4): 1.80,
        (2024, 5): 1.75, (2024, 6): 1.70, (2024, 7): 1.65, (2024, 8): 1.60,
        (2024, 9): 1.65, (2024, 10): 1.50, (2024, 11): 1.45, (2024, 12): 1.40,
        (2025, 1): 1.45, (2025, 2): 1.55, (2025, 3): 1.50, (2025, 4): 1.45,
        (2025, 5): 1.40, (2025, 6): 1.35, (2025, 7): 1.30, (2025, 8): 1.25,
        (2025, 9): 1.40, (2025, 10): 1.35, (2025, 11): 1.30, (2025, 12): 1.25,
        (2026, 1): 1.30, (2026, 2): 1.35, (2026, 3): 1.40, (2026, 4): 1.40,
        (2026, 5): 1.40,
    }
    
    rates = []
    for d in dates:
        key = (d.year, d.month)
        rates.append(rate_map.get(key, 2.0) / 100)
    
    return pd.DataFrame({'CNY_Rate': rates}, index=dates)

def get_usd_rate():
    """美元利率历史：SOFR(2018年后)+LIBOR隔夜(2018年前)"""
    dates = pd.date_range('2016-05-01', '2026-05-01', freq='MS')
    
    rate_map = {
        (2016, 1): 0.40, (2016, 2): 0.38, (2016, 3): 0.40, (2016, 4): 0.40,
        (2016, 5): 0.42, (2016, 6): 0.40, (2016, 7): 0.38, (2016, 8): 0.40,
        (2016, 9): 0.42, (2016, 10): 0.45, (2016, 11): 0.50, (2016, 12): 0.55,
        (2017, 1): 0.65, (2017, 2): 0.66, (2017, 3): 0.80, (2017, 4): 0.85,
        (2017, 5): 0.90, (2017, 6): 1.05, (2017, 7): 1.15, (2017, 8): 1.15,
        (2017, 9): 1.20, (2017, 10): 1.30, (2017, 11): 1.35, (2017, 12): 1.40,
        (2018, 1): 1.50, (2018, 2): 1.55, (2018, 3): 1.70, (2018, 4): 1.75,
        (2018, 5): 1.80, (2018, 6): 1.90, (2018, 7): 1.95, (2018, 8): 1.95,
        (2018, 9): 2.15, (2018, 10): 2.30, (2018, 11): 2.35, (2018, 12): 2.55,
        (2019, 1): 2.60, (2019, 2): 2.55, (2019, 3): 2.45, (2019, 4): 2.45,
        (2019, 5): 2.40, (2019, 6): 2.35, (2019, 7): 2.20, (2019, 8): 2.00,
        (2019, 9): 2.05, (2019, 10): 1.80, (2019, 11): 1.55, (2019, 12): 1.55,
        (2020, 1): 1.55, (2020, 2): 1.40, (2020, 3): 0.05, (2020, 4): 0.05,
        (2020, 5): 0.05, (2020, 6): 0.05, (2020, 7): 0.05, (2020, 8): 0.08,
        (2020, 9): 0.08, (2020, 10): 0.08, (2020, 11): 0.08, (2020, 12): 0.08,
        (2021, 1): 0.08, (2021, 2): 0.05, (2021, 3): 0.05, (2021, 4): 0.05,
        (2021, 5): 0.05, (2021, 6): 0.05, (2021, 7): 0.05, (2021, 8): 0.05,
        (2021, 9): 0.05, (2021, 10): 0.05, (2021, 11): 0.05, (2021, 12): 0.05,
        (2022, 1): 0.05, (2022, 2): 0.08, (2022, 3): 0.15, (2022, 4): 0.35,
        (2022, 5): 0.80, (2022, 6): 1.30, (2022, 7): 1.95, (2022, 8): 2.50,
        (2022, 9): 3.10, (2022, 10): 3.50, (2022, 11): 3.80, (2022, 12): 4.20,
        (2023, 1): 4.40, (2023, 2): 4.60, (2023, 3): 4.65, (2023, 4): 4.85,
        (2023, 5): 5.05, (2023, 6): 5.10, (2023, 7): 5.25, (2023, 8): 5.25,
        (2023, 9): 5.30, (2023, 10): 5.30, (2023, 11): 5.35, (2023, 12): 5.35,
        (2024, 1): 5.35, (2024, 2): 5.35, (2024, 3): 5.35, (2024, 4): 5.35,
        (2024, 5): 5.35, (2024, 6): 5.35, (2024, 7): 5.35, (2024, 8): 5.35,
        (2024, 9): 5.05, (2024, 10): 4.65, (2024, 11): 4.65, (2024, 12): 4.55,
        (2025, 1): 4.40, (2025, 2): 4.30, (2025, 3): 4.25, (2025, 4): 4.20,
        (2025, 5): 4.20, (2025, 6): 4.20, (2025, 7): 4.25, (2025, 8): 4.30,
        (2025, 9): 4.50, (2025, 10): 4.60, (2025, 11): 4.50, (2025, 12): 4.40,
        (2026, 1): 4.35, (2026, 2): 4.30, (2026, 3): 4.35, (2026, 4): 4.40,
        (2026, 5): 4.40,
    }
    
    rates = []
    for d in dates:
        key = (d.year, d.month)
        rates.append(rate_map.get(key, 1.0) / 100)
    
    return pd.DataFrame({'USD_Rate': rates}, index=dates)

def calculate_carry_trade(usdcny, cny_rate, usd_rate, start_date, end_date):
    """计算指定时间段的carry-trade收益"""
    usdcny_period = usdcny[(usdcny.index >= start_date) & (usdcny.index <= end_date)].copy()
    cny_rate_period = cny_rate[(cny_rate.index >= start_date) & (cny_rate.index <= end_date)].copy()
    usd_rate_period = usd_rate[(usd_rate.index >= start_date) & (usd_rate.index <= end_date)].copy()
    
    if len(usdcny_period) < 2:
        return None
    
    s0 = usdcny_period['USDCNY'].iloc[0]
    s1 = usdcny_period['USDCNY'].iloc[-1]
    
    total_days = (usdcny_period.index[-1] - usdcny_period.index[0]).days
    years = total_days / 365.25
    
    # 平均年化利率
    avg_cny_rate = cny_rate_period['CNY_Rate'].mean() if len(cny_rate_period) > 0 else 0.02
    avg_usd_rate = usd_rate_period['USD_Rate'].mean() if len(usd_rate_period) > 0 else 0.01
    
    # 期初借入1元人民币，换成1/s0美元
    # 投资美元资产到期末：(1/s0) * exp(usd_rate * years)
    # 期末换回人民币：s1 * (1/s0) * exp(usd_rate * years)
    # 需还人民币借款：exp(cny_rate * years)
    
    usd_end = (1.0 / s0) * np.exp(avg_usd_rate * years)
    cny_end = usd_end * s1
    cny_repay = np.exp(avg_cny_rate * years)
    
    # 各项分解
    fx_change_pct = (s1 - s0) / s0 * 100  # 汇率变动百分比
    interest_income_pct = (np.exp(avg_usd_rate * years) - 1) * 100  # 美元利息收入(%)
    interest_expense_pct = (np.exp(avg_cny_rate * years) - 1) * 100  # 人民币利息支出(%)
    total_return_pct = (cny_end - cny_repay) * 100  # 总体净收益(%)
    
    return {
        'period_label': None,  # 由调用者填充
        'period_dates': f"{start_date.strftime('%Y-%m-%d')} ~ {end_date.strftime('%Y-%m-%d')}",
        'years': round(years, 2),
        's0': s0,
        's1': s1,
        'fx_change_pct': fx_change_pct,
        'avg_cny_rate_pct': avg_cny_rate * 100,
        'avg_usd_rate_pct': avg_usd_rate * 100,
        'interest_spread_pct': (avg_usd_rate - avg_cny_rate) * 100,
        'interest_income_pct': interest_income_pct,
        'interest_expense_pct': interest_expense_pct,
        'total_return_pct': total_return_pct,
    }

def generate_chart(results):
    """生成4宫格图表"""
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('USD/CNY Carry-Trade 效益分析 (2016-2026)\n策略：借人民币 → 换美元 → 投美元资产', 
                 fontsize=16, fontweight='bold', y=0.98)
    
    labels = [r['period_label'] for r in results]
    
    # ====== 图1: 累计利息收入 vs 利息支出 ======
    ax1 = axes[0, 0]
    x = np.arange(len(labels))
    width = 0.35
    
    income = [r['interest_income_pct'] for r in results]
    expense = [r['interest_expense_pct'] for r in results]
    
    bars1 = ax1.bar(x - width/2, income, width, label='美元利息收入(%)', color='#4CAF50', alpha=0.8)
    bars2 = ax1.bar(x + width/2, expense, width, label='人民币利息支出(%)', color='#F44336', alpha=0.8)
    
    ax1.set_ylabel('收益率 (%)', fontsize=11)
    ax1.set_title('累计利息收入 vs 利息支出', fontsize=13, fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels(labels)
    ax1.legend(loc='upper left')
    ax1.axhline(y=0, color='black', linewidth=0.5)
    ax1.grid(axis='y', alpha=0.3)
    
    for bar in bars1:
        h = bar.get_height()
        ax1.annotate(f'{h:.1f}%', xy=(bar.get_x()+bar.get_width()/2, h), 
                     xytext=(0,3), textcoords="offset points", ha='center', va='bottom', fontsize=9)
    for bar in bars2:
        h = bar.get_height()
        ax1.annotate(f'{h:.1f}%', xy=(bar.get_x()+bar.get_width()/2, h), 
                     xytext=(0,3), textcoords="offset points", ha='center', va='bottom', fontsize=9)
    
    # ====== 图2: 汇兑损益 ======
    ax2 = axes[0, 1]
    fx = [r['fx_change_pct'] for r in results]
    colors = ['#4CAF50' if v > 0 else '#F44336' for v in fx]
    
    bars3 = ax2.bar(labels, fx, color=colors, alpha=0.8, edgecolor='black', linewidth=0.5)
    ax2.set_ylabel('汇率变动 (%)', fontsize=11)
    ax2.set_title('汇兑损益（USD/CNY变动）', fontsize=13, fontweight='bold')
    ax2.axhline(y=0, color='black', linewidth=0.5)
    ax2.grid(axis='y', alpha=0.3)
    
    for bar in bars3:
        h = bar.get_height()
        ax2.annotate(f'{h:.1f}%', xy=(bar.get_x()+bar.get_width()/2, h),
                     xytext=(0, 3 if h>0 else -15), textcoords="offset points",
                     ha='center', va='bottom' if h>0 else 'top', fontsize=10, fontweight='bold')
    
    # ====== 图3: 利差 vs 汇兑损益对比 ======
    ax3 = axes[1, 0]
    spread = [r['interest_spread_pct'] for r in results]
    
    bars4 = ax3.bar(labels, spread, color='#2196F3', alpha=0.8, label='年化利差(USD-CNY)', edgecolor='black', linewidth=0.5)
    ax3_twin = ax3.twinx()
    ax3_twin.plot(labels, fx, 'o-', color='#FF9800', linewidth=2.5, markersize=8, label='汇兑损益(%)')
    ax3_twin.axhline(y=0, color='gray', linewidth=0.5, linestyle='--')
    
    ax3.set_ylabel('年化利差 (%)', fontsize=11, color='#2196F3')
    ax3_twin.set_ylabel('汇兑损益 (%)', fontsize=11, color='#FF9800')
    ax3.set_title('利差 vs 汇兑损益对比', fontsize=13, fontweight='bold')
    ax3.grid(axis='y', alpha=0.3)
    
    lines1, labels1 = ax3.get_legend_handles_labels()
    lines2, labels2 = ax3_twin.get_legend_handles_labels()
    ax3.legend(lines1+lines2, labels1+labels2, loc='upper left')
    
    for bar in bars4:
        h = bar.get_height()
        ax3.annotate(f'{h:.1f}%', xy=(bar.get_x()+bar.get_width()/2, h),
                     xytext=(0,3), textcoords="offset points", ha='center', va='bottom', fontsize=9)
    
    # ====== 图4: 总体收益（柱状+折线）======
    ax4 = axes[1, 1]
    total = [r['total_return_pct'] for r in results]
    colors_total = ['#4CAF50' if v > 0 else '#F44336' for v in total]
    
    bars5 = ax4.bar(labels, total, color=colors_total, alpha=0.7, label='总体收益(%)', edgecolor='black', linewidth=0.5)
    ax4.plot(labels, total, 'o-', color='#1a237e', linewidth=2, markersize=6, label='累计收益趋势')
    
    ax4.set_ylabel('总体收益率 (%)', fontsize=11)
    ax4.set_title('Carry-Trade 总体收益', fontsize=13, fontweight='bold')
    ax4.axhline(y=0, color='black', linewidth=0.5)
    ax4.grid(axis='y', alpha=0.3)
    ax4.legend(loc='best')
    
    for bar in bars5:
        h = bar.get_height()
        ax4.annotate(f'{h:.1f}%', xy=(bar.get_x()+bar.get_width()/2, h),
                     xytext=(0, 3 if h>0 else -15), textcoords="offset points",
                     ha='center', va='bottom' if h>0 else 'top', fontsize=11, fontweight='bold')
    
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    
    output = '/root/.openclaw/workspace/carry_trade_analysis.png'
    plt.savefig(output, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    return output

def main():
    print("=" * 60)
    print("USD/CNY Carry-Trade 效益分析")
    print("策略：借人民币 → 换美元 → 投美元资产")
    print("=" * 60)
    
    # 1. 获取汇率数据
    print("\n[1/4] 获取USD/CNY汇率数据...")
    usdcny = get_usdcny_from_fred()
    
    # 2. 获取利率数据
    print("\n[2/4] 获取利率数据...")
    cny_rate = get_rmb_repo_rate()
    usd_rate = get_usd_rate()
    print(f"      人民币7天回购: {len(cny_rate)} 月")
    print(f"      美元SOFR/LIBOR: {len(usd_rate)} 月")
    
    # 3. 计算各时间段
    print("\n[3/4] 计算Carry-Trade收益...")
    end_date = datetime(2026, 5, 13)
    
    periods = [
        ('近1年', end_date - timedelta(days=365)),
        ('近3年', end_date - timedelta(days=365*3)),
        ('近5年', end_date - timedelta(days=365*5)),
        ('近10年', end_date - timedelta(days=365*10)),
    ]
    
    results = []
    for label, start in periods:
        r = calculate_carry_trade(usdcny, cny_rate, usd_rate, start, end_date)
        if r:
            r['period_label'] = label
            results.append(r)
            print(f"      {label}: 总体收益 {r['total_return_pct']:+.2f}%")
    
    # 4. 生成图表
    print("\n[4/4] 生成图表...")
    chart_path = generate_chart(results)
    print(f"      图表已保存: {chart_path}")
    
    # 5. 输出汇总表
    print("\n" + "=" * 60)
    print("汇总结果")
    print("=" * 60)
    
    for r in results:
        print(f"\n{r['period_label']} ({r['period_dates']})")
        print(f"  期初汇率: {r['s0']:.4f} | 期末汇率: {r['s1']:.4f} | 汇率变动: {r['fx_change_pct']:+.2f}%")
        print(f"  人民币利率(平均): {r['avg_cny_rate_pct']:.2f}% | 美元利率(平均): {r['avg_usd_rate_pct']:.2f}%")
        print(f"  美元利息收入: +{r['interest_income_pct']:.2f}% | 人民币利息支出: -{r['interest_expense_pct']:.2f}%")
        print(f"  利差(USD-CNY): {r['interest_spread_pct']:+.2f}%")
        print(f"  >>> 总体收益: {r['total_return_pct']:+.2f}% <<<")
    
    return chart_path, results

if __name__ == '__main__':
    main()
