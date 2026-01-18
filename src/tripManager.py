"""Trip and TripManager classes for managing trip information.

This module defines the Trip class representing individual trips and TripManager
for coordinating trip data loaded from Excel files.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from utils import reformat_cells


class Trip:
    """Represents a single trip with name, date, and category.

    Attributes:
        name: The name/title of the trip.
        date: Trip date formatted as MM/DD/YYYY string.
        category: Trip category (e.g., "Overnight", "Biking", "Surfing").
    """

    def __init__(self, name: str, date: Union[datetime, str], category: str) -> None:
        """Initialize a Trip instance.

        Args:
            name: Trip name, must be a non-empty string.
            date: Trip date as either a datetime object or date string.
            category: Trip category, must be a non-empty string.

        Raises:
            ValueError: If name is empty, not a string, date format is invalid,
                       or category is empty or not a string.
        """
        if not name:
            raise ValueError("Trip name cannot be empty")
        elif not isinstance(name, str):
            raise ValueError(f"Trip name '{name}' must be a string")

        self.name: str = name

        # Check if the date is a datetime object
        if isinstance(date, datetime):
            self.date: str = date.strftime("%m/%d/%Y")
        elif isinstance(date, str):
            self.date = date
        else:
            raise ValueError(
                f"Trip date for '{name}' must be either an excel datetime or a string"
            )

        if not category:
            raise ValueError(f"Trip category for '{name}' cannot be empty")
        elif not isinstance(category, str):
            raise ValueError(f"Trip category for '{name}' must be a string")
        self.category: str = category

    def __repr__(self) -> str:
        """Return a string representation of the Trip."""
        return f"Trip(name={self.name}, date={self.date}, category={self.category})"


class TripManager:
    """Manages a collection of trips and cell mapping configuration.

    The TripManager coordinates trip data by storing Trip objects and managing
    cell mappings that define where to find trip information in Excel files.

    Attributes:
        trips: List of Trip objects.
        cell_mappings: Dictionary mapping semantic field names to DataFrame indices.
    """

    def __init__(
        self, cell_mappings: Dict[str, Any], trips: Optional[List[Trip]] = None
    ) -> None:
        """Initialize TripManager with cell mappings and optional trip list.

        Args:
            cell_mappings: Dictionary mapping field names to Excel cell references.
                          Values can be strings (e.g., "B2"), integers, or lists.
            trips: Optional initial list of Trip objects. Defaults to empty list.
        """
        self.trips: List[Trip] = trips if trips is not None else []
        self.cell_mappings: Dict[str, Any] = {}

        for key, value in cell_mappings.items():
            # Don't convert integers (e.g., numTrips) - keep as-is
            if isinstance(value, int):
                self.cell_mappings[key] = value
            else:
                self.cell_mappings[key] = reformat_cells(value)

    def add_trip(self, name: str, date: Union[datetime, str], category: str) -> None:
        """Add a new trip to the manager if it doesn't already exist.

        Args:
            name: Trip name.
            date: Trip date as datetime object or string.
            category: Trip category.
        """
        trip = Trip(name, date, category)
        if trip not in self.trips:
            self.trips.append(trip)
        else:
            print("Trip already exists in the list.")

    def get_trips(self) -> List[Trip]:
        """Get all trips managed by this TripManager.

        Returns:
            List of all Trip objects.
        """
        return self.trips

    def get_available_categories(self) -> List[str]:
        """Get unique list of all trip categories.

        Returns:
            List of unique category strings from all trips.
        """
        return list(set([trip.category for trip in self.trips]))
