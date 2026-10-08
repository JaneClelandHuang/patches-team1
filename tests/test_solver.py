import matplotlib

matplotlib.use("Agg")  # headless: no window needed

from types import SimpleNamespace  # noqa: E402

from patches.puzzle import load_puzzle  # noqa: E402
from patches.rules import Rect  # noqa: E402
from patches.solver import solve  # noqa: E402
from patches.ui import PatchesApp  # noqa: E402

from test_rules import PROBLEM1_SOLUTION, SAMPLE_SOLUTION  # noqa: E402


def press(app, key):
    app.on_key(SimpleNamespace(key=key))


def test_solve_problem1():
    assert solve(load_puzzle("puzzles/problem1.json")) == PROBLEM1_SOLUTION


def test_solve_sample():
    assert solve(load_puzzle("puzzles/sample.json")) == SAMPLE_SOLUTION


def test_hint_on_empty_board_places_one_solution_region():
    app = PatchesApp(load_puzzle("puzzles/problem1.json"))
    press(app, "h")
    assert app.board.regions == {"drone_1": PROBLEM1_SOLUTION["drone_1"]}
    assert "drone_1" in app.message


def test_hint_replaces_wrong_region_and_skips_correct_ones():
    app = PatchesApp(load_puzzle("puzzles/problem1.json"))
    app.board.place(PROBLEM1_SOLUTION["drone_1"])
    app.board.place(Rect(0, 3, 1, 2))  # wrong drone_2
    press(app, "h")
    assert app.board.regions["drone_2"] == PROBLEM1_SOLUTION["drone_2"]
    assert len(app.board.regions) == 2


def test_hint_when_solved_does_nothing():
    app = PatchesApp(load_puzzle("puzzles/problem1.json"))
    for rect in PROBLEM1_SOLUTION.values():
        app.board.place(rect)
    press(app, "h")
    assert app.board.regions == PROBLEM1_SOLUTION
    assert app.message == "Already solved."


def test_undo_reverts_a_hint():
    app = PatchesApp(load_puzzle("puzzles/problem1.json"))
    press(app, "h")
    press(app, "u")
    assert app.board.regions == {}
