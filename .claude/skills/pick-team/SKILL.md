---
name: pick-team
description: Build F1 Fantasy team selections from analyzed data
user-invocable: true
---

# F1 Fantasy Team Builder

Build optimal F1 Fantasy team picks for an upcoming race weekend. This skill assumes data has already been fetched and analyzed (by the `f1-fantasy` agent or individual skills). It focuses on team construction, not data gathering.

## Input

The user may provide:
- **Race name** (e.g. "Chinese GP", "Monaco") — if not provided, determine the next upcoming race from `data/2026-calendar.md`
- **Specific constraints** (e.g. "must include Verstappen", "no Aston Martin drivers")
- **Chip to use** (e.g. "Limitless on Team 1") — default: follow strategy in `data/team-strategy.md`

## Game Rules Reference

### Team Composition
- 5 drivers + 2 constructors
- Max 2 drivers from the same constructor
- Starting budget: $100M (but actual budget = $100M + any unspent amount from initial team selection)

### Budget Mechanics
- **Budget = starting budget + accumulated unspent amount.** If a team was built for $96.6M from a $100M cap, the budget is $100M, not $96.6M. But price appreciation/depreciation of owned assets changes the squad value, and the budget adjusts: `available budget = original budget cap + (current squad value - original squad cost)`. In practice, track the user's confirmed total budget per team.
- **Limitless is temporary** — team reverts after the weekend, budget returns to pre-Limitless state
- **Wildcard is permanent** — transfers stick, budget adjusts permanently

### Transfer Rules
- **2 free transfers per Grand Prix** per team
- **1 unused transfer carries over** to the next round (max 1 — does NOT compound beyond that)
- So you can have 2 or 3 free transfers in a given round (2 base + 0 or 1 carried over)
- Extra transfers beyond free ones cost **-10 pts each**
- Transfers are based on **net change from previous race** — swapping a driver out then back = 0 transfers used

### Deadlines
| Weekend Type | Team Lock / Chip Deadline | Final Fix Deadline |
|-------------|------------------------|--------------------|
| **Normal weekend** | Before Qualifying | After Qualifying, before Race |
| **Sprint weekend** | Before Sprint Race (after Sprint Qualifying) | After Sprint, before Race |

### 2x Driver (Captain)
Every race, choose one driver for **double points**. This is NOT a chip — it's available every weekend. The single most important decision each round.

### Power Chips (6 total, one-time use each, max 1 per weekend)

| Chip | Available | Mechanics |
|------|-----------|-----------|
| **No Negative** | Round 1 | All negative points (DNFs, positions lost) become zero. Applied per scoring category. |
| **Auto Pilot** | Round 1 | Automatically gives 2x to your highest-scoring driver. Overrides manual 2x pick. |
| **Final Fix** | Round 1 | Swap ONE driver after lineups lock, before race start. 2x transfers to new driver if applicable. On sprint weekends, unlocks after Sprint only. |
| **Limitless** | Round 2 | Unlimited transfers + ignore budget cap. Team reverts next week. |
| **Wildcard** | Round 2 | Unlimited transfers, must stay within budget. Changes permanent. |
| **x3 Boost** | Round 2 | One driver scores TRIPLE. Can still 2x a DIFFERENT driver. Cannot stack x3+2x on same driver. |

Once activated, a chip **cannot be cancelled**.

### Scoring Quick Reference

**Qualifying:** P1=10, P2=9...P10=1, P11+=0, NC/DSQ=-5
**Race:** P1=25, P2=18, P3=15, P4=12, P5=10, P6=8, P7=6, P8=4, P9=2, P10=1, P11+=0, DNF=-20
**Bonus:** +1/position gained, +1/overtake, +10 fastest lap, +10 DOTD
**Sprint:** P1=8...P8=1, DNF=-10, +5 fastest lap, +1/position gained, +1/overtake
**Constructor Quali:** Both Q3=+10, Both Q2=+5, One Q3=+3, One Q2=+1, Both Q1=-1
**Constructor Race:** Sum of both drivers' race points. Pit stop bonuses: <2.0s=+10, 2.0-2.19s=+10, 2.2-2.49s=+5, 2.5-2.99s=+2, fastest stop=+5 extra

## Steps

### 1. Validate strategy file

Check if `data/team-strategy.md` exists.

**If missing**, use `AskUserQuestion` to interview the user:
1. How many teams do you want to run? (default: 3)
2. For each team: name, philosophy (1-2 sentences), construction approach, 2x driver preference, chip strategy, risk tolerance

Save responses to `data/team-strategy.md` using a structured format with one section per team.

**If it exists**, read it and extract team names and slugs for use throughout the workflow. The slug is the lowercase, hyphen-separated team name (e.g. "Constructor Kings" → `constructor-kings`).

### 2. Load analyzed data

Read the following (all should already exist from prior skill runs):

- `data/team-strategy.md` — team strategies
- Previous round team files (`data/r{XX}-{race-name}/team-{N}-{slug}.md`) — current squads, budgets, transfers
- Current round analysis files (if available):
  - `form-analysis.md` (from `/analyze-form`)
  - `value-analysis.md` (from `/analyze-value`)
  - Transfer recommendations (from `/optimize-transfers`)
  - Simulation results (from `/simulate`)
- Current prices from latest `prices.md` or `fantasy-points.md`

If analysis files don't exist, inform the user they should run the analysis skills first (or use the `f1-fantasy` agent for the full pipeline).

### 3. Determine budget and transfers per team

For each team defined in `data/team-strategy.md`, read the **previous round's team file** to extract:

1. **Actual squad** — the 5 drivers + 2 constructors that were locked in
2. **Total budget** — the confirmed budget (may be >$100M if unspent from R01). If not recorded, ask the user.
3. **Chips used so far** — track which chips each team has already spent
4. **Transfers used last round** — determines carry-over

Then calculate:

| Field | How to calculate |
|-------|-----------------|
| **Current squad value** | Sum of current prices of locked-in picks (prices change between rounds) |
| **Total budget** | As recorded in previous team file. Budget grows/shrinks with price changes of owned assets. |
| **Free transfers** | 2 base + 1 carry-over if <2 were used last round (max 3 total) |
| **Available chips** | 6 minus any already used. Check availability (Round 1 vs Round 2 chips). |
| **Buffer** | Total budget - current squad value |

### 4. Build teams

For each team defined in `data/team-strategy.md`, build a squad following that team's philosophy, construction rules, 2x driver guidance, and chip strategy.

If transfer recommendations exist (from `/optimize-transfers`), apply them. Otherwise, determine transfers independently.

For each team, respect:
- **Actual budget** for that team (not $100M — use the confirmed figure)
- Max 2 drivers from the same constructor
- **Available free transfers** — only propose changes that fit within the free transfer count. If more changes are needed, explicitly note the -10 pts penalty per extra transfer and whether it's worth it.
- Chip strategy per team from `data/team-strategy.md`

When Limitless is active, budget and transfer limits are ignored but note what the team reverts to afterward.

### 5. Present each team

For each team, output:

**Budget & Transfer Status:**
| Squad Value | Budget | Buffer | Free Transfers | Chips Used | Chips Remaining |
|------------|--------|--------|---------------|------------|-----------------|

**Driver table (with sum row):**
| # | Driver | Team | Price | Exp. Pts | PPM | Rationale |
| | **Drivers total** | | **$XX.XM** | | | |

**Constructor table (with sum row):**
| # | Constructor | Price | Exp. Pts | PPM | Rationale |
| | **Constructors total** | | **$XX.XM** | | | |

**Team total: $XX.XM** | **Budget: $XX.XM** ($X.XM buffer)

**Footer:**
- Simulation average, std dev, min, max (if simulation was run)
- 2x driver choice and reasoning
- Transfers made from previous round (list each swap)
- Free transfers remaining after this round (affects carry-over to next round)
- Key risks

Then a **simulation comparison table** across all teams and variants (if simulation data available).

### 6. Save outputs

Create the round folder `data/r{XX}-{race-name}/` if it doesn't exist.

Save each team to `data/r{XX}-{race-name}/team-{N}-{slug}.md` where `{N}` is the team number (1, 2, 3, ...) and `{slug}` is derived from the team name in `data/team-strategy.md` (lowercase, hyphens for spaces, e.g. "Constructor Kings" → `constructor-kings`).

Each team file MUST include in its header:
- **Actual squad** (drivers + constructors with prices)
- **Total budget** for this team
- **Transfers used** this round and carry-over status
- **Chip used** this round (if any)
- **Chips remaining** for the season

This data is essential for the next round's calculations.

## Important Notes

- Constructors score from BOTH drivers — two top-5 finishers beats P1 + P15
- Overtaking points are hidden value — drivers who qualify low but race high
- Price changes weigh last 3 races equally — factor trajectory, not just this week
- In a friends league, differentiation wins — don't copy the consensus team
- When uncertain between two picks at similar price, prefer higher ceiling
- Sprint weekends = ~30-50% more points — factor into chip decisions
- Always use confirmed prices from `prices.md` files — never estimate prices
- Always track and display the actual budget per team, not the default $100M
