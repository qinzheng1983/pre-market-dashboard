# 5-Layer Framework Reference (V3 Technical Refactored Edition)

## Layer 1: Core Drivers & Breakpoint Diagnosis — Detailed Methodology

### Three-Factor Model Architecture

The model evaluates three macro drivers. Their weights are subjective and must be justified in the report.

**Factor 1: Interest Rate Differential**
- Formula: BI Rate − Fed Upper Bound (or relevant comparison rate)
- Normal state: Positive differential attracts carry trade inflows
- Failure state: Differential approaches zero or inverts; market stops pricing rates
- Historical failure: 2013 Taper Tantrum (BI hiked 175bp, IDR still fell 20%)
- Threshold: When 5Y CDS > 100bp, rate factor becomes irrelevant regardless of differential magnitude

**Factor 2: Current Account Resilience**
- Key metrics: Monthly trade balance, import/export growth rates, terms of trade
- Normal state: Persistent surplus provides fundamental support
- Failure state: Surplus narrows rapidly; market switches from "stock" to "flow" analysis
- Historical failure: Indonesia 2011→2013 (surplus +0.2% GDP to deficit −3.2%, IDR −26%)
- Threshold: Monthly surplus < $500M for 2 consecutive months, or any monthly deficit

**Factor 3: Risk Premium**
- Key metrics: 5Y CDS, capital flow data, policy uncertainty index, FX intervention frequency
- Normal state: CDS < 75bp, stable capital flows, predictable policy
- Dominant state: CDS 80-120bp, market prices only risk
- Crisis state: CDS > 150bp, rating downgrade concerns emerge
- Historical failure: Rare; risk premium is usually the last factor to break in EM
- Threshold: CDS 100bp = panic acceleration; CDS 75bp = sentiment repair

### Breakpoint Diagnosis Format

Each factor analysis must follow this 5-part structure:

1. **Model Assumption**: What the textbook says (e.g., "Rate hike → capital inflow → currency appreciation")
2. **Counter-Logic Challenge**: Why the textbook might be wrong now (e.g., "BI hiked 50bp but IDR fell to record low because market prices fiscal risk, not rates")
3. **Historical Failure Case**: When and where this assumption failed before, with quantitative outcomes
4. **Repricing Threshold**: The specific data level that would cause the market to flip its pricing (e.g., "CDS < 80bp AND BI Rate > Fed upper bound")
5. **Current Verdict**: Color-coded conclusion (断裂/脆弱/主导) with weight assignment

### Cross-Factor Fracture Diagnosis

**Mandatory analysis**: USD/IDR vs USD/CNY correlation assumption
- Normal state: 60-80% correlation, indirect hedging via USD/CNY forwards works
- Fracture state: < 30% correlation in extreme scenarios
- Why it fractures: USD appreciation against IDR is amplified by Indonesia-specific risk premium; USD appreciation against CNY is suppressed by PBOC counter-cyclical factor
- Stress test: If USD/IDR +20% and USD/CNY +2%, IDR/CNY depreciates 25.7% — all indirect hedging fails
- Threshold: USD/CNY middle rate > 7.0 triggers further divergence via PBOC intervention

### Quantitative Aggregation Path Methodology

**Not a forecast. A model-encoded path.**
- State the current factor weights explicitly (e.g., "Risk premium 80%, Current account 20%, Rates 0%")
- Use Longforecast.com + CoinCodex as baseline technical inputs
- Present monthly path from current month to year-end
- Label clearly: "If current factor weight structure remains unchanged, technical models encode this path"
- List key limitation: Policy or institutional突变 causes instant path invalidation

## Layer 2: External Market Voices — Sourcing Guidelines

**Voice Types and Minimum Requirements**:

| Type | Minimum | Examples | Update Frequency |
|------|---------|----------|-----------------|
| Major IB | 1 | MUFG, Goldman Sachs, JPMorgan, Citi | Event-driven |
| Central Bank | 1 | BI Governor statement, policy meeting minutes | Monthly |
| Local Economist | 1 | Permata Bank, Mandiri Sekuritas, local university | Quarterly |
| Quant Model | 1 | CoinCodex, Longforecast, Investing.com | Daily |
| Contrarian | 1 (optional) | Independent analyst with bearish view | Event-driven |

**Divergence Analysis Requirements**:
- Measure the gap between most bullish and most bearish camps in pips or percentage
- Identify what the gap represents (e.g., "valuation model vs risk premium pricing")
- Extract actionable insight: "If bull case is right, X happens; if bear case is right, Y happens; structure exposure for both"

## Layer 3: Scenario Analysis — Probability Framework

### Scenario Box Structure

Each scenario must be a self-contained box with:
- **Probability badge** (top-right, color-coded)
- **Title** (descriptive, not just "Optimistic")
- **Trigger conditions** table (4-6 bullet conditions, ALL required for scenario to materialize)
- **USD/IDR target range** (with time horizon)
- **Corporate impact** (customized to user's industry — default is battery materials / nickel processing)
- **Probability justification** (why this weight, referencing Layer 1 factor weights)

### Default Probability Distribution (Adjustable)

| Scenario | Default | Adjustment Rule |
|----------|---------|-----------------|
| Optimistic | 15% | Increase if CDS < 80bp sustained for 2 weeks |
| Base | 55% | Increase if no new catalyst for 1 month |
| Pessimistic | 30% | Increase if CDS > 100bp or policy shock |

### Probability Justification Logic

The probabilities must be explicitly linked to Layer 1:
- "Base case 55% reflects risk premium factor's 80% weight and its high stickiness"
- "Pessimistic 30% reflects proximity to CDS 100bp threshold and Danantara execution uncertainty"
- "Optimistic 15% requires 4 simultaneous conditions, each with low individual probability"

## Layer 4: Pure Technical Analysis — Module Specifications

### Module 4.1: Volatility Surface (25d vs 10d Risk Reversal)

**Definition clarity**:
- In USD/IDR market: Call = right to buy USD/sell IDR = bullish USD / bearish IDR
- Put = right to sell USD/buy IDR = bearish USD / bullish IDR
- Risk Reversal = IV(25d Call) − IV(25d Put)
- Positive RR = Call more expensive = market fears IDR depreciation
- Negative RR = Put more expensive = market fears IDR appreciation

**Required outputs**:
| Metric | Reporting Format | Typical Range (Stress) |
|--------|-----------------|----------------------|
| 25d RR | +X.X to +Y.Y vol pts | +3 to +6 (normal crisis), +6 to +9 (extreme) |
| 10d RR | +X.X to +Y.Y vol pts | +5 to +8 (normal crisis), +8 to +12 (extreme) |
| 10d-25d spread | +X.X to +Y.Y vol pts | +1.5 to +3 (steep skew), <+1 (flat) |

**Historical anchors**:
- 2013 Taper Tantrum peak: 25d RR +6.2 vol pts
- 2018 Turkey contagion peak: 25d RR +8.5 vol pts
- 2016 Jokowi reform trough: 25d RR −1.5 vol pts (IDR bullish)

**Inference methodology** (when direct OTC quotes unavailable):
1. Start with GARCH realized vol forecast (e.g., 15.6% annualized)
2. Add typical EM FX risk premium spread (realized vol + 2-4% = implied vol baseline)
3. Apply EM depreciation stress skew multiplier (25d RR +3 to +5 for current stress level)
4. Apply tail risk premium (10d RR = 25d RR + 1.5 to 2.5)
5. Validate against: (a) CDS level, (b) spot price momentum, (c) historical analogues

**Mandatory disclaimer**: "Inferred from [methodology]. Not direct interbank OTC quote. Confirm with market maker before trading."

### Module 4.2: Implied Volatility Historical Percentile

**Table structure**:
| Tenor | Realized Vol (GARCH) | Implied Vol (Inferred) | Historical Percentile | Status |
|-------|---------------------|------------------------|----------------------|--------|
| 1D | X.XX% | ~XX.X% | XX-XX% | Normal/High/Extreme |
| 1W | X.XX% | ~XX.X% | XX-XX% | Normal/High/Extreme |
| 1M | X.XX% | ~XX.X% | XX-XX% | Normal/High/Extreme |
| 3M | — | ~XX.X-XX.X% | XX-XX% | Normal/High/Extreme |
| 1Y | — | ~XX.X-XX.X% | XX-XX% | Normal/High/Extreme |

**GARCH interpretation**:
- Report α (ARCH term) and β (GARCH term) if available
- High β (>0.9) = volatility persistence; shocks decay slowly
- High α (>0.1) = shock sensitivity; news impact is large
- Typical EM FX: β ≈ 0.90-0.95, α ≈ 0.05-0.10

**Historical context bands**:
- <50% percentile: Normal period (e.g., 2019-2021)
- 50-75%: Elevated (e.g., 2022 Fed hiking cycle)
- 75-90%: High stress (e.g., 2023 regional banking crisis)
- >90%: Crisis (e.g., 2013 Taper Tantrum, 1998 Asian Crisis)

### Module 4.3: Bollinger Bands & Momentum

**Required indicators**:

| Indicator | Calculation | Current Read | Thresholds |
|-----------|------------|--------------|------------|
| Spot Price | — | X,XXX | — |
| 20-day SMA | 20-day mean | ~XX,XXX | — |
| Upper Band (+2σ) | SMA + 2×σ | ~XX,XXX | Breakout = overbought |
| Lower Band (−2σ) | SMA − 2×σ | ~XX,XXX | Breakdown = oversold |
| Bandwidth Status | (Upper−Lower)/SMA | Squeeze/Expansion/Normal | Squeeze < 5% = pre-breakout |
| RSI(14) | 0-100 momentum | XX.X | >70 overbought, <30 oversold |
| 50-day SMA | 50-day mean | XX,XXX | Support/resistance |
| 200-day SMA | 200-day mean | XX,XXX | Long-term trend |

**Bollinger-specific patterns**:
- **Squeeze**: Bands narrow, low volatility → "calm before storm"
- **Expansion**: Bands widen, high volatility → trend confirmation or reversal
- **Walking the band**: Price rides upper/lower band → strong trend, don't fade
- **Reversal**: Price breaks band but closes back inside → exhaustion signal

**Trend classification**:
- Strong uptrend: Price > 50 SMA > 200 SMA, RSI 50-80
- Weak uptrend: Price > 50 SMA but < 200 SMA, RSI 50-70
- Range: Price between bands, RSI 40-60, low bandwidth
- Downtrend: Price < 50 SMA < 200 SMA, RSI 20-50

### Module 4.4: Integrated Technical Forecast

**Short-term (1-4 weeks)**:
- Based on momentum, RSI, band position
- Key question: "Is the trend accelerating, decelerating, or reversing?"
- Target range: ±XXX pips from current
- Confidence: Low-Medium (technical patterns have short half-lives)

**Medium-term (1-6 months)**:
- Based on trend structure, SMA alignment, vol mean reversion
- Key question: "Will the current factor regime persist long enough for technical targets to be reached?"
- Target range: ±XXXX pips from current
- Confidence: Low (fundamental regime shifts override technicals)

**Cross-validation checklist** (Layer 4 vs Layer 1):
- [ ] Technical trend direction matches dominant factor direction?
- [ ] Volatility level consistent with risk premium factor weight?
- [ ] Skew direction consistent with market positioning narrative?
- [ ] If contradiction found, highlight it as "divergence signal"

**Key monitoring indicators** (pure technical, no fundamentals):
1. RSI divergence (price makes new high, RSI makes lower high)
2. Bollinger band contraction after expansion (trend exhaustion)
3. 25d RR convergence from extreme to moderate (sentiment normalization)
4. 50-day SMA cross (price crosses below = trend change warning)

## Layer 5: Hedging Recommendations — Technical-to-Action Transmission

### Scenario-Instrument Mapping

| Scenario | Primary Instrument | Secondary | Rationale |
|----------|-----------------|-----------|-----------|
| Optimistic | Natural hedge, reduce coverage | Spot monitoring | Don't overpay for protection when risk is low |
| Base | Collar (risk reversal) | Forward cover | Balance cost and protection; sell OTM put to fund OTM call |
| Pessimistic | Deep OTM call + full forward | Emergency liquidity reserve | Maximum protection; cost is secondary |

### Technical Input to Hedging Decision

When Layer 4 provides specific readings, they must inform Layer 5:

**25d RR > +5 (expensive calls)**:
- Don't buy outright calls — market is already pricing extreme fear
- Prefer: Collar (sell put to offset call premium), or wait for technical correction to enter
- If 10d RR > +7.5: Even selling put is dangerous; consider full forward instead of options

**RSI > 70 (overbought)**:
- Timing opportunity: Wait for pullback to SMA or lower band to enter protection
- Risk: Trend may continue without pullback; FOMO hedging vs. patient entry tradeoff

**IV > 85% percentile (expensive vol)**:
- Don't buy options when vol is at peak unless you believe vol will go higher
- Prefer: Forwards (no vol exposure), or structures that sell vol (seagull, range accrual)
- Exception: If you believe IV is going to 95%+ (crisis escalation), buy before it gets worse

**Band squeeze → expansion (breakout confirmed)**:
- If breakout is in direction of your risk (IDR depreciation), increase hedge ratio immediately
- If breakout is against your risk (IDR appreciation), reduce hedge ratio cautiously

### Cost Estimation Guidelines

| Cost Level | Description | Annualized Cost Range |
|-----------|-------------|----------------------|
| Low | Natural hedge, no premium | 0-0.5% |
| Medium | Collar, near-zero cost | 0.5-2.0% |
| High | Full forward, deep OTM options | 2.0-5.0% |
| Very High | Emergency hedge in crisis | 5.0-10.0%+ |

## Historical Case Studies

### 2013 Taper Tantrum (Factor Break Template)
- **Rates**: BI hiked 175bp → rates factor FAILED
- **Current account**: Surplus turned to deficit in 2 quarters → current account factor FAILED
- **Risk premium**: CDS spiked from 120bp to 220bp → risk premium factor DOMINATED
- **Outcome**: IDR fell 20% in 3 months despite aggressive hiking
- **Lesson**: When multiple factors break simultaneously, the dominant factor (risk premium) drives everything. Do not expect mean reversion.

### 2016 Jokowi Reform (Factor Recovery Template)
- **Rates**: BI cut rates 25bp → rates factor not driving
- **Current account**: Deficit narrowed to −1.7% GDP → current account factor RECOVERING
- **Risk premium**: CDS fell from 150bp to 80bp → risk premium factor RETREATING
- **Outcome**: IDR appreciated 12% in 12 months despite rate cuts
- **Lesson**: Risk premium is the last factor to break, but also the first to recover when institutional credibility returns.

### 2018 Turkey Contagion (EM Stress Template)
- **Trigger**: Turkey Lira crisis, EM risk-off
- **Indonesia impact**: CDS rose from 100bp to 180bp, IDR fell 10% in 2 months
- **Key feature**: Indonesia fundamentals were fine, but risk premium factor overwhelmed everything
- **Lesson**: EM currencies are "guilty by association" in risk-off. Even good fundamentals don't protect against contagion-driven risk premium spikes.

## Adjustment Rules for Future Months

### When to Adjust Factor Weights

| Condition | Adjustment | Rationale |
|-----------|-----------|-----------|
| CDS > 100bp for 5+ days | Risk premium weight → 90% | Market in panic mode |
| CDS < 75bp sustained | Risk premium weight → 60%, current account → 30% | Risk normalization |
| BI rate > 6.0% AND CDS < 80bp | Rates factor weight → 20% | Rates factor reactivates |
| Monthly trade deficit for 2 months | Current account weight → 10% | Fundamental support gone |
| Danantara execution chaos | Add "policy uncertainty" as 4th factor | New structural driver |

### When to Adjust Scenario Probabilities

| Trigger | Optimistic | Base | Pessimistic |
|---------|-----------|------|-------------|
| CDS crosses 100bp | −5% | −10% | +15% |
| CDS falls below 75bp | +10% | +5% | −15% |
| BI surprises +75bp or more | +5% | +5% | −10% |
| Trade surplus > $2B/month | +5% | +5% | −10% |
| Danantara major announcement | Re-evaluate all | Re-evaluate all | Re-evaluate all |
