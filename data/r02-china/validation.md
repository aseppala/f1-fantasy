# R02 China — Post-Race Validation

**Race:** Chinese Grand Prix | Shanghai International Circuit | March 15, 2026
**Format:** Sprint weekend (SQ + Sprint + Qualifying + Race)
**Validated:** 2026-03-15 (race day — full fantasy API update pending)

> ⚠️ **Data status:** `fantasy-points.md` was fetched 2026-03-14 (pre-race). R02 Total in that file covers SQ + Sprint + Qualifying only. Race session points are estimated from session results + scoring rules. Final verified totals will differ slightly (overtake counts, pit stop tiers, DOTD).

---

## 1. Predicted vs Actual — Driver Race Session

Simulator profiles from `simulator.py` `get_china_profiles()`. Predicted = simulator median for qualifying + race. Actual = qualifying + race only (sprint excluded to match sim scope).

| Driver | Sim Predicted (med Q+Race) | Actual Q+Race (est) | Delta | Error Type |
|--------|--------------------------|---------------------|-------|------------|
| **Antonelli** | ~26 | ~47 (+10 FL, P1 Q, P1 Race) | **+21** | Pace beat — won race outright, fastest lap; sim favored Russell by 1 quali mean position |
| **Russell** | ~30 (2x=60) | ~29 (2x=58) | −2 | On target — P2 Q, P2 Race as expected; just lost the head-to-head with Antonelli |
| **Norris** | ~22 | −15 (DNS) | **−37** | **DNF miss — catastrophic.** DNS on race day not modeled. dnf_chance 0.05 per race severely underestimated fleet-wide mechanical failure risk |
| **Piastri** | ~22 | −14 (DNS) | **−36** | **DNF miss — catastrophic.** Same issue. Double McLaren DNS on same day is a ~0.25% event; dnf_chance needs raising |
| **Hamilton** | ~20 | ~25–35 (+DOTD?) | +5 to +15 | Pace on target (P3 Q, P3 Race). Sim had race_mean 4.5, actual P3. Possible DOTD adds +10 |
| **Leclerc** | ~19 | ~20 (P4 Q, P4 Race) | +1 | Accurate — simulation well calibrated for Leclerc |
| **Bearman** | ~15 | ~22 (P10 Q, P5 Race) | **+7** | **Pace miss — overperforming again.** race_mean=9 but actual P5. Two rounds running he's finishing 4-5 positions ahead of qualifying. Overtake factor correct but race pace underestimated |
| **Gasly** | ~10 | ~17 (P7 Q, P6 Race) | **+7** | **Pace miss.** race_mean=9, actual P6. Alpine significantly faster than profiled. Consistent with SQ P7 surprise |
| **Verstappen** | ~18 | −17 (P8 Q, DNF) | **−35** | DNF miss. dnf_chance=0.05; has now retired in both R01 and R02. Suggest raising to 0.12 |
| **Hadjar** | ~8 | ~9 (P9 Q, P8 Race) | +1 | Accurate |
| **Lindblad** | ~3 | ~6 (P15 Q, P12 Race + sprint DNF already captured) | +3 | Slightly above profile |
| **Hulkenberg** | ~2 | ~1 (P11 Q, P11 Race + sprint DNF captured) | −1 | Accurate |
| **Bottas** | ~1 | ~12 (P20 Q, P13 Race) | **+11** | Big position gain from back; sim underestimates backmarker pos-gained potential at Shanghai |

---

## 2. Constructor Predicted vs Actual (Q+Race)

| Constructor | Sim Predicted | Actual Q+Race (est) | Delta | Notes |
|-------------|--------------|---------------------|-------|-------|
| **Mercedes** | ~48 | ~63 (Q3+10, P1+P2=43, pit~10) | **+15** | Dominated — both drivers on podium, pit stops likely sub-2.2s |
| **McLaren** | ~38 | −30 (Q3+10, 2×DNS=−40) | **−68** | **Catastrophic miss.** Both cars failed to start. McLaren sim DNF risk (0.05 per driver) was 10× too low |
| **Ferrari** | ~35 | ~44 (Q3+10, P3+P4=27, pit~7) | **+9** | Solid — both drivers consistent P3/P4, constructors bonus added up |
| **Racing Bulls** | ~8 | ~15 (Q2+5, Lawson P7=6, pit~4) | +7 | Lawson P7 a positive surprise |
| **Haas** | ~12 | ~17 (one Q3+3, Bearman P5=10, pit~4) | +5 | Bearman P5 boosted constructor |

---

## 3. DOTD Analysis

**DOTD winner: Unknown** (fantasy API update pending)

**Top candidates based on race narrative:**
1. **Hamilton** — P3, Ferrari comeback story, fan favorite (dotd_weight=1.5). Most likely winner.
2. **Bearman** — P5 from P10 (+5 positions), underdog narrative. Strong DOTD contender.
3. **Antonelli** — Race winner, youngest at Shanghai. Narrative is there but he's less of a fan "hero" story.

**Calibration note:** Hamilton is consistently the strongest DOTD candidate when Ferrari scores well. In R01, Leclerc won DOTD. This race favors Hamilton given he's now clearly the faster Ferrari. dotd_weight=1.5 appears correct — no adjustment needed pending confirmation.

---

## 4. Team Scores vs Simulation

### Sprint Weekend Caveat
The simulator models **qualifying + race only**. Sprint weekends add ~60–90 pts per team from SQ + Sprint sessions (not captured in sim averages). All teams will substantially exceed sim averages on sprint weekends.

| Team | Sim Avg (Q+Race only) | Actual Q+Race (est) | Full R02 (est, incl. sprint) |
|------|-----------------------|---------------------|-----------------------------|
| **T1 Safe (Limitless, Russell 2x)** | 239.1 | ~136 | ~263 |
| **T2 Constructor Kings (Bearman 2x)** | ~130 | ~174 | ~279 |
| **T3 Ferrari Nuclear (Hamilton 2x)** | 115.7 | ~179–189 | ~290–300 |

### T1 Deep-Dive: The McLaren Disaster
| Component | Expected | Actual | Impact |
|-----------|----------|--------|--------|
| Norris (in T1 via Limitless) | +22 | −15 | −37 |
| Piastri (in T1 via Limitless) | +22 | −14 | −36 |
| McLaren (C) (in T1 via Limitless) | +38 | −30 | −68 |
| **Total McLaren damage** | **+82** | **−59** | **−141 pts** |

Without the McLaren failure, T1 would have scored ~277 Q+Race pts (vs sim avg 239). The Mercedes + Ferrari + Hamilton selections all outperformed. The Limitless strategy was sound — the result was the right call, just unlucky.

### T2 Summary
Constructor Kings (Mercedes + Ferrari constructors) was the winning formula. Both constructors delivered. Gasly transfer (replacing Hadjar) paid off: Gasly +17 actual vs Hadjar ~+9 expected. Saving 1 transfer for R03 carry-over was correct.

### T3 Summary
Ferrari Nuclear: Both drivers P3/P4, constructor scoring strongly. Hamilton 2x (switched from Leclerc after SQ) appears to have been the right call — Hamilton P3 with possible DOTD makes him higher-scoring than Leclerc P4.

---

## 5. Calibration Notes for R03 Japan

```
## Calibration Notes from R02 China

### Pace Adjustments Suggested

- Bearman: race_mean too pessimistic — profiled at 9, actual P5 (2nd round running he's finished ~5 pos ahead of profile). Suggest race_mean=6.5 for Suzuka
- Gasly: race_mean too pessimistic — profiled at 9, actual P6 (SQ P7 → Race P6). Suggest race_mean=7 for Suzuka
- Antonelli: quali_mean slightly pessimistic — profiled at 2.5, took pole both sessions. Suggest quali_mean=1.8; the Russell/Antonelli gap is narrowing

### DNF/Reliability Notes

- McLaren: CRITICAL — double DNS on race day. This was a team-wide failure (likely aerodynamic regs compliance issue). dnf_chance should be raised to 0.12–0.15 until cause is confirmed and resolved. Do NOT load up on McLaren at Suzuka until reliability is confirmed.
- Verstappen: DNF in both R01 and R02. dnf_chance=0.05 too low. Raise to 0.12 for R03. Red Bull reliability is a systemic concern in 2026.
- Budget drivers (Hulkenberg, Bottas, Lindblad): all DNF'd in sprint (different causes). Sprint DNF rate for midfield/backmarkers higher than modeled. Consider sprint_dnf_chance = 0.12 for B/C/D-tier drivers.
- Albon, Bortoleto: Both DNSd from race grid alongside McLarens. May indicate a wider compliance or technical directive change — worth monitoring.

### DOTD Notes

- Hamilton won DOTD (if confirmed): dotd_weight=1.5 validated. Ferrari P3 finish is enough when the narrative is there.
- Bearman consistently challenges for DOTD (P5 from P10, +5 positions): dotd_weight could rise from 1.2 to 1.4 — underdog + overtaking narrative is strong with fans.

### Constructor Notes

- Mercedes pit_mean=2.3s appears correct (likely sub-2.2 on some stops, scoring well)
- McLaren: do not assume pit_mean matters — focus on DNF risk for R03
- Ferrari showing race_mean closer to 3.5–4 (not 5) — pit execution reliable

### Overtake Factor Notes

- Shanghai overtaking_index=6 felt right overall
- Bottas/Sainz gained 7–8 positions from deep in the grid — backmarker pos_gained underestimated from lowest grid slots (P17–P22 have high floor when grid is compressed)
- Bearman overtake_factor=1.3 validated — gained 5 positions in race

### Overall Calibration — R02

- Simulator was OPTIMISTIC for T1 (McLaren failure), PESSIMISTIC for T2/T3 (Bearman/Gasly outperformed)
- Biggest systematic miss: McLaren reliability (catastrophic) and budget-driver race_mean (both Bearman and Gasly significantly overperformed profiles)
- Confidence in R03 Japan profiles: MEDIUM — 2 rounds of data, clear pecking order emerging (Mercedes > Ferrari > Alpine > Haas in race pace), but reliability picture is murky (McLaren, Verstappen, budget drivers)

### Suzuka-Specific Notes (R03, March 27–29)

- Suzuka overtaking_index: 3 (low — technical circuit, very limited passing opportunities)
- This suppresses overtake bonuses for all drivers; position-from-qualifying is more important
- Key question: Does McLaren fly or is their technical issue chronic?
- Mercedes have historically been strong at Suzuka; Ferrari was competitive here in 2025
```

---

## 6. Pre-R03 Action Items

| Priority | Item |
|----------|------|
| 🔴 HIGH | Monitor McLaren reliability news — was the DNS a one-off or systemic? |
| 🔴 HIGH | Update simulator with new race_mean for Bearman (→6.5) and Gasly (→7) |
| 🔴 HIGH | Raise Verstappen dnf_chance to 0.12 |
| 🟡 MED | Check R03 prices after R02 price updates (Bearman, Gasly likely rise; McLaren drivers may fall) |
| 🟡 MED | T1: Revert to pre-Limitless squad (Leclerc, Antonelli, Bearman, Lindblad, Bottas / Ferrari + Haas). Assess what transfers to make with 2 free (no carry-over from Limitless round) |
| 🟡 MED | T2: 3 free transfers available for R03 (1 carry-over + 2 standard) |
| 🟡 MED | T3: 3 free transfers available for R03 (1 carry-over + 2 standard) |
| 🟢 LOW | Fetch full R02 fantasy points once API updates (likely March 16-17) to verify score estimates |
