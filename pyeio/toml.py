import toml
from pathlib import Path
from pyeio.base.types import FilePath, PyTOML, SerializedTOML
from pyeio.core import io
from pyeio.base.exceptions import IncorrectFileExtensionError
from pyeio.base import utils


def parse(data: SerializedTOML) -> PyTOML:
    if isinstance(data, bytes):
        # todo.fix: will not always work
        data = str(data.decode())
    if not isinstance(data, str):
        # todo: add details on type error
        raise TypeError()
    toml_data = toml.loads(data)
    return toml_data


def serialize(data: PyTOML) -> str:
    serialized_data = toml.dumps(data)
    return serialized_data


def open(
    path: FilePath,
    validate_file_extension: bool = True,
) -> PyTOML:
    path = Path(path)
    if validate_file_extension:
        utils.run_file_extension_validation(
            module_name="toml",
            path=path,
        )
    serialized_toml = io.open_text(path=path)
    return parse(serialized_toml)


def save(): ...


def load(): ...


def download(): ...
