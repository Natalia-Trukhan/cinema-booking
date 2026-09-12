from shlex import join


class Movie:
    def __init__(self, title: str, director: str, year: int, genre: list[str], description: str, duration: int) -> None:
        self.title = title
        self.director = director
        self.year = year
        self.genre = genre
        self.description = description
        self.duration = duration

    @property
    def title(self) -> str:
        return self.__title

    @title.setter
    def title(self, title: str) -> None:
        self.__title = self.validate_title(title)

    @staticmethod
    def validate_title(title: str) -> str:
        cleaned_title = title.strip()
        if not cleaned_title:
            raise ValueError("Title cannot be empty!")
        if len(cleaned_title) < 2:
            raise ValueError("Title must be at least 2 characters long!")
        if not any(letter.isalnum() for letter in cleaned_title):
            raise ValueError("Title must contain letters or numbers!")
        return cleaned_title

    @property
    def director(self) -> str:
        return self.__director

    @director.setter
    def director(self, director: str) -> None:
        self.__director = self.validate_director(director)

    @staticmethod
    def validate_director(director: str) -> str:
        cleaned_director = director.strip()
        if not cleaned_director:
            raise ValueError("Director cannot be empty!")
        if len(cleaned_director) < 2:
            raise ValueError("Director name must be at least 2 characters long!")
        if not all(letter.isalpha() or letter in " -,.'" for letter in cleaned_director):
            raise ValueError("Director name contains invalid characters!")
        return cleaned_director

    @property
    def year(self) -> int:
        return self.__year

    @year.setter
    def year(self, year: int) -> None:
        self.__year = self.validate_year(year)

    @staticmethod
    def validate_year(year: int) -> int:
        if type(year) != int:
            raise ValueError("Year can be an integer only!")
        if year < 1895:
            raise ValueError("Year cannot be earlier than 1895 (invention of cinema)!")
        return year

    @property
    def genre(self) -> list[str]:
        return self.__genre

    @genre.setter
    def genre(self, genre: list[str]) -> None:
        self.__genre = self.validate_genre(genre)

    @staticmethod
    def validate_genre(genre: list[str]) -> list[str]:
        if not genre:
            raise ValueError("Genre cannot be empty!")
        if not all(char.isalpha() or char in " ,-" for gen in genre for char in gen):
            raise ValueError("Genre must contain only letters, spaces, and hyphens allowed!")
        if not all(len(gen) >= 2 for gen in genre):
            raise ValueError("Genre must contain at least 2 characters long!")
        return genre

    @property
    def description(self) -> str:
        return self.__description

    @description.setter
    def description(self, description: str) -> None:
        self.__description = self.validate_description(description)

    @staticmethod
    def validate_description(description: str) -> str:
        if not description:
            raise ValueError("Description cannot be empty!")
        if len(description) < 2:
            raise ValueError("Description must be at least 2 characters long!")
        return description

    @property
    def duration(self) -> int:
        return self.__duration

    @duration.setter
    def duration(self, duration: int) -> None:
        self.__duration = self.validate_duration(duration)

    @staticmethod
    def validate_duration(duration: int) -> int:
        if type(duration) != int:
            raise ValueError("Duration can be an integer only!")
        if duration <= 0:
            raise ValueError("Duration must be larger than 0!")
        return duration

    def __str__(self) -> str:
        return f"Title={self.title}, director={self.director}, year={self.year}, genre={self.genre}, description={self.description}, duration={self.duration}"


class AddFilmToList:
    def __init__(self, list_movies: list[Movie]) -> None:
        self.list_movies = list_movies

    def add_movie(self, movie: Movie) -> None:
        self.list_movies.append(movie)

    def __str__(self) -> str:
        return "\n".join(str(mov) for mov in self.list_movies)

    @staticmethod
    def create_new_film() -> Movie:
        while True:
            try:
                title: str = input("Title: ")
                Movie.validate_title(title)
                break
            except Exception as e:
                print(e)
        while True:
            try:
                director: str = input("Director: ")
                Movie.validate_director(director)
                break
            except Exception as e:
                print(e)
        while True:
            try:
                year: int = int(input("Year: "))
                Movie.validate_year(year)
                break
            except Exception as e:
                print(e)
        while True:
            try:
                genre: str = input("Genre(fiction, romance, etc): ")
                list_genres: list[str] = genre.split(',')
                new_list_genres: list[str] = [gen.strip() for gen in list_genres]
                Movie.validate_genre(new_list_genres)
                break
            except Exception as e:
                print(e)
        while True:
            try:
                description: str = input("Description: ")
                Movie.validate_description(description)
                break
            except Exception as e:
                print(e)
        while True:
            try:
                duration: int = int(input("Duration (minutes): "))
                Movie.validate_duration(duration)
                break
            except Exception as e:
                print(e)
        return Movie(title=title, director=director, year=year, genre=new_list_genres, description=description,
                     duration=duration)

    def search_film(self, name_of_film) -> Movie | str:
        for mov in self.list_movies:
            if mov.title.lower() == name_of_film.lower():
                searched_film = mov
                return searched_film
        return f"{name_of_film} not found."


def prime():
    # 1. Inception
    movie_1 = Movie(
        title="Inception",
        director="Christopher Nolan",
        year=2010,
        genre=["Sci-Fi", "Action", "Thriller"],
        description="A thief who steals corporate secrets through the use of dream-sharing technology.",
        duration=148
    )

    # 2. The Shawshank Redemption
    movie_2 = Movie(
        title="The Shawshank Redemption",
        director="Frank Darabont",
        year=1994,
        genre=["Drama"],
        description="Over the course of several years, two convicts form a friendship, seeking solace and eventual redemption.",
        duration=142
    )

    # 3. Interstellar
    movie_3 = Movie(
        title="Interstellar",
        director="Christopher Nolan",
        year=2014,
        genre=["Sci-Fi", "Drama", "Adventure"],
        description="A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival.",
        duration=169
    )

    # 4. The Matrix
    movie_4 = Movie(
        title="The Matrix",
        director="Lana Wachowski",
        year=1999,
        genre=["Sci-Fi", "Action"],
        description="A computer hacker learns from mysterious rebels about the true nature of his reality.",
        duration=136
    )

    # 5. Dune
    movie_5 = Movie(
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
    list_of_movies = [movie_1, movie_2, movie_3, movie_4, movie_5]
    add_movie = AddFilmToList(list_of_movies)
    print(add_movie)
    while True:
        while True:
            try:
                print("""
        Select one options:
            1 - to add a film
            2 - to search film
            3 - to see all films
            4 - to exit
            """)
                print()
                option: int = int(input("> "))
                if type(option) != int:
                    raise ValueError("Invalid option! Must be between 1 to 4!")
                if option < 1 or option > 4:
                    raise ValueError("Invalid option! Must be between 1 to 4!")
                break
            except Exception as e:
                print(e)

        match option:
                case 1:
                    new_film = AddFilmToList.create_new_film()
                    add_movie.add_movie(new_film)
                case 2:
                    search_mov = input("Enter the name of the film to search for: ")
                    print(add_movie.search_film(search_mov))
                case 3:
                    print(add_movie)
                case 4:
                    print("Finished!")
                    break
                case _:
                    print("Invalid option.")
                    continue

if __name__ == "__main__":
    prime()
