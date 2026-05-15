import os
import sys
import timeit
import random
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


from sortingAlgorithmVisualiser import bubblesort, selectionsort, mergesort
from puzzleChallenge import dijkstra, gridPaths

class TestBenchmarks(unittest.TestCase):

    SORT_STEP_SIZES = [25, 50, 100]
    MERGE_SORT_SIZES = [100, 500, 1000]
    REPEAT = 3

    def makeData(self, size):
        return random.sample(range(size * 10), size)

    def test_benchmark_bubble_sort_steps(self):
        print("\n--- Bubble sort visualisation-step benchmarks ---")

        elapsed = 0

        for size in self.SORT_STEP_SIZES:
            data = self.makeData(size)

            elapsed = timeit.timeit(
                lambda: bubblesort(data[:]),
                number=self.REPEAT
            )

            average_ms = (elapsed / self.REPEAT) * 1000

            print(f"n={size:>4} | average={average_ms:.2f} ms")

        self.assertLess(elapsed, 10.0)

    def test_benchmark_selection_sort_steps(self):
        print("\n--- Selection sort visualisation-step benchmarks ---")

        elapsed = 0

        for size in self.SORT_STEP_SIZES:
            data = self.makeData(size)

            elapsed = timeit.timeit(
                lambda: selectionsort(data[:]),
                number=self.REPEAT
            )

            average_ms = (elapsed / self.REPEAT) * 1000

            print(f"n={size:>4} | average={average_ms:.2f} ms")

        self.assertLess(elapsed, 10.0)

    def test_benchmark_merge_sort(self):
        print("\n--- Merge sort benchmarks ---")

        elapsed = 0

        for size in self.MERGE_SORT_SIZES:
            data = self.makeData(size)

            elapsed = timeit.timeit(
                lambda: mergesort(data[:]),
                number=self.REPEAT
            )

            average_ms = (elapsed / self.REPEAT) * 1000

            print(f"n={size:>4} | average={average_ms:.2f} ms")

        self.assertLess(elapsed, 5.0)

    def test_sort_comparison_summary(self):
        print("\n--- Sort comparison summary ---")

        size = 100
        data = self.makeData(size)

        bubble_time = timeit.timeit(
            lambda: bubblesort(data[:]),
            number=self.REPEAT
        )

        selection_time = timeit.timeit(
            lambda: selectionsort(data[:]),
            number=self.REPEAT
        )

        merge_time = timeit.timeit(
            lambda: mergesort(data[:]),
            number=self.REPEAT
        )

        print(f"Bubble sort visual steps    : {bubble_time:.4f}s")
        print(f"Selection sort visual steps : {selection_time:.4f}s")
        print(f"Merge sort                  : {merge_time:.4f}s")

        self.assertLess(merge_time, bubble_time)

    def test_benchmark_dijkstra(self):
        print("\n--- Dijkstra grid pathfinding benchmarks ---")

        elapsed = 0

        for size in [10, 20, 30]:
            elapsed = timeit.timeit(
                lambda: dijkstra(size, size, (0, 0), (size - 1, size - 1), set()),
                number=self.REPEAT
            )

            average_ms = (elapsed / self.REPEAT) * 1000

            print(f"{size}x{size} grid | average={average_ms:.2f} ms")

        self.assertLess(elapsed, 5.0)

    def test_benchmark_grid_paths(self):
        print("\n--- Dynamic programming grid path benchmarks ---")

        elapsed = 0

        for size in [10, 20, 50]:
            elapsed = timeit.timeit(
                lambda: gridPaths(size, size, set()),
                number=self.REPEAT
            )

            average_ms = (elapsed / self.REPEAT) * 1000

            print(f"{size}x{size} grid | average={average_ms:.2f} ms")

        self.assertLess(elapsed, 5.0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
