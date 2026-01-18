numTrips = 47
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
    "leaderPrefsCell": "E2",
    "nameCell": "C4",
    # Numerical Questions
    "semestersLeftCell": "C5",
    "tripSatisfactionCell": "C6",
    "tripsAssignedCell": "C8",
    "tripDropCell": "C9",
    "tripPickupCell": "C10",
    "tripCancelledCell": "C4", # Removed
    # Short Answer Questions
    "tripInvolvementCell": "C4",  # Removed
    "mainGoalCell": "C12",
    "interestedCategoriesCell": "C13",
    "threeLeadersCell": ["C15", "D15", "E15"],
    #"leadershipStyleCell": ["C15", "D15", "E15"], # MADE TO BE THE SAME SINCE IT WAS DELETED
    "additionalNotesCell": "B19",
    "numTrips": numTrips,
    "nameCellGuideStatus": "C3",  # The header cell
    "firstPromotionalCategoryCell": "D3",  # the last promotional category cell must have a blank column after it, that is the signal to stop
    "leaderGuideStatusFileName": "Data/TLPromotionStatus.xlsx",  # make sure to include the folder name
}
# example cell: 'B2', must start with letter and end with number
