from functions import (
    process_all_pref_files,
    createExcelFileHighlighedOnThirds,
    process_leader_status_file,
    process_trip_status_file,
)
from tripManager import TripManager
from tripLeaderManager import TripLeaderManager
import variables

welcomeText = "Welcome to TRiP-Light! Before you start, please make sure you have all of the prefs in your 'Data' folder located in the same directory as this script. Make sure there is only 1 empty row at the top of the prefs."

if __name__ == "__main__":
    print(welcomeText)

    prefsSheetIndex = variables.prefsSheetIndex
    tripLeaderInfoIndex = variables.tripLeaderInfoIndex
    folderPath = variables.folderPath

    trip_leader_manager = TripLeaderManager(variables.leaderInfoDict)
    trip_manager = TripManager(variables.tripInfoDict)

    tripStatusFileName = trip_manager.cell_mappings["tripStatusFileName"]
    leaderGuideStatusFileName = trip_leader_manager.cell_mappings[
        "leaderGuideStatusFileName"
    ]

    # Add trips and create leaders
    process_all_pref_files(
        trip_leader_manager,
        prefsSheetIndex,
        tripLeaderInfoIndex,
        leaderGuideStatusFileName,
        tripStatusFileName,
        folderPath,
    )

    process_trip_status_file(trip_manager)

    process_leader_status_file(trip_leader_manager, trip_manager)

    createExcelFileHighlighedOnThirds(trip_leader_manager, trip_manager)
    
    for trip in trip_manager.get_trips():
        print(trip)
        
    print("____________________")
    
    for trip_leader in trip_leader_manager.get_all_trip_leaders():
        print(trip_leader)
