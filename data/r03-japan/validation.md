# R03 Japan GP — Post-Race Validation

**Date:** 2026-03-29
**Simulator config:** `data/r03-japan/sim-config.json`
**Sims run:** 50,000 (seed 42)

---

## 1. Driver Predictions vs Actuals

| Driver | Predicted (avg) | Actual Pts | Delta | Notes |
|--------|----------------|------------|-------|-------|
| Antonelli | 27.4 | 50 | **+22.6** | P1 quali + P1 race + FL bonus — race_mean 2.0 too pessimistic |
| Piastri | 21.4 | 43 | **+21.6** | DOTD win (+10) dominated; finished P2 vs race_mean 3.0 |
| Leclerc | 18.3 | 31 | **+12.7** | Pace miss — finished P3 vs race_mean 5.0; +8 overtake pts |
| Gasly | 3.7 | 14 | **+10.3** | Massive pace miss — qualified P7 vs quali_mean 14.0 |
| Hulkenberg | 4.0 | 10 | **+6.0** | Strong Suzuka pace; +8 overtake pts with race_mean 11.0 |
| Norris | 19.7 | 24 | +4.3 | Within range |
| Hamilton | 15.6 | 19 | +3.4 | Accurate — P6 as predicted |
| Perez | 1.6 | 4 | +2.4 | Small gain |
| Ocon | 6.8 | 9 | +2.2 | Slight outperformance |
| Verstappen | 11.8 | 13 | +1.2 | Accurate |
| Bortoleto | 1.7 | 3 | +1.3 | Accurate |
| Colapinto | 2.8 | 4 | +1.2 | Accurate |
| Hadjar | 4.3 | 5 | +0.7 | Accurate |
| Bottas | 1.3 | 2 | +0.7 | Accurate |
| Alonso | 2.2 | 4 | +1.8 | Accurate |
| Lawson | 10.5 | 10 | −0.5 | Accurate |
| Lindblad | 2.0 | 1 | −1.0 | Accurate |
| Sainz | 4.2 | 4 | −0.2 | Accurate |
| Russell | 29.5 | 27 | −2.5 | Finished P4 despite P2 quali; within range |
| Albon | 3.7 | −1 | −4.7 | P20 finish; within variance |
| **Stroll** | 0.7 | **−17** | **−17.7** | DNF miss — −20 race pts |
| **Bearman** | 10.2 | **−14** | **−24.2** | DNF miss — dnf_chance 0.07 was too low for Haas reliability |

---

## 2. Error Classification

| Driver | Error Type | Detail |
|--------|-----------|--------|
| Antonelli | **Pace miss + FL** | race_mean 2.0 too high; he's consistently P1. FL bonus (+10) is a large unmodeled swing |
| Piastri | **DOTD miss** | Won DOTD at dotd_weight 1.4 — right range but Suzuka fan vote favored aggressive P2 drive |
| Leclerc | **Pace miss** | Ferrari race pace understated; race_mean 5.0 → actual P3 |
| Gasly | **Pace miss** | Alpine dramatically faster than modeled; quali_mean 14.0 was 7 positions too pessimistic |
| Hulkenberg | **Overtake miss** | overtake_factor 0.9 underestimated; scored +8 overtake pts at Suzuka |
| Bearman | **DNF miss** | dnf_chance 0.07 too low — 1 DNF from 3 races (33% empirical rate so far) |
| Stroll | **DNF miss** | dnf_chance 0.12 fired; Aston Martin reliability and pace remain poor |

---

## 3. Constructor Calibration

| Constructor | Predicted (avg) | Actual | Delta | Key Drivers |
|-------------|----------------|--------|-------|-------------|
| Ferrari | 51.8 | **75** | **+23.2** | Double pit stop bonus (+15) — both 1st and 2nd fastest pit. Leclerc P3 |
| Mercedes | 75.0 | **92** | **+17.0** | FL bonus via Antonelli (+10) + fastest pit (+5); both drivers scored well |
| McLaren | 59.0 | **72** | **+13.0** | Piastri P2 + DOTD; slightly better than predicted |
| Alpine | 12.4 | **25** | **+12.6** | Gasly P7 — pace miss. Alpine much faster than modeled |
| Audi | 12.7 | **23** | **+10.3** | Hulkenberg +8 overtakes drove the gap vs prediction |
| Red Bull | 33.3 | 25 | −8.3 | Hadjar lost 4 positions; Verstappen recovered from P11 |
| Racing Bulls | 23.8 | 18 | −5.8 | Lindblad −4 positions; within variance |
| Williams | 14.1 | 9 | −5.1 | Both drivers scored poorly; Albon P20 |
| Cadillac | 3.9 | 5 | +1.1 | Accurate |
| Aston Martin | 5.1 | **−12** | **−17.1** | Stroll DNF dominant; both drivers underperformed |
| **Haas** | 26.6 | **−4** | **−30.6** | Bearman DNF (−20 race pts) wiped all projected value |

---

## 4. DOTD Analysis

**Winner: Oscar Piastri** (P2 from P3 grid, +1 position, +6 overtake pts, aggressive Suzuka drive)

- dotd_weight was 1.4 — third highest in the profile, behind Leclerc (1.8) and Norris (1.5)
- Narrative: Piastri pressured Russell throughout and made clean passes; Suzuka fan votes reward overtaking
- Leclerc (dotd_weight 1.8) did NOT win despite P3 — clean race with no dramatic story
- Norris (1.5) finished P5 cleanly — no memorable overtake narrative

Piastri has now shown a pattern of performing when it matters. dotd_weight 1.4 is slightly low — bump to 1.6 for R04. Leclerc at 1.8 appears inflated given he's not converting on the fan vote in clean races; consider reducing to 1.5.

---

## 5. Team Score Validation

| Team | Predicted (avg) | Actual | Delta |
|------|----------------|--------|-------|
| T1 Safe (Antonelli 2x) | 176.2 | 167 | −9.2 |
| T2 Constructor Kings (Bearman 2x) | 170.2 | 169 | **−1.2** |
| T3 Ferrari Nuclear (Leclerc 2x) | 152.6 | 180 | **+27.4** |

- T2 prediction was nearly exact despite Bearman's catastrophic DNF — Mercedes + McLaren constructors absorbed the loss
- T3 significantly outperformed due to Ferrari pit bonuses and Leclerc's better race pace
- T1 slightly underperformed; Bearman DNF and Haas constructor −4 dragged the score

---

## 6. Calibration Notes for R04

```
## Calibration Notes from R03 Japan

### Pace Adjustments Suggested
- Antonelli: quali_mean → 1.5, race_mean → 1.5 (P1 in 2 of 3 races; genuinely dominant)
- Russell: quali_mean → 2.0, race_mean → 2.0 (swap roles with Antonelli in model)
- Leclerc: race_mean → 4.0 (consistently overdelivering vs 5.0 profile)
- Piastri: race_mean → 2.5 (outperforming 3.0 mean consistently)
- Gasly: quali_mean → 9.0, race_mean → 9.0 (Alpine pace 5+ positions faster than modeled)

### DNF Adjustments
- Bearman: dnf_chance → 0.13 (1 DNF from 3 races; Haas reliability questionable)
- Ocon: dnf_chance → 0.10 (Haas has shown reliability issues across both cars)
- Stroll: dnf_chance → 0.15 (consistent DNF and poor performance pattern)

### DOTD Notes
- Piastri won DOTD at dotd_weight 1.4 → bump to 1.6 (Suzuka-style tracks reward clean aggression)
- Leclerc at 1.8 inflated — not converting DOTD votes in clean races → reduce to 1.5
- Hamilton dotd_weight 1.3 appears correct

### Overtake Factor Notes
- Hulkenberg overtake_factor 0.9 underdelivered — bump to 1.1 (scored +8 overtake pts)
- Gasly overtake_factor 1.0 appears right; points came from qualifying and race position
- Suzuka overtaking_index 4 seems correct — meaningful but not extreme overtake scoring

### Constructor Notes
- Ferrari pit_mean → 2.1 (won both fastest pit bonuses; sub-2.2s consistently)
- Mercedes pit_mean → 2.2 (won fastest pit; consistent performance)
- Haas reliability risk overwhelms pit bonus modeling — elevate dnf_chance for both drivers
- Alpine: pace model stale — revisit before R04 qualifying predictions

### Overall Calibration
- Simulation was slightly conservative overall (avg team prediction error: ~+6 pts)
- Biggest systematic miss: Haas constructor (−30.6 delta) — DNF risk heavily underweighted
- Second biggest: Ferrari constructor (+23.2) — pit stop dominance undermodeled
- Third: Alpine constructor (+12.6) — pace model needs full revision
- Driver midfield predictions were accurate (Lawson, Hamilton, Verstappen, Norris all within ±5 pts)
- Three rounds of data now available — patterns becoming more reliable
- Confidence in R04 profiles: medium — Alpine revision and Haas reliability concern remain open
```

---

## 7. Key Takeaways

1. **Haas is a liability** — Bearman's DNF pushed T1 and T3 down significantly; T2's double-Bearman captain choice was a disaster (−28 from captain alone). Haas reliability risk must be elevated in all future profiles.

2. **Ferrari pit stops are a structural advantage** — winning both fastest pit bonuses (+15 constructor pts) was a material edge not fully modeled. Lowering pit_mean to 2.1 better captures this probability.

3. **Antonelli is the dominant driver** — three rounds in, he's P1 or P2 in every race and took FL in Japan. race_mean should move to 1.5 and Russell's to 2.0.

4. **Alpine pace severely underestimated** — Gasly qualifying P7 was 7 spots better than modeled. Revisit Alpine's pace model before R04; Suzuka may specifically suit their car, or the base model is just stale.

5. **T3 Ferrari Nuclear is the highest-upside team** — it underperformed prediction in R01/R02 but exceeded by +27 here. The variance (±48.8) is real — this team swings hardest in both directions.
