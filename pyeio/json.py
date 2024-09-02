import json as pyjson
from pathlib import Path
from typing import TypeVar, Generator, Optional
from pyeio import text


T = TypeVar("T", bound="JSON")
JSON = bool | int | float | str | list[T] | dict[str, T]


def parse(data: str | bytes) -> JSON:
    return pyjson.loads(data)


def dump(data: JSON) -> str:
    return pyjson.dumps(data)


def load(path: str | Path) -> JSON:
    return parse(text.load(path=Path(path)))


def save():
    raise NotImplementedError()


def walk(path: str | Path) -> Generator[tuple[str, JSON], None, None]:
    for file in Path(path).glob("**/*.json"):
        yield (str(file.absolute()), load(file))


# from pathlib import Path


# def crawl(): ...


# def get(url: str):
#     raise NotImplementedError()


# def download(url: str, path: str | Path):
#     raise NotImplementedError()


# # # todo: get recursive from webpage or online directory
# # # webpage: eg - scrape all json links and download to local dir
# # # dir: eg - s3 bucket, dl all
