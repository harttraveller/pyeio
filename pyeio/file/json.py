import orjson
from pathlib import Path
from pyeio.types import FilePath
from pyeio.core.exceptions import InvalidFileExtensionError
from pyeio.core import io
from typing import TypeVar

# from urllib.parse import urlparse
# from functools import cache

T = TypeVar("T", bound="JSON")
JSON = bool | int | float | str | list[T] | dict[str, T]


def open(path: FilePath) -> JSON:
    """
    This function opens a file at the specified path, checks if it has a .json extension,
    reads its contents, and parses it as JSON data.

    Args:
        path (FilePath): The path to the JSON file to be opened and parsed.

    Raises:
        InvalidFileExtensionError: If the file does not have a .json extension.

    Returns:
        JSON: The parsed JSON data as a Python object (dict, list, str, int, float, or bool).
    """
    file_path = Path(path)
    file_extension = file_path.name.split(".")[-1].lower()
    if file_extension != "json":
        raise InvalidFileExtensionError(extension=file_extension, expected="json")
    else:
        text = io.load_text(path=file_path)
        data = orjson.loads(text)
    return data


def save(data: JSON, path: FilePath): ...


def load(url: str, cache: bool = False, force: bool = False) -> JSON:
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
