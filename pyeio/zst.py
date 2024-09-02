from pathlib import Path
from typing import Callable, Generator, Any
from zstandard import ZstdDecompressor


class _ZST:
    def __init__(
        self,
        path: str | Path,
        size: int = 1 << 20,
    ) -> None:
        self.path = path
        self.size = size


def load(): ...


def read(): ...
