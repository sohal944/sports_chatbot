import requests
import json
import os

# API token for SportMonks
API_TOKEN = "FlIUxPHZYsKk3a9sjHHJxUFKxwDu5TLGqZv9evvvGaljU9N9UNFaUc9ZdXFH"

# URL for fetching commentaries and fixtures
COMMENTARY_URL = "https://api.sportmonks.com/v3/football/commentaries"
FIXTURE_HEAD_TO_HEAD_URL = "https://api.sportmonks.com/v3/football/fixtures/head-to-head/{}/{}"

# Load the teams from the teams.json file
def load_teams_data(filename="id_to_name/teams.json"):
    try:
        with open(filename, "r") as f:
            teams_data = json.load(f)
            print("✅ Teams data loaded successfully!")
            return {team["name"].lower(): team["id"] for team in teams_data}
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"❌ Error loading teams data: {e}")
        return {}

# Fetch the fixture ID based on the team names
def get_fixture_id(team1, team2, teams_data):
    team1_id = teams_data.get(team1.lower())
    team2_id = teams_data.get(team2.lower())

    if not team1_id or not team2_id:
        print(f"❌ One or both teams not found in the teams data.")
        return None

    url = FIXTURE_HEAD_TO_HEAD_URL.format(team1_id, team2_id)
    response = requests.get(url, params={"api_token": API_TOKEN})

    if response.status_code == 200:
        fixture_data = response.json().get("data", [])
        if fixture_data:
            return fixture_data[0].get("id")  # Assumes the fixture data is a list with the relevant fixture
        else:
            print(f"❌ No fixture data found between {team1} and {team2}.")
            return None
    else:
        print(f"❌ Failed to fetch fixture data: {response.status_code}")
        print(response.text)
        return None

# Save commentaries to a structured file path
def save_commentaries_to_file(commentaries, team1, team2):
    # Ensure the directory exists
    os.makedirs("data/teams_commentaries", exist_ok=True)

    # Set the output path with team names
    output_path = f"data/teams_commentaries/{team1.lower()}_vs_{team2.lower()}_commentaries.json"
    
    # If the file already exists, don't overwrite
    if os.path.exists(output_path):
        print(f"⚠️ Data already saved for {team1} vs {team2}.")
        return
    
    # Structure the JSON with the "data" key
    data_to_save = {
        "data": commentaries
    }
    
    # Save the commentaries to the file
    with open(output_path, "w") as f:
        json.dump(data_to_save, f, indent=4, ensure_ascii=False)

        print(f"✅ Saved commentaries to {output_path}")

# Fetch commentaries for a given fixture ID and save to a file
def fetch_commentaries_by_fixture_id(fixture_id, team1, team2):
    response = requests.get(COMMENTARY_URL, params={"api_token": API_TOKEN, "fixture_id": fixture_id})

    if response.status_code == 200:
        data = response.json().get("data", [])
        print(f"✅ Fetched {len(data)} commentaries.\n")

        commentaries = []
        for comment in data:
            text = comment.get("comment", "No comment")
            minute = comment.get("minute", "-")
            extra_min = comment.get("extra_minute", "")
            is_goal = comment.get("is_goal", False)
            is_important = comment.get("is_important", False)

            minute_display = f"{minute}+{extra_min}" if extra_min else f"{minute}'"
            goal_marker = "⚽️" if is_goal else ""
            important_marker = "❗" if is_important else ""

            commentaries.append({
                "minute": minute_display,
                "comment": text,
                "goal": goal_marker,
                "important": important_marker,
            })
            print(f"[{minute_display}] {text} {goal_marker}{important_marker}")
            print("—" * 60)

        # Save the commentaries to a structured file path
        save_commentaries_to_file(commentaries, team1, team2)
    else:
        print(f"❌ Failed to fetch commentaries: {response.status_code}")
        print(response.text)

# Main function to orchestrate the fetching of commentaries
def main(team1, team2):
    teams_data = load_teams_data()

    if not teams_data:
        return

    fixture_id = get_fixture_id(team1, team2, teams_data)

    if fixture_id:
        print(f"Fetching commentaries for {team1} vs {team2} (Fixture ID: {fixture_id})\n")
        fetch_commentaries_by_fixture_id(fixture_id, team1, team2)
    else:
        print(f"❌ Unable to get fixture ID for {team1} vs {team2}.")

# Example: Fetch commentaries for a match between Celtic and Kilmarnock
if __name__ == "__main__":
    team1 = "Celtic"
    team2 = "Kilmarnock"
    main(team1, team2)
