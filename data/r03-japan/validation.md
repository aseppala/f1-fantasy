# R03 Japan — Post-Race Validation

**Race:** Aramco Japanese Grand Prix | Suzuka International Racing Course | March 29, 2026
**Format:** Standard weekend (FP1/FP2/FP3/Quali/Race)
**Validated:** 2026-03-29

---

## 1. Predicted vs Actual — Drivers

Predicted = simulator median estimate from `sim-config.json` profiles (qualifying + race only).
Actual = R03 GamedayPoints from fantasy API.

| Driver | Sim Predicted | Actual R03 | Delta | Error Type |
|--------|--------------|------------|-------|------------|
| **Antonelli** | ~22 | **45** | **+23** | Pace miss — sim had race_mean=2.0 (P2), actual pole + win + FL + DOTD. Underestimated ceiling. |
| **Gasly** | ~3 | **10** | **+7** | Pace miss — profiled at race_mean=14 (P14), actual P7 quali AND race. 7-position surprise. |
| **Leclerc** | ~16 | **23** | **+7** | Pace miss — race_mean=5 (P5), actual P3. Ferrari 2 positions better than profiled. |
| **Russell** | ~32 | **19** | **−13** | Race pace miss — sim had Russell as likely winner (race_mean=1.5), actual lost positions in race (P2 grid → P4/5 finish). Possible on-track incident or pace drop. |
| **Bearman** | ~6 | **−4** | **−10** | Quali miss + race miss — profiled Q10, actual Q18 (Q1 out). Race also below profile. Variance underestimated. |
| **Lindblad** | ~4 | **−3** | **−7** | DNF or penalty miss — made Q3 (P10) but scored negative in race. dnf_chance=0.18 flagged this risk. |
| Hamilton | ~13 | 13 | 0 | Accurate |
| Norris | ~18 | 16 | −2 | Accurate |
| Piastri | ~20 | 27 | +7 | Slight underestimate — P2 race vs P3 predicted |
| Lawson | ~8 | 7 | −1 | Accurate |
| Hulkenberg | ~3 | 2 | −1 | Accurate |
| Verstappen | ~10 | 7 | −3 | Slight over — Q11 (Q2 out) worse than profiled, race recovery partially compensated |

---

## 2. Constructor Predicted vs Actual

| Constructor | Sim Predicted | Actual R03 | Delta | Notes |
|-------------|--------------|------------|-------|-------|
| **Mercedes** | ~58 | **79** | **+21** | Dominant — Antonelli win + FL contributes big race pts. Pit bonus sub-2.2s likely. |
| **Ferrari** | ~33 | **61** | **+28** | Massive underestimate — both drivers P3+P6 vs predicted P5+P6. Ferrari significantly faster than profiled. |
| **McLaren** | ~38 | **58** | **+20** | Both drivers P2+P4/5, consistent Q3 bonus. McLaren reliability restored. |
| **Haas** | ~18 | **0** | **−18** | Bearman Q1 out + poor race = zero. Profiled Bearman P9-10, actual P18+. Constructor collapsed. |
| Racing Bulls | ~8 | 9 | +1 | Accurate |
| Alpine | ~5 | 16 | +11 | Gasly pace surprise — constructor benefited from his P7 result |

---

## 3. Team Score Summary

| Team | Predicted | Actual | Delta |
|------|-----------|--------|-------|
| **T1 Safe** (Leclerc 2x / Mercedes C + Haas C) | ~125 | **130** | +5 |
| **T2 Constructor Kings** (Bearman 2x / Mercedes C + McLaren C) | ~129 | **143** | +14 |
| **T3 Ferrari Nuclear** (Leclerc 2x / Ferrari C + Racing Bulls C) | ~102 | **134** | +32 |

### T1 Deep-Dive
| Component | Expected | Actual | Impact |
|-----------|----------|--------|--------|
| Leclerc 2x | ~32 | 46 | +14 (P3 not P5) |
| Gasly | ~3 | 10 | +7 (P7 both sessions) |
| Mercedes C | ~60 | 79 | +19 |
| Bearman | ~6 | −4 | −10 |
| Lindblad | ~4 | −3 | −7 |
| Hulkenberg | ~3 | 2 | −1 |
| Haas C | ~18 | 0 | −18 |

T1 beat prediction largely because Mercedes C and Leclerc 2x overdelivered. Haas C (0 pts) and Bearman/Lindblad negatives nearly cancelled that out. **The decision to take Mercedes C over Ferrari C gained ~18 pts vs what Ferrari C would have scored.**

### T2 Deep-Dive
Constructors (Mercedes 79 + McLaren 58 = 137 pts) carried the entire team. Budget drivers were collectively -1 pts (Bearman −8 2x, Lawson +7, Ocon +3, Perez +2, Hulk +2 = +6 net). **T2's philosophy validated — constructors provide the floor AND the ceiling when drivers underperform.**

### T3 Deep-Dive
Best actual result of the three teams despite lowest sim prediction. Ferrari C delivering 61 pts (vs predicted 33) is the key story — both Ferrari drivers P3+P6, consistent constructor bonus. Leclerc 2x at P3 = 46 pts. Racing Bulls C bonus (Lindblad Q3 = +3 for constructor despite driver scoring negative).

---

## 4. DOTD Analysis

**DOTD winner: Oscar Piastri**

> ⚠️ Data note: The fantasy API `AdditionalStats` fields (including `DriverOfTheDay`) are **cumulative season totals**, not round-specific. Antonelli showed DOTD:10 in his season stats from a prior round — this was initially misread as a R03 win. Piastri's R03 GamedayPoints of 27 also do not yet include DOTD (+10 likely pending API update), making his final R03 total ~37.

Sim dotd_weight for Piastri = 1.4. Result: P2 finish at Suzuka, strong fan favourite, Australian racing story at a Japanese crowd circuit — fans rewarded the attacking drive from P3 to P2. Piastri overtaking narrative (5 overtakes, +1 position gained) combined with his global popularity gave him the edge over Antonelli (race winner).

**Calibration:** Piastri DOTD here is reasonable but not the default Suzuka pattern. Historical Suzuka DOTD went to Leclerc (2024, non-winner) and Tsunoda (2025, home hero, not in 2026). Piastri winning it as a non-winner in 2026 confirms the circuit doesn't auto-vote for the race winner — popular drivers with good race narratives can take it. dotd_weight=1.4 for Piastri feels correct. Antonelli dotd_weight=1.2 may be slightly low for future races — revise to 1.3 (popular, young, winning — but not a fan-favourite DOTD candidate yet like Hamilton or Leclerc).

---

## 5. Calibration Notes for R04 Bahrain

```
## Calibration Notes from R03 Japan

### Pace Adjustments — High Priority

- Antonelli: PROMOTE to race_mean=1.5, quali_mean=1.5. He is now effectively co-#1 with
  Russell. Took pole + won in all three rounds. dnf_chance can drop to 0.04 (no incidents).
  dotd_weight → 1.5 (race winner + youngest driver narrative confirmed).

- Russell: race_mean should remain 1.5 but note Japan race underperformance (started P2,
  finished P4/5). One-round anomaly — don't overadjust. Watch R04.

- Gasly: MAJOR correction. race_mean → 7.0, quali_mean → 7.0 (was 14!). P7 in quali AND
  race in both China and Japan. Alpine is systematically faster than modeled. This is now
  a two-round pattern — treat as real pace.

- Leclerc: race_mean → 3.5 (was 5.0). P3 Japan, P4 China, P3 Australia. Consistently
  outperforming P5 profile. Correct upward.

- Hamilton: race_mean stays 6.0. Two rounds of P3 and P6 — average is P4-5, profile at
  6.0 is slightly pessimistic but close. Minor tweak to 5.5 acceptable.

- Bearman: quali_mean → 12.0 (was 10.0). Q1 out at Suzuka (P18) shows his qualifying
  is more variable than profiled. Increase variance to 4.0. race_mean → 10.0 (was 9.0,
  but two rounds below profile now).

- Lindblad: dnf_chance=0.18 validated — scored negative in race despite Q3. Keep at 0.18
  until reliability improves. race_mean stays 13.0.

### Ferrari Calibration — HIGH PRIORITY

- Ferrari C was 61 pts actual vs ~33 predicted — SYSTEMATIC underestimate two rounds running.
  Ferrari team pace is closer to P3+P5 consistently, not P5+P6.
  - Leclerc: race_mean → 3.5
  - Hamilton: race_mean → 5.5
  - Ferrari C: expect 45-55 pts at power circuits, not 30-35.

### McLaren Calibration

- McLaren reliability restored. Both drivers scored R03 (Piastri P2, Norris P4/5).
  Reduce dnf_chance back toward 0.07 for Bahrain — the China double DNS looks like
  a one-off compliance issue now resolved.
  - Norris: dnf_chance → 0.07
  - Piastri: dnf_chance → 0.07

### Haas Calibration

- Bearman had worst qualifying result of season at Suzuka (Q1). Do not treat as reliable
  top-10 qualifier at every circuit — Suzuka's technical nature exposed a weakness.
  Haas C scored 0 pts. Bahrain is a more conventional circuit so some recovery expected,
  but lower confidence.

### DOTD Notes

- Piastri won DOTD despite Antonelli winning the race — confirms Suzuka does not auto-vote
  for race winner. Popular driver with strong race narrative (P3→P2, overtaking) can take it.
- Piastri dotd_weight=1.4 validated.
- Antonelli dotd_weight → 1.3 (slightly raised; popular but not yet a fan-vote magnet).
- Leclerc dotd_weight=1.8 remains correct for non-winner scenarios at technical circuits.
- ⚠️ Lesson: API AdditionalStats (DOTD, FastestLap, Overtakes) are cumulative season
  totals — never read these as round-specific. Only GamedayPoints is round-specific.

### Overtake Factor Notes

- Suzuka overtaking_index=4 felt right — very limited passing observed. Keep at 4.
- Bahrain overtaking_index should be 6 (open layout, DRS long straights, high overtaking).
  Backmarker position gains amplified at Bahrain vs Suzuka.
- Gasly overtake_factor should rise to 1.1 — consistently picks up positions in race.
- Bearman overtake_factor: no evidence of overtaking at Suzuka (started P18, finished
  poorly). Keep at 1.3 but note it requires good qualifying to be relevant.

### Overall Calibration — R03

- Simulation was broadly accurate for the top-6 drivers individually (Hamilton on target,
  Norris close, Piastri slight underestimate). Main misses: Antonelli ceiling too low
  (didn't model his win upside fully), Gasly pace completely wrong (still using stale
  profile), and Bearman qualifying variance too tight.
- Constructors: Ferrari C and Mercedes C both underestimated by ~20-28 pts each.
  The sim consistently underestimates constructor returns when both drivers finish top 6.
  Consider adding a "both-drivers-top-5 bonus" scenario in the constructor scoring model.
- Confidence in R04 Bahrain profiles: MEDIUM — 3 rounds of data, clear Mercedes/Ferrari
  hierarchy emerging. McLaren pace real but reliability history warrants caution.
  Bahrain is a new circuit type (high deg, power circuit) — opening round of tire
  calibration for this surface.
```

---

## 6. Pre-R04 Action Items

| Priority | Item |
|----------|------|
| 🔴 HIGH | Update sim profiles for Bahrain: Antonelli race_mean→1.5, Gasly race_mean+quali_mean→7.0, Leclerc race_mean→3.5 |
| 🔴 HIGH | McLaren dnf_chance → 0.07 for both drivers (reliability restored) |
| 🔴 HIGH | Fetch R04 Bahrain prices after R03 price update (Gasly, Leclerc likely rise; Bearman/Lindblad likely drop) |
| 🟡 MED | Bearman: decide whether to hold or sell — Q1 at Suzuka + bad race is a warning sign for T2/T3 |
| 🟡 MED | T1: 0 transfers carry into R04. T2: 0 carry. T3: 1 carry. |
| 🟡 MED | Assess chip usage — next sprint weekend is R06 Miami. Consider saving Limitless-class chips for R06/R07. |
| 🟢 LOW | Confirm Verstappen R04 profile — dnf_chance=0.12 still warranted (P11 quali + recovered to P8 race but low pace overall) |
