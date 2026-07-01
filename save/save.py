import json
import os

SAVE_PATH = "./save/save.json"

DEFAULT_SAVE = {
    "version": "1.0.1.2",

    "progress": {
        "stars": 0,
        "highscore": 0
    },

    "challenges": {
        "challenge_1": False,
        "challenge_2": False,
        "challenge_3": False
    },

    "settings": {
        "fullscreen": False,
        "width": 1280,
        "height": 720
    },

    "statistics": {
        "play_time": 0,
        "total_deaths": 0,
        "total_wins": 0
    },

    "animatronics": {
        "Maurello": 5
    }
}

SAVE = {}

def create_save():

    os.makedirs("save", exist_ok=True)

    if not os.path.exists(SAVE_PATH):

        with open(SAVE_PATH, "w") as f:

            json.dump(DEFAULT_SAVE, f, indent=4)
def load_save():

    global SAVE

    with open(SAVE_PATH, "r") as f:
        SAVE = json.load(f)
def save_game(data):

    with open(SAVE_PATH, "w") as f:

        json.dump(data, f, indent=4)
def get_fromSave(path):
    data = SAVE
    for key in path.split("."):
        data = data[key]
    return data

def set_fromSave(path, value):

    data = SAVE

    keys = path.split(".")

    for key in keys[:-1]:
        data = data[key]

    data[keys[-1]] = value

