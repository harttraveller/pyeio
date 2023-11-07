from __future__ import annotations

import toml
import orjson
from pathlib import Path
from typing import Union


class JSON:
    @staticmethod
    def open(path: Union[str, Path]) -> Union[dict, list]:
        with open(path, "r") as file:
            data = orjson.load(file)
        file.close()
        return data

    @staticmethod
    def save(data: Union[dict, list], path: Union[str, Path]) -> None:
        with open(path, "w") as file:
            file.write(orjson.dumps(data, indent=4))
        file.close()

    @staticmethod
    def load(path: Union[str, Path]) -> JSON:
        pass


class JSONL:
    @staticmethod
    def open(path: Union[str, Path]) -> list:
        with open(path, "r") as file:
            data = [orjson.loads(line) for line in file.readlines()]
        file.close()
        return data

    @staticmethod
    def save(data: list, path: Union[str, Path]) -> None:
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
    def open(path: Union[str, Path]) -> dict:
        with open(path, "r") as file:
            data = toml.loads(file.read())
        file.close()
        return data

    @staticmethod
    def save(data: dict, path: Union[str, Path]) -> None:
        with open(path, "w") as file:
            file.write(toml.dumps(data))
        file.close()


class CSV:
    # TODO
    pass


class XLSX:
    # TODO
    pass


OPEN = {}

LOAD = {}
