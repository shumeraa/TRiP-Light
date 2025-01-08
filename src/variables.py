prefsSheetIndex = 1  # 1st sheet is 0, second sheet is 1
tripLeaderInfoIndex = 0
nameCellGuideStatus = "D4"
firstPromotionalCategoryCell = "E4"  # the last promotional category cell must have a blank column after it, that is the signal to stop
leaderGuideStatusFileName = "TripsAndLeaderStatusInfo.xlsx" # should be in the "Data" folder

tripCells = {
    "datesCell": "B2",
    "tripCell": "C2"

}

leaderCells = {
    "leaderTripCell": "C2",
    "leaderPrefsCell": "D2",
    "nameCell": "C4",
    "semestersLeftCell": "D5",
    "tripSatisfactionCell": "D6",
    "tripInvolvementCell": "D7",
    "tripsAssignedCell": "D9",
    "tripDropCell": "D10",
    "tripPickupCell": "D11",
    "tripCancelledCell": "D12",
    "mainGoalCell": "D14",
    "interestedCategoriesCell": "D15",
    "threeLeadersCell": ["C17", "D17", "E17"],
    "leadershipStyleCell": ["C18", "D18", "E18"],
    "additionalNotesCell": "D21",
    "numTrips": 58
}
# example cell: 'B2', must start with letter and end with number
