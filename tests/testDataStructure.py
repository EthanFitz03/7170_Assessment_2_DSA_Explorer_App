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

# focuses on data structure logic
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


from dataStructures import stack, queue, linkedList, BST

# Stack test
class TestStack(unittest.TestCase):
    def setUp(self):
        self.s = stack()

    def test_push_pop_sequence_size(self):
        self.s.push(10)
        self.s.push(20)
        self.s.push(30)

        self.s.pop()
        self.s.pop()

        self.assertEqual(self.s.size(), 1)

    def test_push_pop_sequence_correct_order(self):
        self.s.push(10)
        self.s.push(20)
        self.s.push(30)

        self.s.pop()
        self.s.pop()

        self.assertEqual(self.s.peek(), 10)

    def test_lifo_order(self):
        for value in [5, 15, 25]:
            self.s.push(value)

        self.assertEqual(self.s.pop(), 25)
        self.assertEqual(self.s.pop(), 15)
        self.assertEqual(self.s.pop(), 5)

    def test_pop_empty_stack_returns_none(self):
        self.assertIsNone(self.s.pop())

    def test_peek_empty_stack_returns_none(self):
        self.assertIsNone(self.s.peek())

    def test_peek_does_not_remove(self):
        self.s.push(99)

        self.assertEqual(self.s.peek(), 99)
        self.assertEqual(self.s.size(), 1)

    def test_is_empty_on_new_stack(self):
        self.assertTrue(self.s.isEmpty())

    def test_is_empty_after_push(self):
        self.s.push(1)
        self.assertFalse(self.s.isEmpty())

    def test_items_returns_values_in_order(self):
        self.s.push(1)
        self.s.push(2)
        self.s.push(3)

        self.assertEqual(self.s.items(), [1, 2, 3])

    def test_items_returns_copy(self):
        self.s.push(1)
        self.s.push(2)
        self.s.push(3)

        returned_items = self.s.items()
        returned_items.append(999)

        self.assertEqual(self.s.items(), [1, 2, 3])

# Queue test
class TestQueue(unittest.TestCase):
    def setUp(self):
        self.q = queue()

    def test_insert_remove_fifo_order(self):
        for value in [10, 20, 30, 40]:
            self.q.insert(value)

        self.assertEqual(self.q.remove(), 10)
        self.assertEqual(self.q.remove(), 20)
        self.assertEqual(self.q.remove(), 30)

        self.assertEqual(self.q.size(), 1)
        self.assertEqual(self.q.items(), [40])

    def test_remove_returns_front_element(self):
        self.q.insert(1)
        self.q.insert(2)
        self.q.insert(3)

        self.assertEqual(self.q.remove(), 1)
        self.assertEqual(self.q.remove(), 2)
        self.assertEqual(self.q.remove(), 3)

    def test_remove_empty_queue_returns_none(self):
        self.assertIsNone(self.q.remove())

    def test_size_tracks_correctly(self):
        self.assertEqual(self.q.size(), 0)

        self.q.insert(5)
        self.assertEqual(self.q.size(), 1)

        self.q.remove()
        self.assertEqual(self.q.size(), 0)

    def test_is_empty_on_new_queue(self):
        self.assertTrue(self.q.isEmpty())

    def test_is_empty_after_insert(self):
        self.q.insert(1)
        self.assertFalse(self.q.isEmpty())

    def test_items_returns_copy(self):
        self.q.insert(1)
        self.q.insert(2)

        returned_items = self.q.items()
        returned_items.append(999)

        self.assertEqual(self.q.items(), [1, 2])

# List test
class TestLinkedList(unittest.TestCase):
    def setUp(self):
        self.ll = linkedList()

    def test_insert_at_head(self):
        self.ll.insertAt(20, 0)
        self.ll.insertAt(10, 0)

        self.assertEqual(self.ll.traverse(), [10, 20])

    def test_insert_at_position(self):
        self.ll.insertAt(5, 0)
        self.ll.insertAt(15, 1)
        self.ll.insertAt(25, 2)
        self.ll.insertAt(10, 2)

        self.assertEqual(self.ll.traverse(), [5, 15, 10, 25])

    def test_insert_beyond_end_appends(self):
        self.ll.insertAt(1, 0)
        self.ll.insertAt(2, 999)

        self.assertEqual(self.ll.traverse(), [1, 2])

    def test_delete_existing_node(self):
        for value in [10, 20, 30]:
            self.ll.insertAt(value, len(self.ll.traverse()))

        self.assertTrue(self.ll.delete(20))
        self.assertEqual(self.ll.traverse(), [10, 30])

    def test_delete_head_node(self):
        for value in [10, 20, 30]:
            self.ll.insertAt(value, len(self.ll.traverse()))

        self.assertTrue(self.ll.delete(10))
        self.assertEqual(self.ll.traverse(), [20, 30])

    def test_delete_missing_node_returns_false(self):
        self.ll.insertAt(10, 0)

        self.assertFalse(self.ll.delete(99))
        self.assertEqual(self.ll.traverse(), [10])

    def test_delete_from_empty_list_returns_false(self):
        self.assertFalse(self.ll.delete(99))

    def test_reverse_multiple_nodes(self):
        for value in [1, 2, 3, 4]:
            self.ll.insertAt(value, len(self.ll.traverse()))

        self.ll.reverse()

        self.assertEqual(self.ll.traverse(), [4, 3, 2, 1])

    def test_reverse_empty_list(self):
        self.ll.reverse()
        self.assertEqual(self.ll.traverse(), [])

    def test_reverse_single_node(self):
        self.ll.insertAt(10, 0)
        self.ll.reverse()

        self.assertEqual(self.ll.traverse(), [10])

    def test_traverse_empty_list(self):
        self.assertEqual(self.ll.traverse(), [])

# BST test
class TestBST(unittest.TestCase):
    def setUp(self):
        self.bst = BST()

    def test_inorder_traversal(self):
        for value in [50, 30, 70]:
            self.bst.insert(value)

        self.assertEqual(self.bst.inorder(), [30, 50, 70])

    def test_preorder_traversal(self):
        for value in [50, 30, 70]:
            self.bst.insert(value)

        self.assertEqual(self.bst.preorder(), [50, 30, 70])

    def test_postorder_traversal(self):
        for value in [50, 30, 70]:
            self.bst.insert(value)

        self.assertEqual(self.bst.postorder(), [30, 70, 50])

    def test_inorder_is_sorted(self):
        values = [40, 10, 60, 5, 30, 50, 70]

        for value in values:
            self.bst.insert(value)

        self.assertEqual(self.bst.inorder(), sorted(values))

    def test_duplicate_values_are_ignored(self):
        self.bst.insert(50)
        self.bst.insert(50)

        self.assertEqual(self.bst.inorder(), [50])

    def test_single_node_tree(self):
        self.bst.insert(42)

        self.assertEqual(self.bst.inorder(), [42])
        self.assertEqual(self.bst.preorder(), [42])
        self.assertEqual(self.bst.postorder(), [42])

    def test_empty_tree_traversals(self):
        self.assertEqual(self.bst.inorder(), [])
        self.assertEqual(self.bst.preorder(), [])
        self.assertEqual(self.bst.postorder(), [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
