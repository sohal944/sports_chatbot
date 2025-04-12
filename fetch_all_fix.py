import requests
import json
import os

API_TOKEN = "FlIUxPHZYsKk3a9sjHHJxUFKxwDu5TLGqZv9evvvGaljU9N9UNFaUc9ZdXFH"
OUTPUT_FOLDER = "data"
OUTPUT_FILE = "fixtures_between_dates.json"

def fetch_fixtures_between_dates(api_token, start_date, end_date):
    print(f"📅 Fetching fixtures between {start_date} and {end_date}...")

    # Constructing the URL for the "between" endpoint
    url = f"https://api.sportmonks.com/v3/football/fixtures/between/{start_date}/{end_date}"

    # Specify which data you want to include
    includes = "league;season;venue;participants"

    response = requests.get(url, params={
        "api_token": api_token,
        "include": includes
    })

    if response.status_code != 200:
        print("❌ Failed to fetch data:", response.status_code)
        print(response.text)
        return []

    data = response.json().get("data", [])
    print(f"✅ Got {len(data)} fixtures.")
    return data

def fetch_league_details(league_id):
    url = f"https://api.sportmonks.com/v3/football/leagues/{league_id}"
    response = requests.get(url, params={"api_token": API_TOKEN})
    if response.status_code == 200:
        return response.json().get("data", {}).get("name", "Unknown League")
    return "Unknown League"

def fetch_season_details(season_id):
    url = f"https://api.sportmonks.com/v3/football/seasons/{season_id}"
    response = requests.get(url, params={"api_token": API_TOKEN})
    if response.status_code == 200:
        return response.json().get("data", {}).get("name", "Unknown Season")
    return "Unknown Season"

def extract_team_names(participants, fallback_name=""):
    home, away = None, None
    if isinstance(participants, dict):
        participants = participants.get("data", [])
    if isinstance(participants, list):
        for team in participants:
            loc = team.get("meta", {}).get("location")
            if loc == "home":
                home = team.get("name")
            elif loc == "away":
                away = team.get("name")

    if not home or not away:
        if " vs " in fallback_name:
            parts = fallback_name.split(" vs ")
            home = parts[0].strip()
            away = parts[1].strip()

    return home, away

def flatten_fixture(fixture):
    league_data = fixture.get("league", {}).get("data", {})
    season_data = fixture.get("season", {}).get("data", {})
    venue_data = fixture.get("venue", {}).get("data", {})

    league = league_data.get("name") if league_data else fetch_league_details(fixture.get("league_id"))
    season = season_data.get("name") if season_data else fetch_season_details(fixture.get("season_id"))
    venue = venue_data.get("name") if venue_data else "Unknown Venue"
    
    participants = fixture.get("participants", {})
    home_team, away_team = extract_team_names(participants, fixture.get("name", ""))

    return {
        "fixture_id": fixture.get("id"),
        "match": fixture.get("name"),
        "start_time": fixture.get("starting_at"),
        "duration": fixture.get("length"),
        "result": fixture.get("result_info"),
        "league": league,
        "season": season,
        "venue": venue,
        "home_team": home_team,
        "away_team": away_team
    }

def save_fixtures(data, folder, filename):
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, filename)
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)
    print(f"💾 Saved to {filepath}")

if __name__ == "__main__":
    # Define the date range (e.g., from 2023-01-01 to 2023-12-31)
    start_date = "2023-01-01"
    end_date = "2023-03-31"
    
    # Fetch the fixtures for the given date range
    raw_fixtures = fetch_fixtures_between_dates(API_TOKEN, start_date, end_date)
    
    # Flatten the fixture data
    named_fixtures = [flatten_fixture(fix) for fix in raw_fixtures]
    
    # Save the fixtures to a JSON file
    save_fixtures(named_fixtures, OUTPUT_FOLDER, OUTPUT_FILE)
