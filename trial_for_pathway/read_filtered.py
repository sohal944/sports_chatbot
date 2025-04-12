# read_filtered.py
import json

def read_filtered_scores():
    try:
        with open("stream/processed_filtered.jsonl", "r") as f:
            return [json.loads(line.strip()) for line in f.readlines()]
    except FileNotFoundError:
        return {"error": "Filtered data not found. Run Pathway stream first."}
