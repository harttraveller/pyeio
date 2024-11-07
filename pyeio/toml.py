import toml
from pathlib import Path
from pyeio.base.types import FilePath, PyTOML
from pyeio.core import io
from pyeio.base.exceptions import IncorrectFileExtensionError


def open(
    path: FilePath,
    validate_extension: bool = True,
) -> PyTOML:
    """
    This function opens a file and reads its content as a TOML object.
    It supports both string paths (to files) and `pathlib.Path` objects.

    The function will return the parsed TOML data, which is typed as a
    union type of possible TOML data types.

    Args:
        path (str | Path): The path to the file to be opened and read as a JSON object.

    Returns:
        JSON: bool | int | float | str | list[JSON] | dict[str, JSON]
    """
    # todo: add file extension check
    # todo: add file existence check
    return toml.loads(io.open_text(path=Path(path)))


def save(): ...


def load(): ...


def download(): ...
