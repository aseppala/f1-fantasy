---
name: fetch-tyre-data
description: Fetch Pirelli tire allocations and per-driver usage data
user-invocable: true
---

# Fetch Tyre Data

Collect tire compound allocation and per-driver usage data for a race weekend.

## Input

- **Race name** (optional) — defaults to next/current race from `data/2026-calendar.md`

## Sources

1. **Compound allocation (C1-C5 mapping):** Search for the Pirelli press release or F1.com preview article: "What tyres will the teams have for the {race name}". This tells you which C1-C5 compounds are designated Hard/Medium/Soft for this race.

2. **Per-driver tire usage:** After practice sessions, search CoffeeCornerMotorsport.com for "{race name} 2026 Tyre Strategy" to find best times per compound and which tire each driver used for their fastest lap.

## Output

Update existing practice and qualifying files in `data/r{XX}-{race-name}/`:

1. **Add `**Tire allocation:**` header** to each practice/qualifying file — e.g. "Hard: C1, Medium: C2, Soft: C3"

2. **Add `Tire` column** to practice result tables — Soft/Medium/Hard for each driver's fastest lap. If per-driver data is unavailable, note "Soft" for fastest-lap times (standard practice behavior).

3. **Add "Best Times per Compound" table** at the bottom of practice files:
   ```
   ### Best Times per Compound
   | Compound | Best Time | Driver |
   |----------|-----------|--------|
   | Soft     | 1:xx.xxx  | ...    |
   | Medium   | 1:xx.xxx  | ...    |
   | Hard     | 1:xx.xxx  | ...    |
   ```

## Pace Analysis Notes

When comparing practice times, always account for tire compound:
- A driver P5 on mediums may have better true pace than P1 on softs
- The "Best Times per Compound" table enables compound-normalized comparisons
- Typical soft-to-medium delta: 0.5-0.8s; medium-to-hard delta: 0.5-0.8s (varies by circuit)

## Notes

- Only update files that already exist — don't create session files (that's `fetch-session-results`'s job)
- If Pirelli data isn't available yet (pre-weekend), note this and skip
- If CoffeeCorner data isn't available, default to marking fastest laps as "Soft" and add a note
