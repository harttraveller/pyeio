import json
from typing import TypeVar
from pathlib import Path
from pyeio.base import io
from pyeio.base.exceptions import InvalidFileExtensionError

T = TypeVar("T", bound="JSON")
JSON = bool | int | float | str | list[T] | dict[str, T]


def open(
    path: str | Path,
    validate_extension: bool = True,
) -> JSON:
    """
    This function opens a file and reads its content as a JSON object.
    It supports both string paths (to files) and pathlib.Path objects.
    The function will return the parsed JSON data, which can be of type
    bool, int, float, str, list, or dict, depending on the contents of the file.

    Args:
        path (str | Path): The path to the file to be opened and read as a JSON object.

    Returns:
        JSON: Union type of possible JSON data types.
    """
    # todo: add file extension check
    # todo: add file existence check
    return json.loads(io.open_text(path=Path(path)))


def save(
    data: JSON,
    path: str | Path,
    allow_overwrite: bool = False,
    validate_extension: bool = True,
) -> None:
    path = Path(path)
    file_extension = path.name.split(".")[-1]
    if file_extension.lower() != "json":
        raise InvalidFileExtensionError(extension=file_extension, expected="json")
    io.save_text(data=json.dumps(data), path=path, overwrite=allow_overwrite)
