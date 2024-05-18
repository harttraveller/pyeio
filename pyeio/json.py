import json
from pathlib import Path


def load(path: str | Path) -> list | dict:
    with open(path) as file:
        data = json.loads(file.read())
    file.close()
    return data
