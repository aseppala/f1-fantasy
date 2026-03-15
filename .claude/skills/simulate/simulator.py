#!/usr/bin/env python3
"""F1 Fantasy Monte Carlo scoring simulator."""

import argparse
import random
from dataclasses import dataclass, field


# --- Scoring tables from 2026-fantasy-rules.md ---

QUALI_POINTS = {1: 10, 2: 9, 3: 8, 4: 7, 5: 6, 6: 5, 7: 4, 8: 3, 9: 2, 10: 1}
# P11-P20 = 0, NC/DSQ = -5

RACE_POINTS = {1: 25, 2: 18, 3: 15, 4: 12, 5: 10, 6: 8, 7: 6, 8: 4, 9: 2, 10: 1}
# P11+ = 0, DNF/DSQ = -20

FASTEST_LAP_BONUS = 10
DOTD_BONUS = 10

# Constructor qualifying bonuses
# Both Q3 = +10, Both Q2 = +5, One Q3 = +3, One Q2 = +1, Both Q1 = -1

# Pit stop bonuses
PIT_STOP_TIERS = [
    (0.0, 1.80, 15),   # Record-breaking
    (1.80, 2.00, 10),  # < 2.0s
    (2.00, 2.20, 10),  # 2.0 - 2.19s
    (2.20, 2.50, 5),   # 2.2 - 2.49s
    (2.50, 3.00, 2),   # 2.5 - 2.99s
]
FASTEST_PIT_BONUS = 5


@dataclass
class DriverProfile:
    name: str
    team: str
    price: float
    quali_mean: float
    race_mean: float
    variance: float
    dnf_chance: float
    overtake_factor: float = 1.0
    dotd_weight: float = 1.0  # fan popularity multiplier for DOTD voting


@dataclass
class ConstructorProfile:
    name: str
    price: float
    pit_mean: float  # average pit stop time in seconds
    drivers: list = field(default_factory=list)  # filled in at runtime


@dataclass
class DriverResult:
    name: str
    team: str
    price: float
    quali_pos: int = 0
    race_pos: int = 0
    dnf: bool = False
    overtakes: int = 0
    positions_gained: int = 0
    fastest_lap: bool = False
    dotd: bool = False
    points: float = 0.0


def get_quali_phase(pos: int) -> str:
    if pos <= 10:
        return "Q3"
    elif pos <= 15:
        return "Q2"
    else:
        return "Q1"


def score_driver(result: DriverResult) -> float:
    pts = 0.0

    # Qualifying
    pts += QUALI_POINTS.get(result.quali_pos, 0)

    # Race
    if result.dnf:
        pts -= 20
    else:
        pts += RACE_POINTS.get(result.race_pos, 0)
        # Positions gained (quali -> race)
        gained = max(0, result.quali_pos - result.race_pos)
        pts += gained
        # Overtakes
        pts += result.overtakes

    # Bonuses
    if result.fastest_lap:
        pts += FASTEST_LAP_BONUS
    if result.dotd:
        pts += DOTD_BONUS

    result.points = pts
    return pts


def score_constructor(con: ConstructorProfile, driver_results: dict[str, DriverResult]) -> float:
    d1, d2 = con.drivers
    r1 = driver_results[d1]
    r2 = driver_results[d2]

    pts = 0.0

    # Qualifying bonus
    phase1 = get_quali_phase(r1.quali_pos)
    phase2 = get_quali_phase(r2.quali_pos)

    if phase1 == "Q3" and phase2 == "Q3":
        pts += 10
    elif phase1 == "Q3" or phase2 == "Q3":
        pts += 3
        if phase1 == "Q2" or phase2 == "Q2":
            pass  # one Q3 already counted
    elif phase1 == "Q2" and phase2 == "Q2":
        pts += 5
    elif phase1 == "Q2" or phase2 == "Q2":
        pts += 1
    elif phase1 == "Q1" and phase2 == "Q1":
        pts -= 1

    # Race points: sum of both drivers
    for r in (r1, r2):
        if r.dnf:
            pts -= 20
        else:
            pts += RACE_POINTS.get(r.race_pos, 0)

    # Pit stop bonus (sample one pit stop per constructor)
    pit_time = random.gauss(con.pit_mean, 0.3)
    for low, high, bonus in PIT_STOP_TIERS:
        if low <= pit_time < high:
            pts += bonus
            break

    return pts


def simulate_weekend(drivers: list[DriverProfile], constructors: list[ConstructorProfile],
                     circuit_overtaking_index: int = 5) -> tuple[dict[str, float], dict[str, float], dict[str, DriverResult]]:
    """Run one simulated race weekend. Returns (driver_points, constructor_points, driver_results)."""
    n = len(drivers)

    # --- Qualifying ---
    quali_scores = []
    for d in drivers:
        score = random.gauss(d.quali_mean, d.variance)
        quali_scores.append((score, d))
    quali_scores.sort(key=lambda x: x[0])

    driver_results: dict[str, DriverResult] = {}
    for pos_idx, (_, d) in enumerate(quali_scores):
        result = DriverResult(name=d.name, team=d.team, price=d.price)
        result.quali_pos = pos_idx + 1
        driver_results[d.name] = result

    # --- Race ---
    dnf_drivers = set()
    race_scores = []
    for d in drivers:
        if random.random() < d.dnf_chance:
            dnf_drivers.add(d.name)
            driver_results[d.name].dnf = True
        else:
            score = random.gauss(d.race_mean, d.variance)
            race_scores.append((score, d))

    race_scores.sort(key=lambda x: x[0])
    for pos_idx, (_, d) in enumerate(race_scores):
        driver_results[d.name].race_pos = pos_idx + 1

    # DNF drivers get no race position
    for name in dnf_drivers:
        driver_results[name].race_pos = 0

    # --- Overtakes ---
    # Scale overtake_factor by circuit overtaking index (5 = neutral, 10 = Monza, 1 = Monaco)
    overtake_scale = circuit_overtaking_index / 5.0
    driver_map = {d.name: d for d in drivers}
    for name, r in driver_results.items():
        if r.dnf:
            continue
        gained = max(0, r.quali_pos - r.race_pos)
        r.positions_gained = gained
        ot = max(0, round(random.gauss(gained * driver_map[name].overtake_factor * overtake_scale, 1.5)))
        r.overtakes = ot

    # --- Fastest lap: weighted random among top-10 finishers ---
    top10 = [r for r in driver_results.values() if not r.dnf and r.race_pos <= 10]
    if top10:
        # Front-runners more likely
        weights = [max(1, 11 - r.race_pos) for r in top10]
        fl_winner = random.choices(top10, weights=weights, k=1)[0]
        fl_winner.fastest_lap = True

    # --- DotD: fan-voted, weighted by popularity + positions gained + podium ---
    # dotd_weight captures fan popularity (high for Hamilton, Leclerc, Norris, Russell)
    # positions gained 5+ creates a strong narrative hook for voters
    all_finishers = [r for r in driver_results.values() if not r.dnf]
    if all_finishers:
        dotd_weights = []
        for r in all_finishers:
            popularity = driver_map[r.name].dotd_weight
            positions_narrative = max(1, r.positions_gained * 2) if r.positions_gained >= 5 else max(0.5, r.positions_gained * 0.5)
            w = popularity * positions_narrative
            if r.race_pos == 1:
                w += 5 * popularity
            elif r.race_pos <= 3:
                w += 2 * popularity
            dotd_weights.append(max(0.1, w))
        dotd_winner = random.choices(all_finishers, weights=dotd_weights, k=1)[0]
        dotd_winner.dotd = True

    # --- Score all drivers ---
    driver_points = {}
    for name, r in driver_results.items():
        driver_points[name] = score_driver(r)

    # --- Score constructors ---
    constructor_points = {}
    for con in constructors:
        constructor_points[con.name] = score_constructor(con, driver_results)

    return driver_points, constructor_points, driver_results


def run_simulation(drivers: list[DriverProfile], constructors: list[ConstructorProfile],
                   num_sims: int, teams: dict | None = None,
                   circuit_overtaking_index: int = 5) -> None:
    """Run Monte Carlo simulation and print results."""

    driver_totals: dict[str, list[float]] = {d.name: [] for d in drivers}
    con_totals: dict[str, list[float]] = {c.name: [] for c in constructors}
    team_totals: dict[str, list[float]] = {t: [] for t in (teams or {})}

    driver_map = {d.name: d for d in drivers}

    for _ in range(num_sims):
        dp, cp, dr = simulate_weekend(drivers, constructors, circuit_overtaking_index)

        for name, pts in dp.items():
            driver_totals[name].append(pts)
        for name, pts in cp.items():
            con_totals[name].append(pts)

        if teams:
            for team_name, team_def in teams.items():
                total = 0.0
                captain = team_def.get("captain", "")
                for dname in team_def["drivers"]:
                    pts = dp.get(dname, 0.0)
                    if dname == captain:
                        pts *= 2
                    total += pts
                for cname in team_def["constructors"]:
                    total += cp.get(cname, 0.0)
                team_totals[team_name].append(total)

    return driver_totals, con_totals, team_totals, driver_map


def print_results(drivers, constructors, driver_totals, con_totals, team_totals,
                  driver_map, num_sims, show_drivers=True, show_constructors=True, show_teams=True):
    print(f"\n=== F1 Fantasy Monte Carlo ({num_sims} sims) ===")

    if show_drivers:
        print(f"\n--- Driver Rankings (by expected fantasy points) ---")
        print(f" {'#':>2}  {'Driver':<20} {'Team':<16} {'Price':>7}   {'Avg Pts':>7}  {'Std Dev':>8}  {'PPM':>5}")
        print(f" {'':->2}  {'':->20} {'':->16} {'':->7}   {'':->7}  {'':->8}  {'':->5}")

        stats = []
        for d in drivers:
            vals = driver_totals[d.name]
            avg = sum(vals) / len(vals)
            std = (sum((v - avg) ** 2 for v in vals) / len(vals)) ** 0.5
            ppm = avg / d.price if d.price > 0 else 0
            stats.append((d, avg, std, ppm))

        stats.sort(key=lambda x: -x[1])
        for i, (d, avg, std, ppm) in enumerate(stats, 1):
            print(f" {i:>2}  {d.name:<20} {d.team:<16} ${d.price:>5.1f}M   {avg:>7.1f}  ±{std:>6.1f}  {ppm:>5.2f}")

    if show_constructors:
        print(f"\n--- Constructor Rankings ---")
        print(f" {'#':>2}  {'Constructor':<20} {'Price':>7}   {'Avg Pts':>7}  {'Std Dev':>8}  {'PPM':>5}")
        print(f" {'':->2}  {'':->20} {'':->7}   {'':->7}  {'':->8}  {'':->5}")

        con_stats = []
        for c in constructors:
            vals = con_totals[c.name]
            avg = sum(vals) / len(vals)
            std = (sum((v - avg) ** 2 for v in vals) / len(vals)) ** 0.5
            ppm = avg / c.price if c.price > 0 else 0
            con_stats.append((c, avg, std, ppm))

        con_stats.sort(key=lambda x: -x[1])
        for i, (c, avg, std, ppm) in enumerate(con_stats, 1):
            print(f" {i:>2}  {c.name:<20} ${c.price:>5.1f}M   {avg:>7.1f}  ±{std:>6.1f}  {ppm:>5.2f}")

    if show_teams and team_totals:
        print(f"\n--- Team Comparison ---")
        print(f" {'Team':<30} {'Avg Total':>9}  {'Std Dev':>8}  {'Min':>7}  {'Max':>7}")
        print(f" {'':->30} {'':->9}  {'':->8}  {'':->7}  {'':->7}")

        for name, vals in team_totals.items():
            avg = sum(vals) / len(vals)
            std = (sum((v - avg) ** 2 for v in vals) / len(vals)) ** 0.5
            mn = min(vals)
            mx = max(vals)
            print(f" {name:<30} {avg:>9.1f}  ±{std:>6.1f}  {mn:>7.1f}  {mx:>7.1f}")


# --- Default profiles for Australian GP ---

def get_australia_profiles() -> tuple[list[DriverProfile], list[ConstructorProfile]]:
    # Albert Park overtaking index: 5 (neutral)
    drivers = [
        # S Tier: top teams, consistent front-runners
        DriverProfile("Leclerc", "Ferrari", 22.8, quali_mean=3, race_mean=3, variance=2.5, dnf_chance=0.05, overtake_factor=1.0, dotd_weight=1.6),
        DriverProfile("Piastri", "McLaren", 25.5, quali_mean=3, race_mean=3.5, variance=2.5, dnf_chance=0.05, overtake_factor=1.1, dotd_weight=1.5),  # home race hero
        DriverProfile("Russell", "Mercedes", 27.4, quali_mean=3.5, race_mean=3, variance=2.5, dnf_chance=0.05, overtake_factor=1.0, dotd_weight=1.3),
        DriverProfile("Norris", "McLaren", 27.2, quali_mean=3.5, race_mean=4, variance=2.5, dnf_chance=0.05, overtake_factor=1.0, dotd_weight=1.4),

        # A Tier: fast but slightly less consistent or lower pace
        DriverProfile("Hamilton", "Ferrari", 22.5, quali_mean=5, race_mean=4.5, variance=3.0, dnf_chance=0.05, overtake_factor=1.1, dotd_weight=1.8),
        DriverProfile("Antonelli", "Mercedes", 23.2, quali_mean=4.5, race_mean=4.5, variance=3.0, dnf_chance=0.05, overtake_factor=1.0, dotd_weight=1.2),
        DriverProfile("Verstappen", "Red Bull", 27.7, quali_mean=4, race_mean=5.5, variance=3.0, dnf_chance=0.05, overtake_factor=1.2, dotd_weight=1.0),

        # B+ Tier
        DriverProfile("Hadjar", "Red Bull", 15.1, quali_mean=8, race_mean=8, variance=3.0, dnf_chance=0.07, overtake_factor=1.0, dotd_weight=1.0),

        # B Tier: midfield with potential
        DriverProfile("Bearman", "Haas", 7.4, quali_mean=12, race_mean=11, variance=3.5, dnf_chance=0.08, overtake_factor=1.3, dotd_weight=1.2),
        DriverProfile("Ocon", "Haas", 7.3, quali_mean=11, race_mean=12, variance=3.5, dnf_chance=0.08, overtake_factor=1.1, dotd_weight=1.0),
        DriverProfile("Lindblad", "Racing Bulls", 5.5, quali_mean=13, race_mean=13, variance=3.5, dnf_chance=0.08, overtake_factor=1.0, dotd_weight=1.0),
        DriverProfile("Lawson", "Racing Bulls", 6.5, quali_mean=14, race_mean=14, variance=3.5, dnf_chance=0.08, overtake_factor=1.0, dotd_weight=1.0),

        # C Tier: lower midfield
        DriverProfile("Gasly", "Alpine", 9.0, quali_mean=14, race_mean=14, variance=3.5, dnf_chance=0.08, overtake_factor=1.0, dotd_weight=1.0),
        DriverProfile("Hulkenberg", "Audi", 8.0, quali_mean=13, race_mean=13, variance=3.5, dnf_chance=0.08, overtake_factor=0.9, dotd_weight=1.0),
        DriverProfile("Sainz", "Williams", 12.0, quali_mean=13, race_mean=12, variance=3.5, dnf_chance=0.08, overtake_factor=1.0, dotd_weight=1.1),
        DriverProfile("Albon", "Williams", 10.0, quali_mean=15, race_mean=15, variance=3.5, dnf_chance=0.08, overtake_factor=1.0, dotd_weight=1.0),
        DriverProfile("Colapinto", "Alpine", 6.5, quali_mean=16, race_mean=16, variance=3.5, dnf_chance=0.08, overtake_factor=0.9, dotd_weight=1.0),
        DriverProfile("Bortoleto", "Audi", 6.5, quali_mean=15, race_mean=15, variance=3.5, dnf_chance=0.08, overtake_factor=0.9, dotd_weight=1.0),

        # D Tier: backmarkers
        DriverProfile("Alonso", "Aston Martin", 10.0, quali_mean=18, race_mean=18, variance=3.0, dnf_chance=0.12, overtake_factor=1.0, dotd_weight=1.2),
        DriverProfile("Stroll", "Aston Martin", 8.0, quali_mean=19, race_mean=19, variance=3.0, dnf_chance=0.12, overtake_factor=0.8, dotd_weight=0.8),
        DriverProfile("Bottas", "Cadillac", 5.9, quali_mean=20, race_mean=20, variance=3.0, dnf_chance=0.12, overtake_factor=0.8, dotd_weight=0.9),
        DriverProfile("Perez", "Cadillac", 6.0, quali_mean=21, race_mean=21, variance=3.0, dnf_chance=0.12, overtake_factor=0.8, dotd_weight=0.9),
    ]

    constructors = [
        ConstructorProfile("McLaren", 28.9, pit_mean=2.3),
        ConstructorProfile("Mercedes", 27.5, pit_mean=2.3),
        ConstructorProfile("Red Bull", 26.0, pit_mean=2.2),
        ConstructorProfile("Ferrari", 25.0, pit_mean=2.3),
        ConstructorProfile("Williams", 12.0, pit_mean=2.5),
        ConstructorProfile("Aston Martin", 10.0, pit_mean=2.6),
        ConstructorProfile("Alpine", 8.0, pit_mean=2.5),
        ConstructorProfile("Haas", 7.4, pit_mean=2.5),
        ConstructorProfile("Racing Bulls", 6.3, pit_mean=2.4),
        ConstructorProfile("Audi", 7.0, pit_mean=2.6),
        ConstructorProfile("Cadillac", 5.5, pit_mean=2.8),
    ]

    # Wire up drivers to constructors
    con_map = {c.name: c for c in constructors}
    for d in drivers:
        con_map[d.team].drivers.append(d.name)

    return drivers, constructors


def get_default_teams() -> dict:
    return {
        "Team 1 (Safe PPM)": {
            "drivers": ["Leclerc", "Antonelli", "Bearman", "Lindblad", "Bottas"],
            "constructors": ["Ferrari", "Haas"],
            "captain": "Leclerc",
        },
        "Team 2 (Constructor Kings)": {
            "drivers": ["Hadjar", "Antonelli", "Bearman", "Lindblad", "Bottas"],
            "constructors": ["Ferrari", "Mercedes"],
            "captain": "Hadjar",
        },
        "Team 3 (Ferrari Nuclear)": {
            "drivers": ["Leclerc", "Hamilton", "Bearman", "Lindblad", "Bottas"],
            "constructors": ["Ferrari", "Racing Bulls"],
            "captain": "Leclerc",
        },
    }


# --- China GP profiles (Round 2) ---

def get_china_profiles() -> tuple[list[DriverProfile], list[ConstructorProfile]]:
    """Profiles for Chinese GP based on R01 results + FP1 + Sprint Qualifying."""
    # Shanghai overtaking index: 6 (above neutral, good DRS zones)
    drivers = [
        # S Tier: Mercedes dominant (1-2 in R01, 1-2 FP1, 1-2 SQ)
        DriverProfile("Russell", "Mercedes", 27.7, quali_mean=1.5, race_mean=1.5, variance=1.5, dnf_chance=0.04, overtake_factor=1.0, dotd_weight=1.3),
        DriverProfile("Antonelli", "Mercedes", 23.5, quali_mean=2.5, race_mean=2.5, variance=2.0, dnf_chance=0.06, overtake_factor=1.0, dotd_weight=1.2),

        # A Tier: McLaren + Ferrari fighting for P3-P6
        DriverProfile("Norris", "McLaren", 27.2, quali_mean=3.5, race_mean=4, variance=2.5, dnf_chance=0.05, overtake_factor=1.0, dotd_weight=1.4),
        DriverProfile("Hamilton", "Ferrari", 22.6, quali_mean=4.5, race_mean=4.5, variance=2.5, dnf_chance=0.05, overtake_factor=1.1, dotd_weight=1.8),
        DriverProfile("Piastri", "McLaren", 25.2, quali_mean=5, race_mean=4, variance=2.5, dnf_chance=0.05, overtake_factor=1.1, dotd_weight=1.1),
        DriverProfile("Leclerc", "Ferrari", 23.1, quali_mean=5.5, race_mean=5, variance=2.5, dnf_chance=0.05, overtake_factor=1.0, dotd_weight=1.6),

        # B Tier: Gasly surprise P7 in SQ, Verstappen P8
        DriverProfile("Gasly", "Alpine", 12.2, quali_mean=8, race_mean=9, variance=3.5, dnf_chance=0.07, overtake_factor=1.0, dotd_weight=1.0),
        DriverProfile("Verstappen", "Red Bull", 28.0, quali_mean=7, race_mean=7, variance=3.0, dnf_chance=0.05, overtake_factor=1.3, dotd_weight=1.0),

        # C Tier: midfield (SQ P9-P16)
        DriverProfile("Bearman", "Haas", 8.0, quali_mean=10, race_mean=9, variance=3.0, dnf_chance=0.07, overtake_factor=1.3, dotd_weight=1.2),
        DriverProfile("Hadjar", "Red Bull", 14.5, quali_mean=10, race_mean=10, variance=3.5, dnf_chance=0.08, overtake_factor=1.0, dotd_weight=1.0),
        DriverProfile("Hulkenberg", "Audi", 8.0, quali_mean=11, race_mean=12, variance=3.5, dnf_chance=0.07, overtake_factor=0.9, dotd_weight=1.0),
        DriverProfile("Ocon", "Haas", 7.3, quali_mean=12, race_mean=11, variance=3.5, dnf_chance=0.07, overtake_factor=1.1, dotd_weight=1.0),
        DriverProfile("Lawson", "Racing Bulls", 6.5, quali_mean=13, race_mean=13, variance=3.5, dnf_chance=0.07, overtake_factor=1.0, dotd_weight=1.0),
        DriverProfile("Bortoleto", "Audi", 7.0, quali_mean=14, race_mean=14, variance=3.5, dnf_chance=0.07, overtake_factor=0.9, dotd_weight=1.0),
        DriverProfile("Lindblad", "Racing Bulls", 6.1, quali_mean=15, race_mean=15, variance=3.5, dnf_chance=0.08, overtake_factor=1.0, dotd_weight=1.0),
        DriverProfile("Colapinto", "Alpine", 6.4, quali_mean=16, race_mean=16, variance=3.5, dnf_chance=0.07, overtake_factor=0.9, dotd_weight=1.0),

        # D Tier: backmarkers (SQ P17+)
        DriverProfile("Sainz", "Williams", 12.0, quali_mean=17, race_mean=16, variance=3.5, dnf_chance=0.08, overtake_factor=1.0, dotd_weight=1.1),
        DriverProfile("Albon", "Williams", 10.0, quali_mean=18, race_mean=17, variance=3.5, dnf_chance=0.07, overtake_factor=1.0, dotd_weight=1.0),
        DriverProfile("Alonso", "Aston Martin", 10.0, quali_mean=19, race_mean=18, variance=3.0, dnf_chance=0.12, overtake_factor=1.0, dotd_weight=1.2),
        DriverProfile("Stroll", "Aston Martin", 8.0, quali_mean=20, race_mean=20, variance=3.0, dnf_chance=0.12, overtake_factor=0.8, dotd_weight=0.8),
        DriverProfile("Bottas", "Cadillac", 5.3, quali_mean=21, race_mean=21, variance=3.0, dnf_chance=0.10, overtake_factor=0.8, dotd_weight=0.9),
        DriverProfile("Perez", "Cadillac", 6.0, quali_mean=22, race_mean=22, variance=3.0, dnf_chance=0.10, overtake_factor=0.8, dotd_weight=0.9),
    ]

    constructors = [
        ConstructorProfile("Mercedes", 27.8, pit_mean=2.3),
        ConstructorProfile("McLaren", 28.8, pit_mean=2.3),
        ConstructorProfile("Ferrari", 23.6, pit_mean=2.3),
        ConstructorProfile("Red Bull", 25.5, pit_mean=2.2),
        ConstructorProfile("Haas", 8.0, pit_mean=2.5),
        ConstructorProfile("Audi", 7.0, pit_mean=2.6),
        ConstructorProfile("Alpine", 8.0, pit_mean=2.5),
        ConstructorProfile("Racing Bulls", 6.9, pit_mean=2.4),
        ConstructorProfile("Williams", 12.0, pit_mean=2.5),
        ConstructorProfile("Aston Martin", 9.4, pit_mean=2.6),
        ConstructorProfile("Cadillac", 4.9, pit_mean=2.8),
    ]

    con_map = {c.name: c for c in constructors}
    for d in drivers:
        con_map[d.team].drivers.append(d.name)

    return drivers, constructors


def get_china_teams() -> dict:
    return {
        # --- Team 1 variants ---
        "T1 Safe (Limitless)": {
            "drivers": ["Russell", "Antonelli", "Norris", "Piastri", "Leclerc"],
            "constructors": ["Mercedes", "McLaren"],
            "captain": "Russell",
        },
        "T1 Alt: Hamilton over Leclerc": {
            "drivers": ["Russell", "Antonelli", "Norris", "Piastri", "Hamilton"],
            "constructors": ["Mercedes", "McLaren"],
            "captain": "Russell",
        },
        # --- Team 2 variants ---
        "T2 Constructor Kings (Hadjar 2x)": {
            "drivers": ["Hadjar", "Bearman", "Bortoleto", "Lindblad", "Ocon"],
            "constructors": ["Mercedes", "McLaren"],
            "captain": "Hadjar",
        },
        "T2 Alt: Bearman 2x": {
            "drivers": ["Hadjar", "Bearman", "Bortoleto", "Lindblad", "Ocon"],
            "constructors": ["Mercedes", "McLaren"],
            "captain": "Bearman",
        },
        "T2 Alt: Gasly over Hadjar": {
            "drivers": ["Bearman", "Gasly", "Ocon", "Lindblad", "Hulkenberg"],
            "constructors": ["Mercedes", "McLaren"],
            "captain": "Bearman",
        },
        "T2 Alt: Keep Hadjar + Ferrari C": {
            "drivers": ["Hadjar", "Bearman", "Ocon", "Lindblad", "Hulkenberg"],
            "constructors": ["Mercedes", "Ferrari"],
            "captain": "Bearman",
        },
        # --- Team 3 variants ---
        "T3 Ferrari Nuclear (Leclerc 2x)": {
            "drivers": ["Leclerc", "Hamilton", "Bearman", "Lindblad", "Bottas"],
            "constructors": ["Ferrari", "Racing Bulls"],
            "captain": "Leclerc",
        },
        "T3 Alt: Hamilton 2x": {
            "drivers": ["Leclerc", "Hamilton", "Bearman", "Lindblad", "Bottas"],
            "constructors": ["Ferrari", "Racing Bulls"],
            "captain": "Hamilton",
        },
    }


def parse_args():
    parser = argparse.ArgumentParser(description="F1 Fantasy Monte Carlo Simulator")
    parser.add_argument("--sims", type=int, default=1000, help="Number of simulations (default: 1000)")
    parser.add_argument("--drivers-only", action="store_true", help="Only show driver rankings")
    parser.add_argument("--constructors-only", action="store_true", help="Only show constructor rankings")
    parser.add_argument("--team", type=str, help="Comma-separated driver names for custom team")
    parser.add_argument("--constructors", type=str, help="Comma-separated constructor names for custom team")
    parser.add_argument("--captain", type=str, help="Captain (2x) driver for custom team")
    parser.add_argument("--seed", type=int, help="Random seed for reproducibility")
    parser.add_argument("--race", type=str, default="australia", choices=["australia", "china"],
                        help="Race weekend profiles to use (default: australia)")
    parser.add_argument("--overtaking-index", type=int, default=None,
                        help="Circuit overtaking index 1-10 (overrides race default; 1=Monaco, 10=Monza, 5=neutral)")
    return parser.parse_args()


def main():
    args = parse_args()

    if args.seed is not None:
        random.seed(args.seed)

    if args.race == "china":
        drivers, constructors = get_china_profiles()
        teams = get_china_teams()
        default_overtaking_index = 6
    else:
        drivers, constructors = get_australia_profiles()
        teams = get_default_teams()
        default_overtaking_index = 5

    circuit_overtaking_index = args.overtaking_index if args.overtaking_index is not None else default_overtaking_index

    # Add custom team if specified
    if args.team:
        custom_drivers = [d.strip() for d in args.team.split(",")]
        custom_cons = [c.strip() for c in args.constructors.split(",")] if args.constructors else []
        captain = args.captain.strip() if args.captain else custom_drivers[0]
        teams["Custom Team"] = {
            "drivers": custom_drivers,
            "constructors": custom_cons,
            "captain": captain,
        }

    show_drivers = not args.constructors_only
    show_constructors = not args.drivers_only
    show_teams = not args.drivers_only and not args.constructors_only

    driver_totals, con_totals, team_totals, driver_map = run_simulation(
        drivers, constructors, args.sims, teams if show_teams else None,
        circuit_overtaking_index=circuit_overtaking_index
    )

    print_results(
        drivers, constructors, driver_totals, con_totals, team_totals,
        driver_map, args.sims,
        show_drivers=show_drivers,
        show_constructors=show_constructors,
        show_teams=show_teams,
    )


if __name__ == "__main__":
    main()
