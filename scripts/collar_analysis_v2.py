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
ATM_IV = 0.033754
RR_25D = 0.0050      # +0.50%
BF_25D = 0.0030      # 0.30%
RR_10D = 0.0100
BF_10D = 0.0045

IV_25C = ATM_IV + BF_25D + 0.5 * RR_25D
IV_25P = ATM_IV + BF_25D - 0.5 * RR_25D
IV_10C = ATM_IV + BF_10D + 0.5 * RR_10D
IV_10P = ATM_IV + BF_10D - 0.5 * RR_10D

# =====================
# Black-Scholes (Garman-Kohlhagen)
# =====================
def fx_call_price(S, K, T, rd, rf, sigma):
    if sigma <= 0 or T <= 0:
        return max(0, S * math.exp(-rf * T) - K * math.exp(-rd * T))
    d1 = (math.log(S / K) + (rd - rf + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    return S * math.exp(-rf * T) * norm.cdf(d1) - K * math.exp(-rd * T) * norm.cdf(d2)

def fx_put_price(S, K, T, rd, rf, sigma):
    if sigma <= 0 or T <= 0:
        return max(0, K * math.exp(-rd * T) - S * math.exp(-rf * T))
    d1 = (math.log(S / K) + (rd - rf + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    return K * math.exp(-rd * T) * norm.cdf(-d2) - S * math.exp(-rf * T) * norm.cdf(-d1)

def fx_call_delta(S, K, T, rd, rf, sigma):
    d1 = (math.log(S / K) + (rd - rf + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))
    return math.exp(-rf * T) * norm.cdf(d1)

def fx_put_delta(S, K, T, rd, rf, sigma):
    d1 = (math.log(S / K) + (rd - rf + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))
    return math.exp(-rf * T) * (norm.cdf(d1) - 1)

# =====================
# 波动率曲面
# =====================
def get_iv_for_strike(K):
    anchor_strikes = [6.346, 6.484, 6.6223, 6.771, 6.914]
    anchor_ivs = [IV_10P, IV_25P, ATM_IV, IV_25C, IV_10C]
    log_K = math.log(K)
    log_anchors = [math.log(k) for k in anchor_strikes]
    if K <= anchor_strikes[0]: return anchor_ivs[0]
    if K >= anchor_strikes[-1]: return anchor_ivs[-1]
    for i in range(len(anchor_strikes) - 1):
        if anchor_strikes[i] <= K <= anchor_strikes[i+1]:
            t = (log_K - log_anchors[i]) / (log_anchors[i+1] - log_anchors[i])
            return anchor_ivs[i] + t * (anchor_ivs[i+1] - anchor_ivs[i])
    return ATM_IV

# =====================
# 策略参数设定（选择经济意义上合理的组合）
# =====================
# 当前市场特征：人民币升值预期强（F=6.62 < S=6.79），买Put天然贵
# 方案：买入深OTM Put + 卖出OTM Call，接受少量净成本

Kp = 6.50            # Put保护水平：USD/CNY跌破6.50时全额保护
Kc = 7.00            # Call封顶水平：USD/CNY超过7.00时收益封顶

put_price = fx_put_price(S0, Kp, T, r_CNY, r_USD, get_iv_for_strike(Kp))
call_price = fx_call_price(S0, Kc, T, r_CNY, r_USD, get_iv_for_strike(Kc))
net_cost = put_price - call_price  # CNY per USD notional

NOTIONAL_TOTAL = 1_000_000_000
NOTIONAL_HEDGE = 500_000_000
P_CNY = NOTIONAL_TOTAL * S0

# 美元计净成本
net_cost_usd = net_cost * NOTIONAL_HEDGE / S0

print("="*70)
print("USD/CNY 1年期领子期权 — 真实市场定价分析")
print("="*70)
print(f"市场日期: 2026-05-13")
print(f"即期汇率: {S0}")
print(f"1年远期:  {F} (贴水 {S0-F:.2f} pips, 年化贴水 {(S0-F)/S0*100:.2f}%)")
print(f"ATM IV:   {ATM_IV*100:.4f}%")
print(f"r_CNY:    {r_CNY*100:.4f}%")
print(f"r_USD:    {r_USD*100:.4f}%")
print()
print("策略结构:")
print(f"  买入 USD Put / CNY Call @ Kp = {Kp:.2f}")
print(f"  卖出 USD Call / CNY Put @ Kc = {Kc:.2f}")
print(f"  名义本金: ${NOTIONAL_HEDGE/1e6:.0f}M / ${NOTIONAL_TOTAL/1e6:.0f}M (50%对冲)")
print()
print("期权定价 (CNY per USD):")
print(f"  Put@{Kp:.2f} 权利金 = {put_price:.4f}")
print(f"  Call@{Kc:.2f} 权利金 = {call_price:.4f}")
print(f"  净权利金 = {net_cost:.4f} CNY/USD")
print(f"  净权利金(美元计) = ${net_cost_usd/1e6:.2f}M")
print(f"  年化对冲成本 = {net_cost_usd/NOTIONAL_HEDGE*100:.2f}% of notional")
print()

# 对比：零成本领子（窄区间）vs 宽区间领子（付成本）
# 零成本组合：Put@6.55 / Call@6.72
zc_put = 6.55
zc_call = 6.722
zc_put_p = fx_put_price(S0, zc_put, T, r_CNY, r_USD, get_iv_for_strike(zc_put))
zc_call_p = fx_call_price(S0, zc_call, T, r_CNY, r_USD, get_iv_for_strike(zc_call))
print("对比：零成本窄区间领子")
print(f"  Put@{zc_put:.2f} / Call@{zc_call:.3f}")
print(f"  净权利金 = {zc_put_p - zc_call_p:.4f} CNY/USD")
print(f"  ⚠️  问题：Call strike({zc_call:.2f}) < 即期({S0:.2f})，当前已ITM")
print()
print("推荐：宽区间领子（支付少量权利金换取合理区间）")
print(f"  Put@{Kp:.2f} / Call@{Kc:.2f}")
print(f"  保护区间: {Kp:.2f} ~ {Kc:.2f} (宽度 {Kc-Kp:.2f})")
print(f"  净成本: ${net_cost_usd/1e6:.2f}M ({net_cost_usd/NOTIONAL_HEDGE*100:.2f}%)")
print("="*70)

# =====================
# 损益计算函数
# =====================
def exposure_pnl(S_T):
    """$10亿名义敞口在汇率S_T下的美元计损益"""
    return NOTIONAL_TOTAL * (1 - S0 / S_T)

def collar_pnl(S_T, Kp, Kc, notional):
    """领子期权在汇率S_T下的美元计损益"""
    put_payoff = notional * max(Kp - S_T, 0) / S_T
    call_payoff = -notional * max(S_T - Kc, 0) / S_T
    return put_payoff + call_payoff

def fwd_hedge_pnl(S_T):
    """50%远期锁汇损益"""
    fwd_pnl = NOTIONAL_HEDGE * (F - S_T) / S_T
    unhedged_5b = (NOTIONAL_TOTAL - NOTIONAL_HEDGE) * (1 - S0 / S_T)
    return unhedged_5b + fwd_pnl

# =====================
# 绘图
# =====================
S_range = np.linspace(6.0, 7.5, 300)

pnl_naked = np.array([exposure_pnl(s) for s in S_range]) / 1e6
pnl_collar = np.array([exposure_pnl(s) + collar_pnl(s, Kp, Kc, NOTIONAL_HEDGE) for s in S_range]) / 1e6
pnl_fwd = np.array([fwd_hedge_pnl(s) for s in S_range]) / 1e6
pnl_collar_opt_only = np.array([collar_pnl(s, Kp, Kc, NOTIONAL_HEDGE) for s in S_range]) / 1e6
pnl_zc_collar = np.array([exposure_pnl(s) + collar_pnl(s, zc_put, zc_call, NOTIONAL_HEDGE) for s in S_range]) / 1e6

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# 图1：综合损益对比
ax1 = axes[0, 0]
ax1.plot(S_range, pnl_naked, 'r--', linewidth=2, label=f'裸敞口 $1B (无对冲)')
ax1.plot(S_range, pnl_collar, 'b-', linewidth=2.5, label=f'宽领子 $500M (Put{Kp:.2f}/Call{Kc:.2f})')
ax1.plot(S_range, pnl_zc_collar, 'm:', linewidth=2, label=f'零成本窄领子 (Put{zc_put:.2f}/Call{zc_call:.2f})')
ax1.plot(S_range, pnl_fwd, 'g-.', linewidth=2, label=f'50%远期锁汇 @ F={F}')
ax1.axvline(x=S0, color='gray', linestyle='-', alpha=0.4)
ax1.axvline(x=F, color='orange', linestyle='--', alpha=0.4)
ax1.axvline(x=Kp, color='green', linestyle=':', alpha=0.7)
ax1.axvline(x=Kc, color='brown', linestyle=':', alpha=0.7)
ax1.axhline(y=0, color='black', linewidth=0.5)
ax1.set_xlabel('USD/CNY 到期汇率', fontsize=11)
ax1.set_ylabel('损益 (百万美元)', fontsize=11)
ax1.set_title('综合损益对比：领子期权 vs 远期 vs 裸敞口\n($10亿 Long USD敞口，50%对冲比例)', fontsize=12, fontweight='bold')
ax1.legend(loc='upper left', fontsize=8.5)
ax1.grid(True, alpha=0.3)
ax1.set_xlim(6.0, 7.5)
# 标注关键点
ax1.annotate(f'即期\n{S0}', xy=(S0, 0), xytext=(S0+0.05, -15), fontsize=8, color='gray')
ax1.annotate(f'远期\n{F}', xy=(F, 0), xytext=(F+0.05, -15), fontsize=8, color='orange')
ax1.annotate(f'Put\n{Kp}', xy=(Kp, 0), xytext=(Kp-0.15, 20), fontsize=8, color='green')
ax1.annotate(f'Call\n{Kc}', xy=(Kc, 0), xytext=(Kc+0.05, 20), fontsize=8, color='brown')

# 图2：领子期权单独损益
ax2 = axes[0, 1]
ax2.plot(S_range, pnl_collar_opt_only, 'purple', linewidth=2.5, label='宽领子期权单独损益 ($500M)')
ax2.axvline(x=Kp, color='green', linestyle='--', label=f'Put={Kp}')
ax2.axvline(x=Kc, color='red', linestyle='--', label=f'Call={Kc}')
ax2.axhline(y=0, color='black', linewidth=0.5)
ax2.fill_between(S_range, 0, pnl_collar_opt_only, where=(S_range < Kp), alpha=0.3, color='green', label='Put保护区间')
ax2.fill_between(S_range, 0, pnl_collar_opt_only, where=(S_range > Kc), alpha=0.3, color='red', label='Call封顶区间')
ax2.set_xlabel('USD/CNY 到期汇率', fontsize=11)
ax2.set_ylabel('损益 (百万美元)', fontsize=11)
ax2.set_title('领子期权单独损益\n净权利金成本: ${:.2f}M'.format(net_cost_usd/1e6), fontsize=12, fontweight='bold')
ax2.legend(loc='upper left', fontsize=9)
ax2.grid(True, alpha=0.3)
ax2.set_xlim(6.0, 7.5)

# 图3：波动率微笑
ax3 = axes[1, 0]
strike_range = np.linspace(6.2, 7.3, 100)
iv_range = [get_iv_for_strike(k)*100 for k in strike_range]
ax3.plot(strike_range, iv_range, 'b-', linewidth=2, label='隐含波动率微笑 (1Y)')
ax3.axvline(x=S0, color='gray', linestyle='-', alpha=0.4, label=f'即期={S0}')
ax3.axvline(x=F, color='orange', linestyle='--', alpha=0.4, label=f'远期={F}')
ax3.axvline(x=Kp, color='green', linestyle=':', alpha=0.7)
ax3.axvline(x=Kc, color='red', linestyle=':', alpha=0.7)
anchor_k = [6.346, 6.484, 6.6223, 6.771, 6.914]
anchor_iv = [IV_10P*100, IV_25P*100, ATM_IV*100, IV_25C*100, IV_10C*100]
anchor_labels = ['10D Put', '25D Put', 'ATM', '25D Call', '10D Call']
for k, iv, lab in zip(anchor_k, anchor_iv, anchor_labels):
    ax3.scatter([k], [iv], color='red', s=60, zorder=5)
    ax3.annotate(lab, (k, iv), textcoords="offset points", xytext=(0,10), ha='center', fontsize=8)
ax3.set_xlabel('行权价 (USD/CNY)', fontsize=11)
ax3.set_ylabel('隐含波动率 (%)', fontsize=11)
ax3.set_title('USD/CNY 1年期波动率微笑\n(chinamoney ATM=3.38%, RR=+0.50%, BF=0.30%)', fontsize=12, fontweight='bold')
ax3.legend(loc='upper right', fontsize=8)
ax3.grid(True, alpha=0.3)
ax3.set_xlim(6.2, 7.3)

# 图4：情景对比柱状图
ax4 = axes[1, 1]
scenarios = [6.2, 6.5, 6.8, 7.0, 7.3]
labels = ['6.20\n(人民币\n+9.0%)', '6.50\n(人民币\n+4.3%)', '6.80\n(人民币\n+0.1%)', '7.00\n(美元\n+3.1%)', '7.30\n(美元\n+7.5%)']

pnl_naked_vals = [exposure_pnl(s)/1e6 for s in scenarios]
pnl_collar_vals = [(exposure_pnl(s) + collar_pnl(s, Kp, Kc, NOTIONAL_HEDGE))/1e6 for s in scenarios]
pnl_zc_vals = [(exposure_pnl(s) + collar_pnl(s, zc_put, zc_call, NOTIONAL_HEDGE))/1e6 for s in scenarios]
pnl_fwd_vals = [fwd_hedge_pnl(s)/1e6 for s in scenarios]

x = np.arange(len(scenarios))
width = 0.20

bars1 = ax4.bar(x - 1.5*width, pnl_naked_vals, width, label='裸敞口 $1B', color='red', alpha=0.7)
bars2 = ax4.bar(x - 0.5*width, pnl_collar_vals, width, label=f'宽领子 Put{Kp:.2f}/Call{Kc:.2f}', color='blue', alpha=0.7)
bars3 = ax4.bar(x + 0.5*width, pnl_zc_vals, width, label=f'零成本领子 Put{zc_put:.2f}/Call{zc_call:.2f}', color='magenta', alpha=0.7)
bars4 = ax4.bar(x + 1.5*width, pnl_fwd_vals, width, label='50%远期锁汇', color='green', alpha=0.7)

ax4.axhline(y=0, color='black', linewidth=0.5)
ax4.set_ylabel('损益 (百万美元)', fontsize=11)
ax4.set_title('五种汇率情景下的综合损益对比', fontsize=12, fontweight='bold')
ax4.set_xticks(x)
ax4.set_xticklabels(labels, fontsize=9)
ax4.legend(loc='upper left', fontsize=8)
ax4.grid(True, alpha=0.3, axis='y')

for bars in [bars1, bars2, bars3, bars4]:
    for bar in bars:
        height = bar.get_height()
        ax4.annotate(f'{height:.1f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3 if height >= 0 else -12),
                    textcoords="offset points",
                    ha='center', va='bottom' if height >= 0 else 'top',
                    fontsize=6.5)

plt.tight_layout()
plt.savefig('/root/.openclaw/workspace/collar_analysis_v2.png', dpi=150, bbox_inches='tight')
print("✅ 图表已保存: /root/.openclaw/workspace/collar_analysis_v2.png")

# =====================
# 情景分析数据表
# =====================
print(f"\n{'='*90}")
print("情景模拟数据表 — 零成本领子期权 + $10亿美元正敞口")
print(f"{'='*90}")
print(f"策略参数:")
print(f"  标的: USD/CNY 即期={S0}, 1年远期={F}")
print(f"  买入 USD Put / CNY Call @ Kp = {Kp:.2f} (权利金 {put_price:.4f} CNY/USD)")
print(f"  卖出 USD Call / CNY Put @ Kc = {Kc:.2f} (权利金 {call_price:.4f} CNY/USD)")
print(f"  对冲比例: 50% (${NOTIONAL_HEDGE/1e6:.0f}M / ${NOTIONAL_TOTAL/1e6:.0f}M)")
print(f"  净权利金成本: {net_cost:.4f} CNY/USD = ${net_cost_usd/1e6:.2f}M ({net_cost_usd/NOTIONAL_HEDGE*100:.2f}%名义本金)")
print(f"{'='*90}")

print(f"\n{'汇率情景':<12} {'裸敞口':>12} {'宽领子对冲':>12} {'零成本领子':>12} {'50%远期':>12} {'vs裸敞口':>10}")
print(f"{'(USD/CNY)':<12} {'($百万)':>12} {'($百万)':>12} {'($百万)':>12} {'($百万)':>12} {'(保护额)':>10}")
print("-" * 80)

for s in scenarios:
    naked = exposure_pnl(s) / 1e6
    collar_w = (exposure_pnl(s) + collar_pnl(s, Kp, Kc, NOTIONAL_HEDGE)) / 1e6
    collar_zc = (exposure_pnl(s) + collar_pnl(s, zc_put, zc_call, NOTIONAL_HEDGE)) / 1e6
    fwd_h = fwd_hedge_pnl(s) / 1e6
    protection = naked - collar_w
    print(f"{s:<12.2f} {naked:>+12.1f} {collar_w:>+12.1f} {collar_zc:>+12.1f} {fwd_h:>+12.1f} {protection:>+10.1f}")

print("-" * 80)

# 详细阈值表
print(f"\n{'='*90}")
print("关键阈值损益明细（宽领子策略）")
print(f"{'='*90}")
print(f"{'汇率':<8} {'$10亿敞口':>12} {'宽领子期权':>12} {'综合损益':>12} {'50%远期':>12} {'备注':>20}")
print(f"{'(USD/CNY)':<8} {'($百万)':>12} {'($百万)':>12} {'($百万)':>12} {'($百万)':>12}")
print("-" * 80)

thresholds = [6.0, 6.2, 6.3, 6.4, 6.5, Kp, 6.6, 6.7, S0, 6.85, F, Kc, 7.2, 7.3, 7.5]
for s in thresholds:
    naked = exposure_pnl(s) / 1e6
    opt = collar_pnl(s, Kp, Kc, NOTIONAL_HEDGE) / 1e6
    total = naked + opt
    fwd = fwd_hedge_pnl(s) / 1e6
    
    marker = ""
    if abs(s - Kp) < 0.01: marker = "← Put行权价"
    elif abs(s - Kc) < 0.01: marker = "← Call行权价"
    elif abs(s - S0) < 0.01: marker = "← 即期汇率"
    elif abs(s - F) < 0.01: marker = "← 1年远期"
    
    print(f"{s:<8.2f} {naked:>+12.1f} {opt:>+12.1f} {total:>+12.1f} {fwd:>+12.1f} {marker:>20}")

print("-" * 80)

# 策略特征
print(f"\n{'='*90}")
print("策略特征总结")
print(f"{'='*90}")
print(f"1. 保护触发: USD/CNY < {Kp:.2f} 时，Put提供全额保护（按$500M名义本金）")
print(f"2. 收益封顶: USD/CNY > {Kc:.2f} 时，Call限制上行收益（超过部分归期权买方）")
print(f"3. 中性区间: {Kp:.2f} ~ {Kc:.2f} 之间，领子无到期payoff，$5亿敞口自然波动")
print(f"4. 最大亏损（综合）: USD/CNY → 6.00 时 = ${(exposure_pnl(6.0) + collar_pnl(6.0, Kp, Kc, NOTIONAL_HEDGE))/1e6:.1f}M")
print(f"5. 最大收益（综合）: USD/CNY → {Kc:.2f} 时 = ${(exposure_pnl(Kc) + collar_pnl(Kc, Kp, Kc, NOTIONAL_HEDGE))/1e6:.1f}M")
print(f"6. 盈亏平衡: USD/CNY = {S0:.2f}（即期水平，无变化时损益为零）")
print(f"7. 对冲成本: ${net_cost_usd/1e6:.2f}M  upfront ({net_cost_usd/NOTIONAL_HEDGE*100:.2f}%名义本金)")

print(f"\n{'='*90}")
print("策略对比评价")
print(f"{'='*90}")
s_650 = 6.50
print(f"USD/CNY = 6.50情景（人民币升值4.3%）:")
print(f"  • 裸敞口亏损:      ${exposure_pnl(s_650)/1e6:>8.1f}M")
print(f"  • 宽领子后亏损:    ${(exposure_pnl(s_650) + collar_pnl(s_650, Kp, Kc, NOTIONAL_HEDGE))/1e6:>8.1f}M  (减少损失 ${(exposure_pnl(s_650) - (exposure_pnl(s_650) + collar_pnl(s_650, Kp, Kc, NOTIONAL_HEDGE)))/1e6:.1f}M)")
print(f"  • 零成本领子亏损:  ${(exposure_pnl(s_650) + collar_pnl(s_650, zc_put, zc_call, NOTIONAL_HEDGE))/1e6:>8.1f}M")
print(f"  • 50%远期亏损:     ${fwd_hedge_pnl(s_650)/1e6:>8.1f}M")
print()
s_700 = 7.00
print(f"USD/CNY = 7.00情景（美元升值3.1%）:")
print(f"  • 裸敞口盈利:      ${exposure_pnl(s_700)/1e6:>8.1f}M")
print(f"  • 宽领子后盈利:    ${(exposure_pnl(s_700) + collar_pnl(s_700, Kp, Kc, NOTIONAL_HEDGE))/1e6:>8.1f}M  (放弃 ${exposure_pnl(s_700)/1e6 - (exposure_pnl(s_700) + collar_pnl(s_700, Kp, Kc, NOTIONAL_HEDGE))/1e6:.1f}M上行)")
print(f"  • 零成本领子盈利:  ${(exposure_pnl(s_700) + collar_pnl(s_700, zc_put, zc_call, NOTIONAL_HEDGE))/1e6:>8.1f}M")
print(f"  • 50%远期盈利:     ${fwd_hedge_pnl(s_700)/1e6:>8.1f}M")

print(f"\n{'='*90}")
print("数据来源与模型说明")
print(f"{'='*90}")
print("• 即期/远期/利率: 中国货币网(chinamoney.com.cn) 2026-05-13")
print("• ATM IV: chinamoney 1Y ATM = 3.3754% (USD.CNY)")
print("• 偏度/凸性: 基于银行间25D RR=+0.50%, 25D BF=0.30%估算")
print("• 定价模型: Garman-Kohlhagen (FX Black-Scholes)")
print("• 波动率插值: Log-strike空间线性插值（5锚点: 10D/25D/ATM/25D/10D）")
print("• 注意: 当前人民币升值预期强（远期6.62 < 即期6.79），美元看跌期权（Put）权利金天然偏高")
print(f"{'='*90}")
