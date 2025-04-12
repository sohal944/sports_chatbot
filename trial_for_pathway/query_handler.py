from fetch_live_score import fetch_live_scores
from fetch_team_stats import fetch_team_stats
from fetch_player_stats import fetch_player_stats


def chatbot_query_handler(user_query):
    user_query = user_query.lower()

    if "live score" in user_query or "match" in user_query:
        return fetch_live_scores()

    elif "player" in user_query and "stats" in user_query:
        name = user_query.replace("player stats", "").strip()
        return fetch_player_stats(name)

    elif "team stats" in user_query:
        # Default to Man United (team_id=33) unless parsing done
        return fetch_team_stats(team_id=33)



    else:
        return {"message": "Sorry, I didn't get that. Try asking about live scores, player stats, team stats, or league standings."}
