import json


class JSONSaver:
    def __init__(self):
        self.data = []

    def add_vacancy(self, vacancy: dict):
        self.data.append(vacancy)

    def save_data(self, file_name: str):
        with open(file_name, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)

