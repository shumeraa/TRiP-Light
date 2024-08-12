from datetime import datetime


class Trip:
    def __init__(self, name: str, date: datetime):
        if not name:
            raise ValueError("Trip name cannot be empty")
        if not isinstance(date, datetime):
            raise ValueError("Date must be a datetime object")
        self.name = name
        self.date = date

    def __repr__(self):
        return f"Trip(name={self.name}, date={self.date})"


class TripManager:
    def __init__(self, trips=None):
        self.trips = trips if trips is not None else []

    def add_trip(self, name: str, date: datetime):
        trip = Trip(name, date)
        if trip not in self.trips:
            self.trips.append(trip)
        else:
            print("Trip already exists in the list.")

    def get_trips(self):
        return self.trips

    def get_trips_by_date(self):
        return sorted(self.trips, key=lambda trip: trip.date)



