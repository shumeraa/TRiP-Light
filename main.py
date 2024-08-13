from functions import (
    get_user_input,
    excel_to_df_cell,
    process_excel_files,
    get_sheet_names,
    createExcelFile,
)
from tripManager import TripManager
from tripLeaderManager import TripLeaderManager

welcomeText = "Welcome to TRiP-Light! Before you start, please make sure you have all of the prefs in your 'Data' folder located in the same directory as this script. Make sure there is only 1 empty row at the top of the prefs."

if __name__ == "__main__":
    print(welcomeText)

    numberOfTrips = int(input("How many trips are are there this semester? "))

    dates_cell = get_user_input("Dates")
    trip_cell = get_user_input("TRiP")
    preferences_cell = get_user_input("Preferences")
    name_cell = get_user_input("Name")  # This is not correct, we do not want the header

    dateXY, tripXY, prefXY, nameXY = excel_to_df_cell(
        dates_cell, trip_cell, preferences_cell, name_cell
    )

    prefsSheetIndex = get_sheet_names("Prefs")
    tripLeaderInfoIndex = get_sheet_names("Prefs")

    trip_leader_manager = TripLeaderManager()
    trip_manager = TripManager()

    process_excel_files(
        trip_leader_manager,
        trip_manager,
        numberOfTrips,
        dateXY,
        tripXY,
        prefXY,
        nameXY,
        prefsSheetIndex,
        tripLeaderInfoIndex,
    )

    createExcelFile(trip_leader_manager, trip_manager)


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
