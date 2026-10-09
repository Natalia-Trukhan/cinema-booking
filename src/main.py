from movies import Movie, OperationMovies
from src.booking import BookingMovie, BookingManager
from src.movies import FavoriteManager

# temporary test string
def prime() -> None:
    """Main execution entry point displaying interactive menu and controlling app logic."""

    # Pre-populate sample movies list
    movie_1: Movie = Movie(
        title="Inception",
        director="Christopher Nolan",
        year=2010,
        genre=["Sci-Fi", "Action", "Thriller"],
        description="A thief who steals corporate secrets through dream-sharing technology.",
        duration=148,
    )

    movie_2: Movie = Movie(
        title="The Shawshank Redemption",
        director="Frank Darabont",
        year=1994,
        genre=["Drama"],
        description="Two convicts form a deep friendship over several years seeking redemption.",
        duration=142,
    )

    movie_3: Movie = Movie(
        title="Interstellar",
        director="Christopher Nolan",
        year=2014,
        genre=["Sci-Fi", "Drama", "Adventure"],
        description="Explorers travel through a space wormhole to save humanity.",
        duration=169,
    )

    movie_4: Movie = Movie(
        title="The Matrix",
        director="Lana Wachowski",
        year=1999,
        genre=["Sci-Fi", "Action"],
        description="A computer hacker learns about the true nature of his reality.",
        duration=136,
    )

    movie_5: Movie = Movie(
        title="Dune",
        director="Denis Villeneuve",
        year=2021,
        genre=["Sci-Fi", "Adventure"],
        description="A noble family becomes embroiled in a galactic resource war.",
        duration=155,
    )

    print("\n--- Welcome! Available Movies ---")
    list_of_movies: list[Movie] = [movie_1, movie_2, movie_3, movie_4, movie_5]
    add_movie: OperationMovies = OperationMovies(list_of_movies)
    favor_manager: FavoriteManager = FavoriteManager(add_movie)
    print(add_movie)

    # Main Application Loop
    while True:
        # Loop for reliable user choice validation
        while True:
            try:
                print("""
    Select an option from the list:
        1 - Add a film
        2 - Search a film
        3 - Display all films
        4 - Delete a film
        5 - Book tickets
        6 - Check booking 
        7 - Cancel booking
        8 - Add to favorites 
        9 - Remove from favorites
        10 - calculate discount
        11 - Exit
                """)
                user_input: str = input("> ").strip()
                if not user_input.isdigit():
                    raise ValueError("Input must be a valid integer number!")

                option: int = int(user_input)
                if option < 1 or option > 11:
                    raise ValueError("Invalid option range! Must be between 1 and 11.")
                break
            except ValueError as e:
                print(f"Error: {e}")

        # Action Handler based on user selected menu option
        match option:
            case 1:
                new_film: Movie | None = OperationMovies.create_new_film()
                if new_film:
                    add_movie.add_movie(new_film)
                    print("Movie successfully added!")

            case 2:
                while True:
                    search_mov: str = input("Enter film or director to search (or press Enter to cancel): ").strip()
                    if not search_mov:
                        break

                    results: list[Movie] = add_movie.search_film(search_mov)
                    if results:
                        print("\nFound movies:")
                        for movie in results:
                            print(movie)
                        break
                    else:
                        print(f"'{search_mov}' not found. Please try again!\n")

            case 3:
                print("\nList of all available movies:")
                print(add_movie)

            case 4:
                while True:
                    try:
                        delete_film: str = input(
                            "Enter film name or director to delete (or press Enter to cancel): "
                        ).strip()
                        if not delete_film:
                            break
                        add_movie.delete_film_from_json(delete_film)
                        print("Movie deleted successfully.")
                        break
                    except Exception as e:
                        print(f"Error: {e}")

            case 5:
                print("\nAvailable movies for booking:")
                print(add_movie)
                print()

                book_manager: BookingManager = BookingManager()
                new_book: BookingMovie | None = BookingMovie.create_new_booking()

                if new_book:
                    book_manager.add_customer(new_book)
                    list_custom: list[BookingMovie] = book_manager.get_user_booking(new_book.customer_name)
                    print("\nYour updated booking details:")
                    for booking in list_custom:
                        print(booking)

            case 6:
                while True:
                    print()
                    try:
                        name_cus: str = input(
                            "Enter customer name to search active bookings (or press Enter to return): "
                        ).strip()

                        if not name_cus:
                            break

                        book_manager: BookingManager = BookingManager()
                        list_cus: list[BookingMovie] = book_manager.get_user_booking(name_cus)

                        if list_cus:
                            print(f"\nActive booking details for '{name_cus}':")
                            for booking in list_cus:
                                print(booking)
                            break
                        else:
                            print(f"No bookings found for '{name_cus}'.")
                            continue

                    except Exception as e:
                        print(f"Error: {e}")
                        continue

            case 7:
                cancel_manager: BookingManager = BookingManager()
                cancellation_result: str | None = cancel_manager.cancel_booking()
                if cancellation_result:
                    print(cancellation_result)

            case 8:
                favor_manager.add_favorite_film_to_json()
            case 9:
                favor_manager.delete_favorite_film_from_json()
            case 10:

                try:
                    while True:
                        price: float | str = input("Enter price (or press Enter to stop): ")
                        if not price:
                            break
                        price: float = float(price)
                        if price <= 0:
                            print("Price must be greater than 0!")
                            continue
                        if price > 0:
                            break

                    if price:

                        while True:
                            discount_percent: float | str = input(
                                "Enter discount percentage (or press Enter to stop): ")
                            if not discount_percent:
                                break
                            discount_percent: float = float(discount_percent)
                            if discount_percent <= 0:
                                print("Discount percentage must be greater than 0!")
                                continue
                            if discount_percent > 0:
                                break
                        if price and discount_percent:
                            discount = BookingMovie.calculate_discount(price, discount_percent)
                            print(f"Discounted price: {discount}")

                except ValueError:
                    print("Error: Please enter valid numeric values!")
                except Exception as e:
                    print(f"Error: {e}")
            case 11:
                print("Finished! Exiting application.")
                break
            case _:
                print("Invalid option selected.")
                continue


if __name__ == "__main__":
    prime()
