import requests
import json
import os
import time

API_KEY = "8cc9852171c38bf8694cf172f164291d"
API_URL = "https://v3.football.api-sports.io/fixtures?live=all"
HEADERS = {
    "x-apisports-key": API_KEY
}

def fetch_live_scores():
    print("Fetching live data on user query...")
    response = requests.get(API_URL, headers=HEADERS)
    data = response.json().get("response", [])

    if not os.path.exists("stream"):
        os.makedirs("stream")

    entries = []
    with open("stream/processed_data.jsonl", "a") as f:
        for match in data:
            processed_entry = {
                "home": match["teams"]["home"]["name"],
                "away": match["teams"]["away"]["name"],
                "status": match["fixture"]["status"]["long"],
                "score_home": match["goals"]["home"],
                "score_away": match["goals"]["away"],
                "diff": 1,
                "time": int(time.time() * 1000)
            }
            entries.append(processed_entry)
            f.write(json.dumps(processed_entry) + "\n")

    print(f"✅ Fetched and saved {len(entries)} matches.")
    return entries
