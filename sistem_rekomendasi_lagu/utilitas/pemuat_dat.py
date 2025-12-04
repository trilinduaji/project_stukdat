import json
import os

class Loader:
    @staticmethod
    def muat(path):
        if not os.path.exists(path):
            return {"next_id": 1001, "lagu": []}
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def simpan(path, data):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
