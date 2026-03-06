# F1 Fantasy Team Picker

Pick an optimal F1 Fantasy team for an upcoming race weekend.

## Input

The user may provide:
- **Race name** (e.g. "Australian GP", "Monaco") — if not provided, ask
- **Budget remaining** — default $100M if first race or not specified
- **Specific constraints** (e.g. "must include Verstappen", "no Aston Martin drivers")
- **Chip to use** (e.g. "2x Boost on Leclerc") — default: save all chips

## Steps

### 1. Load existing data

Read all files in `data/` to understand:
- Current driver lineups and prices (`data/2026-driver-lineups.md`)
- Fantasy rules and scoring (`data/2026-fantasy-rules.md`)
- Previous team picks (any `data/2026-r*-team-pick.md` files)
- Any practice/qualifying results for the upcoming race

### 2. Research current form

Use web search to find:
- Latest practice session results (FP1, FP2, FP3) for the upcoming race
- Qualifying results if available
- Recent race results (last 2-3 races) for form assessment
- Any driver injuries, grid penalties, or reliability concerns
- Updated fantasy prices if they've changed since last saved
- **Weather forecast** for qualifying AND race day at the circuit location. Search for "{city} weather {qualifying date}" and "{city} weather {race date}". Note temperature, rain probability, and wind.

### 2b. Weather impact assessment

**Race day weather carries MORE weight than qualifying weather** — the race is where most points are scored.

- **Rain on race day:** High variance. Favors skilled wet-weather drivers (Verstappen, Hamilton, Russell). Increases DNF risk. Midfield drivers can score big from chaos. Consider No Negative chip if rain is likely.
- **Rain in qualifying only:** Can scramble the grid, creating overtaking opportunities on a dry race day. Benefits drivers who are good overtakers (Bearman, Ocon).
- **Extreme heat:** Increases tire degradation. Favors teams with good tire management (Mercedes in testing). Hurts teams with degradation issues (Red Bull).
- **Wind:** Can affect car balance differently. Less predictable — note but don't overweight.
- **Dry and mild:** Default conditions. Rely on practice/testing pace data as normal.

Adjust driver and constructor confidence ratings based on weather. Flag any weather-sensitive picks in the team presentation.

### 3. Analyze value

For each potential pick, calculate estimated Points Per Million (PPM):
- **PPM = Expected Points / Price**
- Consider: recent finishing positions, car pace, overtaking potential, qualifying form
- Flag drivers likely to gain price value (underperforming their car's pace)
- Flag drivers at risk of price drops

### 4. Build the team

Constraints:
- 5 drivers + 2 constructors
- Total must be within budget ($100M default)
- Max 2 drivers from the same constructor (verify this rule)
- Optimize for total expected points, weighted by PPM

Selection approach:
1. Pick 1-2 premium drivers ($20M+) from the fastest teams
2. Pick constructor(s) that pair with premium driver picks for synergy
3. Fill remaining slots with highest-PPM value picks
4. Ensure at least one budget pick ($5-7M) to enable premium selections
5. Leave $1-3M buffer for future transfers

### 5. Present the team

Output a table with:

| # | Role | Pick | Team | Price | Expected Points | PPM | Confidence |
|---|------|------|------|-------|----------------|-----|------------|

Then provide:
- **Total cost** and remaining budget
- **Key reasoning** for each pick (2-3 sentences)
- **Top 3 alternative swaps** with pros/cons
- **Chip recommendation** for this race weekend
- **Differentiation notes** (what makes this team unique vs high-ownership picks)

### 6. Save the pick

Write the team pick to `data/2026-r{XX}-{race-name}-team-pick.md` where:
- `{XX}` is the round number (01, 02, etc.)
- `{race-name}` is lowercase hyphenated (e.g. `australia`, `monaco`)

Update `data/2026-driver-lineups.md` with any new price information discovered.

## Important Notes

- Constructors score from BOTH drivers — a constructor with two top-5 drivers beats one with a P1 and a P15
- Overtaking points matter — drivers who qualify low but race high (like Bearman) have hidden value
- Price changes weigh last 3 races equally — factor in trajectory, not just this week
- In a friends league, differentiation wins — don't just copy the consensus team
- When uncertain between two picks at similar price, prefer the one with higher ceiling
