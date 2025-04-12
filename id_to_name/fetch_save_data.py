import requests
import json
import os

# API token
API_TOKEN = "FlIUxPHZYsKk3a9sjHHJxUFKxwDu5TLGqZv9evvvGaljU9N9UNFaUc9ZdXFH"

# Base URLs
PLAYER_URL = "https://api.sportmonks.com/v3/football/players"
TEAM_URL = "https://api.sportmonks.com/v3/football/teams"
LEAGUE_URL = "https://api.sportmonks.com/v3/football/leagues"
SEASON_URL = "https://api.sportmonks.com/v3/football/seasons"

# Function to fetch and save data
def fetch_and_save_data(url, file_name):
    response = requests.get(url, params={"api_token": API_TOKEN, "include": ""})
    if response.status_code == 200:
        data = response.json().get('data', [])
        if data:
            with open(file_name, 'w') as f:
                json.dump(data, f, indent=4)
            print(f"✅ Data saved to {file_name}")
        else:
            print(f"❌ No data found for {file_name}")
    else:
        print(f"❌ Failed to fetch data from {url}: {response.status_code}")

# Fetch players data
fetch_and_save_data(PLAYER_URL, 'id_to_name/players.json')

# Fetch teams data
fetch_and_save_data(TEAM_URL, 'id_to_name/teams.json')

# Fetch leagues data
fetch_and_save_data(LEAGUE_URL, 'id_to_name/leagues.json')

fetch_and_save_data(SEASON_URL, 'id_to_name/seasons.json')