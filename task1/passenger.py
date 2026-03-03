from person import Person



class Passenger(Person):

    def __init__(self, username, name, email, password):
        super().__init__(username, name, email, password)

    # Polymorphism
    def display_role(self):
        return "Passenger"

    def __str__(self):
        return (f"Role: {self.display_role()}\n"
                f"Username: {self.get_username()}\n"
                f"Name: {self.get_name()}\n"
                f"Email: {self.get_email()}")

    def to_dict(self):
        return {
            "type": "Passenger",
            "username": self.get_username(),
            "name": self.get_name(),
            "email": self.get_email(),
            "password_hash": self.get_password_hash(),
        }

    @classmethod
    def from_dict(cls, data):
        passenger = cls.__new__(cls)
        Person.__init__(passenger, data["username"], data["name"], data["email"], "placeholder")
        passenger.set_password_hash(data["password_hash"])
        return passenger

    # -------------------------
    # Functionalities
    # -------------------------

    def search_flight(self, system, keyword):
        return system.search_flight(keyword)

    def book_flight(self, system, flight_number):
        return system.book_flight(self, flight_number)

    def cancel_booking(self, system, flight_number):
        return system.cancel_booking(self, flight_number)