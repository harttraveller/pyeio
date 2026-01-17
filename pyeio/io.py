# ruff: noqa

from builtins import open
from pathlib import Path
from typing import AnyStr, Callable

from io import (
    DEFAULT_BUFFER_SIZE,
    BufferedRandom,
    open_code,
    FileIO,
    BytesIO,
    BufferedReader,
    BufferedWriter,
    BufferedRandom,
    BufferedRWPair,
    TextIOWrapper,
    StringIO,
    IncrementalNewlineDecoder,
    text_encoding,
)

# FileDescriptor: TypeAlias = int
# StrOrBytes: TypeAlias = str | bytes
# StrOrBytesOrPath: TypeAlias = StrOrBytes | Path
# FileIn: TypeAlias = FileDescriptor | StrOrBytesOrPath


def read_string(
    file: int | bytes | str | Path,
    /,
    *,
    encoding: str = "utf-8",
    size: int | None = None,
) -> str:
    """
    Args:
        file (int | bytes | str | Path):
            The file path or descriptor.
        encoding (str):
            The encoding to use. Defaults to "utf-8".
        size (int | None):
            The number of characters to read.
            If None or negative, will read to EOF.
            Defaults to None.

    Returns:
        str: The string read from the file or descriptor.
    """
    with open(
        # constant
        mode="r",
        # parameter
        file=file,
        encoding=encoding,
        # later
        buffering=-1,
        errors=None,
        newline=None,  # universal
        closefd=True,
        opener=None,
    ) as f:
        data: str = f.read(size)
    f.close()
    return data


def read_binary(
    file: int | bytes | str | Path,
    /,
    *,
    size: int | None = None,
) -> bytes:
    """
    Args:
        file (int | bytes | str | Path):
            The file path or descriptor.
        size (int | None):
            The number of bytes to read.
            If None or negative, will read to EOF.
            Defaults to None.

    Returns:
        bytes: The bytes read from the file or descriptor.
    """
    with open(
        # constant
        mode="rb",
        # parameter
        file=file,
        # later
        buffering=-1,
        closefd=True,
        opener=None,
    ) as f:
        data: bytes = f.read(size)
    f.close()
    return data


reader_function: dict[type, Callable] = {
    str: read_string,
    bytes: read_binary,
}


def read(
    file: int | bytes | str | Path,
    returns: type[AnyStr] = str,
    /,
) -> AnyStr:
    """
    Args:
        file (int | bytes | str | Path):
            The file path or descriptor.
        returns (type[AnyStr]):
            The type to return.

    Returns:
        AnyStr: The data as [str][] or [bytes][].

    Note that if a string is read, then by default,
    the encoding will be assumed "utf-8". For more
    control over the encoding use [read_string][].
    """
    return reader_function[returns](file)


def write_string(
    file: int | bytes | str | Path,
    /,
    data: str,
    *,
    overwrite: bool = False,
    encoding: str = "utf-8",
) -> str: ...


def write_binary(
    file: int | bytes | str | Path,
    /,
    data: bytes,  # TODO: add memoryview?
    *,
    overwrite: bool = False,
) -> None:
    with open(
        file=file,
        mode="wb" if overwrite else "xb",
        buffering=-1,
        closefd=True,
        opener=None,
    ) as f:
        f.write(data)
    f.close()


writer_function: dict[type, Callable] = {
    str: write_string,
    bytes: write_binary,
}


def write(
    file: int | bytes | str | Path,
    data: str | bytes,
    overwrite: bool = False,
    encoding: str = "utf-8",
): ...


def append_string(
    file: int | bytes | str | Path,
    data: str,
): ...


def insert_string(
    file: int | bytes | str | Path,
    data: str,
    loc: int = 0,
): ...


def append_binary(
    file: int | bytes | str | Path,
): ...


def insert_binary(
    file: int | bytes | str | Path,
): ...


def append(
    file: int | bytes | str | Path,
): ...


def insert(
    file: int | bytes | str | Path,
): ...


class ChunkReader: ...


class LineReader: ...
