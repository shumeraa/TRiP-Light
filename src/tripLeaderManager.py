import math
from functions import excel_to_df_indices


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

        for key, value in cell_mappings.items():
            # if it is a list , iterate over each value in the list
            # this is for values like threeLeadersCell
            if isinstance(value, list):
                self.cell_mappings[key] = [
                    self.excel_to_df_indices(cell) for cell in value
                ]
            elif isinstance(value, int):
                self.cell_mappings[key] = value
            else:
                self.cell_mappings[key] = excel_to_df_indices(value)

    def add_trip_leader(self, trip_leader: TripLeader):
        self.trip_leaders[trip_leader.name] = trip_leader

    def get_all_trip_leaders(self):
        # iterate through dict and return list of trip leaders
        return list(self.trip_leaders.values())

    def find_trip_leader(self, name: str):
        return self.trip_leaders.get(name, None)
