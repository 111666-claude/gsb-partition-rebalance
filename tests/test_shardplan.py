import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shardplan import core


class ShardplanTest(unittest.TestCase):
    def test_node_load_counts(self):
        placements = {"s1": "A", "s2": "A", "s3": "B"}
        self.assertEqual(core.node_load(placements), {"A": 2, "B": 1})

    def test_balanced_plan_is_empty(self):
        placements = {"s1": "A", "s2": "B"}
        caps = {"A": 1, "B": 1}
        self.assertEqual(core.plan(placements, caps, 5, core.Counter()), [])

    def test_single_over_cap_moves_one(self):
        placements = {"s1": "A", "s2": "A"}
        caps = {"A": 1, "B": 5}
        moves = core.plan(placements, caps, 5, core.Counter())
        self.assertEqual(len(moves), 1)
        self.assertEqual(moves[0]["src"], "A")

    def test_move_has_dst(self):
        placements = {"s1": "A", "s2": "A"}
        caps = {"A": 1, "B": 5}
        moves = core.plan(placements, caps, 5, core.Counter())
        self.assertIn("dst", moves[0])

    def test_render_reports_line(self):
        placements = {"s1": "A", "s2": "A"}
        caps = {"A": 1, "B": 5}
        moves = core.plan(placements, caps, 5, core.Counter())
        text = core.render(moves, placements, caps)
        self.assertIn("s1 A -> B", text)
        self.assertIn("moves=", text)


if __name__ == "__main__":
    unittest.main()
