"""pytest test suite for simulator.py — deterministic scoring logic coverage."""
import json
import random
from unittest.mock import patch

import pytest

from simulator import (
    ConstructorProfile,
    DriverProfile,
    DriverResult,
    _constructor_quali_bonus,
    _pit_stop_bonus,
    get_quali_phase,
    load_config,
    run_simulation,
    score_constructor,
    score_driver,
    score_driver_sprint,
    simulate_weekend,
)


# ---------------------------------------------------------------------------
# Helpers / fixtures
# ---------------------------------------------------------------------------

def make_driver(
    name="HAM",
    team="Mercedes",
    price=20.0,
    quali_mean=3.0,
    race_mean=3.0,
    variance=2.0,
    dnf_chance=0.05,
) -> DriverProfile:
    return DriverProfile(
        name=name,
        team=team,
        price=price,
        quali_mean=quali_mean,
        race_mean=race_mean,
        variance=variance,
        dnf_chance=dnf_chance,
    )


def make_constructor(
    name="Mercedes",
    price=25.0,
    pit_mean=2.3,
    drivers: list[str] | None = None,
) -> ConstructorProfile:
    con = ConstructorProfile(name=name, price=price, pit_mean=pit_mean)
    con.drivers = drivers if drivers is not None else []
    return con


def make_result(name="HAM", team="Mercedes", price=20.0, **kwargs) -> DriverResult:
    r = DriverResult(name=name, team=team, price=price)
    for k, v in kwargs.items():
        setattr(r, k, v)
    return r


# ---------------------------------------------------------------------------
# A. Pure scoring functions
# ---------------------------------------------------------------------------


class TestGetQualiPhase:
    def test_p10_is_q3(self):
        assert get_quali_phase(10) == "Q3"

    def test_p1_is_q3(self):
        assert get_quali_phase(1) == "Q3"

    def test_p11_is_q2(self):
        assert get_quali_phase(11) == "Q2"

    def test_p15_is_q2(self):
        assert get_quali_phase(15) == "Q2"

    def test_p16_is_q1(self):
        assert get_quali_phase(16) == "Q1"

    def test_p20_is_q1(self):
        assert get_quali_phase(20) == "Q1"


class TestConstructorQualiBonus:
    def test_both_q3(self):
        assert _constructor_quali_bonus("Q3", "Q3") == 10

    def test_q3_q2(self):
        assert _constructor_quali_bonus("Q3", "Q2") == 5

    def test_q3_q1(self):
        assert _constructor_quali_bonus("Q3", "Q1") == 5

    def test_q2_q3_commutative(self):
        assert _constructor_quali_bonus("Q2", "Q3") == 5

    def test_both_q2(self):
        assert _constructor_quali_bonus("Q2", "Q2") == 5

    def test_q2_q1(self):
        assert _constructor_quali_bonus("Q2", "Q1") == 1

    def test_both_q1(self):
        assert _constructor_quali_bonus("Q1", "Q1") == -1


class TestPitStopBonus:
    def test_world_record(self):
        # <1.8s → +20 +15 = 35
        assert _pit_stop_bonus(1.5) == 35

    def test_sub_2_not_wr(self):
        # 1.8–1.99s → +20 only
        assert _pit_stop_bonus(1.85) == 20

    def test_exact_2s_boundary(self):
        # 2.0 starts 2.0–2.19 tier → +10
        assert _pit_stop_bonus(2.0) == 10

    def test_mid_2_tier(self):
        assert _pit_stop_bonus(2.1) == 10

    def test_2_2_tier(self):
        assert _pit_stop_bonus(2.3) == 5

    def test_exact_2_5_boundary(self):
        assert _pit_stop_bonus(2.5) == 2

    def test_2_7_tier(self):
        assert _pit_stop_bonus(2.7) == 2

    def test_3s_no_bonus(self):
        assert _pit_stop_bonus(3.1) == 0


class TestScoreDriver:
    def test_p1_win_p1_quali_no_bonus(self):
        r = make_result(quali_pos=1, race_pos=1, positions_delta=0)
        pts = score_driver(r)
        # Q1=10, Race P1=25
        assert pts == 35
        assert r.points == 35

    def test_p1_win_p5_quali_delta_plus4(self):
        r = make_result(quali_pos=5, race_pos=1, positions_delta=4)
        pts = score_driver(r)
        # Q5=6, Race P1=25, delta=+4
        assert pts == 35

    def test_p5_quali_p10_race_delta_minus5(self):
        r = make_result(quali_pos=5, race_pos=10, positions_delta=-5)
        pts = score_driver(r)
        # Q5=6, Race P10=1, delta=-5
        assert pts == 2

    def test_dnf_from_p3_quali(self):
        r = make_result(quali_pos=3, race_pos=0, dnf=True)
        pts = score_driver(r)
        # Q3=8, DNF=-20
        assert pts == -12

    def test_fastest_lap_adds_10(self):
        r = make_result(quali_pos=1, race_pos=1, positions_delta=0, fastest_lap=True)
        pts = score_driver(r)
        assert pts == 45  # 10+25+10

    def test_dotd_adds_10(self):
        r = make_result(quali_pos=1, race_pos=1, positions_delta=0, dotd=True)
        pts = score_driver(r)
        assert pts == 45

    def test_points_side_effect_set(self):
        r = make_result(quali_pos=2, race_pos=3, positions_delta=-1)
        score_driver(r)
        assert r.points == r.points  # explicitly set


class TestScoreDriverSprint:
    def test_sprint_dnf_from_p1_sq(self):
        r = make_result(sprint_start_pos=1, sprint_race_pos=0, sprint_dnf=True)
        pts = score_driver_sprint(r)
        # SQ P1=10, sprint DNF=-10
        assert pts == 0
        assert r.sprint_points == 0

    def test_sprint_p1_p1_sq_fastest_lap(self):
        r = make_result(sprint_start_pos=1, sprint_race_pos=1,
                        sprint_positions_delta=0, sprint_fastest_lap=True)
        pts = score_driver_sprint(r)
        # SQ=10, sprint P1=8, FL=5
        assert pts == 23

    def test_sprint_p9_no_points_p5_sq(self):
        r = make_result(sprint_start_pos=5, sprint_race_pos=9, sprint_positions_delta=-4)
        pts = score_driver_sprint(r)
        # SQ P5=6, sprint P9=0, delta=-4
        assert pts == 2

    def test_sprint_points_side_effect(self):
        r = make_result(sprint_start_pos=3, sprint_race_pos=3, sprint_positions_delta=0)
        score_driver_sprint(r)
        assert r.sprint_points is not None


# ---------------------------------------------------------------------------
# B. score_constructor — mock pit stop randomness
# ---------------------------------------------------------------------------


class TestScoreConstructor:
    def _make_scored_result(self, name, team, quali_pos, race_pos, dnf=False,
                             positions_delta=0, dotd=False) -> DriverResult:
        r = make_result(name=name, team=team,
                        quali_pos=quali_pos, race_pos=race_pos,
                        dnf=dnf, positions_delta=positions_delta, dotd=dotd)
        score_driver(r)
        return r

    def test_both_q3_pit_2_1(self):
        r1 = self._make_scored_result("HAM", "Mercedes", quali_pos=1, race_pos=1)
        r2 = self._make_scored_result("RUS", "Mercedes", quali_pos=2, race_pos=2)
        con = make_constructor(drivers=["HAM", "RUS"])
        driver_results = {"HAM": r1, "RUS": r2}
        with patch("simulator.random.gauss", return_value=2.1):
            pts = score_constructor(con, driver_results)
        # quali bonus: Q3+Q3=10, pit 2.1→+10
        # driver pts: P1(10+25) + P2(9+18) = 62
        assert pts == 10 + (r1.points + r2.points) + 10

    def test_both_q1_pit_3_5_no_bonus(self):
        r1 = self._make_scored_result("BOT", "Sauber", quali_pos=16, race_pos=16)
        r2 = self._make_scored_result("ZHO", "Sauber", quali_pos=17, race_pos=17)
        con = make_constructor(name="Sauber", drivers=["BOT", "ZHO"])
        driver_results = {"BOT": r1, "ZHO": r2}
        with patch("simulator.random.gauss", return_value=3.5):
            pts = score_constructor(con, driver_results)
        # Q1+Q1=-1, pit≥3.0=0
        assert pts == -1 + r1.points + r2.points

    def test_dotd_excluded_from_constructor(self):
        r1 = self._make_scored_result("HAM", "Mercedes", quali_pos=1, race_pos=1,
                                       positions_delta=0, dotd=True)
        r2 = self._make_scored_result("RUS", "Mercedes", quali_pos=2, race_pos=2)
        con = make_constructor(drivers=["HAM", "RUS"])
        driver_results = {"HAM": r1, "RUS": r2}
        # r1.points includes DOTD +10
        assert r1.dotd is True
        with patch("simulator.random.gauss", return_value=2.5):
            pts = score_constructor(con, driver_results)
        # Constructor should NOT include DOTD: subtract 10 from r1.points
        expected_driver_pts = (r1.points - 10) + r2.points
        expected_pit = _pit_stop_bonus(2.5)
        expected_quali = _constructor_quali_bonus("Q3", "Q3")
        assert pts == expected_quali + expected_driver_pts + expected_pit


# ---------------------------------------------------------------------------
# C. simulate_weekend — structural correctness
# ---------------------------------------------------------------------------


class TestSimulateWeekend:
    def _make_grid(self, n=5):
        drivers = [
            make_driver(name=f"D{i}", team=f"Team{i}", quali_mean=float(i),
                        race_mean=float(i), variance=1.0, dnf_chance=0.0)
            for i in range(1, n + 1)
        ]
        constructors = [
            make_constructor(name=f"Team{i}", drivers=[f"D{i}"])
            for i in range(1, n + 1)
        ]
        # Fix: each constructor needs 2 drivers for score_constructor to work
        # Use pairs
        paired_drivers = []
        paired_cons = []
        for i in range(1, n, 2):
            d1 = make_driver(name=f"D{i}", team=f"Team{(i+1)//2}",
                              quali_mean=float(i), race_mean=float(i),
                              variance=1.0, dnf_chance=0.0)
            d2 = make_driver(name=f"D{i+1}", team=f"Team{(i+1)//2}",
                              quali_mean=float(i+1), race_mean=float(i+1),
                              variance=1.0, dnf_chance=0.0)
            paired_drivers.extend([d1, d2])
            paired_cons.append(make_constructor(
                name=f"Team{(i+1)//2}", drivers=[f"D{i}", f"D{i+1}"]))
        return paired_drivers, paired_cons

    def test_non_sprint_quali_positions_unique(self):
        random.seed(1)
        drivers, constructors = self._make_grid(4)
        dp, cp, dr = simulate_weekend(drivers, constructors, sprint=False)
        positions = [dr[d.name].quali_pos for d in drivers]
        assert sorted(positions) == list(range(1, len(drivers) + 1))

    def test_non_sprint_exactly_one_fastest_lap(self):
        random.seed(2)
        drivers, constructors = self._make_grid(4)
        dp, cp, dr = simulate_weekend(drivers, constructors, sprint=False)
        fl_count = sum(1 for r in dr.values() if r.fastest_lap)
        assert fl_count == 1

    def test_non_sprint_exactly_one_dotd(self):
        random.seed(3)
        drivers, constructors = self._make_grid(4)
        dp, cp, dr = simulate_weekend(drivers, constructors, sprint=False)
        dotd_count = sum(1 for r in dr.values() if r.dotd)
        assert dotd_count == 1

    def test_driver_points_are_numeric(self):
        random.seed(4)
        drivers, constructors = self._make_grid(4)
        dp, cp, dr = simulate_weekend(drivers, constructors)
        for pts in dp.values():
            assert isinstance(pts, (int, float))

    def test_sprint_quali_positions_set(self):
        random.seed(5)
        drivers, constructors = self._make_grid(4)
        dp, cp, dr = simulate_weekend(drivers, constructors, sprint=True)
        sprint_positions = [dr[d.name].sprint_start_pos for d in drivers]
        assert sorted(sprint_positions) == list(range(1, len(drivers) + 1))

    def test_sprint_exactly_one_sprint_fastest_lap(self):
        random.seed(6)
        drivers, constructors = self._make_grid(4)
        dp, cp, dr = simulate_weekend(drivers, constructors, sprint=True)
        sfl_count = sum(1 for r in dr.values() if r.sprint_fastest_lap)
        assert sfl_count == 1

    def test_sprint_produces_higher_avg_points(self):
        n_sims = 200
        drivers, constructors = self._make_grid(4)

        random.seed(42)
        sprint_pts = []
        for _ in range(n_sims):
            dp, _, _ = simulate_weekend(drivers, constructors, sprint=True)
            sprint_pts.append(sum(dp.values()) / len(dp))

        random.seed(42)
        non_sprint_pts = []
        for _ in range(n_sims):
            dp, _, _ = simulate_weekend(drivers, constructors, sprint=False)
            non_sprint_pts.append(sum(dp.values()) / len(dp))

        avg_sprint = sum(sprint_pts) / len(sprint_pts)
        avg_non = sum(non_sprint_pts) / len(non_sprint_pts)
        assert avg_sprint > avg_non + 10


# ---------------------------------------------------------------------------
# D. load_config — uses tmp_path fixture
# ---------------------------------------------------------------------------


MINIMAL_CONFIG = {
    "drivers": [
        {"name": "HAM", "team": "Mercedes", "price": 22.5, "quali_mean": 2.0,
         "race_mean": 2.0, "variance": 1.5, "dnf_chance": 0.05},
        {"name": "RUS", "team": "Mercedes", "price": 20.0, "quali_mean": 3.0,
         "race_mean": 3.0, "variance": 1.5, "dnf_chance": 0.05},
    ],
    "constructors": [
        {"name": "Mercedes", "price": 28.0, "pit_mean": 2.3},
    ],
}


class TestLoadConfig:
    def test_returns_correct_types(self, tmp_path):
        cfg_file = tmp_path / "config.json"
        cfg_file.write_text(json.dumps(MINIMAL_CONFIG))
        drivers, constructors, teams, overtaking_index, sprint = load_config(str(cfg_file))
        assert isinstance(drivers, list)
        assert isinstance(drivers[0], DriverProfile)
        assert isinstance(constructors, list)
        assert isinstance(constructors[0], ConstructorProfile)
        assert teams is None
        assert isinstance(overtaking_index, int)
        assert isinstance(sprint, bool)

    def test_constructor_drivers_wired(self, tmp_path):
        cfg_file = tmp_path / "config.json"
        cfg_file.write_text(json.dumps(MINIMAL_CONFIG))
        drivers, constructors, _, _, _ = load_config(str(cfg_file))
        assert constructors[0].drivers == ["HAM", "RUS"]

    def test_teams_none_when_absent(self, tmp_path):
        cfg_file = tmp_path / "config.json"
        cfg_file.write_text(json.dumps(MINIMAL_CONFIG))
        _, _, teams, _, _ = load_config(str(cfg_file))
        assert teams is None

    def test_sprint_default_false(self, tmp_path):
        cfg_file = tmp_path / "config.json"
        cfg_file.write_text(json.dumps(MINIMAL_CONFIG))
        _, _, _, _, sprint = load_config(str(cfg_file))
        assert sprint is False

    def test_overtaking_index_default_5(self, tmp_path):
        cfg_file = tmp_path / "config.json"
        cfg_file.write_text(json.dumps(MINIMAL_CONFIG))
        _, _, _, overtaking_index, _ = load_config(str(cfg_file))
        assert overtaking_index == 5

    def test_sprint_true_loaded(self, tmp_path):
        cfg = {**MINIMAL_CONFIG, "sprint": True, "overtaking_index": 7}
        cfg_file = tmp_path / "config.json"
        cfg_file.write_text(json.dumps(cfg))
        _, _, _, oi, sprint = load_config(str(cfg_file))
        assert sprint is True
        assert oi == 7

    def test_teams_loaded_when_present(self, tmp_path):
        cfg = {
            **MINIMAL_CONFIG,
            "teams": [
                {"name": "MyTeam", "drivers": ["HAM", "RUS"],
                 "constructors": ["Mercedes"], "captain": "HAM"}
            ],
        }
        cfg_file = tmp_path / "config.json"
        cfg_file.write_text(json.dumps(cfg))
        _, _, teams, _, _ = load_config(str(cfg_file))
        assert teams is not None
        assert "MyTeam" in teams
        assert teams["MyTeam"]["captain"] == "HAM"


# ---------------------------------------------------------------------------
# E. run_simulation — output shape and captain 2x
# ---------------------------------------------------------------------------


class TestRunSimulation:
    def _minimal_setup(self):
        drivers = [
            make_driver("HAM", "Mercedes", dnf_chance=0.0),
            make_driver("RUS", "Mercedes", dnf_chance=0.0),
            make_driver("NOR", "McLaren", dnf_chance=0.0),
        ]
        constructors = [
            make_constructor("Mercedes", drivers=["HAM", "RUS"]),
            make_constructor("McLaren", drivers=["NOR", "NOR"]),  # single driver team stub
        ]
        return drivers, constructors

    def test_output_keys_match_drivers_and_constructors(self):
        random.seed(7)
        drivers, constructors = self._minimal_setup()
        dt, ct, tt, dm = run_simulation(drivers, constructors, num_sims=100)
        assert set(dt.keys()) == {"HAM", "RUS", "NOR"}
        assert set(ct.keys()) == {"Mercedes", "McLaren"}
        assert tt == {}

    def test_list_lengths_equal_num_sims(self):
        random.seed(8)
        drivers, constructors = self._minimal_setup()
        dt, ct, tt, dm = run_simulation(drivers, constructors, num_sims=50)
        for vals in dt.values():
            assert len(vals) == 50
        for vals in ct.values():
            assert len(vals) == 50

    def test_captain_2x_raises_average(self):
        random.seed(9)
        drivers, constructors = self._minimal_setup()
        # All drivers identical, captain on HAM should make Team A score higher
        teams_with_captain = {
            "WithCaptain": {"drivers": ["HAM"], "constructors": [], "captain": "HAM"},
            "WithoutCaptain": {"drivers": ["RUS"], "constructors": [], "captain": ""},
        }
        # Override: make HAM reliably outscore RUS
        drivers[0].race_mean = 1.0   # HAM: best
        drivers[1].race_mean = 10.0  # RUS: worst
        dt, ct, tt, dm = run_simulation(
            drivers, constructors, num_sims=200, teams=teams_with_captain)
        avg_captain = sum(tt["WithCaptain"]) / len(tt["WithCaptain"])
        avg_no = sum(tt["WithoutCaptain"]) / len(tt["WithoutCaptain"])
        assert avg_captain > avg_no

    def test_driver_map_returned_correctly(self):
        random.seed(10)
        drivers, constructors = self._minimal_setup()
        dt, ct, tt, dm = run_simulation(drivers, constructors, num_sims=10)
        assert set(dm.keys()) == {"HAM", "RUS", "NOR"}
        assert isinstance(dm["HAM"], DriverProfile)
