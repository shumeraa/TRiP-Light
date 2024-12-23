import unittest
from src.tripLeaderManager import TripLeader, TripLeaderManager


class TestTripLeader(unittest.TestCase):
    def test_categorize_prefs_empty_list(self):
        leader = TripLeader(name="Alice", prefs=[])
        self.assertEqual(leader.categorize_prefs(), [])

    def test_categorize_prefs_all_nan(self):
        leader = TripLeader(name="Bob", prefs=[float("nan"), float("nan")])
        categorized = leader.categorize_prefs()
        self.assertEqual(len(categorized), 2)
        for _, category in categorized:
            self.assertEqual(category, "nan")

    def test_categorize_prefs_regular(self):
        leader = TripLeader(name="Charlie", prefs=[1, 2, 3, 4, 5, 6])
        expected = [
            (1, "bottom third"),
            (2, "bottom third"),
            (3, "middle third"),
            (4, "middle third"),
            (5, "top third"),
            (6, "top third"),
        ]
        self.assertEqual(leader.categorize_prefs(), expected)

    def test_categorize_prefs_unsorted_input(self):
        leader = TripLeader(name="Diana", prefs=[10, 5, 1, 7, 2, 8])
        expected = [
            (10, "top third"),
            (5, "middle third"),
            (1, "bottom third"),
            (7, "middle third"),
            (2, "bottom third"),
            (8, "top third"),
        ]
        self.assertEqual(leader.categorize_prefs(), expected)

    def test_categorize_prefs_with_nan(self):
        leader = TripLeader(name="Eve", prefs=[1, float("nan"), 3, 2])
        categorized = leader.categorize_prefs()
        self.assertEqual(len(categorized), 4)
        self.assertIn((float("nan"), "nan"), categorized)
        self.assertIn((1, "bottom third"), categorized)
        self.assertIn((2, "middle third"), categorized)
        self.assertIn((3, "top third"), categorized)

    def test_categorize_prefs_single_element(self):
        leader = TripLeader(name="Frank", prefs=[42])
        self.assertEqual(leader.categorize_prefs(), [(42, "top third")])


class TestTripLeaderManager(unittest.TestCase):
    def setUp(self):
        self.manager = TripLeaderManager()

    def test_add_and_find_trip_leader(self):
        leader = TripLeader(name="Grace", prefs=[1, 2, 3])
        self.manager.add_trip_leader(leader)
        self.assertEqual(self.manager.find_trip_leader("Grace"), leader)

    def test_find_trip_leader_not_exist(self):
        self.assertIsNone(self.manager.find_trip_leader("NonExistent"))

    def test_get_all_trip_leaders(self):
        leader1 = TripLeader(name="Hank", prefs=[1])
        leader2 = TripLeader(name="Ivy", prefs=[2, 3])
        self.manager.add_trip_leader(leader1)
        self.manager.add_trip_leader(leader2)
        all_leaders = self.manager.get_all_trip_leaders()
        self.assertIn(leader1, all_leaders)
        self.assertIn(leader2, all_leaders)
        self.assertEqual(len(all_leaders), 2)


if __name__ == "__main__":
    unittest.main()
