import json
import re

def split_team_stats(text: str):
    # Match each team entry ending in "points."
    pattern = r"([A-ZÄÖÜa-zäöüß0-9\s\-\.]+? has played .*? points\.)"
    matches = re.findall(pattern, text)
    return [{"text": match.strip()} for match in matches]

def main():
    with open("mock_data/Bundesliga_2020-2021_summary.txt", "r") as f:
        full_text = f.read()  # Just read raw text here

    split_docs = split_team_stats(full_text)

    with open("static_data.json", "w") as out:
        json.dump(split_docs, out, indent=2)

    print(f"✅ Split {len(split_docs)} entries into 'documents.json'")

if __name__ == "__main__":
    main()
