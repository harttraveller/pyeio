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
from typing import overload, TypeAlias, TypeVar, Literal

StrOrBytes: TypeAlias = str | bytes
T_StrOrBytes = TypeVar("T_StrOrBytes", bound=StrOrBytes)


def read_string() -> str: ...
def read_binary() -> bytes: ...
def write_string() -> str: ...
def write_binary() -> bytes: ...


def read(): ...
def write(): ...
