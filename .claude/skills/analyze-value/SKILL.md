---
name: analyze-value
description: Analyze expected points, PPM, price trends, and buy/sell signals
user-invocable: true
---

# Analyze Value

Calculate expected fantasy points, points-per-million (PPM), price trends, and generate buy/sell signals for all drivers and constructors.

## Input

- **Race name** (optional) — for context-specific analysis (circuit characteristics, practice pace)
- **Save to file** (optional) — saves to `data/r{XX}-{race-name}/value-analysis.md`

## Data Sources

Read:
- Form analysis (from `/analyze-form` output or `fantasy-points.md` files directly)
- Current prices from latest `prices.md` or `fantasy-points.md`
- Practice pace data from current round (if available)
- `data/2026-calendar.md` for circuit characteristics

## Expected Points Calculation

For each driver/constructor, estimate expected points based on:

1. **Historical form** — weighted average of last 3 rounds (most recent weighted highest: 50%/30%/20%)
2. **Practice pace** — if practice data available for current round, adjust expectations
3. **Circuit characteristics** — some circuits favor overtaking (more position/overtake points), some are processional

Present uncertainty: expected points should be a range (low / median / high) not a single number.

## Value Metrics

### Driver Value Table

| Driver | Team | Price | Exp. Pts (Low/Med/High) | PPM | Price Trend | Ownership% | Signal |
|--------|------|-------|------------------------|-----|-------------|-----------|--------|

### Constructor Value Table

| Constructor | Price | Exp. Pts (Low/Med/High) | PPM | Price Trend | Ownership% | Signal |
|-------------|-------|------------------------|-----|-------------|-----------|--------|

### Metrics

- **PPM** = Expected Points (median) / Price — higher is better value
- **Price Trend** = direction based on `Value` vs `OldPlayerValue` across recent rounds
  - Rising: price increased last round
  - Falling: price decreased last round
  - Stable: no change
- **Signal:**
  - **BUY** — High PPM + rising price → buy before they get more expensive
  - **SELL** — Declining form + still expensive → sell before price drops
  - **HOLD** — Stable form at fair price
  - **WATCH** — Low price + improving form → potential future buy
  - **AVOID** — Poor form + poor value

## Buy/Sell Highlights

Summarize the top insights:
- **Best buys:** Top 3-5 drivers/constructors by PPM with positive signals
- **Sell candidates:** Overpriced assets with declining form
- **Budget gems:** Cheapest drivers with positive PPM trends
- **Differential picks:** Low ownership + decent expected points (league advantage)
- **Overtaking value:** Drivers who qualify low but race high → hidden overtake + position points

## Notes

- Always use confirmed prices — never estimate prices
- PPM is the primary value metric, but consider ceiling (high variance can be good with No Negative chip)
- In a friends league, differentiation matters — a slightly suboptimal pick that nobody else has can win the league
- Price changes weigh last 3 races equally — factor trajectory, not just this week
