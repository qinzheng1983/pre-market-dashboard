import numpy as np
import math
from scipy.stats import norm
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Market Data (chinamoney.com.cn 2026-05-13)
S0 = 6.7905
T = 1.0
r_CNY = 0.014547
r_USD = 0.039494
F = 6.6223

# Vol Surface
ATM_IV = 0.033754
RR_25D = 0.0050
BF_25D = 0.0030
RR_10D = 0.0100
BF_10D = 0.0045

IV_25C = ATM_IV + BF_25D + 0.5 * RR_25D
IV_25P = ATM_IV + BF_25D - 0.5 * RR_25D
IV_10C = ATM_IV + BF_10D + 0.5 * RR_10D
IV_10P = ATM_IV + BF_10D - 0.5 * RR_10D

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

# Zero-cost collar strikes
Kp = 6.55
Kc = 6.722

# Wide collar (recommended)
Kp_w = 6.50
Kc_w = 7.00

put_price_w = fx_put_price(S0, Kp_w, T, r_CNY, r_USD, get_iv_for_strike(Kp_w))
call_price_w = fx_call_price(S0, Kc_w, T, r_CNY, r_USD, get_iv_for_strike(Kc_w))

NOTIONAL_TOTAL = 1_000_000_000
NOTIONAL_HEDGE = 500_000_000
P_CNY = NOTIONAL_TOTAL * S0

def exposure_pnl(S_T):
    return NOTIONAL_TOTAL * (1 - S0 / S_T)

def collar_pnl(S_T, Kp, Kc, notional):
    put_payoff = notional * max(Kp - S_T, 0) / S_T
    call_payoff = -notional * max(S_T - Kc, 0) / S_T
    return put_payoff + call_payoff

def fwd_hedge_pnl(S_T):
    fwd_pnl = NOTIONAL_HEDGE * (F - S_T) / S_T
    unhedged_5b = (NOTIONAL_TOTAL - NOTIONAL_HEDGE) * (1 - S0 / S_T)
    return unhedged_5b + fwd_pnl

S_range = np.linspace(6.0, 7.5, 300)

pnl_naked = np.array([exposure_pnl(s) for s in S_range]) / 1e6
pnl_zc_collar = np.array([exposure_pnl(s) + collar_pnl(s, Kp, Kc, NOTIONAL_HEDGE) for s in S_range]) / 1e6
pnl_wide_collar = np.array([exposure_pnl(s) + collar_pnl(s, Kp_w, Kc_w, NOTIONAL_HEDGE) for s in S_range]) / 1e6
pnl_fwd = np.array([fwd_hedge_pnl(s) for s in S_range]) / 1e6

fig, ax = plt.subplots(figsize=(12, 7))

ax.plot(S_range, pnl_naked, 'r--', linewidth=2.2, label='Naked $1B Exposure')
ax.plot(S_range, pnl_zc_collar, 'm:', linewidth=2.2, label=f'Zero-Cost Collar ($500M) @ Put{Kp:.2f}/Call{Kc:.3f}')
ax.plot(S_range, pnl_wide_collar, 'b-', linewidth=2.5, label=f'Wide Collar ($500M) @ Put{Kp_w:.2f}/Call{Kc_w:.2f}')
ax.plot(S_range, pnl_fwd, 'g-.', linewidth=2, label=f'50% Forward Hedge @ F={F}')

# Reference lines
ax.axvline(x=S0, color='gray', linestyle='-', alpha=0.4, linewidth=1)
ax.axvline(x=F, color='orange', linestyle='--', alpha=0.4, linewidth=1)
ax.axhline(y=0, color='black', linewidth=0.5)

# Zone shading
ax.axvspan(6.0, Kp, alpha=0.08, color='green', label='Protection Zone')
ax.axvspan(Kc, 7.5, alpha=0.08, color='red')

# Annotate strikes
ax.annotate(f'Spot\n{S0}', xy=(S0, -10), fontsize=9, color='gray', ha='center')
ax.annotate(f'1Y Fwd\n{F}', xy=(F, -20), fontsize=9, color='orange', ha='center')
ax.annotate(f'Put\n{Kp:.2f}', xy=(Kp, 15), fontsize=9, color='darkgreen', ha='center', fontweight='bold')
ax.annotate(f'Call\n{Kc:.3f}', xy=(Kc, 15), fontsize=9, color='darkred', ha='center', fontweight='bold')

# Scenario markers
scenarios = [6.2, 6.5, 6.8, 7.0, 7.3]
colors = ['red', 'orange', 'green', 'blue', 'purple']
for s, c in zip(scenarios, colors):
    p = (exposure_pnl(s) + collar_pnl(s, Kp, Kc, NOTIONAL_HEDGE)) / 1e6
    ax.scatter([s], [p], color=c, s=80, zorder=5, edgecolors='black', linewidths=1)
    ax.annotate(f'{s}\n${p:.1f}M', xy=(s, p), textcoords="offset points", xytext=(0, 12 if p > 0 else -18),
                ha='center', fontsize=8, fontweight='bold', color=c)

ax.set_xlabel('USD/CNY at Expiry', fontsize=12)
ax.set_ylabel('Total P&L (USD Million)', fontsize=12)
ax.set_title('USD/CNY Collar + $1B Long USD Exposure\nZero-Cost vs Wide Collar vs Forward Hedge (50% Ratio)', fontsize=13, fontweight='bold')
ax.legend(loc='upper left', fontsize=10, framealpha=0.9)
ax.grid(True, alpha=0.3)
ax.set_xlim(6.0, 7.5)
ax.set_ylim(-150, 100)

# Add text box with strategy details
textstr = f'Zero-Cost Collar: Put@{Kp:.2f} / Call@{Kc:.3f}\n' + \
          f'Wide Collar: Put@{Kp_w:.2f} / Call@{Kc_w:.2f} (cost: ${(put_price_w-call_price_w)*NOTIONAL_HEDGE/S0/1e6:.2f}M)\n' + \
          f'Notional: ${NOTIONAL_HEDGE/1e6:.0f}M / ${NOTIONAL_TOTAL/1e6:.0f}M (50%)\n' + \
          f'Market: Spot={S0}, 1Y Fwd={F}, ATM IV={ATM_IV*100:.2f}%'
props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)
ax.text(0.98, 0.25, textstr, transform=ax.transAxes, fontsize=9,
        verticalalignment='top', horizontalalignment='right', bbox=props, family='monospace')

plt.tight_layout()
plt.savefig('/root/.openclaw/workspace/collar_pnl_chart.png', dpi=150, bbox_inches='tight')
print("Chart saved: /root/.openclaw/workspace/collar_pnl_chart.png")

# Print scenario table
print("\n" + "="*90)
print("SCENARIO ANALYSIS TABLE - Zero-Cost Collar + $1B Long USD Exposure")
print("="*90)
print(f"Strategy: Buy Put @ {Kp:.2f}, Sell Call @ {Kc:.3f}, Notional = ${NOTIONAL_HEDGE/1e6:.0f}M (50% of ${NOTIONAL_TOTAL/1e6:.0f}M)")
print(f"Market: Spot={S0}, 1Y Fwd={F}, ATM IV={ATM_IV*100:.4f}%, Date=2026-05-13")
print(f"Net Premium: ~Zero (Put={fx_put_price(S0,Kp,T,r_CNY,r_USD,get_iv_for_strike(Kp)):.4f}, Call={fx_call_price(S0,Kc,T,r_CNY,r_USD,get_iv_for_strike(Kc)):.4f} CNY/USD)")
print("="*90)

print(f"\n{'Scenario':<10} {'Naked':>12} {'Fwd 50%':>12} {'ZC Collar':>12} {'Wide Collar':>12} {'ZC vs Naked':>12}")
print(f"{'(USD/CNY)':<10} {'($M)':>12} {'($M)':>12} {'($M)':>12} {'($M)':>12} {'(Protection)':>12}")
print("-"*80)

for s in scenarios:
    naked = exposure_pnl(s) / 1e6
    fwd = fwd_hedge_pnl(s) / 1e6
    zc = (exposure_pnl(s) + collar_pnl(s, Kp, Kc, NOTIONAL_HEDGE)) / 1e6
    wide = (exposure_pnl(s) + collar_pnl(s, Kp_w, Kc_w, NOTIONAL_HEDGE)) / 1e6
    protection = naked - zc
    print(f"{s:<10.2f} {naked:>+12.1f} {fwd:>+12.1f} {zc:>+12.1f} {wide:>+12.1f} {protection:>+12.1f}")

print("-"*80)

# Additional thresholds
print(f"\n{'='*90}")
print("DETAILED THRESHOLD ANALYSIS (Zero-Cost Collar)")
print(f"{'='*90}")
print(f"{'Rate':<8} {'Naked':>10} {'Collar':>10} {'Combined':>10} {'Fwd 50%':>10} {'Note':>25}")
print(f"{'(USD/CNY)':<8} {'($M)':>10} {'($M)':>10} {'($M)':>10} {'($M)':>10}")
print("-"*75)

thresholds = [6.0, 6.2, 6.3, 6.4, 6.5, Kp, 6.6, 6.7, S0, F, Kc, 7.2, 7.3, 7.5]
for s in thresholds:
    naked = exposure_pnl(s) / 1e6
    opt = collar_pnl(s, Kp, Kc, NOTIONAL_HEDGE) / 1e6
    total = naked + opt
    fwd = fwd_hedge_pnl(s) / 1e6
    note = ""
    if abs(s - Kp) < 0.01: note = "<< Put Strike"
    elif abs(s - Kc) < 0.01: note = "<< Call Strike"
    elif abs(s - S0) < 0.01: note = "<< Spot"
    elif abs(s - F) < 0.01: note = "<< 1Y Forward"
    print(f"{s:<8.2f} {naked:>+10.1f} {opt:>+10.1f} {total:>+10.1f} {fwd:>+10.1f} {note:>25}")

print("-"*75)
print(f"\nKey Metrics:")
print(f"  Break-even (Combined): USD/CNY = {S0:.2f} (no change)")
print(f"  Max Loss (Naked):      USD/CNY=6.00 -> ${exposure_pnl(6.0)/1e6:.1f}M")
print(f"  Max Loss (ZC Collar):  USD/CNY=6.00 -> ${(exposure_pnl(6.0)+collar_pnl(6.0,Kp,Kc,NOTIONAL_HEDGE))/1e6:.1f}M (protected by Put)")
print(f"  Max Gain (ZC Collar):  USD/CNY={Kc:.3f} -> ${(exposure_pnl(Kc)+collar_pnl(Kc,Kp,Kc,NOTIONAL_HEDGE))/1e6:.1f}M (capped by Call)")
print(f"  Protection Range:      USD/CNY < {Kp:.2f} (Put kicks in)")
print(f"  Cap Range:             USD/CNY > {Kc:.3f} (Call caps upside)")
print(f"  Neutral Zone:          {Kp:.2f} ~ {Kc:.3f} (no option payoff at expiry)")
print("="*90)
