import json
from typing import TypeVar
from pathlib import Path
from pyeio.base.types import FilePath, JSON
from pyeio.core import io, web
from pyeio.base.exceptions import InvalidFileExtensionError


# todo.params:
# * validate_file_extension
# * validate_data_structure
# todo.internal:
# * add file existence check
def open(
    path: FilePath,
) -> JSON:
    """
    This function opens a file and reads its content as a JSON object.
    It supports both string paths (to files) and `pathlib.Path` objects.
    The function will return the parsed JSON data, which is typed as a
    union type of possible JSON data types.

    Args:
        path (FilePath): The path to the file to be opened and read as a JSON object.

    Returns:
        JSON: bool | int | float | str | list[JSON] | dict[str, JSON]
    """
    return json.loads(io.open_text(path=Path(path)))


# todo.params:
# allow_file_overwrite: bool = False
# validate_file_extension: bool = True,
def save(
    data: JSON,
    path: FilePath,
) -> None:
    path = Path(path)
    file_extension = path.name.split(".")[-1]
    if file_extension.lower() != "json":
        raise InvalidFileExtensionError(extension=file_extension, expected="json")
    io.save_text(data=json.dumps(data), path=path)


def load(
    url: str,
    chunk_size: int = 1 << 10,
    show_progress: bool = False,
    follow_redirects: bool = True,
    skip_sizecheck: bool = False,
) -> JSON:
    binary_data = web.read_data(
        url, chunk_size, show_progress, follow_redirects, skip_sizecheck
    )
    # todo.fix: need to do character detection and account for when utf-8 fails
    # todo.ext: additionally, do mime detection, data detection, add a bunch of params for exp features
    json_data = json.loads(binary_data.decode("utf-8"))
    return json_data


def download(
    url: str,
    path: FilePath,
    chunk_size: int = 1 << 10,
    show_progress: bool = False,
    follow_redirects: bool = True,
    skip_sizecheck: bool = False,
) -> None:
    json_data = load(url, chunk_size, show_progress, follow_redirects, skip_sizecheck)
    save(json_data, path)
