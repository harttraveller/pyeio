"""
Data format IO builder classes
"""

from pathlib import Path
import json
from typing import Any


class JSON:
    # TODO: add automatic checks for jsonl files
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
            try:
                data = [json.loads(line) for line in file.splitlines()]
            except:
                raise Exception("asdf")

    @staticmethod
    def save(data: list, path: str | Path) -> None:
        JSON.save(data, path)


class NPY:
    pass


class CSV:
    @staticmethod
    def load(path: str | Path) -> Any:
        pass

    @staticmethod
    def save(data: Any, path: str | Path) -> None:
        pass


class XLSX:
    @staticmethod
    def load(path: str | Path) -> Any:
        pass

    @staticmethod
    def save(data: Any, path: str | Path) -> None:
        pass


class YAML:
    @staticmethod
    def load(path: str | Path) -> Any:
        pass

    @staticmethod
    def save(data: Any, path: str | Path) -> None:
        pass


class TOML:
    @staticmethod
    def load(path: str | Path) -> Any:
        pass

    @staticmethod
    def save(data: Any, path: str | Path) -> None:
        pass


class ZIP:
    @staticmethod
    def load(path: str | Path) -> Any:
        pass

    @staticmethod
    def save(data: Any, path: str | Path) -> None:
        pass


class BIN:
    @staticmethod
    def load(path: str | Path) -> Any:
        pass

    @staticmethod
    def save(data: Any, path: str | Path) -> None:
        pass


class NULL:
    "no extension, assumed binary or text file"

    @staticmethod
    def load(path: str | Path) -> Any:
        pass

    @staticmethod
    def save(data: Any, path: str | Path) -> None:
        pass


class PY:
    @staticmethod
    def load(path: str | Path) -> Any:
        pass

    @staticmethod
    def save(data: Any, path: str | Path) -> None:
        pass


class JS:
    @staticmethod
    def load(path: str | Path) -> Any:
        pass

    @staticmethod
    def save(data: Any, path: str | Path) -> None:
        pass


class GRAPHML:
    @staticmethod
    def load(path: str | Path) -> Any:
        pass

    @staticmethod
    def save(data: Any, path: str | Path) -> None:
        pass


class SEVENZIP:
    "7 zip, can't start class name with number"

    @staticmethod
    def load(path: str | Path) -> Any:
        pass

    @staticmethod
    def save(data: Any, path: str | Path) -> None:
        pass
