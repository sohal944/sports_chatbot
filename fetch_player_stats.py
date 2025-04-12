import requests
import json
import os

API_TOKEN = "FlIUxPHZYsKk3a9sjHHJxUFKxwDu5TLGqZv9evvvGaljU9N9UNFaUc9ZdXFH"
SEASON_ID = 1937
TOP_SCORERS_URL = f"https://api.sportmonks.com/v3/football/topscorers/seasons/{SEASON_ID}"
INCLUDES = "player;participant"

def fetch_top_scorers(season_id):
    print(f"🥅 Fetching top scorers for season {season_id} from SportMonks...")

    response = requests.get(
        f"https://api.sportmonks.com/v3/football/topscorers/seasons/{season_id}",
        params={"api_token": API_TOKEN, "include": INCLUDES}
    )

    if response.status_code != 200:
        print(f"❌ Failed to fetch top scorers: {response.status_code}")
        print(response.text)
        return

    response_json = response.json()
    data = response_json.get("data", [])
    print(f"✅ Found {len(data)} top scorers.\n")

    top_scorers_list = []

    for player_data in data:
        player = player_data.get("player", {})
        team = player_data.get("participant", {})
        position = player_data.get("position")
        total_goals = player_data.get("total")

        player_name = player.get("name", "Unknown Player")
        team_name = team.get("name", "Unknown Team")

        print(f"{player_name} ({team_name}) — Goals: {total_goals} | Position: {position}")

        top_scorers_list.append({
            "player": player_name,
            "team": team_name,
            "goals": total_goals,
            "position": position
        })

    # Save to data/season_<id>_top_scorers.json
    os.makedirs("data", exist_ok=True)
    output_path = f"data/players_standings/season_{season_id}_top_scorers.json"
    with open(output_path, "w") as f:
        json.dump(top_scorers_list, f, indent=2)

    print(f"\n💾 Top scorers saved to {output_path}")

# Run it
if __name__ == "__main__":
    fetch_top_scorers(SEASON_ID)
