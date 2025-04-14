import pandas as pd
import os
import time
from urllib.error import HTTPError

LEAGUE_INFO = {
    'Premier League': {'url_name': 'Premier-League', 'id': '9'},
    'La Liga': {'url_name': 'La-Liga', 'id': '12'},
    'Serie A': {'url_name': 'Serie-A', 'id': '11'},
    'Ligue 1': {'url_name': 'Ligue-1', 'id': '13'},
    'Bundesliga': {'url_name': 'Bundesliga', 'id': '20'},
}

def get_fixture_data(league_name, league_url_name, league_id, season):
    print(f'📅 Fetching fixture data for {league_name}, Season: {season}')
    
    url = f'https://fbref.com/en/comps/{league_id}/{season}/schedule/{season}-{league_url_name}-Scores-and-Fixtures'
    
    try:
        tables = pd.read_html(url)
    except Exception as e:
        print(f"❌ Failed to read tables from URL: {url}")
        print(e)
        return

    try:
        fixtures = tables[0][['Wk', 'Day', 'Date', 'Time', 'Home', 'Away', 'xG', 'xG.1', 'Score']].dropna()
    except KeyError:
        print("❌ Expected columns not found in fixture table.")
        return

    fixtures['season'] = season
    fixtures['game_id'] = fixtures.index

    output_dir = os.path.join("final_data", "fixtures", league_url_name)
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, f'{league_url_name}_{season}_fixture_data.json')

    # Only save if data has changed
    if os.path.exists(output_path):
        try:
            old_data = pd.read_json(output_path)
            if fixtures.equals(old_data):
                print(f'⏩ No changes for {league_name} ({season}), skipping save.')
                return
        except:
            print("⚠️ Error reading existing file, will overwrite.")

    fixtures.to_json(output_path, orient='records', indent=2)
    print(f'✅ Updated: {output_path}')


def run_for_league_season(league_name, season):
    if league_name not in LEAGUE_INFO:
        print(f"❌ League {league_name} not recognized.")
        return
    
    league = LEAGUE_INFO[league_name]
    try:
        get_fixture_data(league_name, league['url_name'], league['id'], season)
    except HTTPError:
        print(f"⚠️ HTTPError for {league_name} - {season}, retrying later.")
        time.sleep(5)


def start_live_updating(seasons=["2024-2025"], interval_per_league=60, cooldown_between_cycles=300):
    leagues = list(LEAGUE_INFO.keys())

    while True:
        for season in seasons:
            print(f"\n🔄 Starting update for season {season}...")

            for league in leagues:
                print(f"\n📊 Processing {league} - {season}...")
                run_for_league_season(league, season)
                print(f"⏳ Waiting {interval_per_league} seconds before updating next league...\n")
                time.sleep(interval_per_league)

            print(f"\n🔁 All leagues for {season} updated. Waiting {cooldown_between_cycles // 60} minutes before next full cycle...\n")
            time.sleep(cooldown_between_cycles)


if __name__ == "__main__":
    try:
        start_live_updating()
    except KeyboardInterrupt:
        print("\n🛑 Interrupted by user. Exiting gracefully.")
