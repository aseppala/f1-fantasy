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

## Steps

### 1. Load existing data

Read **all** of the following to build a complete picture:

**Season-level files in `data/`:**
- `data/2026-calendar.md` — race calendar, sprint weekends, race IDs for URL construction
- `data/2026-fantasy-rules.md` — scoring system, chips, transfer rules
- `data/2026-standings.md` — current driver and constructor championship standings
- `data/2026-prices.md` — price tracker across rounds with ownership percentages
- `data/2026-preseason-testing.md` — baseline pace data (less relevant as season progresses)
- `data/team-strategy.md` — the three team strategies (Safe, Constructor Kings, Ferrari Nuclear)

**Previous round folders (`data/r{XX}-{race-name}/`):**
- `prices.md` — confirmed prices and deltas for that round
- `qualifying.md` — full qualifying classification
- `race.md` — full race result with finishing positions, gaps, DNFs, fastest lap
- `practice.md` / `free-practice-1.md` — practice session results
- `sprint-qualifying.md` — sprint qualifying results (sprint weekends only)
- `team-1-safe.md`, `team-2-constructor-kings.md`, `team-3-ferrari-nuclear.md` — previous team picks

**Current round folder (if it exists):**
- Any practice, sprint qualifying, or qualifying results already saved
- Any price data already captured

Read **at minimum** the last 3 rounds of race results and prices to assess form trends.

### 1b. Backfill missing round data

For each previous round folder, check if the following files exist. If any are **missing**, fetch them from formula1.com and save them before proceeding:

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

Check `data/2026-calendar.md` to determine race IDs and whether each round is a sprint weekend.

Also update `data/2026-standings.md` with the latest driver and constructor championship standings from `https://www.formula1.com/en/results/2026/drivers` and `https://www.formula1.com/en/results/2026/team`.

**File format conventions:**
- Each file should have a heading with the round, GP name, session type, date, and circuit
- Qualifying: full classification with Q1/Q2/Q3 times and laps
- Race: full classification with position, driver, team, laps, time/gap/status, points. Include fastest lap holder, all DNFs/DNS with lap retired.
- Practice: position, driver, team, time, gap to leader
- Sprint: same format as race but for sprint distance
- Prices: driver/constructor tables with price, delta from previous round, ownership %, fantasy points scored

### 2. Assess form and trends

Before researching new data, analyze what's already in the files:

**Driver form (last 3 races):**
For each driver, track:
- Qualifying positions (trend: improving, stable, declining?)
- Race finishing positions (trend)
- Fantasy points scored per round
- Price trajectory (rising = good form, falling = poor form or buy opportunity)
- DNF/DNS count (reliability flag)
- Positions gained per race (overtaking ability)

**Constructor form (last 3 races):**
For each constructor, track:
- Combined qualifying performance (both drivers in Q3? One in Q1?)
- Combined race points
- Fantasy points scored per round
- Reliability (any DNFs from either driver?)
- Price trajectory

**Pecking order evolution:**
Compare the current pecking order against:
- Preseason testing rankings
- Round 1 results
- Most recent round results
Flag any teams that have moved up or down significantly.

Summarize findings as a **form table**:

| Driver | Last 3 Races | Trend | Reliability | Notes |
|--------|-------------|-------|-------------|-------|

### 3. Research current weekend

**IMPORTANT: Only use formula1.com for race results, practice, qualifying, and standings data.**

Use `data/2026-calendar.md` to find the correct race ID, then fetch results from formula1.com:
- Practice: `https://www.formula1.com/en/results/2026/races/{race-id}/{race-name}/practice/{session-number}`
- Sprint Qualifying: check if this is a sprint weekend first
- Qualifying: `https://www.formula1.com/en/results/2026/races/{race-id}/{race-name}/qualifying`
- Race results: `https://www.formula1.com/en/results/2026/races/{race-id}/{race-name}/race-result`
- Driver standings: `https://www.formula1.com/en/results/2026/drivers`

Fetch all available sessions for the current weekend. Save each to the round folder as separate files:
- `free-practice-1.md`, `free-practice-2.md`, `free-practice-3.md`
- `sprint-qualifying.md` (sprint weekends)
- `qualifying.md`

**Weather forecast:**
Search for "{city} weather {qualifying date}" and "{city} weather {race date}".
- Race day weather carries MORE weight than qualifying weather
- Rain → high variance, favors wet-weather specialists, consider No Negative chip
- Extreme heat → tire degradation, favors teams with good tire management
- Dry/mild → rely on practice pace data

### 4. Determine current prices and budget

Check the most recent `prices.md` file for confirmed prices. If the user provides updated prices, use those.

For each of the 3 teams, calculate:
- Current squad value (what was locked in last round, adjusted for price changes)
- Available budget
- Free transfers available (2 per round, +1 carry-over if unused last round)

### 5. Analyze value

For each potential pick, calculate:
- **Expected Points** based on form, practice pace, and circuit characteristics
- **PPM = Expected Points / Price**
- **Price trend** — is the driver likely to rise or fall after this round?
- **Ownership %** — low ownership = differentiation opportunity in friends league

Flag:
- Drivers with high PPM who are rising in price (buy before they get expensive)
- Drivers with declining form who are still expensive (avoid or sell)
- Budget drivers who could score big from overtaking (qualify low, race high)

### 6. Build teams

Read `data/team-strategy.md` for the three strategies, then build each team:

**Team 1: "Safe"**
- Follow the dominant constructor, don't bet against the best team
- 1-2 premium drivers from the top team(s)
- Budget-second-driver approach (cheaper driver from top teams)
- 2x on the form driver of the dominant team

**Team 2: "Constructor Kings"**
- Stack the 2 best constructors
- Budget drivers only (no $20M+ drivers)
- 2x on the highest-ceiling budget driver
- Maximize constructor synergy

**Team 3: "Ferrari Nuclear"**
- Both Ferrari drivers + Ferrari constructor, always
- 2x on whichever Ferrari driver is faster this weekend
- Never dilute the Ferrari concentration
- Run a Ferrari Health Check (see strategy file)

For each team, respect:
- $100M budget (unless using Limitless)
- Max 2 drivers from the same constructor
- Available transfers (only changes from last round's team that fit within free transfer count)
- Chip strategy per team from `data/team-strategy.md`

### 7. Run scoring simulation

Update `simulator.py` with current weekend profiles based on practice/qualifying data, then run:
```bash
python simulator.py --race {race} --sims 10000 --seed 42
```

Include team variants to test key decisions:
- Alternative 2x captain choices
- Alternative driver swaps
- Different constructor pairings

If simulation disagrees with manual analysis, investigate and explain why.

### 8. Present each team

For each of the 3 teams, output:

**Header:** Team name, chip used (or "None"), strategy summary

**Driver table:**
| # | Driver | Team | Price | Exp. Pts | PPM | Rationale |

**Constructor table:**
| # | Constructor | Price | Exp. Pts | PPM | Rationale |

**Footer:**
- Total cost and budget remaining
- Simulation average, std dev, min, max
- 2x driver choice and reasoning
- Transfers made from previous round
- Key risks

Then a **simulation comparison table** across all teams and variants.

### 9. Save outputs

Create the round folder `data/r{XX}-{race-name}/` if it doesn't exist.

Save each team to a separate file:
- `data/r{XX}-{race-name}/team-1-safe.md`
- `data/r{XX}-{race-name}/team-2-constructor-kings.md`
- `data/r{XX}-{race-name}/team-3-ferrari-nuclear.md`

Save session results to separate files:
- `data/r{XX}-{race-name}/free-practice-1.md` (etc.)
- `data/r{XX}-{race-name}/sprint-qualifying.md`
- `data/r{XX}-{race-name}/prices.md` (if new price data available)

Update `data/2026-standings.md` if new race results are available.

Do NOT overwrite `data/2026-prices.md` — that file is the master tracker and should only be updated with confirmed prices from the user.

## Important Notes

- Constructors score from BOTH drivers — a constructor with two top-5 drivers beats one with a P1 and a P15
- Overtaking points matter — drivers who qualify low but race high have hidden value
- Price changes weigh last 3 races equally — factor in trajectory, not just this week
- In a friends league, differentiation wins — don't just copy the consensus team
- When uncertain between two picks at similar price, prefer the one with higher ceiling
- Sprint weekends are worth ~30-50% more points — factor this into chip decisions
- Always use confirmed prices from the user or from `prices.md` files — do not estimate prices
