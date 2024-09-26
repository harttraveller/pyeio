from pathlib import Path


def load(): ...


def save(): ...


def get(): ...


# ! ---


class Streamer:
    def __init__(self, url: str) -> None:
        self.url = url


class Reader:
    def __init__(self, file: str | Path) -> None:
        self.file = Path(file)
        self.__column_names: list[str] | None = None

    @property
    def column_names(self) -> list[str]: ...

    def read_rows(self): ...

    def read_column_names(self): ...
