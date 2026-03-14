---
name: fetch-weather
description: Fetch weekend weather forecast for a race
user-invocable: true
---

# Fetch Weather

Get the weather forecast for qualifying and race day to inform chip decisions and strategy.

## Input

- **Race name** (optional) — defaults to next/current race from `data/2026-calendar.md`

## Source

Web search for:
- "{city} weather {qualifying date}"
- "{city} weather {race date}"

Use `data/2026-calendar.md` to look up the city and dates.

## Output

Save to `data/r{XX}-{race-name}/weather.md`:

```markdown
# Weather Forecast — {Race Name}

## Qualifying — {Day, Date}
- Conditions: {sunny/cloudy/rain expected/etc.}
- Temperature: {XX}°C
- Precipitation: {XX}%
- Wind: {XX} km/h

## Race — {Day, Date}
- Conditions: {sunny/cloudy/rain expected/etc.}
- Temperature: {XX}°C
- Precipitation: {XX}%
- Wind: {XX} km/h

## Fantasy Implications
- {e.g. "Rain likely → high variance weekend, consider No Negative chip"}
- {e.g. "Extreme heat → tire degradation concerns, favor teams with good deg"}
- {e.g. "Dry and mild → rely on practice pace data"}
```

## Fantasy Implications Guide

| Condition | Implication |
|-----------|-------------|
| Rain expected | High variance — consider No Negative chip, wet-weather specialists gain value |
| Extreme heat (>35°C) | Tire degradation concerns — favor teams/drivers good on tire management |
| Strong wind (>30 km/h) | Can affect aero-sensitive cars differently |
| Dry/mild | Normal conditions — rely on practice pace data |

## Notes

- Weather forecasts become more reliable closer to the event — note confidence level
- If the race is more than 5 days away, note that the forecast may change significantly
