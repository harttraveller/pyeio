from pathlib import Path
from typing import Callable, Generator, Any
from zstandard import ZstdDecompressor

MAX_WINDOW_SIZE: int = 1 << 31


class StreamReader:
    def __init__(
        self,
        path: str | Path,
        delimiter: bytes,
        size: int = 1 << 20,
    ) -> None:
        self.path = path
        self.size = size


def load(): ...


def read(path: str | Path, delimiter: bytes = b"\n"):
    reader = StreamReader(path=path, delimiter=delimiter)
