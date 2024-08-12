from functions import get_user_input, excel_to_df_cell, process_excel_files
from tripManager import TripManager

welcomeText = "Welcome to TRiP-Light! Before you start, please make sure you have all of the prefs in your 'Data' folder located in the same directory as this script."

if __name__ == "__main__":
    print(welcomeText)

    dates_cell = get_user_input("Dates")
    trip_cell = get_user_input("TRiP")
    preferences_cell = get_user_input("Preferences")
    name_cell = get_user_input("Name")

    dateXY, tripXY, prefXY, nameXY = excel_to_df_cell(dates_cell, trip_cell, preferences_cell, name_cell)
    
    prefsSheetIndex = get_user_input("Prefs")
    tripLeaderInfoIndex = get_user_input("Prefs")
    
    process_excel_files(dateXY, tripXY, prefXY, nameXY)
    


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
