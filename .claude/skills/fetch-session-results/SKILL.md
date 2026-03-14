---
name: fetch-session-results
description: Fetch F1 race/qualifying/practice/sprint results from formula1.com
user-invocable: true
---

# Fetch Session Results

Fetch official session results from formula1.com and save them to the round folder.

## Input

- **Race name or round number** (optional) — defaults to next/current race from `data/2026-calendar.md`
- **Specific session** (optional) — e.g. "qualifying only", "FP1" — defaults to all available sessions

## Source

Use `data/2026-calendar.md` to look up:
- Race ID (for URL construction)
- Race name slug
- Whether it's a sprint weekend

URL pattern: `https://www.formula1.com/en/results/2026/races/{race-id}/{race-name}/{session}`

Session URL suffixes:
| Session | URL suffix |
|---------|-----------|
| Free Practice 1 | `practice/1` |
| Free Practice 2 | `practice/2` (non-sprint only) |
| Free Practice 3 | `practice/3` (non-sprint only) |
| Sprint Qualifying | `sprint-qualifying` (sprint only) |
| Sprint | `sprint-results` (sprint only) |
| Qualifying | `qualifying` |
| Race | `race-result` |
| Fastest Laps | `fastest-laps` |

## Logic

1. Read `data/2026-calendar.md` to determine the race ID, name, and weekend type
2. Check which files already exist in `data/r{XX}-{race-name}/`
3. Only fetch sessions that are missing
4. For race results, also fetch fastest laps and merge the fastest lap holder into the race file
5. For sprint weekends: fetch FP1, sprint qualifying, sprint, qualifying, race (no FP2/FP3)
6. For normal weekends: fetch FP1, FP2, FP3, qualifying, race

## Output

Save each session to `data/r{XX}-{race-name}/` as:
- `free-practice-1.md`
- `free-practice-2.md`
- `free-practice-3.md`
- `sprint-qualifying.md`
- `sprint.md`
- `qualifying.md`
- `race.md`

Each file should contain a markdown table with columns appropriate to the session type (Position, Driver, Team, Time/Gap, Laps, etc.).

## Backfill

When invoked by the agent or with `--backfill`, also check previous round folders and fetch any missing session files for completed rounds.

## Notes

- **Only use formula1.com** for session results — no other sources
- If a session hasn't happened yet (future date), skip it and note it in the output
- Create the round folder if it doesn't exist
