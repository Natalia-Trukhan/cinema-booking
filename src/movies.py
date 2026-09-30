import json
from pathlib import Path


class Movie:
    """Represents a movie entity with properties and validation rules."""

    def __init__(self, title: str, director: str, year: int, genre: list[str], description: str, duration: int) -> None:
        self.title: str = title
        self.director: str = director
        self.year: int = year
        self.genre: list[str] = genre
        self.description: str = description
        self.duration: int = duration

    # --- Title Property & Validation ---
    @property
    def title(self) -> str:
        """Get the title of the movie."""
        return self.__title

    @title.setter
    def title(self, title: str) -> None:
        """Set and validate the title of the movie."""
        self.__title: str = self.validate_title(title)

    @staticmethod
    def validate_title(title: str) -> str:
        """Validate movie title string constraints."""
        cleaned_title: str = title.strip()
        if not cleaned_title:
            raise ValueError("Title cannot be empty!")
        if len(cleaned_title) < 2:
            raise ValueError("Title must be at least 2 characters long!")
        if not any(letter.isalnum() for letter in cleaned_title):
            raise ValueError("Title must contain letters or numbers!")
        return title

    # --- Director Property & Validation ---
    @property
    def director(self) -> str:
        """Get the director of the movie."""
        return self.__director

    @director.setter
    def director(self, director: str) -> None:
        """Set and validate the director of the movie."""
        self.__director: str = self.validate_director(director)

    @staticmethod
    def validate_director(director: str) -> str:
        """Validate director name string constraints."""
        cleaned_director: str = director.strip()
        if not cleaned_director:
            raise ValueError("Director cannot be empty!")
        if len(cleaned_director) < 2:
            raise ValueError("Director name must be at least 2 characters long!")
        if not all(letter.isalpha() or letter in " -,.'" for letter in cleaned_director):
            raise ValueError("Director name contains invalid characters!")
        return director

    # --- Year Property & Validation ---
    @property
    def year(self) -> int:
        """Get the release year of the movie."""
        return self.__year

    @year.setter
    def year(self, year: int) -> None:
        """Set and validate the release year of the movie."""
        self.__year: int = self.validate_year(year)

    @staticmethod
    def validate_year(year: int) -> int:
        """Validate release year integer constraints."""
        if type(year) != int:
            raise ValueError("Year can be an integer only!")
        if year < 1895:
            raise ValueError("Year cannot be earlier than 1895 (invention of cinema)!")
        return year

    # --- Genre Property & Validation ---
    @property
    def genre(self) -> list[str]:
        """Get the genres list of the movie."""
        return self.__genre

    @genre.setter
    def genre(self, genre: list[str]) -> None:
        """Set and validate the genres list of the movie."""
        self.__genre: list[str] = self.validate_genre(genre)

    @staticmethod
    def validate_genre(genre: list[str]) -> list[str]:
        """Validate list of genres constraints."""
        if not genre:
            raise ValueError("Genre cannot be empty!")
        if not all(char.isalpha() or char in " ,-" for gen in genre for char in gen):
            raise ValueError("Genre must contain only letters, spaces, and hyphens allowed!")
        if not all(len(gen) >= 2 for gen in genre):
            raise ValueError("Genre must contain at least 2 characters long!")
        return genre

    # --- Description Property & Validation ---
    @property
    def description(self) -> str:
        """Get the description of the movie."""
        return self.__description

    @description.setter
    def description(self, description: str) -> None:
        """Set and validate the description of the movie."""
        self.__description: str = self.validate_description(description)

    @staticmethod
    def validate_description(description: str) -> str:
        """Validate description string constraints."""
        if not description:
            raise ValueError("Description cannot be empty!")
        if len(description) < 2:
            raise ValueError("Description must be at least 2 characters long!")
        return description

    # --- Duration Property & Validation ---
    @property
    def duration(self) -> int:
        """Get the duration of the movie in minutes."""
        return self.__duration

    @duration.setter
    def duration(self, duration: int) -> None:
        """Set and validate the duration of the movie."""
        self.__duration: int = self.validate_duration(duration)

    @staticmethod
    def validate_duration(duration: int) -> int:
        """Validate duration integer constraints."""
        if type(duration) != int:
            raise ValueError("Duration can be an integer only!")
        if duration <= 0:
            raise ValueError("Duration must be larger than 0!")
        return duration

    def __str__(self) -> str:
        """Return formatted string representation of the movie."""
        return f"Title={self.title}, director={self.director}, year={self.year}, genre={self.genre}, description={self.description}, duration={self.duration}"

    def __eq__(self, other: object) -> bool:
        """Check equality between two Movie objects."""
        if not isinstance(other, Movie):
            return NotImplemented
        return (self.title == other.title and self.director == other.director and
                self.duration == other.duration and self.description == other.description
                and self.genre == other.genre and self.year == other.year)

    def __hash__(self) -> int:
        """Return hash value for storing Movie object in sets or dictionary keys."""
        return hash((self.title, self.director, self.duration, self.description, tuple(self.genre), self.year))


class AddFilmToList:
    """Manages collection of movies, JSON persistence, and user operations."""

    def __init__(self, list_movies: list[Movie]) -> None:
        self.json_file: Path = Path("film_json.json")
        self.list_movies: list[Movie] = self.read_from_json()

        # Initialize JSON file with default movies if storage is empty
        if not self.list_movies and list_movies:
            self.list_movies = list_movies
            self.load_to_json()

    def add_movie(self, movie: Movie) -> None:
        """Append a new movie to the collection and save to JSON file."""
        self.list_movies.append(movie)
        self.load_to_json()

    def __str__(self) -> str:
        """Return all movies in the collection separated by newlines."""
        return "\n".join(str(mov) for mov in self.list_movies)

    @staticmethod
    def create_new_film() -> Movie | None:
        """Prompt user interactively to collect inputs and instantiate a new Movie object."""
        while True:
            try:
                title: str = input("Title: ")
                if not title:
                    print("Creation cancelled.")
                    return None
                Movie.validate_title(title)
                break
            except Exception as e:
                print(e)
        while True:
            try:
                director: str = input("Director: ")
                if not director:
                    print("Creation cancelled.")
                    return None
                Movie.validate_director(director)
                break
            except Exception as e:
                print(e)
        while True:
            try:
                year_move: str = input("Year: ")
                if not year_move:
                    print("Creation cancelled.")
                    return None
                year: int = int(year_move)
                Movie.validate_year(year)
                break
            except Exception as e:
                print(e)

        while True:
            try:
                genre: str = input("Genre(fiction, romance, etc): ")
                if not genre:
                    print("Creation cancelled.")
                    return None
                list_genres: list[str] = genre.split(',')
                new_list_genres: list[str] = [gen.strip() for gen in list_genres]
                Movie.validate_genre(new_list_genres)
                break
            except Exception as e:
                print(e)
        while True:
            try:
                description: str = input("Description: ")
                if not description:
                    print("Creation cancelled.")
                    return None
                Movie.validate_description(description)
                break
            except Exception as e:
                print(e)
        while True:
            try:
                duration_film: str = input("Duration (minutes): ")
                if not duration_film:
                    print("Creation cancelled.")
                    return None
                duration: int = int(duration_film)
                Movie.validate_duration(duration)
                break
            except Exception as e:
                print(e)
        return Movie(title=title, director=director, year=year, genre=new_list_genres,
                     description=description,
                     duration=duration)

    def search_film(self, name_of_film: str) -> list[Movie]:
        """Search movies matching title or director substring."""
        searched_movies: list[Movie] = []
        for mov in self.list_movies:
            if name_of_film.lower() in mov.title.lower() or name_of_film.lower() in mov.director.lower():
                searched_movies.append(mov)
        return searched_movies

    def load_to_json(self) -> None:
        """Save current movie collection list into a JSON file."""
        data_films: list[dict[str, object]] = [
            {
                "title": film.title,
                "director": film.director,
                "year": film.year,
                "genre": film.genre,
                "description": film.description,
                "duration": film.duration
            }
            for film in self.list_movies
        ]

        with open(self.json_file, "w", encoding="utf-8") as file:
            json.dump(data_films, file, ensure_ascii=False, indent=4)

    def read_from_json(self) -> list[Movie]:
        """Load and parse existing movies list from JSON file."""
        list_film: list[Movie] = []
        if not self.json_file.exists():
            return []

        try:
            with open(self.json_file, "r", encoding="utf-8") as file:
                read_file: list[dict[str, object]] = json.load(file)
            for film in read_file:
                movie: Movie = Movie(title=str(film["title"]), director=str(film["director"]), year=int(film["year"]), genre=list(film["genre"]),
                                    description=str(film["description"]), duration=int(film["duration"]))
                list_film.append(movie)
        except (json.JSONDecodeError, KeyError):
            return []
        return list_film

    def delete_film_from_json(self, name_film: str) -> None:
        """Delete selected movie from collection and update JSON file."""
        while True:
            list_film_for_delete: list[Movie] = []

            for film in self.list_movies:
                if name_film.lower() in film.title.lower() or name_film.lower() in film.director.lower():
                    list_film_for_delete.append(film)

            if not list_film_for_delete:
                print(f"Name {name_film} not found.")
                name_film = input(
                    "Enter the name of the film or name of director to delete(or press Enter to cancel): ")
                continue

            if not name_film:
                break

            if list_film_for_delete:
                for index, film in enumerate(list_film_for_delete):
                    print(f"{index} - {film}")
                try:
                    index_to_delete: str = input("Enter number of film to delete: ")
                    if not index_to_delete:
                        break
                    film_to_delete: Movie = list_film_for_delete[int(index_to_delete)]
                except Exception:
                    print("Wrong number! Try again.")
                    continue

                for f in self.list_movies:
                    if f == film_to_delete:
                        self.list_movies.remove(f)
                        break

                self.load_to_json()
                print("The movie was successfully deleted.")
                break
            else:
                break


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
    add_movie: AddFilmToList = AddFilmToList(list_of_movies)
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
            5 - to exit
            """)
                print()
                option: int = int(input("> "))
                if type(option) != int:
                    raise ValueError("Invalid option! Must be between 1 to 5!")
                if option < 1 or option > 5:
                    raise ValueError("Invalid option! Must be between 1 to 5!")
                break
            except Exception as e:
                print(e)

        match option:
            case 1:
                new_film: Movie | None = AddFilmToList.create_new_film()
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
                print("Finished!")
                break
            case _:
                print("Invalid option.")
                continue


if __name__ == "__main__":
    prime()