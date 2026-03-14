---
name: fetch-fantasy-points
description: Fetch fantasy points data from the F1 Fantasy API
user-invocable: true
---

# Fetch Fantasy Points

Fetch driver and constructor fantasy points from the official F1 Fantasy API.

## Input

- **Round number** (optional) — defaults to latest completed round. Can also specify "all" to backfill all completed rounds.

## Source

`https://fantasy.formula1.com/feeds/drivers/{gamedayId}_en.json`

Where `{gamedayId}` = round number (1 = Round 1, 2 = Round 2, etc.).

No authentication required.

## Logic

1. Determine which rounds need fetching by checking for existing `fantasy-points.md` files in each round folder
2. Fetch the JSON for each missing round
3. The feed contains both **drivers** (`Skill: 1`) and **constructors** (`Skill: 2`) in the same response
4. If any `SessionWisePoints` entry is `null`, the round is incomplete — note this in the file header

## Key Fields to Extract

| Field | Description |
|-------|-------------|
| `GamedayPoints` | Points scored this round |
| `OverallPpints` | Cumulative season points (note: API typo is intentional) |
| `Value` | Current price |
| `OldPlayerValue` | Previous price (for delta calculation) |
| `SelectedPercentage` | Ownership % |
| `CaptainSelectedPercentage` | Captain pick % |
| `SessionWisePoints[]` | Per-session breakdown (qualifying, race, sprint, etc.) |
| `AdditionalStats` | Overtakes, DOTD, fastest lap, position pts, DNF/DQ pts, VFM |

## Output

Save to `data/r{XX}-{race-name}/fantasy-points.md` with:

1. Header noting the round, date, and whether data is complete or partial
2. **Driver Points Table** — sorted by GamedayPoints descending:
   - Driver, Team, GamedayPoints, OverallPoints, Value, PriceDelta, Selected%, Captain%, key AdditionalStats
3. **Constructor Points Table** — sorted by GamedayPoints descending:
   - Constructor, GamedayPoints, OverallPoints, Value, PriceDelta, Selected%
4. **Session Breakdown** — per-session points for each driver/constructor

## Notes

- Mid-round fetches will have `null` for incomplete sessions — flag this clearly in the header
- Price delta = `Value - OldPlayerValue`
- Create round folder if it doesn't exist
