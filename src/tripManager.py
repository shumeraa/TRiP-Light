from datetime import datetime
from utils import reformat_cells_manager


class Trip:
    def __init__(self, name: str, date, category):
        if not name:
            raise ValueError("Trip name cannot be empty")
        elif not isinstance(name, str):
            raise ValueError(f"Trip name '{name}' must be a string")

        self.name = name

        # Check if the date is a datetime object
        if isinstance(date, datetime):
            self.date = date.strftime(
                "%m/%d/%Y"
            )  # Format to only include the date part
        elif isinstance(date, str):
            self.date = date  # If it's a string, store it as is
        else:
            raise ValueError(
                f"Trip date for '{name}' must be either an excel datetime or a string"
            )

        if not category:
            raise ValueError(f"Trip category for '{name}' cannot be empty")
        elif not isinstance(category, str):
            raise ValueError(f"Trip category for '{name}' must be a string")
        self.category = category

    def __repr__(self):
        return f"Trip(name={self.name}, date={self.date}, category={self.category})"


class TripManager:
    def __init__(self, cell_mappings, trips=None):
        self.trips = trips if trips is not None else []

        self.cell_mappings = {}

        for key, value in cell_mappings.items():
            # if it is an int, do not convert it
            # this is for values like numTrips
            if isinstance(value, int):
                self.cell_mappings[key] = value
            else:
                self.cell_mappings[key] = reformat_cells_manager(value)

    def add_trip(self, name: str, date, category):
        trip = Trip(name, date, category)
        if trip not in self.trips:
            self.trips.append(trip)
        else:
            print("Trip already exists in the list.")

    def get_trips(self):
        return self.trips

    def get_available_categories(self):
        return list(set([trip.category for trip in self.trips]))
