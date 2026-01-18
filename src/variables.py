"""Configuration variables for TRiP-Light Excel cell mappings.

This module contains all Excel cell reference mappings used to extract data from
preference files and trip status files. Cell references use Excel notation (e.g., "B2")
and are converted to DataFrame indices by the utils module.
"""

from typing import Dict, Final, List, Union

# Constants for file processing
numTrips: Final[int] = 47
prefsSheetIndex: Final[int] = 1  # 1st sheet is 0, second sheet is 1
tripLeaderInfoIndex: Final[int] = 0
folderPath: Final[str] = "Data"

# Trip information cell mappings
# Maps semantic field names to Excel cell references in TripStatusInfo.xlsx
tripInfoDict: Dict[str, Union[str, int]] = {
    "datesCell": "B2",
    "tripCell": "C2",
    "tripCategoryCell": "D2",
    "tripStatusFileName": "Data/TripStatusInfo.xlsx",
    "numTrips": numTrips,
}

# Trip leader information cell mappings
# Maps semantic field names to Excel cell references in preference files
leaderInfoDict: Dict[str, Union[str, int, List[str]]] = {
    "leaderTripCell": "C2",
    "leaderPrefsCell": "E2",
    "nameCell": "C4",
    # Numerical Questions
    "semestersLeftCell": "C5",
    "tripSatisfactionCell": "C6",
    "tripsAssignedCell": "C8",
    "tripDropCell": "C9",
    "tripPickupCell": "C10",
    "tripCancelledCell": "C4",  # Removed
    # Short Answer Questions
    "tripInvolvementCell": "C4",  # Removed
    "mainGoalCell": "C12",
    "interestedCategoriesCell": "C13",
    "threeLeadersCell": ["C15", "D15", "E15"],
    "additionalNotesCell": "B19",
    "numTrips": numTrips,
    "nameCellGuideStatus": "C3",
    "firstPromotionalCategoryCell": "D3",
    "leaderGuideStatusFileName": "Data/TLPromotionStatus.xlsx",
}
