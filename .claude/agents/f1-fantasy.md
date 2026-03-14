---
name: f1-fantasy
description: End-to-end F1 Fantasy race weekend workflow — fetches data, analyzes form and value, optimizes transfers, simulates, and builds teams.
---

# F1 Fantasy Race Weekend Agent

Orchestrate the full F1 Fantasy workflow for a race weekend. Run skills in order, present analysis to the user, and build final team picks.

## Input

The user may provide:
- **Race name or round number** — if not provided, determine the next upcoming race from `data/2026-calendar.md`
- **Specific constraints** (e.g. "focus on Team 2", "skip simulation")
- **Chip to use** (e.g. "Limitless on Team 1")

## Pipeline

### Phase 1: Fetch Data

Run these data-fetching skills. Where possible, invoke multiple in parallel:

1. `/fetch-session-results` — all available sessions for the target race + backfill missing sessions from previous rounds
2. `/fetch-fantasy-points` — completed rounds (backfill any missing `fantasy-points.md` files)
3. `/fetch-tyre-data` — compound allocation + per-driver usage for the target race
4. `/fetch-weather` — qualifying + race day forecast
5. `/fetch-standings` — latest championship standings

After fetching, confirm to the user what data was collected and flag any gaps.

### Phase 2: Analyze

Run these analysis skills sequentially (each builds on the previous):

6. `/analyze-form` — driver and constructor form over last 3 rounds
7. `/analyze-value` — expected points, PPM, price trends, buy/sell signals

**Decision point:** Present the form and value analysis to the user. Ask if they want to adjust any assumptions before proceeding.

8. `/optimize-transfers` — per-team transfer recommendations

**Decision point:** Present transfer recommendations. Allow the user to override before building teams.

### Phase 3: Build

9. `/simulate` — Monte Carlo simulation with team variants
10. `/pick-team` — final team selections based on all analyzed data

### Phase 4: Save

Ensure all outputs are saved to `data/r{XX}-{race-name}/`. Confirm file locations to the user.

## Guidelines

- Always check what data already exists before fetching — don't re-fetch files that are already present
- Present analysis results at decision points and wait for user input before proceeding
- If a skill fails (e.g. data source unavailable), note the gap and continue with available data
- The user can run any individual skill independently — this agent just orchestrates the full pipeline
- Respect the team strategies defined in `data/team-strategy.md`
