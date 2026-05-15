import os
import sys
import unittest
import random
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


from sortingAlgorithmVisualiser import bubblesort, selectionsort, mergesort, mergesortactions
from graphVisualiser import Graph
from heapVisualiser import Heap, EventQueue

# Bubble tests
class TestBubbleSort(unittest.TestCase):
    def test_correctness_spec_array(self):
        steps = bubblesort([5, 3, 8, 1, 2])
        final_data, *_ = steps[-1]

        self.assertEqual(final_data, [1, 2, 3, 5, 8])

    def test_already_sorted(self):
        steps = bubblesort([1, 2, 3])
        final_data, *_ = steps[-1]

        self.assertEqual(final_data, [1, 2, 3])

    def test_reverse_sorted(self):
        steps = bubblesort([5, 4, 3, 2, 1])
        final_data, *_ = steps[-1]

        self.assertEqual(final_data, [1, 2, 3, 4, 5])

    def test_single_element(self):
        steps = bubblesort([7])
        final_data, *_ = steps[-1]

        self.assertEqual(final_data, [7])

    def test_empty_list(self):
        steps = bubblesort([])
        final_data, *_ = steps[-1]

        self.assertEqual(final_data, [])

    def test_swap_flag_is_boolean(self):
        steps = bubblesort([3, 1, 2])

        for _, _, _, swapped in steps:
            self.assertIsInstance(swapped, bool)

    def test_final_step_has_none_indices(self):
        steps = bubblesort([3, 1])
        _, index_a, index_b, _ = steps[-1]

        self.assertIsNone(index_a)
        self.assertIsNone(index_b)

    def test_step_count_reasonable(self):
        steps = bubblesort([3, 1, 2])

        self.assertGreater(len(steps), 1)

# Selection sort test
class TestSelectionSort(unittest.TestCase):
    def test_correctness(self):
        steps = selectionsort([5, 3, 8, 1, 2])
        final_data, *_ = steps[-1]

        self.assertEqual(final_data, [1, 2, 3, 5, 8])

    def test_already_sorted(self):
        steps = selectionsort([1, 2, 3])
        final_data, *_ = steps[-1]

        self.assertEqual(final_data, [1, 2, 3])

    def test_reverse_sorted(self):
        steps = selectionsort([4, 3, 2, 1])
        final_data, *_ = steps[-1]

        self.assertEqual(final_data, [1, 2, 3, 4])

    def test_swap_steps_exist_for_unsorted_input(self):
        steps = selectionsort([3, 1, 2])
        swap_steps = [step for step in steps if step[3] is True]

        self.assertGreater(len(swap_steps), 0)

    def test_no_swap_steps_for_sorted_input(self):
        steps = selectionsort([1, 2, 3])
        swap_steps = [step for step in steps if step[3] is True]

        self.assertEqual(len(swap_steps), 0)

    def test_final_step_has_none_indices(self):
        steps = selectionsort([3, 1])
        _, index_a, index_b, _ = steps[-1]

        self.assertIsNone(index_a)
        self.assertIsNone(index_b)

# Merge test
class TestMergeSort(unittest.TestCase):
    def test_correctness(self):
        self.assertEqual(mergesort([5, 3, 8, 1, 2]), [1, 2, 3, 5, 8])

    def test_empty_list(self):
        self.assertEqual(mergesort([]), [])

    def test_single_element(self):
        self.assertEqual(mergesort([42]), [42])

    def test_duplicates(self):
        self.assertEqual(mergesort([3, 1, 3, 2]), [1, 2, 3, 3])

    def test_large_random_list(self):
        data = random.sample(range(1000), 50)

        self.assertEqual(mergesort(data), sorted(data))

    def test_mergesortactions_final_step_sorted(self):
        steps = mergesortactions([4, 1, 3, 2])
        final_data, *_ = steps[-1]

        self.assertEqual(final_data, [1, 2, 3, 4])

# Graph test
class TestGraph(unittest.TestCase):
    def setUp(self):
        self.g = Graph()

        for vertex in ["A", "B", "C", "D", "E", "F"]:
            self.g.newVertex(vertex)

        self.g.newEdge("A", "B")
        self.g.newEdge("A", "C")
        self.g.newEdge("B", "D")
        self.g.newEdge("B", "E")
        self.g.newEdge("C", "F")
        self.g.newEdge("E", "F")

    def test_vertices_added(self):
        self.assertEqual(set(self.g.vertices()), {"A", "B", "C", "D", "E", "F"})

    def test_edges_added(self):
        edges = self.g.edges()
        edge_sets = {frozenset(edge) for edge in edges}

        self.assertIn(frozenset(("A", "B")), edge_sets)
        self.assertIn(frozenset(("A", "C")), edge_sets)
        self.assertIn(frozenset(("E", "F")), edge_sets)

    def test_bfs_from_A(self):
        result = self.g.breadthFirst("A")

        self.assertEqual(result[0], "A")
        self.assertEqual(len(result), 6)
        self.assertEqual(result, ["A", "B", "C", "D", "E", "F"])

    def test_bfs_levels_from_A(self):
        levels = self.g.breadthFirstL("A")

        self.assertEqual(levels[0], ["A"])
        self.assertEqual(set(levels[1]), {"B", "C"})
        self.assertEqual(set(levels[2]), {"D", "E", "F"})

    def test_bfs_from_F(self):
        result = self.g.breadthFirst("F")

        self.assertEqual(result[0], "F")
        self.assertEqual(result, ["F", "C", "E", "A", "B", "D"])

    def test_bfs_levels_from_F(self):
        levels = self.g.breadthFirstL("F")

        self.assertEqual(levels[0], ["F"])
        self.assertEqual(set(levels[1]), {"C", "E"})
        self.assertEqual(set(levels[2]), {"A", "B"})
        self.assertEqual(levels[3], ["D"])

    def test_dfs_from_A(self):
        result = self.g.depthFirst("A")

        self.assertEqual(result[0], "A")
        self.assertEqual(result, ["A", "B", "D", "E", "F", "C"])

    def test_dfs_from_C(self):
        result = self.g.depthFirst("C")

        self.assertEqual(result[0], "C")
        self.assertEqual(len(result), 6)
        self.assertIn("F", result)
        self.assertIn("A", result)

    def test_dfs_depths_from_A(self):
        depths = self.g.depthFirstD("A")

        self.assertEqual(depths[0], ["A"])
        self.assertIn("B", depths[1])

    def test_bfs_unknown_vertex_returns_empty(self):
        self.assertEqual(self.g.breadthFirst("Z"), [])

    def test_dfs_unknown_vertex_returns_empty(self):
        self.assertEqual(self.g.depthFirst("Z"), [])

    def test_no_self_loops_allowed(self):
        with self.assertRaises(ValueError):
            self.g.newEdge("A", "A")

# Heap test
class TestHeap(unittest.TestCase):
    def setUp(self):
        self.h = Heap()

    def test_insert_and_peek_minimum(self):
        for value in [5, 1, 9, 3]:
            self.h.insert(value)

        self.assertEqual(self.h.peek(), 1)

    def test_remove_returns_minimum(self):
        for value in [5, 1, 9, 3]:
            self.h.insert(value)

        self.assertEqual(self.h.remove(), 1)
        self.assertEqual(self.h.remove(), 3)

    def test_repeated_remove_returns_sorted_values(self):
        values = [7, 2, 5, 1, 8, 3]

        for value in values:
            self.h.insert(value)

        extracted = [self.h.remove() for _ in range(len(values))]

        self.assertEqual(extracted, sorted(values))

    def test_remove_empty_returns_none(self):
        self.assertIsNone(self.h.remove())

    def test_peek_empty_returns_none(self):
        self.assertIsNone(self.h.peek())

    def test_is_empty(self):
        self.assertTrue(self.h.isEmpty())

        self.h.insert(10)

        self.assertFalse(self.h.isEmpty())

# EQ test
class TestEventQueue(unittest.TestCase):
    def setUp(self):
        self.eq = EventQueue()

    def test_priority_one_processed_first(self):
        self.eq.insert(priority=5, time=10, description="Low")
        self.eq.insert(priority=1, time=10, description="High")

        event = self.eq.remove()

        self.assertEqual(event["description"], "High")

    def test_priority_beats_time(self):
        self.eq.insert(priority=5, time=1, description="Low priority early time")
        self.eq.insert(priority=1, time=20, description="High priority later time")

        event = self.eq.remove()

        self.assertEqual(event["description"], "High priority later time")

    def test_time_breaks_tie_when_priority_same(self):
        self.eq.insert(priority=2, time=10, description="Later")
        self.eq.insert(priority=2, time=3, description="Earlier")

        event = self.eq.remove()

        self.assertEqual(event["description"], "Earlier")

    def test_fifo_when_priority_and_time_same(self):
        self.eq.insert(priority=3, time=5, description="First")
        self.eq.insert(priority=3, time=5, description="Second")

        first = self.eq.remove()
        second = self.eq.remove()

        self.assertEqual(first["description"], "First")
        self.assertEqual(second["description"], "Second")

    def test_remove_returns_correct_fields(self):
        self.eq.insert(2, 15, "Test Event")
        event = self.eq.remove()

        self.assertIn("priority", event)
        self.assertIn("time", event)
        self.assertIn("description", event)

    def test_remove_empty_returns_none(self):
        self.assertIsNone(self.eq.remove())

    def test_is_empty(self):
        self.assertTrue(self.eq.isEmpty())

        self.eq.insert(1, 1, "X")

        self.assertFalse(self.eq.isEmpty())

    def test_traverse_returns_priority_order(self):
        self.eq.insert(4, 10, "Low")
        self.eq.insert(1, 20, "High")
        self.eq.insert(2, 5, "Medium")

        result = self.eq.traverse()

        self.assertEqual(result[0][0], 1)
        self.assertEqual(result[1][0], 2)
        self.assertEqual(result[2][0], 4)


if __name__ == "__main__":
    unittest.main(verbosity=2)
