"""Movie Database CLI."""
import os
import random
import statistics
import requests
from dotenv import load_dotenv
import movie_storage_sql as movie_storage

# Load environment variables
load_dotenv()

# Get the API Key securely
API_KEY = os.getenv("API_KEY")
API_URL = "http://www.omdbapi.com/"


def print_title():
    """Prints app title."""
    print("********** My Movies Database **********\n")


def print_menu():
    """Prints menu, gets user choice."""
    print("Menu:")
    print("0. Exit")
    print("1. List movies")
    print("2. Add movie")
    print("3. Delete movie")
    print("4. Update movie")
    print("5. Stats")
    print("6. Random movie")
    print("7. Search movie")
    print("8. Movies sorted by rating")
    print()
    return input("Enter choice (0-8): ").strip()


def _get_valid_string_input(prompt):
    """Loops until user enters non-empty string."""
    while True:
        user_input = input(prompt).strip()
        if user_input:
            return user_input
        print("Input cannot be empty. Please try again.")


def list_movies():
    """Prints all movies with year and rating from storage."""
    movies_by_title = movie_storage.list_movies()
    total_count = len(movies_by_title)
    print(f"\n{total_count} movie{'s' if total_count != 1 else ''} in total")
    for movie_title, movie_data in movies_by_title.items():
        print(f"{movie_title} ({movie_data['year']}): {movie_data['rating']:.1f}")
    print()


def add_movie():
    """Fetches movie data from OMDb API and adds to storage."""
    movie_title = _get_valid_string_input("\nEnter movie name: ")

    try:
        response = requests.get(API_URL, params={"apikey": API_KEY, "t": movie_title})
        response.raise_for_status()
        data = response.json()

        if data.get("Response") == "False":
            print(f"Error: {data.get('Error', 'Movie not found')}\n")
            return

        title = data.get("Title")
        year = int(data.get("Year"))
        rating = float(data.get("imdbRating", 0))
        poster = data.get("Poster", "N/A")

        movie_storage.add_movie(title, year, rating, poster)

    except requests.RequestException as e:
        print(f"API Connection Error: {e}\n")
    except ValueError:
        print("Error parsing movie data from API.\n")


def delete_movie():
    """Prompts user to delete movie from storage."""
    movies_by_title = movie_storage.list_movies()
    movie_title = _get_valid_string_input("\nEnter movie name to delete: ")
    if movie_title not in movies_by_title:
        print("Error: movie not found.\n")
        return
    movie_storage.delete_movie(movie_title)
    print(f"Deleted: {movie_title}\n")


def update_movie():
    """Prompts user to update movie rating in storage."""
    movies_by_title = movie_storage.list_movies()
    movie_title = _get_valid_string_input("\nEnter movie name to update: ")
    if movie_title not in movies_by_title:
        print("Error: movie not found.\n")
        return

    while True:
        try:
            new_rating = float(input("Enter new rating (1.0-10.0): ").strip())
            if 1.0 <= new_rating <= 10.0:
                break
            print("Error: Rating must be between 1.0 and 10.0.")
        except ValueError:
            print("Error: Invalid number.")

    movie_storage.update_movie(movie_title, new_rating)
    print(f"Updated: {movie_title} -> {new_rating:.1f}\n")


def stats():
    """Prints movie statistics from storage."""
    movies_by_title = movie_storage.list_movies()
    print()
    if not movies_by_title:
        print("No movies in database.\n")
        return

    all_ratings = [data["rating"] for data in movies_by_title.values()]
    average_rating = sum(all_ratings) / len(all_ratings)
    median_rating = statistics.median(all_ratings)
    max_rating_value = max(all_ratings)
    min_rating_value = min(all_ratings)

    best_titles = [t for t, d in movies_by_title.items() if d["rating"] == max_rating_value]
    worst_titles = [t for t, d in movies_by_title.items() if d["rating"] == min_rating_value]

    print(f"Average rating: {average_rating:.2f}")
    print(f"Median rating:  {median_rating:.2f}")
    print("Best movie(s):")
    for title in best_titles:
        print(f"- {title}: {max_rating_value:.1f}")
    print("Worst movie(s):")
    for title in worst_titles:
        print(f"- {title}: {min_rating_value:.1f}")
    print()


def random_movie():
    """Prints one random movie from storage."""
    movies_by_title = movie_storage.list_movies()
    print()
    if not movies_by_title:
        print("No movies in database.\n")
        return
    random_title = random.choice(list(movies_by_title.keys()))
    data = movies_by_title[random_title]
    print(f"{random_title} ({data['year']}), {data['rating']:.1f}\n")


def search_movie():
    """Prompts user for search, prints matches from storage."""
    movies_by_title = movie_storage.list_movies()
    search_query = _get_valid_string_input("\nEnter part of movie name: ").lower()

    matched = []
    for title, data in movies_by_title.items():
        if search_query in title.lower():
            matched.append((title, data))

    if not matched:
        print("No matches.\n")
        return

    for title, data in matched:
        print(f"{title} ({data['year']}), {data['rating']:.1f}")
    print()


def movies_sorted_by_rating():
    """Prints movies from storage sorted by rating, descending."""
    movies_by_title = movie_storage.list_movies()
    print()
    if not movies_by_title:
        print("No movies in database.\n")
        return

    # Sort descending by rating
    sorted_movies = sorted(
        movies_by_title.items(),
        key=lambda item: item[1]['rating'],
        reverse=True
    )

    for title, data in sorted_movies:
        print(f"{title} ({data['year']}): {data['rating']:.1f}")
    print()

def main():
    """Main function to run movie app."""
    print_title()
    while True:
        menu_choice = print_menu()
        print()

        if menu_choice == "0":
            print("Bye!")
            break
        if menu_choice == "1":
            list_movies()
        elif menu_choice == "2":
            add_movie()
        elif menu_choice == "3":
            delete_movie()
        elif menu_choice == "4":
            update_movie()
        elif menu_choice == "5":
            stats()
        elif menu_choice == "6":
            random_movie()
        elif menu_choice == "7":
            search_movie()
        elif menu_choice == "8":
            movies_sorted_by_rating()
        else:
            print("Invalid choice, please try again.\n")


if __name__ == "__main__":
    main()