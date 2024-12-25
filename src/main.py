from functions import (
    excel_to_df_cell,
    process_all_pref_files,
    createExcelFileHighlighedOnThirds,
    process_leader_status_file,
)
from tripManager import TripManager
from tripLeaderManager import TripLeaderManager
import variables

welcomeText = "Welcome to TRiP-Light! Before you start, please make sure you have all of the prefs in your 'Data' folder located in the same directory as this script. Make sure there is only 1 empty row at the top of the prefs."

if __name__ == "__main__":
    print(welcomeText)

    # converts excel cell name format to a pandas friendly format
    dateXY, tripXY, prefXY, nameXY, guideStatusNameXY, guideStatusFirstCategoryXY = (
        excel_to_df_cell(
            variables.datesCell,
            variables.tripCell,
            variables.tripPrefsCell,
            variables.nameCell,
            variables.nameCellGuideStatus,
            variables.firstPromotionalCategoryCell,
        )
    )

    trip_leader_manager = TripLeaderManager()
    trip_manager = TripManager()

    # Add trips and create leaders
    process_all_pref_files(
        trip_leader_manager,
        trip_manager,
        variables.numTrips,
        dateXY,
        tripXY,
        prefXY,
        nameXY,
        variables.prefsSheetIndex,
        variables.tripLeaderInfoIndex,
        guideStatusNameXY,
        guideStatusFirstCategoryXY,
        variables.leaderGuideStatusFileName,
    )

    process_leader_status_file(
        variables.leaderGuideStatusFileName,
        trip_leader_manager,
        guideStatusNameXY,
        guideStatusFirstCategoryXY,
    )

    createExcelFileHighlighedOnThirds(trip_leader_manager, trip_manager)


# Example usage:
# leader = TripLeader("John Doe", [10, 3, 5, 8, 2, 7, 1, 9, 6, 4, 0, 0])

# print(f"Trip Leader: {leader.name}")
# print("Preferences categorized:")
# for pref, category in leader.categorize_prefs():
#     print(f"Preference: {pref}, Category: {category}")

# Example usage:
#
# manager.add_trip("Beach Trip", datetime(2024, 8, 15))
# manager.add_trip("Mountain Hike", datetime(2024, 9, 10))

# print(manager.get_trips())
# print(manager.get_trips_by_date())
