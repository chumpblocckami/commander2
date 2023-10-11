import json


class Logger:
    def __init__(self):
        self.path_db = "./recent_cards.json"

    def log_to_db(self, data):
        with open(self.path_db, "r+") as file:
            file_data = json.load(file)
            file_data.append(data)
            file.seek(0)
            json.dump(file_data, file)

    def log_from_db(self):
        with open(self.path_db, "r+") as file:
            recent_cards = json.load(file)
        return recent_cards
