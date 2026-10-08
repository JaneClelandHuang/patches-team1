from types import SimpleNamespace

import matplotlib

matplotlib.use("Agg")  # headless: no window needed

from matplotlib.patches import Circle  # noqa: E402

from patches.puzzle import load_puzzle  # noqa: E402
from patches.ui import PatchesApp, format_time  # noqa: E402

from test_rules import PROBLEM1_SOLUTION  # noqa: E402


def make_app():
    return PatchesApp(load_puzzle("puzzles/problem1.json"))


def test_clues_shown_while_unsolved():
    app = make_app()
    assert len(app.ax.texts) == len(app.puzzle.drones)


def test_clues_become_drones_when_solved():
    app = make_app()
    for rect in PROBLEM1_SOLUTION.values():
        app.board.place(rect)
    app.redraw()
    assert len(app.ax.texts) == 0
    circles = [p for p in app.ax.patches if isinstance(p, Circle)]
    assert len(circles) == 5 * len(app.puzzle.drones)


def test_clues_return_after_unsolving():
    app = make_app()
    for rect in PROBLEM1_SOLUTION.values():
        app.board.place(rect)
    app.board.remove_at(0, 0)
    app.redraw()
    assert len(app.ax.texts) == len(app.puzzle.drones)


# ---- move counter and timer ------------------------------------------------

def mouse(app, row, col, button=1):
    """A fake mouse event over cell (row, col)."""
    return SimpleNamespace(inaxes=app.ax, xdata=col + 0.5, ydata=row + 0.5, button=button)


def drag(app, start, end):
    app.on_press(mouse(app, *start))
    app.on_release(mouse(app, *end))


def test_successful_placement_counts_as_a_move():
    app = make_app()
    assert app.moves == 0
    drag(app, (0, 0), (1, 2))  # contains only drone_1
    assert app.moves == 1
    assert app.start_time is not None


def test_rejected_placement_is_not_a_move():
    app = make_app()
    drag(app, (0, 0), (0, 5))  # contains drone_1 and drone_2
    drag(app, (1, 1), (1, 1))  # contains no drone
    assert app.moves == 0
    assert app.start_time is None


def test_right_click_on_empty_cell_is_not_a_move():
    app = make_app()
    app.on_press(mouse(app, 1, 1, button=3))
    assert app.moves == 0


def test_right_click_removing_a_region_is_a_move():
    app = make_app()
    drag(app, (0, 0), (1, 2))
    app.on_press(mouse(app, 0, 0, button=3))
    assert app.moves == 2


def test_reset_clears_moves_and_timer():
    app = make_app()
    drag(app, (0, 0), (1, 2))
    app.on_key(SimpleNamespace(key="r"))
    assert app.moves == 0
    assert app.start_time is None
    assert app.elapsed(now=1000) == 0


def test_elapsed_uses_given_time():
    app = make_app()
    app.start_time = 100
    assert app.elapsed(now=165) == 65


def test_elapsed_stops_when_solved():
    app = make_app()
    app.start_time, app.end_time = 100, 142
    assert app.elapsed(now=500) == 42


def test_format_time():
    assert format_time(65) == "1:05"
    assert format_time(0) == "0:00"
    assert format_time(102.9) == "1:42"
