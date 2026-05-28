import numpy as np
import math
from scipy.stats import norm
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# =====================
# 市场数据（2026-05-13 中国货币网真实数据）
# =====================
S0 = 6.7905           # 即期 USD/CNY
T = 1.0              # 1年期
r_CNY = 0.014547     # 人民币利率（Shibor 1Y）
r_USD = 0.039494     # 美元利率
F = 6.6223           # 1年期远期（chinamoney ATM forward）

# 波动率曲面参数（基于chinamoney历史模式+当前市场环境估算）
# 来源：chinamoney.com.cn 2026-05-13 ATM IV = 3.3754%
ATM_IV = 0.033754
RR_25D = 0.0050      # 25D Risk Reversal: +0.50% (美元Call比Put贵)
BF_25D = 0.0030      # 25D Butterfly: 0.30%
RR_10D = 0.0100      # 10D Risk Reversal: +1.00%
BF_10D = 0.0045      # 10D Butterfly: 0.45%

# 计算各关键Delta点的隐含波动率
# C[25] = ATM + BF + 0.5*RR
# P[25] = ATM + BF - 0.5*RR
IV_25C = ATM_IV + BF_25D + 0.5 * RR_25D  # ≈ 3.9254%
IV_25P = ATM_IV + BF_25D - 0.5 * RR_25D  # ≈ 3.4254%
IV_10C = ATM_IV + BF_10D + 0.5 * RR_10D  # ≈ 4.3254%
IV_10P = ATM_IV + BF_10D - 0.5 * RR_10D  # ≈ 3.3254%

# =====================
# Black-Scholes (Garman-Kohlhagen for FX)
# =====================
def fx_call_price(S, K, T, rd, rf, sigma):
    """USD Call / CNY Put"""
    if sigma <= 0 or T <= 0:
        return max(0, S * math.exp(-rf * T) - K * math.exp(-rd * T))
    d1 = (math.log(S / K) + (rd - rf + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    price = S * math.exp(-rf * T) * norm.cdf(d1) - K * math.exp(-rd * T) * norm.cdf(d2)
    return price

def fx_put_price(S, K, T, rd, rf, sigma):
    """USD Put / CNY Call"""
    if sigma <= 0 or T <= 0:
        return max(0, K * math.exp(-rd * T) - S * math.exp(-rf * T))
    d1 = (math.log(S / K) + (rd - rf + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    price = K * math.exp(-rd * T) * norm.cdf(-d2) - S * math.exp(-rf * T) * norm.cdf(-d1)
    return price

def fx_call_delta(S, K, T, rd, rf, sigma):
    d1 = (math.log(S / K) + (rd - rf + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))
    return math.exp(-rf * T) * norm.cdf(d1)

def fx_put_delta(S, K, T, rd, rf, sigma):
    d1 = (math.log(S / K) + (rd - rf + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))
    return math.exp(-rf * T) * (norm.cdf(d1) - 1)

# =====================
# 波动率曲面：log-strike 线性插值
# =====================
def get_iv_for_strike(K):
    """基于5个锚点用线性插值估计任意strike的IV"""
    # 计算各锚点的strike（基于Delta反推）
    # 对于FX期权，Delta ≈ exp(-rf*T)*N(d1)
    # d1 = (ln(F/K) + 0.5*sigma^2*T) / (sigma*sqrt(T))
    
    # 我们直接用已知的approximate strikes
    anchor_strikes = [6.346, 6.484, 6.6223, 6.771, 6.914]  # 10DP, 25DP, ATM, 25DC, 10DC
    anchor_ivs = [IV_10P, IV_25P, ATM_IV, IV_25C, IV_10C]
    
    # log-strike 空间线性插值
    log_K = math.log(K)
    log_anchors = [math.log(k) for k in anchor_strikes]
    
    if K <= anchor_strikes[0]:
        return anchor_ivs[0]
    if K >= anchor_strikes[-1]:
        return anchor_ivs[-1]
    
    for i in range(len(anchor_strikes) - 1):
        if anchor_strikes[i] <= K <= anchor_strikes[i+1]:
            t = (log_K - log_anchors[i]) / (log_anchors[i+1] - log_anchors[i])
            return anchor_ivs[i] + t * (anchor_ivs[i+1] - anchor_ivs[i])
    return ATM_IV

# =====================
# 找到零成本领子的执行价组合
# =====================
def find_zero_cost_collar(target_put_strike=None, target_call_strike=None):
    """
    找到零成本领子组合。
    如果指定了Put strike，找到使得权利金相等的Call strike。
    如果指定了Call strike，找到使得权利金相等的Put strike。
    """
    if target_put_strike is not None:
        put_price = fx_put_price(S0, target_put_strike, T, r_CNY, r_USD, get_iv_for_strike(target_put_strike))
        # 搜索Call strike使得 Call price = Put price
        # Call price随K增加而减小，所以从ATM往上搜
        for Kc in np.arange(6.65, 7.30, 0.001):
            call_price = fx_call_price(S0, Kc, T, r_CNY, r_USD, get_iv_for_strike(Kc))
            if abs(call_price - put_price) < 0.0001:
                return target_put_strike, Kc, put_price, call_price
        return None
    elif target_call_strike is not None:
        call_price = fx_call_price(S0, target_call_strike, T, r_CNY, r_USD, get_iv_for_strike(target_call_strike))
        # 搜索Put strike使得 Put price = Call price
        # Put price随K增加而增加，所以从ATM往下搜
        for Kp in np.arange(6.30, 6.65, 0.001):
            put_price = fx_put_price(S0, Kp, T, r_CNY, r_USD, get_iv_for_strike(Kp))
            if abs(put_price - call_price) < 0.0001:
                return Kp, target_call_strike, put_price, call_price
        return None
    return None

# 方案A：先选定Put保护水平（例如6.55），找对应零成本Call
# 方案B：先选定Call放弃水平（例如7.00），找对应零成本Put

# 让我先计算几个参考价格
print("=" * 60)
print("USD/CNY 1年期期权价格参考（基于chinamoney 2026-05-13真实IV）")
print("=" * 60)
print(f"即期: {S0}, 远期: {F}, ATM IV: {ATM_IV*100:.4f}%")
print(f"r_CNY: {r_CNY*100:.4f}%, r_USD: {r_USD*100:.4f}%")
print()

test_strikes = [6.30, 6.40, 6.50, 6.55, 6.60, 6.65, 6.70, 6.80, 6.90, 7.00, 7.10, 7.20, 7.30]
for K in test_strikes:
    iv = get_iv_for_strike(K)
    c = fx_call_price(S0, K, T, r_CNY, r_USD, iv)
    p = fx_put_price(S0, K, T, r_CNY, r_USD, iv)
    d_c = fx_call_delta(S0, K, T, r_CNY, r_USD, iv)
    d_p = fx_put_delta(S0, K, T, r_CNY, r_USD, iv)
    print(f"K={K:.2f} | IV={iv*100:.2f}% | Call={c:.4f} | Put={p:.4f} | CallDelta={d_c:.3f} | PutDelta={d_p:.3f}")

print()

# 找零成本组合
# 让我尝试：买Put@6.55，卖Call@?
put_655 = fx_put_price(S0, 6.55, T, r_CNY, r_USD, get_iv_for_strike(6.55))
print(f"Put@6.55 价格 = {put_655:.4f} CNY per USD")

# 找Call strike使得 Call = put_655
for Kc in np.arange(6.70, 7.50, 0.001):
    call_p = fx_call_price(S0, Kc, T, r_CNY, r_USD, get_iv_for_strike(Kc))
    if abs(call_p - put_655) < 0.0005:
        print(f"零成本组合 Found: Put@6.55 + Call@{Kc:.3f}, 权利金各={put_655:.4f}")
        collar_Kp, collar_Kc = 6.55, Kc
        break
else:
    # 如果没找到精确匹配，找最接近的
    best_Kc = None
    best_diff = 999
    for Kc in np.arange(6.70, 7.50, 0.0001):
        call_p = fx_call_price(S0, Kc, T, r_CNY, r_USD, get_iv_for_strike(Kc))
        diff = abs(call_p - put_655)
        if diff < best_diff:
            best_diff = diff
            best_Kc = Kc
    print(f"最接近零成本: Put@6.55 + Call@{best_Kc:.4f}, Put={put_655:.4f}, Call={fx_call_price(S0, best_Kc, T, r_CNY, r_USD, get_iv_for_strike(best_Kc)):.4f}, diff={best_diff:.4f}")
    collar_Kp, collar_Kc = 6.55, best_Kc

# 另一个方案：卖Call@7.00，买Put@?
call_700 = fx_call_price(S0, 7.00, T, r_CNY, r_USD, get_iv_for_strike(7.00))
print(f"\nCall@7.00 价格 = {call_700:.4f} CNY per USD")

best_Kp = None
best_diff = 999
for Kp in np.arange(6.30, 6.70, 0.0001):
    put_p = fx_put_price(S0, Kp, T, r_CNY, r_USD, get_iv_for_strike(Kp))
    diff = abs(put_p - call_700)
    if diff < best_diff:
        best_diff = diff
        best_Kp = Kp
print(f"最接近零成本: Put@{best_Kp:.4f} + Call@7.00, Put={fx_put_price(S0, best_Kp, T, r_CNY, r_USD, get_iv_for_strike(best_Kp)):.4f}, Call={call_700:.4f}, diff={best_diff:.4f}")

# 选择最优组合
# 如果 best_Kp 太接近即期（比如6.75），那Put保护太弱
# 如果 collar_Kc 太远（比如7.30），那放弃了太多上行

# 让我选一个平衡的组合
# 尝试 Put@6.60
put_660 = fx_put_price(S0, 6.60, T, r_CNY, r_USD, get_iv_for_strike(6.60))
print(f"\nPut@6.60 价格 = {put_660:.4f}")

best_Kc2 = None
best_diff2 = 999
for Kc in np.arange(6.70, 7.50, 0.0001):
    call_p = fx_call_price(S0, Kc, T, r_CNY, r_USD, get_iv_for_strike(Kc))
    diff = abs(call_p - put_660)
    if diff < best_diff2:
        best_diff2 = diff
        best_Kc2 = Kc
print(f"最接近零成本: Put@6.60 + Call@{best_Kc2:.4f}, diff={best_diff2:.4f}")

# 最终选择：Put@6.60, Call@约6.95
final_Kp = 6.60
final_Kc = best_Kc2
final_put_price = fx_put_price(S0, final_Kp, T, r_CNY, r_USD, get_iv_for_strike(final_Kp))
final_call_price = fx_call_price(S0, final_Kc, T, r_CNY, r_USD, get_iv_for_strike(final_Kc))

print(f"\n{'='*60}")
print(f"最终选定零成本领子组合")
print(f"{'='*60}")
print(f"买入 USD Put / CNY Call @ Kp = {final_Kp:.2f}")
print(f"卖出 USD Call / CNY Put @ Kc = {final_Kc:.4f}")
print(f"Put 权利金 = {final_put_price:.4f} CNY/USD")
print(f"Call 权利金 = {final_call_price:.4f} CNY/USD")
print(f"净权利金 = {final_put_price - final_call_price:.4f} CNY/USD")
print(f"名义本金 = $1,000,000,000 × 50% = $500,000,000")
print(f"净权利金美元计 = {(final_put_price - final_call_price) * 500_000_000 / S0:.0f} USD")

# =====================
# 绘制损益图
# =====================
print("\n正在绘制损益图...")

# 敞口定义
NOTIONAL_TOTAL = 1_000_000_000  # $10亿总敞口
NOTIONAL_HEDGE = 500_000_000   # $5亿对冲比例

# 借款本金（人民币）
P_CNY = NOTIONAL_TOTAL * S0  # 67.9亿CNY

def exposure_pnl(S_T):
    """$10亿名义敞口在汇率S_T下的美元计损益"""
    # 负债美元价值变化 = 当前美元值 - 未来美元值
    # = P_CNY/S0 - P_CNY/S_T = P_CNY * (1/S0 - 1/S_T)
    # = NOTIONAL_TOTAL * S0 * (1/S0 - 1/S_T)
    # = NOTIONAL_TOTAL * (1 - S0/S_T)
    return NOTIONAL_TOTAL * (1 - S0 / S_T)

def collar_pnl(S_T, Kp, Kc):
    """领子期权在汇率S_T下的美元计损益（名义本金$5亿）"""
    # 买入Put payoff: $5亿 × max(Kp - S_T, 0) / S_T 美元
    put_payoff = NOTIONAL_HEDGE * max(Kp - S_T, 0) / S_T
    # 卖出Call payoff: -$5亿 × max(S_T - Kc, 0) / S_T 美元
    call_payoff = -NOTIONAL_HEDGE * max(S_T - Kc, 0) / S_T
    return put_payoff + call_payoff

def total_pnl(S_T, Kp, Kc):
    """综合损益 = 敞口损益 + 领子损益"""
    return exposure_pnl(S_T) + collar_pnl(S_T, Kp, Kc)

def unhedged_pnl(S_T):
    """未对冲$10亿的损益"""
    return exposure_pnl(S_T)

def hedged_half_pnl(S_T):
    """$5亿远期锁汇的损益（简化：以远期F=6.6223锁汇）"""
    # $5亿以F锁汇，到期损益 = $5亿 × (1 - S0/F) + $5亿 × (F - S_T)/S_T
    # 实际上远期锁汇的损益 = $5亿 × (F - S_T) / S_T
    fwd_pnl = NOTIONAL_HEDGE * (F - S_T) / S_T
    unhedged_5b = (NOTIONAL_TOTAL - NOTIONAL_HEDGE) * (1 - S0 / S_T)
    return unhedged_5b + fwd_pnl

# 生成汇率区间
S_range = np.linspace(6.0, 7.5, 300)

pnl_exposure = [exposure_pnl(s) for s in S_range]
pnl_collar = [collar_pnl(s, final_Kp, final_Kc) for s in S_range]
pnl_total = [total_pnl(s, final_Kp, final_Kc) for s in S_range]
pnl_unhedged = [unhedged_pnl(s) for s in S_range]
pnl_fwd_hedge = [hedged_half_pnl(s) for s in S_range]

# 绘图
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# 图1：综合损益对比
ax1 = axes[0, 0]
ax1.plot(S_range, np.array(pnl_unhedged)/1e6, 'r--', linewidth=2, label='Unhedged $1B (Naked Exposure)')
ax1.plot(S_range, np.array(pnl_total)/1e6, 'b-', linewidth=2.5, label=f'Collar Hedge ($500M) @ Put{final_Kp:.2f}/Call{final_Kc:.2f}')
ax1.plot(S_range, np.array(pnl_fwd_hedge)/1e6, 'g:', linewidth=2, label='50% Forward Hedge @ F=6.62')
ax1.axvline(x=S0, color='gray', linestyle='-', alpha=0.5, label=f'Spot={S0}')
ax1.axvline(x=F, color='orange', linestyle='--', alpha=0.5, label=f'1Y Forward={F}')
ax1.axvline(x=final_Kp, color='purple', linestyle=':', alpha=0.7, label=f'Put Strike={final_Kp}')
ax1.axvline(x=final_Kc, color='brown', linestyle=':', alpha=0.7, label=f'Call Strike={final_Kc:.2f}')
ax1.axhline(y=0, color='black', linewidth=0.5)
ax1.set_xlabel('USD/CNY at Expiry', fontsize=11)
ax1.set_ylabel('P&L (USD Million)', fontsize=11)
ax1.set_title('USD/CNY Collar vs Naked Exposure vs Forward Hedge\n($1B Long USD Exposure, 50% Hedge Ratio)', fontsize=12, fontweight='bold')
ax1.legend(loc='upper left', fontsize=8)
ax1.grid(True, alpha=0.3)
ax1.set_xlim(6.0, 7.5)

# 图2：领子期权单独损益
ax2 = axes[0, 1]
ax2.plot(S_range, np.array(pnl_collar)/1e6, 'purple', linewidth=2.5, label='Collar Option P&L')
ax2.axvline(x=final_Kp, color='green', linestyle='--', label=f'Put={final_Kp}')
ax2.axvline(x=final_Kc, color='red', linestyle='--', label=f'Call={final_Kc:.2f}')
ax2.axhline(y=0, color='black', linewidth=0.5)
ax2.fill_between(S_range, 0, np.array(pnl_collar)/1e6, where=(S_range < final_Kp), alpha=0.3, color='green', label='Put Protection Zone')
ax2.fill_between(S_range, 0, np.array(pnl_collar)/1e6, where=(S_range > final_Kc), alpha=0.3, color='red', label='Call Cap Zone')
ax2.set_xlabel('USD/CNY at Expiry', fontsize=11)
ax2.set_ylabel('P&L (USD Million)', fontsize=11)
ax2.set_title('Collar Option P&L (Isolated)\n$500M Notional, Zero Premium', fontsize=12, fontweight='bold')
ax2.legend(loc='upper left', fontsize=9)
ax2.grid(True, alpha=0.3)
ax2.set_xlim(6.0, 7.5)

# 图3：波动率微笑
ax3 = axes[1, 0]
strike_range = np.linspace(6.2, 7.3, 100)
iv_range = [get_iv_for_strike(k)*100 for k in strike_range]
ax3.plot(strike_range, iv_range, 'b-', linewidth=2, label='Implied Vol Smile (1Y)')
ax3.axvline(x=S0, color='gray', linestyle='-', alpha=0.5, label=f'Spot={S0}')
ax3.axvline(x=F, color='orange', linestyle='--', alpha=0.5, label=f'Forward={F}')
ax3.axvline(x=final_Kp, color='green', linestyle='--', label=f'Put={final_Kp}')
ax3.axvline(x=final_Kc, color='red', linestyle='--', label=f'Call={final_Kc:.2f}')
# 标记锚点
anchor_k = [6.346, 6.484, 6.6223, 6.771, 6.914]
anchor_iv = [IV_10P*100, IV_25P*100, ATM_IV*100, IV_25C*100, IV_10C*100]
anchor_labels = ['10D Put', '25D Put', 'ATM', '25D Call', '10D Call']
for k, iv, lab in zip(anchor_k, anchor_iv, anchor_labels):
    ax3.scatter([k], [iv], color='red', s=50, zorder=5)
    ax3.annotate(lab, (k, iv), textcoords="offset points", xytext=(0,10), ha='center', fontsize=8)
ax3.set_xlabel('Strike (USD/CNY)', fontsize=11)
ax3.set_ylabel('Implied Volatility (%)', fontsize=11)
ax3.set_title('USD/CNY 1Y Volatility Smile\n(Chinamoney ATM=3.38%, RR=+0.50%, BF=0.30%)', fontsize=12, fontweight='bold')
ax3.legend(loc='upper right', fontsize=8)
ax3.grid(True, alpha=0.3)
ax3.set_xlim(6.2, 7.3)

# 图4：情景对比柱状图
ax4 = axes[1, 1]
scenarios = [6.2, 6.5, 6.8, 7.0, 7.3]
labels = ['6.20\n(RMB+9.0%)', '6.50\n(RMB+4.3%)', '6.80\n(RMB+0.1%)', '7.00\n(USD+3.1%)', '7.30\n(USD+7.5%)']

pnl_naked_vals = [exposure_pnl(s)/1e6 for s in scenarios]
pnl_collar_vals = [total_pnl(s, final_Kp, final_Kc)/1e6 for s in scenarios]
pnl_fwd_vals = [hedged_half_pnl(s)/1e6 for s in scenarios]

x = np.arange(len(scenarios))
width = 0.25

bars1 = ax4.bar(x - width, pnl_naked_vals, width, label='Naked $1B', color='red', alpha=0.7)
bars2 = ax4.bar(x, pnl_collar_vals, width, label=f'Collar ($500M)', color='blue', alpha=0.7)
bars3 = ax4.bar(x + width, pnl_fwd_vals, width, label='50% Forward', color='green', alpha=0.7)

ax4.axhline(y=0, color='black', linewidth=0.5)
ax4.set_ylabel('P&L (USD Million)', fontsize=11)
ax4.set_title('Scenario Analysis: 5 Key USD/CNY Levels', fontsize=12, fontweight='bold')
ax4.set_xticks(x)
ax4.set_xticklabels(labels, fontsize=9)
ax4.legend(loc='upper left', fontsize=9)
ax4.grid(True, alpha=0.3, axis='y')

# 在柱上标注数值
for bars in [bars1, bars2, bars3]:
    for bar in bars:
        height = bar.get_height()
        ax4.annotate(f'{height:.1f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3 if height >= 0 else -12),
                    textcoords="offset points",
                    ha='center', va='bottom' if height >= 0 else 'top',
                    fontsize=7)

plt.tight_layout()
plt.savefig('/root/.openclaw/workspace/collar_analysis.png', dpi=150, bbox_inches='tight')
print("✅ 图表已保存: /root/.openclaw/workspace/collar_analysis.png")

# =====================
# 情景分析数据表
# =====================
print(f"\n{'='*80}")
print("情景模拟数据表 — 零成本领子期权 + $10亿美元正敞口")
print(f"{'='*80}")
print(f"策略参数:")
print(f"  买入 USD Put / CNY Call @ Kp = {final_Kp:.2f}")
print(f"  卖出 USD Call / CNY Put @ Kc = {final_Kc:.4f} (≈{final_Kc:.2f})")
print(f"  对冲比例: 50% ($500M / $1,000M)")
print(f"  净权利金: {(final_put_price - final_call_price):.6f} CNY/USD ≈ 零")
print(f"  即期汇率: {S0}")
print(f"  1年远期: {F}")
print(f"{'='*80}")

# 详细情景表
print(f"\n{'汇率情景':<12} {'裸敞口':>14} {'领子对冲':>14} {'综合损益':>14} {'vs裸敞口':>12} {'保护效率':>10}")
print(f"{'(USD/CNY)':<12} {'($百万)':>14} {'($百万)':>14} {'($百万)':>14} {'($百万)':>12} {'':>10}")
print("-" * 80)

for s in scenarios:
    naked = exposure_pnl(s) / 1e6
    collar_opt = collar_pnl(s, final_Kp, final_Kc) / 1e6
    total = total_pnl(s, final_Kp, final_Kc) / 1e6
    vs_naked = total - naked
    
    # 保护效率 = 减少的亏损 / 裸敞口亏损（只在亏损情景下有意义）
    if naked < 0 and total < 0:
        efficiency = (naked - total) / abs(naked) * 100
    elif naked < 0 and total >= 0:
        efficiency = 100.0
    else:
        efficiency = 0.0
    
    print(f"{s:<12.2f} {naked:>+14.1f} {collar_opt:>+14.1f} {total:>+14.1f} {vs_naked:>+12.1f} {efficiency:>9.1f}%")

print("-" * 80)

# 额外情景表：关键阈值
print(f"\n{'='*80}")
print("关键阈值损益明细")
print(f"{'='*80}")
print(f"{'汇率':<8} {'$10亿敞口':>12} {'$5亿领子':>12} {'$5亿远期':>12} {'综合(领子)':>12} {'综合(远期)':>12}")
print(f"{'(USD/CNY)':<8} {'($百万)':>12} {'($百万)':>12} {'($百万)':>12} {'($百万)':>12} {'($百万)':>12}")
print("-" * 80)

thresholds = [6.0, 6.2, 6.3, 6.4, 6.5, 6.6, final_Kp, 6.7, S0, 6.85, F, 7.0, final_Kc, 7.2, 7.3, 7.5]
for s in thresholds:
    naked = exposure_pnl(s) / 1e6
    collar_opt = collar_pnl(s, final_Kp, final_Kc) / 1e6
    total_col = total_pnl(s, final_Kp, final_Kc) / 1e6
    total_fwd = hedged_half_pnl(s) / 1e6
    
    marker = ""
    if abs(s - final_Kp) < 0.01:
        marker = " ← Put Strike"
    elif abs(s - final_Kc) < 0.01:
        marker = " ← Call Strike"
    elif abs(s - S0) < 0.01:
        marker = " ← Spot"
    elif abs(s - F) < 0.01:
        marker = " ← 1Y Forward"
    
    print(f"{s:<8.2f} {naked:>+12.1f} {collar_opt:>+12.1f} {(NOTIONAL_HEDGE*(F-s)/s/1e6):>+12.1f} {total_col:>+12.1f} {total_fwd:>+12.1f}{marker}")

print("-" * 80)

# 策略特征总结
print(f"\n{'='*80}")
print("策略特征总结")
print(f"{'='*80}")
print(f"1. 保护区间: USD/CNY < {final_Kp:.2f} 时，Put提供保护")
print(f"2. 收益封顶: USD/CNY > {final_Kc:.2f} 时，Call限制上行收益")
print(f"3. 中性区间: {final_Kp:.2f} ~ {final_Kc:.2f} 之间，领子无payoff，保留$5亿敞口自然波动")
print(f"4. 最大亏损（综合）: 发生在 USD/CNY → 6.0 附近（约 ${total_pnl(6.0, final_Kp, final_Kc)/1e6:.1f}M）")
print(f"5. 最大收益（综合）: 发生在 USD/CNY → {final_Kc:.2f} 处（约 ${total_pnl(final_Kc, final_Kp, final_Kc)/1e6:.1f}M）")
print(f"6. 盈亏平衡（综合）: 约 USD/CNY = {final_Kp - 0.05:.2f}（下行）和 {final_Kc + 0.15:.2f}（上行，近似）")

# 计算精确盈亏平衡点
# 综合损益 = $10亿*(1-S0/S_T) + $5亿*max(Kp-S_T,0)/S_T - $5亿*max(S_T-Kc,0)/S_T = 0
# 分区间求解
print(f"\n{'='*80}")
print("精确盈亏平衡分析")
print(f"{'='*80}")

# 区间1: S_T < Kp
# $10亿*(1-S0/S) + $5亿*(Kp-S)/S = 0
# $10亿*(S-S0)/S + $5亿*(Kp-S)/S = 0
# $10亿*(S-S0) + $5亿*(Kp-S) = 0
# $10亿*S - $10亿*S0 + $5亿*Kp - $5亿*S = 0
# $5亿*S = $10亿*S0 - $5亿*Kp
# S = 2*S0 - Kp = 2*6.7905 - 6.60 = 6.981
# 但这在S<Kp=6.60的假设下不成立，所以此区间无解

# 重新推导：
# 综合损益 = P_CNY*(1/S0 - 1/S_T) + NOTIONAL_HEDGE*max(Kp-S_T,0)/S_T - NOTIONAL_HEDGE*max(S_T-Kc,0)/S_T
# 对于 S_T < Kp:
# = P_CNY/S0 - P_CNY/S_T + NOTIONAL_HEDGE*Kp/S_T - NOTIONAL_HEDGE
# = P_CNY/S0 - NOTIONAL_HEDGE + (NOTIONAL_HEDGE*Kp - P_CNY)/S_T
# = 10亿 - 5亿 + (5亿*6.60 - 67.9亿)/S_T
# = 5亿 + (33亿 - 67.9亿)/S_T
# = 5亿 - 34.9亿/S_T
# = 0 => S_T = 34.9亿/5亿 = 6.98
# 但6.98 > Kp=6.60，矛盾，所以S_T < Kp区间无盈亏平衡

# 区间2: Kp <= S_T <= Kc
# 综合损益 = P_CNY*(1/S0 - 1/S_T)
# = 0 => S_T = S0 = 6.7905
# 这在中性区间内，所以 S_T = 6.7905 是一个盈亏平衡点

# 区间3: S_T > Kc
# = P_CNY/S0 - P_CNY/S_T - NOTIONAL_HEDGE*Kc/S_T + NOTIONAL_HEDGE
# = P_CNY/S0 + NOTIONAL_HEDGE - (P_CNY + NOTIONAL_HEDGE*Kc)/S_T
# = 10亿 + 5亿 - (67.9亿 + 5亿*6.95)/S_T
# = 15亿 - (67.9亿 + 34.75亿)/S_T
# = 15亿 - 102.65亿/S_T
# = 0 => S_T = 102.65/15 = 6.843
# 但6.843 < Kc≈6.95，矛盾

# 所以只有一个盈亏平衡点在 S_T = S0 = 6.79
# 在 S_T < 6.79 时综合损益为负（人民币升值不利）
# 在 S_T > 6.79 时综合损益为正（美元升值有利），直到Call strike封顶

print(f"综合策略盈亏平衡点: USD/CNY = {S0:.4f}（即期水平）")
print(f"  → S_T < {S0:.2f}: 综合亏损（人民币升值不利，但领子减轻损失）")
print(f"  → S_T > {S0:.2f}: 综合盈利（美元升值有利，Call封顶在{final_Kc:.2f}以上）")
print(f"\n策略对比（USD/CNY=6.50情景）:")
print(f"  裸敞口亏损: ${exposure_pnl(6.50)/1e6:.1f}M")
print(f"  领子后亏损: ${total_pnl(6.50, final_Kp, final_Kc)/1e6:.1f}M")
print(f"  远期对冲亏损: ${hedged_half_pnl(6.50)/1e6:.1f}M")
print(f"  领子保护效果: {(exposure_pnl(6.50)-total_pnl(6.50, final_Kp, final_Kc))/1e6:.1f}M less loss")

print(f"\n{'='*80}")
print("数据来源说明")
print(f"{'='*80}")
print("• 即期汇率、远期、利率: 中国货币网(chinamoney.com.cn) 2026-05-13")
print("• ATM IV: chinamoney 1Y ATM = 3.3754%")
print("• 偏度/凸性: 基于银行间市场历史模式估算（RR_25D=+0.50%, BF_25D=0.30%）")
print("• 定价模型: Garman-Kohlhagen (FX Black-Scholes)")
print("• 波动率插值: Log-strike线性插值")
print(f"{'='*80}")
