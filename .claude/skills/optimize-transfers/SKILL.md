---
name: optimize-transfers
description: Find optimal transfer sets for each fantasy team
user-invocable: true
---

# Optimize Transfers

Recommend optimal transfers for each fantasy team, respecting free transfer limits, budget constraints, and chip strategy.

## Input

- **Team name/number** (optional) — defaults to "all" teams from `data/team-strategy.md`
- **Round** (optional) — defaults to next upcoming round

## Data Sources

Read:
- `data/team-strategy.md` — team philosophies, chip plans, construction rules
- Previous round team files (`data/r{XX}-{race-name}/team-{N}-{slug}.md`) — current squads, budgets, transfers used
- Current prices from latest `prices.md` or `fantasy-points.md`
- Form analysis and value analysis (if available in current round folder)

## Transfer Rules Reference

- **2 free transfers per Grand Prix** per team
- **1 unused transfer carries over** (max 1 — does NOT compound beyond that)
- Maximum free transfers in a round: 3 (2 base + 1 carried over)
- Extra transfers beyond free ones cost **-10 pts each**
- Transfers are based on **net change from previous race** — swapping out then back = 0 transfers used

## Logic

For each team:

### 1. Determine Available Transfers

| Field | Calculation |
|-------|-------------|
| Base transfers | 2 |
| Carry-over | 1 if previous round used < 2 transfers, else 0 |
| **Total free** | Base + carry-over (max 3) |

### 2. Identify Transfer Candidates

**Sell candidates** (players to remove):
- Declining form (2+ rounds of decreasing points)
- Overpriced relative to expected output (low PPM)
- Price likely to drop (sell before value loss)
- Not aligned with team philosophy

**Buy candidates** (players to add):
- High PPM (best value for money)
- Rising form / improving trend
- Price likely to rise (buy before value gain)
- Aligned with team philosophy
- Low ownership (differentiation in friends league)

### 3. Generate Transfer Sets

For each team, propose:

1. **Recommended transfers** (within free transfer limit):
   - List each swap: OUT → IN, price delta, expected point gain
   - Net budget impact
   - Rationale per swap

2. **Optional paid transfers** (if high-value opportunity exists):
   - Only suggest if expected gain > **+15 pts net** (after -10 pt penalty)
   - Clearly mark the penalty cost
   - Make the case for why the extra transfer is worth it

3. **"Do nothing" baseline** — expected points if no transfers are made

### 4. Constraints

- Stay within team budget (budget = previous budget adjusted for price changes of owned assets)
- Max 2 drivers from same constructor
- Respect team philosophy from `data/team-strategy.md`
- **Penalty threshold:** Only suggest paid transfers if expected gain > +15 pts net (configurable)

### 5. Chip Synergy

- **Pre-Wildcard:** Don't burn transfers on short-term fixes if Wildcard is planned soon
- **Pre-Limitless:** Hold budget flexibility — Limitless reverts afterward so budget matters
- **Post-Limitless:** May need transfers to rebuild since Limitless team reverts
- Coordinate with chip plan from `data/team-strategy.md`

## Output

For each team:

```markdown
## Team {N}: {Name}

**Current squad:** {list drivers + constructors}
**Budget:** ${XX.X}M | **Free transfers:** {N}

### Recommended Transfers
| # | Out | In | Price Delta | Exp. Pts Gain | Rationale |
|---|-----|----|-------------|---------------|-----------|
| 1 | ... | .. | ...         | ...           | ...       |

**Net budget impact:** +/- ${X.X}M
**Expected point gain over "do nothing":** +{X} pts

### Optional Paid Transfer (if applicable)
| Out | In | Price Delta | Exp. Pts Gain | Penalty | Net Gain |
|-----|----|-----------  |---------------|---------|----------|

### Squad After Transfers
| # | Driver/Constructor | Price | Exp. Pts |
|---|-------------------|-------|----------|
```

## Notes

- Squad continuity matters — prefer minimal changes when gains are marginal
- Don't suggest transfers just for the sake of using them — "do nothing" is valid
- Rising prices are an investment signal — buying before a rise preserves future budget flexibility
- Factor in the specific round's characteristics (sprint weekend = more points available, weather, etc.)
