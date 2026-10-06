import json
from pathlib import Path  # Corrected import for standard file paths


class BookingMovie:
    """Represents a single movie ticket booking with validated fields."""

    def __init__(self, movie_name: str, customer_name: str, number_tickets: int) -> None:
        """Initialize BookingMovie instance."""
        self.movie_name: str = movie_name
        self.customer_name: str = customer_name
        self.number_tickets: int = number_tickets

    @property
    def movie_name(self) -> str:
        """Get the movie name."""
        return self.__movie_name

    @movie_name.setter
    def movie_name(self, movie_name: str) -> None:
        """Set and validate the movie name."""
        self.__movie_name: str = self.validate_name(movie_name)

    @property
    def customer_name(self) -> str:
        """Get the customer name."""
        return self.__customer_name

    @customer_name.setter
    def customer_name(self, customer_name: str) -> None:
        """Set and validate the customer name."""
        self.__customer_name: str = self.validate_name(customer_name)

    @staticmethod
    def validate_name(name: str) -> str:
        """Validate customer or movie name string constraints."""
        cleaned_movie_name: str = name.strip()
        if len(cleaned_movie_name) < 2:
            raise ValueError("Name cannot be shorter than 2 characters!")
        # Added space ' ' to allowed characters to support multi-word titles and names
        if not all(char.isalnum() or char in ' -,.`\'' for char in cleaned_movie_name):
            raise ValueError("Name must contain only letters or numbers!")
        return cleaned_movie_name.strip()

    @property
    def number_tickets(self) -> int:
        """Get the number of tickets."""
        return self.__number_tickets

    @number_tickets.setter
    def number_tickets(self, number_tickets: int) -> None:
        """Set and validate the number of tickets."""
        self.__number_tickets: int = self.validate_number_tickets(number_tickets)

    @staticmethod
    def validate_number_tickets(num_tickets: int) -> int:
        """Validate ticket count ensuring it is non-negative."""
        if num_tickets < 0:
            raise ValueError("Number of tickets cannot be negative!")
        return num_tickets

    def __str__(self) -> str:
        """Return a user-friendly string representation of the booking."""
        return f"Name customer={self.customer_name}, movie={self.movie_name}, ticket={self.number_tickets}"

    @staticmethod
    def create_new_booking() -> None | BookingMovie:
        while True:
            try:
                selected_mov = input("(Movies name)> ")
                if not selected_mov:
                    print("Creation cancelled.")
                    return None

                BookingMovie.validate_name(selected_mov)
                break

            except Exception as e:
                print(e)
        while True:
            try:
                name_customer = input("Enter the name of the customer who will book the film> ")

                if not name_customer:
                    print("Creation cancelled.")
                    return None
                BookingMovie.validate_name(name_customer)
                break

            except Exception as e:
                print(e)
        while True:
            try:
                num_tickets = input("Enter the number of tickets you would like to book> ")

                if not num_tickets:
                    print("Creation cancelled.")
                    return None
                BookingMovie.validate_number_tickets(int(num_tickets))
                break

            except Exception as e:
                print(e)
        new_cus = BookingMovie(selected_mov, name_customer, int(num_tickets))
        return new_cus


class BookingManager:
    """Manages the collection of bookings and handles JSON persistence."""

    def __init__(self) -> None:
        """Initialize BookingManager and load existing bookings from file."""
        self.path_json_booking: Path = Path('booking.json')
        self.list_customer: list[BookingMovie] = self.read_booking_list_from_json()

    def __str__(self) -> str:
        return "\n".join(str(c) for c in self.list_customer)

    def save_booking_list_to_json(self) -> None:
        """Save the current list of bookings to a JSON file."""
        data: list[dict[str, str | int]] = [
            {
                "customer_name": c.customer_name,
                "movie_name": c.movie_name,
                "number_tickets": c.number_tickets
            } for c in self.list_customer
        ]

        # Fixed encoding to 'utf-8'
        with open(self.path_json_booking, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def read_booking_list_from_json(self) -> list[BookingMovie]:
        """Read and parse bookings from the JSON file."""
        list_cus: list[BookingMovie] = []
        if not self.path_json_booking.exists():
            return []

        try:
            # Fixed encoding to 'utf-8' and wrapped load operation inside try block
            with open(self.path_json_booking, 'r', encoding='utf-8') as file:
                customer_file: list[dict[str, str | int]] = json.load(file)

            for c in customer_file:
                # Corrected arguments order matching BookingMovie init (movie_name, customer_name, number_tickets)
                cus: BookingMovie = BookingMovie(str(c['movie_name']), str(c['customer_name']),
                                                 int(c['number_tickets']))
                list_cus.append(cus)
            return list_cus
        except (json.JSONDecodeError, KeyError):
            return []

    def add_customer(self, booking: BookingMovie) -> None:
        """Add a new booking to the list and save changes to JSON."""
        self.list_customer.append(booking)
        self.save_booking_list_to_json()

    def get_user_booking(self, name_customer: str) -> list[BookingMovie]:
        """Retrieve all bookings associated with a specific customer name."""
        list_user: list[BookingMovie] = []
        name_customer = BookingMovie.validate_name(name_customer)
        for name_c in self.list_customer:
            if name_c.customer_name.lower() == name_customer.strip().lower():
                list_user.append(name_c)
        return list_user
