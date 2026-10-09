import json
from pathlib import Path  # Standard library class for platform-independent file path handling


class BookingMovie:
    """Represents a single movie ticket booking with validated fields."""

    def __init__(self, movie_name: str, customer_name: str, number_tickets: int) -> None:
        """
        Initialize a BookingMovie instance with validation via property setters.

        Args:
            movie_name (str): The name of the booked movie.
            customer_name (str): The name of the customer booking tickets.
            number_tickets (int): The quantity of tickets reserved.
        """
        # Property setters are triggered automatically during initialization to validate input values
        self.movie_name: str = movie_name
        self.customer_name: str = customer_name
        self.number_tickets: int = number_tickets

    # --- MOVIE NAME PROPERTY ---
    @property
    def movie_name(self) -> str:
        """Get the private movie name attribute."""
        return self.__movie_name

    @movie_name.setter
    def movie_name(self, movie_name: str) -> None:
        """Set and validate the movie name via the static validation method."""
        self.__movie_name: str = self.validate_name(movie_name)

    # --- CUSTOMER NAME PROPERTY ---
    @property
    def customer_name(self) -> str:
        """Get the private customer name attribute."""
        return self.__customer_name

    @customer_name.setter
    def customer_name(self, customer_name: str) -> None:
        """Set and validate the customer name via the static validation method."""
        self.__customer_name: str = self.validate_name(customer_name)

    # --- STATIC VALIDATION METHODS ---
    @staticmethod
    def validate_name(name: str) -> str:
        """
        Validate strings for customer or movie names against length and character constraints.

        Args:
            name (str): The name string to be validated.

        Returns:
            str: Cleaned and validated string.

        Raises:
            ValueError: If string length is under 2 characters or contains unsupported symbols.
        """
        cleaned_movie_name: str = name.strip()
        if len(cleaned_movie_name) < 2:
            raise ValueError("Name cannot be shorter than 2 characters!")

        # Allowed symbols include alphanumeric characters, spaces, and basic punctuation marks
        if not all(char.isalnum() or char in " -,.`'" for char in cleaned_movie_name):
            raise ValueError("Name must contain only letters, numbers, or standard punctuation!")
        return cleaned_movie_name

    # --- NUMBER OF TICKETS PROPERTY ---
    @property
    def number_tickets(self) -> int:
        """Get the private ticket quantity attribute."""
        return self.__number_tickets

    @number_tickets.setter
    def number_tickets(self, number_tickets: int) -> None:
        """Set and validate the ticket quantity."""
        self.__number_tickets: int = self.validate_number_tickets(number_tickets)

    @staticmethod
    def validate_number_tickets(num_tickets: int) -> int:
        """
        Ensure ticket count is a non-negative integer.

        Args:
            num_tickets (int): Number of tickets.

        Returns:
            int: Validated ticket count.

        Raises:
            ValueError: If ticket number is less than 0.
        """
        if num_tickets < 0:
            raise ValueError("Number of tickets cannot be negative!")
        return num_tickets

    def __str__(self) -> str:
        """Return a user-friendly string representation of the booking object."""
        return f"Customer={self.customer_name}, Movie={self.movie_name}, Tickets={self.number_tickets}"

    # --- FACTORY CREATION METHOD ---
    @staticmethod
    def create_new_booking() -> "BookingMovie | None":
        """
        Interactively collect and validate user inputs to construct a new BookingMovie object.

        Returns:
            BookingMovie | None: Created BookingMovie instance or None if cancelled by pressing Enter.
        """
        # Step 1: Prompt for Movie Name
        while True:
            try:
                selected_mov: str = input("(Movie name)> ")
                if not selected_mov:
                    print("Creation cancelled.")
                    return None

                BookingMovie.validate_name(selected_mov)
                break
            except ValueError as e:
                print(f"Error: {e}")

        # Step 2: Prompt for Customer Name
        while True:
            try:
                name_customer: str = input("Enter customer name> ")
                if not name_customer:
                    print("Creation cancelled.")
                    return None
                BookingMovie.validate_name(name_customer)
                break
            except ValueError as e:
                print(f"Error: {e}")

        # Step 3: Prompt for Ticket Count
        while True:
            try:
                num_tickets_str: str = input("Enter number of tickets> ")
                if not num_tickets_str:
                    print("Creation cancelled.")
                    return None

                num_tickets: int = int(num_tickets_str)
                BookingMovie.validate_number_tickets(num_tickets)
                break
            except ValueError as e:
                print(f"Error: {e}. Please enter a valid number.")

        return BookingMovie(selected_mov, name_customer, num_tickets)

    @staticmethod
    def calculate_discount(price: float, discount_percent: float) -> float:
        """Calculate discounted ticket price."""
        return price * (1 - discount_percent / 100)


class BookingManager:
    """Manages the collection of active bookings and handles JSON file storage operations."""

    def __init__(self) -> None:
        """Initialize the manager with default file path and load existing JSON data."""
        self.path_json_booking: Path = Path("booking.json")
        self.list_customer: list[BookingMovie] = self.read_booking_list_from_json()

    def __str__(self) -> str:
        """Return newline-separated string representation of all managed bookings."""
        return "\n".join(str(c) for c in self.list_customer)

    def __repr__(self) -> str:
        """Return developer-facing representation of internal list."""
        return repr(self.list_customer)

    def save_booking_list_to_json(self) -> None:
        """Serialize the list of BookingMovie objects into JSON format and write to disk."""
        data: list[dict[str, str | int]] = [
            {
                "customer_name": c.customer_name,
                "movie_name": c.movie_name,
                "number_tickets": c.number_tickets,
            }
            for c in self.list_customer
        ]

        with open(self.path_json_booking, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def read_booking_list_from_json(self) -> list[BookingMovie]:
        """
        Load and parse JSON file data into a list of BookingMovie objects.

        Returns:
            list[BookingMovie]: Restored list of booking instances.
        """
        list_cus: list[BookingMovie] = []
        if not self.path_json_booking.exists():
            return []

        try:
            with open(self.path_json_booking, "r", encoding="utf-8") as file:
                customer_file: list[dict[str, str | int]] = json.load(file)

            for c in customer_file:
                # Instantiate BookingMovie ensuring positional parameters match constructor (movie_name, customer_name, number_tickets)
                cus: BookingMovie = BookingMovie(
                    movie_name=str(c["movie_name"]),
                    customer_name=str(c["customer_name"]),
                    number_tickets=int(c["number_tickets"]),
                )
                list_cus.append(cus)
            return list_cus
        except (json.JSONDecodeError, KeyError):
            return []

    def add_customer(self, booking: BookingMovie) -> None:
        """
        Append a new booking to memory and update persistent JSON storage.

        Args:
            booking (BookingMovie): The new booking instance to store.
        """
        self.list_customer.append(booking)
        self.save_booking_list_to_json()

    def get_user_booking(self, name_customer: str) -> list[BookingMovie]:
        """
        Find and return all active bookings registered under a specific customer name (case-insensitive).

        Args:
            name_customer (str): Search parameter name.

        Returns:
            list[BookingMovie]: Filtered list containing customer bookings.
        """
        list_user: list[BookingMovie] = []
        validated_name: str = BookingMovie.validate_name(name_customer)

        for booking in self.list_customer:
            if booking.customer_name.lower() == validated_name.lower():
                list_user.append(booking)
        return list_user

       def cancel_booking(self) -> str | None:
        """
        Interactive workflow allowing a user to cancel a specific booking by movie title and name.

        Returns:
            str | None: Cancellation confirmation message or None if cancelled.
        """
        while True:
            try:
                name_user: str = input("Enter customer name to cancel (or press Enter to return): ").strip()
                if not name_user:
                    print("Cancellation rejected.")
                    return None

                BookingMovie.validate_name(name_user)

                user_bookings: list[BookingMovie] = []
                for b in self.list_customer:
                    if b.customer_name.lower() == name_user.lower():
                        user_bookings.append(b)

                if not user_bookings:
                    print(f"No active bookings found for '{name_user}'. Please try again.")
                    continue

                print("\nActive bookings for this user:")
                for b in user_bookings:
                    print(f"- {b}")

                name_mov: str = input("\nEnter film name to cancel (or press Enter to return): ").strip()
                if not name_mov:
                    print("Cancellation rejected.")
                    return None

                BookingMovie.validate_name(name_mov)

                for booking in self.list_customer:
                    if booking.customer_name.lower() == name_user.lower() and booking.movie_name.lower() == name_mov.lower():
                        # Restore tickets count back to film_list.json
                        movies.OperationMovies.calculate_available_tickets(name_mov, -booking.number_tickets)

                        self.list_customer.remove(booking)
                        self.save_booking_list_to_json()
                        return f"Booking for '{name_user}' with movie '{name_mov}' successfully cancelled."

                print(f"No movie matching '{name_mov}' was found for this user.")
                return None

            except ValueError as e:
                print(f"Error: {e}")
                continue
