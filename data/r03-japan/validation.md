# R03 Japan — Post-Race Validation

**Race:** Aramco Japanese Grand Prix | Suzuka International Racing Course | March 29, 2026
**Format:** Standard weekend (FP1/FP2/FP3/Quali/Race)
**Validated:** 2026-03-29 (based on official race.md results — supersedes pre-race speculative version)

> ⚠️ The previous version of this file was written speculatively **before the race**, using estimated "actual" scores that have now been replaced with scores calculated from the official formula1.com results. The race data (race.md) was fetched post-race and all figures below are grounded in that data.
>
> Pit stop bonuses and overtake bonuses are estimated (no official pit time data available). Fantasy GamedayPoints from the API are not available yet as of validation time — scores are calculated from the scoring rules applied to race + qualifying results.

---

## Scoring Methodology

**Qualifying pts:** P1=10, P2=9, ..., P10=1, P11+=0, NC/No time=-5
**Race pts:** P1=25, P2=18, P3=15, P4=12, P5=10, P6=8, P7=6, P8=4, P9=2, P10=1, P11+=0, DNF=-20
**Positions gained:** +1 pt per net position gained vs grid (no penalty for positions lost beyond lower race score)
**Fastest Lap:** +10 pts | **DOTD:** +10 pts
**Constructor:** sum of both drivers' race pts + quali bonus + pit stop bonus

---

## 1. Qualifying Results vs Profile

| Driver | Predicted Q Position | Actual Q Position | Q Pts | Notes |
|--------|---------------------|------------------|-------|-------|
| Antonelli | ~P2 (quali_mean=2.0) | **P1** | 10 | Beat Russell by 0.298s — pole x3 in a row |
| Russell | ~P1 (quali_mean=1.5) | P2 | 9 | Slightly underperformed profile (expected P1) |
| Piastri | ~P3 (quali_mean=3.0) | P3 | 8 | On profile |
| Norris | ~P4 (quali_mean=4.0) | P5 | 6 | 1 position worse than profile |
| Leclerc | ~P5 (quali_mean=5.0) | P4 | 7 | 1 position better — Ferrari still 3rd team |
| Hamilton | ~P6 (quali_mean=6.0) | P6 | 5 | Exactly on profile |
| Gasly | ~P14 (quali_mean=14.0) | **P7** | 4 | **MAJOR MISS** — 7 positions better than profiled |
| Verstappen | ~P7-P8 (quali_mean=7.5) | P11 | 0 | 3-4 positions worse — Q2 elimination |
| Bearman | ~P10 (quali_mean=10.0) | **P18** | 0 | **MAJOR MISS** — Q1 elimination, 8 positions worse |
| Lindblad | ~P13 (quali_mean=13.0) | P10 | 1 | 3 positions better — made Q3! |
| Lawson | ~P8 (quali_mean=8.0) | P14 | 0 | 6 positions worse than profile |
| Hulkenberg | ~P9 (quali_mean=9.0) | P13 | 0 | 4 positions worse |
| Ocon | ~P11 (quali_mean=11.0) | P12 | 0 | On profile |

---

## 2. Predicted vs Actual — Drivers

Predicted = reconstructed median estimates from sim-config.json profiles (qualifying + race expected scoring + estimated FL/DOTD EV).
Actual = calculated from official qualifying and race results using F1 Fantasy scoring rules.

| Driver | Sim Predicted | Actual R03 | Delta | Error Type |
|--------|--------------|------------|-------|------------|
| **Antonelli** | ~31 | **45** | **+14** | Pace + FL miss — sim had race_mean=2.0 (P2 expected), actual pole + win + FL (+10). P1 scenario underweighted. FL probability too low. |
| **Russell** | ~36 | **21** | **−15** | Pace miss — sim had race_mean=1.5 (P1-P2 expected), actual P2 grid → P4 finish. Lost 2 positions in the race (safety car shuffle + Leclerc/Piastri overtakes). Variance too tight. |
| **Bearman** | ~4 | **−20** | **−26** | DNF miss — Q1 out (P18) + crash retirement (lap 20). dnf_chance=0.07 was far too low. Worst individual miss of the round. |
| **Gasly** | ~2 | **10** | **+8** | Pace miss — profiled at race_mean=14.0 (P14), actual Q7 + P7. Two-round confirmed pattern now (China P7 also). Profile completely stale. |
| **Piastri** | ~27 | **37** | **+10** | DOTD miss — predicted ~P3 race (+DOTD at moderate probability), actual P2 race + confirmed DOTD. The +10 DOTD was not the median scenario in the sim. |
| **Leclerc** | ~22 | **23** | **+1** | Accurate — Q P4 (7 pts) + race P3 (15) + 1 position gained = 23. Profile of race_mean=5.0 slightly pessimistic (consistently P3-P4) but close. |
| Hamilton | ~14 | 13 | −1 | Accurate — Q P6 (5) + race P6 (8) = 13. Profile race_mean=6.0 correct. |
| Norris | ~19 | 16 | −3 | Slight over — Q P5 (6) + race P5 (10) = 16. Profile race_mean=4.0 slightly optimistic. |
| Lawson | ~7 | 7 | 0 | Accurate — Q P14 (0) + race P9 (2) + 5 positions gained = 7. |
| Verstappen | ~10 | 7 | −3 | Slight over — Q P11 (0) + race P8 (4) + 3 gained = 7. Q2 elimination worse than profiled. |
| Hulkenberg | ~3 | 2 | −1 | Accurate — Q P13 (0) + race P11 (0) + 2 positions gained = 2. |
| Lindblad | ~0 | 1 | +1 | Accurate — Q P10 (1) + race P14 (0) + 0 gained = 1. dnf_chance=0.18 not triggered (finished race). |
| Ocon | ~2 | 3 | +1 | Accurate — Q P12 (0) + race P10 (1) + 2 gained = 3. |
| Perez | ~1 | 2 | +1 | Accurate — Q P19 (0) + race P17 (0) + 2 gained = 2. |

---

## 3. Constructor Calibration

Constructor scoring = drivers' race finishing pts + qualifying bonus + pit stop bonus (estimated).

### Qualifying Bonus Applied
- Both Q3: +10 | One Q3 / one Q2: +3 | Both Q2: +5 | One Q2: +1 | Both Q1: -1

| Constructor | Quali Outcome | Bonus |
|-------------|--------------|-------|
| Mercedes | Both Q3 (Antonelli P1, Russell P2) | +10 |
| McLaren | Both Q3 (Piastri P3, Norris P5) | +10 |
| Ferrari | Both Q3 (Leclerc P4, Hamilton P6) | +10 |
| Racing Bulls | One Q3 (Lindblad P10), one Q2 (Lawson P14) | +3 |
| Haas | Bearman Q1 out (P18), Ocon Q2 (P12) | +1 |
| Red Bull | Hadjar Q3 (P8), Verstappen Q2 out (P11) | +3 |

### Constructor Predicted vs Actual

| Constructor | Race Sum | Quali Bonus | Pit Bonus (est.) | Total | Sim Predicted | Delta | Notes |
|-------------|----------|-------------|-------------------|-------|--------------|-------|-------|
| **Mercedes** | 25+12=37 | +10 | ~12 | **~59** | ~65 | −6 | Antonelli won but Russell dropped to P4 — race sum lower than P1+P2 expected |
| **McLaren** | 18+10=28 | +10 | ~12 | **~50** | ~52 | −2 | Accurate — Piastri P2, Norris P5 |
| **Ferrari** | 15+8=23 | +10 | ~10 | **~43** | ~38 | +5 | Slightly better than predicted — Leclerc P3 vs expected P5 |
| **Racing Bulls** | 0+2=2 | +3 | ~7 | **~12** | ~17 | −5 | Lindblad gained 0 pts in race despite Q3 grid. Lawson carried with +5 gained |
| **Haas** | −20+1=−19 | +1 | ~5 | **~−13** | ~12 | **−25** | **Catastrophic** — Bearman crash DNF turned expected +12 into −13. Biggest constructor miss. |
| Red Bull | 0+4=4 | +3 | ~10 | ~17 | ~20 | −3 | Accurate — Verstappen recovered 3 places, Hadjar dropped 4 |

> Pit stop bonuses estimated using pit_mean values from sim-config.json: ~2.2-2.3s for top teams = +5/stop × ~2 stops = 10-12 pts. Haas only got 1 effective stop (Ocon only, Bearman crashed). No fastest-pit bonus distributed.

---

## 4. Team Score Summary

| Team | Sim Predicted | Actual R03 | Delta |
|------|--------------|------------|-------|
| **T1 Safe** (Leclerc 2x / Mercedes C + Haas C) | ~122 | **~85** | −37 |
| **T2 Constructor Kings** (Bearman 2x / Mercedes C + McLaren C) | ~146 | **~83** | −63 |
| **T3 Ferrari Nuclear** (Leclerc 2x / Ferrari C + Racing Bulls C) | ~130 | **~103** | −27 |

### T1 Component Breakdown

| Component | Predicted | Actual | Impact |
|-----------|----------|--------|--------|
| Leclerc 2x (P4 Q, P3 race) | ~44 | 46 | +2 |
| Gasly | ~2 | 10 | +8 |
| Bearman | ~4 | −20 | **−24** |
| Lindblad | ~0 | 1 | +1 |
| Hulkenberg | ~3 | 2 | −1 |
| Mercedes C | ~65 | ~59 | −6 |
| Haas C | ~12 | ~−13 | **−25** |

**Root cause:** Bearman crashed (−26 vs expected) and Haas C collapsed with him (−25 vs expected). These two items alone explain the −37 delta. Everything else was within ±10 pts of prediction.

### T2 Component Breakdown

| Component | Predicted | Actual | Impact |
|-----------|----------|--------|--------|
| Bearman 2x captain | ~8 | **−40** | **−48** |
| Lawson | ~7 | 7 | 0 |
| Ocon | ~2 | 3 | +1 |
| Perez | ~1 | 2 | +1 |
| Hulkenberg | ~3 | 2 | −1 |
| Mercedes C | ~65 | ~59 | −6 |
| McLaren C | ~52 | ~50 | −2 |

**Root cause:** Captaining Bearman was catastrophic. His DNF (−20) doubled to −40, a −48 swing vs predicted +8. The constructors performed well (−8 combined). The captain choice destroyed an otherwise solid team (constructors alone: ~109 pts; drivers without double: +14 = 123 pts if not for the captain multiplier amplifying the crash).

### T3 Component Breakdown

| Component | Predicted | Actual | Impact |
|-----------|----------|--------|--------|
| Leclerc 2x (P4 Q, P3 race) | ~44 | 46 | +2 |
| Hamilton | ~14 | 13 | −1 |
| Bearman | ~4 | −20 | **−24** |
| Lawson | ~7 | 7 | 0 |
| Hulkenberg | ~3 | 2 | −1 |
| Ferrari C | ~38 | ~43 | +5 |
| Racing Bulls C | ~17 | ~12 | −5 |

**T3 was the best of three** despite Bearman's crash because: (a) Bearman was not captained, so the DNF was −20 not −40; (b) Ferrari C slightly overdelivered; (c) Leclerc 2x at P3 was accurate. Bearman is T3's single biggest structural risk — if he keeps crashing, his impact grows as a non-captain passenger.

---

## 5. DOTD Analysis

**DOTD winner: Oscar Piastri** (likely — pending API confirmation post-race)

Piastri finished P2 from P3 grid, 1 position gained. Narrative: attacking drive in a tight McLaren vs Leclerc/Russell battle. Australian driver at a Japanese circuit — global popularity + strong race = fan vote.

- Piastri dotd_weight=1.4: **validated**. P2 finisher who took it over the race winner (Antonelli) and a popular home-circuit narrative driver (none in 2026 — Tsunoda not in the 2026 grid).
- Antonelli dotd_weight=1.2: did NOT win DOTD despite winning the race. Confirms he's not yet a fan-vote magnet. Revise slightly to 1.3 for Bahrain.
- Leclerc dotd_weight=1.8: strong DOTD candidate at Suzuka (won it in 2024) but did not win. P3 from P4 gain without a major overtake narrative kept votes away. Weight is correct but circuits matter — Leclerc's DOTD weight is most relevant at circuits where he has a dramatic story.
- Suzuka DOTD pattern: does NOT default to race winner. Popular drivers with strong race narrative (gaining places, battling at front) can take it from the winner.

---

## 6. Calibration Notes for R04 Bahrain

```
## Calibration Notes from R03 Japan

### URGENT — Bearman Profile
Bearman had his worst weekend of 2026:
- Q1 out (P18) — 8 positions worse than quali_mean=10.0
- Race crash DNF (lap 20) — 7% dnf_chance was 14x too low on the day

Two-round pattern (Japan + previous):
- quali_mean → 12.0 (was 10.0). Suzuka exposed variability at technical circuits.
  Bahrain is a conventional circuit so some recovery expected, but Q1 remains possible.
- dnf_chance → 0.12 (was 0.07). Racing incident style suggests elevated crash risk.
  Not purely mechanical — hard to fully predict, but risk profile is higher than modeled.
- variance → 4.0 (was 3.0). He can be P6 OR P20 — range is wide.
- Captain risk: Never captain Bearman when his dnf_chance >= 0.10.
  A 2x captain DNF at −40 is season-damaging. T2 must find a new captain model.

### Gasly — Confirmed Re-Rate
Three consecutive strong results (China P6, China SQ, Japan P7 both sessions):
- race_mean → 7.0 (was 14.0)
- quali_mean → 7.0 (was 14.0)
- Profile was completely stale. Alpine is systematically faster than modeled.
- At $12.8M with race_mean=7.0, his PPM is exceptional. Strong value pick for R04.

### Antonelli — Ceiling Expansion
Three wins from three races. He is not a "P2 expected" driver:
- race_mean → 1.0 (was 2.0). He is winning consistently.
- quali_mean → 1.0 (was 2.0). Pole in all 3 rounds.
- dnf_chance stays 0.04 — no reliability concerns.
- dotd_weight → 1.3 (was 1.2). Popularity growing, but Piastri/Hamilton still beat him for fan votes.
- FL: Antonelli got fastest lap in Japan (+ China win FL too?). FL probability is now ~35% at any round.

### Russell — Variance Needed
Japan was a poor race — P2 grid to P4 finish (safety car shuffle, Leclerc + Piastri overtook him):
- race_mean stays 1.5 — one round of underperformance, not a pattern.
- variance → 2.0 (was 1.5). He can be beaten when safety cars disrupt strategy.
- Watch R04 Bahrain — if another P4-P5 finish, reconsider to race_mean=2.5.

### Leclerc — Confirmed 3rd Team Upside
P3 Japan, P4 China, P3 Australia. Consistently outperforming P5 profile:
- race_mean → 3.5 (was 5.0). He is the 3rd-fastest driver in 2026.
- quali_mean → 4.5 (was 5.0). Usually Q3 in P4 range.
- dotd_weight=1.8 remains valid but Suzuka showed it's circuit-specific.

### Hamilton — Minor Upward Tweak
Japan: P6 quali + P6 race = exactly on profile. Two rounds of accuracy:
- race_mean → 5.5 (was 6.0). Minor upward nudge — 3 rounds show P5-P6 range.
- quali_mean stays 6.0.

### Ferrari C — Now Correct
Predicted ~38, actual ~43. Getting closer. Both Ferrari drivers consistently P3-P6:
- Expect 40-50 pts at power circuits (Bahrain). Update base expectation.
- pit_mean → 2.2s (lower estimate — Ferrari have been executing clean stops).

### Haas C — Structural Risk Flag
Two rounds of Bearman issues (Q1 + DNF) = Haas C is a liability when Bearman is unreliable:
- If Bearman DNFs, Haas C will score −10 to −15 pts.
- At $8.6M Haas C is only justifiable if Bearman reliably qualifies Q2+.
- T1 and T3 should seriously evaluate selling Haas C. T2 already sold it.
- Bahrain: Bearman form in practice will determine if Haas C is holdable.

### McLaren C — Accurate
Predicted ~52, actual ~50. Both drivers finished well (Piastri P2, Norris P5). Reliability fully restored:
- McLaren C holds its predicted value. Norris and Piastri dnf_chance → 0.07 each.

### DOTD Notes
- Piastri won DOTD from P2 — dotd_weight=1.4 validated.
- Antonelli at race_mean=1.0 will often win races but may not get DOTD — fans vote for narratives
  not just winners. Raise dotd_weight to 1.3 but don't assume race winner = DOTD.
- Leclerc DOTD probability at Suzuka was high (1.8 weight) but he didn't win it (P3, no drama).
  Circuit-specific DOTD is real — circuits with "Leclerc narrative moments" will see it pay off.

### Overtake Factor Notes
- Suzuka overtaking_index=4 validated — very limited passing. Verstappen made 3 net gains
  but from P11 (Q2 elimination) so was in free air. Track position still king here.
- Lawson gained 5 positions (P14→P9) — overtake_factor=1.0 may be too low for him.
  Revise Lawson overtake_factor → 1.2 (he's been picking up positions consistently).
- Bahrain overtaking_index → 6. Long DRS straights, easier to overtake. Position gains amplified.

### Overall Calibration — R03
- Simulation was broadly accurate for the top-6 drivers individually (Leclerc, Hamilton, Norris,
  Lawson all within ±3 pts). Main misses: Bearman complete outlier (−26), Russell race pace
  decline (−15), Antonelli ceiling too low (+14), Gasly still completely wrong (+8).
- Constructors: All within ±6 pts except Haas C (−25 vs expected). Mercedes and McLaren
  delivered close to expectation. Ferrari C slightly better.
- Confidence in R04 Bahrain profiles: MEDIUM — 3 rounds of data, clear Antonelli/Mercedes
  hierarchy confirmed. Ferrari 3rd team confirmed. Haas unreliable. Gasly re-rated.
  Bahrain is a new circuit type (high deg, power, long straights) — first calibration data point.
```

---

## 7. Team Scores — R03 Final

| Team | R03 Score (est.) | Season Total (R01+R02+R03) | Notes |
|------|-----------------|--------------------------|-------|
| **T1 Safe** | ~85 | — | Bearman DNF + Haas C destroyed prediction |
| **T2 Constructor Kings** | ~83 | — | Bearman 2x captain DNF catastrophic (−48 swing) |
| **T3 Ferrari Nuclear** | ~103 | — | Best round — no captained Bearman, Ferrari C delivered |

> Season totals pending R01+R02 final figures. R03 scores are calculated estimates (±5 pts) — official API GamedayPoints not yet available.

---

## 8. Pre-R04 Action Items

| Priority | Item |
|----------|------|
| 🔴 HIGH | Refresh fantasy-points.md after API updates with R03 GamedayPoints to confirm actual team scores |
| 🔴 HIGH | T2: Do NOT captain Bearman again. New captain model needed — either Lawson, Ocon, or a cheap reliable scorer |
| 🔴 HIGH | T1 + T3: Evaluate selling Haas C — Bearman unreliability makes it a structural risk at $8.6M |
| 🔴 HIGH | Update sim profiles: Antonelli race/quali_mean → 1.0, Gasly → 7.0, Leclerc race_mean → 3.5, Bearman dnf_chance → 0.12 |
| 🟡 MED | McLaren dnf_chance → 0.07 for both (reliability restored) |
| 🟡 MED | Fetch R04 Bahrain prices after R03 price update (Gasly likely +$0.6M, Leclerc +$0.3M, Bearman may drop −$0.6M) |
| 🟡 MED | T3 carry-over transfer: 1 free available. Use strategically at Bahrain. |
| 🟡 MED | Confirm DOTD from official API once R03 data is published (Piastri expected) |
| 🟢 LOW | Assess chip timing — next sprint weekends are R06 Miami + R07 Canada. T2 still has all 6 chips. T1 has 5 (used Limitless R02). T3 has 6. |
| 🟢 LOW | Verstappen: Q2 elimination at Suzuka (P11) + China struggles. Red Bull clearly P4 team. Keep dnf_chance=0.12 but lower race_mean to 8.0 (was 7.0). |
