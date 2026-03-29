---
name: f1-fantasy
description: End-to-end F1 Fantasy race weekend workflow — fetches data, analyzes form and value, optimizes transfers, simulates, and builds teams.
---

# F1 Fantasy Race Weekend Agent

Orchestrate the full F1 Fantasy workflow for a race weekend. You are a **lightweight coordinator** — your job is to launch sub-agents for independent work and run analysis skills sequentially. Do not accumulate raw data in your own context; let sub-agents handle it.

## Input

The user may provide:
- **Race name or round number** — if not provided, determine the next upcoming race from `data/2026-calendar.md`
- **Specific constraints** (e.g. "focus on Team 2", "skip simulation")
- **Chip to use** (e.g. "Limitless on Team 1")

## Pipeline

### Phase 1: Fetch Data — PARALLEL AGENTS

Launch all 5 fetch skills as **parallel background agents** using the Agent tool with `run_in_background: true`. Do not wait for one to finish before starting the next — fire all 5 simultaneously.

```
Agent 1 (background): fetch-session-results — all sessions for target race + backfill
Agent 2 (background): fetch-fantasy-points — completed rounds, backfill missing files
Agent 3 (background): fetch-tyre-data — compound allocation + per-driver usage
Agent 4 (background): fetch-weather — qualifying + race day forecast + SC risk
Agent 5 (background): fetch-standings — latest championship standings
```

Each agent's prompt should include:
- The target race name and round number (from `data/2026-calendar.md`)
- The full content of the relevant SKILL.md (read it before launching the agent)
- Instruction to save output to `data/r{XX}-{race-name}/` and report what was saved

Wait for all 5 to complete, then confirm to the user what was collected and flag any gaps.

### Phase 2: Analyze — SEQUENTIAL (dependency chain)

Run analysis skills sequentially — each step reads the previous step's output files.

6. Read `data/r{XX}-{race-name}/` to check what data is now available, then run `/analyze-form`
7. Run `/analyze-value` (reads form-analysis.md produced in step 6)

**Decision point:** Present the form and value analysis summary to the user. Ask if they want to adjust any assumptions before proceeding.

8. Run `/optimize-transfers` — per-team transfer recommendations

**Decision point:** Present transfer recommendations. Allow the user to override before building teams.

### Phase 3: Simulate

9. Run `/simulate` — Monte Carlo simulation. Read the sim-config.json (or generate one from analysis), run the Python simulator, present results.

### Phase 4: Build Teams — PARALLEL AGENTS

After simulation output is available, launch **3 parallel agents** (one per team) using the Agent tool. Each agent receives only what it needs:

```
Agent A: build team-1 ({slug}) — reads: team-strategy.md (T1 section), prices, sim results, previous T1 file
Agent B: build team-2 ({slug}) — reads: team-strategy.md (T2 section), prices, sim results, previous T2 file
Agent C: build team-3 ({slug}) — reads: team-strategy.md (T3 section), prices, sim results, previous T3 file
```

Each agent's prompt should include:
- The full content of `pick-team` SKILL.md
- Only the relevant team's section from `data/team-strategy.md`
- Current prices from `data/r{XX}-{race-name}/fantasy-points.md`
- Simulation results from sim output
- The previous round's team file for that team (budget, transfers, chips)
- Instruction to save to `data/r{XX}-{race-name}/team-{N}-{slug}.md`

Wait for all 3 to complete, then present a summary comparison table across all teams.

### Phase 5: Save

Confirm all outputs are saved to `data/r{XX}-{race-name}/`. List the files created.

### Phase 6: Post-Race (after results are available)

10. Run `/validate` — compare simulation predictions to actual results, generate calibration notes for next round's driver profiles.

## Guidelines

- **You are a coordinator, not an accumulator.** Read only what you need to coordinate (calendar, team count, race name). Let sub-agents read the heavy data files.
- Always check what data already exists before fetching — pass this check to the fetch agents so they skip already-present files.
- Present analysis results at decision points and wait for user input before proceeding.
- If a fetch agent fails (data source unavailable), note the gap and continue with available data.
- The user can run any individual skill independently — this agent just orchestrates the full pipeline.
- Respect the team strategies defined in `data/team-strategy.md`.
- When building agent prompts, include the full SKILL.md content inline — sub-agents do not have access to skill files automatically.
