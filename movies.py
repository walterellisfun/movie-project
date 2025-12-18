"""Movie Database CLI."""
import random
import statistics
import movie_storage
import datetime


def print_title():
    """Prints app title."""
    print("********** My Movies Database **********\n")


def print_menu():
    """
    Prints menu, gets user choice.

    Returns:
        str: User's menu choice.
    """
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


def _get_valid_float_input(prompt, min_val, max_val):
    """Loops until user enters valid float in range."""
    while True:
        try:
            user_input = input(prompt).strip()
            value = float(user_input)
            if min_val <= value <= max_val:
                return value
            print(f"Error: Rating must be between {min_val} and {max_val}.")
        except ValueError:
            print(f"Error: '{user_input}' is not a valid number.")


def _get_valid_int_input(prompt, min_val, max_val):
    """Loops until user enters valid int in range."""
    while True:
        try:
            user_input = input(prompt).strip()
            value = int(user_input)
            if min_val <= value <= max_val:
                return value
            print(f"Error: Year must be between {min_val} and {max_val}.")
        except ValueError:
            print(f"Error: '{user_input}' is not a valid year.")


def list_movies():
    """Prints all movies with year and rating from storage."""
    movies_by_title = movie_storage.get_movies()
    total_count = len(movies_by_title)
    print(f"\n{total_count} movie{'s' if total_count != 1 else ''} in total")
    for movie_title, movie_data in movies_by_title.items():
        print(f"{movie_title} ({movie_data['year']}): {movie_data['rating']:.1f}")
    print()


def add_movie():
    """Prompts user to add new movie to storage."""
    movies_by_title = movie_storage.get_movies()
    movie_title = _get_valid_string_input("\nEnter movie name: ")
    if movie_title in movies_by_title:
        print("Error: movie already exists.\n")
        return

    movie_rating = _get_valid_float_input("Enter rating (1.0-10.0): ", 1.0, 10.0)
    current_year = datetime.datetime.now().year
    movie_year = _get_valid_int_input(f"Enter year (1888-{current_year + 1}): ", 1888, current_year + 1)
    movie_storage.add_movie(movie_title, movie_year, movie_rating)
    print(f"Added: {movie_title} ({movie_year}) with rating {movie_rating:.1f}\n")


def delete_movie():
    """Prompts user to delete movie from storage."""
    movies_by_title = movie_storage.get_movies()
    movie_title = _get_valid_string_input("\nEnter movie name to delete: ")
    if movie_title not in movies_by_title:
        print("Error: movie not found.\n")
        return
    movie_storage.delete_movie(movie_title)
    print(f"Deleted: {movie_title}\n")


def update_movie():
    """Prompts user to update movie rating in storage."""
    movies_by_title = movie_storage.get_movies()
    movie_title = _get_valid_string_input("\nEnter movie name to update: ")
    if movie_title not in movies_by_title:
        print("Error: movie not found.\n")
        return
    new_rating = _get_valid_float_input("Enter new rating (1.0-10.0): ", 1.0, 10.0)
    movie_storage.update_movie(movie_title, new_rating)
    print(f"Updated: {movie_title} -> {new_rating:.1f}\n")


def stats():
    """Prints movie statistics from storage."""
    movies_by_title = movie_storage.get_movies()
    print()
    if not movies_by_title:
        print("No movies in database.\n")
        return

    all_ratings = [data["rating"] for data in movies_by_title.values()]
    average_rating = sum(all_ratings) / len(all_ratings)
    median_rating = statistics.median(all_ratings)

    max_rating_value = max(all_ratings)
    min_rating_value = min(all_ratings)

    best_titles = []
    for title, data in movies_by_title.items():
        if data["rating"] == max_rating_value:
            best_titles.append(title)

    worst_titles = []
    for title, data in movies_by_title.items():
        if data["rating"] == min_rating_value:
            worst_titles.append(title)

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
    movies_by_title = movie_storage.get_movies()
    print()
    if not movies_by_title:
        print("No movies in database.\n")
        return
    all_titles = list(movies_by_title.keys())
    random_title = random.choice(all_titles)
    movie_data = movies_by_title[random_title]
    print(f"{random_title} ({movie_data['year']}), {movie_data['rating']:.1f}\n")


def search_movie():
    """Prompts user for search, prints matches from storage."""
    movies_by_title = movie_storage.get_movies()
    search_query_lower = _get_valid_string_input("\nEnter part of movie name: ").lower()
    matched_titles = []
    for title, data in movies_by_title.items():
        if search_query_lower in title.lower():
            matched_titles.append((title, data))

    if not matched_titles:
        print("No matches.\n")
        return

    for title, data in matched_titles:
        print(f"{title} ({data['year']}), {data['rating']:.1f}")
    print()


def movies_sorted_by_rating():
    """Prints movies from storage sorted by rating, descending."""
    movies_by_title = movie_storage.get_movies()
    print()
    if not movies_by_title:
        print("No movies in database.\n")
        return

    remaining_items = list(movies_by_title.items())
    sorted_by_rating_desc = []

    # Sort: descending by rating, then ascending by title
    while remaining_items:
        current_best_index = 0
        current_best_title, current_best_data = remaining_items[0]
        current_best_rating = current_best_data["rating"]
        idx = 1
        while idx < len(remaining_items):
            title, data = remaining_items[idx]
            rating = data["rating"]
            should_take = (rating > current_best_rating) or (
                rating == current_best_rating and title < current_best_title
            )
            if should_take:
                current_best_index = idx
                current_best_title = title
                current_best_rating = rating
            idx += 1
        sorted_by_rating_desc.append(remaining_items.pop(current_best_index))

    for title, data in sorted_by_rating_desc:
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
