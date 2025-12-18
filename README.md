# Movie Database App 🎥

A robust Command Line Interface (CLI) application for managing a personal movie collection. This project demonstrates the integration of **Python**, **SQL (SQLite)**, **External APIs (OMDb)**, and **Static Web Generation**.

## 🚀 Features

* **Database Storage:** Utilizes a persistent **SQLite** database managed via **SQLAlchemy** for efficient and scalable data handling.
* **OMDb API Integration:** Automatically fetches movie details (Year, Rating, Poster URL) by just entering the title.
* **CRUD Operations:** Create, Read, Update, and Delete movies from the database.
* **Data Analytics:** View statistics like average rating, median rating, and best/worst movies.
* **Website Generator:** Generates a visual HTML/CSS portfolio of your movie collection with a single command.
* **Search & Sort:** Filter movies by name or sort them by rating.

## 🛠️ Tech Stack

* **Language:** Python 3.x
* **Database:** SQLite3
* **ORM:** SQLAlchemy
* **API:** OMDb (Open Movie Database)
* **Libraries:** `requests`, `python-dotenv`

## 📦 Installation

1.  **Clone the repository**
    ```bash
    git clone https://github.com/YOUR_USERNAME/movie-database-app.git
    cd movie-database-app
    ```

2.  **Install Dependencies**
    ```bash
    pip install sqlalchemy requests python-dotenv
    ```

3.  **Get an API Key**
    * Sign up for a free API key at [OMDb API](http://www.omdbapi.com/apikey.aspx).

4.  **Configure Environment**
    * Create a file named `.env` in the root directory.
    * Add your API key:
        ```text
        API_KEY=your_actual_api_key_here
        ```

## 🖥️ Usage

Run the main application script:

```bash
python3 main.py
```
### Menu Options

* **List movies:** Displays all movies currently in the database.
* **Add movie:** Enter a title (e.g., "Matrix") -> The app fetches data from OMDb and saves it.
* **Delete movie:** Remove a movie by title.
* **Update movie:** Manually update the rating of a movie.
* **Stats:** Show average/median ratings and highest/lowest rated films.
* **Generate website:** Creates an `index.html` file in the `_static` folder to visualize your collection.

## 📂 Project Structure

```text
├── main.py              # Main application entry point (CLI Menu)
├── movie_storage_sql.py   # Database handling (SQLAlchemy layer)
├── movies.db              # SQLite database (Created automatically)
├── .env                   # Environment variables (API Key) - Not committed to Git
├── .gitignore             # Git ignore rules
└── _static/
    ├── index_template.html # HTML Template for website generation
    ├── style.css          # CSS styling for the website
    └── index.html         # The generated website (Output)
```