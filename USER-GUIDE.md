# User Guide

## Quick Start

Open the project in Claude Code:

```bash
cd f1-fantasy
claude
```

For a full race weekend workflow, run the agent:

```
> @f1-fantasy
```

Or run individual skills as needed — see the skill reference below.

## Race Weekend Workflow

A typical race weekend follows this sequence. The `@f1-fantasy` agent runs all steps automatically, pausing at decision points for your input.

### 1. Fetch data

```
> /fetch-session-results         # grab FP1/FP2/FP3/quali/race from F1.com
> /fetch-fantasy-points          # pull scoring data from the Fantasy API
> /fetch-tyre-data               # add tire compound info to session files
> /fetch-weather                 # get forecast for quali & race day
> /fetch-standings               # update championship standings
```

Each fetch skill checks what already exists and only downloads missing data. Safe to re-run.

### 2. Analyze

```
> /analyze-form                  # form trends over last 3 rounds
> /analyze-value                 # expected points, PPM, buy/sell signals
> /optimize-transfers            # recommended transfers per team
```

Review the analysis before proceeding. You can ask follow-up questions or adjust assumptions.

### 3. Build teams

```
> /simulate                      # Monte Carlo simulation with team variants
> /pick-team                     # final team selections
```

`/pick-team` reads the analysis and simulation results, applies your team strategies from `data/team-strategy.md`, and produces team files with full budget and transfer accounting.

## Skill Reference

### Data Fetching

| Skill | What it does | Example |
|-------|-------------|---------|
| `/fetch-session-results` | Fetches race/quali/practice results from formula1.com | `/fetch-session-results` or `/fetch-session-results Monaco` |
| `/fetch-fantasy-points` | Fetches fantasy points from the F1 Fantasy API | `/fetch-fantasy-points` or `/fetch-fantasy-points all` (backfill) |
| `/fetch-tyre-data` | Adds tire compound data to session files | `/fetch-tyre-data China` |
| `/fetch-weather` | Gets weather forecast for a race weekend | `/fetch-weather` |
| `/fetch-standings` | Updates championship standings | `/fetch-standings` |

### Analysis

| Skill | What it does | Example |
|-------|-------------|---------|
| `/analyze-form` | Analyzes driver/constructor form over recent rounds | `/analyze-form` (last 3) or `/analyze-form 5` (last 5) |
| `/analyze-value` | Calculates PPM, price trends, buy/sell signals | `/analyze-value` |
| `/optimize-transfers` | Recommends transfers per team within constraints | `/optimize-transfers` or `/optimize-transfers Team 2` |

### Building

| Skill | What it does | Example |
|-------|-------------|---------|
| `/simulate` | Runs Monte Carlo scoring simulation | `/simulate` or `/simulate China` |
| `/pick-team` | Builds final team selections | `/pick-team` or `/pick-team must include Verstappen` |

## Managing Your Teams

### Team strategy

Your three team philosophies are defined in `data/team-strategy.md`. Edit this file to change construction rules, chip plans, or risk tolerance. The `/pick-team` skill reads it every time.

### Budget tracking

Each team file (`data/r{XX}-{race-name}/team-{N}-{slug}.md`) records:
- Current squad with prices
- Total budget (not always $100M — grows/shrinks with price changes)
- Transfers used and carry-over status
- Chips used and remaining

These carry forward to the next round automatically.

### Transfers

You get 2 free transfers per round per team. If you used fewer than 2 last round, 1 carries over (max 3 total). Extra transfers cost -10 points each.

`/optimize-transfers` respects these limits and only suggests paid transfers when the expected gain exceeds +15 points net (after the penalty).

### Chips

Six one-time-use chips, max one per weekend:

| Chip | When | What it does |
|------|------|-------------|
| No Negative | Round 1+ | Zeroes out all negative scoring categories |
| Auto Pilot | Round 1+ | Auto-assigns 2x to your highest scorer |
| Final Fix | Round 1+ | Swap one driver after lock, before race |
| Limitless | Round 2+ | Ignore budget + unlimited transfers (team reverts next round) |
| Wildcard | Round 2+ | Unlimited transfers within budget (permanent) |
| x3 Boost | Round 2+ | Triple one driver's score (can still 2x another) |

Chip strategy per team is tracked in `data/team-strategy.md`.

## Data Files

### Season-level (in `data/`)

| File | Purpose |
|------|---------|
| `2026-calendar.md` | Full calendar with sprint flags and race IDs |
| `2026-driver-lineups.md` | All drivers, teams, and starting prices |
| `2026-fantasy-rules.md` | Complete scoring and rules reference |
| `2026-preseason-testing.md` | Bahrain testing pace data |
| `2026-prices.md` | Price tracker across rounds |
| `2026-standings.md` | Latest championship standings |
| `team-strategy.md` | Your team philosophies and construction rules |

### Round-level (in `data/r{XX}-{race-name}/`)

Each completed round folder contains:
- Session results: `free-practice-{1,2,3}.md`, `qualifying.md`, `race.md`
- Sprint sessions (sprint weekends only): `sprint-qualifying.md`, `sprint.md`
- `fantasy-points.md` — official scoring from the Fantasy API
- `prices.md` — confirmed prices for that round
- `weather.md` — weekend weather forecast
- `form-analysis.md`, `value-analysis.md` — analysis outputs
- `team-{N}-{slug}.md` — your team picks with full accounting

## Running the Simulator Directly

The Monte Carlo simulator can be run as a standalone Python script:

```bash
# Default (Australia, 1000 sims)
python .claude/skills/simulate/simulator.py

# Specific race, more sims, fixed seed
python .claude/skills/simulate/simulator.py --race china --sims 10000 --seed 42

# Custom team
python .claude/skills/simulate/simulator.py \
  --team "Russell,Antonelli,Norris,Bearman,Lindblad" \
  --constructors "Mercedes,Haas" \
  --captain Russell \
  --sims 10000 --seed 42

# Driver rankings only
python .claude/skills/simulate/simulator.py --drivers-only --sims 5000
```

No external dependencies — just Python 3.10+.

## Tips

- **Sprint weekends** generate 30-50% more points than normal weekends. Good time for offensive chips (Limitless, x3 Boost).
- **PPM is king.** A $7M driver averaging 15 pts (2.14 PPM) beats a $25M driver averaging 40 pts (1.60 PPM) because the budget savings unlock better picks elsewhere.
- **Overtaking = hidden value.** Drivers who qualify low but race high earn both position-gained and overtake points. Budget midfielders with good race pace are the best value.
- **Constructors score from both drivers.** Two consistent top-8 finishers beats P1 + P15. Ferrari with Leclerc and Hamilton is the ceiling play.
- **Differentiation wins in friends leagues.** When in doubt, pick the less-owned option at similar expected points.
- **Price appreciation is an investment.** Buying rising drivers early preserves future budget flexibility.
