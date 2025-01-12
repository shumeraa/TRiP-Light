import math
from utils import reformat_cells


class TripLeader:
    def __init__(
        self,
        name,
        prefs,
        # Numerical Questions
        semestersLeft,
        tripSatisfaction,
        tripsAssigned,
        tripDropped,
        tripPickedUp,
        tripCancelled,
        # Short Answer Questions
        mainGoal,
        interestedCategories,
        threeLeaders,
        leadershipStyle,
        additionalNotes,
    ):
        self.guideStatus = {}  # will be added after instantiation
        self.name = name
        self.prefs = prefs
        self.semestersLeft = semestersLeft
        self.tripSatisfaction = tripSatisfaction
        self.tripsAssigned = tripsAssigned
        self.tripDropped = tripDropped
        self.tripPickedUp = tripPickedUp
        self.tripCancelled = tripCancelled
        self.mainGoal = mainGoal
        self.interestedCategories = interestedCategories
        self.threeLeaders = threeLeaders
        self.leadershipStyle = leadershipStyle
        self.additionalNotes = additionalNotes

    def __repr__(self):
        prefs_str = ", ".join(map(str, self.prefs))
        guide_status_str = ", ".join(f"{k}: {v}" for k, v in self.guideStatus.items())
        return f"TripLeader(name={self.name}, prefs=[{prefs_str}], guideStatus={{ {guide_status_str} }})"

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
            key: reformat_cells(value) for key, value in cell_mappings.items()
        }

    def add_trip_leader(self, trip_leader: TripLeader):
        self.trip_leaders[trip_leader.name] = trip_leader

    def get_all_trip_leaders(self):
        # iterate through dict and return list of trip leaders
        return list(self.trip_leaders.values())

    def find_trip_leader(self, name: str):
        return self.trip_leaders.get(name, None)
