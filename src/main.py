from functions import (
    excel_to_df_cell,
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
    trip_manager = TripManager()

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

    process_leader_status_file(trip_leader_manager)

    process_trip_status_file(trip_manager)

    createExcelFileHighlighedOnThirds(trip_leader_manager, trip_manager)
