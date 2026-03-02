"""
Modern GUI for Flight Booking System using PyWebView.
Run this file to launch the application.
"""

import webview
import json
import os
from flight_system import System
from flights import Flight
from passenger import Passenger
from admin import Admin
import time

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.json")

# =========================================================
# Backend API – exposed to JavaScript via pywebview bridge
# =========================================================
class Api:
    """Bridge between the HTML/JS frontend and the Python backend."""

    def __init__(self):
        self.system = System()
        self.current_user = None
        if not self.system.load_from_json(DATA_FILE):
            self._seed_demo_data()
            self._save()

    # ----- helpers -----
    def _save(self):
        self.system.save_to_json(DATA_FILE)

    def _seed_demo_data(self):
        """Pre-populate some flights so the UI is not empty on first run."""
        demo_flights = [
            Flight("CA1001", "Beijing",    "Shanghai",   "2026-03-15 08:00", 120, "Airbus A319"),
            Flight("MU2045", "Guangzhou",  "Chengdu",    "2026-03-16 10:30", 150, "Airbus A320"),
            Flight("CZ3521", "Shenzhen",   "Hangzhou",   "2026-03-17 14:00", 80, "C909"),
            Flight("HU7890", "Shanghai",   "Beijing",    "2026-03-18 18:45", 220, "Boeing 787-9"),
            Flight("FM9101", "Chengdu",    "Kunming",    "2026-03-19 07:15", 120, "Boeing 737-700"),
        ]
        for f in demo_flights:
            self.system.add_flight(f)

        # Demo admin (level 3 – full permissions)
        demo_admin = Admin("admin", "Admin User", "admin@airline.com", "admin123", 3)
        self.system.register_user(demo_admin)

    # ---------- Auth ----------
    def register(self, username, name, email, password, role):
        """Register a new user. Returns JSON string."""
        # Check duplicate username
        for u in self.system.get_all_users():
            if u.get_username() == username:
                return json.dumps({"ok": False, "msg": "Username already exists"})
        if role == "admin":
            user = Admin(username, name, email, password, 3)
        else:
            user = Passenger(username, name, email, password)
        self.system.register_user(user)
        self.current_user = user
        self._save()
        return json.dumps({"ok": True, "msg": "Registration successful",
                           "role": user.display_role()})

    def login(self, username, password):
        for u in self.system.get_all_users():
            if u.get_username() == username and u.check_password(password):
                self.current_user = u
                return json.dumps({"ok": True, "role": u.display_role(),
                                   "name": u.get_name()})
        return json.dumps({"ok": False, "msg": "Invalid username or password"})

    def logout(self):
        self.current_user = None
        return json.dumps({"ok": True})

    def get_current_user(self):
        if self.current_user is None:
            return json.dumps({"ok": False})
        return json.dumps({
            "ok": True,
            "username": self.current_user.get_username(),
            "name": self.current_user.get_name(),
            "email": self.current_user.get_email(),
            "role": self.current_user.display_role(),
        })

    # ---------- Flights (read) ----------
    def get_flights(self):
        flights = self.system.get_all_flights()
        return json.dumps([self._flight_dict(f) for f in flights])

    def search_flights(self, keyword):
        flights = self.system.search_flight(keyword)
        return json.dumps([self._flight_dict(f) for f in flights])

    # ---------- Passenger actions ----------
    def book_flight(self, flight_number):
        if self.current_user is None:
            return json.dumps({"ok": False, "msg": "Not logged in"})
        msg = self.system.book_flight(self.current_user, flight_number)
        ok = msg == "Booking successful"
        time.sleep(0.1)
        if ok:
            self._save()
        return json.dumps({"ok": ok, "msg": msg})

    def cancel_booking(self, flight_number):
        if self.current_user is None:
            return json.dumps({"ok": False, "msg": "Not logged in"})
        msg = self.system.cancel_booking(self.current_user, flight_number)
        ok = msg == "Booking cancelled"
        if ok:
            self._save()
        return json.dumps({"ok": ok, "msg": msg})

    def get_my_bookings(self):
        if self.current_user is None:
            return json.dumps([])
        result = []
        for f in self.system.get_all_flights():
            if self.current_user in f.get_passenger_list():
                result.append(self._flight_dict(f))
        return json.dumps(result)

    # ---------- Admin actions ----------
    def add_flight(self, number, origin, dest, time, capacity, aircraft):
        if not self._is_admin():
            return json.dumps({"ok": False, "msg": "Permission denied"})
        flight = Flight(number, origin, dest, time, int(capacity), aircraft)
        msg = self.current_user.add_flight(self.system, flight)
        ok = msg == "Flight added successfully"
        if ok:
            self._save()
        return json.dumps({"ok": ok, "msg": msg})

    def remove_flight(self, flight_number):
        if not self._is_admin():
            return json.dumps({"ok": False, "msg": "Permission denied"})
        msg = self.current_user.remove_flight(self.system, flight_number)
        ok = msg == "Flight removed successfully"
        if ok:
            self._save()
        return json.dumps({"ok": ok, "msg": msg})

    def update_flight_time(self, flight_number, new_time):
        if not self._is_admin():
            return json.dumps({"ok": False, "msg": "Permission denied"})
        msg = self.current_user.update_flight_time(self.system, flight_number, new_time)
        ok = msg == "Flight time updated"
        if ok:
            self._save()
        return json.dumps({"ok": ok, "msg": msg})

    def get_flight_passengers(self, flight_number):
        if not self._is_admin():
            return json.dumps([])
        for f in self.system.get_all_flights():
            if f.get_flight_number() == flight_number:
                return json.dumps([
                    {"username": p.get_username(), "name": p.get_name(), "email": p.get_email()}
                    for p in f.get_passenger_list()
                ])
        return json.dumps([])

    # ---------- internal helpers ----------
    def _is_admin(self):
        return self.current_user is not None and self.current_user.display_role() == "Admin"

    @staticmethod
    def _flight_dict(f):
        return {
            "number": f.get_flight_number(),
            "origin": f.get_origin(),
            "destination": f.get_destination(),
            "departure": f.get_departure_time(),
            "aircraft": f.get_aircraft(),
            "seats": f.get_available_seats(),
        }



# =========================================================
# Application entry-point
# =========================================================
def main():
    api = Api()
    window = webview.create_window(
        title="SkyBooker – Flight Booking System",
        url="gui.html",
        js_api=api,
        width=1180,
        height=780,
        min_size=(900, 600),
    )
    webview.start(debug=False)


if __name__ == "__main__":
    main()
