import json
from pathlib import Path
from typing import TypeVar, Generator, Optional

from pyeio.core import io
from pyeio.core.exceptions import InvalidFileExtensionError

T = TypeVar("T", bound="JSON")
JSON = bool | int | float | str | list[T] | dict[str, T]


def open(path: str | Path) -> JSON:
    return json.loads(io.open_text(path=Path(path)))


def save(data: JSON, path: str | Path, overwrite: bool = False) -> None:
    path = Path(path)
    file_extension = path.name.split(".")[-1]
    if file_extension.lower() != "json":
        raise InvalidFileExtensionError(extension=file_extension, expected="json")
    io.save_text(data=json.dumps(data), path=path, overwrite=overwrite)


# def load(url: str) -> JSON:
#     raise NotImplementedError()


# def download(url: str, path: str | Path):
#     raise NotImplementedError()


# ! unsure

# def parse(data: str | bytes) -> JSON:
#     return orjson.loads(data)


# ingest - ingest and apply handler function at each node/branch of tree
# apply - same diff, except resave file after, either overwriting, or to new file path

# def dump(data: JSON) -> str:
#     return orjson.dumps(data).decode()


# def walk(path: str | Path) -> Generator[tuple[str, JSON], None, None]:
#     for file in Path(path).glob("**/*.json"):
#         yield (str(file.absolute()), load(file))


# # def crawl(): ...
# # # # todo: get recursive from webpage or online directory
# # # # webpage: eg - scrape all json links and download to local dir
# # # # dir: eg - s3 bucket, dl all
