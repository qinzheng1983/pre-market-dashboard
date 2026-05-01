#!/usr/bin/env python3
"""
多货币对夏普比率计算与马科维茨组合优化
货币对: USDCNH, EURCNH, CNYRUB, CNYTHB
时间范围: 过去5年
"""

import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import minimize
import time
import warnings
warnings.filterwarnings('ignore')

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

print("=" * 60)
print("多货币对夏普比率计算与马科维茨组合优化")
print("=" * 60)

# 定义货币对和对应的Yahoo Finance Ticker
tickers = {
    'USDCNH': 'CNH=X',         # 美元兑离岸人民币 (Yahoo格式)
    'EURUSD': 'EURUSD=X',      # 欧元兑美元 (用于计算EURCNH)
    'USDRUB': 'RUB=X',         # 美元兑卢布
    'USDTHB': 'THB=X',         # 美元兑泰铢
    'USDCNY': 'CNY=X',         # 美元兑在岸人民币
}

# 下载历史数据的函数 (带重试)
def download_with_retry(ticker, start, end, max_retries=3):
    for attempt in range(max_retries):
        try:
            time.sleep(1)  # 延迟1秒避免限流
            df = yf.download(ticker, start=start, end=end, progress=False)
            if len(df) > 50:
                return df
        except Exception as e:
            print(f"    重试 {attempt+1}/{max_retries}...", end=' ')
            time.sleep(2)
    return None

# 下载5年历史数据
print("\n📊 正在下载历史数据...")
print("-" * 40)

end_date = pd.Timestamp.now()
start_date = end_date - pd.DateOffset(years=5)

print(f"时间范围: {start_date.strftime('%Y-%m-%d')} 至 {end_date.strftime('%Y-%m-%d')}")

data_dict = {}
available_tickers = []

for name, ticker in tickers.items():
    try:
        print(f"  获取 {name} ({ticker})...", end=' ')
        df = download_with_retry(ticker, start_date, end_date)
        if df is not None and len(df) > 100:
            # 处理多级列索引
            if isinstance(df.columns, pd.MultiIndex):
                close_col = ('Close', ticker)
                if close_col in df.columns:
                    data_dict[name] = df[close_col].squeeze()
                else:
                    data_dict[name] = df['Close'].squeeze()
            else:
                data_dict[name] = df['Close'].squeeze()
            available_tickers.append(name)
            print(f"✓ ({len(df)} 条数据)")
        else:
            print(f"✗ 数据不足")
    except Exception as e:
        print(f"✗ 失败: {str(e)[:50]}")

print(f"\n✅ 成功获取 {len(available_tickers)} 个基础汇率")

# 计算派生汇率
print("\n📊 计算目标货币对...")

# USDCNH (直接使用或从USDCNY估算)
if 'USDCNH' in available_tickers:
    print("  ✓ USDCNH 已获取")
elif 'USDCNY' in available_tickers:
    print("  使用 USDCNY 作为 USDCNH 近似")
    data_dict['USDCNH'] = data_dict['USDCNY']
    available_tickers.append('USDCNH')

# EURCNH = EURUSD * USDCNH (1 EUR = X USD = X * USDCNH CNY)
if 'EURUSD' in available_tickers and 'USDCNH' in available_tickers:
    print("  计算 EURCNH = EURUSD × USDCNH...")
    eurusd = data_dict['EURUSD']
    usdcnh = data_dict['USDCNH']
    common_dates = eurusd.index.intersection(usdcnh.index)
    if len(common_dates) > 100:
        eurcnh = eurusd.loc[common_dates] * usdcnh.loc[common_dates]
        data_dict['EURCNH'] = eurcnh
        available_tickers.append('EURCNH')
        print(f"    ✓ EURCNH 已计算 ({len(eurcnh)} 条)")

# CNYRUB = USDRUB / USDCNH (1 CNY = X RUB)
if 'USDRUB' in available_tickers and 'USDCNH' in available_tickers:
    print("  计算 CNYRUB = USDRUB / USDCNH...")
    usdrub = data_dict['USDRUB']
    usdcnh = data_dict['USDCNH']
    common_dates = usdrub.index.intersection(usdcnh.index)
    if len(common_dates) > 100:
        cnyrub = usdrub.loc[common_dates] / usdcnh.loc[common_dates]
        data_dict['CNYRUB'] = cnyrub
        available_tickers.append('CNYRUB')
        print(f"    ✓ CNYRUB 已计算 ({len(cnyrub)} 条)")

# CNYTHB = USDTHB / USDCNH (1 CNY = X THB)
if 'USDTHB' in available_tickers and 'USDCNH' in available_tickers:
    print("  计算 CNYTHB = USDTHB / USDCNH...")
    usdthb = data_dict['USDTHB']
    usdcnh = data_dict['USDCNH']
    common_dates = usdthb.index.intersection(usdcnh.index)
    if len(common_dates) > 100:
        cnythb = usdthb.loc[common_dates] / usdcnh.loc[common_dates]
        data_dict['CNYTHB'] = cnythb
        available_tickers.append('CNYTHB')
        print(f"    ✓ CNYTHB 已计算 ({len(cnythb)} 条)")

# 目标货币对
target_pairs = ['USDCNH', 'EURCNH', 'CNYRUB', 'CNYTHB']
available_target_pairs = [p for p in target_pairs if p in available_tickers]

print(f"\n📈 可用于分析的货币对: {available_target_pairs}")

if len(available_target_pairs) < 2:
    print("\n❌ 可用货币对不足，无法进行分析")
    print("\n尝试使用备用方案 - 生成合成历史数据用于演示...")
    
    # 生成合成数据用于演示
    np.random.seed(42)
    dates = pd.date_range(start=start_date, end=end_date, freq='B')
    
    # 基于真实统计特征生成合成数据
    # USD/CNH: 均值约7.0, 年波动约3%
    usdcnh_base = 7.0
    usdcnh_returns = np.random.normal(0.00002, 0.004, len(dates))
    usdcnh_prices = usdcnh_base * np.exp(np.cumsum(usdcnh_returns))
    data_dict['USDCNH'] = pd.Series(usdcnh_prices, index=dates)
    
    # EUR/CNH: 均值约7.8, 年波动约8%
    eurcnh_base = 7.8
    eurcnh_returns = np.random.normal(0.00001, 0.005, len(dates))
    eurcnh_prices = eurcnh_base * np.exp(np.cumsum(eurcnh_returns))
    data_dict['EURCNH'] = pd.Series(eurcnh_prices, index=dates)
    
    # CNY/RUB: 均值约13, 年波动约15% (高波动)
    cnyrub_base = 13.0
    cnyrub_returns = np.random.normal(0.00005, 0.01, len(dates))
    cnyrub_prices = cnyrub_base * np.exp(np.cumsum(cnyrub_returns))
    data_dict['CNYRUB'] = pd.Series(cnyrub_prices, index=dates)
    
    # CNY/THB: 均值约4.8, 年波动约5%
    cnythb_base = 4.8
    cnythb_returns = np.random.normal(0.00001, 0.003, len(dates))
    cnythb_prices = cnythb_base * np.exp(np.cumsum(cnythb_returns))
    data_dict['CNYTHB'] = pd.Series(cnythb_prices, index=dates)
    
    available_target_pairs = ['USDCNH', 'EURCNH', 'CNYRUB', 'CNYTHB']
    print(f"✅ 已生成合成数据用于演示分析")
    print(f"⚠️  注意: 以下结果基于合成数据，仅用于展示计算方法")

# 创建统一的数据框
print("\n📊 构建收益率矩阵...")
print("-" * 40)

# 对齐所有数据
all_dates = None
for pair in available_target_pairs:
    if all_dates is None:
        all_dates = data_dict[pair].index
    else:
        all_dates = all_dates.intersection(data_dict[pair].index)

print(f"共同交易日: {len(all_dates)} 天")

# 构建价格矩阵
price_df = pd.DataFrame(index=all_dates)
for pair in available_target_pairs:
    price_df[pair] = data_dict[pair].loc[all_dates]

# 删除任何缺失值
price_df = price_df.dropna()

# 计算日收益率 (对数收益率)
returns_df = np.log(price_df / price_df.shift(1)).dropna()

print(f"收益率样本数: {len(returns_df)}")

# 显示基本统计
print(f"\n各货币对基本统计:")
print("-" * 40)
for pair in available_target_pairs:
    start_price = price_df[pair].iloc[0]
    end_price = price_df[pair].iloc[-1]
    total_return = (end_price / start_price - 1) * 100
    print(f"{pair:10}: 起始={start_price:.4f}, 结束={end_price:.4f}, 总收益={total_return:+.2f}%")

# 计算年化收益率和波动率
trading_days_per_year = 252

annual_returns = returns_df.mean() * trading_days_per_year
annual_volatility = returns_df.std() * np.sqrt(trading_days_per_year)

# 计算夏普比率
# 假设无风险利率为 2% (中国国债收益率近似)
risk_free_rate = 0.02

sharpe_ratios = (annual_returns - risk_free_rate) / annual_volatility

print("\n" + "=" * 60)
print("📈 夏普比率计算结果")
print("=" * 60)
print(f"{'货币对':<12} {'年化收益':<12} {'年化波动':<12} {'夏普比率':<12}")
print("-" * 60)
for pair in available_target_pairs:
    ret = annual_returns[pair]
    vol = annual_volatility[pair]
    sr = sharpe_ratios[pair]
    print(f"{pair:<12} {ret:<+12.4%} {vol:<12.4%} {sr:<+12.4f}")

# 保存夏普比率结果
sharpe_results = pd.DataFrame({
    'Currency_Pair': available_target_pairs,
    'Annual_Return': [annual_returns[p] for p in available_target_pairs],
    'Annual_Volatility': [annual_volatility[p] for p in available_target_pairs],
    'Sharpe_Ratio': [sharpe_ratios[p] for p in available_target_pairs]
})

output_dir = '/root/.openclaw/workspace/fx_analysis'
import os
os.makedirs(output_dir, exist_ok=True)

sharpe_results.to_csv(f'{output_dir}/sharpe_ratios.csv', index=False)
print(f"\n✅ 夏普比率结果已保存至: {output_dir}/sharpe_ratios.csv")

# ============================================
# 马科维茨投资组合优化
# ============================================
print("\n" + "=" * 60)
print("🎯 马科维茨投资组合优化")
print("=" * 60)

# 计算协方差矩阵
cov_matrix = returns_df.cov() * trading_days_per_year

print("\n年化协方差矩阵:")
print(cov_matrix.round(6))

# 投资组合优化函数
def portfolio_performance(weights, returns, cov_matrix):
    """计算投资组合的收益、波动率和夏普比率"""
    portfolio_return = np.sum(returns * weights)
    portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
    sharpe_ratio = (portfolio_return - risk_free_rate) / portfolio_volatility if portfolio_volatility > 0 else 0
    return portfolio_return, portfolio_volatility, sharpe_ratio

def negative_sharpe(weights, returns, cov_matrix):
    """负夏普比率 (用于最小化)"""
    return -portfolio_performance(weights, returns, cov_matrix)[2]

def portfolio_volatility(weights, returns, cov_matrix):
    """投资组合波动率"""
    return portfolio_performance(weights, returns, cov_matrix)[1]

# 约束条件
n_assets = len(available_target_pairs)
constraints = {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}  # 权重和为1
bounds = tuple((0, 0.5) for _ in range(n_assets))  # 每个资产权重0-50%

# 初始猜测 (等权重)
initial_guess = np.array([1/n_assets] * n_assets)

# 1. 最优夏普比率组合 (切线组合)
optimal_sharpe = minimize(
    negative_sharpe,
    initial_guess,
    args=(annual_returns.values, cov_matrix.values),
    method='SLSQP',
    bounds=bounds,
    constraints=constraints
)

optimal_weights = optimal_sharpe.x
optimal_return, optimal_volatility, optimal_sharpe_ratio = portfolio_performance(
    optimal_weights, annual_returns.values, cov_matrix.values
)

print(f"\n🎯 最优夏普比率组合 (最大夏普比率):")
print("-" * 40)
for i, pair in enumerate(available_target_pairs):
    bar = '█' * int(optimal_weights[i] * 40)
    print(f"  {pair:10}: {optimal_weights[i]:>7.2%} {bar}")
print(f"\n  组合年化收益: {optimal_return:+.4%}")
print(f"  组合年化波动: {optimal_volatility:.4%}")
print(f"  组合夏普比率: {optimal_sharpe_ratio:.4f}")

# 2. 最小方差组合
min_variance = minimize(
    portfolio_volatility,
    initial_guess,
    args=(annual_returns.values, cov_matrix.values),
    method='SLSQP',
    bounds=bounds,
    constraints=constraints
)

min_var_weights = min_variance.x
min_var_return, min_var_volatility, min_var_sharpe = portfolio_performance(
    min_var_weights, annual_returns.values, cov_matrix.values
)

print(f"\n🛡️ 最小方差组合 (最低风险):")
print("-" * 40)
for i, pair in enumerate(available_target_pairs):
    bar = '█' * int(min_var_weights[i] * 40)
    print(f"  {pair:10}: {min_var_weights[i]:>7.2%} {bar}")
print(f"\n  组合年化收益: {min_var_return:+.4%}")
print(f"  组合年化波动: {min_var_volatility:.4%}")
print(f"  组合夏普比率: {min_var_sharpe:.4f}")

# 3. 等权重组合
equal_weights = np.array([1/n_assets] * n_assets)
eq_ret, eq_vol, eq_sharpe = portfolio_performance(
    equal_weights, annual_returns.values, cov_matrix.values
)

print(f"\n⚖️  等权重组合:")
print("-" * 40)
for i, pair in enumerate(available_target_pairs):
    print(f"  {pair:10}: {equal_weights[i]:>7.2%}")
print(f"\n  组合年化收益: {eq_ret:+.4%}")
print(f"  组合年化波动: {eq_vol:.4%}")
print(f"  组合夏普比率: {eq_sharpe:.4f}")

# ============================================
# 生成有效前沿
# ============================================
print("\n📊 生成有效前沿...")

# 生成多个目标收益水平
target_returns = np.linspace(annual_returns.min() * 0.8, annual_returns.max() * 1.2, 100)
efficient_portfolios = []

for target in target_returns:
    # 约束: 达到目标收益
    target_constraint = [
        {'type': 'eq', 'fun': lambda x: np.sum(x) - 1},
        {'type': 'eq', 'fun': lambda x: np.sum(annual_returns * x) - target}
    ]
    
    result = minimize(
        portfolio_volatility,
        initial_guess,
        args=(annual_returns.values, cov_matrix.values),
        method='SLSQP',
        bounds=bounds,
        constraints=target_constraint
    )
    
    if result.success:
        eff_return, eff_volatility, eff_sharpe = portfolio_performance(
            result.x, annual_returns.values, cov_matrix.values
        )
        efficient_portfolios.append({
            'return': eff_return,
            'volatility': eff_volatility,
            'sharpe': eff_sharpe,
            'weights': result.x
        })

# ============================================
# 绘制马科维茨组合图
# ============================================
print("\n📈 绘制马科维茨组合图...")

fig, ax = plt.subplots(figsize=(16, 12))

# 1. 生成随机组合用于散点图
print("  生成随机组合散点...")
np.random.seed(42)
n_portfolios = 5000
random_returns_list = []
random_vols_list = []
random_sharpes_list = []

for _ in range(n_portfolios):
    weights = np.random.random(n_assets)
    weights /= np.sum(weights)
    
    p_return, p_volatility, p_sharpe = portfolio_performance(
        weights, annual_returns.values, cov_matrix.values
    )
    random_returns_list.append(p_return)
    random_vols_list.append(p_volatility)
    random_sharpes_list.append(p_sharpe)

# 绘制随机组合散点
scatter = ax.scatter(
    random_vols_list, 
    random_returns_list,
    c=random_sharpes_list,
    cmap='viridis',
    alpha=0.4,
    s=15,
    zorder=1
)
cbar = plt.colorbar(scatter, ax=ax)
cbar.set_label('Sharpe Ratio', fontsize=11)

# 2. 绘制有效前沿
if efficient_portfolios:
    eff_vols = [p['volatility'] for p in efficient_portfolios]
    eff_rets = [p['return'] for p in efficient_portfolios]
    ax.plot(eff_vols, eff_rets, 'b-', linewidth=3, label='Efficient Frontier', zorder=3)

# 3. 绘制资本市场线 (CML)
x_cml = np.linspace(0, max(max(random_vols_list), optimal_volatility) * 1.1, 100)
y_cml = risk_free_rate + (optimal_return - risk_free_rate) / optimal_volatility * x_cml
ax.plot(x_cml, y_cml, 'r--', linewidth=2, alpha=0.7, label='Capital Market Line', zorder=2)

# 4. 绘制单个资产
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
for i, pair in enumerate(available_target_pairs):
    ax.scatter(
        annual_volatility[pair], 
        annual_returns[pair],
        s=400,
        marker='o',
        c=colors[i % len(colors)],
        edgecolors='black',
        linewidths=2,
        label=f'{pair} (SR={sharpe_ratios[pair]:.2f})',
        zorder=4
    )
    ax.annotate(
        pair,
        (annual_volatility[pair], annual_returns[pair]),
        xytext=(12, 8),
        textcoords='offset points',
        fontsize=12,
        fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8)
    )

# 5. 标记最优组合 (最大夏普比率) - 金色星星
ax.scatter(
    optimal_volatility, 
    optimal_return,
    s=800,
    marker='*',
    c='gold',
    edgecolors='darkred',
    linewidths=3,
    label=f'OPTIMAL (SR={optimal_sharpe_ratio:.2f})',
    zorder=6
)

# 6. 标记最小方差组合 - 绿色方块
ax.scatter(
    min_var_volatility,
    min_var_return,
    s=500,
    marker='s',
    c='lightgreen',
    edgecolors='darkgreen',
    linewidths=2,
    label=f'Min Variance (Vol={min_var_volatility:.1%})',
    zorder=5
)

# 7. 标记等权重组合 - 紫色菱形
ax.scatter(
    eq_vol, eq_ret,
    s=400,
    marker='D',
    c='plum',
    edgecolors='purple',
    linewidths=2,
    label=f'Equal Weight (SR={eq_sharpe:.2f})',
    zorder=5
)

# 8. 绘制无风险利率线
ax.axhline(y=risk_free_rate, color='gray', linestyle=':', alpha=0.5)
ax.text(ax.get_xlim()[1]*0.95, risk_free_rate+0.002, f'Risk-free ({risk_free_rate:.0%})', 
        fontsize=9, color='gray', ha='right')

# 设置图表样式
ax.set_xlabel('Annual Volatility (Standard Deviation)', fontsize=13, fontweight='bold')
ax.set_ylabel('Annual Expected Return', fontsize=13, fontweight='bold')
ax.set_title(
    f'Markowitz Portfolio Optimization\nCurrency Pairs: {", ".join(available_target_pairs)}',
    fontsize=15,
    fontweight='bold',
    pad=20
)
ax.legend(loc='upper left', fontsize=10, framealpha=0.9)
ax.grid(True, alpha=0.3, linestyle='--')

# 设置坐标轴格式为百分比
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: '{:.0%}'.format(y)))
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: '{:.0%}'.format(x)))

# 添加注释框 - 最优组合详情
textstr = '╔══════════════════════════════════════╗\n'
textstr += '║     OPTIMAL PORTFOLIO (Max Sharpe)    ║\n'
textstr += '╠══════════════════════════════════════╣\n'
for i, pair in enumerate(available_target_pairs):
    textstr += f'║  {pair:10}: {optimal_weights[i]:>7.1%}                 ║\n'
textstr += '╠══════════════════════════════════════╣\n'
textstr += f'║  Expected Return:  {optimal_return:>8.2%}          ║\n'
textstr += f'║  Volatility:       {optimal_volatility:>8.2%}          ║\n'
textstr += f'║  Sharpe Ratio:     {optimal_sharpe_ratio:>8.3f}          ║\n'
textstr += '╚══════════════════════════════════════╝'

props = dict(boxstyle='round', facecolor='lightyellow', alpha=0.95, edgecolor='darkred', linewidth=2)
ax.text(0.02, 0.98, textstr, transform=ax.transAxes, fontsize=10,
        verticalalignment='top', horizontalalignment='left', bbox=props, family='monospace')

plt.tight_layout()
plt.savefig(f'{output_dir}/markowitz_portfolio.png', dpi=150, bbox_inches='tight', facecolor='white')
print(f"✅ 马科维茨组合图已保存至: {output_dir}/markowitz_portfolio.png")

# 保存详细结果
results = {
    'analysis_date': pd.Timestamp.now().strftime('%Y-%m-%d'),
    'data_period': f"{returns_df.index[0].strftime('%Y-%m-%d')} to {returns_df.index[-1].strftime('%Y-%m-%d')}",
    'trading_days': len(returns_df),
    'risk_free_rate': risk_free_rate,
    'individual_assets': {
        pair: {
            'annual_return': float(annual_returns[pair]),
            'annual_volatility': float(annual_volatility[pair]),
            'sharpe_ratio': float(sharpe_ratios[pair])
        } for pair in available_target_pairs
    },
    'optimal_portfolio': {
        'weights': {pair: float(optimal_weights[i]) for i, pair in enumerate(available_target_pairs)},
        'annual_return': float(optimal_return),
        'annual_volatility': float(optimal_volatility),
        'sharpe_ratio': float(optimal_sharpe_ratio)
    },
    'min_variance_portfolio': {
        'weights': {pair: float(min_var_weights[i]) for i, pair in enumerate(available_target_pairs)},
        'annual_return': float(min_var_return),
        'annual_volatility': float(min_var_volatility),
        'sharpe_ratio': float(min_var_sharpe)
    },
    'equal_weight_portfolio': {
        'weights': {pair: float(1/n_assets) for pair in available_target_pairs},
        'annual_return': float(eq_ret),
        'annual_volatility': float(eq_vol),
        'sharpe_ratio': float(eq_sharpe)
    }
}

# 保存为JSON
import json
with open(f'{output_dir}/portfolio_results.json', 'w') as f:
    json.dump(results, f, indent=2)

print(f"✅ 详细结果已保存至: {output_dir}/portfolio_results.json")

# 打印最终汇总
print("\n" + "=" * 70)
print("📊 分析完成 - 最终结果汇总")
print("=" * 70)
print(f"\n分析货币对: {', '.join(available_target_pairs)}")
print(f"数据时间范围: {returns_df.index[0].strftime('%Y-%m-%d')} 至 {returns_df.index[-1].strftime('%Y-%m-%d')}")
print(f"总交易日: {len(returns_df)}")
print(f"无风险利率假设: {risk_free_rate:.0%}")

print("\n" + "-" * 70)
print("📈 各货币对夏普比率排名:")
print("-" * 70)
sorted_sharpe = sorted([(pair, sharpe_ratios[pair]) for pair in available_target_pairs], 
                       key=lambda x: x[1], reverse=True)
for rank, (pair, sr) in enumerate(sorted_sharpe, 1):
    ret = annual_returns[pair]
    vol = annual_volatility[pair]
    print(f"  {rank}. {pair:10} | 夏普: {sr:+.4f} | 收益: {ret:+.2%} | 波动: {vol:.2%}")

print("\n" + "-" * 70)
print("🎯 马科维茨最优组合 (最大夏普比率):")
print("-" * 70)
for i, pair in enumerate(available_target_pairs):
    bar = '█' * int(optimal_weights[i] * 50)
    print(f"  {pair:10}: {optimal_weights[i]:>7.2%} {bar}")
print(f"\n  组合夏普比率: {optimal_sharpe_ratio:.4f}")
print(f"  组合年化收益: {optimal_return:+.4%}")
print(f"  组合年化波动: {optimal_volatility:.4%}")

print("\n" + "=" * 70)
print("📁 输出文件:")
print(f"  • 夏普比率: {output_dir}/sharpe_ratios.csv")
print(f"  • 组合图表: {output_dir}/markowitz_portfolio.png")
print(f"  • 详细结果: {output_dir}/portfolio_results.json")
print("=" * 70)
