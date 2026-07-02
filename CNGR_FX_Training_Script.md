# CNGR FX Risk Management Framework — Training Script

---

## Slide 1: Opening

**Speaker Notes:**

Good morning, everyone. Today we're going to walk through the **CNGR Full-Cycle FX Risk Management Framework** — the schematic you see on the screen.

This is not a theoretical model. This is the actual operating system we use to identify, measure, execute, and report foreign-exchange risk across our global footprint. We operate in five currency corridors — USD/CNY, EUR/CNY, KRW/CNY, IDR/CNY, and JPY/CNY — and this framework is designed to ensure nothing falls through the cracks.

The framework is divided into **three temporal phases**: Ex-Event, In-Event, and Post-Event. Think of it as before the risk crystallizes, while the risk is live, and after the risk has impacted the books. Every box on this diagram represents a workflow, a control point, or a decision gate.

Let's start at the top.

---

## Slide 2: Phase I — Ex-Event: Risk Identification & Strategic Hedging

**Speaker Notes:**

The green section is **Ex-Event Management**. This is where we earn our keep — before the market moves against us. The guiding principle here is: **you cannot hedge what you cannot measure, and you cannot measure what you have not identified.**

### 2.1 Investment & Project-Level Assessment

On the left, we have **Capital Expenditure and Greenfield/Brownfield Project Finance**. Any new factory, any mining investment, any ODI structure — before a single dollar is committed, we run four analyses:

1. **Working Capital Optimization via Inventory/AR/AP Simulation.** We model how inventory cycles, receivable terms, and payable terms in different currencies create natural offsets or compounding exposures. For example, our Indonesian nickel operation has IDR-denominated local costs but USD-denominated export revenues. The payables cycle determines how long that IDR/USD mismatch stays live on the balance sheet.

2. **P&L Sensitivity & Breakeven Analysis.** We stress-test the project IRR under adverse currency scenarios. If IDR depreciates 15%, does the project still breakeven? If KRW strengthens and our Korean base's local costs become more expensive in CNY terms, what happens to the consolidated margin?

3. **Supply Chain & Trade Flow Routing Optimization.** This is where we decide whether to route through Hong Kong, ship directly from Indonesia to Europe, or use our Korean base as a regional hub. Each routing decision changes the currency profile of the transaction.

4. **ODI + Cross-Border Borrowing Routes.** This is critical for CNGR because of our **12-billion-USD equivalent capital-layer exposure** — the RMB-denominated parent borrowing that funds our USD-functional Indonesian subsidiary. When we structure this, we decide: Is it a shareholder loan? Is it an equity injection? Is it a third-party offshore borrowing with parent guarantee? Each has a different FX accounting treatment and hedgeability.

### 2.2 Pre-Budget Risk Management

Moving to the right side of the green section, we have **Pre-Budget Management**. This is where operational finance and treasury intersect.

- **Sales-Purchase-Inventory Simulation Analysis.** We run Monte-Carlo-style simulations on our forward order book. If Tesla places a high-nickel precursor order for Q3, when will the USD receivable hit our books? When will we need to buy the nickel feedstock? What's the gap?

- **Dynamic Liquidity Gap Forecasting.** We maintain a **rolling 3-month horizon** aligned to our average payables term. This is not a static annual budget. This is a living forecast that updates weekly. It tells us exactly when we need USD in Hong Kong, when we need KRW in Seoul, when we need IDR in Jakarta, and when CNY needs to leave China.

- **FX Risk Trigger Identification.** We define quantitative triggers. For example: "If USD/CNY spot trades 500 pips away from the daily fixing for three consecutive days, escalate to the CFO." Or: "If IDR depreciates beyond 16,500 per USD, activate the Indonesia crisis playbook."

### 2.3 Risk-Adjusted Cost of Funding

All of this feeds into one bottom-line number: the **Risk-Adjusted Cost of Funding & All-in Borrowing Rate Assessment.** Before we sign any loan agreement, we don't just look at the coupon. We add the expected FX volatility cost, the basis swap spread, the hedge cost, and the potential CTA hit. That gives us the true economic cost of the capital.

---

## Slide 3: Phase II — In-Event: Risk Measurement, Netting & Execution

**Speaker Notes:**

The blue section is where the rubber meets the road. This is **In-Event Management** — the daily operating rhythm of the treasury function. Three workstreams run in parallel.

### 3.1 Exchange Rate Setting & Publication

This is our internal price-discovery engine. We set four categories of rates every day:

- **Intercompany Transaction Rate Setting.** When our Indonesian subsidiary sells nickel matte to our Korean base, what rate do we use? We use a rolling average of the previous 5-day mid-market rate, updated daily, to avoid intra-day arbitrage and transfer-pricing scrutiny.

- **Commercial Contract Rate Setting.** For external sales — say, a USD-denominated contract with a European customer — we set the budget rate at the time of contract signing, and we track variance against that rate monthly.

- **Borrowing Transfer Pricing Rate.** For that 12-billion-USD capital layer, we have a fixed transfer-pricing rate for internal interest allocation. This determines how much "interest expense" is booked in Jakarta versus Shanghai, and it directly affects the CTA calculation.

- **Budget Rate.** This is the rate the business units use for their quarterly planning. If the budget rate is 6.90 and the spot is 6.76, the business unit thinks they're making more margin than treasury sees. That variance is tracked and explained.

**CTA — Cumulative Translation Adjustment.** This is the equity-accounting line that absorbs the FX difference when we consolidate our USD-functional Indonesian subsidiary into our CNY-functional parent. In 2025, this was the single biggest driver of our 45% surge in FX-related profit-and-loss volatility. We track CTA monthly, and any movement above a threshold triggers a hedging review.

### 3.2 FX-Related Business Data Collection

Treasury cannot manage what operations do not report. We collect six data categories in real time:

| Data Category | Source System | Update Frequency |
|---------------|--------------|------------------|
| Import/export trade business data | ERP (SAP) | Daily |
| Internal borrowing | Treasury management system | Real-time |
| FX transactions | Trading platform (Bloomberg/Reuters) | Real-time |
| External borrowing | Loan administration system | Weekly |
| Capital injection | Board resolutions + bank confirmations | Event-driven |
| Dividends | Board resolutions + tax clearances | Event-driven |

This data feeds directly into the third column.

### 3.3 FX Exposure Risk Statistics

This is the nerve center. We run three calculations in parallel:

**First: Currency Exposure vs. RMB → Exposure Rate Cost Calculation.**

For each currency pair — EUR/CNY, KRW/CNY, IDR/CNY, JPY/CNY — we calculate the net open position in RMB terms. Then we ask: what is the cost of hedging this exposure at current market rates? If the 12-month forward KRW/CNY is trading at a 3% premium to spot, that is the cost of certainty. We compare that to our risk appetite.

**Second: Individual Company FX Exposure → Group Consolidated FX Exposure.**

This is the netting step. Company A may be long USD 50 million. Company B may be short USD 30 million. At the group level, the net exposure is only USD 20 million. But here's the catch: **natural netting only works if the legal entities can actually offset each other.** Our Indonesian subsidiary cannot legally net its USD receivable against our Hong Kong entity's USD payable. So we track both the gross and the net, and the gap between them tells us how much intercompany settlement efficiency we are losing.

**Third: Individual Company FX Gains/Losses → Group Consolidated FX Gains/Losses Calculation.**

This is the backward-looking P&L impact. Every month, each entity reports its realized and unrealized FX gains/losses. We consolidate them, eliminate intercompany items, and present the group number to the board. In 2025, this number was **CNY 1.269 billion** — a 45% increase. That is why this framework exists.

### 3.4 Risk Limit Framework (RLF) & Automated Triggers

Below the three columns, we have our control layer:

- **Exposure Limit Management.** We set hard limits by currency pair, by entity, and by tenor. For example: "Indonesia entity may not carry more than USD 200 million of unhedged USD/IDR exposure beyond 90 days."

- **Stop-Loss Limit Management.** If a hedging position moves against us by more than a pre-set threshold — say, 2% of notional — the system auto-generates a stop-loss alert. The trader has 4 hours to respond before the position is escalated to the CFO.

- **FX Derivative Limit Management.** We cap the total notional of outstanding forwards, options, and swaps. This prevents over-hedging and ensures we never have more derivative exposure than underlying physical exposure.

### 3.5 Dynamic Hedging & Regional Crisis Playbooks

On the right side of the pink bar:

- **FX Trading Decisions.** This is the execution layer. Based on the exposure statistics, the limit utilization, and the market view, the treasury team decides: hedge now, or wait? Use forwards, options, or a collar? What tenor?

- **Update Risk Management Strategies.** This is the quarterly review. We look back at hedge effectiveness. Did our forwards lock in better rates than the average spot? Did our options expire worthless? What does the market imply about future volatility? We update the playbook accordingly.

---

## Slide 4: Phase III — Post-Event Management

**Speaker Notes:**

The gray section is **Post-Event Management**. Many treasury teams think their job ends when the trade settles. We believe it begins there.

### 4.1 Prevent Liquidation Risk

First: **Prevent liquidation risk due to fund shortages or operational issues.** This is not an FX problem per se, but FX can cause it. If IDR depreciates sharply and our Indonesian subsidiary's local-currency cash flow cannot cover its USD-denominated debt service, we face a liquidity crisis. Our post-event monitoring includes a 13-week cash-flow forecast for every major entity, updated weekly, with FX stress scenarios built in.

### 4.2 Economic Exposure & Competitive Devaluation

Second: **Economic Exposure & Competitive Devaluation Impact Assessment.** This is the strategic layer. If the Argentine peso devalues by 30%, what happens to our competitors who source from Argentina? Do we gain or lose competitive position? If the Korean won strengthens, do our Korean-made precursors become uncompetitive against Chinese-made alternatives? This is not a balance-sheet exposure. This is a **long-term cash-flow and market-share exposure**, and it informs our geographic sourcing decisions.

### 4.3 Business Continuity Plan (BCP)

Third: **Business Continuity Plan triggered by market turbulence or operational shifts.** We have predefined BCP triggers. For example:

- **Level 1:** Local currency moves >5% in a week. Activate enhanced daily reporting.
- **Level 2:** Key counterparty bank fails or a country's FX controls tighten. Activate alternative settlement routes.
- **Level 3:** War, sanctions, or sovereign default. Activate crisis committee and freeze all non-essential hedging.

### 4.4 Key Issue Reporting

Finally, **Key Issue Reporting.** Every quarter, the treasury team produces a report for the Audit Committee covering: limit breaches, hedge effectiveness, CTA movements, and any regulatory or operational issues. This is not a compliance checkbox. This is how the board understands whether our FX risk management is actually working.

---

## Slide 5: Key Takeaways

**Speaker Notes:**

Let me leave you with five principles that make this framework work:

1. **Pre-event is more valuable than post-event.** Every dollar spent on identification and simulation saves ten dollars in crisis management.

2. **Measure gross and net.** Natural netting is elegant on paper, but legal and tax boundaries often prevent it in practice. Know both numbers.

3. **CTA is not an accounting footnote.** For a company with a 12-billion-USD capital-layer exposure, CTA is a real economic cost that affects your debt covenants, your credit rating, and your shareholder equity.

4. **Automate the routine, reserve human judgment for exceptions.** The limit framework and VaR triggers run automatically. Human traders should only intervene when the market does something the model did not expect.

5. **FX risk management is not a cost center.** When done correctly, it is a profit protector. In 2025, without this framework, our FX-related P&L volatility could have been materially worse. The goal for 2026 is to bring that volatility down to **plus or minus 20% year-on-year.**

Any questions?

---

*End of Training Script*
