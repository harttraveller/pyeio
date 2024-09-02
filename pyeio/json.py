from pathlib import Path
from typing import TypeVar, Generator
from pyeio.core.exceptions import InvalidFileExtensionError
from pyeio.core import io

try:
    import orjson as _json
except:
    import json as _json


T = TypeVar("T", bound="JSON")
JSON = bool | int | float | str | list[T] | dict[str, T]


# todo: consolidate walk with open via is a directory check
def open(file: str | Path) -> JSON:
    file_path = Path(file)
    file_extension = file_path.name.split(".")[-1].lower()
    if file_extension != "json":
        raise InvalidFileExtensionError(extension=file_extension, expected="json")
    else:
        text = io.load_text(path=file_path)
        data = _json.loads(text)
    return data


def walk(
    path: str | Path,
) -> Generator[tuple[str, JSON], None, None]:
    # todo: is a directory check
    for file in Path(path).glob("**/*.json"):
        yield (str(file.absolute()), open(file))


def save():
    raise NotImplementedError()


def load(data: str | bytes) -> JSON: ...


def dump(data: JSON, indent: int | None = None) -> str:
    raise NotImplementedError()
