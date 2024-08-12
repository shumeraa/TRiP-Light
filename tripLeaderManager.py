class TripLeader:
    def __init__(self, name: str, prefs=None):
        self.name = name
        self.prefs = prefs if prefs is not None else []

    def categorize_prefs(self):
        if not self.prefs:
            return []

        # Filter out zeroes and sort the remaining preferences
        sorted_prefs = sorted([pref for pref in self.prefs if pref != 0])
        length = len(sorted_prefs)

        if length == 0:
            return [(pref, "No Category") for pref in self.prefs]

        # Define the indices for the thirds
        bottom_third = sorted_prefs[: length // 3]
        middle_third = sorted_prefs[length // 3 : 2 * length // 3]
        top_third = sorted_prefs[2 * length // 3 :]

        # Categorize each preference
        categorized_prefs = []
        for pref in self.prefs:
            if pref == 0:
                continue
            if pref in bottom_third:
                categorized_prefs.append((pref, "bottom third"))
            elif pref in middle_third:
                categorized_prefs.append((pref, "middle third"))
            elif pref in top_third:
                categorized_prefs.append((pref, "top third"))

        return categorized_prefs


class TripLeaderManager:
    def __init__(self):
        self.trip_leaders = []

    def add_trip_leader(self, trip_leader: TripLeader):
        self.trip_leaders.append(trip_leader)

    def get_all_trip_leaders(self):
        return self.trip_leaders

    def find_trip_leader(self, name: str):
        for leader in self.trip_leaders:
            if leader.name == name:
                return leader
        return None


# # Example usage:
# manager = TripLeaderManager()

# leader1 = TripLeader("John Doe", [10, 3, 5, 8, 2, 7, 1, 9, 6, 4])
# leader2 = TripLeader("Jane Smith", [20, 15, 5, 10, 25, 0])

# manager.add_trip_leader(leader1)
# manager.add_trip_leader(leader2)

# # Retrieve and print all trip leaders
# all_leaders = manager.get_all_trip_leaders()
# for leader in all_leaders:
#     print(f"Trip Leader: {leader.name}")
#     print("Categorized Preferences:", leader.categorize_prefs())

# # Find a specific trip leader by name
# found_leader = manager.find_trip_leader("Jane Smith")
# if found_leader:
#     print(f"Found Trip Leader: {found_leader.name}")
#     print("Categorized Preferences:", found_leader.categorize_prefs())
# else:
#     print("Trip Leader not found.")
