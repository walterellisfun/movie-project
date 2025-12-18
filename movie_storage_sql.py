from sqlalchemy import create_engine, text

# Define the database URL
DB_URL = "sqlite:///movies.db"

# Create the engine
engine = create_engine(DB_URL, echo=False)  # Set echo=True for debugging

# Create the movies table if it does not exist
def setup_database():
    with engine.connect() as connection:
        connection.execute(text("""
            CREATE TABLE IF NOT EXISTS movies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT UNIQUE NOT NULL,
                year INTEGER NOT NULL,
                rating REAL NOT NULL
            )
        """))
        connection.commit()

# Initialize DB
setup_database()

def list_movies():
    """
    Retrieve all movies from the database.
    Returns a dictionary to match legacy format:
    { "Title": {"year": 2000, "rating": 8.5}, ... }
    """
    with engine.connect() as connection:
        result = connection.execute(text("SELECT title, year, rating FROM movies"))
        movies = result.fetchall()

    return {row[0]: {"year": row[1], "rating": row[2]} for row in movies}

def add_movie(title, year, rating):
    """Add a new movie to the database."""
    with engine.connect() as connection:
        try:
            connection.execute(
                text("INSERT INTO movies (title, year, rating) VALUES (:title, :year, :rating)"),
                {"title": title, "year": year, "rating": rating}
            )
            connection.commit()
        except Exception as e:
            print(f"Error adding movie: {e}")

def delete_movie(title):
    """Delete a movie from the database."""
    with engine.connect() as connection:
        try:
            connection.execute(
                text("DELETE FROM movies WHERE title = :title"),
                {"title": title}
            )
            connection.commit()
        except Exception as e:
            print(f"Error deleting movie: {e}")

def update_movie(title, rating):
    """Update a movie's rating in the database."""
    with engine.connect() as connection:
        try:
            connection.execute(
                text("UPDATE movies SET rating = :rating WHERE title = :title"),
                {"rating": rating, "title": title}
            )
            connection.commit()
        except Exception as e:
            print(f"Error updating movie: {e}")