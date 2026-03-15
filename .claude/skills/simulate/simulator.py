#!/usr/bin/env python3
"""F1 Fantasy Monte Carlo scoring simulator."""

import argparse
import json
import random
from dataclasses import dataclass, field
from typing import Any


# --- Scoring tables from 2026-fantasy-rules.md ---

QUALI_POINTS = {1: 10, 2: 9, 3: 8, 4: 7, 5: 6, 6: 5, 7: 4, 8: 3, 9: 2, 10: 1}
# P11-P20 = 0, NC/DSQ = -5

RACE_POINTS = {1: 25, 2: 18, 3: 15, 4: 12, 5: 10, 6: 8, 7: 6, 8: 4, 9: 2, 10: 1}
# P11+ = 0, DNF/DSQ = -20

SPRINT_POINTS = {1: 8, 2: 7, 3: 6, 4: 5, 5: 4, 6: 3, 7: 2, 8: 1}
# P9+ = 0, DNF = -10

FASTEST_LAP_BONUS = 10
SPRINT_FASTEST_LAP_BONUS = 5
DOTD_BONUS = 10

# Constructor qualifying bonuses
# Both Q3 = +10, Both Q2 = +5, One Q3 = +5, One Q2 = +1, Both Q1 = -1

# Pit stop bonuses (official):
#   <2.0s = +20; world record (<1.8s) adds +15 on top → +35 total
#   2.0–2.19s = +10, 2.2–2.49s = +5, 2.5–2.99s = +2, >=3.0s = 0
PIT_STOP_TIERS = [
    (2.00, 2.20, 10),
    (2.20, 2.50, 5),
    (2.50, 3.00, 2),
]
PIT_STOP_UNDER_2S_BONUS = 20
PIT_STOP_WORLD_RECORD_THRESHOLD = 1.8
PIT_STOP_WORLD_RECORD_EXTRA = 15  # on top of +20 → +35 total
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
    drivers: list[str] = field(default_factory=list)  # filled in at runtime


@dataclass
class DriverResult:
    name: str
    team: str
    price: float
    quali_pos: int = 0
    race_pos: int = 0
    dnf: bool = False
    overtakes: int = 0
    positions_delta: int = 0  # quali_pos - race_pos; +ve = gained, -ve = lost
    fastest_lap: bool = False
    dotd: bool = False
    points: float = 0.0
    # Sprint fields
    sprint_start_pos: int = 0
    sprint_race_pos: int = 0
    sprint_dnf: bool = False
    sprint_positions_delta: int = 0
    sprint_overtakes: int = 0
    sprint_fastest_lap: bool = False
    sprint_points: float = 0.0


def get_quali_phase(pos: int) -> str:
    if pos <= 10:
        return "Q3"
    elif pos <= 15:
        return "Q2"
    else:
        return "Q1"


def _constructor_quali_bonus(phase1: str, phase2: str) -> float:
    if phase1 == "Q3" and phase2 == "Q3":
        return 10
    elif phase1 == "Q3" or phase2 == "Q3":
        return 5  # one Q3 = +5
    elif phase1 == "Q2" and phase2 == "Q2":
        return 5  # both Q2 = +5
    elif phase1 == "Q2" or phase2 == "Q2":
        return 1
    else:  # both Q1
        return -1


def score_driver(result: DriverResult) -> float:
    pts = 0.0

    # Qualifying
    pts += QUALI_POINTS.get(result.quali_pos, 0)

    # Race
    if result.dnf:
        pts -= 20
    else:
        pts += RACE_POINTS.get(result.race_pos, 0)
        # Positions delta: +1 per gained, -1 per lost
        pts += result.positions_delta
        # Overtakes (only counted when positions gained)
        pts += result.overtakes

    # Bonuses
    if result.fastest_lap:
        pts += FASTEST_LAP_BONUS
    if result.dotd:
        pts += DOTD_BONUS

    result.points = pts
    return pts


def score_driver_sprint(result: DriverResult) -> float:
    """Score sprint qualifying + sprint race for a driver."""
    pts = 0.0

    # Sprint qualifying (same points table as main qualifying)
    pts += QUALI_POINTS.get(result.sprint_start_pos, 0)

    # Sprint race
    if result.sprint_dnf:
        pts -= 10
    else:
        pts += SPRINT_POINTS.get(result.sprint_race_pos, 0)
        pts += result.sprint_positions_delta
        pts += result.sprint_overtakes

    if result.sprint_fastest_lap:
        pts += SPRINT_FASTEST_LAP_BONUS

    result.sprint_points = pts
    return pts


def _pit_stop_bonus(pit_time: float) -> float:
    if pit_time < 2.0:
        bonus = PIT_STOP_UNDER_2S_BONUS
        if pit_time < PIT_STOP_WORLD_RECORD_THRESHOLD:
            bonus += PIT_STOP_WORLD_RECORD_EXTRA
        return bonus
    for low, high, bonus in PIT_STOP_TIERS:
        if low <= pit_time < high:
            return bonus
    return 0


def score_constructor(con: ConstructorProfile, driver_results: dict[str, DriverResult]) -> float:
    d1, d2 = con.drivers
    r1 = driver_results[d1]
    r2 = driver_results[d2]

    pts = 0.0

    # Constructor qualifying tier bonus
    phase1 = get_quali_phase(r1.quali_pos)
    phase2 = get_quali_phase(r2.quali_pos)
    pts += _constructor_quali_bonus(phase1, phase2)

    # Both drivers' full points (excluding DOTD — constructor does not get DOTD bonus)
    # r.points is already computed by score_driver() before this is called
    for r in (r1, r2):
        driver_pts = r.points
        if r.dotd:
            driver_pts -= DOTD_BONUS
        pts += driver_pts

    # Pit stop bonus
    pit_time = random.gauss(con.pit_mean, 0.3)
    pts += _pit_stop_bonus(pit_time)

    return pts


def score_constructor_sprint(con: ConstructorProfile, driver_results: dict[str, DriverResult]) -> float:
    """Score constructor sprint weekend bonus (SQ tier + sprint race sum)."""
    d1, d2 = con.drivers
    r1 = driver_results[d1]
    r2 = driver_results[d2]

    pts = 0.0

    # Sprint qualifying tier bonus
    phase1 = get_quali_phase(r1.sprint_start_pos)
    phase2 = get_quali_phase(r2.sprint_start_pos)
    pts += _constructor_quali_bonus(phase1, phase2)

    # Both drivers' sprint points (sprint_points already computed by score_driver_sprint())
    for r in (r1, r2):
        pts += r.sprint_points

    return pts


def simulate_sprint_qualifying(drivers: list[DriverProfile],
                                driver_results: dict[str, DriverResult]) -> None:
    """Simulate sprint qualifying. Sets sprint_start_pos on each driver result."""
    sq_scores = [(random.gauss(d.quali_mean, d.variance), d) for d in drivers]
    sq_scores.sort(key=lambda x: x[0])
    for pos_idx, (_, d) in enumerate(sq_scores):
        driver_results[d.name].sprint_start_pos = pos_idx + 1


def simulate_sprint_race(drivers: list[DriverProfile],
                          driver_results: dict[str, DriverResult],
                          circuit_overtaking_index: int = 5) -> None:
    """Simulate sprint race. Sets sprint_race_pos and related fields."""
    dnf_drivers = set()
    sprint_race_scores = []

    for d in drivers:
        # Sprint DNFs are less frequent (shorter race)
        if random.random() < d.dnf_chance * 0.5:
            dnf_drivers.add(d.name)
            driver_results[d.name].sprint_dnf = True
        else:
            score = random.gauss(d.race_mean, d.variance)
            sprint_race_scores.append((score, d))

    sprint_race_scores.sort(key=lambda x: x[0])
    for pos_idx, (_, d) in enumerate(sprint_race_scores):
        driver_results[d.name].sprint_race_pos = pos_idx + 1

    # Positions delta and overtakes
    overtake_scale = circuit_overtaking_index / 5.0
    driver_map = {d.name: d for d in drivers}
    for name, r in driver_results.items():
        if r.sprint_dnf:
            continue
        delta = r.sprint_start_pos - r.sprint_race_pos
        r.sprint_positions_delta = delta
        if delta > 0:
            ot = max(0, round(random.gauss(
                delta * driver_map[name].overtake_factor * overtake_scale, 1.5)))
            r.sprint_overtakes = ot

    # Fastest lap: all finishers eligible (not just top 10)
    finishers = [r for r in driver_results.values() if not r.sprint_dnf]
    if finishers:
        weights = [max(1, 9 - r.sprint_race_pos) for r in finishers]
        random.choices(finishers, weights=weights, k=1)[0].sprint_fastest_lap = True


def simulate_weekend(drivers: list[DriverProfile], constructors: list[ConstructorProfile],
                     circuit_overtaking_index: int = 5,
                     sprint: bool = False) -> tuple[dict[str, float], dict[str, float], dict[str, DriverResult]]:
    """Run one simulated race weekend. Returns (driver_points, constructor_points, driver_results)."""

    # Initialize driver results
    driver_results: dict[str, DriverResult] = {
        d.name: DriverResult(name=d.name, team=d.team, price=d.price) for d in drivers
    }
    driver_map = {d.name: d for d in drivers}

    # --- Sprint sessions ---
    if sprint:
        simulate_sprint_qualifying(drivers, driver_results)
        simulate_sprint_race(drivers, driver_results, circuit_overtaking_index)

    # --- Main Qualifying ---
    quali_scores = [(random.gauss(d.quali_mean, d.variance), d) for d in drivers]
    quali_scores.sort(key=lambda x: x[0])
    for pos_idx, (_, d) in enumerate(quali_scores):
        driver_results[d.name].quali_pos = pos_idx + 1

    # --- Main Race ---
    dnf_drivers = set()
    race_scores = []
    for d in drivers:
        if random.random() < d.dnf_chance:
            dnf_drivers.add(d.name)
            driver_results[d.name].dnf = True
        else:
            race_scores.append((random.gauss(d.race_mean, d.variance), d))

    race_scores.sort(key=lambda x: x[0])
    for pos_idx, (_, d) in enumerate(race_scores):
        driver_results[d.name].race_pos = pos_idx + 1

    # --- Positions delta and overtakes ---
    overtake_scale = circuit_overtaking_index / 5.0
    for name, r in driver_results.items():
        if r.dnf:
            continue
        delta = r.quali_pos - r.race_pos
        r.positions_delta = delta
        if delta > 0:
            ot = max(0, round(random.gauss(
                delta * driver_map[name].overtake_factor * overtake_scale, 1.5)))
            r.overtakes = ot

    # --- Fastest lap: weighted random among top-10 finishers ---
    top10 = [r for r in driver_results.values() if not r.dnf and r.race_pos <= 10]
    if top10:
        weights = [max(1, 11 - r.race_pos) for r in top10]
        random.choices(top10, weights=weights, k=1)[0].fastest_lap = True

    # --- DotD: fan-voted, weighted by popularity + positions gained + podium ---
    all_finishers = [r for r in driver_results.values() if not r.dnf]
    if all_finishers:
        dotd_weights = []
        for r in all_finishers:
            popularity = driver_map[r.name].dotd_weight
            positions_narrative = (max(1, r.positions_delta * 2) if r.positions_delta >= 5
                                   else max(0.5, r.positions_delta * 0.5))
            w = popularity * positions_narrative
            if r.race_pos == 1:
                w += 5 * popularity
            elif r.race_pos <= 3:
                w += 2 * popularity
            dotd_weights.append(max(0.1, w))
        random.choices(all_finishers, weights=dotd_weights, k=1)[0].dotd = True

    # --- Score drivers ---
    driver_points = {}
    for name, r in driver_results.items():
        pts = score_driver(r)
        if sprint:
            pts += score_driver_sprint(r)
            r.points = pts  # update total
        driver_points[name] = pts

    # --- Score constructors (uses r.points set above) ---
    constructor_points = {}
    for con in constructors:
        pts = score_constructor(con, driver_results)
        if sprint:
            pts += score_constructor_sprint(con, driver_results)
        constructor_points[con.name] = pts

    return driver_points, constructor_points, driver_results


def load_config(path: str) -> tuple[list[DriverProfile], list[ConstructorProfile], dict | None, int, bool]:
    """Load race config from JSON. Returns (drivers, constructors, teams, overtaking_index, sprint)."""
    with open(path) as f:
        cfg = json.load(f)

    drivers = []
    for d in cfg["drivers"]:
        drivers.append(DriverProfile(
            name=d["name"],
            team=d["team"],
            price=d["price"],
            quali_mean=d["quali_mean"],
            race_mean=d["race_mean"],
            variance=d["variance"],
            dnf_chance=d["dnf_chance"],
            overtake_factor=d.get("overtake_factor", 1.0),
            dotd_weight=d.get("dotd_weight", 1.0),
        ))

    constructors = []
    con_map: dict[str, ConstructorProfile] = {}
    for c in cfg["constructors"]:
        con = ConstructorProfile(name=c["name"], price=c["price"], pit_mean=c["pit_mean"])
        constructors.append(con)
        con_map[c["name"]] = con

    # Wire up drivers to constructors
    for d in drivers:
        if d.team in con_map:
            con_map[d.team].drivers.append(d.name)

    teams = None
    if "teams" in cfg:
        teams = {}
        for t in cfg["teams"]:
            teams[t["name"]] = {
                "drivers": t["drivers"],
                "constructors": t["constructors"],
                "captain": t.get("captain", t["drivers"][0]),
            }

    overtaking_index = cfg.get("overtaking_index", 5)
    sprint = cfg.get("sprint", False)

    return drivers, constructors, teams, overtaking_index, sprint


def run_simulation(drivers: list[DriverProfile], constructors: list[ConstructorProfile],
                   num_sims: int, teams: dict | None = None,
                   circuit_overtaking_index: int = 5,
                   sprint: bool = False) -> tuple[
    dict[str, list[float]],
    dict[str, list[float]],
    dict[str, list[float]],
    dict[str, DriverProfile],
]:
    """Run Monte Carlo simulation and return accumulated results."""

    driver_totals: dict[str, list[float]] = {d.name: [] for d in drivers}
    con_totals: dict[str, list[float]] = {c.name: [] for c in constructors}
    team_totals: dict[str, list[float]] = {t: [] for t in (teams or {})}

    driver_map = {d.name: d for d in drivers}

    for _ in range(num_sims):
        dp, cp, dr = simulate_weekend(drivers, constructors, circuit_overtaking_index, sprint=sprint)

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
                  driver_map, num_sims, sprint=False,
                  show_drivers=True, show_constructors=True, show_teams=True):
    sprint_label = " — Sprint Weekend" if sprint else ""
    print(f"\n=== F1 Fantasy Monte Carlo ({num_sims} sims){sprint_label} ===")

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


def parse_args():
    parser = argparse.ArgumentParser(description="F1 Fantasy Monte Carlo Simulator")
    parser.add_argument("--config", type=str, required=True,
                        help="Path to race config JSON file")
    parser.add_argument("--sims", type=int, default=1000,
                        help="Number of simulations (default: 1000)")
    parser.add_argument("--seed", type=int, help="Random seed for reproducibility")
    parser.add_argument("--overtaking-index", type=int, default=None,
                        help="Override circuit overtaking index 1-10 (1=Monaco, 10=Monza, 5=neutral)")
    parser.add_argument("--drivers-only", action="store_true", help="Only show driver rankings")
    parser.add_argument("--constructors-only", action="store_true", help="Only show constructor rankings")
    # Custom team override
    parser.add_argument("--team", type=str, help="Comma-separated driver names for ad-hoc team")
    parser.add_argument("--constructors", type=str, help="Comma-separated constructor names for ad-hoc team")
    parser.add_argument("--captain", type=str, help="Captain (2x) driver for ad-hoc team")
    return parser.parse_args()


def main():
    args: Any = parse_args()

    if args.seed is not None:
        random.seed(args.seed)

    drivers, constructors, teams, overtaking_index, sprint = load_config(args.config)

    if args.overtaking_index is not None:
        overtaking_index = args.overtaking_index

    teams = teams or {}

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
        drivers, constructors, args.sims,
        teams=teams if show_teams else None,
        circuit_overtaking_index=overtaking_index,
        sprint=sprint,
    )

    print_results(
        drivers, constructors, driver_totals, con_totals, team_totals,
        driver_map, args.sims, sprint=sprint,
        show_drivers=show_drivers,
        show_constructors=show_constructors,
        show_teams=show_teams,
    )


if __name__ == "__main__":
    main()
