---
name: fetch-fantasy-points
description: Fetch fantasy points data from the F1 Fantasy API
user-invocable: true
---

# Fetch Fantasy Points

Fetch driver and constructor fantasy points from the official F1 Fantasy API.

## Input

- **Round number** (optional) — defaults to latest completed round. Can also specify "all" to backfill all completed rounds.

## Sources

### 1. Gameday feed (summary)
`https://fantasy.formula1.com/feeds/drivers/{gamedayId}_en.json`

Where `{gamedayId}` = round number (1 = Round 1, 2 = Round 2, etc.).
Contains all drivers and constructors. Extract `PlayerId` from each entry for use in the detail feed.

### 2. Player stats feed (per-player detail)
`https://fantasy.formula1.com/feeds/popup/playerstats_{playerId}.json`

One request per player (22 drivers + 11 constructors = 33 requests). Fetch all in parallel.
Contains round-specific scoring breakdown — this is the authoritative source for per-session and per-stat points.

No authentication required for either endpoint.

## Logic

1. Determine which rounds need fetching by checking for existing `fantasy-points.md` files in each round folder
2. Fetch the gameday JSON for each missing round
3. The feed contains both **drivers** (`Skill: 1`) and **constructors** (`Skill: 2`) in the same response
4. Extract `PlayerId` for every player in the gameday feed
5. Fetch `playerstats_{playerId}.json` for each player (all in parallel)
6. From each player stats response, extract the entry in `Value.MatchWiseStats` where `RaceDayWise[].MeetingNumber` matches the current round — this gives round-specific session stats
7. If any `SessionWisePoints` entry is `null` in the gameday feed, the round is incomplete — note this in the file header

> ⚠️ **Important:** `AdditionalStats` fields in the gameday feed (Overtakes, DOTD, FastestLap, etc.) are **cumulative season totals**, not round-specific. Always use the `playerstats` feed for round-specific stat breakdowns.

## Key Fields — Gameday Feed

| Field | Description |
|-------|-------------|
| `PlayerId` | Player ID — use to fetch detail stats |
| `GamedayPoints` | Points scored this round (round-specific ✓) |
| `OverallPpints` | Cumulative season points — API typo is intentional |
| `Value` | Current price |
| `OldPlayerValue` | Previous price (for delta calculation) |
| `SelectedPercentage` | Ownership % |
| `CaptainSelectedPercentage` | Captain pick % |
| `AdditionalStats` | **Cumulative season totals** — do not treat as round-specific |

## Key Fields — Player Stats Feed (`playerstats_{id}.json`)

All fields are nested under `Value`:

| Field path | Description |
|------------|-------------|
| `PlayerId` | Confirms player identity |
| `GamedayWiseStats[{round}].StatsWise[]` | Per-round stats: `Event`, `Frequency`, `Value` tuples |
| `MatchWiseStats[].RaceDayWise[]` | Per-session breakdown with `SessionName`, `SessionType`, `MeetingNumber`, `StatsWise[]` |
| `FixtureWiseStats[].RaceDayWise[]` | Per-session with ownership/captain % per session |
| `TourWiseStats[].StatsWise[]` | Season total stats |

### StatsWise event names (examples)
Each `StatsWise` entry has `Event` (stat name), `Frequency` (occurrences), `Value` (fantasy points from that stat):

| Event | What it means |
|-------|--------------|
| `QUALIFYING_POSITION` | Qualifying position points |
| `RACE_POSITION` | Race finishing position points |
| `SPRINT_POSITION` | Sprint race position points |
| `POSITIONS_GAINED` | +1 pt per net position gained |
| `OVERTAKE` | Overtake bonus points |
| `FASTEST_LAP` | +10 pts fastest lap |
| `DRIVER_OF_THE_DAY` | +10 pts DOTD |
| `DNF` / `DQ` | Negative points for retirement/disqualification |
| `PIT_STOP` | Constructor pit stop bonus |
| `QUALIFYING_BONUS` | Constructor Q3/Q2 appearance bonus |

## Output

Save to `data/r{XX}-{race-name}/fantasy-points.md` with:

1. Header noting the round, date, and whether data is complete or partial
2. **Driver Points Table** — sorted by GamedayPoints descending:
   - Driver, Team, GamedayPoints, OverallPoints, Value, PriceDelta, Selected%, Captain%
3. **Constructor Points Table** — sorted by GamedayPoints descending:
   - Constructor, GamedayPoints, OverallPoints, Value, PriceDelta, Selected%
4. **Per-Player Session Breakdown** (from player stats feed) — for each driver and constructor, a row per session showing session name and points, plus a stat breakdown (qualifying pts, race pts, positions gained, overtakes, FL, DOTD, DNF — all round-specific)

## Notes

- Fetch all 33 player stats requests in parallel after the gameday feed
- Match `MeetingNumber` in the player stats to the current round number
- Mid-round fetches will have incomplete sessions — flag this clearly in the header
- Price delta = `Value - OldPlayerValue`
- Create round folder if it doesn't exist
