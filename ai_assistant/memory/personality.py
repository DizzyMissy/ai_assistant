import json
from tools.file_tools import save_memory, read_memory

PROFILE_FILE = "workspace/personality.json"

# Initialize default personality
def load_personality():
    try:
        with open(PROFILE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "name": None,
            "tone": "friendly and concise",
            "interests": [],
            "goals": [],
        }

def save_personality(profile):
    with open(PROFILE_FILE, "w", encoding="utf-8") as f:
        json.dump(profile, f, indent=2)
    return "Personality saved."

def update_personality(key, value):
    profile = load_personality()
    profile[key] = value
    save_personality(profile)
