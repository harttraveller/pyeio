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
        self.delimiter = delimiter
        self.size = size
        self.reset()

    def reset(self) -> None:
        self.stream = ZstdDecompressor(
            max_window_size=MAX_WINDOW_SIZE,
        ).stream_reader(open(self.path, "rb"))
        self.buffer = b""
        self.lines = []

    def __iter__(self) -> Generator[bytes, None, None]:
        while True:
            try:
                yield next(self)
            except StopIteration:
                break

    def __next__(self) -> bytes:
        if len(self.lines):
            return self.lines.pop(0)
        else:
            chunk = self.stream.read(self.size)
            if chunk:
                self.lines = (self.buffer + chunk).split(self.delimiter)
                self.buffer = self.lines[-1]
                self.lines = self.lines[:-1]
                return self.lines.pop(0)
            else:
                raise StopIteration()

    def read_chunk(self) -> bytes:
        return self.__next__()

    def read_chunks(self, n: int) -> list[bytes]:
        return [self.read_chunk() for _ in range(n)]


def load(): ...


def read(path: str | Path, delimiter: bytes = b"\n"):
    reader = StreamReader(path=path, delimiter=delimiter)
