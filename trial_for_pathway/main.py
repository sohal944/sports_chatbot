# main.py
from fastapi import FastAPI
from trial_for_pathway.fetch_and_save import fetch_live_scores
from trial_for_pathway.data_ingestion import run_pathway_pipeline
from trial_for_pathway.read_filtered import read_filtered_scores

app = FastAPI()

@app.get("/live-scores")
def get_live_scores():
    fetch_live_scores()              # Step 1: Fetch live scores and save to processed_data.jsonl
    run_pathway_pipeline()           # Step 2: Run Pathway and generate processed_filtered.jsonl
    return read_filtered_scores()    # Step 3: Read filtered scores and return
