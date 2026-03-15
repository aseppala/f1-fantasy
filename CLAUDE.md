# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AI-assisted F1 Fantasy 2026 team management. Three differentiated fantasy teams are run in a friends league on fantasy.formula1.com, using Claude Code skills and an orchestrator agent to make data-driven picks each race weekend.

## Architecture

The system has no traditional build/test/lint pipeline. It is a **data + skills + agent** setup:

- **`.claude/skills/`** — Individual slash-command skills (fetch data, analyze, simulate, pick teams). Each skill has a `SKILL.md` that fully defines its behavior.
- **`.claude/agents/f1-fantasy.md`** — Orchestrator agent that chains skills into a full race weekend pipeline: Fetch → Analyze → Build.
- **`.claude/skills/simulate/simulator.py`** — Python 3.10+ Monte Carlo engine (no external dependencies). Run with: `python .claude/skills/simulate/simulator.py --race <name> --sims 10000 --seed 42`
- **`data/`** — All persistent state. Season-level files at root, round-specific data in `data/r{XX}-{race-name}/` folders.

## Skill Pipeline

```
/fetch-session-results  →  /analyze-form       →  /simulate
/fetch-fantasy-points   →  /analyze-value       →  /pick-team
/fetch-tyre-data        →  /optimize-transfers
/fetch-weather
/fetch-standings

Post-race: /validate   (compare predictions to actual results, calibrate next round)
```

Or run the full pipeline via the `/f1-fantasy` agent.

## Data Conventions

- Round folders: `data/r{XX}-{race-name}/` (e.g., `data/r01-australia/`, `data/r02-china/`)
- Team pick files: `data/r{XX}-{race-name}/team-{N}-{slug}.md` where slug is lowercase-hyphenated team name
- Prices must come from confirmed `prices.md` or `fantasy-points.md` files — never estimate prices
- Team files must include: actual squad, total budget, transfers used, chips used/remaining (needed for next round calculations)
- Always check what data files already exist before fetching — don't re-fetch

## Three Teams

Each team has a distinct philosophy defined in `data/team-strategy.md`. Never copy picks across teams. Team identities:

1. **Safe** — ride the dominant constructor, low variance
2. **Constructor Kings** — premium constructors, budget drivers
3. **Ferrari Nuclear** — both Ferrari drivers + constructor, max concentration

## Key Rules

- Budget is per-team (not always $100M — tracks price appreciation of owned assets)
- 2 free transfers per GP, max 1 carry-over, extra transfers cost -10 pts each
- 6 one-time power chips per team (No Negative, Auto Pilot, Final Fix available R1; Limitless, Wildcard, x3 Boost available R2+)
- Max 2 drivers from the same constructor per team
- PPM (Points Per Million) is the core evaluation metric

## Data Sources

| Source | URL Pattern | Data |
|--------|------------|------|
| formula1.com | `/en/results/2026/races/{id}/{name}/{session}` | Session results, standings |
| fantasy.formula1.com | Public JSON feeds | Fantasy points, prices, ownership |
| Pirelli / CoffeeCornerMotorsport | Press releases | Tire allocations, per-driver usage |
