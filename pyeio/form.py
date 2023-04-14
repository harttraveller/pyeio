"""
Data format IO builder classes
"""

import json
from pathlib import Path


class JSON:
    @staticmethod
    def load(path: str | Path) -> dict | list:
        with open(path, "r") as file:
            data = json.load(file)
        file.close()
        return data

    @staticmethod
    def save(data: dict | list, path: str | Path) -> None:
        with open(path, "w") as file:
            file.write(json.dumps(data, indent=4))
        file.close()


class JSONL:
    @staticmethod
    def load(path: str | Path) -> list:
        with open(path, "r") as file:
            data = [json.loads(line) for line in file.readlines()]
        file.close()
        return data

    @staticmethod
    def save(data: list, path: str | Path) -> None:
        with open(path, "w") as file:
            for line in data:
                file.write(json.dumps(line) + "\n")
        file.close()


class TOML:
    @staticmethod
    def load(path: str | Path) -> dict:
        pass

    @staticmethod
    def save(data: dict, path: str | Path) -> None:
        pass
