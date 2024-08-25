import orjson
from pathlib import Path
from pyeio.data.types import PathLike
from pyeio.core import io
from typing import TypeVar, Callable

T = TypeVar("T", bound="JSON")
JSON = bool | int | float | str | list[T] | dict[str, T]


def load(path: PathLike) -> JSON:
    return orjson.loads(io.load_text(path))


def read(url: str) -> JSON: ...


def save(): ...


def append(): ...


def apply(): ...


def parse(): ...


# todo
# fix issues with file, like encoding or parsing stuff
# def fix(): ...


# apply operation on file to change
# not too useful here, but useful for recursive apply
# def apply(): ...


# def load_recursive(): ...


# def apply_recursive(): ...

# todo: get recursive from webpage or online directory
# webpage: eg - scrape all json links and download to local dir
# dir: eg - s3 bucket, dl all
