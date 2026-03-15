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
3. **Circuit characteristics** — read `data/circuits.md` for the current circuit:
   - `overtaking_index` ≥7: add overtake/position-gained upside for drivers starting outside top 10
   - `overtaking_index` ≤3: reduce overtake-based upside, qualifying position is critical
   - `sc_probability` = high: add +2 to +5 pts to midfield drivers' upside (SC creates chaos value)
   - `tire_deg` = high: flag constructors with good tire management as having a hidden edge
4. **DOTD probability** — estimate each driver's chance of winning DOTD (worth 10 pts). Base weights:
   - Fan-favorite drivers (Hamilton 1.8×, Leclerc 1.6×, Norris 1.4×, Russell 1.3×, Antonelli 1.2×, Bearman 1.2×, Alonso 1.2×)
   - Home race drivers get +50% boost to their DOTD weight
   - Midfield hero scenario (P15+ start → top 10 finish): strong DOTD candidate regardless of popularity
   - Read `dotd_notes` from `data/circuits.md` for circuit-specific DOTD patterns

Present uncertainty: expected points should be a range (low / median / high) not a single number.

## Value Metrics

### Driver Value Table

| Driver | Team | Price | Exp. Pts (Low/Med/High) | DOTD% | PPM | Price Trend | Ownership% | Signal |
|--------|------|-------|------------------------|-------|-----|-------------|-----------|--------|

**DOTD%** — estimated probability this driver wins Driver of the Day (worth 10 pts). Derived from `dotd_weight` (popularity), circuit DOTD profile from `data/circuits.md`, and expected race position gain.

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
- **DOTD upside:** Top 2-3 drivers with highest DOTD probability — note if their expected pts are close to another option (DOTD can swing the pick)
- **SC chaos value:** If `sc_probability` = high, flag midfield drivers starting P12–P18 with high overtake potential as lottery tickets — SC restart can unlock 8–15 bonus pts

## Notes

- Always use confirmed prices — never estimate prices
- PPM is the primary value metric, but consider ceiling (high variance can be good with No Negative chip)
- In a friends league, differentiation matters — a slightly suboptimal pick that nobody else has can win the league
- Price changes weigh last 3 races equally — factor trajectory, not just this week
