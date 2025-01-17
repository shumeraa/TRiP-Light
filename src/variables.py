numTrips = 58
prefsSheetIndex = 1  # 1st sheet is 0, second sheet is 1
tripLeaderInfoIndex = 0
folderPath = "Data"

tripInfoDict = {
    "datesCell": "B2",
    "tripCell": "C2",
    "tripCategoryCell": "D2",
    "tripStatusFileName": "Data/TripStatusInfo.xlsx",  # make sure to include the folder name
    "numTrips": numTrips,
}

leaderInfoDict = {
    "leaderTripCell": "C2",
    "leaderPrefsCell": "D2",
    "nameCell": "C4",
    # Numerical Questions
    "semestersLeftCell": "C5",
    "tripSatisfactionCell": "C6",
    "tripsAssignedCell": "C9",
    "tripDropCell": "C10",
    "tripPickupCell": "C11",
    "tripCancelledCell": "C12",
    # Short Answer Questions
    "tripInvolvementCell": "C7",
    "mainGoalCell": "C14",
    "interestedCategoriesCell": "C15",
    "threeLeadersCell": ["C17", "D17", "E17"],
    "leadershipStyleCell": ["C18", "D18", "E18"],
    "additionalNotesCell": "B21",
    "numTrips": numTrips,
    "nameCellGuideStatus": "C3",  # The header cell
    "firstPromotionalCategoryCell": "D3",  # the last promotional category cell must have a blank column after it, that is the signal to stop
    "leaderGuideStatusFileName": "Data/TL Promotion Status.xlsx",  # make sure to include the folder name
}
# example cell: 'B2', must start with letter and end with number
