import orjson
from pathlib import Path
from pyeio.core.types import ResourceLocation
from pyeio.core import io
from typing import TypeVar, Callable


T = TypeVar("T", bound="JSON")
JSON = bool | int | float | str | list[T] | dict[str, T]


def load(loc: ResourceLocation) -> JSON:
    if isinstance(loc, Path):
        text: str = io.load_text(loc)
        data: JSON = orjson.loads(text)
        return data
    elif isinstance(loc, str):
        # do check
        ...
    else:
        raise TypeError(
            "Resource location must be pathlib.Path or str (file path or URL)."
        )


def save(): ...


def parse(): ...


# def read(loc: str) -> JSON: ...

# def append(): ...


# def apply(): ...


# def parse(): ...


# # todo
# # fix issues with file, like encoding or parsing stuff
# # def fix(): ...


# # apply operation on file to change
# # not too useful here, but useful for recursive apply
# # def apply(): ...


# # def load_recursive(): ...


# # def apply_recursive(): ...

# # todo: get recursive from webpage or online directory
# # webpage: eg - scrape all json links and download to local dir
# # dir: eg - s3 bucket, dl all
