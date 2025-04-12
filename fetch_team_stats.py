import requests
import json
import os

API_TOKEN = "FlIUxPHZYsKk3a9sjHHJxUFKxwDu5TLGqZv9evvvGaljU9N9UNFaUc9ZdXFH"
INCLUDES = "participant;rule.type;details.type;form;stage;league;group"
BASE_URL = "https://api.sportmonks.com/v3/football/standings/seasons"
LEAGUE_FILE = "id_to_name/leagues.json"  # Local league ID → name mapping

def load_league_mapping(filepath):
    try:
        with open(filepath, "r") as f:
            leagues_data = json.load(f)
        return {item["id"]: item["name"] for item in leagues_data}
    except Exception as e:
        print(f"⚠️ Failed to load leagues.json: {e}")
        return {}

def fetch_team_standings(season_id):
    print(f"📊 Fetching standings for season {season_id}...")

    url = f"{BASE_URL}/{season_id}"
    response = requests.get(url, params={"api_token": API_TOKEN, "include": INCLUDES})

    if response.status_code != 200:
        print(f"❌ Failed to fetch standings: {response.status_code}")
        print(response.text)
        return

    json_data = response.json()
    data = json_data.get("data", [])
    league_mapping = load_league_mapping(LEAGUE_FILE)

    print(f"✅ Fetched standings for {len(data)} teams.\n")

    standings_list = []
    for team_data in data:
        team = team_data.get("participant", {})
        stage = team_data.get("stage", {}).get("name", "Unknown Stage")
        points = team_data.get("points")
        rank = team_data.get("position")
        team_name = team.get("name", "Unknown Team")
        league_id = team_data.get("league_id", -1)
        league_name = league_mapping.get(league_id, "Unknown League")

        print(f"{team_name} — Points: {points} | Rank: {rank} | League: {league_name}")

        standings_list.append({
            "team": team_name,
            "points": points,
            "rank": rank,
            "stage": stage,
            "league": league_name
        })

    # Save to JSON file
    os.makedirs("data", exist_ok=True)
    filename = f"data/team_standings/season_{season_id}_standings.json"
    with open(filename, "w") as f:
        json.dump(standings_list, f, indent=2)
    print(f"\n💾 Standings saved to {filename}")

# Example usage
if __name__ == "__main__":
    SEASON_ID = 1273  # Replace with your desired season ID
    fetch_team_standings(SEASON_ID)
