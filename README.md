# TMDb Horror Movie Scraper

This Python script searches for horror movies using The Movie Database (TMDb) API and saves the results to a CSV file. It utilizes the `requests` library to interact with the TMDb API and fetches horror movies based on their genre ID.

## Features

- Searches for horror movies using the TMDb API
- Saves the retrieved movie titles to a CSV file
- Handles pagination to retrieve all available horror movies
- Provides error handling for failed API requests

## Prerequisites

- Python 3.x
- `requests` library
- TMDb API key

## Installation

1. Clone the repository:
2. git clone https://github.com/your-username/tmdb-horror-movie-scraper.git
3. Obtain a TMDb API key from [TMDb](https://www.themoviedb.org/documentation/api) and replace `api_key` in the script with your key.

## Usage

1. Run the script:
2. python tmdb_scraper.py
2. The script will search for horror movies using the TMDb API and save the results to a CSV file named `horror_movies.csv`.
3. Once completed, you can find the list of horror movies in the `horror_movies.csv` file.

## Example CSV Format
Title
A Nightmare on Elm Street
Friday the 13th
Halloween


## Contributors
Joshua Hemingway

## License

This project is licensed under the GNU License - see the [LICENSE](LICENSE) file for details.




