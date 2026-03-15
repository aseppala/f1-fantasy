---
name: analyze-form
description: Analyze driver and constructor form trends from recent rounds
user-invocable: true
---

# Analyze Form

Analyze driver and constructor form over recent rounds using fantasy points data.

## Input

- **Rounds to look back** (optional) — default: 3 (or all available if fewer than 3 completed)
- **Save to file** (optional) — if specified, saves output to `data/r{XX}-{race-name}/form-analysis.md`

## Data Sources

Read `fantasy-points.md` files from the last N round folders (`data/r{XX}-{race-name}/fantasy-points.md`).

Also read:
- `data/2026-preseason-testing.md` — baseline pace data for pecking order comparison
- `data/2026-standings.md` — cumulative championship position

## Driver Form Analysis

For each driver, extract from `fantasy-points.md`:

| Metric | Source Field |
|--------|-------------|
| Fantasy points per round | `GamedayPoints` |
| Session breakdown | `SessionWisePoints[]` (qualifying vs race vs sprint contributions) |
| Overtakes | `AdditionalStats.overtakes` |
| DOTD wins | `AdditionalStats.dotd` |
| Fastest laps | `AdditionalStats.fastest_lap` |
| Positions gained/lost | `AdditionalStats.total_position_gained_lost` |
| DNF/DQ penalties | `AdditionalStats.total_dnf_dq_pts` |
| Price trajectory | `Value` vs `OldPlayerValue` |
| Ownership | `SelectedPercentage`, `CaptainSelectedPercentage` |

### Output: Driver Form Table

| Driver | Team | Price | R{n-2} | R{n-1} | R{n} | Avg | Trend | Reliability | Overtake Rate | Ownership% | Captain% |
|--------|------|-------|--------|--------|------|-----|-------|-------------|---------------|-----------|----------|

**Trend:** Rising (3+ consecutive increase), Falling (3+ consecutive decrease), Stable, or Volatile (big swings).

## Constructor Form Analysis

Same approach for constructors:

| Constructor | Price | R{n-2} | R{n-1} | R{n} | Avg | Trend | Quali Bonus Avg | Pit Stop Bonus Avg | Reliability | Ownership% |
|-------------|-------|--------|--------|------|-----|-------|----------------|-------------------|-------------|-----------|

## Pecking Order Evolution

Compare the current pecking order (from recent form) against:
1. Preseason testing rankings
2. R01 results
3. Most recent round

Present as a table showing movement:

| Team | Testing | R01 | Current | Movement |
|------|---------|-----|---------|----------|

## Circuit Fit Analysis

After the main form tables, add a circuit fit section for the upcoming race.

**Step:** Look up the upcoming circuit in `data/circuits.md` and cross-reference each driver/constructor's form against historical circuit results.

### Circuit Fit Table

| Driver/Constructor | Circuit King? | Recent Circuit Results | Fit Signal |
|--------------------|--------------|------------------------|------------|
| (e.g. Leclerc) | Yes — Monaco 2× wins | 1st 2024, 1st 2025 | ✅ Strong |
| (e.g. Verstappen) | Yes — Suzuka 3× wins | 1st 2023, 1st 2024 | ✅ Strong |

**Fit Signals:**
- ✅ Strong — circuit king (2+ wins or podiums at this track)
- ➡️ Neutral — no strong historical data either way
- ⚠️ Weak — historically poor at this track or track type doesn't suit team

**Notes for circuit fit:**
- Check `type` field — power circuits favor high-straight-speed teams (Mercedes, Red Bull historically); downforce circuits favor aerodynamically efficient cars
- Check `overtaking_index` — low index (≤3) means qualifying position is critical; high index (≥7) means race pace + overtake factor matter more
- Check `circuit_kings` field for driver-specific historical advantages
- Note `sc_probability` — high SC circuits increase variance and favor midfield starters with high overtake potential

## Notes

- If fewer than 3 rounds of data exist, use what's available and note the limited sample
- Flag any driver/constructor with DNF in recent rounds as a reliability concern
- Highlight drivers with high overtake rates — these are hidden fantasy value (overtake + position gained points)
- Flag ownership for differentiation: low ownership + good form = high value in friends league
