---
name: simulate
description: Run Monte Carlo simulation for F1 Fantasy scoring
user-invocable: true
---

# Simulate

Run Monte Carlo simulations to estimate expected fantasy points for drivers, constructors, and team configurations.

## Input

- **Config file** (required) — path to a race-specific JSON config file (e.g. `data/r03-bahrain/sim-config.json`)
- **Sims** (optional) — number of simulations, default: 10000
- **Seed** (optional) — random seed for reproducibility, default: 42

## Prerequisites

Before running the simulation, ensure you have:
- Practice pace data (from `/fetch-session-results`)
- Form analysis (from `/analyze-form`)
- Current confirmed prices

## Steps

### 1. Generate the Config JSON

Create `data/r{XX}-{race-name}/sim-config.json` with driver/constructor profiles derived from latest session data.

**Config format:**
```json
{
  "race": "bahrain",
  "sprint": false,
  "overtaking_index": 7,
  "drivers": [
    {
      "name": "Russell", "team": "Mercedes", "price": 27.7,
      "quali_mean": 1.5, "race_mean": 1.5, "variance": 1.5,
      "dnf_chance": 0.04, "overtake_factor": 1.0, "dotd_weight": 1.0
    }
  ],
  "constructors": [
    {"name": "Mercedes", "price": 27.8, "pit_mean": 2.3}
  ],
  "teams": [
    {
      "name": "Safe PPM",
      "drivers": ["Russell", "Norris", "Bearman", "Bottas", "Lindblad"],
      "constructors": ["Ferrari", "Mercedes"],
      "captain": "Russell"
    }
  ]
}
```

**Profile calibration:**
- `quali_mean` / `race_mean` — lower = faster (rank-based, e.g. 1.5 = likely P1-2). Use practice pace, recent quali/race positions, circuit characteristics.
- `variance` — spread of outcomes. 1.5 for dominant drivers, 3.0–3.5 for midfield.
- `dnf_chance` — per-race DNF probability. Use reliability history from form analysis.
- `overtake_factor` — multiplier on position-gain overtake model. 1.3 for aggressive overtakers.
- `dotd_weight` — fan popularity. 2.0 for Norris, 1.6 for Leclerc, 1.0 for baseline.
- `pit_mean` — constructor average pit time in seconds. 2.2–2.3 for top teams, 2.5–2.8 for backmarkers.
- `overtaking_index` — circuit overtaking difficulty 1–10 (Monaco=1, neutral=5, Monza=10).
- `sprint: true` — activates Sprint Qualifying + Sprint Race scoring.
- `teams` — optional; if absent, only driver/constructor rankings are shown.

### 2. Define Team Variants

For each team in `data/team-strategy.md`, include in `teams` array:
- The **base team** (after recommended transfers from `/optimize-transfers`)
- **2–3 variants** testing key decisions (different captain, alternative transfer, chip usage)

### 3. Run Simulation

```bash
python .claude/skills/simulate/simulator.py --config data/r{XX}-{race}/sim-config.json --sims 10000 --seed 42
```

Other useful flags:
```bash
# Override overtaking index without editing the config
python .claude/skills/simulate/simulator.py --config ... --overtaking-index 8 --sims 10000 --seed 42

# Driver or constructor rankings only
python .claude/skills/simulate/simulator.py --config ... --drivers-only
python .claude/skills/simulate/simulator.py --config ... --constructors-only

# Ad-hoc team (comma-separated, no spaces after commas)
python .claude/skills/simulate/simulator.py --config ... \
  --team "Russell,Norris,Bearman,Bottas,Lindblad" \
  --constructors "Ferrari,Mercedes" \
  --captain Russell
```

### 4. Interpret Results

Present results with:
- Driver rankings by expected fantasy points (avg, std dev, PPM)
- Constructor rankings by expected fantasy points
- Team comparison table (avg, std dev, min, max)
- Key takeaways: optimal captain, which variant wins, sprint premium (if applicable)

## Scoring Rules Reference

**Qualifying:** P1=10, P2=9…P10=1, P11+=0, NC/DSQ=-5
**Race:** P1=25, P2=18, P3=15, P4=12, P5=10, P6=8, P7=6, P8=4, P9=2, P10=1, P11+=0, DNF=-20
**Positions delta:** +1/position gained, -1/position lost (both qualifying→race and sprint)
**Overtakes:** +1 per overtake (only when positions are gained)
**Fastest lap:** +10 (top-10 eligible); Sprint fastest lap: +5 (all finishers eligible)
**DOTD:** +10 (driver only, not counted for constructor)

**Sprint Race:** P1=8…P8=1, P9+=0, DNF=-10, +1/pos gained, -1/pos lost, +5 fastest lap
**Sprint Qualifying:** same points table as main qualifying (P1=10…P10=1)

**Constructor Qualifying Tier:** Both Q3=+10, One Q3=+5, Both Q2=+5, One Q2=+1, Both Q1=-1
**Constructor Race:** Full sum of both drivers' points (excl. DOTD) + qualifying tier + pit stop bonus
**Pit stop:** <2.0s=+20 (+15 extra if world record <1.8s = +35 total), 2.0–2.19s=+10, 2.2–2.49s=+5, 2.5–2.99s=+2, ≥3.0s=0; fastest pit of race=+5

## Notes

- Always generate a fresh config file before running — stale profiles produce misleading results
- Use `--seed 42` for reproducibility unless exploring variance
- Sprint weekend config (`"sprint": true`) adds ~40–60 pts per driver vs non-sprint
- Simulation is a comparison tool, not a predictor — focus on relative rankings and team deltas, not absolute numbers
