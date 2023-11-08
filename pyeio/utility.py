from pathlib import Path
from typing import Any, Union


def parse_file_name(path: Union[str, Path]) -> str:
    "get file name from path"
    return str(path).split("/")[-1]


def file_format(path: Union[str, Path]) -> str:
    "get file format from path"
    return parse_file_name(path).split(".")[-1]


def file_size(path: Union[str, Path]) -> int:
    "get file size in bytes from path"
    raise NotImplementedError()


def data_type(obj: Any) -> str:
    "get object type as string"
    return str(type(obj)).split("'")[-2]


def read():
    pass
