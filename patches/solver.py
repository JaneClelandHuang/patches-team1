"""Backtracking solver for Patches. No drawing code here."""

from .rules import Rect, is_solved, region_errors


def candidates(puzzle, drone):
    """Every rectangle on the grid that is a valid region for `drone`."""
    n = puzzle.grid_size
    return [rect
            for top in range(n)
            for left in range(n)
            for height in range(1, n - top + 1)
            for width in range(1, n - left + 1)
            if not region_errors(puzzle, drone, rect := Rect(top, left, height, width))]


def solve(puzzle):
    """Return the solution as {drone_id: Rect}, or None if there is none."""
    options = [candidates(puzzle, d) for d in puzzle.drones]
    chosen = {}

    def search(i, used):
        if i == len(puzzle.drones):
            return is_solved(puzzle, chosen)
        drone = puzzle.drones[i]
        for rect in options[i]:
            cells = rect.cells()
            if cells & used:
                continue
            chosen[drone.id] = rect
            if search(i + 1, used | cells):
                return True
            del chosen[drone.id]
        return False

    return dict(chosen) if search(0, set()) else None
