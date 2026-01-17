# ruff: noqa

from typing import Any, Iterator
from dataclasses import dataclass
from pathlib import Path
from pyeio import io
import orjson


@dataclass
class Reader:
    file: bytes | str | Path
    size: int = io.DEFAULT_BUFFER_SIZE
    delimiter: bytes = b"\n"

    def __post_init__(self) -> None:
        self.open()

    def open(self) -> None:
        self.stream = open(self.file, "rb")
        self.buffer = bytes()
        self.chunks = list()

    def close(self) -> None:
        self.stream.close()

    @property
    def done(self) -> bool:
        return bool(self.peek(1))

    def peek(self, size: int, /) -> bytes:
        if size < self.size:
            return self.stream.peek(1)[:size]
        else:
            lookahead = (self.size // size) + 1
            return self.stream.peek(lookahead)[:size]

    def advance(self) -> bytes:
        """
        Advance n `size` chunks until the delimiter is encountered.
        """
        while self.delimiter not in self.buffer:
            chunk = self.stream.read(self.size)
            if chunk:
                self.buffer += chunk
            else:
                result = self.buffer
                self.buffer = bytes()
                return result
        result, self.buffer = self.buffer.split(self.delimiter, maxsplit=1)
        return result

    def __next__(self) -> dict[str, Any]:
        line = self.advance()
        if line:
            return orjson.loads(line)
        raise StopIteration()

    def __iter__(self) -> Iterator[dict[str, Any]]:
        while True:
            try:
                yield next(self)
            except StopIteration:
                break
