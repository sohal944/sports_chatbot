import requests
import json
import time

API_TOKEN = "FlIUxPHZYsKk3a9sjHHJxUFKxwDu5TLGqZv9evvvGaljU9N9UNFaUc9ZdXFH"
LEAGUE_FILE = "id_to_name/leagues.json"
TEAM_FILE = "id_to_name/teams.json"

def load_lookup(filepath):
    with open(filepath, "r") as f:
        data = json.load(f)
        if isinstance(data, list):
            return {entry["id"]: entry["name"] for entry in data}
        elif isinstance(data, dict):
            return {entry["id"]: entry["name"] for entry in data.get("data", [])}
        return {}

def fetch_live_scores(api_token, league_lookup, team_lookup):
    url = "https://soccer.sportmonks.com/api/v2.0/livescores"
    print("📡 Fetching live scores from SportMonks v2.0...")

    response = requests.get(url, params={
        "api_token": api_token,
        "include": ""  # You can add "localTeam,visitorTeam" if needed
    })

    if response.status_code != 200:
        print("❌ Failed to fetch live scores.")
        return []

    data = response.json().get("data", [])
    if not data:
        print("⚠️ No live matches right now.")
        return []

    live_matches = []
    for match in data:
        match_id = match.get("id")
        league_id = match.get("league_id")
        league = league_lookup.get(league_id, "Unknown League")
        status = match.get("time", {}).get("status", "Unknown")

        scores = match.get("scores", {})
        local_score = scores.get("localteam_score", "N/A")
        visitor_score = scores.get("visitorteam_score", "N/A")

        home_team_id = match.get("localteam_id")
        away_team_id = match.get("visitorteam_id")
        home_team = team_lookup.get(home_team_id, f"Team {home_team_id}")
        away_team = team_lookup.get(away_team_id, f"Team {away_team_id}")

        match_name = f"{home_team} vs {away_team}"
        start_time = match.get("time", {}).get("starting_at", {}).get("date_time", "Unknown")

        live_matches.append({
            "match_id": match_id,
            "match": match_name,
            "status": status,
            "score": f"{local_score} - {visitor_score}",
            "league": league,
            "home_team": home_team,
            "away_team": away_team,
            "start_time": start_time
        })

    print(f"✅ Found {len(live_matches)} live match(es).")
    return live_matches

if __name__ == "__main__":
    league_lookup = load_lookup(LEAGUE_FILE)
    team_lookup = load_lookup(TEAM_FILE)

    while True:
        live_scores = fetch_live_scores(API_TOKEN, league_lookup, team_lookup)

        with open("final_data/live_score/live_scores_named.json", "w") as f:
            json.dump(live_scores, f, indent=2)
        print("💾 Saved live scores to data/live_scores_named.json")

        time.sleep(60)  # Wait for 60 seconds before fetching again
