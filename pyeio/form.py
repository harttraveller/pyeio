"""
Data format IO builder classes
"""

import toml
import orjson
from pathlib import Path


class JSON:
    @staticmethod
    def load(path: str | Path) -> dict | list:
        with open(path, "r") as file:
            data = orjson.load(file)
        file.close()
        return data

    @staticmethod
    def save(data: dict | list, path: str | Path) -> None:
        with open(path, "w") as file:
            file.write(orjson.dumps(data, indent=4))
        file.close()


class JSONL:
    @staticmethod
    def load(path: str | Path) -> list:
        with open(path, "r") as file:
            data = [orjson.loads(line) for line in file.readlines()]
        file.close()
        return data

    @staticmethod
    def save(data: list, path: str | Path) -> None:
        with open(path, "w") as file:
            for line in data:
                file.write(orjson.dumps(line) + "\n")
        file.close()

    @staticmethod
    def add(data, path) -> None:
        # TODO
        pass


class TOML:
    @staticmethod
    def load(path: str | Path) -> dict:
        with open(path, "r") as file:
            data = toml.loads(file.read())
        file.close()
        return data

    @staticmethod
    def save(data: dict, path: str | Path) -> None:
        with open(path, "w") as file:
            file.write(toml.dumps(data))
        file.close()


class CSV:
    # TODO
    pass


class XLSX:
    # TODO
    pass
