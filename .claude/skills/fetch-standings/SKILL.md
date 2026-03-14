---
name: fetch-standings
description: Fetch latest championship standings from formula1.com
user-invocable: true
---

# Fetch Standings

Fetch the latest driver and constructor championship standings.

## Source

- Drivers: `https://www.formula1.com/en/results/2026/drivers`
- Constructors: `https://www.formula1.com/en/results/2026/team`

## Output

Update `data/2026-standings.md` with:

```markdown
# 2026 Championship Standings

*Updated: {date}*

## Driver Standings
| Pos | Driver | Team | Points |
|-----|--------|------|--------|
| 1   | ...    | ...  | ...    |

## Constructor Standings
| Pos | Constructor | Points |
|-----|-------------|--------|
| 1   | ...         | ...    |
```

## Notes

- Always overwrite the full file with fresh data
- Only use formula1.com as the source
- If the season hasn't started yet, note "No results available"
