import math
from utils import reformat_cells_manager


class TripLeader:
    def __init__(self, name: str, prefs=None):
        self.name = name
        self.prefs = prefs if prefs is not None else []
        self.guideStatus = {}

    def categorize_prefs(self):
        if not self.prefs:
            return []

        # Filter out zeroes and sort the remaining preferences
        sorted_prefs = sorted(
            [
                pref
                for pref in self.prefs
                if not (isinstance(pref, float) and math.isnan(pref))
            ]
        )
        length = len(sorted_prefs)

        if length == 0:
            return [(pref, "nan") for pref in self.prefs]

        # Define the indices for the thirds
        bottom_third = sorted_prefs[: length // 3]
        middle_third = sorted_prefs[length // 3 : 2 * length // 3]
        top_third = sorted_prefs[2 * length // 3 :]

        # Categorize each preference
        categorized_prefs = []
        for pref in self.prefs:
            if isinstance(pref, float) and math.isnan(pref):
                categorized_prefs.append((pref, "nan"))
            if pref in bottom_third:
                categorized_prefs.append((pref, "bottom third"))
            elif pref in middle_third:
                categorized_prefs.append((pref, "middle third"))
            elif pref in top_third:
                categorized_prefs.append((pref, "top third"))

        return categorized_prefs


class TripLeaderManager:
    def __init__(self, cell_mappings):
        self.trip_leaders = {}

        self.cell_mappings = {}

        self.cell_mappings = {
            key: reformat_cells_manager(value) for key, value in cell_mappings.items()
        }

    def add_trip_leader(self, trip_leader: TripLeader):
        self.trip_leaders[trip_leader.name] = trip_leader

    def get_all_trip_leaders(self):
        # iterate through dict and return list of trip leaders
        return list(self.trip_leaders.values())

    def find_trip_leader(self, name: str):
        return self.trip_leaders.get(name, None)
