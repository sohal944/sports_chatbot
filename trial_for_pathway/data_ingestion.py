# run_pathway_filter.py
import pathway as pw

class MatchSchema(pw.Schema):
    home: str
    away: str
    status: str
    score_home: int
    score_away: int
    diff: int
    time: int

def run_pathway_pipeline():
    live_data = pw.io.jsonlines.read(
        "stream/processed_data.jsonl", schema=MatchSchema, mode="static"
    )

    filtered = live_data.filter(pw.this.status != "Match Postponed")
    pw.io.jsonlines.write(filtered, "stream/processed_filtered.jsonl")

    pw.run()
