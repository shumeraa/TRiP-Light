from datetime import datetime
from functions import excel_to_df_indices

class Trip:
    def __init__(self, name: str, date):
        if not name:
            raise ValueError("Trip name cannot be empty")
        self.name = name

        # Check if the date is a datetime object
        if isinstance(date, datetime):
            self.date = date.strftime(
                "%m/%d/%Y"
            )  # Format to only include the date part
        elif isinstance(date, str):
            self.date = date  # If it's a string, store it as is
        else:
            raise ValueError("Date must be either a datetime object or a string")

    def __repr__(self):
        return f"Trip(name={self.name}, date={self.date})"


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
                self.cell_mappings[key] = excel_to_df_indices(value)

    def add_trip(self, name: str, date):
        trip = Trip(name, date)
        if trip not in self.trips:
            self.trips.append(trip)
        else:
            print("Trip already exists in the list.")

    def get_trips(self):
        return self.trips
