import json
from typing import TypeVar, Union
from pathlib import Path
from pyeio.core import io
from pyeio.base.exception import InvalidFileExtensionError

T = TypeVar("T", bound="JSON")
JSON = Union[bool, int, float, str, list[T], dict[str, T]]


def open(
    path: str | Path,
    validate_extension: bool = True,
) -> JSON:
    """
    This function opens a file and reads its content as a JSON object.
    It supports both string paths (to files) and `pathlib.Path` objects.
    The function will return the parsed JSON data, which is typed as a
    union type of possible JSON data types.

    Args:
        path (str | Path): The path to the file to be opened and read as a JSON object.

    Returns:
        JSON: bool | int | float | str | list[JSON] | dict[str, JSON]
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
    """_summary_

    Args:
        data (JSON): _description_
        path (str | Path): _description_
        allow_overwrite (bool, optional): _description_. Defaults to False.
        validate_extension (bool, optional): _description_. Defaults to True.

    Raises:
        InvalidFileExtensionError: _description_
    """
    path = Path(path)
    file_extension = path.name.split(".")[-1]
    if file_extension.lower() != "json":
        raise InvalidFileExtensionError(extension=file_extension, expected="json")
    io.save_text(data=json.dumps(data), path=path, overwrite=allow_overwrite)
