import os
import sys
import unittest
from unittest.mock import MagicMock

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)

if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

_pygame_mock = MagicMock()

for _submodule in [
    "pygame",
    "pygame.font",
    "pygame.draw",
    "pygame.display",
    "pygame.event",
    "pygame.time",
    "pygame.transform",
]:
    sys.modules[_submodule] = _pygame_mock


from puzzleChallenge import dijkstra, gridPaths

# Dijkstra test
class TestDijkstra(unittest.TestCase):
    def test_simple_path_no_obstacles(self):
        path, visited = dijkstra(3, 3, (0, 0), (2, 2), set())

        self.assertEqual(path[0], (0, 0))
        self.assertEqual(path[-1], (2, 2))
        self.assertGreater(len(visited), 0)

    def test_path_length_no_obstacles(self):
        path, _ = dijkstra(3, 3, (0, 0), (2, 2), set())

        # Shortest path on a clear 3x3 grid is Manhattan distance + 1.
        self.assertEqual(len(path), 5)

    def test_path_avoids_obstacles(self):
        obstacles = {(0, 1), (1, 1)}
        path, _ = dijkstra(3, 3, (0, 0), (0, 2), obstacles)

        for cell in path:
            self.assertNotIn(cell, obstacles)

    def test_no_path_when_blocked(self):
        obstacles = {(0, 1), (1, 0), (1, 1)}
        path, _ = dijkstra(2, 2, (0, 0), (1, 1), obstacles)

        self.assertEqual(path, [])

    def test_start_equals_end(self):
        path, _ = dijkstra(3, 3, (1, 1), (1, 1), set())

        self.assertEqual(path, [(1, 1)])

    def test_visit_order_starts_at_start(self):
        _, visit_order = dijkstra(3, 3, (0, 0), (2, 2), set())

        self.assertEqual(visit_order[0], (0, 0))

    def test_path_is_contiguous(self):
        path, _ = dijkstra(5, 5, (0, 0), (4, 4), set())

        for index in range(len(path) - 1):
            row_1, col_1 = path[index]
            row_2, col_2 = path[index + 1]

            manhattan_distance = abs(row_2 - row_1) + abs(col_2 - col_1)

            self.assertEqual(
                manhattan_distance,
                1,
                f"Non-adjacent cells found at path index {index}"
            )

    def test_path_includes_start_and_end_only_once(self):
        path, _ = dijkstra(4, 4, (0, 0), (3, 3), set())

        self.assertEqual(path.count((0, 0)), 1)
        self.assertEqual(path.count((3, 3)), 1)

# Dynamic Programming test
class TestGridPaths(unittest.TestCase):
    def test_2x2_no_obstacles(self):
        dp = gridPaths(2, 2, set())

        self.assertEqual(dp[1][1], 2)

    def test_3x3_no_obstacles(self):
        dp = gridPaths(3, 3, set())

        self.assertEqual(dp[2][2], 6)

    def test_obstacle_reduces_count(self):
        dp_clean = gridPaths(3, 3, set())
        dp_blocked = gridPaths(3, 3, {(1, 1)})

        self.assertLess(dp_blocked[2][2], dp_clean[2][2])

    def test_obstacle_at_start_zero_paths(self):
        dp = gridPaths(3, 3, {(0, 0)})

        self.assertEqual(dp[2][2], 0)

    def test_obstacle_at_end_zero_paths(self):
        dp = gridPaths(3, 3, {(2, 2)})

        self.assertEqual(dp[2][2], 0)

    def test_obstacle_cell_is_zero(self):
        dp = gridPaths(3, 3, {(1, 1)})

        self.assertEqual(dp[1][1], 0)

    def test_single_cell_grid(self):
        dp = gridPaths(1, 1, set())

        self.assertEqual(dp[0][0], 1)

    def test_single_cell_grid_blocked(self):
        dp = gridPaths(1, 1, {(0, 0)})

        self.assertEqual(dp[0][0], 0)

    def test_top_row_all_ones_when_no_obstacles(self):
        dp = gridPaths(3, 5, set())

        for col in range(5):
            self.assertEqual(dp[0][col], 1)

    def test_left_column_all_ones_when_no_obstacles(self):
        dp = gridPaths(5, 3, set())

        for row in range(5):
            self.assertEqual(dp[row][0], 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)

