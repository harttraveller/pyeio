import orjson
from pyeio.core.types import FilePath
from typing import TypeVar, Callable
from urllib.parse import urlparse
from functools import cache

T = TypeVar("T", bound="JSON")
JSON = bool | int | float | str | list[T] | dict[str, T]


def open(path: FilePath) -> JSON: ...


def save(data: JSON, path: FilePath): ...


def load(url: str, cache: bool = False) -> JSON:
    """
    Load some JSON data from the web.

    Args:
        url (str): The URL for the JSON file.
        cache (bool): Whether to cache the data in memory. Defaults to False.

    Returns:
        JSON: JSON data
    """
    ...


# def load(loc: FileLocation) -> JSON:
#     if isinstance(loc, str):
#         parse_result = urlparse(loc)
#         if len(parse_result.scheme):
#             # is url, handle...
#         else:

#         # todo.fix: check to see if url propertly
#         if loc.startswith("http"):
#             ...
#     if isinstance(loc, Path):
#         text: str = io.load_text(loc)
#         data: JSON = orjson.loads(text)
#         return data
#     elif isinstance(loc, str):
#         # do check
#         ...
#     else:
#         raise TypeError(
#             "Resource location must be pathlib.Path or str (file path or URL)."
#         )


# def parse(): ...


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
