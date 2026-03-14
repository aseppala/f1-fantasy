---
name: pick-team
description: F1 Fantasy Team Picker
user_invocable: true
---

# F1 Fantasy Team Picker

Pick optimal F1 Fantasy teams for an upcoming race weekend. Produces three team picks following distinct strategies.

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

### 1. Load existing data

Read **all** of the following to build a complete picture:

**Season-level files in `data/`:**
- `data/2026-calendar.md` — race calendar, sprint weekends, race IDs for URL construction
- `data/2026-standings.md` — current driver and constructor championship standings
- `data/2026-prices.md` — price tracker across rounds with ownership percentages
- `data/2026-preseason-testing.md` — baseline pace data (less relevant as season progresses)
- `data/team-strategy.md` — the three team strategies (Safe, Constructor Kings, Ferrari Nuclear)

**Previous round folders (`data/r{XX}-{race-name}/`):**
- `prices.md` — confirmed prices and deltas for that round
- `qualifying.md` — full qualifying classification
- `race.md` — full race result with finishing positions, gaps, DNFs, fastest lap
- `free-practice-1.md`, `free-practice-2.md`, `free-practice-3.md` — practice sessions
- `sprint-qualifying.md`, `sprint.md` — sprint weekend sessions
- `team-1-safe.md`, `team-2-constructor-kings.md`, `team-3-ferrari-nuclear.md` — previous team picks (contain actual squad, budget, transfers used, chips used)

**Current round folder (if it exists):**
- Any practice, sprint qualifying, or qualifying results already saved
- Any price data already captured

Read **at minimum** the last 3 rounds of data to assess form trends.

### 1b. Backfill missing round data

For each previous round folder, check if the following files exist. If any are **missing**, fetch them from formula1.com and save them:

| File | URL pattern | When to fetch |
|------|------------|---------------|
| `qualifying.md` | `.../races/{race-id}/{race-name}/qualifying` | Always |
| `race.md` | `.../races/{race-id}/{race-name}/race-result` | Always (include fastest lap from `.../fastest-laps`) |
| `free-practice-1.md` | `.../races/{race-id}/{race-name}/practice/1` | Always |
| `free-practice-2.md` | `.../races/{race-id}/{race-name}/practice/2` | Only non-sprint weekends |
| `free-practice-3.md` | `.../races/{race-id}/{race-name}/practice/3` | Only non-sprint weekends |
| `sprint-qualifying.md` | `.../races/{race-id}/{race-name}/sprint-qualifying` | Sprint weekends only |
| `sprint.md` | `.../races/{race-id}/{race-name}/sprint-results` | Sprint weekends only |
| `prices.md` | N/A — can only come from user | Flag as missing, ask user |

Use `data/2026-calendar.md` for race IDs and sprint weekend identification.

Also update `data/2026-standings.md` from `https://www.formula1.com/en/results/2026/drivers` and `https://www.formula1.com/en/results/2026/team`.

### 2. Assess form and trends

**Driver form (last 3 races):**
- Qualifying positions (trend: improving, stable, declining?)
- Race finishing positions (trend)
- Fantasy points scored per round
- Price trajectory (rising = buy signal, falling = sell or buy-low opportunity)
- DNF/DNS count (reliability flag)
- Positions gained per race (overtaking ability)

**Constructor form (last 3 races):**
- Combined qualifying performance (both Q3? one Q1?)
- Combined race points and fantasy points
- Reliability (any DNFs?)
- Price trajectory

**Pecking order evolution:**
Compare current order against preseason testing, R01, and most recent round.

Summarize as a **form table**:

| Driver | Last 3 Races | Trend | Reliability | Notes |
|--------|-------------|-------|-------------|-------|

### 3. Research current weekend

**IMPORTANT: Only use formula1.com for race results, practice, qualifying, and standings data.**

Use `data/2026-calendar.md` for the race ID, then fetch all available sessions. Save each to the round folder as separate files.

**Weather forecast:**
Search for "{city} weather {qualifying date}" and "{city} weather {race date}".
- Rain → high variance, consider No Negative chip
- Extreme heat → tire degradation concerns
- Dry/mild → rely on practice pace data

### 4. Determine budget and transfers per team

For each of the 3 teams, read the **previous round's team file** to extract:

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

Present a **budget summary table** at the top of each team pick:

| Team | Squad Value | Budget | Buffer | Free Transfers | Chips Remaining |
|------|------------|--------|--------|---------------|----------------|

### 5. Analyze value

For each potential pick, calculate:
- **Expected Points** from form + practice pace + circuit characteristics
- **PPM = Expected Points / Price**
- **Price trend** — likely to rise or fall?
- **Ownership %** — low ownership = differentiation in friends league

Flag:
- High PPM + rising price → buy before they get expensive
- Declining form + still expensive → sell
- Budget drivers who qualify low but race high → overtaking value

### 6. Build teams

Read `data/team-strategy.md` for the three strategies, then build each team:

**Team 1: "Safe"** — Ride the dominant constructor
**Team 2: "Constructor Kings"** — 2 best constructors, budget drivers
**Team 3: "Ferrari Nuclear"** — Both Ferrari drivers + constructor, always

For each team, respect:
- **Actual budget** for that team (not $100M — use the confirmed figure)
- Max 2 drivers from the same constructor
- **Available free transfers** — only propose changes that fit within the free transfer count. If more changes are needed, explicitly note the -10 pts penalty per extra transfer and whether it's worth it.
- Chip strategy per team from `data/team-strategy.md`

When Limitless is active, budget and transfer limits are ignored but note what the team reverts to afterward.

### 7. Run scoring simulation

Update `simulator.py` with current weekend profiles, then run:
```bash
python simulator.py --race {race} --sims 10000 --seed 42
```

Include variants to test key decisions per team.

### 8. Present each team

For each of the 3 teams, output:

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
- Simulation average, std dev, min, max
- 2x driver choice and reasoning
- Transfers made from previous round (list each swap)
- Free transfers remaining after this round (affects carry-over to next round)
- Key risks

Then a **simulation comparison table** across all teams and variants.

### 9. Save outputs

Create the round folder `data/r{XX}-{race-name}/` if it doesn't exist.

Save each team to a separate file:
- `data/r{XX}-{race-name}/team-1-safe.md`
- `data/r{XX}-{race-name}/team-2-constructor-kings.md`
- `data/r{XX}-{race-name}/team-3-ferrari-nuclear.md`

Each team file MUST include in its header:
- **Actual squad** (drivers + constructors with prices)
- **Total budget** for this team
- **Transfers used** this round and carry-over status
- **Chip used** this round (if any)
- **Chips remaining** for the season

This data is essential for the next round's calculations.

Save session results to separate files. Update `data/2026-standings.md` if new results available. Do NOT overwrite `data/2026-prices.md` — only update with confirmed prices from the user.

## Important Notes

- Constructors score from BOTH drivers — two top-5 finishers beats P1 + P15
- Overtaking points are hidden value — drivers who qualify low but race high
- Price changes weigh last 3 races equally — factor trajectory, not just this week
- In a friends league, differentiation wins — don't copy the consensus team
- When uncertain between two picks at similar price, prefer higher ceiling
- Sprint weekends = ~30-50% more points — factor into chip decisions
- Always use confirmed prices from `prices.md` files — never estimate prices
- Always track and display the actual budget per team, not the default $100M
