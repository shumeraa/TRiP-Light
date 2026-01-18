"""TripLeader and TripLeaderManager classes for managing trip leader data.

This module defines the TripLeader class representing individual trip leaders with
their preferences and survey responses, plus TripLeaderManager for coordinating
all trip leader data.
"""

import math
from typing import Any, Dict, List, Optional, Tuple, Union

from utils import reformat_cells


class TripLeader:
    """Represents a trip leader with preferences and survey responses.

    Attributes:
        name: Leader's name (lowercase, stripped).
        prefs: List of trip preference rankings (integers or None for unavailable).
        semestersLeft: Number of semesters remaining.
        tripSatisfaction: Satisfaction rating for past trips.
        tripsAssigned: Number of trips assigned.
        tripDropped: Number of trips dropped.
        tripPickedUp: Number of trips picked up.
        tripCancelled: Number of trips cancelled.
        tripInvolvement: Text response about trip involvement.
        mainGoal: Leader's main goal text.
        interestedCategories: Categories of interest.
        threeLeaders: Three other leaders mentioned.
        additionalNotes: Additional notes from leader.
        guideStatus: Dictionary mapping trip categories to guide status (0=AG, 1=LG).
    """

    def __init__(
        self,
        name: str,
        prefs: List[Union[int, float, str, None]],
        # Numerical Questions
        semestersLeft: Union[int, float],
        tripSatisfaction: Union[int, float],
        tripsAssigned: Union[int, float],
        tripDropped: Union[int, float],
        tripPickedUp: Union[int, float],
        tripCancelled: Union[int, float],
        # Short Answer Questions
        tripInvolvement: str,
        mainGoal: str,
        interestedCategories: str,
        threeLeaders: str,
        additionalNotes: str,
    ) -> None:
        """Initialize a TripLeader instance.

        Args:
            name: Leader's name.
            prefs: List of preference rankings or None for unavailable trips.
            semestersLeft: Semesters remaining in school.
            tripSatisfaction: Trip satisfaction rating.
            tripsAssigned: Number of trips assigned.
            tripDropped: Number of trips dropped.
            tripPickedUp: Number of trips picked up.
            tripCancelled: Number of trips cancelled.
            tripInvolvement: Text response about trip involvement.
            mainGoal: Leader's main goal.
            interestedCategories: Categories the leader is interested in.
            threeLeaders: Three other leaders the leader wants to work with.
            additionalNotes: Any additional notes from the leader.
        """
        self.guideStatus: Dict[str, int] = {}  # Added after instantiation
        self.name = name
        self.prefs = prefs
        self.semestersLeft = semestersLeft
        self.tripSatisfaction = tripSatisfaction
        self.tripsAssigned = tripsAssigned
        self.tripDropped = tripDropped
        self.tripPickedUp = tripPickedUp
        self.tripCancelled = tripCancelled
        self.tripInvolvement = tripInvolvement
        self.mainGoal = mainGoal
        self.interestedCategories = interestedCategories
        self.threeLeaders = threeLeaders
        self.additionalNotes = additionalNotes

    def __repr__(self) -> str:
        """Return a string representation of the TripLeader."""
        prefs_str = ", ".join(map(str, self.prefs))
        guide_status_str = ", ".join(f"{k}: {v}" for k, v in self.guideStatus.items())
        return (
            f"TripLeader(name={self.name}, prefs=[{prefs_str}], "
            f"guideStatus={{ {guide_status_str} }}, "
            f"semestersLeft={self.semestersLeft}, "
            f"tripSatisfaction={self.tripSatisfaction}, "
            f"tripsAssigned={self.tripsAssigned}, tripDropped={self.tripDropped}, "
            f"tripPickedUp={self.tripPickedUp}, tripCancelled={self.tripCancelled}, "
            f"tripInvolvement={self.tripInvolvement}, mainGoal={self.mainGoal}, "
            f"interestedCategories={self.interestedCategories}, "
            f"threeLeaders={self.threeLeaders}, "
            f"additionalNotes={self.additionalNotes})"
        )

    def categorize_prefs(
        self,
    ) -> List[Tuple[Union[int, float, str, None], str]]:
        """Categorize preferences into bottom, middle, and top thirds.

        Filters out NaN values, sorts the remaining preferences, and divides them
        into three equal groups. Each preference is returned with its category label.

        Returns:
            List of tuples (preference_value, category_label) where category_label
            is one of: "bottom third", "middle third", "top third", or "nan".

        Examples:
            If prefs are [5, 1, 3, 2, 4], sorted becomes [1, 2, 3, 4, 5].
            Bottom third: [1], Middle: [2, 3], Top: [4, 5]
        """
        if not self.prefs:
            return []

        # Filter out NaN values and sort the remaining preferences
        sorted_prefs = sorted(
            [
                pref
                for pref in self.prefs
                if not (isinstance(pref, float) and math.isnan(pref))
            ]
        )
        length = len(sorted_prefs)

        if length == 0:
            return [(pref, "nan") for pref in self.prefs]

        # Divide into thirds based on sorted order
        bottom_third = sorted_prefs[: length // 3]
        middle_third = sorted_prefs[length // 3 : 2 * length // 3]
        top_third = sorted_prefs[2 * length // 3 :]

        # Categorize each original preference
        categorized_prefs = []
        for pref in self.prefs:
            if isinstance(pref, float) and math.isnan(pref):
                categorized_prefs.append((pref, "nan"))
            elif pref in bottom_third:
                categorized_prefs.append((pref, "bottom third"))
            elif pref in middle_third:
                categorized_prefs.append((pref, "middle third"))
            elif pref in top_third:
                categorized_prefs.append((pref, "top third"))

        return categorized_prefs


class TripLeaderManager:
    """Manages a collection of trip leaders and cell mapping configuration.

    The TripLeaderManager coordinates trip leader data by storing TripLeader objects
    and managing cell mappings that define where to find leader information in Excel.

    Attributes:
        trip_leaders: Dictionary mapping leader names to TripLeader objects.
        cell_mappings: Dictionary mapping field names to DataFrame indices.
    """

    def __init__(self, cell_mappings: Dict[str, Any]) -> None:
        """Initialize TripLeaderManager with cell mappings.

        Args:
            cell_mappings: Dictionary mapping field names to Excel cell references.
                          All values are converted from Excel notation to DataFrame
                          indices via reformat_cells().
        """
        self.trip_leaders: Dict[str, TripLeader] = {}
        self.cell_mappings: Dict[str, Any] = {
            key: reformat_cells(value) for key, value in cell_mappings.items()
        }

    def add_trip_leader(self, trip_leader: TripLeader) -> None:
        """Add a trip leader to the manager.

        Args:
            trip_leader: TripLeader object to add. Indexed by leader name.
        """
        self.trip_leaders[trip_leader.name] = trip_leader

    def get_all_trip_leaders(self) -> List[TripLeader]:
        """Get all trip leaders managed by this TripLeaderManager.

        Returns:
            List of all TripLeader objects.
        """
        return list(self.trip_leaders.values())

    def find_trip_leader(self, name: str) -> Optional[TripLeader]:
        """Find a trip leader by name.

        Args:
            name: Leader name to search for (case-sensitive).

        Returns:
            TripLeader object if found, None otherwise.
        """
        return self.trip_leaders.get(name, None)
