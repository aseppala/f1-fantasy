# F1 Fantasy 2026

AI-assisted F1 Fantasy team management for the 2026 season, built on [Claude Code](https://claude.ai/claude-code) skills and agents.

Runs three differentiated fantasy teams in a friends league on [fantasy.formula1.com](https://fantasy.formula1.com), using Monte Carlo simulation, form analysis, and value optimization to make data-driven picks each round.

## How It Works

The system is a set of Claude Code **skills** (individual tasks) orchestrated by an **agent** (end-to-end pipeline). Each skill can be invoked independently via slash commands or chained together by the agent for a full race weekend workflow.

```
  /f1-fantasy agent (full pipeline)
  ┌─────────────────────────────────────────────────────┐
  │                                                     │
  │  Fetch ──────────► Analyze ──────────► Build        │
  │                                                     │
  │  /fetch-session-results   /analyze-form    /simulate│
  │  /fetch-fantasy-points    /analyze-value   /pick-team│
  │  /fetch-tyre-data         /optimize-transfers       │
  │  /fetch-weather                                     │
  │  /fetch-standings                                   │
  │                                                     │
  └─────────────────────────────────────────────────────┘
```

## Project Structure

```
f1-fantasy/
├── .claude/
│   ├── agents/
│   │   └── f1-fantasy.md              # Orchestrator agent
│   └── skills/
│       ├── fetch-session-results/     # F1.com race/quali/practice results
│       ├── fetch-fantasy-points/      # Fantasy API points & ownership data
│       ├── fetch-tyre-data/           # Pirelli compound allocations
│       ├── fetch-weather/             # Weekend weather forecasts
│       ├── fetch-standings/           # Championship standings
│       ├── analyze-form/              # Driver/constructor form trends
│       ├── analyze-value/             # PPM, price trends, buy/sell signals
│       ├── optimize-transfers/        # Per-team transfer recommendations
│       ├── simulate/                  # Monte Carlo simulation engine
│       │   ├── SKILL.md
│       │   └── simulator.py           # Python scoring simulator
│       └── pick-team/                 # Team builder (given analyzed data)
│
├── data/
│   ├── 2026-calendar.md               # 24-race calendar with sprint flags
│   ├── 2026-driver-lineups.md         # All teams, drivers, and prices
│   ├── 2026-fantasy-rules.md          # Scoring, chips, 2026 rule changes
│   ├── 2026-preseason-testing.md      # Bahrain testing pace data
│   ├── 2026-prices.md                 # Price tracker across rounds
│   ├── 2026-standings.md              # Championship standings
│   ├── team-strategy.md               # Team philosophies and construction rules
│   │
│   ├── r01-australia/                 # Round 1 — completed
│   │   ├── free-practice-{1,2,3}.md
│   │   ├── qualifying.md
│   │   ├── race.md
│   │   ├── fantasy-points.md
│   │   ├── prices.md
│   │   └── team-{1,2,3}-*.md          # Team picks with budgets & transfers
│   │
│   └── r02-china/                     # Round 2 — in progress (sprint)
│       ├── free-practice-1.md
│       ├── sprint-qualifying.md
│       ├── fantasy-points.md
│       ├── prices.md
│       └── team-{1,2,3}-*.md
│
└── README.md
```

## Team Strategies

Three teams run in parallel, each with a distinct philosophy to maximize differentiation in a friends league:

| Team | Philosophy | Approach |
|------|-----------|----------|
| **1 — Safe** | Ride the dominant constructor | 1 premium driver per top team, 3 budget drivers, low variance |
| **2 — Constructor Kings** | Premium constructors over premium drivers | 2 expensive constructors, 4-5 budget drivers, constructor scoring ceiling |
| **3 — Ferrari Nuclear** | Double down on Ferrari | Both Ferrari drivers + constructor, high variance, explosive upside |

All three share core principles: PPM optimization, Monte Carlo validation, constructor-driver synergy, overtaking value, price appreciation tracking, and coordinated chip usage.

## Data Sources

| Source | Data | Auth |
|--------|------|------|
| [formula1.com](https://www.formula1.com/en/results/2026) | Session results, standings | None |
| [fantasy.formula1.com](https://fantasy.formula1.com) | Fantasy points, prices, ownership | None (public JSON feeds) |
| [Pirelli](https://press.pirelli.com) | Tire compound allocations | None |
| [CoffeeCornerMotorsport.com](https://coffeecornermotorsport.com) | Per-driver tire usage | None |

## Simulation Engine

`simulator.py` is a Monte Carlo scoring engine that models a full race weekend:

- Qualifying and race position sampling from driver skill distributions
- DNF probability per driver (reliability modeling)
- Overtaking simulation based on qualifying-to-race position deltas
- Fastest lap and Driver of the Day weighted random assignment
- Constructor scoring: qualifying bonuses, race point sums, pit stop time sampling
- Team scoring with captain (2x) multiplier
- Configurable sim count and random seed for reproducibility

Run directly:
```bash
python .claude/skills/simulate/simulator.py --race australia --sims 10000 --seed 42
```

## Requirements

- [Claude Code](https://claude.ai/claude-code) CLI
- Python 3.10+ (for simulator — no external dependencies)
