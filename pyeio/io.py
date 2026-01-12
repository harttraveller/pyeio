# ruff: noqa

from builtins import open
from io import (
    DEFAULT_BUFFER_SIZE,
    SEEK_CUR,
    SEEK_END,
    SEEK_SET,
    BlockingIOError,
    BufferedIOBase,
    BufferedRandom,
    BufferedReader,
    BufferedRWPair,
    BufferedWriter,
    BytesIO,
    FileIO,
    IncrementalNewlineDecoder,
    IOBase,
    RawIOBase,
    StringIO,
    TextIOBase,
    TextIOWrapper,
    UnsupportedOperation,
    open_code,
    text_encoding,
)
from typing import overload, TypeAlias, TypeVar, Literal, AnyStr
from pathlib import Path

# StrOrBytes: TypeAlias = str | bytes
# T_StrOrBytes = TypeVar("T_StrOrBytes", bound=StrOrBytes)


def read_string(
    file: str | Path,
    encoding: str = "utf-8",
) -> str: ...


def write_string(
    file: str,
    overwrite: bool = False,
    encoding: str = "utf-8",
) -> str: ...


def append_string(file: str | Path, data: str): ...


def insert_string(file: str | Path, data: str, loc: int = 0): ...


def read_binary(file: str | Path) -> bytes: ...


def write_binary() -> bytes: ...


def append_binary(): ...


def insert_binary(): ...


def read(
    file: str | Path,
    returns: type[AnyStr] = str,
    /,
    *,
    encoding: str = "utf-8",
) -> AnyStr: ...


def write(data: str | bytes, overwrite: bool = False, encoding: str = "utf-8"): ...


def append(): ...


def insert(): ...
