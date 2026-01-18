"""Main entry point for TRiP-Light preference processing.

This script orchestrates the complete trip leader preference processing pipeline:
1. Reads preference files from the Data/ directory
2. Processes trip status and leader guide status information
3. Generates three formatted Excel output files with highlighted preferences

Usage:
    python src/main.py

Output files are created in the output/ directory:
- prefsOutput.xlsx: Preferences highlighted by leader guide status
- numericalQuestionsOutput.xlsx: Numerical metrics for each leader
- shortAnswerQuestionsOutput.xlsx: Text responses from leaders
"""

import config
from functions import (
    outputNumericalQuestions,
    outputPrefsHighlightOnLeader,
    outputShortAnswerQuestions,
    process_all_pref_files,
    process_leader_status_file,
    process_trip_status_file,
)
from tripLeaderManager import TripLeaderManager
from tripManager import TripManager

WELCOME_TEXT = (
    "Welcome to TRiP-Light! Before you start, please make sure you have all of the "
    "prefs in your 'Data' folder located in the same directory as this script. "
    "Make sure there is only 1 empty row at the top of the prefs."
)

if __name__ == "__main__":
    print(WELCOME_TEXT)

    # Load configuration variables
    prefsSheetIndex = config.prefsSheetIndex
    tripLeaderInfoIndex = config.tripLeaderInfoIndex
    folderPath = config.folderPath

    # Initialize managers with cell mapping dictionaries
    trip_leader_manager = TripLeaderManager(config.leaderInfoDict)
    trip_manager = TripManager(config.tripInfoDict)

    # Extract file paths from cell mappings
    tripStatusFileName = trip_manager.cell_mappings["tripStatusFileName"]
    leaderGuideStatusFileName = trip_leader_manager.cell_mappings[
        "leaderGuideStatusFileName"
    ]

    # Process all preference files and load trip leaders
    process_all_pref_files(
        trip_leader_manager,
        prefsSheetIndex,
        tripLeaderInfoIndex,
        leaderGuideStatusFileName,
        tripStatusFileName,
        folderPath,
    )

    # Load trip information from TripStatusInfo.xlsx
    process_trip_status_file(trip_manager)

    # Load leader guide status and add to trip leaders
    process_leader_status_file(trip_leader_manager, trip_manager)

    # Generate output files
    outputPrefsHighlightOnLeader(trip_leader_manager, trip_manager)
    outputNumericalQuestions(trip_leader_manager)
    outputShortAnswerQuestions(trip_leader_manager)
