# Geopolitical Risk Assessment Model

## Data Sources

### Official Statements (30% weight)

**Trump statements (30% of category = 9% total)**
- Sources: Truth Social, official statements, press briefings
- Escalation signals: Threats of military action, harsh rhetoric against Iran
- De-escalation signals: Offers of negotiation, moderated language

**Netanyahu statements (20% of category = 6% total)**
- Sources: Israeli government statements, press conferences
- Escalation: Threats against Iran, military readiness announcements
- De-escalation: Diplomatic overtures, ceasefire indications

**Iran statements (50% of category = 15% total)**
- Sources: IRGC statements, Foreign Ministry, Supreme Leader
- Escalation: Retaliation threats, closure of Hormuz threats
- De-escalation: Diplomatic engagement, willingness to negotiate

### Military Actions (30% weight)

**Hormuz Strait shipping (40% of category = 12% total)**
- Data: AIS shipping data, Lloyd's List, maritime agencies
- Escalation: Vessel seizures, inspection delays, traffic disruption
- Sources: MarineTraffic, Reuters shipping alerts

**US/Israel strikes on Iran (30% of category = 9% total)**
- Military targets hit in Iran
- Cyber attacks on Iranian infrastructure
- Drone strikes, missile attacks

**Iran strikes on US/Israel (30% of category = 9% total)**
- Missile/drone attacks on Israeli territory
- Attacks on US bases in region
- Proxy attacks (Hezbollah, Houthis, militias)

### Financial Markets (30% weight)

**Crude Oil - Brent (50% of category = 15% total)**
- Thresholds:
  - < $75: Neutral (0-20)
  - $75-85: Elevated (20-50)
  - $85-100: High (50-75)
  - > $100: Critical (75-100)
- Daily change >5% adds +10 to component

**US Dollar Index DXY (20% of category = 6% total)**
- Thresholds:
  - Stable (103-107): Neutral
  - Rising >107: Flight to safety (+10)
  - Spike >110: High risk (+20)
- Daily change >1% adds +5

**Gold (20% of category = 6% total)**
- Thresholds:
  - <$2000: Neutral
  - $2000-2200: Elevated
  - >$2200: High risk
- Daily change >2% adds +5

**Japan/Korea markets (10% of category = 3% total)**
- Nikkei 225 and KOSPI
- Sharp declines (>2%) indicate risk-off sentiment

### Diplomatic Signals (10% weight)

**China (30% of category = 3% total)**
- Statements on conflict, oil import policy changes
- Military posture in region

**Russia (20% of category = 2% total)**
- Iran-Russia coordination
- Statements on military support

**Japan (10% of category = 1% total)**
- Energy security statements
- Maritime security concerns

**Saudi Arabia (10% of category = 1% total)**
- Regional mediation efforts
- Oil policy coordination

**UAE (10% of category = 1% total)**
- Diplomatic initiatives
- Regional stability statements

## Scoring Methodology

### Daily Component Score (0-100)

Each of 4 categories scored 0-100, then weighted:
- Official: score × 0.30
- Military: score × 0.30
- Markets: score × 0.30
- Diplomatic: score × 0.10

### Aggregation

Total Risk Score = Σ(weighted components)

### Day-over-Day Change

Δ = Today's Score - Yesterday's Score
- Δ > 10: Significant escalation
- Δ 5-10: Moderate escalation
- Δ -5 to 5: Stable
- Δ < -5: De-escalation

## Historical Baseline (March 2025)

Since March 1, 2025 conflict:
- Min observed: ~25
- Max observed: ~65
- Current typical: 35-45

Use these as calibration points for "normal" vs "elevated" risk.
