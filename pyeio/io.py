# ruff: noqa

from builtins import open
from pathlib import Path
from typing import AnyStr, Callable, overload

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


def read_string(
    file: str | Path,
    /,
    *,
    encoding: str = "utf-8",
    size: int | None = None,
) -> str:
    """
    Args:
        file (str | Path): The file path.
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
    file: str | Path,
    /,
    *,
    size: int | None = None,
) -> bytes:
    """
    Args:
        file (str | Path): The file path.
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
    file: str | Path,
    returns: type[AnyStr] = str,
    /,
) -> AnyStr:
    """
    Read file content. If str, assumes "utf-8" encoding.

    Args:
        file (str | Path): The file path.
        returns (type[AnyStr]): The type to return.

    Returns:
        AnyStr: The data as [str][] or [bytes][].
    """
    return reader_function[returns](file)


def write_string(
    file: str | Path,
    data: str,
    /,
    *,
    overwrite: bool = False,
    encoding: str = "utf-8",
) -> None:
    with open(
        file=file,
        mode="w" if overwrite else "x",
        encoding=encoding,
        errors=None,
        newline=None,
        closefd=True,
        opener=None,
    ) as f:
        f.write(data)
    f.close()


def write_binary(
    file: str | Path,
    data: bytes,
    /,
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
    file: str | Path,
    data: str | bytes,
    *,
    overwrite: bool = False,
) -> None:
    writer_function[type(data)](file, data, overwrite=overwrite)


def append_string(): ...


def append_binary(): ...


appender_function: dict[type, Callable] = {
    str: append_string,
    bytes: append_binary,
}


def append(): ...


def insert_string(): ...


def insert_binary(): ...


inserter_function: dict[type, Callable] = {
    str: insert_string,
    bytes: insert_binary,
}


def insert(): ...
