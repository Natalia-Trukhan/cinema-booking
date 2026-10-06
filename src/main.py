from movies import Movie, OperationMovies
from src.booking import BookingMovie, BookingManager


def prime() -> None:
    """Main execution function displaying menu and controlling program flow."""
    # 1. Inception
    movie_1: Movie = Movie(
        title="Inception",
        director="Christopher Nolan",
        year=2010,
        genre=["Sci-Fi", "Action", "Thriller"],
        description="A thief who steals corporate secrets through the use of dream-sharing technology.",
        duration=148
    )

    # 2. The Shawshank Redemption
    movie_2: Movie = Movie(
        title="The Shawshank Redemption",
        director="Frank Darabont",
        year=1994,
        genre=["Drama"],
        description="Over the course of several years, two convicts form a friendship, seeking solace and eventual redemption.",
        duration=142
    )

    # 3. Interstellar
    movie_3: Movie = Movie(
        title="Interstellar",
        director="Christopher Nolan",
        year=2014,
        genre=["Sci-Fi", "Drama", "Adventure"],
        description="A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival.",
        duration=169
    )

    # 4. The Matrix
    movie_4: Movie = Movie(
        title="The Matrix",
        director="Lana Wachowski",
        year=1999,
        genre=["Sci-Fi", "Action"],
        description="A computer hacker learns from mysterious rebels about the true nature of his reality.",
        duration=136
    )

    # 5. Dune
    movie_5: Movie = Movie(
        title="Dune",
        director="Denis Villeneuve",
        year=2021,
        genre=["Sci-Fi", "Adventure"],
        description="A noble family becomes embroiled in a war for control over the galaxy's most valuable asset.",
        duration=155
    )

    print("""
Here you can see all our films:
    """)
    list_of_movies: list[Movie] = [movie_1, movie_2, movie_3, movie_4, movie_5]
    add_movie: OperationMovies = OperationMovies(list_of_movies)
    print(add_movie)
    while True:
        while True:
            try:
                print("""
        Select one options:
            1 - to add a film
            2 - to search film
            3 - to see all films
            4 - to delete fim
            5 - to book tickets
            6 - to cancel booking tickets
            7 - to exit
            """)
                print()
                option: int = int(input("> "))
                if type(option) != int:
                    raise ValueError("Invalid option! Must be between 1 to 7!")
                if option < 1 or option > 7:
                    raise ValueError("Invalid option! Must be between 1 to 7!")
                break
            except Exception as e:
                print(e)

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
                print(add_movie)
            case 4:
                while True:
                    try:
                        delete_film: str = input(
                            "Enter the name of the film or name of director to delete (or press Enter to cancel): ")
                        if not delete_film:
                            break
                        add_movie.delete_film_from_json(delete_film)
                        break
                    except Exception as e:
                        print(e)

            case 5:
                print("Select movie to book from the list:")
                print(add_movie)
                print()

                book_manager = BookingManager()
                new_book = BookingMovie.create_new_booking()

                if new_book:
                    book_manager.add_customer(new_book)
                    list_custom = book_manager.get_user_booking(new_book.customer_name)
                    print("\nYour booking details:")
                    for booking in list_custom:
                        print(booking)

                while True:
                    print()
                    try:
                        name_cus = input(
                            "Enter customer name to search active bookings (or press Enter to return to menu): "
                        ).strip()

                        if not name_cus:
                            break

                        list_cus = book_manager.get_user_booking(name_cus)

                        if list_cus:
                            print(f"\nBooking details for '{name_cus}':")
                            for booking in list_cus:
                                print(booking)
                        else:
                            print(f"No bookings found for '{name_cus}'.")
                            continue


                    except Exception as e:
                        print(f"Error: {e}")
                        continue

            case 7:
                print("Finished!")
                break
            case _:
                print("Invalid option.")
                continue


if __name__ == "__main__":
    prime()
