import json


def load_json(path: str) -> dict:
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(data: dict, path: str) -> dict:
    with open(path, 'w', encoding='utf-8') as f:
        return json.dump(data, f)
