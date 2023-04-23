"""Add, Delete and List google calendar events from Python"""
import json


def load_json(path):
    """Load json file"""
    with open(path, mode="r", encoding="utf8") as file:
        data = json.load(file)
    return data

if __name__ == "__main__":
    events = load_json("study_guide.json")
    print(events)
