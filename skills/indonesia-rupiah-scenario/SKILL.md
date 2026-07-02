---
name: indonesia-rupiah-scenario
description: "Generate professional monthly scenario analysis reports for USD/IDR (Indonesian Rupiah) with a 5-layer analytical framework. Use when: (1) the user asks for 印尼盾月度报告 or 印尼盾情景分析 or IDR scenario or 印尼市场月度分析, (2) generating monthly reports for Indonesian Rupiah exposure management, (3) analyzing USD/IDR trends, risk factors, or hedging strategies for Indonesia-based operations, (4) any request involving Indonesia currency risk, Danantara policy impact, or BI Rate decisions, (5) updating or modifying the Indonesia Rupiah monthly scenario report template or framework."
---

# Indonesia Rupiah Monthly Scenario Analysis Report

## Overview

This skill generates a professional, investment-grade monthly scenario analysis report for USD/IDR (Indonesian Rupiah). The report follows a **5-layer analytical framework** designed for corporate treasury and FX risk management.

## The 5-Layer Framework (V3 Technical Refactored Edition)

Each report MUST contain exactly these 5 layers in this order:

| Layer | Name | Content | Purpose |
|-------|------|---------|---------|
| 1 | Core Drivers & Breakpoint Diagnosis | Factor analysis with self-challenge logic | Expose contradictions, not conclusions |
| 2 | External Market Voices | Institutions / Central Bank / Economists | Capture disagreement as signal |
| 3 | Scenario Analysis (USD/IDR) | Optimistic / Base / Pessimistic scenarios | Map probabilities to price paths |
| 4 | Pure Technical Analysis | Vol surface, skew, Bollinger, momentum | Independent technical layer |
| 5 | Hedging Recommendations | Scenario-matched instruments | Actionable, cost-aware |

### Key Principles

1. **No indirect currency assumptions**: All scenarios directly reference USD/IDR, not IDR/CNY or other cross rates. The "cross-factor fracture" diagnosis (Layer 1) explicitly warns that USD/IDR vs USD/CNY correlations break in extreme scenarios.

2. **Self-challenge logic**: Every factor must include: (a) model assumption, (b) counter-logic challenge, (c) historical failure case, (d) repricing threshold, (e) current verdict.

3. **Divergence as signal**: When Layer 1 quantitative paths diverge from Layer 2 institutional views, treat the gap itself as a risk signal. Never resolve the contradiction—preserve it.

4. **Technical independence**: Layer 4 must be readable and analyzable independently of Layer 1. Cross-validation between layers is welcome, but Layer 4 should not depend on Layer 1 conclusions.

5. **Inference transparency**: Any option market data (25d/10d Risk Reversal, IV historical percentiles) that cannot be obtained from direct bank OTC quotes must be clearly labeled as "inferred" with methodology stated.

## Report Structure Details

### Layer 1: Core Drivers & Breakpoint Diagnosis

**Three-factor model** (adjustable weights):
- Interest rate differential factor
- Current account resilience factor
- Risk premium factor (CDS, capital flows, policy uncertainty)

**Required sub-sections**:
1.1 Three-factor status matrix (objective readings)
1.2 Factor-by-factor breakpoint diagnosis (self-challenge format)
1.3 Cross-factor fracture diagnosis (correlation risk)
1.4 Factor model self-check checklist
1.5 Quantitative aggregation path (model-encoded, not forecast)

### Layer 2: External Market Voices

Minimum 4 voices required:
- 1 major investment bank (MUFG, GS, JPM, etc.)
- 1 central bank or monetary authority statement
- 1 economist or local bank analyst
- 1 quantitative/statistical model (CoinCodex, Longforecast, etc.)

**Required divergence analysis**: Highlight the gap between bullish and bearish camps, measure in basis points or percentage points.

### Layer 3: Scenario Analysis

Three scenarios with explicit probability weights:
- Optimistic (typically 15%)
- Base (typically 55%)
- Pessimistic (typically 30%)

Each scenario box must contain:
- Trigger conditions
- USD/IDR target range
- Impact on corporate operations (customizable to user's company)
- Why this probability is justified

### Layer 4: Pure Technical Analysis

**Four modules** (all mandatory):

4.1 **Volatility Surface**: 25d vs 10d Risk Reversal
- Define: RR = IV(25d Call) − IV(25d Put)
- Explain: Call = buy USD/sell IDR; Put = sell USD/buy IDR
- Report 25d RR, 10d RR, and 10d-25d spread
- Historical comparison anchors (2013 Taper Tantrum, 2018 Turkey contagion)

4.2 **Implied Volatility Historical Percentiles**
- Table: 1-day / 1-week / 1-month / 3-month / 1-year
- GARCH model parameters (α, β) if available
- Status classification: normal / elevated / extreme

4.3 **Bollinger Bands & Momentum**
- Current price, 20-day SMA, upper/lower bands, bandwidth status
- RSI(14), 50-day SMA, 200-day SMA
- Trend classification, squeeze/expansion status

4.4 **Integrated Technical Forecast**
- Short-term (1-4 weeks) and medium-term (1-6 months) predictions
- Key monitoring indicators (divergence signals, band contraction, skew convergence)
- Cross-validation with Layer 1

### Layer 5: Hedging Recommendations

Scenario-matched instrument table:
| Scenario | Instrument | Execution Points | Cost |
|----------|-----------|-----------------|------|

**Technical-to-hedging transmission**: Layer 4 insights must inform Layer 5 (e.g., when 25d RR > +5, Collar is preferred over outright Call; when RSI > 70, timing entry for better vol).

## Output Format

- **Format**: Single HTML file, responsive, professional styling
- **Style**: Dark blue (#1a1a2e) header, red accent (#e94560), green/yellow/red cell backgrounds
- **Compatibility**: Standard HTML tables, no flexbox/grid, no gradients, no emoji
- **Quality rating**: 4-star or 5-star badge in header (4-star if technical data contains inferred components)
- **Disclaimer**: Mandatory footer with data source table and inference limitation note

## Data Source Priority

| Data Type | Primary Source | Fallback | Note |
|-----------|---------------|----------|------|
| USD/IDR spot | Reuters, Bloomberg, 中新社 | Investing.com | Daily close |
| BI Rate | 印尼央行官网, 新浪财经 | — | Monthly meeting |
| 5Y CDS | WorldGovernmentBonds | Bloomberg | Daily |
| Quantitative path | Longforecast.com, CoinCodex | — | Daily update |
| GARCH vol | NYU Stern V-Lab | — | Model output |
| Option skew | Inferred from EM typical pattern | Direct broker quote | Must label as inferred |
| Bollinger/RSI | Investing.com, Barchart | TradingView | Daily |
| Trade data | BPS (印尼统计局), 海关总署 | — | Monthly, lagging |
| Institutional views | MUFG Research, 央行声明 | 财联社, Reuters | Event-driven |

## Quality Standards

- **Data freshness**: All market data must be T or T-1. Monthly data (trade, CPI) can be lagging but must be labeled.
- **Cross-verification**: Key prices (USD/IDR, CDS) must be verified from 2+ independent sources.
- **Inference labeling**: Any option market data not from direct broker quotes must be labeled "inferred" with methodology.
- **Year check**: Always confirm current year (2026, not 2025). Use `date` command before data collection.

## Bundled Resources

- **references/framework.md**: Complete 5-layer framework documentation with detailed methodology for each layer, factor weight adjustment rules, and historical case studies (2013 Taper Tantrum, 2018 Turkey contagion, 2016 Jokowi reform).
- **assets/template.html**: Full HTML report template with all CSS styling, table structures, and placeholder sections. Copy this file and replace content for new reports.

## Workflow

1. Read `references/framework.md` for detailed layer methodology
2. Copy `assets/template.html` to new report file
3. Collect data following the priority table above
4. Execute `date` command to confirm current year/month/day
5. Fill each layer following the structure in this SKILL.md
6. Cross-validate Layer 1 and Layer 4 conclusions
7. Add quality rating and disclaimer
8. Save as `reports/indonesia_monthly_scenario_YYYYMM.html`
