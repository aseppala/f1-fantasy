---
name: validate
description: Post-race calibration — compare simulation predictions to actual results and generate calibration notes for next round
user-invocable: true
---

# Post-Race Validation

After a race, compare the simulator's predicted point distributions against actual fantasy points. Identify systematic over/under-predictions and generate calibration notes for the next round's driver profiles.

## Input

- **Race round/name** — the round just completed (e.g. "r02-china")

## Data Sources

Read:
- `data/r{XX}-{race-name}/sim-output.md` or the most recent simulation run output (look for any saved sim results)
- `data/r{XX}-{race-name}/fantasy-points.md` — actual fantasy points (fetch if not present)
- `data/r{XX}-{race-name}/` — any qualifying/race session result files for position context

## Steps

### 1. Load Predicted vs Actual

Build a comparison table. If a saved sim output is available, use those expected-points numbers. Otherwise reconstruct expected points from the driver profiles in `simulator.py` for the relevant race.

| Driver | Predicted (med) | Actual Pts | Delta | Notes |
|--------|----------------|------------|-------|-------|
| Russell | 42 | 61 | +19 | Dominated — qualifying and race mean both too low |
| Hamilton | 38 | 22 | -16 | DNF not in profile — dnf_chance too low |

### 2. Classify Each Driver's Prediction Error

For each driver with |delta| > 10 pts, classify the miss:

| Error Type | Description |
|-----------|-------------|
| **Pace miss** | Driver consistently faster/slower than predicted quali_mean or race_mean |
| **DNF miss** | Unexpected retirement — dnf_chance was too low |
| **Overtake miss** | Overtake scoring higher/lower than overtake_factor predicted |
| **DOTD miss** | Won DOTD when not expected — or favored driver didn't win |
| **Sprint miss** | Sprint-specific results diverged from expected (sprint weekends only) |

### 3. Constructor Calibration

Compare predicted vs actual constructor points:

| Constructor | Predicted (med) | Actual | Delta | Key Driver |
|-------------|----------------|--------|-------|------------|
| Mercedes | 55 | 72 | +17 | Both drivers finished P1/P2 |

Identify pit stop bonus over/underestimation and quali bonus assumptions.

### 4. DOTD Analysis

- Who won DOTD? Was this driver in the top 3 predicted DOTD candidates?
- If not: what was the narrative that swayed votes? (home race? dramatic overtakes? underdog story?)
- Update note: if a driver consistently wins DOTD when not predicted, flag for dotd_weight adjustment

### 5. Generate Calibration Notes

Output a block suitable for pasting into the next round's simulator profile comments:

```
## Calibration Notes from R{XX} {Race Name}

### Pace Adjustments Suggested
- Russell: race_mean too high by ~2 positions — actually qualified/raced ~1.5 avg
- Hamilton: consider dnf_chance bump to 0.07 (two consecutive retirement risks)

### DOTD Notes
- Hamilton won DOTD despite P4 finish — fan vote dominated; dotd_weight 1.8 correct
- Bearman DOTD miss: P12→P8 overtake narrative wasn't enough against Hamilton popularity

### Overtake Factor Notes
- Shanghai overtaking_index=6 felt right — position gains correlated well with overtake_factor
- Bearman overtake_factor=1.3 underdelivered — only gained 1 position despite starting P10

### Constructor Notes
- Mercedes pit_mean should be ~2.2s — executed two sub-2.2 stops in race
- Haas reliability concern: Ocon mechanical DNF — consider bump to dnf_chance=0.10

### Overall Calibration
- Simulation was [conservative/accurate/optimistic] overall
- Biggest systematic miss: [describe]
- Confidence in R{XX+1} profiles: [high/medium/low] pending more data
```

### 6. Save Output

Save to `data/r{XX}-{race-name}/validation.md`.

## Notes

- If `fantasy-points.md` isn't available yet (race just finished, data lag), note that and prompt user to re-run after data is available
- Focus calibration on drivers who will be in teams next round — don't over-engineer adjustments for drivers not in any squad
- Three or more rounds of calibration notes are needed before patterns become reliable — flag if this is only R01 or R02
- DOTD is inherently noisy (fan vote) — don't over-adjust dotd_weight based on a single race
