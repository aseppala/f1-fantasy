# F1 Fantasy 2026 - Rules & Scoring

## Basic Format

- **Budget:** $100M cost cap
- **Team:** 5 drivers + 2 constructors
- **Up to 3 teams** per account (one with head, one with heart, one for chaos)
- **Transfers:** 2 free transfers per Grand Prix per team. Extra transfers cost -10 pts each. One unused transfer carries over (doesn't compound).
- **Price range:** $3M (floor) to ~$30M

## Scoring System

### Qualifying (Drivers)
| Position | Points |
|----------|--------|
| P1 | 10 |
| P2 | 9 |
| P3 | 8 |
| P4 | 7 |
| P5 | 6 |
| P6 | 5 |
| P7 | 4 |
| P8 | 3 |
| P9 | 2 |
| P10 | 1 |
| P11-P20 | 0 |
| NC/DSQ/No time | -5 |

### Race Points (Drivers)
| Position | Points |
|----------|--------|
| P1 | 25 |
| P2 | 18 |
| P3 | 15 |
| P4 | 12 |
| P5 | 10 |
| P6 | 8 |
| P7 | 6 |
| P8 | 4 |
| P9 | 2 |
| P10 | 1 |
| P11+ | 0 |
| DNF/DSQ | -20 |

### Bonus Points (Drivers)
- **Positions gained:** +1 pt each (qualifying position vs race finish)
- **Positions lost:** −1 pt each (confirmed from API data — positions lost DO subtract)
- **Overtakes:** +1 pt each (tracked independently of net position change — a driver can gain overtake pts even with zero or negative net positions)
- **Fastest lap:** +10 pts
- **Driver of the Day:** +10 pts

### Sprint Scoring (Drivers)
- P1: 8 pts down to P8: 1 pt
- DNF/DSQ: -10 pts (reduced from -20 in 2026)
- Fastest lap in sprint: +5 pts
- Positions gained: +1 pt each
- Overtakes: +1 pt each

### Constructor Qualifying
- Both drivers reach Q3: +10 pts
- Both drivers reach Q2: +5 pts
- One driver reaches Q3: +3 pts
- One driver reaches Q2: +1 pt
- Both eliminated in Q1: -1 pt
- Driver DSQ: -5 pts per driver

### Constructor Race Scoring
- Sum of both drivers' race finishing points
- Driver DSQ: -20 pts per driver

### Constructor Pit Stop Bonus
| Pit Stop Time | Points |
|--------------|--------|
| 2.5 - 2.99s | +2 |
| 2.2 - 2.49s | +5 |
| 2.0 - 2.19s | +10 |
| < 2.0s | +10 |
| Fastest pit stop of race | +5 extra |
| Record-breaking (< 1.8s) | +15 |

## 2x Driver (Captain)

Every race, you choose one driver as your **2x driver** — their points are doubled. This is NOT a chip; it's a permanent feature available every race weekend. Picking the right 2x driver is one of the most important decisions each round.


## Power Chips (6 Total)

Only one chip per race weekend. Each can only be used once per season. Once activated, a chip cannot be cancelled. 3 available from Round 1, 3 unlock after Round 1.

### Chip Summary

| Chip | Available | Description |
|------|-----------|-------------|
| **No Negative** | Round 1 | All negative points (DNFs, positions lost) become zero for that race week. Applied per scoring category, not just the overall total. |
| **Auto Pilot** | Round 1 | Automatically gives 2x boost to whichever driver in your team scores the most points that weekend. Overrides your manual 2x pick. |
| **Final Fix** | Round 1 | Swap ONE driver after lineups lock, before the race starts. If the swapped driver had 2x boost, it transfers to the new driver. |
| **Limitless** | Round 2 | Unlimited transfers AND ignore the budget cap for one race week. Team returns to normal the following week (temporary). |
| **Wildcard** | Round 2 | Unlimited transfers but must stay within your budget cap. Changes are permanent (unlike Limitless). |
| **x3 Boost** | Round 2 | One driver scores TRIPLE points. You can still assign 2x to a different driver, so two drivers get boosted (one x3, one x2). Cannot stack x3 and x2 on the same driver. |

### Chip Deadlines

| Weekend Type | Chip Activation Deadline | Final Fix Deadline |
|-------------|------------------------|--------------------|
| **Normal weekend** | Before Qualifying | After Qualifying, before Race |
| **Sprint weekend** | Before Sprint Race (after Sprint Qualifying) | After Sprint, before Race |

### Key Rules

- **Max 1 chip per weekend** — cannot combine chips (e.g., no Limitless + No Negative)
- **Each chip is one-time use** — once used, gone for the season
- **Limitless is temporary** — your team reverts to the pre-Limitless lineup after the weekend
- **Wildcard is permanent** — transfers made with Wildcard stick
- **x3 + 2x = two boosted drivers** — one at 3x, one at 2x, must be different drivers
- **Auto Pilot vs manual 2x** — Auto Pilot retroactively picks your highest scorer; manual 2x is your pre-race choice
- **Final Fix on sprint weekends** — only unlocks after the Sprint race, not before

### Strategy Notes

- **Limitless** is strongest on sprint weekends (more points available) with a clear pecking order
- **x3 Boost** is strongest on sprint weekends too — deploy on your most confident pick
- **No Negative** is best for wet races or street circuits (Monaco, Singapore, Baku) where DNF risk is high
- **Auto Pilot** is useful when form is unclear or multiple drivers on your team could be top scorer
- **Final Fix** is insurance — use when a driver has a qualifying incident or mechanical issue
- **Wildcard** is best after a major form shift mid-season when multiple transfers are needed

## 2026 Rule Changes (vs 2025)

### 1. Sprint DNF Penalty Reduced
- Was: -20 pts for DNF/NC in Sprint
- Now: -10 pts
- Addresses community feedback about harsh penalties

### 2. Net Transfer Calculation
- Transfers now based on "net change from previous race"
- Swapping a driver out then back = 0 transfers used
- Allows experimentation without accidentally locking in wrong team

### 3. Price Floor Reduced
- Was: $4.5M minimum
- Now: $3M minimum
- Drivers can lose more value before hitting floor
- Creates more budget flexibility for cheap assets

### 4. Global League Prize Eligibility
- Was: Only "Team 1" eligible for prizes
- Now: Any of your 3 teams can win Global League prizes
- Still limited to one prize per account

### 5. Everything Else Unchanged
- $100M cost cap retained
- 5 drivers + 2 constructors
- Six power chips
- Two free transfers per GP
- Dynamic pricing based on performance

## Price Change Algorithm

### How It Works
- Prices update after each race based on performance
- Weighs the last 3 races equally (2/3 already determined, 1/3 from latest race)
- Two tiers: A Tier (>$20M) and B Tier (<$20M) with different adjustment magnitudes

### Points Per Million (PPM)
- PPM = Score / Price
- Key metric for evaluating value
- A cheap driver scoring 8 points has better PPM than an expensive driver scoring 15

### Budget Growth Strategy
- When a driver's price rises $1M, your budget effectively increases by $1M
- Pick underpriced drivers early -> price rises -> more budget later
- Example: Bearman at $7.4M needs only 9 pts for maximum price gain
- Early-season budget growth enables stronger teams for later rounds

## Key Deadlines

- Team must be locked before qualifying starts each race weekend
- Transfers reset after each race
- Australian GP 2026 deadline: Before qualifying, Saturday March 7
