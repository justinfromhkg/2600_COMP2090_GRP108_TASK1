class Flight:
    def __init__(self, flight_number, origin, 
                 destination, departure_time, capacity, aircraft, flight_date):
        # encapsulation
        self._flight_number = flight_number
        self._origin = origin
        self._destination = destination
        self._departure_time = departure_time
        self._capacity = capacity
        self._booked_passengers = []
        self._aircraft = aircraft
        self._flight_date = flight_date

    # -------------------------
    # Getter methods
    # -------------------------
    def get_flight_number(self):
        return self._flight_number

    def get_origin(self):
        return self._origin

    def get_destination(self):
        return self._destination

    def get_departure_time(self):
        return self._departure_time

    def get_available_seats(self):
        return self._capacity - len(self._booked_passengers)

    def get_passenger_list(self):
        return self._booked_passengers
    
    def get_aircraft(self):
        return self._aircraft

    def get_flight_date(self):
        return self._flight_date

    # -------------------------
    # Setter
    # -------------------------
    def set_flight_number(self, new_number):
        self._flight_number = new_number

    def set_departure_time(self, new_time):
        self._departure_time = new_time

    def set_origin(self, new_origin):
        self._origin = new_origin

    def set_destination(self, new_dest):
        self._destination = new_dest

    def update_capacity(self, new_capacity):
        if new_capacity < len(self._booked_passengers):
            return "Cannot reduce capacity below current bookings"
        self._capacity = new_capacity
        return "Capacity updated"

    def set_aircraft(self, new_aircraft):
        self._aircraft = new_aircraft

    def set_flight_date(self, new_date):
        self._flight_date = new_date

    # -------------------------
    # Booking logic
    # -------------------------
    def get_passenger_list(self):
        return self._booked_passengers
    
    def add_passenger(self, passenger):
        if self.get_available_seats() > 0:
            self._booked_passengers.append(passenger)
            return True
        return False

    def remove_passenger(self, passenger):
        if passenger in self._booked_passengers:
            self._booked_passengers.remove(passenger)
            return True
        return False

    def get_capacity(self):
        return self._capacity

    def to_dict(self):
        return {
            "flight_number": self._flight_number,
            "origin": self._origin,
            "destination": self._destination,
            "departure_time": self._departure_time,
            "capacity": self._capacity,
            "aircraft": self._aircraft,
            "flight_date": self._flight_date,
            "booked_passengers": [p.get_username() for p in self._booked_passengers],
        }

    @classmethod
    def from_dict(cls, data, users_map):
        flight = cls(
            data["flight_number"],
            data["origin"],
            data["destination"],
            data["departure_time"],
            data["capacity"],
            data["aircraft"],
            data.get("flight_date", ""),
        )
        for username in data.get("booked_passengers", []):
            if username in users_map:
                flight._booked_passengers.append(users_map[username])
        return flight

    def __str__(self):
        return (f"Flight: {self._flight_number} | "
                f"{self._origin} → {self._destination} | "
                f"Departure: {self._departure_time} | "
                f"Available Seats: {self.get_available_seats()}")