# ruff: noqa

# utils
from importlib import import_module
from typing import TYPE_CHECKING

# io
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

# io extras
from pyeio.io import (
    read_string,
    read_binary,
    write_string,
    write_binary,
    append_string,
    append_binary,
    insert_string,
    insert_binary,
    read,
    write,
    append,
    insert,
)

if TYPE_CHECKING:
    # file formats
    from pyeio import json
