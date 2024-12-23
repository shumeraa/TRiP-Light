from functions import (
    get_user_input,
    excel_to_df_cell,
    process_excel_files,
    get_sheet_names,
    createExcelFileHighlighedOnThirds,
)
from tripManager import TripManager
from tripLeaderManager import TripLeaderManager
import CONSTANTS

welcomeText = "Welcome to TRiP-Light! Before you start, please make sure you have all of the prefs in your 'Data' folder located in the same directory as this script. Make sure there is only 1 empty row at the top of the prefs."

if __name__ == "__main__":
    print(welcomeText)

    # converts excel cell name format to a pandas friendly format 
    dateXY, tripXY, prefXY, nameXY = excel_to_df_cell(
        CONSTANTS.datesCell, CONSTANTS.tripCell, CONSTANTS.tripPrefsCell, CONSTANTS.nameCell
    )

    trip_leader_manager = TripLeaderManager()
    trip_manager = TripManager()

    # Add trips and create leaders
    process_excel_files(
        trip_leader_manager,
        trip_manager,
        CONSTANTS.numTrips,
        dateXY,
        tripXY,
        prefXY,
        nameXY,
        CONSTANTS.prefsSheetIndex,
        CONSTANTS.tripLeaderInfoIndex,
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
