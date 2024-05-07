import requests
import csv
import os.path
import time

# Function to retrieve genre names and IDs using TMDb API
def get_genre_list(api_key):
    # Base URL for TMDb API
    base_url = "https://api.themoviedb.org/3"

    # Endpoint for retrieving genre list
    endpoint = "/genre/movie/list"

    # Parameters for the API request
    params = {
        "api_key": api_key
    }

    # Send GET request to TMDb API
    response = requests.get(base_url + endpoint, params=params)

    # Check if request was successful
    if response.status_code == 200:
        # Parse JSON response
        data = response.json()
        # Get genre list
        genres = data.get('genres', [])
        # Create a dictionary of genre names and IDs
        genre_dict = {genre['name'].lower(): genre['id'] for genre in genres}
        return genre_dict
    else:
        # Print error message if request failed
        print("Failed to fetch genre list. Error:", response.status_code)
        return None

# Function to search for movies by genre using TMDb API
def search_movies_by_genre(api_key, genre_id, num_recommendations):
    # Base URL for TMDb API
    base_url = "https://api.themoviedb.org/3"

    # Endpoint for discovering movies by genre
    endpoint = "/discover/movie"

    # Start with page 1
    page = 1
    total_movies = []
    movies_fetched = 0

    # Continue fetching pages until the desired number of recommendations is reached
    while movies_fetched < num_recommendations:
        # Parameters for the API request
        params = {
            "api_key": api_key,
            "with_genres": genre_id,
            "page": page
        }

        # Send GET request to TMDb API
        response = requests.get(base_url + endpoint, params=params)

        # Check if request was successful
        if response.status_code == 200:
            # Parse JSON response
            data = response.json()
            # Get movies from this page
            movies = data.get('results', [])
            # If no movies found, break out of the loop
            if not movies:
                break
            # Add movies to the list
            total_movies.extend([movie['title'] for movie in movies])
            movies_fetched += len(movies)
            # If we have fetched enough movies, break out of the loop
            if movies_fetched >= num_recommendations:
                break
            # Move to the next page
            page += 1
        elif response.status_code == 400:
            choice = input("Error 400: There may not be enough recommendations available. Do you want to wait 2 minutes and try again? (yes/no): ").lower()
            if choice != 'yes':
                break
            else:
                print("Waiting for 2 minutes...")
                time.sleep(120)
        else:
            # Print error message if request failed
            print("Failed to fetch movies. Error:", response.status_code)
            break

    return total_movies

# Function to display available genre IDs
def display_genre_help(genre_dict):
    print("Available genres:")
    for genre_name, genre_id in genre_dict.items():
        print(f"{genre_name}: {genre_id}")

# Prompt user for genre ID
def prompt_genre_id(genre_dict):
    while True:
        genre_input = input("Enter the genre name or ID (type 'help' for options): ").lower()
        if genre_input == 'help':
            display_genre_help(genre_dict)
        elif genre_input.isdigit():
            genre_id = int(genre_input)
            if genre_id in genre_dict.values():
                return genre_id
            else:
                print("Invalid genre ID. Please try again.")
        elif genre_input in genre_dict:
            return genre_dict[genre_input]
        else:
            print("Invalid genre name or ID. Please try again.")

# Function to write movies to a CSV file
def write_movies_to_csv(csv_file_name, movies):
    if os.path.exists(csv_file_name):
        print("CSV file already exists. Skipping existing movies.")
        existing_movies = set()
        with open(csv_file_name, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip header row
            for row in reader:
                existing_movies.add(row[0])
        movies = [movie for movie in movies if movie not in existing_movies]

    with open(csv_file_name, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        if os.path.getsize(csv_file_name) == 0:
            writer.writerow(['Title'])
        writer.writerows([[movie] for movie in movies])

# Your TMDb API key
api_key = ""

# Get genre list
genre_dict = get_genre_list(api_key)

if genre_dict:
    # Prompt user for genre ID
    genre_id = prompt_genre_id(genre_dict)

    # Prompt user for the number of recommendations
    num_recommendations = int(input("How many recommendations do you want? "))

    # Search for movies by genre
    print("Searching for movies...")
    movies = search_movies_by_genre(api_key, genre_id, num_recommendations)

    # Prompt user for CSV file name
    csv_file_name = input("Enter the CSV file name to save the movies: ")

    # Write movies to a CSV file
    print("Writing movies to CSV file...")
    write_movies_to_csv(csv_file_name, movies)

    print("Operation completed successfully.")
