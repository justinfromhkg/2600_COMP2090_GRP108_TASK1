import json
import os
from flights import Flight
from passenger import Passenger
from admin import Admin


class System:

    def __init__(self):
        self._flights = []
        self._users = []

    # -------------------------
    # User Management
    # -------------------------
    def register_user(self, user):
        self._users.append(user)
        return "User registered successfully"

    def get_all_users(self):
        return self._users

    # -------------------------
    # Flight Management
    # -------------------------
    def add_flight(self, flight):
        self._flights.append(flight)
        return "Flight added successfully"

    def remove_flight(self, flight_number, departure_time):
        for flight in self._flights:
            if flight.get_flight_number() == flight_number and flight.get_departure_time() == departure_time:
                self._flights.remove(flight)
                return "Flight removed successfully"
        return "Flight not found"

    def get_all_flights(self):
        return self._flights

    def search_flight(self, keyword):
        result = []
        for flight in self._flights:
            if (keyword.lower() in flight.get_flight_number().lower()
                    or keyword.lower() in flight.get_origin().lower()
                    or keyword.lower() in flight.get_destination().lower()):
                result.append(flight)
        return result

    def update_flight_time(self, flight_number, departure_time, new_time):
        for flight in self._flights:
            if flight.get_flight_number() == flight_number and flight.get_departure_time() == departure_time:
                flight.set_departure_time(new_time)
                return "Flight time updated"
        return "Flight not found"

    # -------------------------
    # Booking Logic
    # -------------------------
    def book_flight(self, passenger, flight_number, departure_time):
        for flight in self._flights:
            if flight.get_flight_number() == flight_number and flight.get_departure_time() == departure_time:
                if passenger in flight.get_passenger_list():
                    return "You have booked the flight already"
                if flight.add_passenger(passenger):
                    return "Booking successful"
                return "No available seats"
        return "Flight not found"

    def cancel_booking(self, passenger, flight_number, departure_time):
        for flight in self._flights:
            if flight.get_flight_number() == flight_number and flight.get_departure_time() == departure_time:
                if flight.remove_passenger(passenger):
                    return "Booking cancelled"
                return "Passenger not booked on this flight"

        return "Flight not found"

    # -------------------------
    # JSON Persistence
    # -------------------------
    def save_to_json(self, filepath):
        data = {
            "users": [u.to_dict() for u in self._users],
            "flights": [f.to_dict() for f in self._flights],
        }
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def load_from_json(self, filepath):
        if not os.path.exists(filepath):
            return False
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        self._users = []
        users_map = {}
        for u in data.get("users", []):
            if u["type"] == "Admin":
                user = Admin.from_dict(u)
            else:
                user = Passenger.from_dict(u)
            self._users.append(user)
            users_map[user.get_username()] = user

        self._flights = []
        for fd in data.get("flights", []):
            flight = Flight.from_dict(fd, users_map)
            self._flights.append(flight)

        return True
