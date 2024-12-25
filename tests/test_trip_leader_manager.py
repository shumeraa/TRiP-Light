import math
import pytest
import sys
import os
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from src.tripLeaderManager import TripLeader, TripLeaderManager


def test_categorize_prefs_empty_list():
    leader = TripLeader(name="Alice", prefs=[])
    assert leader.categorize_prefs() == []


def test_categorize_prefs_all_nan():
    leader = TripLeader(name="Bob", prefs=[float("nan"), float("nan")])
    categorized = leader.categorize_prefs()
    assert len(categorized) == 2
    for _, category in categorized:
        print(category)
        assert category == "nan"


def test_categorize_prefs_regular():
    leader = TripLeader(name="Charlie", prefs=[1, 2, 3, 4, 5, 6])
    expected = [
        (1, "bottom third"),
        (2, "bottom third"),
        (3, "middle third"),
        (4, "middle third"),
        (5, "top third"),
        (6, "top third"),
    ]
    assert leader.categorize_prefs() == expected


def test_categorize_prefs_unsorted_input():
    leader = TripLeader(name="Diana", prefs=[10, 5, 1, 7, 2, 8])
    expected = [
        (10, "top third"),
        (5, "middle third"),
        (1, "bottom third"),
        (7, "middle third"),
        (2, "bottom third"),
        (8, "top third"),
    ]
    assert leader.categorize_prefs() == expected


def test_categorize_prefs_with_nan():
    leader = TripLeader(name="Eve", prefs=[1, float("nan"), 3, 2])
    categorized = leader.categorize_prefs()
    assert len(categorized) == 4
    assert any(math.isnan(pref) and category == "nan" for pref, category in categorized)
    assert (1, "bottom third") in categorized
    assert (2, "middle third") in categorized
    assert (3, "top third") in categorized


def test_categorize_prefs_single_element():
    leader = TripLeader(name="Frank", prefs=[42])
    assert leader.categorize_prefs() == [(42, "top third")]


@pytest.fixture
def trip_leader_manager():
    return TripLeaderManager()


def test_add_and_find_trip_leader(trip_leader_manager):
    leader = TripLeader(name="Grace", prefs=[1, 2, 3])
    trip_leader_manager.add_trip_leader(leader)
    assert trip_leader_manager.find_trip_leader("Grace") == leader


def test_find_trip_leader_not_exist(trip_leader_manager):
    assert trip_leader_manager.find_trip_leader("NonExistent") is None


def test_get_all_trip_leaders(trip_leader_manager):
    leader1 = TripLeader(name="Hank", prefs=[1])
    leader2 = TripLeader(name="Ivy", prefs=[2, 3])
    trip_leader_manager.add_trip_leader(leader1)
    trip_leader_manager.add_trip_leader(leader2)
    all_leaders = trip_leader_manager.get_all_trip_leaders()
    assert leader1 in all_leaders
    assert leader2 in all_leaders
    assert len(all_leaders) == 2
