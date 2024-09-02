from pathlib import Path
from typing import TypeVar, Generator
from pyeio.core.exceptions import MissingExtraError
from pyeio.core import io

try:
    import orjson
except ImportError:
    raise MissingExtraError(extra="json")


T = TypeVar("T", bound="JSON")
JSON = bool | int | float | str | list[T] | dict[str, T]


def open(path: str | Path) -> JSON:
    return orjson.loads(io.load_text(path=Path(path)))


def walk(path: str | Path) -> Generator[tuple[str, JSON], None, None]:
    for file in Path(path).glob("**/*.json"):
        yield (str(file.absolute()), open(file))


def save():
    raise NotImplementedError()


def load(data: str | bytes) -> JSON: ...


def dump(data: JSON, indent: int | None = None) -> str:
    raise NotImplementedError()


# from pathlib import Path


# def crawl(): ...


# def get(url: str):
#     raise NotImplementedError()


# def download(url: str, path: str | Path):
#     raise NotImplementedError()


# # # todo: get recursive from webpage or online directory
# # # webpage: eg - scrape all json links and download to local dir
# # # dir: eg - s3 bucket, dl all
