from pathlib import Path
from typing import Any


def file_name(path: str | Path) -> str:
    "get file name from path"
    return str(path).split("/")[-1]


def file_format(path: str | Path) -> str:
    "get file format from path"
    return file_name(path).split(".")[-1]


def file_size(path: str | Path) -> int:
    "get file size in bytes from path"
    raise NotImplementedError()


def data_type(obj: Any) -> str:
    "get object type as string"
    return str(type(obj)).split("'")[-2]


def read():
    pass
