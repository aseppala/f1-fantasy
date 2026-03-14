---
name: simulate
description: Run Monte Carlo simulation for F1 Fantasy scoring
user-invocable: true
---

# Simulate

Run Monte Carlo simulations to estimate expected fantasy points for drivers, constructors, and team configurations.

## Input

- **Race name** (optional) — defaults to next/current race from `data/2026-calendar.md`
- **Sims** (optional) — number of simulations, default: 10000
- **Seed** (optional) — random seed for reproducibility, default: 42
- **Teams** (optional) — specific team variants to simulate. If not provided, uses teams from previous round files + transfer recommendations.

## Prerequisites

Before running the simulation, ensure you have:
- Practice pace data (from `/fetch-session-results`)
- Form analysis (from `/analyze-form`)
- Current prices

## Steps

### 1. Update Driver/Constructor Profiles

Before running `simulator.py`, update the race-specific profiles in the script based on latest data:

- **quali_mean / race_mean:** Based on practice pace, recent qualifying/race positions, and circuit characteristics
- **variance:** Higher for volatile drivers, lower for consistent performers
- **dnf_chance:** Based on reliability history (`AdditionalStats.total_dnf_dq_pts`)
- **overtake_factor:** Based on overtaking rate from form analysis
- **prices:** Current confirmed prices
- **pit_mean:** Constructor pit stop averages from recent rounds

Add a new `get_{race}_profiles()` function and `get_{race}_teams()` function, and register the race in the `--race` choices.

### 2. Define Team Variants

For each team in `data/team-strategy.md`, create:
- The **base team** (after recommended transfers from `/optimize-transfers`)
- **2-3 variants** testing key decisions (different captain, alternative transfers, chip usage)

### 3. Run Simulation

```bash
python .claude/skills/simulate/simulator.py --race {race} --sims 10000 --seed 42
```

### 4. Interpret Results

Present results with:
- Driver rankings by expected fantasy points (avg, std dev, PPM)
- Constructor rankings by expected fantasy points
- Team comparison table (avg, std dev, min, max)
- Key takeaways: which captain choice is optimal, which variant wins

## Scoring Rules (for profile calibration)

**Qualifying:** P1=10, P2=9...P10=1, P11+=0, NC/DSQ=-5
**Race:** P1=25, P2=18, P3=15, P4=12, P5=10, P6=8, P7=6, P8=4, P9=2, P10=1, P11+=0, DNF=-20
**Bonus:** +1/position gained, +1/overtake, +10 fastest lap, +10 DOTD
**Sprint:** P1=8...P8=1, DNF=-10, +5 fastest lap, +1/position gained, +1/overtake
**Constructor Quali:** Both Q3=+10, Both Q2=+5, One Q3=+3, One Q2=+1, Both Q1=-1
**Constructor Race:** Sum of both drivers' race points. Pit stop bonuses: <2.0s=+10, 2.0-2.19s=+10, 2.2-2.49s=+5, 2.5-2.99s=+2, fastest stop=+5 extra

## Notes

- Always update profiles before running — stale profiles produce misleading results
- Use `--seed 42` for reproducibility unless exploring variance
- The simulator models normal weekends; sprint weekends need additional sprint scoring (future enhancement)
- Simulation is a tool for comparison, not prediction — focus on relative rankings, not absolute numbers
